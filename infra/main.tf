# --- 1. Terraform Base & Provider Setup ---
terraform {
  required_version = ">= 1.5.0" # Supports modern import blocks and security syntax
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# --- 2. Amazon ECR Container Registry ---
resource "aws_ecr_repository" "agent_platform_repo" {
  name                 = "langgraph-multi-agent-platform"
  image_tag_mutability = "MUTABLE"
  force_destroy        = true # Crucial for zero-cost 'terraform destroy'! Wipes images cleanly.

  image_scanning_configuration {
    scan_on_push = true
  }
}

# --- 3. IAM Execution Security Role ---
resource "aws_iam_role" "agentcore_execution_role" {
  name = "langgraph-agentcore-platform-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })
}

# Explicit policy granting secure permissions to call Bedrock models and pull images from ECR
resource "aws_iam_role_policy" "agentcore_platform_policy" {
  name = "langgraph-agentcore-platform-policy"
  role = aws_iam_role.agentcore_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream" # Used for real-time text token streaming
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
        Resource = aws_ecr_repository.agent_platform_repo.arn
      }
    ]
  })
}

# --- 4. Amazon Bedrock AgentCore Runtime Resource Configuration ---
resource "aws_bedrockagentcore_agent_runtime" "platform_runtime" {
  name        = "langgraph-multi-agent-runtime"
  description = "Serverless execution runtime for hosting dynamic multi-agent LangGraph platform layers."
  role_arn    = aws_iam_role.agentcore_execution_role.arn

  # Define the serverless custom container environment settings
  container_configuration {
    # Targets the exact ARM64 image pushed to ECR (Bedrock AgentCore runs on high-performance AWS Graviton chips)
    container_uri = "${aws_ecr_repository.agent_platform_repo.repository_url}:latest"

    # 🔐 ENVIRONMENT VARIABLES INJECTION (Safely passes non-hardcoded configs into Python)
    environment_variables = {
      SENDER_EMAIL       = var.sender_email
      GMAIL_APP_PASSWORD = var.gmail_app_password
      SMTP_SERVER        = var.smtp_server
      SMTP_PORT          = var.smtp_port
      AWS_REGION         = var.aws_region
    }
  }
}

# --- 5. Provision the Secure Invocation Endpoint interface ---
resource "aws_bedrockagentcore_agent_runtime_endpoint" "platform_endpoint" {
  name             = "platform-public-gateway"
  agent_runtime_id = aws_bedrockagentcore_agent_runtime.platform_runtime.id
}
