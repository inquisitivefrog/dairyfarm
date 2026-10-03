#!/usr/bin/env bash
# Parse the GitHub Actions workflow and check its expected CI/deploy jobs.
set -euo pipefail

WORKFLOW="${1:-.github/workflows/ci.yml}"

if [[ ! -f "$WORKFLOW" ]]; then
  echo "Workflow file not found: $WORKFLOW" >&2
  exit 2
fi

if ! command -v ruby >/dev/null; then
  echo "Ruby is required to parse YAML. Install Ruby or run this check on macOS." >&2
  exit 1
fi

ruby - "$WORKFLOW" <<'RUBY'
require "yaml"

path = ARGV.fetch(0)
workflow = YAML.load_file(path)
abort "Workflow YAML must contain a mapping." unless workflow.is_a?(Hash)

jobs = workflow["jobs"]
abort "Workflow is missing its jobs mapping." unless jobs.is_a?(Hash)
abort "Workflow is missing the test job." unless jobs.key?("test")

deploy = jobs["deploy-gcp"]
abort "Workflow is missing the GCP deployment job." unless deploy.is_a?(Hash)
abort "GCP deployment must wait for the test job." unless deploy["needs"] == "test"

puts "Valid workflow YAML: #{path}"
puts "CI test and dependent GCP deployment jobs are present."
RUBY
