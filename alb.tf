
resource "aws_alb" "main" {
    name = "cb-load-balancer"
    subnets = aws_subnet.public.*.id
    security_groups = [aws_security_group.lb.id]
}




#### Target Groups


resource "aws_alb_target_group" "service" {
  for_each = local.services

  name        = "${each.key}-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    healthy_threshold   = 3
    interval            = 30
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = 3
    path                = var.health_check_path
    unhealthy_threshold = 2
  }
}


### Listener

resource "aws_alb_listener" "front_end" {
  load_balancer_arn = aws_alb.main.id
  port              = var.app_port
  protocol          = "HTTP"

  default_action {
      target_group_arn = aws_alb_target_group.service["user"].arn
      type             = "forward"
  }
}




#### Path rules
resource "aws_alb_listener_rule" "routes" {
  for_each     = local.alb_paths
  listener_arn = aws_alb_listener.front_end.arn
  priority     = lookup({auth=10, user=20, ticket=30, event=40}, each.key, 50)

  action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.service[each.key].arn
  }

  condition {
    path_pattern {
      values = [each.value]
    }
  }
}





