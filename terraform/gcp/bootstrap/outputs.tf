output "state_bucket_name" {
  description = "GCS bucket for the main Terraform state."
  value       = google_storage_bucket.terraform_state.name
}

output "backend_init_command" {
  description = "Run this from terraform/gcp after bootstrapping the state bucket."
  value       = "terraform init -backend-config=\"bucket=${google_storage_bucket.terraform_state.name}\" -backend-config=\"prefix=dairyfarm/gcp\""
}
