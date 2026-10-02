# Copilot CLI status — 2026-10-01

## Current local application

- Repository: `/Users/tim/Documents/workspace/python3/dairyfarm`, branch
  `ai-assisted`; local Compose app runs at <http://localhost:8000/>.
- Local stack uses the legacy Python 3.6.15 / Django 2.0.1 app with PostgreSQL,
  Memcached, and an Nginx static UI proxy. It is local-only and not safe for
  public deployment.
- The local database has three principal demo logins in use: `foster`,
  `berkeley`, and `ai-managed`. The AI-managed login owns the separate
  synthetic 2019–2026 farm and has a user-set password; do not record it here.
- The synthetic AI-managed data is explicitly separate from original fixtures.
  Its repeatable loader now generates varying annual/monthly milk totals and
  illness/injury health records. The local database was reloaded with this
  varied dataset on Oct 1.

## Completed during this session

- Added farm-local **Herd #** display to the cow list, preserving global
  database IDs for detail links. The shared page numbers from 1 for each farm
  and carries numbering across pagination. API ordering is by cow ID.
  New assets are `demo/static/templates/cow_list_herd.html` and
  `demo/static/js/farmAppCowListByClientCtrlHerd.js`; `farmApp.js` routes to the
  new template. The API tenant-isolation test class passed (17 tests).
- Fixed annual/monthly report links to use the farm/client ID rather than the
  report row ID. Recalculated the 10 annual and 102 monthly saved reports for
  all clients so existing links are repaired. Confirmed the AI-managed 2019
  link returns all 12 months.
- Monthly API results now sort by month number and serialize month names.
  Confirmed Jan–Dec order and passed the targeted synthetic dataset, summary
  API, and serializer tests (31 tests).
- Updated Marketing Requirements document internal section links to preserve
  the Angular route and target valid anchors. New static template:
  `demo/static/templates/docs_mrd_links.html`; matching app route is in
  `demo/static/js/farmApp.js`.
- Restructured the desktop layout into independently scrolling sidebar and
  document panes. Added nested navigation links for the Marketing
  Requirements, Assets Design, and Reporting Design documents. Fixed malformed
  document TOC wrappers that had caused all content to remain hidden, added a
  `ClientSelectionController.openDocumentation` handler to load and scroll
  within the document pane, and left-aligned/indented the hierarchy. Updated
  stylesheet cache URL to `?v=document-sidebar-2` and added
  `?v=document-scroll-1` for the controller script.
- The latest API and UI images were rebuilt successfully after Docker Hub
  connectivity recovered. The served app shell and assets were checked, and
  all configured sidebar section links were matched against IDs in their
  documents. **The latest layout/navigation still needs a browser-level
  confirmation**: user reported that document and section selection did not
  display content; the code now addresses the malformed wrappers and handles
  pane scrolling, but there was no follow-up screenshot after this fix.

## Verification

- Full Django test suite last passed with **478 tests** after the synthetic
  data improvements, before today’s report serializer and documentation
  navigation edits.
- After report changes, targeted tests passed: synthetic dataset, summary API,
  and summary serializers (31 tests).
- After the current documentation navigation changes, `node --check` on
  `farmAppClientSelectionCtrl.js`, a parser-based check for valid section
  targets/outside-TOC placement, and `git diff --check` passed. The full suite
  has not been rerun since these changes.
- `python manage.py check --deploy` on the local legacy app reported expected
  development warnings: missing HSTS, HTTPS redirect disabled, insecure
  session/CSRF cookies, and `DEBUG=True`.

## Deferred modernization work

- The documented SQLite/Django compatibility issue remains: fixture tests on
  newer SQLite can fail with `no such table: main.auth_user__old`; the
  PostgreSQL-backed suite passes. See `docker/README.md`.
- Python dependency modernization remains planned, not started. Current
  requirements pin Django 2.0.1, Django REST Framework 3.7.7, psycopg2 2.7.3.2,
  python-memcached 1.59, pytz 2017.3, six 1.11.0, and old dev/lint tools. The
  planned path is a staged upgrade (candidate Python 3.13 and Django 5.2 LTS),
  replacing deprecated imports/routes as the framework upgrade exposes them;
  do not blindly bump all pins.
- A repository search found no standalone website probing script. The existing
  `sre-tools/deployment_preflight.py` checks deployment runtime/configuration
  and Django deployment checks; it is not an HTTP route probe.

## Worktree cautions

- The worktree contains numerous pre-existing user changes, deletions, and
  untracked files, including Docker/dependency edits, docs, fixture and image
  changes, and `.icloud` placeholders. Preserve them; do not revert broad
  changes or assume every dirty file is part of the latest task.
- The currently changed documentation files and static files include renamed
  or newly created assets listed above. Review `git status --short` before
  staging anything.
- No cloud host was selected and no cloud deployment was performed.
