output "gcp_project_id" {
  description = "GCP project managed by this Terraform configuration."
  value       = var.gcp_project_id
}

output "gcp_region" {
  description = "Deployment region."
  value       = var.gcp_region
}

output "project_name" {
  description = "Resource name prefix."
  value       = var.project_name
}

output "artifact_registry_repository" {
  description = "Regional Artifact Registry path for the two container images."
  value       = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.images.repository_id}"
}

output "api_service_url" {
  description = "Cloud Run API URL; present after deploy_workloads=true."
  value       = try(google_cloud_run_v2_service.api[0].uri, null)
}

output "ui_service_url" {
  description = "Public demo URL after public_access=true."
  value       = try(google_cloud_run_v2_service.ui[0].uri, null)
}

output "database_connection_name" {
  description = "Cloud SQL connection name used by the Cloud Run connector."
  value       = google_sql_database_instance.main.connection_name
}

output "initialization_job_name" {
  description = "Cloud Run job that applies migrations and loads the reviewed synthetic dataset."
  value       = try(google_cloud_run_v2_job.initialize_database[0].name, null)
}

output "github_workload_identity_provider" {
  description = "Provider resource name to set as the GCP_WIF_PROVIDER GitHub Actions variable."
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "github_deployer_service_account" {
  description = "Service account email to set as the GCP_DEPLOY_SERVICE_ACCOUNT GitHub Actions variable."
  value       = google_service_account.github_deployer.email
}
