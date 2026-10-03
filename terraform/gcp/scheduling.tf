resource "google_service_account" "sql_scheduler" {
  account_id   = "${var.project_name}-sql-scheduler"
  display_name = "DairyFarm Cloud SQL schedule controller"
}

resource "google_project_iam_custom_role" "sql_scheduler" {
  role_id     = "dairyfarmDemoSqlScheduler"
  title       = "DairyFarm Cloud SQL scheduler"
  description = "Allows scheduled Cloud SQL start and stop for the DairyFarm demo."
  permissions = [
    "cloudsql.instances.get",
    "cloudsql.instances.update",
  ]
}

resource "google_project_iam_member" "sql_scheduler" {
  project = var.gcp_project_id
  role    = google_project_iam_custom_role.sql_scheduler.name
  member  = "serviceAccount:${google_service_account.sql_scheduler.email}"

  condition {
    title       = "Only DairyFarm Cloud SQL instance"
    description = "Limits the scheduler identity to starting and stopping the DairyFarm database."
    expression  = "resource.name == \"projects/${var.gcp_project_id}/instances/${google_sql_database_instance.main.name}\""
  }
}

resource "google_cloud_scheduler_job" "sql_start" {
  name             = "${var.project_name}-sql-start"
  description      = "Start Cloud SQL before the DairyFarm demo availability window."
  region           = var.gcp_region
  schedule         = "30 4 * * *"
  time_zone        = "America/Los_Angeles"
  attempt_deadline = "320s"

  http_target {
    http_method = "PATCH"
    uri = format(
      "https://sqladmin.googleapis.com/sql/v1beta4/projects/%s/instances/%s?updateMask=settings.activationPolicy",
      var.gcp_project_id,
      google_sql_database_instance.main.name,
    )
    body = base64encode(jsonencode({
      settings = {
        activationPolicy = "ALWAYS"
      }
    }))

    oauth_token {
      service_account_email = google_service_account.sql_scheduler.email
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }

  depends_on = [
    google_project_iam_member.sql_scheduler,
    google_project_service.required,
  ]
}

resource "google_cloud_scheduler_job" "sql_stop" {
  name             = "${var.project_name}-sql-stop"
  description      = "Stop Cloud SQL at the end of the DairyFarm demo availability window."
  region           = var.gcp_region
  schedule         = "0 18 * * *"
  time_zone        = "America/Los_Angeles"
  attempt_deadline = "320s"

  http_target {
    http_method = "PATCH"
    uri = format(
      "https://sqladmin.googleapis.com/sql/v1beta4/projects/%s/instances/%s?updateMask=settings.activationPolicy",
      var.gcp_project_id,
      google_sql_database_instance.main.name,
    )
    body = base64encode(jsonencode({
      settings = {
        activationPolicy = "NEVER"
      }
    }))

    oauth_token {
      service_account_email = google_service_account.sql_scheduler.email
      scope                 = "https://www.googleapis.com/auth/cloud-platform"
    }
  }

  depends_on = [
    google_project_iam_member.sql_scheduler,
    google_project_service.required,
  ]
}
