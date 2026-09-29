# Local Docker baseline

This Compose setup reproduces the current application locally; its Python 3.6
image and Django dependencies are obsolete and must not be used for a public
deployment.

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
Django's test database and does not seed the demo dataset. The Compose
PostgreSQL database starts empty; safe demo account/data setup is a separate
follow-up and is not performed by container startup.

At this baseline, the full PostgreSQL test run reports 47 fixture setup
errors: 36 attempts to load `demo/demo/fixtures/client.json` fail because a
client name exceeds the model's `max_length=20`, and 11 attempts to load
`demo/demo/fixtures/treatment.json` fail because a treatment name exceeds its
`max_length=20`. SQLite had allowed these fixture values, so this identifies
database-specific data/model mismatches to investigate before treating
PostgreSQL as interchangeable with SQLite.

The legacy SQLite test baseline has a separate failure on newer SQLite:
fixtures can fail with `no such table: main.auth_user__old`. A focused class
passed when SQLite's `legacy_alter_table` behavior was enabled in an isolated
container. This is a Django 2.0/SQLite compatibility observation, not a
workaround enabled by this Compose setup.

## Demo data and cleanup

The historical data setup scripts create accounts with hard-coded passwords,
including a superuser. Do not use those accounts for a public deployment. Review
the script before running it, and do not run `demo/tools/reset` or
`demo/tools/stress`: they delete the local SQLite database and migration files.

`docker compose down` stops the services while retaining PostgreSQL data.
Removing the `postgres-data` volume permanently deletes the local PostgreSQL
dataset.
