# CLAUDE.md — Blended Project Context

<!-- Maintainer note (stripped before Claude reads this file): keep CLAUDE.md under ~200 lines.
     Always-true rules only. File-specific rules go in .claude/rules/ (paths:), procedures in
     .claude/skills/, reference and history in docs/. Restructured in PR #253. -->

Blended is a fork of Blender 5.2 (GPL-2.0-or-later) being rebuilt from the foundation up, by subtraction.

**Built with Claude and Codex, throughout** (BLENDED.md §4): Claude (Anthropic) implements, Codex (OpenAI) reviews every PR, for every version and phase. Don't describe either role as limited to a version range.

**Read `BLENDED.md` first.** It is the design authority: identity, architecture, the datablock audit, locked decisions, open questions and guardrails. This file is the operational context for Claude sessions.

**Current version:** Blended 1.0.0-dev — 0.9.0 base: CI-complete (Windows x64, build 101, commit `c8e87078`). Third first-try on the project. 0.9.0 delivered: `.blend` import ✓ — OB_MBALL versioning pass 502.31, `BKE_main_clear` Scar 2 drain (PA/TE/CU/LS), `BKE_screen_blend_read_data` deletion, dropped-data manifest Text block. Layer 3 post-read LS drain removed — Codex catch PR #229. 1.0.x: foundation complete — two sequential phases: Phase 1 runtime audit (developer runs build, checklists, triage loop with Claude) in progress — build 103/104/106 crashes diagnosed and fixed, build 107 empty crash log fixed (PR #242) and verified on hardware in build 108 — first real backtrace of the startup crash; root cause identified (`wm_add_default` workspace/screen bootstrap), launcher-bootstrap fix (PR #244) verified on hardware in build 109 — Blended reaches its own UI (the launcher) for the first time; build 109 findings (bl_ui syntax error → navigate-gizmo crash, window manager refining to plain `ID` in RNA) fixed and verified on hardware in build 110; build 110 findings (File > Open crash when the file browser closes, upstream splash over the launcher, Cycles `MetaBall` registration error, empty launcher keymap, spurious "loading empty scene" warning) fixed and verified on hardware in build 111 — the first session with no crash; build 111 findings (a scene behind the launcher, a too-faint project-state cue, upstream branding in the render window and status bar) fixed; build 112 CI-green with the smoke test passing, awaiting hardware verification (its test list is on PRs #250–#254; the open multi-window check is two windows in one running Blended, not a second instance, PR #256). Category D table updated. CI now smoke-tests each packaged build headless (`tests/python/blended_smoke_test.py`), and every PR runs fast source checks (`tools/check_blended.py`; PR #252, which also hardened the workflows and fixed a latent render-curve crash the check found). Docs restructured for Claude Code and Codex (PR #253): CLAUDE.md core, `.claude/rules/`, skills, `docs/`, `AGENTS.md`. Phase 2 GitHub Pages launch pending Phase 1 completion. Release tag when both phases clear.

---

## Where things live

| Path | Read it when |
|------|--------------|
| `BLENDED.md` | Always first. Design authority; its appendix holds the Development Philosophy |
| `docs/runtime-audit.md` | Before calling anything a new bug: the audit protocol, open runtime checks, Categories A–D, build findings |
| `docs/scars.md` | Before your first session, and when a rule below points to a scar: the full story behind each rule |
| `docs/fork-reference.md` | Branding locations, rig compatibility, update checker, completed layers, datablock audit |
| `CHANGELOG.md` | Release record, per-session detail, Claude AI contributor notes |
| `docs/wtf.md` | Who the developer is and how to work with them (see the end of this file) |
| `docs/upstream-sync.md` | Merging upstream Blender: the process, conflict-prone files, the divergence register |
| `AGENTS.md` | What Codex reads (review guidelines). Keep it consistent with this file |
| `.claude/rules/` | Load automatically for matching files: `id-types.md` (C/C++), `docs.md` (the docs), `workflows.md` (CI) |
| `.claude/skills/` | `runtime-audit` (build hand-off and triage), `steward` (PR loop), `version-bump` |

---

## Status and roadmap

Phase 1 of 1.0.0, the runtime audit, is in progress: the developer runs each Windows build on hardware and reports; Claude triages, fixes and documents; the next build verifies. Use the `runtime-audit` skill when a build finishes or a report comes in. Phase 2 (GitHub Pages) starts after the audit checklist clears; the release tag needs both.

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
| 1.1.0+ | Post-1.0 roadmap (minor versions). Entries: user workspaces (decide where they live, BLENDED.md §9 item 10; give them an owner; re-enable Duplicate/Delete/Reorder/Cycle), Blended keymap and theme presets, open into the right mode for every mode, revive the upstream Python test suite, upstream 5.2 LTS fixes (small verified cherry-pick batches, fork point in `docs/upstream-sync.md`), the settings folder name (publisher folder or not). Plans in CHANGELOG.md "Post-1.0 roadmap". | Planned |

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

