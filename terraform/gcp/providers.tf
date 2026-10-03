provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region

  default_labels = {
    application = "dairyfarm-demo"
    managed_by  = "terraform"
  }
}
