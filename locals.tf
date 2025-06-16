locals {
  services = {
    auth = {
      family         = "auth-service-family"
      image          = var.auth_image
      port           = var.auth_port
      container_name = "auth-service"
      template_file  = local.auth_task_def
    }
    user = {
      family         = "user-service-family"
      image          = var.user_image
      port           = var.user_port
      container_name = "user-service"
      template_file  = local.user_task_def
    }
    event = {
      family         = "event-service-family"
      image          = var.event_image
      port           = var.event_port
      container_name = "event-service"
      template_file  = local.event_task_def
    }
    ticket = {
      family         = "ticket-service-family"
      image          = var.ticket_image
      port           = var.ticket_port
      container_name = "ticket-service"
      template_file  = local.ticket_task_def
    }
  }

  alb_paths = {
    auth   = "/auth/*"
    user   = "/user/*"
    event  = "/event/*"
    ticket = "/ticket/*"
  }

  scale_config = {
    min_capacity          = 2
    max_capacity          = 3
    scale_up_threshold    = 85
    scale_down_threshold  = 10
  }

  auth_task_def = templatefile("${path.module}/templates/ecs/auth_service.json.tpl", {
  auth_image      = var.auth_image
  auth_port       = var.auth_port
  fargate_cpu    = var.fargate_cpu
  fargate_memory = var.fargate_memory
})

user_task_def = templatefile("${path.module}/templates/ecs/user_service.json.tpl", {
  user_image      = var.user_image
  user_port       = var.user_port
  fargate_cpu    = var.fargate_cpu
  fargate_memory = var.fargate_memory
})

ticket_task_def = templatefile("${path.module}/templates/ecs/ticket_service.json.tpl", {
  ticket_image      = var.ticket_image
  ticket_port       = var.ticket_port
  fargate_cpu    = var.fargate_cpu
  fargate_memory = var.fargate_memory
})

event_task_def = templatefile("${path.module}/templates/ecs/event_service.json.tpl", {
  event_image      = var.event_image
  event_port       = var.event_port
  fargate_cpu    = var.fargate_cpu
  fargate_memory = var.fargate_memory
})

}
