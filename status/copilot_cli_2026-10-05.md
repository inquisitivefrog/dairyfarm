# Copilot CLI status — 2026-10-05

## Public demo URL

- Resume URL: <https://dairyfarm-demo-ui-u4ndlctsla-uc.a.run.app>
- The user chose to use the existing Cloud Run URL; no custom-domain or DNS
  changes are planned. The URL remains stable while the Cloud Run service
  exists, but could change if that service is deleted and recreated.
- A branded hostname, `demo.dairyfarm.inquisitivefrog.com`, was considered.
  DNS control was not confirmed, and the user preferred the existing URL with
  no additional infrastructure.

## GCP schedule and deployment

- Cloud Scheduler is configured to start Cloud SQL at 4:30 a.m. and stop it
  at 6:00 p.m. daily, including weekends, in `America/Los_Angeles`.
- Cloud SQL was confirmed `RUNNABLE` on Oct 5 after the morning scheduled
  start. The resource checker reported 10 passed, 0 failed.
- The deployment workflow was pushed to `ai-assisted`. Its first deploy failed
  because the CI deployer role lacked `run.executions.get` (needed by
  `gcloud run jobs execute --wait`). The permission was added to the custom
  role in `terraform/gcp/github-actions.tf` and applied with Terraform; the
  plan showed only that role change plus harmless Cloud Run client-metadata
  drift.
- The rerun and the follow-up push (`dad1e61`) both completed successfully:
  tests, secret scan, and the GCP deploy job all passed.
- The next push (`75b2ffd`) deployed at about 6:39 p.m. Pacific, after Cloud
  SQL had stopped. The initialization job could not reach the database and
  the deploy job failed (the live Cloud Run services were untouched). The
  deploy job now checks the Pacific hour and skips, with a notice, outside
  5:00 a.m.-6:00 p.m.; `workflow_dispatch` was added so it can be re-run
  manually during operating hours. The edit is scripted in
  `scripts/gate-deploy-on-hours.py` (idempotent). Pushed as `89476b7`.
- That run's tests failed once on a flaky collision: the list tests in
  `demo/assets/tests/test_serializers.py` (`TestInjurySerializer` and
  `TestIllnessSerializer`) create 10 records with random 10-10000 suffixes, so
  two could rarely match the unique `diagnosis` constraint (about 0.5% per
  run). Each loop value now gets a unique index suffix. The affected tests
  pass locally; this fix is committed in the next push.
- Closed four stale Dependabot PRs (#4-#7, 2021-2022 bumps against the legacy
  `master` stack). `master` and `ai-assisted` remain separate branches.
- Expected next step: after 5 a.m. Pacific on Oct 6, trigger the workflow
  manually on `ai-assisted` and confirm a real deploy passes end to end.
- The public smoke test passed all 10 checks: only the synthetic farm is
  visible, farm numbering starts at 1, login and writes are blocked, and HTTPS
  with HSTS is active.
- Dependabot reports 57 open alerts on the default branch (5 critical); this
  is existing dependency debt on `master`, and `ai-assisted` has already
  upgraded the runtime.
- Cloud SQL stops at 6 p.m. and restarts at 4:30 a.m. as scheduled.
