variable "subscription_id" {
  description = "Azure subscription ID. Set locally via terraform.tfvars or ARM_SUBSCRIPTION_ID environment variable."
  type        = string
  default     = null
  nullable    = true
}

variable "location" {
  description = "Azure region for the resources."
  type        = string
  default     = "Central India"
}

variable "project_name" {
  description = "Short project prefix used in Azure resource names."
  type        = string
  default     = "carepoint-demo"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "dev"
}

variable "app_service_sku" {
  description = "App Service Plan SKU. Review current Azure pricing before applying."
  type        = string
  default     = "B1"
}
