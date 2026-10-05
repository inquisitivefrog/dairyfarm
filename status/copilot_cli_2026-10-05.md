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
- The deployment workflow change is in local commit `7d40d36` on
  `ai-assisted`; it has not been pushed, so its GitHub Actions deployment has
  not run.
