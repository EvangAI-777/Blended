# AGENTS.md — Blended

Instructions for coding agents other than Claude Code, Codex code review in particular. Claude
Code reads `CLAUDE.md` instead; the two say the same things where they overlap.

## What this repository is

Blended is a fork of Blender 5.2 (GPL-2.0-or-later), published by CHJ 3 Productions LLC, being
rebuilt by **subtraction**: Blender features that don't belong are removed completely, and the
compile errors are followed to every dependent site. `BLENDED.md` is the design authority. It
records what was removed and why (§10, the datablock audit: 39 → ~19 ID types), and its decisions
are locked: don't propose restoring something it removed.

Built with Claude (Anthropic) as implementation partner and Codex (OpenAI) as reviewer of every pull request, across the whole project, not a version range (`BLENDED.md` §4, "Built with Claude and Codex").

Status: 1.0.0-dev, Phase 1 runtime audit. The developer runs each Windows CI build on hardware
and reports; fixes go in through pull requests. `docs/runtime-audit.md` lists known runtime
behavior (Categories A–D). Check it before reporting expected behavior as a bug.

## Map

| Path | What it is |
|------|------------|
| `BLENDED.md` | Design authority and locked decisions |
| `CLAUDE.md` | Operational rules for AI sessions (conventions, CI, PR loop) |
| `CHANGELOG.md` | Release record and per-session detail |
| `docs/runtime-audit.md` | Runtime audit protocol, known behavior, build findings |
| `docs/scars.md` | Past failures and the rules they produced |
| `docs/upstream-sync.md` | Merging upstream Blender; the divergence register |
| `.claude/rules/` | File-scoped rules (C++ ID types, docs, CI) |
| `tools/check_blended.py` | Fast source checks, run on every PR |

## Conventions

C/C++: 2-space indent, 99 columns, `snake_case`, `#pragma once`, SPDX headers, `blender::`
namespaces, `BKE_`/`BLI_`/`ED_`/`WM_`/`RNA_`/`DNA_` prefixes. Python: PEP 8, 120 columns.
Run `python3 tools/check_blended.py` before pushing.

## Review guidelines

Judge the change, not the author. This repo is about work ethic and quality, not personal
judgments (`BLENDED.md` §4, "Work, not judgment").

Check these first. Each comes from a bug that shipped in a build:

1. **Deregistered ID types** (`.claude/rules/id-types.md`). These codes have no `IDTypeInfo`:
   `ID_SCR_LEGACY`, `ID_WM_LEGACY`, `ID_WS_LEGACY`, `ID_PA`, `ID_GD_LEGACY`, `ID_LS`, `ID_MB`,
   `ID_TE`, `ID_CU_LEGACY`, `ID_CF`, `ID_LP`, `ID_PAL`, `ID_LT`, `ID_MSK`, `ID_VF`, `ID_BR`. Any
   generic ID API that goes through the type info fails or crashes for them: `BKE_libblock_alloc`,
   `BKE_id_new`, `BKE_id_new_nomain`, `BKE_id_new_name_validate` (namemap index -1),
   `BKE_id_copy`, `BKE_id_free` (except screens), `IDRemapper::add`. Flag any such call reachable
   with one of these types.
2. **`Main` listbases of removed types stay.** `bmain->screens`, `bmain->wm`, `bmain->curves` and
   the other non-indexed listbases are kept and routed by `which_libbase`. Removing one, or adding
   it to `BKE_main_lists_get`, is a regression.
3. **Removed Python types.** `bpy.types.MetaBall`, `Speaker`, `PaintCurve`, `CacheFile` and the
   removed `bpy.data` collections (for example `bpy.data.workspaces`, `bpy.data.curves`) don't
   exist. One error in `scripts/startup/bl_ui` stops the whole UI from loading.
4. **Keymaps.** An item a Blended editor adds in C must also be in
   `scripts/presets/keyconfig/keymap_data/blender_default.py`, or the default keyconfig wipes it.
5. **File format.** `.blended` is the native format; `.blend` is read-only import. A file-type
   change touches three paths: what writes the format, what reads it, and what classifies files by
   `FILE_TYPE_BLENDER` / `FILE_TYPE_BLENDED`. Check all three.
6. **Documentation consistency.** A change that alters behavior updates `CLAUDE.md`,
   `CHANGELOG.md`, `BLENDED.md` and `.github/README.md` in the same PR. Within a PR, ordered lists,
   version numbers, dates, build numbers and commit hashes must agree across files. Dates come from
   the CHANGELOG version headings; the project began in spring 2026.
7. **Workflows** (`.github/workflows/`). Actions pinned to full commit SHAs; no `${{ }}`
   expressions inside `run:` scripts (pass them through `env:`); least-privilege `permissions`.

Claude follows the update process in `docs/codex-standard.md` for every change; a PR that skips one of its steps (for example a doc the step 4 update matrix requires) is a finding.

A finding should name the input or call path that reaches the failure. Plans written into
`CLAUDE.md` or `docs/` at implementation detail are reviewed as if they were code.
