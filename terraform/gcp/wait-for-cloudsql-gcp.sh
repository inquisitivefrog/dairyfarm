#!/usr/bin/env bash
# Wait for the DairyFarm Cloud SQL instance to reach a requested lifecycle state.
set -euo pipefail

TF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ID="${GCP_PROJECT_ID:-$(terraform -chdir="$TF_DIR" output -raw gcp_project_id)}"
REGION="${GCP_REGION:-$(terraform -chdir="$TF_DIR" output -raw gcp_region)}"
INSTANCE="${CLOUDSQL_INSTANCE:-$(terraform -chdir="$TF_DIR" output -raw project_name)-postgres}"
TARGET_STATE="${1:-RUNNABLE}"
TIMEOUT_SECONDS="${CLOUDSQL_WAIT_TIMEOUT_SECONDS:-1800}"
POLL_INTERVAL_SECONDS="${CLOUDSQL_POLL_INTERVAL_SECONDS:-10}"

case "$TARGET_STATE" in
  RUNNABLE|STOPPED) ;;
  *)
    echo "Usage: $0 [RUNNABLE|STOPPED]" >&2
    exit 2
    ;;
esac

if [[ -z "$PROJECT_ID" || -z "$REGION" || -z "$INSTANCE" ]]; then
  echo "Project, region, and Cloud SQL instance must be configured." >&2
  exit 2
fi

command -v gcloud >/dev/null || {
  echo "gcloud is required." >&2
  exit 1
}

printf 'Project: %s\nRegion: %s\nInstance: %s\nTarget state: %s\n' \
  "$PROJECT_ID" "$REGION" "$INSTANCE" "$TARGET_STATE"

deadline=$((SECONDS + TIMEOUT_SECONDS))
while (( SECONDS < deadline )); do
  state="$(gcloud sql instances describe "$INSTANCE" \
    --project "$PROJECT_ID" --format='value(state)')"
  printf '%s\n' "$state"
  if [[ "$state" == "$TARGET_STATE" ]]; then
    printf 'Cloud SQL %s reached %s.\n' "$INSTANCE" "$TARGET_STATE"
    exit 0
  fi
  sleep "$POLL_INTERVAL_SECONDS"
done

echo "Timed out after ${TIMEOUT_SECONDS}s waiting for ${INSTANCE} to reach ${TARGET_STATE}; last state: ${state:-unknown}" >&2
exit 1
