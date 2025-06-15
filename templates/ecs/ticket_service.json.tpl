{
  "family": "ticket-service-family",
  "containerDefinitions": [
    {
      "name": "ticket_service",
      "image": "${app_image}",
      "portMappings": [
        {
          "containerPort": ${app_port},
          "hostPort": ${app_port}
        }
      ],
      "essential": true
    }
  ],
  "cpu": "${fargate_cpu}",
  "memory": "${fargate_memory}",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"]
}