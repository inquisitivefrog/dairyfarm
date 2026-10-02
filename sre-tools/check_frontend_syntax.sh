#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(dirname "$script_dir")
cd "$repo_root"

if ! command -v node >/dev/null 2>&1; then
    printf '%s\n' "ERROR: Node.js is required to check JavaScript syntax." >&2
    exit 1
fi

checked=0
for file in demo/static/js/*.js; do
    node --check "$file"
    checked=$((checked + 1))
done

printf 'JavaScript syntax checks passed for %s files.\n' "$checked"
