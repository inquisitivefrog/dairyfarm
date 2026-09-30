# Copilot CLI status — 2026-09-29

## Major decisions

- Complete the authentication, authorization, tenant-isolation, account
  credential, and deployment-safety changes together before committing them.
  The batch was committed as `cc88eed` (`Harden tenant boundaries and
  authentication`).
- Keep staff cross-tenant access intentional and restricted to trusted
  operators; ordinary users remain scoped to their own clients and records.
- Keep historical deployment credential revocation as an explicit operational
  task. No deployment was attempted, and no remote credentials were rotated.
- Add CI now for pull requests: build the API image, run the PostgreSQL-backed
  Django suite and system/migration checks, lint the SRE tools, review changed
  dependencies, and scan the current working tree for secrets.
- Keep CD disabled until the runtime and Django versions meet the deployment
  preflight. Once modernized, the intended promotion path is one immutable
  image through staging checks and approval to production.
- Store project decisions in tool-neutral, tracked repository notes rather than
  `~/.copilot/`, which is for personal preferences shared across projects.
- Keep operational status distinct from stable Copilot instructions: dated
  notes record decisions; repository instructions describe lasting project
  conventions.
- Pin workflow actions and scanner images to immutable revisions/digests;
  Dependabot can propose reviewed updates.

## Validation and limitations

- The security batch passed all 477 Django tests, `manage.py check`, and the
  migration dry-run check.
- Existing repository-wide flake8 reports a large legacy backlog. The initial
  CI gate therefore lints `sre-tools/`; broad application lint needs a separate
  baseline/cleanup decision.
- CI uses disposable, non-production credentials and does not deploy.
- Gitleaks scans the checked-out source tree, not Git history. Historical
  credentials still require out-of-band revocation, and GitHub secret scanning
  should be enabled separately in repository settings.
