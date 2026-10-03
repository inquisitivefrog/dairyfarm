resource "google_artifact_registry_repository" "images" {
  location      = var.gcp_region
  repository_id = "${var.project_name}-images"
  description   = "DairyFarm API and UI container images"
  format        = "DOCKER"

  cleanup_policies {
    id     = "keep-recent"
    action = "KEEP"
    most_recent_versions {
      keep_count = 5
    }
  }

  cleanup_policy_dry_run = false

  depends_on = [google_project_service.required]
}
