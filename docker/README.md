# Local Docker baseline

This Compose setup reproduces the current application locally; its Python 3.6
image and Django dependencies are obsolete and must not be used for a public
deployment.

## Deployment preflight

Before considering a public deployment, run
`python sre-tools/deployment_preflight.py` inside the deployment image. It exits
nonzero unless the runtime is at least Python 3.10 / Django 5.2,
`DJANGO_ENVIRONMENT=production`, `DEBUG` is disabled, allowed hosts and a
generated secret are configured, a non-SQLite database is used, secure
cookies/HTTPS redirect/HSTS are enabled, and Django's deployment checks pass.
The current legacy image is expected to fail this gate; do not disable the
checks to force a deployment.

Configure production security settings through `DJANGO_SECURE_SSL_REDIRECT`,
`DJANGO_SESSION_COOKIE_SECURE`, `DJANGO_CSRF_COOKIE_SECURE`, and
`DJANGO_HSTS_SECONDS`. Enable HSTS only after HTTPS is correctly configured
for the domain and its subdomains.

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

The legacy SQLite test baseline has a separate failure on newer SQLite:
fixtures can fail with `no such table: main.auth_user__old`. A focused class
passed when SQLite's `legacy_alter_table` behavior was enabled in an isolated
container. This is a Django 2.0/SQLite compatibility observation, not a
workaround enabled by this Compose setup.

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
