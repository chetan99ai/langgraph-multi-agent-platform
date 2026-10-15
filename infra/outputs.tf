output "ecr_repository_url" {
  description = "The absolute tracking URL of your Amazon ECR Repository. Pass this to GitHub Actions to tag and push Docker images."
  value       = aws_ecr_repository.agent_platform_repo.repository_url
}

output "agent_runtime_id" {
  description = "The serverless runtime identification string assigned by Bedrock. Required for routing your Postman and CI/CD CLI commands."
  value       = aws_bedrockagentcore_agent_runtime.platform_runtime.id
}

output "agent_runtime_endpoint" {
  description = "The public target gateway URL endpoint where your React SSR application or Postman client transmits chat prompt payloads."
  value       = aws_bedrockagentcore_agent_runtime_endpoint.platform_endpoint.endpoint_url
}
