resource "aws_ecs_cluster" "main" {
    name = "ticket-cluster"
}

resource "aws_iam_role_policy_attachment" "ecs_task_logs" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


resource "aws_iam_role_policy_attachment" "ecr_access" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}


resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}




resource "aws_ecs_task_definition" "service" {
  for_each                 = local.services
  family                   = each.value.family
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory

  container_definitions = jsonencode([{
    name  = each.value.container_name
    image = each.value.image
    portMappings = [{
      containerPort = each.value.port
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = "/ecs/cb-app"
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = each.key
      }
    }
    essential = true
  }])

  depends_on = [aws_cloudwatch_log_group.ecs]
}



resource "aws_ecs_service" "service" {
  for_each       = local.services
  name           = "${each.key}-service"
  cluster        = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.service[each.key].arn
  desired_count  = 2
  launch_type    = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.private[*].id
    assign_public_ip = false
  }

load_balancer {
  target_group_arn = aws_alb_target_group.service[each.key].arn
  container_name   = each.value.container_name
  container_port   = each.value.port
}

  depends_on = [
  aws_alb_listener.front_end,
  aws_iam_role_policy_attachment.ecs_task_logs,
  aws_iam_role_policy_attachment.ecr_access
]

}
