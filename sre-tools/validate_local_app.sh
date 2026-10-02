#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname "$script_dir")
cd "$repo_root"

if ! command -v docker >/dev/null 2>&1; then
    printf '%s\n' "ERROR: Docker is required to validate the local app." >&2
    exit 1
fi
if ! command -v curl >/dev/null 2>&1; then
    printf '%s\n' "ERROR: curl is required for HTTP smoke checks." >&2
    exit 1
fi

base_url=${DAIRYFARM_BASE_URL:-http://127.0.0.1:8000}

printf '%s\n' "Checking frontend JavaScript syntax..."
sre-tools/check_frontend_syntax.sh

printf '%s\n' "Running Django system checks..."
docker compose exec -T api python manage.py check

printf '%s\n' "Running Django tests..."
docker compose exec -T api python manage.py test

printf '%s\n' "Checking the app and updated static assets at $base_url..."
for path in \
    / \
    /static/js/farmApp.js \
    /static/js/farmAppMenuAboutCtrl.js \
    /static/js/farmAppMenuContactCtrl.js \
    /static/templates/menu_contact.html \
    /static/templates/docs_dd_assets_full.html \
    /static/templates/docs_dd_summary.html
do
    curl --fail --silent --show-error --location --output /dev/null "$base_url$path"
    printf '  OK %s\n' "$path"
done

printf '%s\n' "Local app validation passed."
