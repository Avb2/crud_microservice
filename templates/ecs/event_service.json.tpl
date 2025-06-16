{
  "family": "event-service-family",
  "containerDefinitions": [
    {
      "name": "event_service",
      "image": "${event_image}",
      "portMappings": [
        {
          "containerPort": ${event_port},
          "hostPort": ${event_port}
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