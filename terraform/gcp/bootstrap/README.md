# Terraform state bucket bootstrap

This small one-time Terraform configuration creates a private, versioned GCS
bucket for the main DairyFarm Terraform state. It intentionally uses local
state because it creates the bucket needed by the main configuration's GCS
backend.

From this directory, authenticate with Google Application Default Credentials,
copy `terraform.tfvars.example` to `terraform.tfvars`, set the dedicated GCP
project ID, then run:

```sh
terraform init
terraform plan
terraform apply
```

Review the plan before applying. The bucket blocks public access, uses uniform
bucket-level IAM, retains object versions, and has `prevent_destroy`.

After applying, copy the `backend_init_command` output and run it from
`terraform/gcp`. Do not commit either Terraform state file. The main state
contains generated secret values and must remain accessible only to trusted
project operators.

The bootstrap state remains local. Back it up securely; it contains only the
state bucket resource metadata. Do not delete the bucket until the main state
and all resources it manages have been deliberately retired.
