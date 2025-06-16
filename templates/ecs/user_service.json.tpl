{
  "family": "user-service-family",
  "containerDefinitions": [
    {
      "name": "user_service",
      "image": "${user_image}",
      "portMappings": [
        {
          "containerPort": ${user_port},
          "hostPort": ${user_port}
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