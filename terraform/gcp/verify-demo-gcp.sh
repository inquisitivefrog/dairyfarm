#!/usr/bin/env bash
# Smoke-test the deployed DairyFarm demo API before or after making it public.
set -euo pipefail

TF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:---private}"

case "$MODE" in
  --private|--public) ;;
  *)
    echo "Usage: $0 [--private|--public]" >&2
    exit 2
    ;;
esac

API_URL="$(cd "$TF_DIR" && terraform output -raw api_service_url 2>/dev/null)"
if [[ -z "$API_URL" || "$API_URL" == *$'\n'* ]]; then
  echo "Could not read api_service_url from Terraform output." >&2
  exit 2
fi
UI_URL="$(cd "$TF_DIR" && terraform output -raw ui_service_url 2>/dev/null)"
if [[ -z "$UI_URL" || "$UI_URL" == *$'\n'* ]]; then
  echo "Could not read ui_service_url from Terraform output." >&2
  exit 2
fi

if [[ "$MODE" == "--private" ]]; then
  TOKEN="$(gcloud auth print-identity-token)"
  if [[ -z "$TOKEN" ]]; then
    echo "Could not get an identity token. Run gcloud auth login first." >&2
    exit 2
  fi
  AUTH_HEADER="Authorization: Bearer ${TOKEN}"
else
  AUTH_HEADER=""
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
PASS=0

request() {
  local name="$1" method="$2" path="$3" expected="$4"
  local output_file="$5"
  local status
  local -a curl_args=(-sS -o "$output_file" -w '%{http_code}'
    -X "$method")
  if [[ -n "$AUTH_HEADER" ]]; then
    curl_args+=(-H "$AUTH_HEADER")
  fi
  if [[ "$method" == "POST" ]]; then
    curl_args+=(-H 'Content-Type: application/json' -d '{}')
  fi
  status="$(curl "${curl_args[@]}" "${API_URL}${path}")"
  if [[ "|${expected}|" != *"|${status}|"* ]]; then
    printf 'FAIL  %s: expected HTTP %s, got HTTP %s\n' \
      "$name" "$expected" "$status" >&2
    cat "$output_file" >&2
    exit 1
  fi
  printf 'PASS  %s: HTTP %s\n' "$name" "$status"
  PASS=$((PASS + 1))
}

request "Synthetic client listing" GET \
  "/assets/api/clients/" 200 "$TMP_DIR/clients.json"
python3 - "$TMP_DIR/clients.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as response_file:
    payload = json.load(response_file)
clients = payload.get("results", payload) if isinstance(payload, dict) else payload
if not isinstance(clients, list) or len(clients) != 1:
    raise SystemExit(f"Expected exactly one visible client; got {clients!r}")
client = clients[0]
if client.get("name") != "AI-Assisted Demo Farm (2019-2026)":
    raise SystemExit(f"Unexpected visible client: {client!r}")
print(f"PASS  Only the synthetic farm is visible (client ID {client.get('id')})")
PY
PASS=$((PASS + 1))

CLIENT_ID="$(python3 - "$TMP_DIR/clients.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as response_file:
    payload = json.load(response_file)
clients = payload.get("results", payload) if isinstance(payload, dict) else payload
print(clients[0]["id"])
PY
)"
request "Synthetic cow listing" GET \
  "/assets/api/cows/client/${CLIENT_ID}/" 200 "$TMP_DIR/cows.json"
python3 - "$TMP_DIR/cows.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as response_file:
    payload = json.load(response_file)
if payload.get("count", 0) <= 0:
    raise SystemExit("Synthetic farm has no cows.")
cows = payload.get("results", [])
if not cows or cows[0].get("farm_number") != 1:
    raise SystemExit(f"Expected first cow farm_number=1; got {cows[:1]!r}")
print(
    f"PASS  Synthetic cows returned ({payload['count']} total); "
    "farm numbering starts at 1"
)
PY
PASS=$((PASS + 1))

request "Account/profile disclosure blocked" GET \
  "/ui_logged_in/" 403 "$TMP_DIR/profile.json"
request "Login blocked" GET \
  "/login/" 403 "$TMP_DIR/login.txt"
request "API write blocked" POST \
  "/assets/api/cows/" "401|403" "$TMP_DIR/write.json"

headers_file="$TMP_DIR/headers.txt"
curl_args=(-sS -D "$headers_file" -o /dev/null -I)
if [[ -n "$AUTH_HEADER" ]]; then
  curl_args+=(-H "$AUTH_HEADER")
fi
curl "${curl_args[@]}" "${API_URL}/assets/api/clients/"
if ! grep -qi '^strict-transport-security: max-age=86400' "$headers_file"; then
  echo "FAIL  API response is missing the expected HSTS header." >&2
  cat "$headers_file" >&2
  exit 1
fi
echo "PASS  HTTPS response includes the one-day HSTS header"
PASS=$((PASS + 1))

ui_status="$(curl -sS -o "$TMP_DIR/ui.html" -w '%{http_code}' "$UI_URL/")"
if [[ "$ui_status" != "200" ]]; then
  echo "FAIL  UI home page: expected HTTP 200, got HTTP ${ui_status}" >&2
  cat "$TMP_DIR/ui.html" >&2
  exit 1
fi
if ! grep -q 'data-public-demo="true"' "$TMP_DIR/ui.html"; then
  echo "FAIL  UI did not render the public read-only demo configuration." >&2
  exit 1
fi
echo "PASS  UI home page is public and renders public-demo mode (HTTP 200)"
PASS=$((PASS + 1))

ui_css_status="$(curl -sS -o /dev/null -w '%{http_code}' \
  "${UI_URL}/static/css/farmApp.css")"
if [[ "$ui_css_status" != "200" ]]; then
  echo "FAIL  UI static stylesheet: expected HTTP 200, got ${ui_css_status}" >&2
  exit 1
fi
echo "PASS  UI serves static CSS over HTTPS (HTTP 200)"
PASS=$((PASS + 1))

echo "All ${PASS} deployment smoke checks passed (${MODE})."
