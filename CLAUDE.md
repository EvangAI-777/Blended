# CLAUDE.md — Blended Project Context

Blended is a fork of Blender 5.2 (GPL-2.0-or-later) being rebuilt from the foundation up.

**Read `BLENDED.md` first.** It is the design authority — identity, architecture, datablock audit, pipeline specs, locked decisions, open questions, and guardrails. This file is operational context for Claude sessions: what's been built, what the patterns are, what not to repeat.

**Current version:** Blended 1.0.0-dev — 0.9.0 base: CI-complete (Windows x64, build 101, commit `c8e87078`). Third first-try on the project. 0.9.0 delivered: `.blend` import ✓ — OB_MBALL versioning pass 502.31, `BKE_main_clear` Scar 2 drain (PA/TE/CU/LS), `BKE_screen_blend_read_data` deletion, dropped-data manifest Text block. Layer 3 post-read LS drain removed — Codex catch PR #229. 1.0.x: foundation complete — two sequential phases: Phase 1 runtime audit (developer runs build, checklists, triage loop with Claude) in progress — build 103/104/106 crashes diagnosed and fixed, build 107 empty crash log fixed (PR #242) and verified on hardware in build 108 — first real backtrace of the startup crash; root cause identified (`wm_add_default` workspace/screen bootstrap), launcher-bootstrap fix (PR #244) verified on hardware in build 109 — Blended reaches its own UI (the launcher) for the first time; build 109 findings (bl_ui syntax error → navigate-gizmo crash, window manager refining to plain `ID` in RNA) fixed and verified on hardware in build 110; build 110 findings (File > Open crash when the file browser closes, upstream splash over the launcher, Cycles `MetaBall` registration error, empty launcher keymap, spurious "loading empty scene" warning) fixed, awaiting build verification. Category D table updated. CI now smoke-tests each packaged build headless (`tests/python/blended_smoke_test.py`), and every PR runs fast source checks (`tools/check_blended.py`; PR #252, which also hardened the workflows and fixed a latent render-curve crash the check found). Phase 2 GitHub Pages launch pending Phase 1 completion. Release tag when both phases clear.

---

## Runtime Audit (Phase 1)

The runtime audit reference lives in [`docs/runtime-audit.md`](docs/runtime-audit.md): the audit protocol, the open runtime checks, the Known Runtime Artifacts (Categories A–D: expected changes, resolved crash paths, leaks, fixed crashes) and the build-by-build findings. **Check it before assuming a new bug.** When a build report comes in, use the `runtime-audit` skill.

### Foundation Layer Roadmap

| Version | Layer | Status |
|---------|-------|--------|
| 0.4.x | Datablock audit — 9 fossil removals (Bucket 5+6) | ✓ CI-complete (build 70) |
| 0.5.x | Datablock audit — complete (Bucket 3 fold-downs; 39 → ~19 ID types) | ✓ CI-complete (build 81, commit `d6ee8478`) |
| 0.6.x | Evaluation model — close seam between declared ~19-type world and depsgraph/draw/editor dispatch; ~95 hits audited: ~71 live fold-down dispatch (stays), 5 OOB guards (confirm permanent), 2 EEVEE →true workarounds (resolve), 5 dead-code refs (remove) | ✓ CI-complete (build 82, commit `8f7dda22`) |
| 0.7.x | App lenses — launcher (§11), all 28 mode lenses (§12), full product identity (§16), `.blended` format design. Two phases: skeleton first, aesthetic second. | ✓ CI-complete (build 99, commit `2ddd1dd0`). Phase 1 + Phase 2 complete. Logo ✓ + accent ✓ (`#ff7f00`) + app icon ✓ + splash ✓. |
| 0.8.x | File format — `.blended` is the project, import/export is the boundary | ✓ CI-complete (build 100, commit `99e20b96`). First try. Magic bytes `"BLENDED"`, 23 layers, ~80 sites, platform integration, all tests green. |
| 0.9.x | `.blend` import — seamless read with dropped-data manifest output | ✓ CI-complete (build 101, commit `c8e87078`). Third first-try on the project. OB_MBALL versioning pass, Scar 2 drain (PA/TE/CU/LS), manifest Text block, dead-code deletion. |
| 1.0.0 | Foundation complete. Two sequential phases: (1) runtime audit — developer runs build, reports findings, Claude triages and fixes; (2) GitHub Pages — polished marketing + tech demo site, WASM interactive demo as stretch goal. Release tag when both phases clear. | In progress |
| 1.1.0+ | Post-1.0 roadmap (minor versions). First entry: user workspaces — decide where they live (BLENDED.md §9 item 10), give them an owner, re-enable Duplicate/Delete/Reorder/Cycle. Plan in CHANGELOG.md "Post-1.0 roadmap". | Planned |

