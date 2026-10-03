locals {
  bucket_name = "${var.project_name}-tfstate-${var.gcp_project_id}"
}

resource "google_storage_bucket" "terraform_state" {
  name                        = local.bucket_name
  location                    = upper(var.gcp_region)
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}
