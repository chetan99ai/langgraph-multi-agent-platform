variable "aws_region" {
  type        = string
  description = "The target AWS deployment region where your multi-agent architecture will run."
  default     = "us-east-1"
}

variable "bedrock_model_id" {
  type        = string
  description = "The specific Foundational Language Model utilized by the platform routing engines."
  default     = "anthropic.claude-3-5-sonnet-v2:0"
}

# --- Dynamic Email Configuration Injections (Passed directly to AgentCore Container) ---

variable "sender_email" {
  type        = string
  description = "The authorized SMTP email address used to dispatch messages (e.g. chetan99ai@gmail.com)."
}

variable "gmail_app_password" {
  type        = string
  description = "The secure provider application passkey used to bypass traditional multifactor challenges."
  sensitive   = true # Ensures Terraform automatically masks this token string inside terminal logs
}

variable "smtp_server" {
  type        = string
  description = "The target outbound relay server endpoint address (e.g. ://gmail.com)."
  default     = "://gmail.com"
}

variable "smtp_port" {
  type        = string
  description = "The explicit connection interface routing port utilized by the SMTP protocol."
  default     = "587"
}
