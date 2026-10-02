#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname "$script_dir")
cd "$repo_root"

usage() {
    cat <<'EOF'
Run Django tests and publish a grouped HTML report.

Usage:
  sre-tools/run_and_publish_test_results.sh [options]

Options:
  --input FILE       Render a previously captured verbose test transcript
                     instead of running the full Django suite.
  --output FILE      Report path (default: demo/static/templates/docs_tests_YEAR.html)
  --run-date DATE    Report date (default: local date)
  --command TEXT    Command recorded in the report.
  -h, --help         Show this help

The normal mode runs:
  docker compose exec -T api python manage.py test -v 2

Reports are grouped by Django app and test module. Test failures still produce
a report and cause this script to exit nonzero.
EOF
}

input_file=
command_override=
run_date=$(date +%F)
output_file="demo/static/templates/docs_tests_$(date +%Y).html"

while (($#)); do
    case "$1" in
        --input)
            (($# >= 2)) || { echo "ERROR: --input requires a file." >&2; exit 2; }
            input_file=$2
            shift 2
            ;;
        --output)
            (($# >= 2)) || { echo "ERROR: --output requires a file." >&2; exit 2; }
            output_file=$2
            shift 2
            ;;
        --run-date)
            (($# >= 2)) || { echo "ERROR: --run-date requires a date." >&2; exit 2; }
            run_date=$2
            shift 2
            ;;
        --command)
            (($# >= 2)) || { echo "ERROR: --command requires text." >&2; exit 2; }
            command_override=$2
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: unexpected argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

transcript=
test_status=0
if [[ -n "$input_file" ]]; then
    if [[ ! -f "$input_file" ]]; then
        echo "ERROR: transcript not found: $input_file" >&2
        exit 2
    fi
    transcript=$input_file
    command_text=${command_override:-"Previously captured Django test transcript"}
else
    if ! command -v docker >/dev/null 2>&1; then
        echo "ERROR: Docker is required to run Django tests." >&2
        exit 1
    fi
    transcript=$(mktemp "${TMPDIR:-/tmp}/dairyfarm-tests.XXXXXX")
    trap 'rm -f "$transcript"' EXIT
    command_text=${command_override:-"docker compose exec -T api python manage.py test -v 2"}

    printf '%s\n' "Running Django tests and capturing output..."
    set +e
    docker compose exec -T api python manage.py test -v 2 2>&1 |
        tee "$transcript"
    pipeline_status=("${PIPESTATUS[@]}")
    set -e
    test_status=${pipeline_status[0]}
fi

printf '%s\n' "Rendering grouped report to $output_file..."
python3 sre-tools/render_test_results.py \
    --input "$transcript" \
    --output "$output_file" \
    --run-date "$run_date" \
    --command "$command_text"

if ((test_status != 0)); then
    printf 'ERROR: Django tests failed with exit code %s; report was saved.\n' \
        "$test_status" >&2
    exit "$test_status"
fi

printf '%s\n' "Test report saved successfully."
