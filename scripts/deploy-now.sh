#!/usr/bin/env bash
# Manually run the CI/deploy workflow on ai-assisted and watch it finish.
# Deploys only work while Cloud SQL runs (5:00 a.m.-6:00 p.m. Pacific).
set -euo pipefail

BRANCH="${1:-ai-assisted}"
export GCP_PROJECT_ID="${GCP_PROJECT_ID:-project-4c5a8821-da4c-4c68-97f}"
INSTANCE="${GCP_SQL_INSTANCE:-dairyfarm-demo-postgres}"

hour="$(TZ=America/Los_Angeles date +%-H)"
if (( hour < 5 || hour >= 18 )); then
  echo "Outside operating hours (5:00 a.m.-6:00 p.m. Pacific); Cloud SQL is" \
    "scheduled to be stopped. Try again during operating hours." >&2
  exit 1
fi

state="$(gcloud sql instances describe "$INSTANCE" \
  --project "$GCP_PROJECT_ID" --format='value(state)')"
if [[ "$state" != "RUNNABLE" ]]; then
  echo "Cloud SQL is $state, not RUNNABLE. Wait for it with:" >&2
  echo "  ./terraform/gcp/wait-for-cloudsql-gcp.sh" >&2
  exit 1
fi

echo "Cloud SQL is RUNNABLE. Dispatching CI on $BRANCH..."
before="$(gh run list --branch "$BRANCH" --event workflow_dispatch \
  --limit 1 --json databaseId -q '.[0].databaseId // 0' 2>/dev/null | tail -1)"
gh workflow run ci.yml --ref "$BRANCH"

run_id=""
for _ in $(seq 1 30); do
  sleep 4
  run_id="$(gh run list --branch "$BRANCH" --event workflow_dispatch \
    --limit 1 --json databaseId -q '.[0].databaseId // 0' 2>/dev/null | tail -1)"
  [[ -n "$run_id" && "$run_id" != "0" && "$run_id" != "$before" ]] && break
  run_id=""
done
if [[ -z "$run_id" ]]; then
  echo "Could not find the dispatched run; check the Actions tab." >&2
  exit 1
fi

echo "Watching run $run_id..."
gh run watch "$run_id" --exit-status >/dev/null 2>&1 || true
gh run view "$run_id" --json status,conclusion,jobs 2>/dev/null |
  python3 -c '
import json, sys
data = json.load(sys.stdin)
print(data["status"], data["conclusion"])
for job in data["jobs"]:
    print(" ", job["name"], job["conclusion"])
sys.exit(0 if data["conclusion"] == "success" else 1)'
