# How to work in this repo (Claude)

- Make small, focused diffs; modify only touched hunks.
- Tests: run the project's test command before finalizing (set below).
- For any infra/API/IaC/auth change, FIRST call `ref.search_documentation`
  and cite the doc URL with a 2–3 bullet summary.
- Use tools with `response_format="concise"` unless IDs are required.
- Prefer the output shape: PLAN → PATCH → TESTS → RUN → RISKS.
- Avoid full-file pastes; prefer `git.diff` and line-scoped reads.

## Project Commands (adjust per project)
- Python: tests `pytest -q`, lint `ruff check .`, types `mypy .`
- JS/TS: tests `npm test`, lint `eslint .`, types `tsc --noEmit`