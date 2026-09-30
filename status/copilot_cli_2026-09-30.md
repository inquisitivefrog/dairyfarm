# Copilot CLI status — 2026-09-30

## Major decisions

- Keep `ai-assisted` separate from `main`; do not merge the branches until the
  user decides to do so. Use this branch for ongoing AI-assisted development
  and validation.
- Run CI on pushes to both `ai-assisted` and `main`, as well as on pull
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
