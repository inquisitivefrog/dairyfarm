variable "gcp_project_id" {
  description = "Dedicated GCP project ID for the DairyFarm demo."
  type        = string
}

variable "gcp_region" {
  description = "Region for the Terraform state bucket."
  type        = string
  default     = "us-central1"
}

variable "project_name" {
  description = "Prefix used for the globally unique Terraform state bucket name."
  type        = string
  default     = "dairyfarm-demo"
}
