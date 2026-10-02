# Local Docker baseline

This Compose setup runs the application locally on Python 3.14, Django 5.2 LTS,
and Django REST Framework 3.18. It is a development baseline, not by itself a
complete public deployment configuration.

## Deployment preflight

Before considering a public deployment, run
`python sre-tools/deployment_preflight.py` inside the deployment image. It exits
nonzero unless the runtime is at least Python 3.14 / Django 5.2,
`DJANGO_ENVIRONMENT=production`, `DEBUG` is disabled, allowed hosts and a
generated secret are configured, a non-SQLite database is used, secure
cookies/HTTPS redirect/HSTS are enabled, and Django's deployment checks pass.
Do not disable the checks to force a deployment.

Configure production security settings through `DJANGO_SECURE_SSL_REDIRECT`,
`DJANGO_SESSION_COOKIE_SECURE`, `DJANGO_CSRF_COOKIE_SECURE`,
`DJANGO_HSTS_SECONDS`, and `DJANGO_HSTS_INCLUDE_SUBDOMAINS`. Set
`DJANGO_HSTS_PRELOAD=true` only when deploying on a domain you control and
intend to submit to browser preload lists. Enable HSTS only after HTTPS is
correctly configured for the domain and its subdomains.
Set `DJANGO_CSRF_TRUSTED_ORIGINS` to the exact scheme-and-host origins used by
the browser, comma-separated (for example, `https://farm.example.com`). The
local Compose defaults trust only `http://localhost` and
`http://127.0.0.1`.

## Configure and start

1. Copy `.env.example` to `.env`.
2. Replace `DJANGO_SECRET_KEY` with a locally generated random key and set a
   local-only `POSTGRES_PASSWORD`. Do not reuse historical demo credentials.
3. From the repository root, run `docker compose up --build`.
4. Open <http://localhost:8000/>.

The UI service serves the existing static AngularJS assets and proxies other
requests to Django, preserving the existing same-origin routes. Django runs as
the API service. PostgreSQL data persists in the `postgres-data` volume;
Memcached is a separate cache service.

For a temporary BusyBox shell with network access to the Compose services, run
`docker compose run --rm debug`. Compose starts the API dependencies and
attaches the debug container to the same network. Use BusyBox tools such as
`nslookup api` or `wget -S -O- --header='Host: localhost' http://api:8000/`.
The debug service is profile-gated and is not started by the normal `up`
command.

`requirements.txt` lists the packages currently needed by the app runtime.
`requirements-dev.txt` includes those packages plus test and quality tools.
The local Compose build opts into the development dependencies so it can run
tests; a direct Docker build installs runtime requirements only by default.
The runtime dependencies are pinned to the currently validated versions.

## Checks and tests

Run the Django system check:

```sh
docker compose run --rm api python manage.py check
```

Run the full Django suite:

```sh
docker compose run --rm api python manage.py test
```

The API container applies migrations before starting. The test command uses
Django's temporary test database and does not seed the demo dataset. The
Compose PostgreSQL database starts empty; safe demo account/data setup is
separate and is not performed by container startup. The full PostgreSQL test
suite currently passes.

GitHub Actions runs these checks on pull requests and pushes to `ai-assisted`
and `master`. It also reviews dependency changes for high-severity
vulnerabilities and scans the checked-out source tree for secrets. The lint
gate is limited to `sre-tools/` while the legacy application-wide flake8
backlog is addressed. This workflow does not deploy; production deployment
remains blocked until the supported runtime/framework baseline and deployment
preflight are satisfied.
Enable GitHub's dependency graph/Dependabot alerts and secret scanning with
push protection in repository settings as well; workflow configuration cannot
turn on those repository-level features.

SQLite fixture tests previously failed on the legacy Django baseline with
`no such table: main.auth_user__old`; the supported validation path uses
PostgreSQL.

## Demo data and cleanup

The user-creation helper now prompts for passwords without echoing them and
creates regular accounts by default. Django staff or superuser access must be
requested explicitly. Historical credentials exposed in prior revisions are
compromised and must not be reused. The checked-in user fixture has unusable
passwords and no privileged accounts; it is test data, not a deployable
identity store. Do not run `demo/tools/reset` or `demo/tools/stress`: they
delete the local SQLite database and migration files.
Staff accounts intentionally retain cross-tenant access for support/admin
workflows; grant staff status only to trusted operators.

If a persistent database was previously seeded with these demo users, review
the configured database before running `python tools/disable_demo_accounts.py`
from `demo/` (dry run). Add `--apply` to deactivate the fixture accounts,
remove any elevated privileges, and invalidate their passwords and sessions.
This does not revoke credentials or sessions on any separately hosted
historical deployment; those must be rotated or disabled there directly.

`docker compose down` stops the services while retaining PostgreSQL data.
Removing the `postgres-data` volume permanently deletes the local PostgreSQL
dataset.
