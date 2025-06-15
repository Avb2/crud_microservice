resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/cb-app"
  retention_in_days = 7
}
