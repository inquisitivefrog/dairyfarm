# Copilot CLI status — 2026-09-30

## Major decisions

- Keep `ai-assisted` separate from `main`; do not merge the branches until the
  user decides to do so. Use this branch for ongoing AI-assisted development
  and validation.
- Run CI on pushes to both `ai-assisted` and `master`, as well as on pull
  requests. Do not enable CD yet; later deployment workflows should be
  explicitly scoped to the agreed branch and protected environment.
- Preserve clear authorship for interviews: identify independently authored
  work as the user's work and AI-assisted work as a collaboration. Do not
  overstate authorship or obscure the use of AI.
- Continue keeping dated, project-specific decision notes in the repository so
  the history remains tool-neutral and portable.

## CI status

- CI ran successfully on the `ai-assisted` push as workflow run `36750053646`:
  the PostgreSQL-backed Django tests/checks and Gitleaks scan passed.
- Dependency review is configured for pull requests only and was therefore
  skipped on the branch-push run.
- The first run warned that checkout v4's Node.js 20 runtime is deprecated.
  The workflow now pins checkout v7.0.1 by immutable commit SHA.
- The active default branch is `master`, not `main`; CI push filters and
  documentation now use `ai-assisted` and `master`.

## Dependency modernization discovery

- GitHub reports 55 open Dependabot alerts from `requirements.txt`. These are
  advisory records, not 55 distinct affected packages; several are multiple
  advisories against the same pinned legacy package.
- Direct application use includes Django 2.0.1, Django REST Framework 3.7.7,
  the PostgreSQL driver, python-memcached, and pytz. BeautifulSoup is used by
  tests; flake8 is used for SRE-tool linting.
- Initial source search found no direct use of NumPy, Requests, django-heroku,
  dj-database-url, or Gunicorn in the current Docker startup path. Confirm
  tooling/deployment needs before removing them; transitive requirements should
  be regenerated rather than manually guessed.
- Django 2.0 compatibility blockers include old `django.utils.six` test imports
  and deprecated `django.conf.urls.url` routes. There is no need to rewrite
  these until the staged framework upgrade exposes the exact failures.
- Python 3.10 reaches end of life in October 2026, so the existing preflight
  minimum of Python 3.10 is too weak as a future deployment target. Candidate
  target: Python 3.13 with the maintained Django 5.2 LTS line, after validating
  dependency compatibility and the hosting platform.
- Next technical step: remove confirmed unused dependencies, separate runtime
  from test/lint dependencies, generate reproducible constraints, then upgrade
  the runtime and framework under CI. Do not try to silence the alert count
  with blind package bumps.
- Dependency inventory step started: make `requirements.txt` the current
  runtime set, and place BeautifulSoup plus flake8 and its pinned lint
  dependencies in `requirements-dev.txt`. Local Compose opts into the dev set;
  direct Docker builds default to runtime dependencies only.
- Removed unused legacy requirements: NumPy, Requests and its standalone
  urllib3-related pins, nose, pipenv/pew/virtualenv tooling, and unused Heroku
  deployment packages (django-heroku, dj-database-url, gunicorn, WhiteNoise).
  The empty historical Pipfile is not the active package manifest.
- Added an opt-in BusyBox Compose sidecar (`docker compose run --rm debug`) for
  shell/network diagnostics. It depends on the API service, is available only
  under the `debug` profile, and does not add BusyBox to the app image. The
  BusyBox image is pinned by version and digest.
- The split dependency set builds successfully for the Compose target
  architecture. The full PostgreSQL-backed test suite still passes (477),
  `pip check`, Django system/migration checks, and SRE-tool lint pass. A
  runtime-only image was also verified to omit BeautifulSoup and flake8.
- A direct native ARM64 build of the legacy psycopg2 2.7.3.2 package fails
  because that old release lacks a compatible wheel and the image lacks
  PostgreSQL build headers. The supported local Compose path explicitly targets
  linux/amd64 and passes; direct Docker builds on Apple Silicon must specify
  `--platform=linux/amd64`. Revisit architecture support during modernization.

## Local application review

- Resumed the authenticated local UI review using the seeded Foster Farms Dairy
  sample data. Home, Reload Cache, Logout, the design documents, asset pages,
  and annual/monthly reports were opened and reviewed.
- Confirmed UI defects: About displays the untranslated `{{text}}` and a
  broken image because its controller logs `$scookie.text` and throws before
  assigning the image URL; Contact displays raw Django template tags in a
  static Angular partial and does not render the response fetched by its
  controller; Marketing Requirements contents links lose the Angular route
  when navigating to bare fragment URLs.
- Reporting Design Doc Appendix contains only a blank glossary row. Unit Test
  Results is an intentionally saved historical transcript showing tests were
  run against a prior build; it is not live test output for the current code.
- Asset pages showed sample data: 130 cows, 5,173 events, 725 exercises, 780
  inspections, 742 milkings, 13 pastures, and 10 seed records for Foster Farms
  Dairy. Annual and monthly reports also loaded; the monthly report has no
  further drilldown.
- Investigated apparently empty RFID dropdowns against the local database:
  all 234 Cow records have an RFID value, and all 234 values are distinct.
  Therefore, the closed dropdown appearance alone is not evidence of missing
  RFID data. Other closed selectors were not tested for options and remain
  unverified.
- No application code was changed during this UI review. The existing local
  Compose stack and database were left running and intact.
