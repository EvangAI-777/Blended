---
paths:
  - "CLAUDE.md"
  - "CHANGELOG.md"
  - "BLENDED.md"
  - "AGENTS.md"
  - "CONTRIBUTING.md"
  - "SECURITY.md"
  - ".github/README.md"
  - "docs/**/*.md"
  - ".claude/**/*.md"
---

# Editing the project documentation

Loaded when editing the docs. Moved from CLAUDE.md "Key Documentation" and the Codex Standard (Part 1) in PR #253.

## Where things go

**Document responsibility pattern** — for any structural change:

| What | Where it goes |
|------|--------------|
| Design rationale (*why* something is removed/changed) | `BLENDED.md` — the locked decision |
| Code progress (per-layer status, file lists) | `CHANGELOG.md` — *Unreleased* section |
| Claude AI contributor notes (what was built, per-session detail) | `CHANGELOG.md` — *Unreleased* section, same place as code progress |
| Always-true operational rules | `CLAUDE.md` (keep it under ~200 lines) |
| Rules that matter only for some files | `.claude/rules/*.md` with `paths:` |
| Multi-step procedures | `.claude/skills/*/SKILL.md` |
| Reference detail and history | `docs/` (`runtime-audit.md`, `scars.md`, `fork-reference.md`) |
| Implementation plans for Codex pre-audit (BLENDED.md §4) | a file under `docs/`, written at implementation resolution, pushed before the code |
| One-liner status for humans landing on GitHub | `.github/README.md` — "What's Different" section |

**Claude AI contributor notes go in CHANGELOG, not the README.** The README Contributors section is two sentences linking to CHANGELOG. All per-session implementation detail — what was built, what was removed, what scars were applied — belongs in the CHANGELOG *Unreleased* entry for that version, alongside the code progress rows. The README is a landing page.

**After every milestone or structural change, all four documents must be updated before the session ends.** The four are: `CLAUDE.md`, `CHANGELOG.md`, `BLENDED.md`, `.github/README.md`. Specific targets per document:
- **CLAUDE.md** — current version line updated, roadmap table row updated
- **CHANGELOG.md** — milestone note added; Claude AI contributor detail added to *Unreleased* section
- **BLENDED.md** — Status line updated; relevant sections updated
- **`.github/README.md`** — version/status sentence updated

## How to edit them

- **Read the whole file before editing a long one** (Scar 21). Edit one logical section per Edit call, never the whole document at once (Scar 5: stream idle timeouts).
- **Write from evidence** (Scar 6): screenshots, logs and crash logs are the ground truth. Write the version the evidence shows, even when it's less flattering.
- **Verify with specific artifacts** (Scar 14, compaction variant): to confirm something is recorded, grep for its commit hash, PR number or build number, not the general topic.
- **Fix a wrong thing; don't label it** (Scar 24). A wrong template with a warning note is still a wrong template.
- **Write `build 57`, never `build #57`** in PR descriptions and commit messages: GitHub links `#N` to PR N.
- **Maintainer-only notes in CLAUDE.md go in block HTML comments** (`<!-- ... -->`). Claude Code strips them before loading the file, so they cost no context.

## Part 1 — Documentation Consistency *(Scar 7)*

*Applies to every commit touching CLAUDE.md, CHANGELOG.md, BLENDED.md, or any file with cross-references, ordered lists, version maps, or architectural decisions.*

1. **Run `git diff` and read the entire output.** Not a skim. Every line.
2. **For every ordered list in the diff, find every other representation of that same order in the diff and in the touched files.** All representations must agree.
3. **For every statement of the form "do X last / first / never / always," grep the diff for X.** Verify nothing else in the same diff contradicts it.
4. **For every version number mentioned, verify it matches the version map in CHANGELOG.md.**
5. **Search all sections within each of the four mandatory docs for stale references to the version or milestone being updated.** The headline status lines (CLAUDE.md "Current version", BLENDED.md "Status", README "Currently at") are obvious. The non-obvious ones are harder: internal roadmap tables, mid-document planning sections, version-specific subsection headers. `grep -n "0\\.X" CHANGELOG.md` (replace X with the version) will surface every reference — update all of them, not just the first one. The 0.6.0 design session caught a stale `### 0.6.x — Evaluation model` planning block at CHANGELOG.md:706 and a stale `In progress` status in the CLAUDE.md roadmap table — both invisible to a headline-only pass.
6. **Fix any inconsistency before staging.** Not after. Not in a follow-up commit. Before.

*Why: Scar 7 — chisel order corrected in prose but left wrong in the same commit's table. A bot caught it.*