---

## Repository Layout

| Directory | Contents |
|-----------|----------|
| `source/blender/` | C++ modules: blenkernel, gpu, draw, editors, makesdna, makesrna, etc. |
| `intern/` | Internal libs: Cycles, Ghost, OpenVDB, OpenSubdiv, MantaFlow, LibMV |
| `scripts/startup/` | Python startup scripts — Blended-specific ones are prefixed `blended_` |
| `scripts/addons_core/` | Official add-ons: FBX, glTF2, Rigify, Node Wrangler, etc. |
| `build_files/cmake/config/` | Build configs incl. `blended_release.cmake` |
| `tests/` | GTests (C++), Python tests (`tests/python/`) |
| `release/` | Platform packaging: Windows `.rc`, Linux `.desktop`, icons, datafiles |

**Upstream sync conflict-prone files:** `BKE_blender_version.h` (we added `BLENDED_VERSION_*`), `CMakeLists.txt` (project name), `wm_window.cc`, `wm_splash_screen.cc`, and all branding/release files. Check `UPSTREAM_SYNC.md` before merging upstream Blender releases.

---

## Build Commands

```bash
# Desktop builds
make debug          # Debug binary
make release        # Release with all options
make lite           # Smaller binary, faster build (not used by CI — the workflow has no branch-push trigger)
make ninja          # Use Ninja instead of Make
make ccache         # Use ccache for faster rebuilds

# Blended release build (used by CI for tag/manual runs)
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -C build_files/cmake/config/blended_release.cmake
cmake --build build --target install

# Testing
make test           # Run ctest
make check_pep8     # Python PEP8
make check_cppcheck # Static analysis
make check_mypy     # Python type checking
```

---

## Coding Conventions

| Language | Indent | Line Limit | Style | Enforced By |
|----------|--------|------------|-------|-------------|
| C/C++ | 2 spaces | 99 chars | `snake_case`, `#pragma once`, SPDX headers | `.clang-format` |
| Python | 4 spaces | 120 chars | PEP8, autopep8 aggressive=2 | `pyproject.toml` |
| CMake | 2 spaces | 99 chars | lowercase commands | `.editorconfig` |
| GLSL | 2 spaces | 99 chars | follows C conventions | `.editorconfig` |

- **C/C++ function prefixes**: `BKE_*` (blenkernel), `BLI_*` (blenlib), `ED_*` (editors), `WM_*` (window manager), `RNA_*` (runtime data), `DNA_*` (stored data)
- **C++ namespaces**: `blender::module::submodule` pattern
- **SPDX headers**: Every file starts with `/* SPDX-FileCopyrightText: ... */` and `/* SPDX-License-Identifier: GPL-2.0-or-later */`
- **Header guards**: `#pragma once` (not `#ifndef` guards)

---

## Fork-Specific Patterns (What Makes Blended Different)

### Branding, rig compatibility, update checker

Publisher: **CHJ 3 Productions LLC** (Indiana); upstream code keeps its Blender Foundation copyright under GPL-2.0-or-later. Code locations for the branding, `scripts/startup/blended_rig_compat.py` (pre-5.0 `action.fcurves`) and `scripts/startup/blended_update_check.py`: [`docs/fork-reference.md`](docs/fork-reference.md).

