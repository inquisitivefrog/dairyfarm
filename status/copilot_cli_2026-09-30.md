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
