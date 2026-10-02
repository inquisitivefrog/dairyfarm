# Copilot instructions for dairyfarm

## Build, test, and lint

This repository is a legacy Django application. Run commands from the `demo/` directory unless otherwise noted.

- Full Django test suite:
  - `cd demo && python manage.py test`
- Quick validation / startup sanity check:
  - `cd demo && python manage.py check`
- Single test module or case:
  - `cd demo && python manage.py test assets.tests.test_views`
  - `cd demo && python manage.py test assets.tests.test_views.TestIndexView`
  - `cd demo && python manage.py test summary.tests.test_api_views`
- Linting:
  - `cd demo && flake8 .` (the repo includes `flake8` in `requirements.txt`)

For a fresh local setup, the project README indicates using a virtualenv and installing the repo requirements before running Django commands:

- `python3 -m venv <venv>`
- `source <venv>/bin/activate`
- `pip install -r requirements.txt`
- `cd demo && python manage.py test`

## High-level architecture

The project is a Django + Django REST Framework app for managing a dairy farm inventory and reporting system.

- `demo/` is the Django project root:
  - `demo/settings.py` configures the app, sqlite database, DRF, auth, and static files.
  - `demo/urls.py` mounts the main URL routes for the app and admin.
  - `demo/views.py` contains the top-level UI and auth-related views.
- `assets/` is the main domain app.
  - `assets/models.py` defines the core inventory and operational records: clients, cows, breeds/colors, events, milk, exercise, pasture/seed, health records, etc.
  - `assets/api_views.py` contains the REST API endpoints and business filtering rules (by client, year, month, etc.).
  - `assets/serializers.py` has read/write serializer pairs for most models; when adding API behavior, match this split instead of inventing a new pattern.
  - `assets/tests/` contains app-specific tests for models, serializers, API views, URLs, and page views.
- `summary/` is the reporting layer.
  - `summary/models.py` stores summary records for annual and monthly client reporting.
  - `summary/api_views.py` exposes summary endpoints.
  - `summary/constants.py` / `summary/helpers.py` centralize year/month metadata and report stats.
- Frontend is served as static AngularJS assets rather than a separate frontend app.
  - `demo/static/js/` contains the Angular controllers and services.
  - `demo/static/templates/` contains the server-rendered HTML templates consumed by the Angular app.
  - The main entry point is the Django view + static template flow, not a modern SPA build step.
- Data fixtures live under `demo/demo/fixtures/` and are used in tests (`fixtures = [...]` in test classes).

## Key conventions in this codebase

- This is a legacy Django 2.0 / DRF 3.x codebase. Some files still use older Django patterns such as `django.conf.urls.url` instead of `path()`, and older generic class patterns. Follow the surrounding file style rather than modernizing unrelated code.
- Model classes routinely override `save()` to compute and persist generated `link` URLs after the instance is created. If you add a model or update a save path, preserve that pattern when a resource needs a canonical URL.
- The repo uses separate read/write serializer classes for many resources (for example `CowReadSerializer` / `CowWriteSerializer`, `EventReadSerializer` / `EventWriteSerializer`). When adding or changing an API schema, keep the same pattern unless the surrounding code clearly defines a different convention.
- API filtering is heavily route-driven. Many endpoint patterns are parameterized by `client`, `year`, `month`, and `pk`, and tests often exercise those URL conventions directly.
- The app is fixture-heavy. Tests frequently rely on preloaded fixtures and Django `APITestCase`, not isolated factories.
- The project keeps business logic in Django model / API view layers, while the UI is mostly static HTML plus AngularJS controllers.
- Respect the app boundaries: domain models and endpoints live in `assets`, reporting logic lives in `summary`. Avoid adding ad hoc report logic to the wrong app.

## Working style and scope notes

- Prefer surgical changes that match existing patterns in neighboring files.
- When a bug or feature touches both API and UI, check the corresponding Django app and Angular template/controller together; the repo’s behavior is split between them.
- Do not assume a modern Node/React toolchain is present. The project is Python/Django-based and uses static JS assets.