### CI / Build Config
- `.github/workflows/build-windows.yml` — triggers only on `v*` tag pushes and manual `workflow_dispatch` (PRs and pushes to `main` get only the Checks workflow below; other branch pushes run nothing). Full release build → artifact → build-provenance attestation → headless smoke test of the packaged build (`tests/python/blended_smoke_test.py`: startup, Python startup scripts, window-manager RNA, File > Open of a legacy `.blend`, Save As `.blended` and reopen). On tags, a separate `release` job (the only one with write access) publishes the zip and its `.sha256`. Read-only token by default; one build per ref at a time (a second dispatch queues).
- `.github/workflows/checks.yml` — on every PR to `main`, pushes to `main` and dispatch, a few minutes on Linux: `tools/check_blended.py` (Python syntax of `scripts/`, the Cycles add-on and `tests/python`; `BKE_libblock_alloc`/`BKE_id_new` with a deregistered ID type; `bpy.types` references to removed RNA types; `LISTBASE_FOREACH` outside `listbase.cc`) and a YAML parse of `.github/`. Run `python3 tools/check_blended.py` locally before pushing. When a new class of runtime bug can be caught from source, add a check there.
- Every action in `.github/workflows/` is pinned to a full commit SHA with the version in a trailing comment. `.github/dependabot.yml` opens monthly update PRs. Never put `${{ }}` expressions straight into a `run:` block; pass them through `env:` (script injection).
- `build_files/cmake/config/blended_release.cmake` — inherits `blender_release.cmake`, disables `WITH_CYCLES_CUDA/HIP/ONEAPI_BINARIES` and `WITH_FREESTYLE`

### Version Management

`source/blender/blenkernel/BKE_blender_version.h` (`BLENDED_VERSION_MAJOR/MINOR/PATCH`) is the single source of truth; the CI artifact name comes from it. Bump MINOR on the first commit of a new dev cycle, PATCH for fixes within one; from 1.0.0 on, standard semantic versioning. Every bump updates the four mandatory docs in the same commit. The full procedure and checklist: the `version-bump` skill.

### Datablock Audit — Complete (BLENDED.md §10)

39 → ~19 ID types; all buckets closed. Per-type detail: [`docs/fork-reference.md`](docs/fork-reference.md) and BLENDED.md §10.

## Battle Scars, Philosophy, Session Discipline

Moved out of this file verbatim in PR #253:
- The full scars (Scars 1–26, the note for the next version of you, the full Codex Standard), session discipline and the full PR instructions: [`docs/scars.md`](docs/scars.md).
- The Development Philosophy: [`BLENDED.md`](BLENDED.md), "Appendix — Development Philosophy".

---

## Key Documentation

| Document | Purpose |
|----------|---------|
| `BLENDED.md` | **Read first.** Design authority — identity, architecture, locked decisions |
| `CLAUDE.md` | This file — operational context for Claude sessions |
| `CHANGELOG.md` | Release record + versioned roadmap + Unreleased section for in-flight work; Claude AI contributor detail |
| `.github/README.md` | GitHub landing page — one-liner status per active item; use `git add -f` to stage (in `.gitignore`) |
| `wtf.md` | Who the developer is and how to work with them (moved out of `CLAUDE.md` on 2026-10-16) |
| `UPSTREAM_SYNC.md` | How to merge upstream Blender, conflict-prone files |

**Document responsibility pattern** — for any structural change:

| What | Where it goes |
|------|--------------|
| Design rationale (*why* something is removed/changed) | `BLENDED.md` — the locked decision |
| Code progress (per-layer status, file lists) | `CHANGELOG.md` — *Unreleased* section |
| Claude AI contributor notes (what was built, per-session detail) | `CHANGELOG.md` — *Unreleased* section, same place as code progress |
| Operational grep pattern / session instructions | `CLAUDE.md` — this file |
| One-liner status for humans landing on GitHub | `.github/README.md` — "What's Different" section |

**Claude AI contributor notes go in CHANGELOG, not the README.** The README Contributors section is two sentences linking to CHANGELOG. All per-session implementation detail — what was built, what was removed, what scars were applied — belongs in the CHANGELOG *Unreleased* entry for that version, alongside the code progress rows. The README is a landing page.

