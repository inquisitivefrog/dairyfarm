resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "${var.project_name}-github"
  display_name              = "DairyFarm GitHub Actions"
  description               = "Keyless deployments from the configured GitHub branch."
  disabled                  = false
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name                       = "DairyFarm GitHub OIDC"
  description                        = "OIDC trust restricted to the DairyFarm deploy branch."

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "assertion.repository == '${var.github_repository}' && assertion.ref == 'refs/heads/${var.github_deploy_branch}'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

resource "google_service_account" "github_deployer" {
  account_id   = "${var.project_name}-github-deployer"
  display_name = "DairyFarm GitHub Actions deployer"
}

resource "google_service_account_iam_member" "github_deployer" {
  service_account_id = google_service_account.github_deployer.name
  role               = "roles/iam.workloadIdentityUser"
  member = format(
    "principalSet://iam.googleapis.com/%s/attribute.repository/%s",
    google_iam_workload_identity_pool.github.name,
    var.github_repository,
  )
}

resource "google_project_iam_custom_role" "github_run_deployer" {
  role_id     = "dairyfarmDemoRunDeployer"
  title       = "DairyFarm Cloud Run deployer"
  description = "Allows GitHub Actions to update DairyFarm Cloud Run services and jobs."
  permissions = [
    "run.jobs.get",
    "run.jobs.run",
    "run.jobs.update",
    "run.operations.get",
    "run.services.get",
    "run.services.update",
  ]
}

resource "google_project_iam_member" "github_run_deployer" {
  project = var.gcp_project_id
  role    = google_project_iam_custom_role.github_run_deployer.name
  member  = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_project_iam_member" "github_service_usage" {
  project = var.gcp_project_id
  role    = "roles/serviceusage.serviceUsageConsumer"
  member  = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_artifact_registry_repository_iam_member" "github_writer" {
  project    = var.gcp_project_id
  location   = google_artifact_registry_repository.images.location
  repository = google_artifact_registry_repository.images.repository_id
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_service_account_iam_member" "github_act_as_runtime" {
  service_account_id = google_service_account.runtime.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github_deployer.email}"
}

resource "google_service_account_iam_member" "github_act_as_ui" {
  service_account_id = google_service_account.ui.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github_deployer.email}"
}
