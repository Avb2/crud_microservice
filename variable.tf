variable "aws_region" {
    description = "us-east-2"
}

variable "az_count" {
    default = "2"
}


variable "app_port" {
    default = 80
}

variable "health_check_path" {
  default = "/health"
}


variable "auth_image" {
    default = "public.ecr.aws/i4n6p6k3/eventapi/auth:v8"
}

variable "auth_port" {
    default = 5000
}

variable "user_image" {
    default = "public.ecr.aws/i4n6p6k3/eventapi/user:v6"
}

variable "user_port" {
    default = 5001
}

variable "event_image" {
    default = "public.ecr.aws/i4n6p6k3/eventapi/events:v5"
}

variable "event_port" {
    default = 5002
}

variable "ticket_image" {
    default = "public.ecr.aws/i4n6p6k3/eventapi/tickets:v5"
}

variable "ticket_port" {
    default = 5003
}


variable "fargate_cpu" {
    default = "1024"
}

variable "fargate_memory" {
    default = "2048"
}