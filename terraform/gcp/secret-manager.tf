resource "random_password" "django_secret_key" {
  length  = 64
  special = false
}

resource "random_password" "database_password" {
  length  = 48
  special = false
}

resource "google_secret_manager_secret" "django_secret_key" {
  secret_id = "${var.project_name}-django-secret-key"

  replication {
    auto {}
  }

  depends_on = [google_project_service.required]
}

resource "google_secret_manager_secret_version" "django_secret_key" {
  secret      = google_secret_manager_secret.django_secret_key.id
  secret_data = random_password.django_secret_key.result
}

resource "google_secret_manager_secret" "database_password" {
  secret_id = "${var.project_name}-database-password"

  replication {
    auto {}
  }

  depends_on = [google_project_service.required]
}

resource "google_secret_manager_secret_version" "database_password" {
  secret      = google_secret_manager_secret.database_password.id
  secret_data = random_password.database_password.result
}

resource "google_secret_manager_secret_iam_member" "django_secret_key" {
  project   = var.gcp_project_id
  secret_id = google_secret_manager_secret.django_secret_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}

resource "google_secret_manager_secret_iam_member" "database_password" {
  project   = var.gcp_project_id
  secret_id = google_secret_manager_secret.database_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.runtime.email}"
}
