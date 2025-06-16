{
  "family": "ticket-service-family",
  "containerDefinitions": [
    {
      "name": "ticket_service",
      "image": "${ticket_image}",
      "portMappings": [
        {
          "containerPort": ${ticket_port},
          "hostPort": ${ticket_port}
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