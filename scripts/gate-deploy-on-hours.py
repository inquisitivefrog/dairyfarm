#!/usr/bin/env python3
"""Gate the GCP deploy job on demo operating hours (idempotent).

Cloud SQL runs 5:00 a.m.-6:00 p.m. Pacific, so a deploy outside those hours
would fail when the initialization job cannot reach the database.
"""
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else ".github/workflows/ci.yml"
MARKER = "id: hours"

OLD_IF = """    if: github.event_name == 'push' && github.ref == 'refs/heads/ai-assisted'
"""
NEW_IF = """    if: >-
      github.ref == 'refs/heads/ai-assisted' &&
      (github.event_name == 'push' || github.event_name == 'workflow_dispatch')
"""

OLD_FIRST_STEPS = """    steps:
      - name: Check out repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

      - name: Authenticate to Google Cloud"""
NEW_FIRST_STEPS = """    steps:
      - name: Check demo operating hours
        id: hours
        run: |
          hour="$(TZ=America/Los_Angeles date +%-H)"
          if [ "$hour" -ge 5 ] && [ "$hour" -lt 18 ]; then
            echo "open=true" >> "$GITHUB_OUTPUT"
          else
            echo "open=false" >> "$GITHUB_OUTPUT"
            echo "::notice::Cloud SQL is stopped outside 5:00 a.m.-6:00 p.m. Pacific; deployment skipped. Re-run this workflow during operating hours."
          fi

      - name: Check out repository
        if: steps.hours.outputs.open == 'true'
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

      - name: Authenticate to Google Cloud"""

GATED_STEPS = [
    "Authenticate to Google Cloud with Workload Identity Federation",
    "Set up gcloud",
    "Build and push Cloud Run images",
    "Deploy Cloud Run API, UI, and initialization job",
    "Verify deployed revisions and public UI",
]

with open(PATH) as handle:
    text = handle.read()

if MARKER in text:
    print("Operating-hours gate already present; no changes made.")
    sys.exit(0)

for old, new in ((OLD_IF, NEW_IF), (OLD_FIRST_STEPS, NEW_FIRST_STEPS)):
    if old not in text:
        sys.exit("Expected workflow text not found; aborting without changes.")
    text = text.replace(old, new, 1)

for name in GATED_STEPS:
    old = "      - name: %s\n" % name
    if old not in text:
        sys.exit("Step not found: %s" % name)
    text = text.replace(
        old, old + "        if: steps.hours.outputs.open == 'true'\n", 1)

with open(PATH, "w") as handle:
    handle.write(text)
print("Added operating-hours gate and workflow_dispatch to %s" % PATH)
