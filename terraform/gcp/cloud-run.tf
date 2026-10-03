locals {
  image_root    = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.images.repository_id}"
  api_image     = "${local.image_root}/api:${var.image_tag}"
  ui_image      = "${local.image_root}/ui:${var.image_tag}"
  api_host      = ".run.app"
  database_host = "/cloudsql/${google_sql_database_instance.main.connection_name}"
}

resource "google_cloud_run_v2_job" "initialize_database" {
  count    = var.deploy_workloads ? 1 : 0
  name     = "${var.project_name}-initialize"
  location = var.gcp_region

  template {
    template {
      service_account = google_service_account.runtime.email
      timeout         = "900s"
      max_retries     = 0

      containers {
        image   = local.api_image
        command = ["/bin/sh"]
        args    = ["-c", "python manage.py migrate && python manage.py load_ai_assisted_dataset"]

        env {
          name  = "DJANGO_ENVIRONMENT"
          value = "production"
        }
        env {
          name  = "DJANGO_DEBUG"
          value = "false"
        }
        env {
          name  = "DJANGO_PUBLIC_DEMO_READ_ONLY"
          value = "true"
        }
        env {
          name  = "DJANGO_DB_ENGINE"
          value = "django.db.backends.postgresql"
        }
        env {
          name  = "DJANGO_DB_NAME"
          value = google_sql_database.main.name
        }
        env {
          name  = "DJANGO_DB_USER"
          value = google_sql_user.app.name
        }
        env {
          name  = "DJANGO_DB_HOST"
          value = local.database_host
        }
        env {
          name  = "DJANGO_DB_PORT"
          value = "5432"
        }
        env {
          name = "DJANGO_SECRET_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.django_secret_key.secret_id
              version = "latest"
            }
          }
        }
        env {
          name = "DJANGO_DB_PASSWORD"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.database_password.secret_id
              version = "latest"
            }
          }
        }

        volume_mounts {
          name       = "cloudsql"
          mount_path = "/cloudsql"
        }
      }

      volumes {
        name = "cloudsql"
        cloud_sql_instance {
          instances = [google_sql_database_instance.main.connection_name]
        }
      }
    }
  }

  depends_on = [
    google_project_iam_member.cloud_sql_client,
    google_secret_manager_secret_iam_member.database_password,
    google_secret_manager_secret_iam_member.django_secret_key,
    google_sql_database.main,
    google_sql_user.app,
  ]
}

resource "google_cloud_run_v2_service" "api" {
  count    = var.deploy_workloads ? 1 : 0
  name     = "${var.project_name}-api"
  location = var.gcp_region

  template {
    service_account = google_service_account.runtime.email
    timeout         = "60s"
    scaling {
      min_instance_count = 0
      max_instance_count = var.api_max_instances
    }

    containers {
      image   = local.api_image
      command = ["gunicorn"]
      args = [
        "demo.wsgi:application",
        "--bind",
        "0.0.0.0:8080",
        "--access-logfile",
        "-",
        "--error-logfile",
        "-",
      ]

      ports {
        container_port = 8080
      }

      env {
        name  = "DJANGO_ENVIRONMENT"
        value = "production"
      }
      env {
        name  = "DJANGO_DEBUG"
        value = "false"
      }
      env {
        name  = "DJANGO_TRUST_X_FORWARDED_PROTO"
        value = "true"
      }
      env {
        name  = "DJANGO_PUBLIC_DEMO_READ_ONLY"
        value = "true"
      }
      env {
        name  = "DJANGO_ALLOWED_HOSTS"
        value = local.api_host
      }
      env {
        name  = "DJANGO_CSRF_TRUSTED_ORIGINS"
        value = "https://*.run.app"
      }
      env {
        name  = "DJANGO_SECURE_SSL_REDIRECT"
        value = "true"
      }
      env {
        name  = "DJANGO_SESSION_COOKIE_SECURE"
        value = "true"
      }
      env {
        name  = "DJANGO_CSRF_COOKIE_SECURE"
        value = "true"
      }
      env {
        name  = "DJANGO_HSTS_SECONDS"
        value = "86400"
      }
      env {
        name  = "DJANGO_DB_ENGINE"
        value = "django.db.backends.postgresql"
      }
      env {
        name  = "DJANGO_DB_NAME"
        value = google_sql_database.main.name
      }
      env {
        name  = "DJANGO_DB_USER"
        value = google_sql_user.app.name
      }
      env {
        name  = "DJANGO_DB_HOST"
        value = local.database_host
      }
      env {
        name  = "DJANGO_DB_PORT"
        value = "5432"
      }
      env {
        name = "DJANGO_SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.django_secret_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "DJANGO_DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.database_password.secret_id
            version = "latest"
          }
        }
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.main.connection_name]
      }
    }
  }

  depends_on = [
    google_project_iam_member.cloud_sql_client,
    google_secret_manager_secret_iam_member.database_password,
    google_secret_manager_secret_iam_member.django_secret_key,
    google_sql_database.main,
    google_sql_user.app,
  ]
}

resource "google_cloud_run_v2_service" "ui" {
  count    = var.deploy_workloads ? 1 : 0
  name     = "${var.project_name}-ui"
  location = var.gcp_region

  template {
    service_account = google_service_account.ui.email
    timeout         = "60s"
    scaling {
      min_instance_count = 0
      max_instance_count = var.ui_max_instances
    }

    containers {
      image = local.ui_image
      ports {
        container_port = 8080
      }
      env {
        name  = "API_ORIGIN"
        value = google_cloud_run_v2_service.api[0].uri
      }
      env {
        name  = "NGINX_ENVSUBST_FILTER"
        value = "^(PORT|API_ORIGIN)$"
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "api_public" {
  count    = var.deploy_workloads && var.public_access ? 1 : 0
  project  = var.gcp_project_id
  location = google_cloud_run_v2_service.api[0].location
  name     = google_cloud_run_v2_service.api[0].name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service_iam_member" "ui_public" {
  count    = var.deploy_workloads && var.public_access ? 1 : 0
  project  = var.gcp_project_id
  location = google_cloud_run_v2_service.ui[0].location
  name     = google_cloud_run_v2_service.ui[0].name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
