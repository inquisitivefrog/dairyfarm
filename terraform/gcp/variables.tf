variable "gcp_project_id" {
  description = "Dedicated GCP project ID for the DairyFarm demo."
  type        = string
}

variable "gcp_region" {
  description = "Region for Cloud Run, Artifact Registry, and Cloud SQL."
  type        = string
  default     = "us-central1"
}

variable "project_name" {
  description = "Short prefix used to name DairyFarm resources in this project."
  type        = string
  default     = "dairyfarm-demo"
}

variable "db_tier" {
  description = "Cloud SQL tier; db-f1-micro minimizes fixed cost and is intended for a demo, not production workloads."
  type        = string
  default     = "db-f1-micro"
}

variable "db_disk_size_gb" {
  description = "Initial Cloud SQL disk allocation."
  type        = number
  default     = 10
}

variable "database_deletion_protection" {
  description = "Keep Cloud SQL deletion protection enabled unless deliberately preparing to destroy the demo environment."
  type        = bool
  default     = true
}

variable "image_tag" {
  description = "Image tag deployed to Cloud Run. The production pipeline updates the stable production tag; Cloud Run revisions retain their resolved image digest."
  type        = string
  default     = "production"
}

variable "deploy_workloads" {
  description = "Create Cloud Run services and the private migration/seed job after images have been pushed."
  type        = bool
  default     = false
}

variable "public_access" {
  description = "Allow unauthenticated invocation of the UI and read-only API. Keep false until the migration/seed job succeeds."
  type        = bool
  default     = false
}

variable "api_max_instances" {
  description = "Maximum Cloud Run API instances to cap demo scaling and cost."
  type        = number
  default     = 2
}

variable "ui_max_instances" {
  description = "Maximum Cloud Run UI instances to cap demo scaling and cost."
  type        = number
  default     = 2
}

variable "github_repository" {
  description = "GitHub owner/repository allowed to deploy through Workload Identity Federation."
  type        = string
  default     = "inquisitivefrog/dairyfarm"
}

variable "github_deploy_branch" {
  description = "Only this Git branch may impersonate the deployment service account."
  type        = string
  default     = "ai-assisted"
}
