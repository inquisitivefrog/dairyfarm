resource "google_service_account" "runtime" {
  account_id   = "${var.project_name}-runtime"
  display_name = "DairyFarm Cloud Run runtime"
}

resource "google_service_account" "ui" {
  account_id   = "${var.project_name}-ui"
  display_name = "DairyFarm Cloud Run UI"
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.gcp_project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.runtime.email}"
}
