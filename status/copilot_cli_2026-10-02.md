# Copilot CLI status — 2026-10-02

## Modernization decision

- Public-cloud planning is paused. No GCP project, Terraform configuration, or
  cloud resources were created for DairyFarm.
- The user approved Python 3.14, Django 5.2 LTS, and a current Django REST
  Framework 3.18.x release as the modernization target.
- The AngularJS frontend remains unchanged as a separate client of the
  same-origin Django routes/API.

## Runtime upgrade completed locally

- Updated the Docker runtime from Python 3.6 to Python 3.14 and upgraded the
  app dependencies to Django 5.2.17, DRF 3.18.1, psycopg 3.3.6, PyMemcache
  4.0.0, and Gunicorn 26.2.0.
- Replaced removed Django URL/static-template/cache APIs, `django.utils.six`,
  and deprecated settings. Preserved integer model primary-key defaults to
  avoid unintended schema changes.
- Replaced `pytz` usage with standard-library `datetime`, `timezone`, and
  `zoneinfo`; set `TIME_ZONE` to the canonical IANA name
  `America/Los_Angeles`.
- Replaced Python's removed `unittest.TestCase.assertEquals` aliases and fixed
  invalid regex escape literals without changing their string values.
- Updated the deployment preflight baseline to Python 3.14 and documented
  explicit HSTS subdomain/preload settings. Preload remains an explicit
  domain-dependent choice.
- Rebuilt the local API and UI containers. The existing PostgreSQL volume was
  retained; startup applied the pending standard Django admin/auth migrations.

## Validation

- Full PostgreSQL-backed test suite passes: **491 tests**.
- Django system and migration checks pass; `pip check` reports no broken
  requirements; SRE-tool flake8 passes.
- Python compilation passes with `SyntaxWarning` treated as an error; frontend
  syntax checks pass for 37 JavaScript files.
- Deployment preflight passes when production HTTPS, cookie, HSTS, and host
  settings are explicitly supplied.
- Local app shell, contact template, design-document template, and restored
  Milking Shorthorn image return HTTP 200 through the UI proxy.

## Remaining roadmap

- A read-only audit of the local PostgreSQL database found 11 active ordinary
  accounts, none staff/superusers. Nine match the historical user fixture; the
  fixture cleanup helper's dry run would disable all nine, including the
  `foster` and `berkeley` accounts currently used locally. No account changes
  were applied.
- The local database contains legacy Foster/Berkeley demo records and a
  separately owned AI-assisted synthetic farm. The original farm data's
  provenance is not explicit enough to assume it is safe to publish; prefer a
  fresh public database seeded only with reviewed, explicitly synthetic data.
- The AI-assisted dataset loader now creates its own minimal reference data and
  synthetic-only owner/farm on an otherwise empty migrated database. It does
  not need or import historical user/client fixtures, refuses to take over a
  farm owned by another account, and leaves its new owner's password unusable.
  This was validated with clean-database, ownership-conflict, and idempotency
  tests; the existing local database was not modified.
- The user chose a public, read-only demo model. An opt-in
  `DJANGO_PUBLIC_DEMO_READ_ONLY` mode now allows safe anonymous reads scoped to
  the configured synthetic farm, rejects API writes even for authenticated
  users, and displays a read-only UI state. The flag defaults off; this has
  been tested locally and temporarily enabled on the localhost-only Docker UI
  for user review. It has not been publicly deployed.
- Farm-local sequence numbers now appear consistently in asset lists, detail
  views, and result views. They start at one per farm and asset type, continue
  across pagination, and do not alter database primary keys or object links.
- An additional active `login-probe` account and empty farm are present only in
  the local database, not in source or fixtures. Its origin is unknown; it was
  left unchanged.
- Public deployment remains paused. Before it is reconsidered, revoke any
  historical credentials shared externally, provision a fresh database with
  only reviewed synthetic data, finish domain-specific production security
  configuration, and confirm operational/backup requirements.
- The existing Django/Gunicorn/Docker upgrade is local only; there is no
  Terraform or cloud deployment configuration for DairyFarm yet.
