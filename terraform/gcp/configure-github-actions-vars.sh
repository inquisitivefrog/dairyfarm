#!/usr/bin/env bash
# Populate the GitHub repository variables required by the GCP deploy workflow.
set -euo pipefail

TF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY="${1:-inquisitivefrog/dairyfarm}"

command -v gh >/dev/null || {
  echo "GitHub CLI (gh) is required." >&2
  exit 1
}
command -v terraform >/dev/null || {
  echo "Terraform is required." >&2
  exit 1
}
gh auth status >/dev/null 2>&1 || {
  echo "Authenticate the GitHub CLI first with 'gh auth login'." >&2
  exit 1
}

terraform_output() {
  local value
  value="$(terraform -chdir="$TF_DIR" output -raw "$1")"
  if [[ -z "$value" || "$value" == *$'\n'* ]]; then
    echo "Terraform output '$1' is empty or invalid." >&2
    exit 1
  fi
  printf '%s' "$value"
}

gh variable set GCP_PROJECT_ID --repo "$REPOSITORY" \
  --body "$(terraform_output gcp_project_id)"
gh variable set GCP_WIF_PROVIDER --repo "$REPOSITORY" \
  --body "$(terraform_output github_workload_identity_provider)"
gh variable set GCP_DEPLOY_SERVICE_ACCOUNT --repo "$REPOSITORY" \
  --body "$(terraform_output github_deployer_service_account)"
gh variable set GCP_ARTIFACT_REGISTRY --repo "$REPOSITORY" \
  --body "$(terraform_output artifact_registry_repository)"

echo "Configured GCP deployment variables for ${REPOSITORY}."