**Upstream sync conflict-prone files:** `BKE_blender_version.h` (we added `BLENDED_VERSION_*`), `CMakeLists.txt` (project name), `wm_window.cc`, `wm_splash_screen.cc`, and all branding/release files. Check `docs/upstream-sync.md` before merging upstream Blender releases.

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

## Fork-Specific Patterns

### Branding, rig compatibility, update checker

Publisher: **CHJ 3 Productions LLC** (Indiana); upstream code keeps its Blender Foundation copyright under GPL-2.0-or-later. Code locations for the branding, `scripts/startup/blended_rig_compat.py` (pre-5.0 `action.fcurves`) and `scripts/startup/blended_update_check.py`: [`docs/fork-reference.md`](docs/fork-reference.md).

### CI / Build Config
- `.github/workflows/build-windows.yml` — triggers only on `v*` tag pushes and manual `workflow_dispatch` (PRs and pushes to `main` get only the Checks workflow below; other branch pushes run nothing). Full release build → artifact → build-provenance attestation → headless smoke test of the packaged build (`tests/python/blended_smoke_test.py`: startup, Python startup scripts, window-manager RNA, File > Open of a legacy `.blend`, Save As `.blended` and reopen, the launcher keymap, Cycles, File > New, the first-run copy, and a second start that reloads saved preferences; a Python `Traceback` or `SyntaxError` in either log fails it). If a check doesn't need a window, it belongs here, not on the developer's hardware list. On tags, a separate `release` job (the only one with write access) publishes the zip and its `.sha256`. Read-only token by default; one build per ref at a time (a second dispatch queues).
- `.github/workflows/checks.yml` — on every PR to `main`, pushes to `main` and dispatch, a few minutes on Linux: `tools/check_blended.py` (Python syntax of `scripts/`, the Cycles add-on and `tests/python`; `BKE_libblock_alloc`/`BKE_id_new` with a deregistered ID type; `bpy.types` references to removed RNA types; `LISTBASE_FOREACH` outside `listbase.cc`) and a YAML parse of `.github/`. Run `python3 tools/check_blended.py` locally before pushing. When a new class of runtime bug can be caught from source, add a check there.
- Every action in `.github/workflows/` is pinned to a full commit SHA with the version in a trailing comment. `.github/dependabot.yml` opens monthly update PRs. Never put `${{ }}` expressions straight into a `run:` block; pass them through `env:` (script injection).
- `build_files/cmake/config/blended_release.cmake` — inherits `blender_release.cmake`, disables `WITH_CYCLES_CUDA/HIP/ONEAPI_BINARIES` and `WITH_FREESTYLE`

### Version Management

`source/blender/blenkernel/BKE_blender_version.h` (`BLENDED_VERSION_MAJOR/MINOR/PATCH`) is the single source of truth; the CI artifact name comes from it. Bump MINOR on the first commit of a new dev cycle, PATCH for fixes within one; from 1.0.0 on, standard semantic versioning. Every bump updates the four mandatory docs in the same commit. The full procedure and checklist: the `version-bump` skill.

### Datablock Audit — Complete (BLENDED.md §10)

39 → ~19 ID types; all buckets closed. Per-type detail: [`docs/fork-reference.md`](docs/fork-reference.md) and BLENDED.md §10.

---

## Rules that hold in every session

Each comes from a real failure. The full story is in `docs/scars.md`; read it when the rule alone doesn't settle a case.

- **Commit and push after every logical unit** (Scar 3). Never hold unpushed commits: a dead session loses them. One layer, one commit, one push.
- **Don't over-delete** (Scar 1). A file with ID-system glue and runtime logic loses only the glue.
- **Deregistered ID types never go through generic ID APIs** (Scars 2, 10, 25). The list, the allocation template and the kept-listbase rule are in `.claude/rules/id-types.md`; `tools/check_blended.py` enforces the allocation part.
- **Read a whole file before editing it** if it's longer than ~200 lines (Scar 21). Revert a botched edit instead of fixing forward.
- **Instructions about how are as binding as instructions about what** (Scar 5). "Section by section" means one Edit call per section.
- **Write from evidence** (Scar 6). Screenshots, logs and crash logs are the ground truth; don't soften a failure.
- **Read the full diff before committing docs** (Scar 7); every list, version and date must agree across files (`.claude/rules/docs.md`).
- **Don't produce a menu about something plainly wrong; fix it** (Scar 14). Verify that something exists by grepping the specific commit, PR or build number, not the topic.
- **After a rename, grep the whole repo with no filters** (Scar 20): `grep -rn "old_name" . --exclude-dir=.git`.
- **A format change has three axes** (Scar 22): what writes it, what reads it, what classifies files by type flag. When a grep returns several hits in a file, read every one.
- **Take precise git terms literally** (Scar 23): "fast forward" is `git merge --ff-only`, never a rebase.
- **Fix a wrong thing; don't label it** (Scar 24).
- **Run a new checklist rule against the whole codebase in the same session** (Scar 25).
- **Identity work covers artifact names** (Scar 26): check `OUTPUT_NAME` per platform, not just UI strings.
- **Collaboration, not control** (BLENDED.md §4): aim caution at the code, not the developer. Say a thing once, only when it's new to them; checks go into the docs or the smoke test, not onto the developer.
- **Verify includes for every new or rewritten `.cc`**: grep the `#include` list for each API you call (`MEM_guardedalloc.h` for `MEM_new`).