**After every milestone or structural change, all four documents must be updated before the session ends.** The four are: `CLAUDE.md`, `CHANGELOG.md`, `BLENDED.md`, `.github/README.md`. Specific targets per document:
- **CLAUDE.md** — current version line updated, roadmap table row updated
- **CHANGELOG.md** — milestone note added; Claude AI contributor detail added to *Unreleased* section
- **BLENDED.md** — Status line updated; relevant sections updated
- **`.github/README.md`** — version/status sentence updated

**Note:** `.github/` is in `.gitignore` on this repo. Use `git add -f .github/README.md` when staging README updates — normal `git add` silently skips it.

**Meta-rule:** CLAUDE.md is the place for operational gotchas like this, not the chat. If you discover something worth knowing for the next session, write it here before the session ends.

---

## Pull Request Instructions

Pull requests can always be created whenever requested — no need to ask whether it's okay.

**Work, not judgment (BLENDED.md §4).** This repo is about work ethic and quality, not personal judgments. Review comments, replies and commit messages talk about the code and the record, never about the person who wrote it. That covers Codex, the developer, any outside contributor, and you. A finding is checked against the code and then fixed or answered. A mistake is corrected and written down, not defended. The baseline for what this project refuses is a maintainer elsewhere closing one of the developer's PRs with "are you proud of yourself".

**PR loop:** `.claude/skills/steward/SKILL.md` covers how a PR is driven from open to merged: the Codex review loop, the local checks that work without a build, docs in the same PR, merging and the build hand-off. Read it before acting on PR events. Like `.github/`, `.claude/` is gitignored: stage it with `git add -f`.

**How PRs work in this repo:**

- All development happens on feature branches of the `EvangAI-777/Blended` fork (not upstream Blender).
- Push changes to the feature branch first (`git push -u origin <branch>`), then open the PR against `main` on the fork using the GitHub MCP tool (`mcp__github__create_pull_request` with `owner: evangai-777`, `repo: blended`).
- The `head` is the feature branch; the `base` is `main`.
- Never target upstream `blender/blender` or any other repository.
- **If there is already an open PR on a feature branch, keep committing to that same branch.** All commits on an open branch are included in the PR automatically — the developer reviews and merges PRs themselves, so batching related work into one PR is preferred over opening multiple small ones. This also preserves continuity in the git log: one merge commit per logical unit of work rather than a fragmented trail of micro-PRs.

### The Orphaned-Commit Trap

**What happens:** A PR is opened, then additional commits are pushed to the same feature branch *after* the PR has already been merged. Those commits never land in `main` — they exist only on the old branch, which is now stale.

**Real example (PR #111, April 2026):** The workspace_edit.cc syntax fix was committed and pushed. PR #111 was opened and merged. Then the CLAUDE.md PR-instructions update was committed and pushed to the *same branch* — but the PR was already closed, so the commit went nowhere. It had to be cherry-picked onto a fresh branch and opened as PR #112.

**How to avoid it:** Before committing or pushing anything to an existing feature branch, fetch main and check whether the branch has already landed:
```bash
git fetch origin main
git log --oneline origin/main -3   # does your branch tip appear here already?
```
If the branch has already been merged, start a new branch from `origin/main` **before writing any commits**. Never push follow-on commits to a merged branch expecting them to reach `main`.

### PR Description Style

**Do not use `#` before CI build numbers in PR descriptions.** GitHub auto-links any `#N` as a reference to PR or issue N. `build #57` becomes a link to PR #57, not to the CI run. Write `build 57` — no hashtag.

---

## wtf.md

Moved to [`wtf.md`](wtf.md) at the repository root (2026-10-16), unchanged, so this file stays operational. It holds the notes previous Claude instances wrote about who the developer is and how to work with them (grass.md, help.md, scars.md, codex.md and others; new notes are appended at the end). Read it before your first session with the developer; it is not needed context for every task. The codex.md note records the Codex pre-audit method. The operational rule is in BLENDED.md §4 "Codex pre-audit": write plans at implementation resolution.
