#!/usr/bin/env bash
# Check the live DairyFarm GCP resources managed by this Terraform stack.
set -uo pipefail

TF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

tf_output() {
  local value
  value="$(cd "$TF_DIR" && terraform output -raw "$1" 2>/dev/null)" || return 1
  [[ -n "$value" && "$value" != *$'\n'* ]] || return 1
  printf '%s' "$value"
}

PROJECT_ID="$(tf_output gcp_project_id)" || {
  echo "Terraform outputs unavailable. Initialize and apply terraform/gcp first."
  exit 2
}
REGION="$(tf_output gcp_region)" || {
  echo "Could not read gcp_region from Terraform outputs."
  exit 2
}
PREFIX="$(tf_output project_name)" || {
  echo "Could not read project_name from Terraform outputs."
  exit 2
}

PASS=0
FAIL=0

check() {
  local label="$1"
  shift
  local output error_file result
  error_file="$(mktemp)"
  output="$("$@" 2>"$error_file")"
  result=$?
  if [[ $result -eq 0 && -n "$output" && "$output" != "None" ]]; then
    printf '  PASS  %s: %s\n' "$label" "$output"
    PASS=$((PASS + 1))
  else
    printf '  FAIL  %s: missing, empty, or query failed (%s)\n' \
      "$label" "$(cat "$error_file")"
    FAIL=$((FAIL + 1))
  fi
  rm -f "$error_file"
}

check_value() {
  local label="$1" expected="$2"
  shift 2
  local output error_file result
  error_file="$(mktemp)"
  output="$("$@" 2>"$error_file")"
  result=$?
  if [[ $result -eq 0 && "$output" == "$expected" ]]; then
    printf '  PASS  %s: %s\n' "$label" "$output"
    PASS=$((PASS + 1))
  else
    printf '  FAIL  %s: expected %s, got %s (%s)\n' \
      "$label" "$expected" "${output:-empty}" "$(cat "$error_file")"
    FAIL=$((FAIL + 1))
  fi
  rm -f "$error_file"
}

echo "== DairyFarm GCP resource check (project: $PROJECT_ID, region: $REGION) =="
echo

echo "-- Managed services --"
SQL_STATE="$(gcloud sql instances describe "${PREFIX}-postgres" \
  --project "$PROJECT_ID" --format="value(state)" 2>/dev/null)"
if [[ "$SQL_STATE" == "RUNNABLE" || "$SQL_STATE" == "STOPPED" ]]; then
  printf '  PASS  Cloud SQL state: %s\n' "$SQL_STATE"
  PASS=$((PASS + 1))
else
  printf '  FAIL  Cloud SQL state: expected RUNNABLE or STOPPED, got %s\n' \
    "${SQL_STATE:-empty}"
  FAIL=$((FAIL + 1))
fi
if [[ "$SQL_STATE" == "RUNNABLE" ]]; then
  check "Cloud SQL database" \
    gcloud sql databases describe dairyfarm --instance="${PREFIX}-postgres" \
    --project "$PROJECT_ID" --format="value(name)"
elif [[ "$SQL_STATE" == "STOPPED" ]]; then
  if terraform -chdir="$TF_DIR" state list 2>/dev/null |
      grep -Fxq "google_sql_database.main"; then
    echo "  PASS  Cloud SQL database resource is tracked in Terraform state (live database metadata is unavailable while stopped)."
    PASS=$((PASS + 1))
  else
    echo "  FAIL  Cloud SQL database resource is not present in Terraform state."
    FAIL=$((FAIL + 1))
  fi
fi
check "Artifact Registry repository" \
  gcloud artifacts repositories describe "${PREFIX}-images" \
  --location "$REGION" --project "$PROJECT_ID" --format="value(name)"
check "Runtime service account" \
  gcloud iam service-accounts describe \
  "${PREFIX}-runtime@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project "$PROJECT_ID" --format="value(email)"
check "UI service account" \
  gcloud iam service-accounts describe \
  "${PREFIX}-ui@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project "$PROJECT_ID" --format="value(email)"
check "Django secret metadata" \
  gcloud secrets describe "${PREFIX}-django-secret-key" \
  --project "$PROJECT_ID" --format="value(name)"
check "Database password secret metadata" \
  gcloud secrets describe "${PREFIX}-database-password" \
  --project "$PROJECT_ID" --format="value(name)"
echo

echo "-- Optional Cloud Run workloads --"
if gcloud run services describe "${PREFIX}-api" --region "$REGION" \
  --project "$PROJECT_ID" --format="value(name)" >/dev/null 2>&1; then
  check_value "API service ready condition" "True" \
    gcloud run services describe "${PREFIX}-api" --region "$REGION" \
    --project "$PROJECT_ID" --format="value(status.conditions[0].status)"
  check_value "UI service ready condition" "True" \
    gcloud run services describe "${PREFIX}-ui" --region "$REGION" \
    --project "$PROJECT_ID" --format="value(status.conditions[0].status)"
  check "Database initialization job" \
    gcloud run jobs describe "${PREFIX}-initialize" --region "$REGION" \
    --project "$PROJECT_ID" --format="value(name)"

  API_POLICY="$(gcloud run services get-iam-policy "${PREFIX}-api" \
    --region "$REGION" --project "$PROJECT_ID" \
    --format="value(bindings.members)" 2>/dev/null || true)"
  if grep -q 'allUsers' <<<"$API_POLICY"; then
    echo "  INFO  API allows public invocation; confirm the API stays read-only."
  else
    echo "  INFO  API does not appear publicly invokable."
  fi
else
  echo "  SKIP  Cloud Run services and initialization job are not deployed."
fi
echo

echo "== Summary: $PASS passed, $FAIL failed =="
if [[ "$FAIL" -gt 0 ]]; then
  exit 1
fi