### Before every commit (the Codex Standard)

Ask: would Codex catch this? Catch it first. Run `python3 tools/check_blended.py`; for docs, the Part 1 checklist in `.claude/rules/docs.md`; then answer the rules above as yes/no questions. The full checklist is in `docs/scars.md`.

### Session discipline

- **Three or more steps means a todo list**, one item per step, marked done the moment it's done. The Codex Standard check is an item before every commit.
- Be specific (file, function, line); prefer direct grep and reads over agents for known targets; commit before starting anything risky. Details and emergency mode: `docs/scars.md`, "Working with Claude Code Efficiently".

### Philosophy in five lines

Subtraction is the method: delete, follow the compile errors, and treat the breakage as the audit. Do the work instead of designing around it. Cut the whole thing; a stub that compiles but lies is worse than an error. When the developer says you're wrong or describes what they see, believe them and re-examine from scratch. Functionality over ego. The full text: `BLENDED.md`, "Appendix — Development Philosophy".

---

## Documentation

**After every milestone or structural change, update all four mandatory docs before the session ends:** `CLAUDE.md` (current-version line, roadmap row), `CHANGELOG.md` (milestone note, Claude AI contributor note), `BLENDED.md` (status line, affected sections), `.github/README.md` (status sentence). Where each kind of content goes, and how to edit the docs, is in `.claude/rules/docs.md`. If you learn something the next session needs, write it into the right doc before the session ends, not just into the chat.

---

## Pull Request Instructions

Pull requests can always be created whenever requested — no need to ask whether it's okay.

**Work, not judgment (BLENDED.md §4).** This repo is about work ethic and quality, not personal judgments. Review comments, replies and commit messages talk about the code and the record, never about the person who wrote it. That covers Codex, the developer, any outside contributor, and you. A finding is checked against the code and then fixed or answered. A mistake is corrected and written down, not defended.

**PR loop:** the `steward` skill (`.claude/skills/steward/SKILL.md`) covers driving a PR from open to merged: the Codex review loop, the local checks, docs in the same PR, merging and the build hand-off.

**How PRs work in this repo:**

- All development happens on feature branches of the `EvangAI-777/Blended` fork (not upstream Blender).
- Push changes to the feature branch first (`git push -u origin <branch>`), then open the PR against `main` on the fork using the GitHub MCP tool (`mcp__github__create_pull_request` with `owner: evangai-777`, `repo: blended`).
- The `head` is the feature branch; the `base` is `main`.
- Never target upstream `blender/blender` or any other repository.
- **If there is already an open PR on a feature branch, keep committing to that same branch.** All commits on an open branch are included in the PR automatically — the developer reviews and merges PRs themselves, so batching related work into one PR is preferred over opening multiple small ones. This also preserves continuity in the git log: one merge commit per logical unit of work rather than a fragmented trail of micro-PRs.
- **The orphaned-commit trap:** before committing to an existing branch, `git fetch origin main` and check whether the branch already merged. If it did, restart it from `origin/main` before writing any commits. (Story: `docs/scars.md`.)
- **Write `build 57`, never `build #57`**: GitHub links `#N` to PR N.
- **The PR's Test Plan covers every kind of testing:** automated, build testing (written before merge; the build's full chat list goes verbatim on each merged PR it carries), developer testing, user testing where it applies (`.github/pull_request_template.md`).

---

## wtf.md

[`docs/wtf.md`](docs/wtf.md): moved out of this file on 2026-10-16 and into `docs/` in PR #253, unchanged except for an index at the top. It holds the notes previous Claude instances wrote about who the developer is and how to work with them (grass.md, help.md, scars.md, codex.md and others; new notes are appended at the end and added to the index). Read it before your first session with the developer; it is not needed context for every task. The codex.md note records the Codex pre-audit method. The operational rule is in BLENDED.md §4 "Codex pre-audit": write plans at implementation resolution.
