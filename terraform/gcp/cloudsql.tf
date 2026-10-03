resource "google_sql_database_instance" "main" {
  name                = "${var.project_name}-postgres"
  region              = var.gcp_region
  database_version    = "POSTGRES_15"
  deletion_protection = var.database_deletion_protection

  settings {
    edition           = "ENTERPRISE"
    tier              = var.db_tier
    disk_type         = "PD_SSD"
    disk_size         = var.db_disk_size_gb
    availability_type = "ZONAL"
    activation_policy = "ALWAYS"

    ip_configuration {
      ipv4_enabled = true
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = false
      backup_retention_settings {
        retained_backups = 1
        retention_unit   = "COUNT"
      }
    }
  }

  lifecycle {
    ignore_changes = [settings[0].activation_policy]
  }

  depends_on = [google_project_service.required]
}

resource "google_sql_database" "main" {
  name     = "dairyfarm"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = "dairyfarm"
  instance = google_sql_database_instance.main.name
  password = random_password.database_password.result
}
