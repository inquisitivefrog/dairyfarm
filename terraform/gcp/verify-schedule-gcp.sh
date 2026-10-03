#!/usr/bin/env bash
# Check the schedule or exercise the full SQL stop/maintenance/start sequence.
set -euo pipefail

TF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:---check}"
PROJECT_ID="${GCP_PROJECT_ID:-$(terraform -chdir="$TF_DIR" output -raw gcp_project_id)}"
REGION="${GCP_REGION:-$(terraform -chdir="$TF_DIR" output -raw gcp_region)}"
PREFIX="$(terraform -chdir="$TF_DIR" output -raw project_name)"
UI_URL="$(terraform -chdir="$TF_DIR" output -raw ui_service_url)"
TIMEOUT_SECONDS="${SCHEDULE_TEST_TIMEOUT_SECONDS:-600}"

case "$MODE" in
  --check|--exercise) ;;
  *)
    echo "Usage: $0 [--check|--exercise]" >&2
    exit 2
    ;;
esac

command -v gcloud >/dev/null || {
  echo "gcloud is required." >&2
  exit 1
}
command -v curl >/dev/null || {
  echo "curl is required." >&2
  exit 1
}

check_job() {
  local name="$1" expected="$2" schedule timezone state
  schedule="$(gcloud scheduler jobs describe "$name" \
    --location "$REGION" --project "$PROJECT_ID" \
    --format='value(schedule)')"
  timezone="$(gcloud scheduler jobs describe "$name" \
    --location "$REGION" --project "$PROJECT_ID" \
    --format='value(timeZone)')"
  state="$(gcloud scheduler jobs describe "$name" \
    --location "$REGION" --project "$PROJECT_ID" \
    --format='value(state)')"
  if [[ "$schedule" != "$expected" ||
        "$timezone" != "America/Los_Angeles" ||
        "$state" != "ENABLED" ]]; then
    printf 'FAIL %s: schedule=%s timezone=%s state=%s\n' \
      "$name" "$schedule" "$timezone" "$state" >&2
    return 1
  fi
  printf 'PASS %s: %s America/Los_Angeles (%s)\n' \
    "$name" "$schedule" "$state"
}

check_job "${PREFIX}-sql-start" "30 4 * * *"
check_job "${PREFIX}-sql-stop" "0 18 * * *"

if [[ "$MODE" == "--check" ]]; then
  echo "Schedule configuration is valid. Use --exercise to stop and restart Cloud SQL."
  exit 0
fi

state="$(gcloud sql instances describe "${PREFIX}-postgres" \
  --project "$PROJECT_ID" --format='value(state)')"
if [[ "$state" != "RUNNABLE" ]]; then
  echo "Refusing the exercise because Cloud SQL is not RUNNABLE (state: $state)." >&2
  exit 1
fi

restore_database() {
  local state
  state="$(gcloud sql instances describe "${PREFIX}-postgres" \
    --project "$PROJECT_ID" --format='value(state)' 2>/dev/null || true)"
  if [[ "$state" != "RUNNABLE" ]]; then
    echo "Ensuring Cloud SQL is restarted after schedule test..."
    gcloud scheduler jobs run "${PREFIX}-sql-start" \
      --location "$REGION" --project "$PROJECT_ID" --quiet || return
    local deadline=$((SECONDS + TIMEOUT_SECONDS))
    while (( SECONDS < deadline )); do
      state="$(gcloud sql instances describe "${PREFIX}-postgres" \
        --project "$PROJECT_ID" --format='value(state)' 2>/dev/null || true)"
      printf 'Waiting for Cloud SQL recovery: %s\n' "${state:-unknown}"
      [[ "$state" == "RUNNABLE" ]] && return
      sleep 10
    done
    echo "Cloud SQL did not recover within ${TIMEOUT_SECONDS}s." >&2
    return 1
  fi
}
trap restore_database EXIT

echo "WARNING: this exercise temporarily stops the public demo database."
gcloud scheduler jobs run "${PREFIX}-sql-stop" \
  --location "$REGION" --project "$PROJECT_ID" --quiet

deadline=$((SECONDS + TIMEOUT_SECONDS))
state=""
while (( SECONDS < deadline )); do
  state="$(gcloud sql instances describe "${PREFIX}-postgres" \
    --project "$PROJECT_ID" --format='value(state)')"
  printf 'Waiting for Cloud SQL to stop: %s\n' "$state"
  [[ "$state" == "STOPPED" ]] && break
  sleep 10
done
if [[ "$state" != "STOPPED" ]]; then
  echo "Cloud SQL did not reach STOPPED within ${TIMEOUT_SECONDS}s." >&2
  exit 1
fi
echo "PASS Cloud SQL stopped."

body_file="$(mktemp)"
trap 'rm -f "$body_file"; restore_database' EXIT
status="$(curl -sS --max-time 30 -o "$body_file" -w '%{http_code}' \
  "${UI_URL}/")"
if [[ "$status" != "503" ]] ||
   ! grep -q 'DairyFarm demo is offline' "$body_file"; then
  echo "FAIL expected the maintenance page (HTTP 503), got HTTP ${status}." >&2
  cat "$body_file" >&2
  exit 1
fi
echo "PASS UI serves the friendly maintenance page while Cloud SQL is stopped."

gcloud scheduler jobs run "${PREFIX}-sql-start" \
  --location "$REGION" --project "$PROJECT_ID" --quiet

deadline=$((SECONDS + TIMEOUT_SECONDS))
state=""
while (( SECONDS < deadline )); do
  state="$(gcloud sql instances describe "${PREFIX}-postgres" \
    --project "$PROJECT_ID" --format='value(state)')"
  printf 'Waiting for Cloud SQL to start: %s\n' "$state"
  [[ "$state" == "RUNNABLE" ]] && break
  sleep 10
done
if [[ "$state" != "RUNNABLE" ]]; then
  echo "Cloud SQL did not reach RUNNABLE within ${TIMEOUT_SECONDS}s." >&2
  exit 1
fi
echo "PASS Cloud SQL is RUNNABLE."

"$TF_DIR/verify-demo-gcp.sh" --public
echo "Cloud SQL schedule exercise passed."
