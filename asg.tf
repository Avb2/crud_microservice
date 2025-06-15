resource "aws_appautoscaling_target" "target" {
  for_each             = local.services
  service_namespace    = "ecs"
  resource_id          = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.service[each.key].name}"
  scalable_dimension   = "ecs:service:DesiredCount"
  min_capacity         = local.scale_config.min_capacity
  max_capacity         = local.scale_config.max_capacity
}

resource "aws_appautoscaling_policy" "scale_up" {
  for_each             = local.services
  name                 = "${each.key}-scale-up"
  service_namespace    = "ecs"
  resource_id          = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.service[each.key].name}"
  scalable_dimension   = "ecs:service:DesiredCount"

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 60
    metric_aggregation_type = "Maximum"

    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = 1
    }
  }

  depends_on = [aws_appautoscaling_target.target]
}

resource "aws_appautoscaling_policy" "scale_down" {
  for_each             = local.services
  name                 = "${each.key}-scale-down"
  service_namespace    = "ecs"
  resource_id          = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.service[each.key].name}"
  scalable_dimension   = "ecs:service:DesiredCount"

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 60
    metric_aggregation_type = "Maximum"

    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = -1
    }
  }

  depends_on = [aws_appautoscaling_target.target]
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  for_each             = local.services
  alarm_name           = "${each.key}-high-cpu"
  comparison_operator  = "GreaterThanOrEqualToThreshold"
  evaluation_periods   = 2
  metric_name          = "CPUUtilization"
  namespace            = "AWS/ECS"
  period               = 60
  statistic            = "Average"
  threshold            = local.scale_config.scale_up_threshold

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.service[each.key].name
  }

  alarm_actions = [aws_appautoscaling_policy.scale_up[each.key].arn]
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  for_each             = local.services
  alarm_name           = "${each.key}-low-cpu"
  comparison_operator  = "LessThanOrEqualToThreshold"
  evaluation_periods   = 2
  metric_name          = "CPUUtilization"
  namespace            = "AWS/ECS"
  period               = 60
  statistic            = "Average"
  threshold            = local.scale_config.scale_down_threshold

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = aws_ecs_service.service[each.key].name
  }

  alarm_actions = [aws_appautoscaling_policy.scale_down[each.key].arn]
}
