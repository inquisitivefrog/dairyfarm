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

- The workflow update adds push validation for `ai-assisted`. GitHub Actions
  should run after this change is pushed; a run has not yet been observed.
