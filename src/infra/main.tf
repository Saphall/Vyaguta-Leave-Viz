# Terraform required version and provider setup
terraform {
  required_providers {
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "~> 1.10.0"
    }
  }
  required_version = ">= 1.0.0"
}
