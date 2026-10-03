#!/usr/bin/env bash
# Rough list-price estimate from live DairyFarm GCP resources, not billing data.
set -uo pipefail

TF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOURS_PER_DAY=24
HOURS_PER_MONTH=730

tf_output() {
  local value
  value="$(cd "$TF_DIR" && terraform output -raw "$1" 2>/dev/null)" || return 1
  [[ -n "$value" && "$value" != *$'\n'* ]] || return 1
  printf '%s' "$value"
}

PROJECT_ID="$(tf_output gcp_project_id)" || {
  echo "No Terraform outputs found; no applied DairyFarm GCP stack to inspect."
  echo "Estimated managed-resource baseline: \$0.00/day (no resources verified)."
  exit 0
}
REGION="$(tf_output gcp_region)" || {
  echo "Could not read gcp_region from Terraform outputs."
  exit 2
}
PREFIX="$(tf_output project_name)" || {
  echo "Could not read project_name from Terraform outputs."
  exit 2
}

# Editable approximate rates in USD. Confirm against current regional pricing.
# Cloud SQL rates are deliberately parameters: pricing depends on edition, region,
# tier, and billing terms; unknown tiers are not assigned a guessed compute price.
CLOUDSQL_F1_MICRO_HOURLY="${CLOUDSQL_F1_MICRO_HOURLY:-0.0150}"
CLOUDSQL_PD_SSD_GB_MONTH="${CLOUDSQL_PD_SSD_GB_MONTH:-0.17}"
STATE_BUCKET_GB_MONTH="${STATE_BUCKET_GB_MONTH:-0.020}"
DB_HOURS_PER_DAY="${DB_HOURS_PER_DAY:-13.5}"

TOTAL_HOURLY=0
UNKNOWN_COST=0

line() {
  local label="$1" hourly="$2" daily monthly
  daily="$(awk -v h="$hourly" -v d="$HOURS_PER_DAY" \
    'BEGIN { printf "%.4f", h*d }')"
  monthly="$(awk -v h="$hourly" -v m="$HOURS_PER_MONTH" \
    'BEGIN { printf "%.2f", h*m }')"
  printf '  %-48s $%s/hr   $%s/day   $%s/mo\n' \
    "$label" "$hourly" "$daily" "$monthly"
  TOTAL_HOURLY="$(awk -v t="$TOTAL_HOURLY" -v h="$hourly" \
    'BEGIN { printf "%.6f", t+h }')"
}

line_scheduled_daily() {
  local label="$1" hourly="$2" hours="$3" daily monthly average_hourly
  daily="$(awk -v h="$hourly" -v n="$hours" 'BEGIN { printf "%.4f", h*n }')"
  monthly="$(awk -v h="$hourly" -v n="$hours" -v d="$HOURS_PER_MONTH" \
    'BEGIN { printf "%.2f", h*n*d/24 }')"
  average_hourly="$(awk -v h="$hourly" -v n="$hours" \
    'BEGIN { printf "%.6f", h*n/24 }')"
  printf '  %-48s $%s/day   $%s/mo (%s h/day)\n' \
    "$label" "$daily" "$monthly" "$hours"
  TOTAL_HOURLY="$(awk -v t="$TOTAL_HOURLY" -v h="$average_hourly" \
    'BEGIN { printf "%.6f", t+h }')"
}

echo "== DairyFarm GCP list-price estimate (project: $PROJECT_ID, region: $REGION) =="
echo "Rates are rough, editable assumptions; this is NOT billing data."
echo "Cloud Run usage, egress, backups, and image/state storage are not fully modeled."
echo

SQL_DETAILS="$(gcloud sql instances describe "${PREFIX}-postgres" \
  --project "$PROJECT_ID" \
  --format="value(settings.tier,settings.dataDiskSizeGb,state)" 2>/dev/null || true)"
if [[ -n "$SQL_DETAILS" ]]; then
  IFS=$'\t' read -r SQL_TIER SQL_DISK_GB SQL_STATE <<<"$SQL_DETAILS"
  SQL_DISK_GB="${SQL_DISK_GB:-0}"
  echo "-- Cloud SQL --"
  echo "  Live tier: ${SQL_TIER:-unknown}; state: ${SQL_STATE:-unknown}"
  if [[ "$SQL_TIER" == "db-f1-micro" ]]; then
    line_scheduled_daily "Cloud SQL ${SQL_TIER} compute (approx)" \
      "$CLOUDSQL_F1_MICRO_HOURLY" "$DB_HOURS_PER_DAY"
  else
    echo "  UNKNOWN Cloud SQL compute price for tier '${SQL_TIER:-unknown}'; excluded."
    UNKNOWN_COST=1
  fi
  if [[ "$SQL_DISK_GB" =~ ^[0-9]+$ ]]; then
    SQL_DISK_HOURLY="$(awk -v gb="$SQL_DISK_GB" \
      -v r="$CLOUDSQL_PD_SSD_GB_MONTH" -v m="$HOURS_PER_MONTH" \
      'BEGIN { printf "%.6f", gb*r/m }')"
    line "Cloud SQL SSD storage (${SQL_DISK_GB}GB, approx)" "$SQL_DISK_HOURLY"
  else
    echo "  UNKNOWN Cloud SQL disk size; storage excluded."
    UNKNOWN_COST=1
  fi
else
  echo "-- Cloud SQL --"
  echo "  (no Cloud SQL instance found)"
fi
echo

echo "-- Cloud Run --"
if gcloud run services describe "${PREFIX}-api" --region "$REGION" \
  --project "$PROJECT_ID" --format="value(name)" >/dev/null 2>&1; then
  echo "  API and UI services found; configured to scale to zero."
  echo "  Usage-based CPU, memory, and requests are excluded; inspect Cloud Billing for actual usage."
else
  echo "  (Cloud Run services not deployed)"
fi
echo

echo "-- Other resources --"
echo "  Artifact Registry storage, Secret Manager versions, GCS state storage,"
echo "  backups, and network egress are excluded or depend on usage."
if gcloud storage buckets describe "gs://${PREFIX}-tfstate-${PROJECT_ID}" \
  --project "$PROJECT_ID" >/dev/null 2>&1; then
  echo "  Terraform state bucket found; storage cost depends on stored state/version size."
else
  echo "  Terraform state bucket not found in this project."
fi
echo

TOTAL_DAILY="$(awk -v h="$TOTAL_HOURLY" -v d="$HOURS_PER_DAY" \
  'BEGIN { printf "%.4f", h*d }')"
TOTAL_MONTHLY="$(awk -v h="$TOTAL_HOURLY" -v m="$HOURS_PER_MONTH" \
  'BEGIN { printf "%.2f", h*m }')"
echo "== Estimated modeled baseline: \$${TOTAL_HOURLY}/hr   \$${TOTAL_DAILY}/day   \$${TOTAL_MONTHLY}/mo =="
if [[ "$UNKNOWN_COST" -eq 1 ]]; then
  echo "Some managed-resource costs were unknown and are excluded; actual total is higher."
fi
echo "Use Cloud Billing reports for actual charges. Estimates exclude usage-based costs and may be stale."
