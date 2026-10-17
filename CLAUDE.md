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

### 0.8.0 — Complete

Magic bytes `"BLENDED"`, `.blended` extension on all write paths, `FILE_TYPE_BLENDED` bit flag (`1 << 20`), 23 implementation layers (~80 sites), platform integration (Windows registry, Linux MIME, macOS UTI), Python scripts, UI strings, tests. CI-complete build 100, commit `99e20b96`. Site-by-site tables and implementation notes in CHANGELOG.md `## 0.8.0` section and PR #225.

**Key architectural decisions carried forward:**
- Open/browse dialogs: `FILE_TYPE_BLENDER | FILE_TYPE_BLENDED`. Save dialogs: `FILE_TYPE_BLENDED` only.
- `filter_blender` and `filter_blended` are **separate** operator properties in `wm_operator_props.cc` — collapsing them into one causes `filesel.cc` to re-expand `.blended`-only save dialogs to include `.blend` (Codex catch, PR #225).
- Bundled upstream datafiles (e.g. `compositing_nodes_essentials.blend`) stay `.blend`.

---

### 0.9.0 — Complete

✓ CI-complete (build 101, commit `c8e87078`, 2026-06-01). Third first-try on the project. Five layers: OB_MBALL versioning pass 502.31, `BKE_main_clear` Scar 2 drain (PA/TE/CU/LS), `BKE_screen_blend_read_data` deletion, dropped-data manifest Text block. Layer 3 post-read LS drain removed by Codex catch (PR #229). See CHANGELOG.md `## 0.9.0` for full implementation notes and site-by-site detail.

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

### Branding

**Publisher:** Blended is developed and published by **CHJ 3 Productions LLC**, an Indiana-registered LLC. This is the legal entity behind the fork. All Blended-specific design decisions, the product identity, and fork-specific code additions are the work of CHJ 3 Productions LLC. Upstream Blender code retains its original copyright (Blender Foundation and contributors) under GPL-2.0-or-later — Blended inherits and preserves that license.

**Code locations:**
- `CMakeLists.txt:81` — `project(Blended)`
- `source/blender/blenkernel/BKE_blender_version.h` — `BLENDED_VERSION_MAJOR/MINOR/PATCH` defines (see Version Management section for bump procedure), plus `BKE_blended_version_string()` declaration
- `source/blender/blenkernel/intern/blender.cc` — `blended_version_string` built in `blender_version_init()`, `BKE_blended_version_string()` implemented
- `source/blender/windowmanager/intern/wm_window.cc` — fallback title `"Blended"`, title suffix `"- Blended X.Y.Z"` via `BKE_blended_version_string()` (rendered dynamically from the defines above)
- `source/blender/windowmanager/intern/wm_splash_screen.cc` — about dialog name/description, tagline `"Blender, simplified."`, splash version label

### Pre-5.0 Rig Compatibility
- `scripts/startup/blended_rig_compat.py` — adds `action.fcurves` as a Python property on `bpy.types.Action`
- Returns `_FCurvesCompat` proxy flattening FCurves from all channelbags across all layers/strips
- Restores iteration, `len()`, indexed access, `find()` — the subset Rigify `ActionCurveTable` uses
- `register()` uses `bpy.types.Action.fcurves = property(...)` only if not already present
- `unregister()` uses `type.__delattr__(bpy.types.Action, 'fcurves')` — Blender's metaclass `__delattr__` only handles RNA props, not plain Python descriptors

### Update Checker
- `scripts/startup/blended_update_check.py` — background thread on `load_post` handler
- Polls GitHub Releases API, 24-hour JSON cache in `bpy.utils.user_resource('CONFIG')`
- `BLENDED_MT_update_topbar` menu appended to `TOPBAR_HT_upper_bar` when update available
- `BLENDED_PT_update_prefs` panel in System Preferences
- `BLENDED_OT_open_update_page` operator opens browser via `webbrowser.open()`
- Reads `bpy.app.blended_version_major/minor/patch` (wired into `source/blender/python/intern/bpy_app.cc` — `app_info_fields[]` + `make_app_info()`).

### CI / Build Config
- `.github/workflows/build-windows.yml` — triggers only on `v*` tag pushes and manual `workflow_dispatch` (PRs and pushes to `main` get only the Checks workflow below; other branch pushes run nothing). Full release build → artifact → build-provenance attestation → headless smoke test of the packaged build (`tests/python/blended_smoke_test.py`: startup, Python startup scripts, window-manager RNA, File > Open of a legacy `.blend`, Save As `.blended` and reopen). On tags, a separate `release` job (the only one with write access) publishes the zip and its `.sha256`. Read-only token by default; one build per ref at a time (a second dispatch queues).
- `.github/workflows/checks.yml` — on every PR to `main`, pushes to `main` and dispatch, a few minutes on Linux: `tools/check_blended.py` (Python syntax of `scripts/`, the Cycles add-on and `tests/python`; `BKE_libblock_alloc`/`BKE_id_new` with a deregistered ID type; `bpy.types` references to removed RNA types; `LISTBASE_FOREACH` outside `listbase.cc`) and a YAML parse of `.github/`. Run `python3 tools/check_blended.py` locally before pushing. When a new class of runtime bug can be caught from source, add a check there.
- Every action in `.github/workflows/` is pinned to a full commit SHA with the version in a trailing comment. `.github/dependabot.yml` opens monthly update PRs. Never put `${{ }}` expressions straight into a `run:` block; pass them through `env:` (script injection).
- `build_files/cmake/config/blended_release.cmake` — inherits `blender_release.cmake`, disables `WITH_CYCLES_CUDA/HIP/ONEAPI_BINARIES` and `WITH_FREESTYLE`

### Version Management

**The single source of truth:** `source/blender/blenkernel/BKE_blender_version.h` — three defines:
```c
#define BLENDED_VERSION_MAJOR 1
#define BLENDED_VERSION_MINOR N   // ← bump for new features (post-1.0.0 semantic versioning)
#define BLENDED_VERSION_PATCH 0   // ← bump for bug fixes and CI repairs within a layer
```
The CI workflow reads these at build time. Packaged artifact name (`Blended-X.Y.Z-windows-x64`) derives entirely from these defines — no other file needs to be changed for the package label to update.

**When to bump MINOR (new dev-cycle start):**
Bump `BLENDED_VERSION_MINOR` on the **first commit of a new dev cycle**, not when CI goes green. Example: the first commit of 0.5.x work bumps minor to 5 even though 0.5.0 won't be CI-complete for weeks. This way the version string in a dev build always names the cycle in progress. *Do not wait for CI to go green before bumping.*

**When to bump PATCH:**
Bump `BLENDED_VERSION_PATCH` for CI fixes, doc updates, and build repairs within an existing layer that don't add new foundation work. A patch release is a stable point within a cycle — e.g., the ID_LP CI-fix PRs within 0.5.x would be 0.5.1 if they warranted a tagged release.

**Post-1.0.0 — standard semantic versioning from here:**
Once the 1.0.0 release tag ships, the foundation-layer versioning scheme retires. From 1.0.0 onward: `BLENDED_VERSION_PATCH` bumps for bug fixes, CI repairs, and doc updates (1.0.1, 1.0.2, …); `BLENDED_VERSION_MINOR` bumps for new features, pipeline sections, and modes (1.1.0, 1.2.0, …); `BLENDED_VERSION_MAJOR` bumps for breaking changes or major architectural shifts (2.0.0, …). The four-mandatory-docs update procedure and the quick checklist still apply to every version bump — only the bump rules change.

**Version lag — what happened with 0.3.0 → 0.4.0:**
The 0.4.0 CI-complete milestone (build 70) shipped without bumping the version header from 0.3.0. The product ran as "0.3.0" for the entire 0.5.x dev cycle until manually caught. The fix: treat the version bump as a required checklist item when a layer goes CI-green, not as something to do later.

**Full procedure — bump + update all four mandatory docs:**

1. **`BKE_blender_version.h`** — increment `BLENDED_VERSION_MINOR` (or `PATCH`).

2. **`CLAUDE.md`** (this file) — update the "Current version" line at the top:
   - For a new dev-cycle start: `Blended X.Y.0-dev — [layer description] in progress`
   - For a CI-complete milestone: `Blended X.Y.0-dev — X.(Y-1).0 base: CI-complete (Windows x64, build N, commit XXXXXXX)`

3. **`CHANGELOG.md`** — add a version bump note to the active *Unreleased* section (or the completed version section):
   - One line: which define changed, old value → new value, what triggered it, commit reference.
   - If CI just went green: also add a CI-complete note with build number and commit hash.

4. **`BLENDED.md`** — update the **Status** line at the top of the file to match.

5. **`.github/README.md`** — update the version/status sentence under the repo description. Stage with `git add -f .github/README.md` (it is in `.gitignore`).

**Quick checklist (run after any CI-green milestone or new dev-cycle start):**
```
□ BKE_blender_version.h — MINOR or PATCH bumped
□ CLAUDE.md — "Current version" line updated; roadmap table row updated
□ CHANGELOG.md — version bump note + CI-complete note added; grep all sections for stale version refs
□ BLENDED.md — Status line updated; grep all sections for stale version refs
□ .github/README.md — version/status sentence updated (git add -f)
□ All five changes in one commit, pushed to the working branch
```
**Note:** The four mandatory docs each contain multiple sections that reference version state — roadmap tables, mid-document planning blocks, subsection headers. A headline-only pass misses them. `grep -n "0\\.X" <file>` (replace X with the version) before staging each doc.

### Datablock Audit — Complete (BLENDED.md §10)
Result: 39 → ~19 ID types. All buckets closed.
- **Bucket 4 (UI state, remove):** `ID_WS` ✓ (0.2.0), `ID_SCR` ✓ (0.3.0), `ID_WM` ✓ (0.3.0)
- **Bucket 5 (upstream deprecations, finish):** `ID_CU_LEGACY` ✓ (0.4.0), `ID_GD_LEGACY` ✓ (0.4.0)
- **Bucket 6 (fossils, cut):** `ID_CF` ✓ (0.4.0); `ID_PC` ✓ (0.4.0); `ID_SPK` ✓ (0.4.0); `ID_PA` ✓ (0.4.0); `ID_LS` ✓ (0.4.0); `ID_MB` ✓ (0.4.0); `ID_TE` ✓ (0.4.0)
- **Bucket 3 (runtime types, fold-down then permanent home):** `ID_LP` ✓ (0.5.0 fold-down → 0.7.0 Light type flag), `ID_PAL` ✓ (0.5.0 → 0.7.0 Brush embed), `ID_LT` ✓ (0.5.0 → 0.7.0 LatticeModifierData), `ID_MSK` ✓ (0.5.0 → 0.7.0 compositor NodeTree), `ID_VF` ✓ (0.5.0 → 0.7.0 OB_FONT filepath), `ID_BR` ✓ (0.5.0 → 0.7.0 project-optional flag)

---

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
