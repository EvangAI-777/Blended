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

Loaded when editing the docs. Moved from CLAUDE.md "Key Documentation" in PR #253; the update process itself is `docs/codex-standard.md` (PR #256).

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

**Which docs a change updates** is the update matrix, step 4 of [`docs/codex-standard.md`](../../docs/codex-standard.md). Every change gets a CHANGELOG entry; any change to behavior, workflow, process or structure updates all four mandatory docs (`CLAUDE.md`, `CHANGELOG.md`, `BLENDED.md`, `.github/README.md`) in the same commit. This file covers where the content goes inside each doc and how to edit them.

## How to edit them

- **Read the whole file before editing a long one** (Scar 21). Edit one logical section per Edit call, never the whole document at once (Scar 5: stream idle timeouts).
- **Write from evidence** (Scar 6): screenshots, logs and crash logs are the ground truth. Write the version the evidence shows, even when it's less flattering.
- **Verify with specific artifacts** (Scar 14, compaction variant): to confirm something is recorded, grep for its commit hash, PR number or build number, not the general topic.
- **Fix a wrong thing; don't label it** (Scar 24). A wrong template with a warning note is still a wrong template.
- **Write `build 57`, never `build #57`** in PR descriptions and commit messages: GitHub links `#N` to PR N.
- **A new scar** goes in `docs/scars.md` with the same header as the others (when, impact, root cause, rule; blameless: what happened, not who), then the story, and gets a one-line rule in CLAUDE.md. **A new `wtf.md` note** goes at the end of `docs/wtf.md` and gets a row in its index; existing notes stay as written.
- **Maintainer-only notes in CLAUDE.md go in block HTML comments** (`<!-- ... -->`). Claude Code strips them before loading the file, so they cost no context.

## Consistency check *(Scar 7)*

The former Part 1 checklist is step 5 of [`docs/codex-standard.md`](../../docs/codex-standard.md): read the whole diff, make lists, versions, build and PR numbers agree, grep the four docs for stale references, verify by artifact, and fix everything before staging.
