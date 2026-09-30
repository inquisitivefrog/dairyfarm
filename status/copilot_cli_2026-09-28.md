# Copilot CLI status — 2026-09-28

## Major decisions

- Treat the existing Docker setup as a local reproduction of the legacy app,
  not as a public deployment target. The app currently runs Python 3.6 and
  Django 2.0.1; deployment must wait for a supported runtime/framework upgrade.
- Keep the existing AngularJS UI for now rather than rewriting it for trend
  reasons. The HTTP/JSON boundary allows the backend to be modernized
  independently; remove avoidable risk such as loading AngularJS from a CDN.
- Use synthetic, isolated Django test data to check security invariants such as
  tenant isolation. This complements, but is distinct from, external production
  synthetics that continually test service availability and recovery.
- Apply tenant access rules using each client’s owner, with cross-tenant access
  reserved for trusted staff/support accounts. Add regression tests for both
  tenant separation and the staff exception.
- Treat historical demo credentials as compromised. Do not reuse them; fixture
  cleanup or source changes do not revoke accounts or credentials on an
  already-deployed service.
- Prioritize security findings by evidence, severity, and available remediation
  capacity rather than attempting to fix every scanner finding indiscriminately.
