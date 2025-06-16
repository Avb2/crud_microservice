{
  "family": "auth-service-family",
  "containerDefinitions": [
    {
      "name": "auth_service",
      "image": "${auth_image}",
      "portMappings": [
        {
          "containerPort": ${auth_port},
          "hostPort": ${auth_port}
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