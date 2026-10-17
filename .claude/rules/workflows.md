---
paths:
  - ".github/workflows/**"
  - ".github/dependabot.yml"
  - "tools/check_blended.py"
  - "tests/python/blended_smoke_test.py"
---

# GitHub Actions workflows and CI checks

Loaded when editing CI. Rules from PR #252 (repository standards); background in CHANGELOG.md.

- **Pin every action to a full 40-character commit SHA**, with the version in a trailing comment (`uses: actions/checkout@<sha> # v5.1.0`). Resolve annotated tags to the commit with `git ls-remote <repo> 'refs/tags/vX.Y.Z^{}'`. Dependabot (`.github/dependabot.yml`) opens monthly update PRs.
- **Prefer Node 24 majors.** GitHub retired Node 20 on hosted runners in 2026; check an action's runtime in its `action.yml` (`runs.using`) before choosing a version.
- **Never put `${{ }}` expressions straight into a `run:` block** (script injection). Pass them through `env:` and read `"$VAR"` in the script; validate user input (for example `git check-ref-format`).
- **Least privilege.** Workflow-level `permissions: contents: read`; a job asks only for what it needs. Only the tag-only `release` job in `build-windows.yml` has `contents: write`. `actions/checkout` uses `persist-credentials: false` unless a later step pushes.
- **Don't let CI changes cost a build's artifact.** In `build-windows.yml` the artifact upload comes before anything optional (provenance runs after it with `continue-on-error` outside tags). A broken workflow is only found by the next 2-hour build, so keep steps that can fail late and non-fatal where possible.
- **Validate locally before pushing:** `actionlint` (`pip install actionlint-py` in a venv) on `.github/workflows/*.yml`, and `python3 tools/check_blended.py`.
- **`tools/check_blended.py`** runs on every PR (`checks.yml`). When a new class of runtime bug can be caught from source, add a check there, run it against the whole tree in the same PR (Scar 25), and test it against a planted violation.
- **The smoke test** (`tests/python/blended_smoke_test.py`) runs the packaged build headless in `build-windows.yml`; anything that needs a window stays on the hardware checklist in `docs/runtime-audit.md`.
