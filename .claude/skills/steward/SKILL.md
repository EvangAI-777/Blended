---
name: steward
description: How Claude drives a Blended pull request from open to merged — Codex review loop, local checks, docs, merge and build hand-off. Read before acting on any PR event or check-in for a PR in EvangAI-777/Blended.
---

# Steward — PR handling for Blended

Repo-specific conventions for PRs Claude opens or drives. CLAUDE.md is the project's operational
context; this file covers only the PR loop.

## What "green" means here

- **PRs get the fast Checks workflow only** (`.github/workflows/checks.yml`, a few minutes:
  `tools/check_blended.py` and a workflow YAML parse). A red Checks run is work now, like any red
  CI. The Windows build (`build-windows.yml`) runs only on `workflow_dispatch` and `v*` tags, so
  it never runs on a PR. Never wait for it there.
- **The review signal is Codex** (`chatgpt-codex-connector[bot]`). It reviews when a PR opens and
  when someone comments `@codex review`. A clean pass is the receipt comment "Didn't find any major
  issues" or a 👍 reaction. Its summary comment shows `has_unresolved_findings`.
- A PR is ready for the developer when Codex's latest review of the **current head** is clean, all
  threads are answered and resolved, and GitHub reports it mergeable.

## Codex findings

1. **Verify every finding against the code before acting.** Trace a real caller or input to the
   failure. Codex has been right most of the time on this repo (PR #243/#244/#245), but not always:
   for example, operator properties can't hold data-block pointers (`docs/runtime-audit.md`, startup crash
   step 10).
2. **Real → fix it in this PR.** Badges (P1/P2) are not optionality labels. A P2 that is a real bug
   gets fixed like a P1.
3. **Not real → reply with the traced reason** and put the call to the developer. Don't build code
   for a far-fetched path.
4. After the fix is pushed, **reply on the thread** with the commit and what it changes, then
   **resolve the thread**, then comment `@codex review` (with the attribution footer).
5. Your own replies come back as events. Skip them.

## Before every push

Run the Codex Standard: CLAUDE.md "Before every commit" and, for docs, the Part 1 checklist in
`.claude/rules/docs.md`. The local checks that work in this
container:

- **Everything:** `python3 tools/check_blended.py` (the same checks the PR runs, about 15 seconds).
- **Workflows:** `actionlint` on `.github/workflows/*.yml` (`pip install actionlint-py` in a venv).
- **Python:** `python3 -m py_compile <file>`, then delete the `__pycache__` directories it creates.
- **C++:** there is no full build. Compile only the changed file with `g++ -fsyntax-only`, and run it
  once on `git stash`ed sources and once with the change. Only errors that appear with the change
  count. Some errors come from the container's libraries and are there both times.
- **YAML:** `python3 -c "import yaml; yaml.safe_load(open(path))"`.
- **RNA runtime code** (`rna_*.cc` under `RNA_RUNTIME`) only compiles through makesrna. Check names
  against the generated prototypes and existing patterns instead.

State plainly in the PR what could not be checked locally.

## Docs in the same PR

Any fix or finding that changes behavior updates the four mandatory docs (CLAUDE.md, CHANGELOG.md,
BLENDED.md, `.github/README.md`) in the same PR. That covers Category tables, the open-findings
section, status lines and the CHANGELOG contributor note.

## PR description

- Follow `.github/pull_request_template.md`.
- **The Test Plan covers every kind of testing the PR needs:** automated (what ran), build testing
  (the hardware test list for the next Windows build, **verbatim** as given to the developer in
  chat), developer testing (hands-on checks and calls beyond that list) and user testing when it
  applies. When the chat list changes, update the PR to match. Write "None" with the reason for a
  part that doesn't apply.
- When later commits change what the PR does (a Codex fix, a new commit), **rewrite the
  description** so it matches the final diff before handing the PR to the developer.
- Write `build 110`, never `build #110`.

## Branch

- Work on the session's designated branch. After its PR merges, restart the branch from
  `origin/main` (`git checkout -B <branch> origin/main`). A force push is fine only while the branch
  holds nothing but already-merged history.
- Before committing to an existing branch, check it hasn't already merged (CLAUDE.md, "The orphaned-commit trap").

## Merge and build

- **The developer merges.** Claude merges only when asked, using the full 40-character head SHA as
  `expectedHeadSha`.
- After a merge Claude did on request: unsubscribe from the PR and cancel its check-in. If the
  developer asked for a build, dispatch `build-windows.yml` on `main` with
  `inputs: {"build_type": "Release"}` and schedule one check on the result about 110 minutes out.
  A build takes 1.5–2 hours.
- A finished build goes to the developer for the hardware run: the `runtime-audit` skill. Their
  report starts the next triage loop.
