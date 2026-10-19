# The Codex Standard — the update process

Every change to this repository is a cut in the chiseling (BLENDED.md §4) and follows these steps,
in this order, every time, whatever the size: code, docs, CI, a one-line fix. Ask at each step: *would Codex catch this?* Then catch it
first. A step that doesn't apply is skipped on purpose, never by forgetting. Refer to items by
number ("Codex Standard 3.2").

Consolidated in PR #256 from what had been spread across CLAUDE.md, `docs/scars.md` (Part 2),
`.claude/rules/docs.md` (Part 1), the `steward` skill and the four-docs rule. This file is the one
place the process lives; the others point here. The stories behind the rules are in
`docs/scars.md`.

**Index**

| Step | When | What |
|------|------|------|
| [1. Start](#1-start) | Before the first edit | Branch, todo list, read before editing |
| [2. Code](#2-code) | Code, scripts or CI changed | Local checks and the code questions |
| [3. Tests](#3-tests) | Behavior changed | Where each new check goes |
| [4. Docs](#4-docs) | Every change | The update matrix: which docs each kind of change touches |
| [5. Consistency](#5-consistency) | Every change that touches docs | Read the diff; lists, versions and references agree |
| [6. Commit and push](#6-commit-and-push) | Every logical unit | Message, push now |
| [7. Pull request](#7-pull-request) | Every push to a PR | Template, Test Plan, description, Codex |
| [8. Merge, build and session end](#8-merge-build-and-session-end) | After merge, after a build, before the session ends | Branch reset, build lists, what the next session needs |

The Codex Standard is an item on the todo list before every commit, never after (CLAUDE.md,
"Session discipline").

---

## 1. Start

- **1.1 Branch.** `git fetch origin main`. If the session branch already merged, restart it from
  `origin/main` before writing anything (the orphaned-commit trap, `docs/scars.md`). If its PR is
  still open, keep committing to it.
- **1.2 Todo list.** Three or more steps means a list, one item per step, marked done the moment
  it's done. This process is one of the items.
- **1.3 Read before editing.** Read a whole file before editing it if it's longer than ~200 lines
  (Scar 21). Edit one logical section per Edit call (Scar 5). Revert a botched edit instead of
  fixing forward.
- **1.4 Write from evidence** (Scar 6). Screenshots, logs and crash logs are the ground truth.

## 2. Code

Run what applies. State in the PR what could not be checked in this container.

- **2.1 `python3 tools/check_blended.py`.** Always; it's the same check the PR runs.
- **2.2 C++:** `g++ -fsyntax-only` on each changed file, once on `git stash`ed sources and once
  with the change; only new errors count (some come from the container's libraries and appear both times). RNA runtime code compiles only through makesrna: check
  names against the generated prototypes instead.
- **2.3 Python:** `python3 -m py_compile <file>`, then delete the `__pycache__` it creates.
- **2.4 Workflows:** `actionlint` on `.github/workflows/*.yml` (`pip install actionlint-py` in a venv); `.claude/rules/workflows.md` (SHA
  pins, no `${{ }}` in `run:`, least privilege).
- **2.5 YAML:** `python3 -c "import yaml; yaml.safe_load(open(path))"`.
- **2.6 The code questions.** Answer each that applies, yes or no:
  - Did I over-delete? A file with ID-system glue and runtime logic loses only the glue (Scar 1).
  - Does every deregistered ID type still avoid the generic ID APIs, and does `which_libbase`
    still route its listbase (Scars 2, 10; `.claude/rules/id-types.md`)?
  - For every new or rewritten `.cc`: is there an `#include` for each API I call
    (`MEM_guardedalloc.h` for `MEM_new`)?
  - After a rename: `grep -rn "old_name" . --exclude-dir=.git` returns nothing (Scar 20).
  - A format or type-flag change: did I cover what writes it, what reads it, and what classifies
    files by the flag (Scar 22)? When a grep returns several hits in a file, did I read every one?
  - Identity work: did I check artifact names (`OUTPUT_NAME` per platform), not just UI strings
    (Scar 26)?
  - Did I fix each wrong thing I found instead of labeling it (Scar 24)?
  - Is this a menu about something plainly wrong? Then fix it instead (Scar 14).

## 3. Tests

- **3.1 Source-detectable bug class** → a check in `tools/check_blended.py`, tested against a
  planted violation.
- **3.2 Runtime check that doesn't need a window** → `tests/python/blended_smoke_test.py` (CI),
  not the developer's hardware list.
- **3.3 Needs a window** → the build testing part of the PR's Test Plan (step 7.2) and the open
  runtime checks in `docs/runtime-audit.md`.
- **3.4 A new rule or check** → run it against the whole codebase in the same session (Scar 25).

## 4. Docs

Every change gets a CHANGELOG entry. Then every row that matches the change applies; most
changes match more than one.

| The change | Update |
|------------|--------|
| **Any change** | `CHANGELOG.md` *Unreleased*: a note on what changed and why, with PR number; a "Claude AI contributor" note for the session's work. |
| **Behavior, workflow, process or structure** (code that changes what the program does, a CI change, a new rule, a new procedure) | All four mandatory docs: `CLAUDE.md` (the current-version line or roadmap row if status changed; a rule line if it's an always-true rule), `CHANGELOG.md`, `BLENDED.md` (the Status line, and the section the change belongs to, e.g. §4 for methodology), `.github/README.md` (the status sentence, or a line in the section it belongs to). |
| **A build result or hardware finding** | `docs/runtime-audit.md` (verified list, findings, open checks, Categories A–D) and the status lines in CLAUDE.md, BLENDED.md and the README. |
| **A design decision, or one under discussion** | `BLENDED.md`, in the section it belongs to; an undecided one is marked "under discussion", and the code doesn't change until it's decided. |
| **A version bump** | The `version-bump` skill: the header plus all four docs in one commit. |
| **A review rule Codex should apply** | `AGENTS.md`, kept consistent with CLAUDE.md. |
| **The PR loop, the template or how testing is recorded** | The `steward` skill, `.github/pull_request_template.md`, CONTRIBUTING.md. |
| **The build hand-off or triage** | The `runtime-audit` skill. |
| **Rules for one kind of file** | `.claude/rules/*.md` with `paths:`. |
| **An upstream divergence** | The divergence register in `docs/upstream-sync.md`. |
| **A failure that produced a rule** | A new scar in `docs/scars.md` (blameless header), a one-line rule in CLAUDE.md, and the rule in this file if it's a check. |
| **Something about working with the developer** | A new note at the end of `docs/wtf.md`, with an index row. Existing notes stay as written. |
| **Something the next session needs** | The doc it belongs to, before the session ends, not just the chat. |

Placement within each doc follows `.claude/rules/docs.md` ("Where things go"). CLAUDE.md stays
under ~200 lines.

## 5. Consistency

*Scar 7. For every commit that touches docs, or any file with cross-references, ordered lists,
version maps or decisions.*

- **5.1 Read the whole `git diff`.** Every line, not a skim.
- **5.2 Ordered lists:** every representation of the same order, in the diff and the touched
  files, agrees.
- **5.3 "Always / never / first / last" statements:** grep the diff for the subject; nothing in
  it contradicts them.
- **5.4 Versions** match the version map in CHANGELOG.md. **Build numbers, PR numbers, commits
  and dates** match across every file that names them; dates come from the CHANGELOG headings.
- **5.5 Stale references:** grep all four mandatory docs for the version, milestone, build or
  wording being changed (`grep -n "0\.X" CHANGELOG.md`), not just the headline status lines.
  Roadmap tables, planning blocks and subsection headers hide them.
- **5.6 Verify by artifact** (Scar 14): to confirm something is recorded, grep its commit hash, PR
  number or build number, not the topic.
- **5.7 Fix every inconsistency before staging.** Not in a follow-up commit.

## 6. Commit and push

- **6.1 One logical unit per commit, pushed immediately** (Scar 3). Never hold unpushed commits.
- **6.2 The message** says what changed and why. Write `build 57`, never `build #57`. End with the
  attribution lines. No model identifiers.
- **6.3 Commit before anything risky**, so there's a clean base to return to.

## 7. Pull request

- **7.1 Template.** Fill in `.github/pull_request_template.md`. When later commits change what
  the PR does, rewrite the description to match the final diff, including the commit table.
- **7.2 Test Plan, four parts** (BLENDED.md §4 "Test plans"): automated (what ran), build testing
  (the hardware tests for the next Windows build, written before merge in the chat-list form),
  developer testing, user testing where it applies. "None" with the reason for a part that
  doesn't apply.
- **7.3 Codex.** After each push, comment `@codex review` (with the attribution footer). Verify
  each finding against the code; fix real ones in the same PR, answer the rest with the traced
  reason. Reply on each thread with the commit, then resolve it. A PR is ready when Codex's latest
  review of the current head is clean, all threads are resolved, and GitHub reports it mergeable.
  The `steward` skill has the full loop.

## 8. Merge, build and session end

- **8.1 Merge** only when the developer asks, with the full head SHA. Then unsubscribe from the PR
  and restart the branch from `origin/main`.
- **8.2 Build hand-off** (`runtime-audit` skill): the test list goes to the developer in chat and,
  verbatim, as a comment on each merged PR the build carries; record the build result per step 4.
- **8.3 Session end:** anything the next session needs is written into the doc it belongs to
  (step 4, last row).
