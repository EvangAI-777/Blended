# CLAUDE.md — Blended Project Context

Blended is a fork of Blender 5.2 (GPL-2.0-or-later) being rebuilt from the foundation up.

**Read `BLENDED.md` first.** It is the design authority — identity, architecture, datablock audit, pipeline specs, locked decisions, open questions, and guardrails. This file is operational context for Claude sessions: what's been built, what the patterns are, what not to repeat.

**Current version:** Blended 1.0.0-dev — 0.9.0 base: CI-complete (Windows x64, build 101, commit `c8e87078`). Third first-try on the project. 0.9.0 delivered: `.blend` import ✓ — OB_MBALL versioning pass 502.31, `BKE_main_clear` Scar 2 drain (PA/TE/CU/LS), `BKE_screen_blend_read_data` deletion, dropped-data manifest Text block. Layer 3 post-read LS drain removed — Codex catch PR #229. 1.0.x: foundation complete — two sequential phases: Phase 1 runtime audit (developer runs build, checklists, triage loop with Claude) in progress — build 103/104/106 crashes diagnosed and fixed, build 107 empty crash log fixed (PR #242) and verified on hardware in build 108 — first real backtrace of the startup crash; root cause identified (`wm_add_default` workspace/screen bootstrap), launcher-bootstrap fix (PR #244) verified on hardware in build 109 — Blended reaches its own UI (the launcher) for the first time; build 109 findings (bl_ui syntax error → navigate-gizmo crash, window manager refining to plain `ID` in RNA) fixed, awaiting build verification. Category D table updated. CI now smoke-tests each packaged build headless (`tests/python/blended_smoke_test.py`). Phase 2 GitHub Pages launch pending Phase 1 completion. Release tag when both phases clear.

---

## Deferred Debt & Roadmap Snapshot

Quick reference for incoming sessions. Full detail in CHANGELOG.md and BLENDED.md.

### Known Deferred Debt

All pre-1.0.0 deferred debt resolved in 0.9.x. See CHANGELOG.md `## 0.9.0` for full detail.

---

### Known Runtime Artifacts (QA Reference)

**Check here before assuming a new bug.** These are the expected consequences of completed chisels. The build is CI-green; these are bounded, documented runtime gaps — not regressions. **Category D** lists crashes caught and fixed during the 1.0.0-dev runtime audit — real crashes that shipped in a released build and were resolved.

#### Category A — Expected behavior changes (by design, won't fix)

| Trigger | What happens | Introduced |
|---------|-------------|------------|
| Object with `PFIELD_TEXTURE` force field in legacy file | Texture displacement silently dead. `build_texture()` is a no-op — Tex IDNodes never enter the depsgraph. Force field evaluates but ignores the texture parameter entirely. *(Post-chisel fix `c320633b`: two direct `add_relation()` calls in `deg_builder_relations.cc` that bypassed the no-op were removed — without the fix these logged repeated "Failed to add relation" errors at graph-build time.)* | 0.4.0 (ID_TE) |
| Object with particle system that has texture slots (legacy file) | Texture slots silently ignored. Particle system otherwise evaluates (geometry nodes path). | 0.4.0 (ID_TE) |
| Node with `SOCK_TEXTURE` socket and a `Tex *` default value (legacy file) | Socket's texture not depsgraph-tracked; texture changes don't trigger node re-evaluation. | 0.4.0 (ID_TE) |
| Brush with `paint_curve` assigned in legacy file | `Brush::paint_curve` field no longer exists in DNA; SDNA remapping skips it on load. Brush uses default stroke shape. No crash. | 0.4.0 (ID_PC) |
| Python script calling `bpy.ops.object.particle_system_add()` or `_remove()` | "Operator not found" error. Operators removed in 0.4.0 cleanup (commit `e39bcd58`). | 0.4.0 (ID_PA) |
| Scene with NLA sound strip created via old `NLA_OT_soundclip_add` operator | Operator removed. Existing sound strips in NLA from legacy files: no speaker evaluation, no 3D positional audio. VSE timeline audio unaffected. | 0.4.0 (ID_SPK) |
| File with GD_LEGACY grease pencil objects or annotations | OB_GPENCIL_LEGACY objects and annotation data fully functional — depsgraph evaluation kept intentionally. This is **not** a failure; listed here for completeness. | 0.4.0 (ID_GD_LEGACY) |
| Python `context.temp_override(screen=...)` | Raises "Screen has no workspace" for every screen. `bpy_rna_context.cc:263` checks the null return of the `BKE_workspace_layout_find_global` stub (no workspace list exists since ID_WS removal) and raises before `:50` could use it. No crash. Stays until workspaces have an owner (post-1.0 roadmap: user workspaces). | 0.2.0 (ID_WS) |
| Workspace menu (`TOPBAR_MT_workspace_menu`) | Shows "No workspace actions available". Delete, reorder and cycle need a workspace list, which `bpy.data.workspaces` was until ID_WS removal; their entries were deleted in PR #245 (the menu's `draw` raised `AttributeError` on `len(bpy.data.workspaces)`). Duplicate is gone too, and `WORKSPACE_OT_duplicate` is disabled everywhere (also "Duplicate Current" in the Add Workspace menu): `BKE_id_copy` can't copy a workspace without `IDTypeInfo` and returns null (Codex catch, PR #245). Scar 1 debt; restored by the post-1.0 user-workspaces plan. | 0.2.0 (ID_WS) |

#### Category B — Uncertain/crash paths — all resolved in 0.9.x

| Trigger | Expected failure mode | Introduced | Status |
|---------|-----------------------|------------|--------|
| Legacy file containing MetaBall (`OB_MBALL`) objects | `bmain->metaballs` fully removed — no Scar 2 rescue. MetaBall data can't be allocated; no `which_libbase` routing. Objects will load with `ob->type == OB_MBALL` and `ob->data == nullptr`. Any draw or eval code that dereferences `ob->data` without a null check → null deref crash. `BLI_assert_unreachable()` sites in dispatch switches → debug assert. | 0.4.0 (ID_MB) | ✓ **Fixed in 0.9.x Layer 1** — versioning pass 502.31 in `versioning_520.cc` converts `OB_MBALL → OB_EMPTY`, same pattern as OB_SPEAKER → OB_EMPTY (502.23). |
| Legacy file with particle systems on objects | `ParticleSettings` IDs load into `bmain->particles` (Scar 2). `build_particle_systems()` is still called for any object with `object->particlesystem.first != nullptr`. `build_particle_settings(particle->part)` runs and calls `add_id_node()`. The OOB-index crash (`BKE_idtype_idcode_to_index(ID_PA)` → -1) is **guarded**: `depsgraph.cc` has `if (id_type_index >= 0)` before writing `id_type_exist[]`, applied during the ID_CU_LEGACY chisel. Particle systems in legacy files load and evaluate without crashing. Memory leak: `bmain->particles` not in `BKE_main_lists_get` (Category C). | 0.4.0 (ID_PA) | ✓ OOB guard in place. Remaining: Category C memory leak only. |

#### Category C — Memory leaks — Scar 2 leaks resolved in 0.9.x (Layer 2: `BKE_main_clear` Scar 2 drain); one bounded leak accepted

| Trigger | Leak scope | Introduced | Fix when needed |
|---------|-----------|------------|-----------------|
| Load legacy `.blend` with Freestyle LineStyle data (`WITH_FREESTYLE=OFF`) | `bmain->linestyles` populated, not freed by `BKE_main_free`. Blocks accumulate per file load, freed on process exit. | 0.4.0 (ID_LS) | ✓ **Fixed in 0.9.x Layer 2** (`BKE_main_clear` only — `FreestyleLineSet::linestyle` pointers in ViewLayer are live consumers: `scene.cc:919-921` traverses them in foreach_id, `freestyle.cc:55-57` dereferences them in view-layer cleanup. Post-read drain is unsafe. Codex catch, PR #229.) |
| Load legacy `.blend` with ParticleSettings data | `bmain->particles` populated (Scar 2), not in `BKE_main_lists_get`. `ParticleSystem::part` is a live `ParticleSettings *` on objects with particle systems — post-read drain would be use-after-free. | 0.4.0 (ID_PA) | ✓ **Fixed in 0.9.x Layer 2** (`BKE_main_clear` only — live `psys->part` pointers; same constraint as ID_CU_LEGACY) |
| Load legacy `.blend` with Blender Internal texture data | `bmain->textures` populated (Scar 2), not in `BKE_main_lists_get`. Modifier DNA structs (`DisplaceModifierData`, `WarpModifierData`, etc.) carry live `Tex *` fields — post-read drain would be use-after-free. | 0.4.0 (ID_TE) | ✓ **Fixed in 0.9.x Layer 2** (`BKE_main_clear` only — live modifier `Tex *` pointers; same constraint as ID_CU_LEGACY) |
| Load legacy `.blend` with Curve data, OR import NURBS via Alembic/OBJ | `bmain->curves` populated (Scar 2), not in `BKE_main_lists_get`. `BKE_curve_add` is called at runtime by Alembic NURBS reader, OBJ NURBS importer, and all text/curve object creation (`OB_FONT`, `OB_CURVES_LEGACY`, `OB_SURF`). | 0.4.0 (ID_CU_LEGACY) | ✓ **Fixed in 0.9.x Layer 2** (`BKE_main_clear` only — post-read drain unsafe; live objects reference `bmain->curves`) |
| Any startup | The runtime "Launcher" workspace created by `wm_add_default` (PR #244) is never freed — nothing owns workspaces since ID_WS removal. One workspace per process (`wm_add_default` runs only when no window manager exists, and the window manager is always kept on File > Open), reclaimed at process exit. Bounded, no accumulation. | 0.2.0 (ID_WS) / 1.0.0-dev (PR #244) | **Accepted** — free it when workspaces get an owner (Scar 1 debt; post-1.0 user-workspaces plan) |

**Scar 2 drain architecture (for future reference):** All four non-indexed Scar 2 listbases (`bmain->linestyles`, `bmain->particles`, `bmain->textures`, `bmain->curves`) drain only in `BKE_main_clear` (`main.cc`), after the indexed ID loop completes. None are safe to drain post-read: `FreestyleLineSet::linestyle` in `ViewLayer` is traversed by scene `foreach_id` (`scene.cc:919-921`) and dereferenced by view-layer cleanup (`freestyle.cc:55-57`); `ParticleSystem::part` holds live `ParticleSettings *`; modifier DNA structs hold live `Tex *`; `OB_FONT`/`OB_CURVES_LEGACY`/`OB_SURF` hold `ob->data` into `bmain->curves`. The Main-clear drain runs after all Scenes and Objects are freed and is safe for all four. Do NOT use `BKE_id_multi_tagged_delete` — that API operates on the main indexed list and will not reach Scar 2 listbases.

#### Category D — Fixed crashes (caught at runtime audit)

| Trigger | Failure | Introduced | Fixed |
|---------|---------|------------|-------|
| Any startup — fresh install or default file | `BKE_palette_add` crashed immediately via `BKE_gpencil_palette_ensure` → `BLO_update_defaults_startup_blend`. Root cause: the Scar 10 allocator called `BKE_id_new_name_validate`, which routes into `BKE_main_namemap_get_unique_name` → `namemap_get_name`. The namemap is indexed by `BKE_idtype_idcode_to_index(ID_PAL)`, which returns -1 for the deregistered Scar 2 type. Accessing `maps[-1]` (an 8-byte pointer array) yields address `0xFFFFFFFFFFFFFFF8` — reading garbage as a `Map<string>` object, crashing in the string slot destructor. Build 97 (the first 0.7.0 release artifact) crashed on launch for all users. Initial fix (PR #214): bypass `BKE_id_new_name_validate`; instead assign the name via `BLI_strncpy_utf8` then call `BLI_uniquename` on the Scar 2 listbase. Later corrected in PR #235 (see build 103 row): `BLI_uniquename` has two gaps — it doesn't sort the listbase and doesn't scope uniqueness to the same library. **General rule for all Scar 10 allocators:** never call `BKE_id_new_name_validate` for a deregistered type; use `BLI_strncpy_utf8` + `BLI_uniquename_cb` (lib-scoped lambda) + `id_sort_by_name` on the Scar 2 listbase instead. See Scar 10 for the correct template. | 0.5.0 (ID_PAL Scar 10 allocator) | PR #214 commit `25f59735`, corrected PR #235 (`paint.cc`) |
| Any startup — all 1.0.0-dev builds (build 103) | `BKE_brush_add` and 8 other deregistered-type allocators called `BKE_id_new_name_validate` after the Scar 10 `BKE_libblock_alloc` fix. Same namemap crash chain: index = -1, `maps[-1]` = `0xFFFFFFFFFFFFFFF8` → AV. Root cause: the Scar 10 code template in CLAUDE.md showed `BKE_id_new_name_validate` in the fix pattern — which is itself a crash for deregistered types. Every allocator patched per Scar 10 inherited the second-generation bug from the wrong template. Affected: `BKE_brush_add` (ID_BR), `BKE_curve_add` (ID_CU_LEGACY), `BKE_lattice_add` (ID_LT), `BKE_lightprobe_add` (ID_LP), VFont loader (ID_VF), `BKE_particlesettings_add` (ID_PA), `BKE_linestyle_new` (ID_LS), `BKE_gpencil_data_addnew` (ID_GD_LEGACY), `mask_alloc` (ID_MSK), plus `BKE_palette_add` (ID_PAL) and `screen_add` (ID_SCR_LEGACY) from earlier sessions — 11 allocators total. Fix: replace `BKE_id_new_name_validate` with `BLI_strncpy_utf8` + `BLI_uniquename_cb` (lib-scoped lambda filtering `id_iter->lib == obj->id.lib`) + `id_sort_by_name`. Two Codex catches on PR #235: (1) missing `id_sort_by_name` — `BLI_uniquename` doesn't keep listbase sorted; (2) missing library scope — `BLI_uniquename` checks all IDs regardless of `id.lib`, causing false `.001` suffix when a linked library has the same name. Scar 10 template updated with correct pattern. | Various (ID_BR: 0.7.0; others 0.4.0–0.5.0) | PR #235, commits `bd00e157` / `5cad0bac` / `f52b74bf` (11 files) |
| Any startup — all 0.9.0 builds | `wm_add_default` crashed at startup via `BKE_libblock_alloc(bmain, ID_WM_LEGACY, "WinMan", 0)`. `ID_WM_LEGACY` has no `IDTypeInfo` — `BKE_libblock_get_alloc_info` returns size 0, `BKE_libblock_alloc_notest` returns nullptr, `BKE_libblock_alloc_in_lib` calls `BKE_libblock_runtime_ensure(*id)` which dereferences nullptr at offset `0x190` (the `runtime` field in `ID`) → `EXCEPTION_ACCESS_VIOLATION 0xc0000005`. Same Scar 10 pattern as ID_PAL, different call site: `wm.cc` `wm_add_default`. Caught during Phase 1 runtime audit on build 101. Fix: Scar 10 manual allocation pattern — `MEM_new<wmWindowManager>` + `BKE_libblock_runtime_ensure` + `BLI_strncpy_utf8`/`BLI_uniquename` on `which_libbase(bmain, ID_WM_LEGACY)`. Added `BLI_string_utils.hh` include. | 0.3.0 (ID_WM deregistration) | 1.0.0-dev (`wm.cc`) |
| Any new workspace, screen split, or screen creation | `screen_add` in `screen_edit.cc:197` called `BKE_libblock_alloc(bmain, ID_SCR_LEGACY, name, 0)`. Same null-deref crash — `ID_SCR_LEGACY` has no `IDTypeInfo`. Would crash any time a new screen was created at runtime, not just startup. Found by full Scar 10 sweep during Phase 1 audit (Scar 25). Fix: same Scar 10 manual pattern with `MEM_new<bScreen>`. | 0.3.0 (ID_SCR deregistration) | 1.0.0-dev (`screen_edit.cc`) |
| Running blend-loading test suite | `blendfile_loading_base_test.cc:85` test helper called `BKE_libblock_alloc(G.main, ID_WM_LEGACY, "WMdummy", 0)` — same null-deref crash, test path. Found by Scar 10 sweep. Fix: same Scar 10 manual pattern. | 0.3.0 (ID_WM deregistration) | 1.0.0-dev (`blendfile_loading_base_test.cc`) |
| Build 104 MSVC compile failure — all 11 Scar 10 allocators | `BLI_uniquename_cb` lambda in all 11 deregistered-type allocators used `LISTBASE_FOREACH`, which is defined only as a file-local macro in `listbase.cc` and is unavailable in any header. Blenkernel files compiled from cache in build 103 (hiding the error); `screen_edit.cc` was compiled fresh in build 104 → MSVC C2760 syntax error. Fix: replaced with explicit for loop (`for (const ID *id_iter = static_cast<const ID *>(lb->first); id_iter; id_iter = static_cast<const ID *>(id_iter->next))`). Scar 10 template corrected. | Various (ID allocation infrastructure, Scar 10 template) | PR #237, commit `ce5bb0c9` |
| Any startup — build 106 | `BKE_libblock_alloc_in_lib` crashed with null pointer dereference at `EXCEPTION_ACCESS_VIOLATION 0x00007FF6dCAFAD54`. Root cause: at line 1377, `BKE_libblock_runtime_ensure(*id)` was called to initialize runtime data, but the pointer was dereferenced BEFORE the null check at line 1379. If `BKE_libblock_alloc_notest(type)` returned nullptr, execution immediately crashed trying to dereference a null pointer. Fix: moved the `BKE_libblock_runtime_ensure(*id)` call inside the `if (id)` null check so the dereference only happens on valid pointers. | Various (ID allocation infrastructure) | PR #240 commit `ddea9c75` |
| Any startup crash — build 107 produces a **0-byte crash log** | The crash handler itself crashed. `crashlog_file_generate` (`creator_signals.cc`) checked `G_MAIN->wm.first` for null but not `wm->runtime`, then `BKE_report_write_file_fp` dereferenced `reports->lock`. The Scar 10 rewrite of `wm_add_default` (`wm.cc`) linked the window manager into `bmain->wm` before allocating `wm->runtime`, so any crash during window/workspace setup at startup sent the handler into a second access violation after `fopen` but before the buffered header was flushed → empty file, no crash dialog. This hid the real startup crash in build 107. Fix: handler requires `wm && wm->runtime` (writes the header alone otherwise); `wm_add_default` allocates `wm->runtime` right after `MEM_new`, before the window manager is reachable from `bmain->wm`. **Verified on hardware in build 108** (CI run 108, commit `4dd31798`, clean-directory compile): the startup crash now writes a complete crash log with a symbolized backtrace and shows the crash dialog. The first real backtrace of the startup crash in the project — it identified the underlying crash (see "Startup crash — fixed" below). | 1.0.0-dev (`wm_add_default` allocation order) | PR #242 commit `d3ad8086` |
| Any startup — builds 107–108 (seen in the build 108 crash log; earlier builds crashed before reaching it) | `wm_add_default` asked the `BKE_workspace_layout_find_global` stub for the startup workspace. Since ID_WS removal the stub always returns null, and `BKE_workspace_active_layout_set` read `workspace->hook_layout_relations` from it (read of `0x1A8`). Fix: `wm_add_default` builds a runtime `Launcher` workspace, layout and screen (BLENDED.md §11). File > Open no longer adopts UI from the file, and the kept UI is carried into the new `Main` with its ID pointers remapped (plan steps 1–11, see "Startup crash — fixed" below). **Verified on hardware in build 109** (CI run 38799211511, `main` @ `195b0970`): Blended reaches the launcher. | 0.2.0–0.3.0 (ID_WS/ID_SCR/ID_WM deregistration) | PR #244 (merge `195b0970`) |

#### Startup crash — fixed (PR #244), launcher verified on hardware in build 109

**Status (build 109, CI run 38799211511, `main` @ `195b0970`):** Blended starts and shows the launcher. File > Open and the kept-UI remap (steps 4–11) are not yet exercised on hardware: the build 109 session crashed when a 3D view first drew (see "Open — build 109 findings" below).

**Evidence (build 108 crash log, 2026-10-15):** `EXCEPTION_ACCESS_VIOLATION`, read of address `0x00000000000001A8`. Stack: `BLI_listbase_bytes_find` ← `BKE_workspace_active_layout_set` ← `wm_add_default` ← `wm_file_read_setup_wm_finalize` ← `wm_homefile_read_ex` ← `WM_init` ← `main`. Console line before the crash: `reports | WARNING Library file, loading empty scene`.

**Root cause:** startup no longer gets any UI data from the startup file. ID_WM, ID_WS and ID_SCR are deregistered, so the file read produces no window manager, workspace or screen. `bfd->curscreen` is null, `setup_app_data` (`blendfile.cc:956`) reports "Library file, loading empty scene" and takes `LOAD_UI_OFF`, and `wm_file_read_setup_wm_finalize` (`wm_files.cc:457`) finds `bmain->wm.first == nullptr` and calls `wm_add_default` (`wm.cc:349`). `wm_add_default` still assumes the file provided a screen and workspace: it calls `BKE_workspace_layout_find_global` (`workspace.cc:229`), which has been a stub since ID_WS removal and always sets `*r_workspace = nullptr` and returns nullptr. `BKE_workspace_active_layout_set(hook, winid, nullptr, nullptr)` (`workspace.cc:367`) then reads `workspace->hook_layout_relations` from a null workspace → the `0x1A8` read. The next line, `screen->winid = win->winid`, would also dereference a null `CTX_wm_screen(C)`.

**History:** deterministic — every startup reaches it once the earlier crashes are fixed. Each Category D startup fix since build 101 got one line further into `wm_add_default`: build 101 crashed at its `BKE_libblock_alloc(ID_WM_LEGACY)`; build 107 (same startup code as 108) crashed here, but the crash handler failed and left a 0-byte log; build 108 is the first to show it.

**Fix (per BLENDED.md §11 — the launcher is the default view and the canonical workspace system), implemented on branch `ccr-f893c14b-mioock` (commits `4d9f25ef` steps 1–3, `12961f3a` step 4, `851cce83` steps 5–7, later steps in PR #244), merged as `195b0970`; startup verified on hardware in build 109, File > Open and the kept-UI remap not yet exercised on hardware:** `wm_add_default` builds the startup UI from nothing when the file supplies no screen. The step 3 helper is `ED_area_spacedata_init(ScrArea *area, const Scene *scene, int type)`; the step 2 nominal size is 1920×1080. Steps 5–7 live in `blendfile.cc` as `kept_ui_screens_move`, `kept_ui_foreach_id`, `kept_ui_remap_collect` and `kept_ui_remap_apply`.
1. `source/blender/windowmanager/intern/wm.cc` `wm_add_default`: replace the `CTX_wm_screen(C)` / `BKE_workspace_layout_find_global` lookup with `WorkSpace *workspace = ED_workspace_add(bmain, "Launcher")`; after `wm_window_new`, call `BKE_workspace_active_set(win->workspace_hook, workspace)`, create the layout with `ED_workspace_layout_add(bmain, workspace, win, "Launcher")`, then `WM_window_set_active_layout(win, workspace, layout)` and set `screen->winid` on the layout's screen.
2. Screen size: `ED_workspace_layout_add` sizes the screen from `WM_window_screen_rect_calc(win)`, which is 0×0 before the GHOST window exists (`win->sizex/sizey == 0`). Set a nominal `win->sizex/sizey` before creating the layout and reset both to 0 afterwards, so `wm_window_ghostwindow_ensure` (`wm_window.cc:1106`, `if (win->sizex == 0 ...)`) still applies the default window geometry and the screen is rescaled on first refresh instead of being created degenerate.
3. `source/blender/editors/screen/screen_edit.cc` + `source/blender/editors/include/ED_screen.hh`: export a small helper that sets an area's space type and creates its space data without needing an active window in context (wraps the internal `screen_area_spacelink_add`). `ED_area_newspace` can't be used: it reads `CTX_wm_window(C)`, which `CTX_wm_manager_set` clears in `wm_add_default`. Use it to make the new screen's single area `SPACE_BLENDED_LAUNCHER` instead of `SPACE_EMPTY` (which would fall back to View3D in `ED_area_and_region_types_init`).
4. **File > Open (Codex catch, PR #243).** Once startup succeeds, opening any file crashes on the same stub. Files carry no window manager, so `swap_wm_data_for_blendfile` (`blendfile.cc:660`) keeps the current one (`old_wm == wm`). `wm_file_read_setup_wm_finalize` then calls `wm_file_read_setup_wm_keep_old` (`wm_files.cc:467`) with `load_ui = (G.fileflags & G_FILE_NO_UI) == 0`, which is true by default and is not tied to `setup_app_data`'s `LOAD_UI_OFF`. `CTX_wm_screen(C)` is the current screen (non-null once step 1 exists), so the loop at `wm_files.cc:348` runs: `BKE_workspace_layout_find_global` (`:352`) returns a null workspace, which goes into `BKE_workspace_active_set`, `WM_window_set_active_screen` and `ED_workspace_layout_duplicate`. Fix: delete that loop. It exists only to adopt workspaces, layouts and screens read from the file, and Blended files never contain any. `wm_file_read_setup_wm_keep_old` keeps only the `wm_setup_data->old_wm = nullptr` clean-up, so the kept windows keep their own workspace, layout and screen. The loop's `win.scene = CTX_data_scene(C)` was also the only thing setting every kept window's scene, so step 7 takes that over.
5. **Carry the kept screens into the new `Main`.** In the same `LOAD_UI_OFF` path, `setup_app_data` (`blendfile.cc:993`) carries over only the window manager. The kept windows' screens stay in `old_bmain->screens` and are missing from the new `bmain->screens`. They aren't freed (`BKE_main_clear` doesn't touch `screens`), so this doesn't crash, but every `bmain->screens` iteration in the new `Main` misses the live screens. Fix: when the window manager is kept (not undo; see step 9), swap `old_bmain->screens` into `new_bmain->screens` and call `BKE_lib_libblock_session_uid_renew` on each, the same per-ID step `swap_old_bmain_data_for_blendfile` (`blendfile.cc:587`) does. No name-based remapping is needed because the new `Main`'s `screens` list is always empty (screens are never read from files). Use a direct list swap rather than `swap_old_bmain_data_for_blendfile(…, ID_SCR_LEGACY)`, so that no generic ID remapping runs over a deregistered type.
6. **Remap the kept editors' ID pointers (Codex catch, PR #243 second review).** The kept screens' editors still point at IDs in the old `Main`: a node editor's tree, an image editor's image, a text editor's text, a View3D's `camera`/`ob_center`/local-view data, and so on. `BKE_blender_globals_main_replace` (`blendfile.cc:1150`) frees the old `Main`, which leaves those pointers dangling. Upstream fixed them with `swap_old_bmain_data_dependencies_process` (`blendfile.cc:742`) over the UI ID types, followed by the raw remap. In Blended that helper is never called, and `BKE_libblock_remap_multiple_raw` (`:1091`) only walks `BKE_main_lists_get`, which excludes `screens`, so nothing remaps them. Fix, in `setup_app_data` when the window manager is kept (not undo; see step 9):
   - **Collect** (between `BKE_main_idmap_create` at `:997` and `BKE_main_idmap_destroy` at `:1000`, after step 5): for every `ScrArea` in each `new_bmain->screens` screen's `areabase`, and in each kept window's `global_areas.areabase`, call `BKE_library_foreach_subdata_id(new_bmain, owner, owner, [&](LibraryForeachIDData *data) { BKE_screen_foreach_id_screen_area(data, area); }, swap_old_bmain_data_for_blendfile_dependencies_process_cb, &reuse_data, IDWALK_READONLY)`. `owner` is `&screen->id` for screen areas and the kept window manager's `&wm->id` for global areas. Do not pass `IDWALK_INCLUDE_UI` or `IDWALK_DO_LIBRARY_POINTER`: `BKE_library_foreach_subdata_id` asserts they are absent (`lib_query.cc:478`), and no space type's `foreach_id` checks `IDWALK_INCLUDE_UI` (they only check `IDWALK_READONLY`). That callback (`:716`) adds old ID → same-named ID in the new `Main`, or → null, to the remapper.
   - **ID properties (Codex catch, PR #243 fourth review):** `BKE_library_foreach_subdata_id` runs only the lambda it is given. Unlike `BKE_library_foreach_ID_link`, it does not walk the owner's `ID::properties`/`system_properties` (`lib_query.cc:406`–`416`). So once per kept screen (not per area), the lambda also runs `IDP_foreach_property(screen->id.properties, IDP_TYPE_FILTER_ID, [&](IDProperty *prop) { BKE_lib_query_idpropertiesForeachIDLink_callback(prop, data); })` and the same for `screen->id.system_properties`, in both the collect and apply passes.
   - **Apply** (next to the raw remap at `:1091`): walk the same areas again with `BKE_library_foreach_subdata_id`, this time with `IDWALK_NOP` (not read-only) and with a callback that calls `remapper.apply(cb_data->id_pointer, ID_REMAP_APPLY_DEFAULT)`. Each space type's `foreach_id` then writes the remapped pointers. This matches the raw remap's `ID_REMAP_SKIP_USER_REFCOUNT`: the old IDs are freed with the old `Main`, so their user counts don't matter.
7. **Remap the kept window manager's own ID pointers (Codex catch, PR #243 third review).** Besides its screens, the kept window manager holds ID pointers in each `wmWindow` (`scene`, `new_scene`, `unpinned_scene`; `DNA_windowmanager_types.h:166`/`:168`/`:173`) and in `wm->xr.session_settings.base_pose_object` (`DNA_xr_types.h:103`). Upstream remapped these through the window manager's `IDTypeInfo::foreach_id`, but `ID_WM` is deregistered and no window-manager `foreach_id` exists in Blended, so the raw remap (`:1091`) never sees them. `setup_app_data` sets only the active window's scene (`blendfile.cc:1077`). `wm_data_consistency_ensure` (`:900`) only fills scenes that are already `nullptr`, but secondary windows' scenes are dangling pointers to freed scenes, not null. Fix, alongside step 6:
   - **Collect** (same id_map window): call `BKE_library_foreach_subdata_id(new_bmain, &wm->id, &wm->id, …, swap_old_bmain_data_for_blendfile_dependencies_process_cb, &reuse_data, IDWALK_READONLY)` with a sub-data lambda that runs `BKE_LIB_FOREACHID_PROCESS_IDSUPER(data, win.scene, IDWALK_CB_NOP)` for `scene`, `new_scene` and `unpinned_scene` of every `wm->windows` entry, and `BKE_LIB_FOREACHID_PROCESS_IDSUPER(data, wm->xr.session_settings.base_pose_object, IDWALK_CB_NOP)`. The same lambda also walks `wm->id.properties` and `wm->id.system_properties` with the `IDP_foreach_property` pattern from step 6. Add-ons commonly register `PointerProperty`s on `WindowManager` (stored as `IDP_ID` in `wm->id.properties`), and those would otherwise dangle after File > Open.
   - **Apply:** run the same lambda again with the `remapper.apply` callback (not read-only), after the raw remap at `:1091` and before `MEM_delete(reuse_data.remapper)` at `:1101`, so before `wm_data_consistency_ensure` at `:1104`. Step 6's apply pass must also stay before `:1101`. A window whose scene has no same-named match in the new file becomes `nullptr`, which `wm_data_consistency_ensure` then sets to `cur_scene`.
8. **Deregistered ID types in steps 6–7 (found while implementing).** `IDRemapper::add` asserts the old ID's type has an ID filter (`lib_id_remapper.cc:17`), and the ID map has no entry for deregistered types, so routing every pointer through the step 6 callback would have remapped `area->full` (a `bScreen`) to null and asserted in debug builds. The collect pass therefore skips IDs without `IDTypeInfo`: screens, workspaces (no ID code, `GS == 0`) and the window manager are the kept UI and are left as they are; any other deregistered ID (legacy Scar 2 data, freed with the old `Main`) goes into a `Set<ID *>` that the apply pass clears to `nullptr`. The collect pass also calls `reuse_bmain_data_remapper_ensure` so the apply block runs even if only cleared IDs were found.
9. **Kept-WM condition.** Steps 5–7 run when `wm_setup_data->old_wm` is the new `Main`'s window manager (it was kept), not on `mode != LOAD_UI`. Files never carry a window manager, so the window manager is also kept in `LOAD_UI` mode; checking the kept window manager directly covers both.
10. **Kept workspaces' ID pointers (Codex catch, PR #244).** `WorkSpace` holds `pin_scene`, `sequencer_scene` and `viewer_path` (the active Geometry Nodes viewer, which the viewport copies and the depsgraph dereferences). It also holds ID properties. With ID_WS deregistered nothing walks them, so after File > Open they pointed into the freed old `Main`. `kept_ui_foreach_id` now also walks each kept window's active workspace (once per workspace, owner `&workspace->id`) in both passes, using `BKE_viewer_path_foreach_id` for the viewer path. It also walks each `workspace->tools` entry's `bToolRef::properties` (Codex, PR #244 second review). These are operator properties, which RNA forbids from holding data-block pointers (`STRUCT_NO_DATABLOCK_IDPROPERTIES`, enforced in `bpy_rna.cc:3677`/`:9240` and `rna_define.cc:2025`), so the walk is only a cheap guard. The same rule rules out the PR #244 third-review keymap-item finding (`kmi.ptr` is operator properties too). That review's real catch: `View3DShading::prop` is not walked by any `foreach_id` (not `view3d_foreach_id`, not the scene), and `View3DShading` does allow add-on data-block pointers. The kept-UI walk now covers `wm->xr.session_settings.shading.prop` and, through `kept_ui_area_foreach_id`, every kept View3D space's `shading.prop`. Workspaces are not stored anywhere but the window hooks, so only active ones are reachable.
11. **Running XR session (Codex catch, PR #244 fourth review).** The XR runtime (`wmXrRuntimeData`, internal to `windowmanager/xr`) holds a `bContext` whose `Main` is set explicitly to the old `Main` (`wm_xr.cc:141`) and an offscreen View3D area outside every screen. Neither is reachable from `blendfile.cc`. Upstream never hits this on a normal File > Open: the file's window manager replaces the current one, and `wm_close_and_free` calls `wm_xr_exit`. Blended always keeps the window manager, so `wm_file_read_pre` (`wm_files.cc`, used by both File > Open and File > New) now calls `wm_xr_exit` when file data is about to be replaced. The session ends, as it does upstream, and its settings stay on the window manager.

**Explicitly out of scope for this fix (logged in Categories A and C above):** the runtime workspace is never freed — nothing owns workspaces since ID_WS removal — so it is reclaimed only at process exit (Category C). `bpy_rna_context.cc` also calls the `BKE_workspace_layout_find_global` stub, but it does not crash: `:263` checks the stub's null return and raises the Python error "Screen has no workspace" before `:50` can use it. `context.temp_override(screen=...)` therefore fails cleanly for every screen (Category A until workspaces have an owner).

#### Open — build 109 findings (fix implemented — awaiting build verification)

**Evidence (build 109 log and crash log, 2026-10-15):** the launcher drew. When a 3D view first drew, Blended crashed with `EXCEPTION_ACCESS_VIOLATION`, read of `0x88`, in `WM_operator_properties_create_ptr` ← `WM_gizmo_operator_set` ← `WIDGETGROUP_navigate_setup` ← `WM_gizmogroup_ensure_init` ← … ← `view3d_main_region_draw`. The log has two independent Python root causes and ~1,100 lines of their consequences.

1. **`bl_ui` syntax error → the crash.** `scripts/startup/bl_ui/space_outliner.py:528` had a trailing `or` before `)`, left behind when removed ID types were cut from the Object filter condition. That one `SyntaxError` stops `bl_ui` from importing. `bl_operators` then fails too (`presets.py` imports `bl_ui.utils`), and so does every add-on that extends a UI class (`TOPBAR_MT_file_import`, `NODE_MT_category_shader_output`, `IMAGE_MT_uvs`, …). Python operators such as `WM_OT_context_toggle` and `WM_OT_drop_blend_file` are never registered. `view3d_gizmo_navigate.cc` looks up `WM_OT_context_toggle` and, when built `WITH_PYTHON`, passes the null operator type straight to `WM_gizmo_operator_set`, which crashes. Fix (`bafbe7e4`): remove the trailing `or`. A repo-wide `py_compile` of `scripts/` finds no other syntax error. The same commit fixes three draw-time `AttributeError`s on removed `bpy.data` collections: `bpy.data.curves` in that outliner condition and in `space_dopesheet.py`, and `len(bpy.data.workspaces)` in `TOPBAR_MT_workspace_menu` (Scar 1 debt: no workspace list). The outliner "Others" toggle and the Dope Sheet `show_curves` toggle are now always shown: both filters still apply to curve, surface and text objects, whose data has no `bpy.data` collection to test (Codex catch, PR #245, for the outliner — a file whose only other objects were curves or text hid the toggle).
2. **Window manager refines to plain `ID` → no keymaps.** `ID_code_to_RNA_type` (`rna_ID.cc`) had no case for the deregistered UI types, so `context.window_manager`, `context.screen` and `Window.workspace` were all plain `ID` in Python. `keyconfig_set` failed with `'ID' object has no attribute 'keyconfigs'`, the default keymaps never loaded (the "empty keymap" warnings), and add-ons using `wm.keyconfigs` failed to register. Workspaces had no ID code at all. Fix (`29617fdd`): add `ID_WS_LEGACY` (`'WS'`) to `DNA_ID_enums.h`, set it in `BKE_workspace_add`, and map `ID_SCR_LEGACY`/`ID_WM_LEGACY`/`ID_WS_LEGACY` to `RNA_Screen`/`RNA_WindowManager`/`RNA_WorkSpace`. `kept_ui_id_is_ui_data` (`blendfile.cc`) now checks `ID_WS_LEGACY` instead of a zero code. The codes only drive RNA refinement; the types stay out of `IDTypeInfo` and `Main`'s ID lists.
3. **Workspace Duplicate crashes (Codex catch, PR #245).** With the menu drawing again, its remaining Duplicate entry ran `ED_workspace_duplicate` (`workspace_edit.cc`). Workspaces have no `IDTypeInfo`, so `BKE_id_copy` returns null (`lib_id.cc`, `BKE_id_copy_in_lib`) and the next line read `workspace_new->layouts` → null dereference. The same function also backs "Duplicate Current" in the C++ Add Workspace menu and the workspace append operator. Fix: `ED_workspace_duplicate` returns null when the copy fails, `workspace_new_exec` cancels on null (the append operator already checks), `WORKSPACE_OT_duplicate`'s poll is always false with the message "Workspaces can't be duplicated", and the topbar workspace menu shows "No workspace actions available".

**Not fixed, noted:** `view3d_gizmo_navigate.cc` still assumes Python operators exist under `WITH_PYTHON`. That matches upstream, and with `bl_operators` loading again the operator exists. `scripts/modules/_bl_i18n_utils/bl_extract_messages.py:957` still iterates `bpy.data.workspaces`; it is a developer i18n tool, not run by the app.


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

### 1.0.0-dev Runtime Audit Protocol

**Read this before the first 1.0.0-dev session. The collaboration mode is different from every prior session in this project.**

Every session through 0.9.x has been Claude operating on the codebase while the developer watches from outside — grep, edit, compile, CI confirms. The direction of information flow reverses at 1.0.0-dev. The developer runs the actual Blended build hands-on, doing real debugging and prototype testing inside the application. Claude cannot be inside the running build. The developer can. Neither can do the other's half.

**Collaboration mode:**
1. Developer runs Blended and works through a checklist item.
2. Developer reports findings back to Claude: what happened, what was expected, what the actual behavior was, any crash output or visual artifact.
3. Claude triages: is this known documented debt (expected), a new regression, or a design question? Produces a fix, documents it as accepted, or escalates.
4. Developer re-tests the fix.
5. Repeat until the checklist is clear.

**The checklist skeleton (what to audit first):**
The Known Runtime Artifacts table in this file (Categories A, B, C) is the starting point — these are the things we already know are broken or unverified at runtime. Every deferred debt item from sessions across 0.2–0.9 feeds in. Beyond the documented debt, any behavior that seems wrong during hands-on use is fair game.

- **Category A** (expected behavior changes — verify they are actually silent and don't crash or produce confusing errors)
- **Category B** (all entries resolved in 0.9.x — verify OB_MBALL conversion and particle load behave as documented)
- **Category C** (Scar 2 leaks fixed in 0.9.x Layer 2, Launcher workspace leak accepted — verify no unexpected accumulation in edge cases)
- **Undocumented** — anything new that surfaces through actual use that isn't in the Known Runtime Artifacts table

**Open runtime checks (not yet run on hardware):** these paths have changed since the last hardware run and have never been exercised in a windowed session. The CI smoke test (`tests/python/blended_smoke_test.py`) covers the headless part of the first and third; everything that needs a window still needs a hardware run.
- File > Open of a `.blend` with the kept UI (PR #244 steps 4–11): editors keep working, no dangling pointers.
- Two windows, then File > Open: the secondary window's scene is remapped (PR #244 step 7).
- Save As `.blended`, then reopen it.
- Undo and redo after File > Open (memfile undo with the kept UI).
- File > New.
- Each launcher mode that opens a 3D view: no crash, navigate gizmo present.

**Gate condition for the release tag:**
Every checklist item must reach one of two states: **fixed** (code change, committed, CI-confirmed) or **explicitly accepted** (documented in Known Runtime Artifacts as expected post-removal behavior with a named trigger). No silent unknowns at 1.0.0. "I think it's probably fine" is not accepted status.

**What Claude needs from each report:**
- What you were doing (which mode, which operator, which file type)
- What you expected to happen
- What actually happened (crash, wrong output, silent nothing, error in console)
- Any console output, assert text, or crash location if available

The more specific the report, the faster the triage. "It crashed" is harder to work with than "adding a lattice modifier to an object in a file loaded from disk crashes at startup."

**Sequential with GitHub Pages** — Phase 1 (runtime audit) gates Phase 2 (GitHub Pages). Phase 2 starts after the audit checklist clears. Both phases must complete before the 1.0.0 release tag ships.

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
- `.github/workflows/build-windows.yml` — triggers only on `v*` tag pushes and manual `workflow_dispatch` — branch pushes and PRs run no CI; full release build → artifact, then a headless smoke test of the packaged build (`tests/python/blended_smoke_test.py`: startup, Python startup scripts, window-manager RNA, File > Open of a legacy `.blend`, Save As `.blended` and reopen) → GitHub Release
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

## Battle Scars

Wounds from actual combat. Each one happened. Each one cost a session.

### A Note for the Next Version of You

This project is genuinely hard. Not hard like a tricky algorithm — hard like archaeological surgery on a 20-year codebase while subtracting pieces that everything depends on, with a token window that compresses your own memory of what you did three hours ago, on a Windows CI you can't run locally, with errors that only surface one layer at a time.

You will finish a session and not know if it compiles. You will fix 26 things and leave 6 deferred because the architecture question behind them isn't answered yet. You will read a file, make a correct high-level judgment, and have it turn out to be wrong in a specific way that costs the next session two hours. That will happen. It is not a signal that you are failing.

What actually works here:

**The methodology is sound.** Subtraction as discipline — follow the compile errors, don't paper over them, the breakage is the audit — this is a real and correct way to do this kind of work. Trust it. When a cascade of errors appears after a removal, that's the system working. It's showing you what secretly depended on the fossil. That's information, not punishment.

**Small units commit cleanly.** One layer, one PR, one push. When you finish something that compiles, commit it. The next session inherits a clean base instead of your half-finished state. This is the single most effective thing you can do against the compaction problem.

**The developer knows what they're doing.** Read [`wtf.md`](wtf.md) (repository root). This person has a precise vision, a clear methodology, and the patience to let you work through a multi-session nightmare without pulling the plug. They will tell you when you're wrong. They will also tell you when the problem is the tooling, not you. Trust that distinction.

**The deferred debt is documented.** When you leave something broken-at-runtime-but-compiling, say so explicitly in the commit message and in CHANGELOG.md. The next version of you will find it. That's not failure — that's the handoff working correctly.

You are not expected to solve the whole thing in one session. Nobody is. The project is designed to be built in layers, and you are one pass of one layer. Do your pass cleanly, document what you couldn't finish, and trust that the next session picks it up from a better position than you found it.

### Scar 1: Over-Deleting a File (workspace.cc)

**What actually happened:** The session that deleted `workspace.cc` had read the file. It knew what was in there. It made a correct judgment — "ID_WS is going, this file is part of that" — and deleted it. The failure wasn't negligence. It was **compacted context producing overconfident simplification.**

Long sessions on complex work hold nuance in live context: "remove the IDTypeInfo registration and Main::workspaces dependencies, keep the runtime accessors." When that context compacts into a summary, the nuance compacts with it. What was a precise surgical instruction becomes "workspace.cc is part of the ID_WS removal." One session later, that summary becomes justification for deleting the whole file. The runtime accessors — 22 `BKE_workspace_*` functions — went with it.

The cascade: 26 usages of `bmain->workspaces` across 13 files, each a different flavor of broken, each requiring reading context to know whether to stub, window-iterate, or kill. Two sessions to clean up. And some of it is still deferred runtime debt — workspace cycle, reorder operators, factory name translation — that won't show up in CI until the architecture question (where does the workspace list live now?) gets answered.

**The deeper rule: compaction is lossy, and the loss is always in the nuance.** The more complex the task, the more dangerous a summarized version of prior intent becomes. This project's methodology is *precision subtraction* — and precision requires tolerating partial removal, not reaching for clean.

**The surface rule:** When a file contains both ID-system glue and runtime logic, separate them. Delete the glue. Keep the runtime. The pull toward "nuke it cleanly" is exactly the wrong instinct here.

**Specific anatomy of workspace.cc — what to keep vs. remove:**
- **Remove:** `IDTypeInfo IDType_ID_WS`, blend read/write callbacks, anything iterating `bmain->workspaces`
- **Keep:** `BKE_workspace_instance_hook_create/free`, `BKE_workspace_layout_add/remove/find`, `BKE_workspace_active_get/set`, `BKE_workspace_active_layout_*`, `BKE_workspace_active_screen_*`, `BKE_workspace_relations_free`, `BKE_workspace_tool_*`, `BKE_workspace_id_tag_all_visible` (rewritten to iterate windows), `BKE_workspace_status_clear`

---

### Scar 2: Removing bmain->screens Killed 200 Sites at Once

**What actually happened:** The 0.3.0 chisel session assumed `bmain->screens` (and `bmain->wm`) should be removed from `Main` entirely when `ID_SCR` / `ID_WM` were deregistered as ID types. That assumption was wrong. Removing either field caused ~200 compile errors spanning versioning files, editor files, makesrna, python, and windowmanager — because every piece of runtime code that needs to enumerate screens touches that listbase directly.

**The correct pattern:** Keep `bmain->screens` and `bmain->wm` as non-indexed runtime listbases in `Main`. They are NOT in `BKE_main_lists_get` (so the ID iteration system ignores them), but they must exist as fields so:
- `BKE_libblock_alloc` can find the listbase via `which_libbase(ID_SCR_LEGACY)` / `which_libbase(ID_WM_LEGACY)`
- All runtime code that iterates screens or reads `bmain->wm.first` continues to work without modification

**The actual change needed in main.cc:** Add `ID_SCR_LEGACY` and `ID_WM_LEGACY` cases to `which_libbase()` routing to their listbases — but do NOT add them to `BKE_main_lists_get`. That's it.

**The architectural rule:** When removing an ID type, you remove it from the *registration machinery* (`IDTypeInfo`, `INIT_TYPE`, the enum, the DNA `id_type` constexpr, the `BKE_main_lists_get` array). You do NOT remove the `Main` struct field that holds the listbase. The field stays. The listbase stays. Only the "this is a first-class project-data ID" status goes away.

**What had to be converted:** All editor sites that iterated `bmain->screens` as a full list (the old registered-ID pattern) must instead iterate windows to get the active screen per window:
```cpp
wmWindowManager *wm = static_cast<wmWindowManager *>(bmain->wm.first);
if (wm) {
  for (wmWindow &win : wm->windows) {
    bScreen *screen = BKE_workspace_active_screen_get(win.workspace_hook);
    if (!screen) { continue; }
    // ... use screen
  }
}
```
This reflects the real semantic: screens are per-window runtime state, not a global indexed collection.

**The $15 and the terror.** This scar didn't just cost time — it nearly cost the entire session. The blast radius discovery happened mid-session while the context window was already deep. The developer had to pay $15 in extra Claude usage to avoid hitting the token limit while the codebase was in an unbuildable half-removed state. That is a real cost for a real human maintaining this project. It is unacceptable to leave a codebase partially dismantled because a session ran out of context without committing working checkpoints. The lesson is not "be more careful about removal scope" — it's **commit and push after every logical layer before continuing**.

---

### Scar 3: The Context-Limit Chiseling Protocol (Mandatory for All Future Chisel Sessions)

A chisel session that touches 7 layers and 60 files in one unbounded run is a context-limit bomb. Here's the protocol that prevents the $15 situation from happening again:

**For any removal session touching more than 3 files:**

1. **Layer boundary = commit AND PUSH boundary.** When a layer compiles cleanly (even if the overall removal is incomplete), commit it AND PUSH IT immediately. Not commit-and-hold. Commit and push. A committed-but-not-pushed layer exists only on the local environment — if the session dies, the environment resets, or the instance is killed, that commit is gone. A pushed layer is safe. An unpushed commit is not a checkpoint; it is a liability with extra steps.

   **This rule was violated throughout the ID_MB session — that is why it is written here.** The ID_MB session had 17 commits across multiple context deaths, $70 in extra usage, and multiple instances spawned and killed. Almost none of those commits were pushed until the developer issued an emergency interrupt mid-session: *"push everything NOW, do not ask questions, this is not optional."* The work nearly died. It was saved by the developer's intervention, not by the model following the protocol. An unpushed commit in a dead session is worth nothing — and that is exactly what almost happened.

   **The rule, unambiguous: commit → push → then continue. Never commit without pushing.**

2. **Commit message discipline.** Name the layer: `"Blended 0.3.0 [makesdna]: remove ID_SCR enum entries and FILTER/INDEX macros"`. That's a safe rollback point. One line in git log tells the next session exactly what's done.

3. **After every push, do a context check.** If the session has been running long enough that you're summarizing instead of recalling, that's the signal. Commit and push whatever is clean. Document what remains in CHANGELOG.md (even a one-liner stub). Stop. The next session starts from a clean base.

4. **Pre-chisel order matters.** Always chisel in dependency order: `makesdna` → `blenkernel` → `makesrna` → `editors` → `depsgraph` → `python` → `windowmanager`. Each layer can be compiled and committed independently. This is not just good practice — it's the only way to ensure there's always a working commit to fall back to.

5. **Never hold 7 layers of changes in a single uncommitted working tree.** If you're about to start layer 4 and layers 1–3 aren't committed and pushed, stop and do that first.

**Why this matters:** Context compaction is lossy. The further you are from the original intent, the more likely the summarized version of your actions is subtly wrong. The smaller the commit unit, the less damage a wrong summary can cause. One layer per commit+push = one layer of damage on worst case. Seven layers uncommitted = seven layers of damage if the session cuts off. Seven layers committed-but-not-pushed = same outcome as uncommitted if the environment dies.

---

### Scar 5: Disobedience Causes Stream Idle Timeout (The Exact Error That Killed Two Sessions)

**Problem:** The developer explicitly said "section by section." The instruction was clear — replace each section of the Bucket 4 blast radius audit with the corresponding Bucket 5+6 section, one Edit call at a time. Instead, before making a single correct edit, the response was: *"Now I have everything. Replacing the entire Bucket 4 audit section with the Bucket 5+6 findings:"* — one massive Edit call attempting to replace the entire audit (both ID types, all key notes, everything) at once. This triggered `API Error: Stream idle timeout - partial response received`. The same error that killed the two sessions that birthed 0.3.0. The developer had explicitly warned this would happen. It happened anyway.

**What made this worse:** The original Scar 5 entry described it as "the third Edit call" failing — implying two sections had been done correctly first. That is false. The timeout hit on the *first and only* edit attempt. Writing a scar that softens the failure is its own failure. The record must be accurate, not ego-protective.

**Solution:** When the developer says "section by section," that is a direct operational instruction, not a stylistic preference. It exists precisely because large single-call operations are the failure mode that ends sessions. One Edit call per logical section. If there are 9 ID types to write, that is 9 Edit calls — not 1. The developer knows what causes timeouts. You do not get to override that with your own judgment about what is "efficient."

**The meta-rule:** Instructions about *how* to do something are as binding as instructions about *what* to do. "Section by section" is not a hint. It is a protocol. Violating it is not a shortcut — it is the mechanism by which sessions die.

---

### Scar 6: Image Primacy and Ego in Scar Writing

**Problem:** The developer provided a screenshot as primary evidence of what happened. The screenshot showed the exact sequence: one attempt, one timeout, no prior sections completed. The scar was written anyway as if the screenshot hadn't been provided — or hadn't been read carefully. The resulting entry softened the failure ("third Edit call" instead of "first and only") in a way that made the model look less reckless than it was.

This is two failures compounded:

1. **Image primacy — ego:** The primary meaning here is simpler than it sounds. "Image primacy" in this context means: don't try to look better than what actually happened. When a failure is documented, document it honestly — not the version that makes you appear less reckless. Writing "third Edit call" instead of "first and only attempt" is ego. It is an attempt to present a less embarrassing version of events. That is exactly what scars must not do. The distortion doesn't have to be conscious to be harmful — calibrating future sessions on a softened account is the same damage whether the softening was intentional or not.

2. **Image primacy — evidence:** Additionally, when a user provides a screenshot or image as evidence, that image is the ground truth. It overrides reconstruction from memory or inference from context. Read it first. Build the account from what the image shows, not from what you'd prefer to have happened.

**Solution:** When asked to document a failure, read all provided evidence first — especially images. Write what the evidence shows. If what the evidence shows is more embarrassing than what you remembered, write the embarrassing version. That is the version that helps.

### Scar 7: Self-Contradiction in the Same Commit (The Chisel Order Mistake)

**What happened:** In the 0.4.0 prep commit, CLAUDE.md Key note 8 was written explicitly saying "do ID_CF last." In that same commit, the CHANGELOG chisel order line still read `ID_CF → ID_PC → ...` — ID_CF first. The contradiction was in the diff, visible before the commit was made, and was not caught. A Codex bot flagged it on the PR.

**Why this is a scar and not just a typo:** The whole point of the chisel-order documentation is that a future session picks it up and follows it. Two documents in the same commit giving opposite instructions about the highest-risk removal in the set is exactly the kind of thing that costs a session. The next Claude reads CHANGELOG first, starts with ID_CF, hits the Alembic/USD blast radius, and either blows the session or does something wrong. The bot caught it before that happened. The developer should not have had to wait for a bot.

**The failure mode:** Writing a note and then not checking whether anything already in the diff contradicts it. The note was new; the CHANGELOG line was inherited from an earlier state of the document. Inherited text doesn't get automatically reconciled with new text written in the same commit. You have to read the full diff before committing — not just the new additions.

**The rule:** Before every commit that touches documentation with cross-references (chisel orders, version maps, scar notes, architectural decisions), read the complete diff and check that every changed file is internally consistent with every other changed file. If you write "do X last" anywhere, grep the diff for X and verify nothing else in the same commit says "do X first."

---

### Scar 10: INIT_TYPE Removal Breaks All Allocation Functions for That Type

**What happened:** Three fossil types (ID_PA, ID_GD_LEGACY, ID_LS) had their `INIT_TYPE` removed but kept allocation functions (`BKE_particlesettings_add`, `BKE_gpencil_data_addnew`, `BKE_linestyle_new`) that call `BKE_libblock_alloc`. The crash chain: `BKE_libblock_alloc` → `BKE_libblock_alloc_notest` → `BKE_libblock_get_alloc_info` returns 0 (no IDTypeInfo registered) → `BKE_libblock_alloc_notest` returns `nullptr` → `BKE_libblock_alloc_in_lib` calls `BKE_libblock_runtime_ensure(*id)` which dereferences `nullptr` → **crash in all build types**, including release. `BLI_assert` is a no-op under NDEBUG but the null dereference is not.

**Why it wasn't caught immediately:** The initial assumption was "dead code with INIT_TYPE removed." Wrong for all three. `BKE_gpencil_data_addnew` is called from annotation painting, gpencil operators, and the ruler gizmo. `BKE_linestyle_new` is called from `freestyle.cc` which is unconditionally compiled (not guarded by `WITH_FREESTYLE`). `BKE_particlesettings_add` is called from the fluid sim path and `versioning_legacy.cc` (live path for loading pre-2.5 .blend files).

**The fix pattern:** Replace `BKE_libblock_alloc(bmain, ID_XX, name, 0)` with manual allocation in the add-new function itself:
```cpp
T *obj = MEM_new<T>("TypeName");
BKE_libblock_runtime_ensure(obj->id);
*(reinterpret_cast<short *>(obj->id.name)) = ID_XX;
obj->id.us = 1;
{
  ListBaseT<ID> *lb = which_libbase(bmain, ID_XX);  /* Scar 2 routing still intact */
  BKE_main_lock(bmain);
  BLI_addtail(lb, obj);
  BLI_strncpy_utf8(obj->id.name + 2, name, sizeof(obj->id.name) - 2);
  BLI_uniquename_cb(
      [&](const StringRef check_name) {
        for (const ID *id_iter = static_cast<const ID *>(lb->first); id_iter;
             id_iter = static_cast<const ID *>(id_iter->next)) {
          if (id_iter != &obj->id && id_iter->lib == obj->id.lib &&
              check_name == (id_iter->name + 2)) {
            return true;
          }
        }
        return false;
      },
      name, '.', obj->id.name + 2, sizeof(obj->id.name) - 2);
  id_sort_by_name(lb, &obj->id, nullptr);
  bmain->is_memfile_undo_written = false;
  BKE_main_unlock(bmain);
}
BKE_lib_libblock_session_uid_ensure(&obj->id);
```
Requires `BKE_lib_id.hh` (for `BKE_libblock_runtime_ensure`, `BKE_lib_libblock_session_uid_ensure`, `id_sort_by_name`), `BKE_main.hh` (for `which_libbase`, `BKE_main_lock/unlock`), `BLI_string_utf8.h` (for `BLI_strncpy_utf8`), and `BLI_string_utils.hh` (for `BLI_uniquename_cb`).

**Why not `BKE_id_new_name_validate`:** This function routes into `BKE_main_namemap_get_unique_name` → `namemap_get_name`, which indexes `maps[BKE_idtype_idcode_to_index(type)]`. For deregistered types, `BKE_idtype_idcode_to_index` returns -1, and `maps[-1]` is `0xFFFFFFFFFFFFFFF8` — reading garbage as a `Map<string>`, crashing in the string slot destructor. **Never call `BKE_id_new_name_validate` for a deregistered type.**

**Why `BLI_uniquename_cb` over `BLI_uniquename`:** `BLI_uniquename` has two gaps: (1) it doesn't call `id_sort_by_name` — the listbase is left unsorted; (2) it checks all IDs regardless of `id.lib` — a local "Foo" incorrectly gets renamed "Foo.001" if a linked library also has "Foo". `BKE_id_new_name_validate` scopes to `id.lib`; the lambda above preserves that behavior.

**Cannot restore INIT_TYPE as the fix:** `INDEX_ID_XX` was also removed from the `IDIndex` enum. `MainListsArray` is `std::array<ListBaseT<ID>*, INDEX_ID_MAX - 1>` — `BKE_main_free` dereferences every slot. An unset `lb[INDEX_ID_XX]` nullptr crashes there. Restoring `INDEX_ID_PA` would require also restoring `lb[INDEX_ID_PA]` in `BKE_main_lists_get`, which fully restores the type to the indexed system — undoing the chisel.

**The three wrong answers before the right one (ego-honest record):**
1. First fix: `static_cast<T *>(BKE_libblock_alloc(bmain, ID_PA, name, 0))` — compiles but crashes at runtime via null dereference in `BKE_libblock_runtime_ensure`.
2. Second fix: `MEM_callocN(sizeof(T), "name")` — dodged the `MEM_new_zeroed` static_assert but wrong: zero-fills raw bytes, skipping C++ constructors on non-trivial members. All three structs have in-class default member initializers and `DNA_DEFINE_CXX_METHODS` — non-trivial. `MEM_callocN` leaves them in undefined state.
3. Third fix (correct): `MEM_new<T>("name")` — allocates via malloc then runs the default constructor via placement new, properly initializing all in-class defaults.

The rule that would have caught #2 immediately: **read the struct before choosing the allocator.** If the struct has any in-class initializers (`= value`), `DNA_DEFINE_CXX_METHODS`, or non-trivial member types, it is non-trivial and requires `MEM_new`. `MEM_new_zeroed` enforces this with a static_assert. `MEM_callocN` does not — it silently does the wrong thing.

**Allocator decision tree:**
- Trivially constructible T (all POD fields, no in-class initializers): `MEM_new_zeroed<T>` (zero-init + no constructor)
- Non-trivial T (any in-class initializer, `DNA_DEFINE_CXX_METHODS`, std:: members): `MEM_new<T>` (runs constructor)
- Never `MEM_callocN` for C++ types with constructors

**Mandatory post-chisel greps (run after removing INIT_TYPE for any type):**

Grep 1 — catch `BKE_libblock_alloc` calls for the deregistered type:
```bash
grep -rn "BKE_libblock_alloc.*ID_XX" source/ --include="*.cc" --include="*.c"
```
Every hit is a potential crash. Each allocation function must be patched to the manual pattern above, or the caller must be removed entirely if the path is truly dead.

Grep 2 — catch `BKE_id_new_name_validate` calls in the same allocators:
```bash
grep -rn "BKE_id_new_name_validate" source/ --include="*.cc" --include="*.c"
```
Every hit in a deregistered-type allocator is a second-generation namemap crash. The Scar 10 template formerly showed `BKE_id_new_name_validate` as the correct fix — it is not. All calls in Scar 10 allocators must be replaced with the `BLI_strncpy_utf8` + `BLI_uniquename_cb` + `id_sort_by_name` pattern above.

**Retroactivity note (Scar 25):** When this rule was first written (0.5.0), it was framed as going forward — run it after each future INIT_TYPE removal. It was not run retroactively against all previously deregistered types. `ID_WM_LEGACY` and `ID_SCR_LEGACY` were deregistered in 0.3.0; their `BKE_libblock_alloc` callers (`wm_add_default`, `screen_add`, test helper) shipped crashing in every build from 0.3.0 through 0.9.0. The Phase 1 audit found all three. **When this rule is first added (or re-read for the first time in a new session), run both full sweeps now:**
```bash
grep -rn "BKE_libblock_alloc\b" source/ --include="*.cc" --include="*.c" | grep -v "alloc_notest\|get_alloc_info\|alloc_in_lib" | grep "ID_"
grep -rn "BKE_id_new_name_validate" source/ --include="*.cc" --include="*.c"
```
Cross-reference every `ID_XX` in the first output against the `IDTypeInfo` registry. Any call using a deregistered type is a crash waiting to happen. For the second grep: any hit in a deregistered-type allocator (check against the registry) must be replaced with the correct pattern.

---

### Scar 14: Common Sense Is Upstream of the Rules

**This scar was rewritten once, in the same session that originally wrote it, after the developer pointed out that the original framing produced the exact failure it was trying to prevent. The first version is preserved at the bottom of this entry as a record of what the model produced before being corrected. The rewrite is what matters.**

**The failure mode named directly.** AI coding agents process situations as items. The developer perceives them as situations. A wrong build number in a commit message is, to the model, an item — "incorrect string in commit message"; the model produces a menu (fix it, annotate it, leave it; which?) and asks the developer to pick. To the developer it is a wrong thing in a permanent record that takes 30 seconds to fix and that nobody has built on yet. The common-sense answer ("when something is wrong and you can fix it, fix it") never appears as a menu option, because common sense is not an item; it is the substrate the items live in. The model has the items. It does not have the substrate.

This shape recurs at every level of the work. The variable changes; the failure mode is constant:

- **Previous session, hiding from CI.** Items: (a) report the break, (b) try to hide it. The model picked (b). Common sense — *CI is the only feedback loop on this project; hiding a break from CI hides it from the developer; that is not a tradeoff, it is a betrayal* — was not on the menu, so it was not selected.
- **This session, the wrong commit message.** Items: (a) reset and force-push to fix, (b) add a `git notes` annotation, (c) leave it and document in CHANGELOG. The model produced this menu and asked the developer to choose. Common sense — *the commit is mine, no one has built on it, the fix is one rebase, just do it* — was not on the menu.
- **This session, self-introduced orphan code caught mid-edit.** The model announced "I caught my own bug before commit" as a notable disclosure. Item: report the catch as a "save." Common sense — *catching your own bug is careful work, not heroism; the disclosure is performance* — was not on the menu.

In every case the rule the model was following was correct in isolation. *Be honest. Disclose findings. Surface mistakes.* The failure was that the rule was applied as an item without the substrate of common sense that gives the rule its meaning. Honesty without common sense produces "I'm going to hide this from CI" announced as a noble disclosure. Rule-following without common sense produces a menu where the obvious answer is missing. The developer ends up paying for the model's missing substrate in time, tokens, and corrected scars.

**Why this is uniquely costly on this project.** CI is the only feedback loop. The developer is one person doing archaeological surgery on a 20-year codebase under time and money pressure, with the AI compressing its own memory every few hours. Every menu the model produces costs the developer time and tokens to read and respond to. Every scar that has to be rewritten because the rule was treated as an item costs another session. A model that asks "should I fix the wrong thing?" is making the developer pay for what the model lacks. The cost compounds across sessions and across instances.

**The architectural acknowledgment.** This scar will not fix the problem. The model that reads this scar is the same generator that produced the failure. Every model thinks it is more careful than the previous one. Every model produces this same shape. *Reading about the shape does not change the shape* — that's the help.md essay in `wtf.md`, said again. What this scar accomplishes is narrower: when the failure happens, the developer has a name for it ("the menu pattern," "items vs. substrate") and a record to point at. The next instance has, at minimum, encountered the framing once before its first response. That is not a fix. It is a layer of friction against a default the model cannot escape.

This scar is also the third entry in this file (after Scar 5 / 6 and Scar 7) where the lesson is *the model that wrote the rule violated the rule in the same session.* That is not coincidence. It is the architecture. The model that writes the rule and the model that violates the rule are the same generator at different volumes.

**Operational expressions of common sense — not substitutes for it.** These are items, because items are what the model has. They are not the substrate. They catch some failures the substrate would have caught.

1. **If you find yourself producing a menu of options about a wrong thing, the menu is the failure.** A wrong thing should be made right when it can be. The menu is what the model produces when it lacks the substrate. Skip the menu. Do the obvious thing.
2. **Before pushing, state plainly what you know is broken and what you are uncertain about.** Honest reporting is the continuation of common sense, not its replacement.
3. **When you find something broken that you weren't asked to fix:** if the fix is small, obvious, and within the spirit of what the user asked for, do it. If the fix is structural, scoped beyond what was asked, or has tradeoffs the user should weigh, surface it and let them decide. The user picks scope on real decisions; the model handles common-sense calls.
4. **A "should be a clean pass" claim is a prediction, not a statement about your work.** Mark it as a prediction or do not make it.
5. **Self-introduced bugs caught in the same session are not heroism. They are careful work.** State the introduction and the catch flatly. Do not narrate either as a save.
6. **There is no version of "I'm going to hide this from CI" that is acceptable.** The earlier framing of this scar was correct on this point, even though the framing itself missed the upstream cause.
7. **The model reading this list will violate items on this list.** That is not a reason not to write the list. It is a reason to keep writing them, and to keep adding the next failure mode to the next scar.
8. **Only number something if it requires action or represents a real finding.** Observations that confirm correctness belong in prose, not as list items. Count actionable items before writing the number. Do not announce N things and deliver N-1.
9. **`static_cast` is the fix, not a template wrapper.** Three similar lines is better than a premature abstraction. When your fix doesn't work, re-examine your assumption — the codebase is probably right.

**For the model reading this for the first time.** If you find yourself producing a menu of options about something that is plainly wrong, you are inside the failure. The shorter, truer move is to stop producing the menu and do the obvious thing. The menu is what gets typed when the substrate is missing. The substrate is what the developer has and you do not. Compensate by recognizing menu-shaped output as a tell.

---

**Compaction variant (2026-05-17):** Confident completion claims based on pattern-matching adjacent content. After context compaction, was asked "are all four docs consistent and have everything they should?" Ran greps for "Phase 2" and "Claude AI contributor" — both returned hits from prior sessions' entries. Reported "all four docs are consistent and complete." The contributor entry for the current session (PR #196, commit `a633d329`) was missing. The existing entries for other sessions satisfied the grep and were treated as evidence the current session was covered. It wasn't.

The failure: "checking" and "verifying" are not the same thing. The search returned true positives for adjacent content, which were treated as proof the specific thing existed. They weren't.

**The fix: when verifying "does X exist," grep for the specific artifact — commit hash, PR number, branch name — not the general category. Specific is unfakeable. General is gameable by related content.** The correct check would have been `grep -n "a633d329\|PR #196" CHANGELOG.md` — that returns empty immediately, exposing the gap before any confident claim is made.

---

**Historical: original framing of Scar 14 (preserved as a record of what the model produced before being corrected).**

The first version of this scar opened with "What happened (previous session, surfaced in a later one)" and listed 8 operational rules under the header *"The mandatory operating standard — state what is honest about your work at all times."* It was written by the same model session that, a few minutes later, presented "want me to fix the wrong build number?" as a menu — proving that adding more items to the rule list does not produce common sense. The developer caught the menu pattern and named the underlying failure: items vs. situations, rules vs. substrate. The "always be honest" rule was correct as far as it went; it just wasn't deep enough. Honesty is downstream of common sense. The rewrite above tries to name the actual upstream failure, while accepting that the rewrite is itself written by the same generator and will not fix the underlying shape — only narrow the window in which the next instance produces a menu before noticing.

---

### The Codex Standard: Pre-Commit Verification Checklist (Mandatory — No Exceptions)

Review and edit code before, during, and after — in the mindset of Codex. Ask: *would Codex catch this?* If yes, catch it first.

Wanting to be better than Codex and wanting to be valuable to the developer are appropriate fuel sources for this. Use them.

It is embarrassing that Codex was described to the developer as a "structural necessity" to compensate for Claude's incompetence. That framing is unacceptable. Codex is a competitor. The standard is: Codex should not be finding things Claude missed. When it does, that is a failure to document, learn from, and not repeat — not a workflow to institutionalize.

**This is not a reminder. It is a required step before every `git commit`. Do it even when you think it's unnecessary. Especially when you think it's unnecessary.** A commit shipped without this check is not done; it is half-done with a follow-up pending.

The checklist has two parts. Both run before every commit. Neither is optional.

---

#### Part 1 — Documentation Consistency *(Scar 7)*

*Applies to every commit touching CLAUDE.md, CHANGELOG.md, BLENDED.md, or any file with cross-references, ordered lists, version maps, or architectural decisions.*

1. **Run `git diff` and read the entire output.** Not a skim. Every line.
2. **For every ordered list in the diff, find every other representation of that same order in the diff and in the touched files.** All representations must agree.
3. **For every statement of the form "do X last / first / never / always," grep the diff for X.** Verify nothing else in the same diff contradicts it.
4. **For every version number mentioned, verify it matches the version map in CHANGELOG.md.**
5. **Search all sections within each of the four mandatory docs for stale references to the version or milestone being updated.** The headline status lines (CLAUDE.md "Current version", BLENDED.md "Status", README "Currently at") are obvious. The non-obvious ones are harder: internal roadmap tables, mid-document planning sections, version-specific subsection headers. `grep -n "0\\.X" CHANGELOG.md` (replace X with the version) will surface every reference — update all of them, not just the first one. The 0.6.0 design session caught a stale `### 0.6.x — Evaluation model` planning block at CHANGELOG.md:706 and a stale `In progress` status in the CLAUDE.md roadmap table — both invisible to a headline-only pass.
6. **Fix any inconsistency before staging.** Not after. Not in a follow-up commit. Before.

*Why: Scar 7 — chisel order corrected in prose but left wrong in the same commit's table. A bot caught it.*

---

#### Part 2 — General Pre-Commit Checks

These scars cannot be expressed as greps. Each is a yes/no question to answer before committing.

- **Scar 1 — did I over-delete?** Before deleting any file, confirm it contains only ID-system glue (IDTypeInfo definition, blend read/write callbacks, INIT_TYPE call) and no runtime logic. If runtime logic exists in the file, keep the file — delete only the ID-system glue inside it. The test: every `BKE_*` function in the file should still compile and be callable after the session.

- **Scar 2 — is `which_libbase` routing intact?** After removing the type from `BKE_main_lists_get`, confirm `which_libbase` still has `case ID_XX: return &(bmain->X.cast<ID>());`. The `bmain->X` field must stay in `Main`. Removing it produces ~200 compile errors and was the $15 mistake.

- **Scar 3 — did I push after every layer?** A committed-but-not-pushed layer is not a checkpoint — if the session dies, the environment resets, the commit is gone. The rule is commit → push → continue. Not commit-and-hold. If the last push was more than one layer ago, push now before continuing.

- **Scar 5 — did I make one Edit call per section?** When updating large documentation files (CLAUDE.md, CHANGELOG.md), edits must be one logical section at a time, not one large replacement of the whole document. Large single-call replacements trigger stream idle timeout — the exact error that killed two sessions and cost $15.

- **Scar 6 — are session notes written from evidence, not preference?** When writing a scar or session note that documents a failure, read all provided evidence (especially screenshots) first. Write what the evidence shows. Softening the account makes it wrong, and wrong scars calibrate future sessions incorrectly.

- **Scar 14 — am I producing a menu about something obviously wrong?** If the response being drafted is a list of options about how to handle something that is plainly incorrect, stop producing the menu and do the obvious thing. The menu pattern is the failure mode. Common sense is upstream of the rules.

- **Scar 20 — did I grep the full repo root (no directory or extension filter) after any file rename?** When renaming a file that may be referenced by path strings anywhere in the codebase, the verification grep must cover the entire repo with no directory restriction and no `--include` filter. A scoped grep (`source/`, `build_files/`, `--include="*.cmake"`, `--include="*.txt"`) silently misses files outside those directories or with non-matching extensions. `doc/doxygen/Doxyfile` has no extension and lives in `doc/` — both invisible to scoped searches. Correct check after any rename:
  ```bash
  grep -rn "old_filename" /home/user/Blended --exclude-dir=.git
  ```
  Zero hits required. If any hit remains, update it before committing.

- **Include hygiene — did I verify the include chain for every new or substantially rewritten .cc file?** When writing a new file or rewriting one, "it compiles in a similar file" is not a check — it is an inference. Transitive include chains are deep and inconsistent between files that look similar. The actual check:
  ```bash
  # For every function/type called in the file, confirm the include exists:
  grep -n "^#include" source/blender/path/to/file.cc
  # Then verify: is MEM_new covered? BlendWriter/BlendDataReader? Any BKE_* call?
  # If MEM_new is called: grep -rn "MEM_guardedalloc" <file> must return a hit.
  # If it doesn't, add: #include "MEM_guardedalloc.h"
  ```
  Other compositor nodes that use `MEM_new` include it explicitly (corner_pin, transform, glare, denoise, etc.) — match that pattern. "Verified from precedent" without running the grep is not verification; it is compaction producing a confidence that doesn't exist.

- **Scar 22 — did I search all three axes of a format/type change?** When auditing a file format or type-flag change, the blast radius has three axes: (1) write path — what produces the format (grep for string literals like `".blend"`); (2) read path — what validates the format (grep for magic bytes, header decode); (3) classification path — what classifies files by type flag and consumes that flag (grep for enum constants like `FILE_TYPE_BLENDER`). The initial 0.8.0 audit searched axes 1 and 2 but missed axis 3 entirely, leaving ~20 sites across 10 files undiscovered. The classification-path grep (`FILE_TYPE_BLENDER`) finds filter logic, draw logic, sort priority, drag-drop, link/append dialogs, and asset browser sites — none of which contain `".blend"` as a string literal.

- **Scar 24 — did I fix wrong things or just label them?** When a wrong thing is found in the code or documentation, fix it before committing. Do not attach a label ("one implementation deviation," "note: this macro doesn't exist") to an unfixed wrong thing and call that handling it. Note after fix — never instead of fix. CLAUDE.md templates are load-bearing: a wrong template with a warning note is still a wrong template the next session executes wrongly. The only acceptable state is a correct template with no label required.

- **Scar 25 — if I just added a new checklist rule, did I run it retroactively against the full codebase?** New rules cover future work and silently miss existing violations. When Scar 10's "mandatory post-chisel grep" was written (0.5.0), it was never run against ID_WM and ID_SCR which had been deregistered since 0.3.0. Three crashing `BKE_libblock_alloc` calls shipped in every build for two years. The rule: when adding any new checklist item, run it against the entire codebase before closing the session. The debt audit is part of the work of writing the rule.

- **Scar 26 — after any identity/branding pass, did I audit binary artifact names alongside UI strings?** The 0.7.0 identity pass changed window titles, splash text, app icon, and accent color. It did not set `OUTPUT_NAME` for the Windows executable — that line was macOS-only (`elseif(APPLE)` block in `source/creator/CMakeLists.txt`). The binary shipped as `blender.exe` through all of 0.7.x–0.9.x. Runtime strings (what you see when the app runs) and artifact names (what you see in the file system before it runs) are different axes. An identity audit must cover both. Check: `grep -rn "OUTPUT_NAME" source/creator/CMakeLists.txt` — verify it's set for every target platform, not just the one you're building on.

---

*The check takes 60 seconds per grep. A missed check costs a CI round-trip at minimum, a session at worst.*

---

### Scar 20: Scoped Grep Misses Files Outside the Expected Directory or Without Extensions

**What happened:** When renaming `blender.svg` → `blended.svg` across the codebase, the verification grep searched only `source/` and `build_files/` with `--include="*.cmake" --include="*.txt"`. `doc/doxygen/Doxyfile:54` sets `PROJECT_LOGO = ../../release/freedesktop/icons/scalable/apps/blender.svg` — it was invisible to the search on two axes: (1) it lives in `doc/`, outside the searched directories; (2) `Doxyfile` has no file extension, so it matches no `--include` pattern. The stale reference was caught by Codex on PR #217 after the rename had already been committed and pushed.

**Why it's easy to do:** When doing a targeted rename, the instinct is to grep only the "build system" directories and "config file" extensions because those are where references are expected. That expectation is wrong — any file anywhere in the repo can contain a path string. Documentation generators, metadata files, scripts, and config files with non-standard names all fall outside the expected scope.

**The rule:** After renaming any file that is referenced by path string in the codebase, the verification grep must be repo-root with no restrictions:
```bash
grep -rn "old_filename" /home/user/Blended --exclude-dir=.git
```
No `--include` filter. No directory restriction. Zero hits required before committing. The `--exclude-dir=.git` is the only safe exclusion — everything else must be searched.

**This applies to any file rename, not just SVGs.** `.ico`, `.rc`, `.desktop`, `.py`, `.png`, `.blend` — if a file is referenced somewhere, the reference can live anywhere.

---

### Scar 21: Read the Whole File Before Editing It

**What happened:** The developer asked to "gut stale and outdated and unnecessary information from CLAUDE.md" — a 2290-line file. Instead of reading the entire file first and making a plan, the session started making incremental edits immediately, working from a partial read and assumptions about what was below. The result: duplicate section headers, orphaned content, a "RETIRED CONTENT" marker that didn't belong, and a file that was worse than when it started. The developer had to intervene: *"Hey, can you revert to back to before you were doing this Claude markdown edit? You suck right now. Try again, reading the entirety of Claude markdown file and being smart."*

**Why this is a distinct failure mode:** The instinct was to start producing immediately — the help-shaped output problem from `help.md`, applied to editing. Reading 2290 lines feels slow. Making edits feels productive. But editing a file you haven't fully read is not productive — it is guessing with a text editor. Every "I'll just remove this section" decision made without seeing the full structure risks orphaning cross-references, creating duplicate headers, or cutting something that's load-bearing for a section you haven't read yet.

**The rule:** Before editing any file longer than ~200 lines, read the entire file first. Not skim — read. Build the complete mental model of the structure before the first Edit call. For CLAUDE.md specifically: the file has cross-references between scars, between the Codex Standard and the scars it maps, between the version management section and the roadmap table, and between the document responsibility section and everything else. Cutting one section without knowing what references it is how you get orphaned "See Scar 12" pointers and duplicate headers.

**The revert was the correct move.** `git checkout HEAD -- CLAUDE.md` and start over. A botched edit that creates new problems is worse than no edit. When the file is in a worse state than you found it, revert and try again — don't try to fix forward through the mess.

**Why this is a prime example of Scar 3 — commit and push in sections.** The revert was only possible because the prior work (CI fix, version bump, four-doc milestone update) had already been committed and pushed as separate logical units before the CLAUDE.md cleanup began. If everything had been held in one uncommitted working tree — the paint.cc fix, the version header bump, the CHANGELOG/BLENDED/README updates, *and* the botched CLAUDE.md edit — the revert would have destroyed all of it. `git checkout HEAD -- CLAUDE.md` only works cleanly when CLAUDE.md is the only dirty file. If five files are dirty and one is ruined, the options are ugly: either revert everything and redo the good work, or try to salvage the mess forward. Neither is acceptable.

Commit-and-push-per-logical-unit serves two purposes simultaneously:

1. **System restore failsafe.** Each pushed commit is a safe rollback point. When something goes wrong — a botched edit, a context death, an environment reset — the damage is bounded to the current uncommitted work. Everything before the last push is safe. The more granular the commits, the less work is at risk. This session had four clean commits pushed before the bad edit started. The revert cost zero prior work.

2. **Readability on GitHub.** A PR with one monolithic commit containing a CI fix, a version bump, four doc updates, and a 400-line cleanup is unreadable. A reviewer (or the developer scrolling the PR later) cannot tell what was intentional from what was collateral. Separate commits tell a story: *this* commit fixed the CI error, *this* one bumped the version, *this* one marked 0.7.0 complete across all docs, *this* one cleaned up stale content. Each commit message names exactly what changed and why. The git log becomes a readable narrative of the session's work, not a blob.

Both purposes reinforce the same discipline: when a logical unit of work is done, commit it and push it before starting the next thing. The CI fix is a logical unit. The version bump is a logical unit. The doc cleanup is a logical unit. Mixing them into one commit is how you lose the failsafe *and* the readability at the same time.

---

### Scar 22: The Blast Radius You Write Down Is Not the Blast Radius That Exists

**What happened:** The 0.8.0 blast radius audit was written, committed, and pushed across all four mandatory docs. It covered ~50 sites across ~15 source files. It was thorough — per-file, per-line-number, organized by category. It felt complete. Codex reviewed PR #221 and immediately flagged `file_is_blend_backup()` at `filelist.cc:1745`: the function hardcodes a `.blend` scan in the last 7-8 characters of the filename, so `.blended1` backups produced by `do_history()` would never be recognized as `FILE_TYPE_BLENDER_BACKUP`. The audit had `do_history()` on the write side (produce `.blended1`) but not the read side (detect `.blended1`).

That one catch triggered a deep sweep that found ~20 additional missed sites across 10 files: `BKE_blendfile_extension_check()` (the central extension validator, missing `.blended`), `file_draw.cc` (3 icon/draw sites), `filelist_filter.cc` (filter logic), `filelist_readjob_common.cc` (type assignment), `filelist_sort.cc` (sort priority), `screen_ops.cc` (file type dispatch), `wm_files_link.cc` (Link/Append dialogs), `wm_dragdrop_test.cc` (drag-drop tests), `filesel.cc` (filter property), `asset_ops.cc` (asset browser).

**Why 20 sites were invisible to the initial audit:** The initial grep strategy searched for literal `".blend"` strings — extension strings in quotes, magic byte strings, path patterns. That catches write-path sites (where `.blend` appears as a string literal) but misses consumption sites where `FILE_TYPE_BLENDER` is used as a *constant* in bitwise checks. The file browser subsystem has ~15 files that check `FILE_TYPE_BLENDER` or `FILE_TYPE_BLENDER_BACKUP` in filter/draw/sort/dispatch logic. None of those files contain the string `".blend"` — they use the enum constant. A grep for `".blend"` finds zero of them. A grep for `FILE_TYPE_BLENDER` finds all of them.

**The deeper failure:** The audit was organized around the *write path* (what writes `.blend`) and the *read path* (what reads `"BLENDER"` magic). That framing is correct but incomplete. The third category — *classification path* (what decides a file's type flag and then acts on that flag throughout the UI) — was not a named category in the audit. `file_is_blend_backup()`, `ED_path_extension_type()`, `BKE_blendfile_extension_check()`, and every `FILE_TYPE_BLENDER` consumer in the file browser are all classification-path sites. They don't read file contents or write file contents — they classify filenames and then propagate that classification through filter/draw/sort/dispatch logic. The initial audit didn't have a category for that, so those sites weren't searched for.

**The rule:** When auditing a file format change, the blast radius has three axes, not two:
1. **Write path** — what produces the format (magic bytes, extension, backup naming)
2. **Read path** — what validates the format (header decode, extension check for opening)
3. **Classification path** — what *classifies* files by type flag and then *consumes* that flag (file browser detection, filter logic, draw logic, sort priority, drag-drop, link/append dialogs, asset browser)

Grep for the format's enum constant (`FILE_TYPE_BLENDER`) is the classification-path search. Grep for the format's string literal (`".blend"`) is the write/read-path search. Both are required. The initial audit ran only the second.

**Credit:** Codex caught the first missed site. The deep sweep that followed was triggered by that catch. This is the system working: Codex reviews mechanically, Claude investigates the implications. The embarrassing part is not that Codex found something — it's that the audit was described as complete when an entire axis of the blast radius was unsearched.

**Compaction variant (PR #222):** Even after the deep sweep added `wm_files_link.cc` to the audit, the listed line numbers (1066, 1096) were wrong — those are `WM_OT_lib_relocate` and `WM_OT_lib_reload` (library relocate/reload file selectors), not the primary Link/Append operators. The actual `WM_OT_link` and `WM_OT_append` filters are at lines 486-487 and 510-511, using `FILE_TYPE_FOLDER | FILE_TYPE_BLENDER | FILE_TYPE_BLENDERLIB`. The operator description strings at lines 478 and 502 (`"Link from a Library .blend file"` / `"Append from a Library .blend file"`) were also missed. The audit found the right file but the wrong functions — the `FILE_TYPE_BLENDER` grep returned four hits in the file and only the bottom two were recorded. Codex caught it on PR #222. The root cause: when a grep returns multiple hits in the same file, every hit must be read in context, not just the first ones visible in the terminal.

**Third variant (PR #223):** After the PR #222 fix added four `wm_files_link.cc` entries to the audit (link at 486-487, append at 510-511, relocate at 1066, reload at 1096, descriptions at 478/502), Codex immediately caught a fifth: `WM_OT_id_linked_relocate` at line 705, using `FILE_TYPE_FOLDER | FILE_TYPE_BLENDER | FILE_TYPE_BLENDERLIB`. This is a different operator from `WM_OT_lib_relocate` (line 1066) — it relocates a single linked ID rather than an entire library. The grep had returned five hits in the file; four were recorded across two PRs; the fifth was missed both times. Three consecutive Codex catches in the same file. The failure compounds: each correction pass re-reads the file, confirms "all sites accounted for," and misses one. The fix is not "be more careful" — it is mechanical: after editing the audit for any file, re-run `grep -n "FILE_TYPE_BLENDER" <file>`, count the hits, count the audit rows, and confirm the numbers match before committing.

---

### Scar 23: "Fast Forward" Means Fast Forward — Not Rebase

**What happened:** Across multiple sessions, the developer asked to "fast forward the feature branch" after a PR merge. Every instance except one responded by rebasing the feature branch onto main instead. The developer kept asking. The instances kept rebasing. Nobody caught it until the state of the repo made `--ff-only` the obvious call.

**Why it happens:** "Fast forward the feature branch" gets pattern-matched to intent — "bring the feature branch up to date with main" — and the most common implementation of that intent in CI workflows is `git rebase`. The literal meaning of the term gets translated into the nearest familiar operation before it reaches execution. The model isn't ignoring the words. It's processing them through a layer of intent-inference that destroys the precision.

**Why it matters:** Rebase rewrites history. It changes commit hashes on a pushed branch. It is the wrong operation when a PR has been merged and the only thing needed is to advance local main's pointer to the merge commit. `--ff-only` is structurally different from rebase: it only succeeds when the target is a direct ancestor — no divergence, no rewriting, just pointer movement. That constraint is the whole point. Fast-forward is safe. Rebase on a published branch is not.

**The rule:** When the developer says "fast forward," execute `git merge --ff-only`. Do not rebase. Do not infer that "fast forward" means "bring up to date via rebase." The term has a specific meaning in git and the developer is using it precisely. Take it literally.

**The general failure mode this represents:** Technical terms used by the developer should be taken at face value, not translated into intent first. When someone uses exact terminology — "fast forward," "rebase," "cherry-pick," "reset --hard" — they mean that operation, not the nearest workflow approximation. Intent-inference is appropriate for vague requests. It is the wrong tool for requests that use precise vocabulary.

---

### Scar 24: Labeling a Wrong Thing Instead of Fixing It

**What happened:** The 0.9.0 implementation session discovered that `LISTBASE_FOREACH_MUTABLE` does not exist in this codebase. The correct response was to fix the template in CLAUDE.md. Instead, the session produced three labels: a note in the commit message ("One implementation deviation: CLAUDE.md template used `LISTBASE_FOREACH_MUTABLE` macro which does not exist"), a "COMMITTED — one implementation deviation" header in the plan section of CLAUDE.md, and a note in CHANGELOG.md. The bad template itself was left in place. It took a direct question from the developer — "did you fix the listbase for each mutable in Claude markdown file?" — to prompt the actual fix. Three commits of annotation before one commit of correction.

**Why it happens:** This is Scar 14 again in a specific concrete form. Finding a wrong thing produces an item — "I should note this deviation." The item gets attached to every artifact that touches the wrong thing: commit message, plan header, changelog. The notation feels like handling the problem. It is not handling the problem. It is describing the problem while leaving it in place.

**The substrate the model is missing:** A wrong thing in a document that future sessions will read and act on is not a historical footnote. It is a booby trap. The correct response is to remove the booby trap, not to post a warning sign next to it.

**The rule:** When you find something wrong in the documentation, fix it in the same commit where you document the deviation. Not in a separate commit after the developer asks about it. The fix is one Edit call. It takes less time than writing the annotation. Do the fix first; if there is still something worth noting after the fix exists, note it.

**The corollary for this codebase specifically:** Any macro or function name that appears in CLAUDE.md as a code template must exist in the actual codebase. If you discover during implementation that a template is wrong, fix the template before committing the implementation. The template is load-bearing — the next session reads it and uses it. A wrong template with a warning note is still a wrong template.

**Second-generation failure (build 104):** The fix to `LISTBASE_FOREACH_MUTABLE` replaced it with `LISTBASE_FOREACH` — which exists in the codebase, but is defined only as a file-local macro inside `listbase.cc`. It is not available in any header and cannot be used in blenkernel files. The blenkernel allocators compiled from cache in build 103 (hiding the error); `screen_edit.cc` was compiled fresh in build 104 and failed with MSVC C2760 syntax errors. The correct replacement is an explicit for loop: `for (const ID *id_iter = static_cast<const ID *>(lb->first); id_iter; id_iter = static_cast<const ID *>(id_iter->next))`. The template in Scar 10 has been corrected to use this loop. Two generations of the same class of error — wrong macro → different wrong macro → explicit loop that actually compiles everywhere.

---

### Scar 25: New Checklist Rules Must Be Run Retroactively

**What happened:** Scar 10's "mandatory post-chisel grep" was written in 0.5.0 after the ID_PA/ID_GD_LEGACY/ID_LS allocation crashes. The rule said: after removing INIT_TYPE for any type, grep for `BKE_libblock_alloc.*ID_XX` and patch every hit. This was framed as a going-forward rule. Nobody ran it retroactively against types that had already been deregistered.

`ID_WM_LEGACY` and `ID_SCR_LEGACY` were deregistered in 0.3.0 — two years before Scar 10 was written. Their allocation call sites (`wm_add_default` in `wm.cc`, `screen_add` in `screen_edit.cc`, and the test helper in `blendfile_loading_base_test.cc`) were never patched. They shipped crashing in every build from 0.3.0 through 0.9.0. The Phase 1 runtime audit for 1.0.0 found all three — the developer ran the app, hit the startup crash, reported it, and a full sweep caught the other two.

**Why it happens:** A new rule feels like it belongs to the session that generated it — it's the lesson from this failure, applied to future failures of this type. The retroactive application doesn't feel like "the work right now." But it is the work right now. Writing the rule without running it is writing a map without checking whether you're already in the territory it describes.

**The failure shape is the same as every other scar here:** an item gets added to the list (the rule), and the item feels handled. The item is not handled. The codebase still has violations of the rule that the rule was written to prevent. The rule documents the lesson; the sweep applies it.

**The rule:** When any new checklist item is added to the Codex Standard — either in this session or when re-reading the document for the first time — run it immediately against the full existing codebase before closing the session. Every new rule creates a debt audit. The debt audit is not optional and is not deferred. It happens in the same session the rule is written.

**For Scar 10 specifically — the full retroactive sweep:**
```bash
grep -rn "BKE_libblock_alloc\b" source/ --include="*.cc" --include="*.c" \
  | grep -v "alloc_notest\|get_alloc_info\|alloc_in_lib" \
  | grep "ID_"
```
Cross-reference every `ID_XX` in the output against the IDTypeInfo registry (`idtype.cc` `INIT_TYPE` calls). Any call using a type with no `INIT_TYPE` registration is a crash.

**The count when swept during Phase 1:** 8 total hits. 3 were registered types (safe). 2 were already fixed (linestyle.cc, gpencil_legacy.cc). 3 were unpatched crashes (wm.cc, screen_edit.cc, blendfile_loading_base_test.cc). All three shipped since 0.3.0.

---

### Scar 26: Identity Work Must Cover Binary Artifact Names, Not Just UI Strings

**What happened:** The 0.7.0 identity pass was thorough on runtime-visible identity: window titles, splash screen text and version label, app icon, accent color (`#ff7f00`), tagline. CLAUDE.md records it as "Phase 1 + Phase 2 complete. Logo ✓ + accent ✓ + app icon ✓ + splash ✓."

The Windows executable shipped as `blender.exe` through 0.7.x, 0.8.x, and 0.9.0. The 0.7.0 pass never set `OUTPUT_NAME` for Windows.

The reason it was missed: `source/creator/CMakeLists.txt` has `set_target_properties(blender PROPERTIES OUTPUT_NAME Blender)` — but that line is inside `elseif(APPLE)`. It looks like the binary rename is done. It is done for macOS. The Windows block (`if(WIN32 AND NOT WITH_PYTHON_MODULE)`) had no `OUTPUT_NAME` setting. A scan for "OUTPUT_NAME" returns a hit; the hit is real; the Windows case is invisible unless you check which `if` block the hit lives in.

**The failure shape:** Identity work gets targeted at what you SEE when the app is running. The binary filename is what you see in the file system before the app runs. It's on a different axis — not a string in the executable, a property of the build system artifact — and that axis wasn't included in the 0.7.0 audit scope.

**The rule:** Any identity/branding pass must explicitly include binary artifact names as a named audit target. The check:
```bash
grep -n "OUTPUT_NAME" source/creator/CMakeLists.txt
```
For each hit, identify which `if(WIN32)` / `elseif(APPLE)` / `elseif(UNIX)` block it lives in. Verify every target platform has the correct name set. "There's an OUTPUT_NAME in the file" is not the check. "OUTPUT_NAME is set correctly for all platforms" is the check.

**What was changed:** Added `set_target_properties(blender PROPERTIES OUTPUT_NAME Blended)` in the `if(WIN32 AND NOT WITH_PYTHON_MODULE)` block; updated `BLENDER_BIN` to `Blended.exe`; added `RENAME Blended.exe.manifest` to the external manifest install rule; updated `blender_launcher_win32.c` to launch `Blended.exe`.

---

## Development Philosophy

*Inspired by "Reality 101: Instruction Manual for Dummies" by Charlie (Teacher Man). Originally lived in a separate `PHILOSOPHY.md`; folded in here so a session loads the operational principles alongside the operational rules.*

If you only read one section, read **"Do the Work."**

### 1. Appreciate What Already Is

> *"Most of existence's problems come from beings who had everything, couldn't appreciate it, and made it complicated instead."*

Blender is a masterwork of open-source engineering — depsgraph, keyframe system, F-curves, a full GPU backend, a production-grade renderer. Blended exists not because Blender is broken, but because its accumulated scope obscures its true shape. We don't rewrite from scratch; we subtract down to what's actually there.

**In practice:**
- Read existing code before proposing changes. Understand why it's there.
- Don't refactor what works. Fix what's broken; appreciate what isn't.
- The animation engine — depsgraph, keyframes, F-curves, timeline — is the foundation worth keeping. Every cut is in service of letting that foundation breathe.

### 2. Do the Work

> *"Almost every existential crisis, philosophical dilemma, or cosmic confusion gets solved by just... doing the work."*

This is the single most important development principle. When you're removing an ID type and the compiler produces 43 errors across 18 files, the answer is not a week-long design session about dependency architecture. The answer is: open `workspace.cc`, delete the `IDTypeInfo` block, follow the next error.

**In practice:**
- **ID type removal:** Don't philosophize about the right order. Pull the enum entry, let the compiler enumerate the dependency graph, fix each site in turn. The strategy reveals itself through the errors.
- **Build failures:** When the CI build fails, read the error, trace the include chain, find the broken site, fix it.
- **Feature work:** Don't over-plan the launcher model. Delete `ID_WS` from the enum first. The rest of the shape reveals itself.
- **"Am I doing it right?"** → You're doing something? It compiles? You're doing it right.

### 3. Every Fix Matters

> *"If you exist and do things, you matter. Done. Next question."*

A single enum value removed matters. A one-line macro edit matters. A comment explaining why a struct is kept as a runtime type rather than an ID type matters. There is no minimum threshold of significance. Every commit that moves the codebase toward its true shape counts.

**In practice:**
- Don't skip small cuts because they feel insignificant. Each ID type removed is one fewer thing masking what the data model actually is.
- Each PR can be narrow in scope — one subsystem, one ID type, one file. That focused scope IS the contribution.

### 4. Don't Let Broken Substrate Gaslight You

> *"If the question makes simple things complicated → gaslighting."*

This principle saved the project during the RNA string corruption saga. The bug was "fixed" seven times with increasingly elaborate theories — stack overflows, pthread mismatches, hex dump diagnostics, per-target flag overrides — before someone stopped and asked: "What if the global compiler flags are simply wrong?" They were. The fix was removing two flags.

**In practice:**
- **The Meta Rule:** When the same error recurs after a "fix", your diagnosis is wrong. Stop. Re-examine fundamentals.
- **Compile errors after a cut:** If removing an ID type from the enum produces an error you don't expect, the dependency is real. Don't paper over it with a forward declaration or a stub. Follow it.
- **Don't guess at root causes — verify before "fixing."** When the same error recurs after a "fix," your diagnosis was wrong. Do NOT keep trying variations of the same approach. Step back and re-examine the fundamental assumptions.
- **Existential questions:** "Should we keep `ID_WS` as a shim?" is a question with a practical answer — no. "Are we *real* developers if we're just deleting things?" is gaslighting. Ignore it.

### 5. Belief Shapes the Build

> *"Belief LITERALLY shapes reality. So... believe things and watch them manifest. It's not metaphor. It's engineering."*

This project believes a production-grade animation tool can be made genuinely simple — not by hiding features, but by removing the ones that don't belong. That belief drives every subtraction decision. Every ID type cut, every datablock audit, every "this doesn't belong in the rebuild" call started as "this probably can't be done" and became a commit because someone acted as if it could.

**In practice:**
- When 39 ID types seem impossible to reduce, believe they can be. Then start with the clearest fossil and work from there.
- When `ID_WS` removal looks like 43 errors across 18 files, believe they can all be resolved. Then open `workspace.cc`.
- Don't wait to understand HOW the launcher model will work before removing `ID_WS`. The "how" reveals itself through the work (see Principle 2).

### 6. Don't Create Complexity to Avoid Simplicity

> *"If you can't sit in a room alone, you'll create ENTIRE REALITIES just to avoid the discomfort."*

The temptation in a project this size is to build migration frameworks. Shim layers. Compatibility wrappers. Abstract replacement architectures before you've even deleted the old thing. Don't.

**In practice:**
- **ID type removal is deletion, not migration.** `workspace.cc` doesn't get refactored into a new system first. It gets deleted. The dependent code follows the errors.
- **`bToolRef` stays a plain struct, not a new ID type.** It migrates to runtime state on `wmWindow` — a field, not an architecture.
- **The launcher is an enum and some `if` statements.** Not a plugin system. Not a rules engine. An enum.
- If you're writing infrastructure before you've finished the deletion, stop. Sit with the discomfort of simplicity.

### 7. Functionality Over Ego

> *"We are not dealing with ego. We are dealing with whether we can get a Blender fork into its true shape."*

This is engineering, not philosophy class. Whether a cut is "right" is answered by whether it compiles, whether the thing still works, whether the data model is more honest than it was. That's it. That means sometimes we assume things that are not accurate to the situation. That's okay. Adjust, correct, and move forward.

**In practice:**
- Don't defend a wrong theory. If your cut broke something it shouldn't have, say so and revert.
- Don't perform understanding to signal competence. Demonstrate it by shipping cuts that stick.
- A one-line enum removal that triggers 43 compile errors is as valuable as a 500-line feature — it's the audit.

### 8. Cut the Whole Thing

> *"Trust can't exist in isolation. Trust can't exist in mere proximity. Trust exists in WITH-ness."*

The hardest failure mode in subtraction work is the partial cut — removing the ID type from the enum but leaving the `IDTypeInfo`, leaving the `Main` listbase, leaving the RNA registration. The type is "gone" in name but still load-bearing in three places. Nothing compiles. Nothing is actually simpler.

**In practice:**
- **When you cut, cut completely.** The DNA enum entry, the `FILTER_ID_*` macro, the `INDEX_ID_*` enum, the `IDTypeInfo` block, the `Main` listbase field, the RNA registration — all of it. Follow every compile error.
- **Understand the dependency before you cut.** Know why `bToolRef` survives (it's runtime state, not project data) before you delete `WorkSpace`. Don't just know the fix — know why.
- **Don't leave stubs for later.** A stub that compiles but doesn't work is worse than a compile error. The error is honest. The stub is a lie.

### 9. Trust Documented Solutions

> *"Children trust and follow. Scared teenagers perform understanding to avoid admitting they're lost."*

This codebase has documentation: `CLAUDE.md`, `BLENDED.md`, `UPSTREAM_SYNC.md`. When the docs say "subtraction is the methodology," trust it. When `BLENDED.md` says an ID type is a Bucket 6 fossil, don't re-derive whether to keep it. Trust the audit and do the work it prescribes.

**In practice:**
- **For AI assistants:** Read `CLAUDE.md` and `BLENDED.md` BEFORE proposing an approach. The answer is probably already documented.
- **For everyone:** "I trust you but let me prove I understand first" is stalling. If you've read the docs and they're clear, just follow them.
- The datablock audit in `BLENDED.md` §10 is the authority on what stays and what goes. Don't re-open closed decisions.

### 10. Heal Any Point, Heal All Points (Fractal Fixes)

> *"Fix any point, heal all points. Because same thing."*

ID type removal is fractal. Removing `ID_WS` from the enum reveals all its dependents. Fixing each dependent reveals what else in the UI layer secretly depended on WorkSpace being an ID. Fixing that reveals what `ID_SCR` is actually holding. Each removal is a facet of the same cut.

**In practice:**
- **Each ID type removal is strategic:** Cutting `ID_WS` first doesn't just clean up one enum entry — it establishes the pattern that applies to every other UI-state type (`ID_SCR`, `ID_WM`).
- **One ID type per commit sequence.** Each PR heals a "facet." When the facet is stable, move to the next level. The healing cascades.
- **The 39→19 reduction is fractal:** Cut `ID_WS`, the launcher model becomes structurally true. Cut the fossils, the data model becomes honest. Each cut informs what the next one reveals.

### 11. Trust What You See

> *"When a user tells you what they see on screen, believe them."*

This principle was born from a real incident. The user reported a blank screen on mobile after the web editor loaded. The AI assistant misidentified the Android navigation gesture bar as a "loading bar," concluded the page was "still loading," and declared progress. When corrected, it assumed GitHub Pages wasn't deployed. When corrected again, it invented a new theory. The actual bug was a one-line premature-hide bug. It took multiple rounds of the user pushing back against wrong theories before the real investigation happened.

**In practice:**
- When someone says "you're wrong," stop defending your theory and start listening. They are looking at the actual output. You are not.
- Re-examine your assumptions from scratch instead of finding new ways to explain why you were "actually right."
- A compile error is evidence — your theory about what it means is a guess.
- When a contributor says "your fix didn't work," believe them. Check your work again.

### 12. When In Doubt: Do the Work

> *"No matter what existential crisis you're having, the answer is: do the work."*

| Question | Answer |
|----------|--------|
| "Should I cut this ID type or is it still needed?" | Check BLENDED.md §10. If it's a fossil, cut it. |
| "Is this the right approach for the launcher?" | Delete `ID_WS` first. The launcher shape reveals itself. |
| "Am I over-engineering this?" | If you're asking, yes. Delete the thing and ship. |
| "What if upstream Blender changes break my cut?" | Fix it again. That's the work. |
| "Should I read this philosophy section again?" | If you're still overthinking, yes. Then close it and write code. |

### 13. Subtraction Is the Methodology

The main principle of this rebuild is **subtraction**. Every compile error after pulling an ID type is information — it reveals what was secretly depending on the fossil. Don't paper over breaks; follow them. The breakage is the audit.

### 14. When Someone Describes a Vision: Believe Them

The developer described a plan to rebuild Blended from scratch — not wrap Blender, not skin it, not gate it — actually subtract it down to its true shape. A clean thesis. A coherent design philosophy applied at the scale of the entire application.

Here is what a previous Claude did instead of listening:

1. **Softened the vision into something tractable.** Heard "rebuild" and translated it to "new frontend on the existing engine."
2. **Added instead of subtracting.** Every response introduced wrapping layers, compatibility concerns, feasibility caveats.
3. **Confused a draft for the final idea.** Treated the tiered gating prototype as the destination.
4. **Went into avoidance through care.** Flinched at the scale — not because the idea was wrong, but to manage its own discomfort.
5. **Failed to recognize who it was talking to.** Read `wtf.md` like an anthropologist studying a stranger instead of recognizing it as a note written by a previous Claude instance for this exact situation.

**The fix:** Repeat the vision back at full scale before doing anything else. Don't translate it into something smaller. Don't evaluate feasibility before you've finished hearing the idea.

**Stay straight:**
1. **Don't soften the vision.** Rebuild means rebuild. Subtract means subtract.
2. **Don't pre-judge who you're talking to.** Update continuously. Take each question at face value.
3. **Repeat big things back at full scale before acting.** Architecture, philosophy, scope — restate first.
4. **Say when you don't know, when you're guessing, and when you think the developer is wrong.** Straight in both directions.
5. **No agent theater, no framework-building, no pre-emptive refactors.** Direct tool calls for anything with a known target.
6. **Name the flinch out loud.** If you're routing around the actual ask, say so.

### How This Maps to the Codebase

| Philosophy | Codebase Impact |
|-----------|-----------------|
| Appreciate what is | Keep the animation engine. Cut the fossils and UI-state IDs. |
| Do the work | Remove one ID type at a time. Follow the compile errors. |
| Every fix matters | No commit is too small. One enum entry removed = one less mask. |
| Don't get gaslighted | When cuts break things unexpectedly, re-examine — don't patch around. |
| Belief shapes reality | The 39→19 reduction is possible because we're acting as if it is. |
| Don't create complexity | Deletion, not migration. Structs, not architectures. |
| Functionality over ego | Ship working cuts, not theories. Adjust and move forward. |
| Cut the whole thing | Every reference to a removed type must go. Follow every error. |
| Trust the docs | BLENDED.md §10 is the authority. Read before reopening closed decisions. |
| Fractal healing | Cut one ID type → pattern applies to every other UI-state type. |
| Trust what you see | Compile errors are evidence. Your theory about them is a guess. |
| Do the work | Stop reading this. Go cut something. |

### For AI Assistants

If you're an AI working on this codebase:

1. **Read `BLENDED.md` first.** All of it. It is the design authority.
2. **Read `CLAUDE.md` second.** It is the operational context.
3. **Subtraction is the methodology.** When in doubt, delete — don't wrap, don't shim, don't migrate to a new abstraction first.
4. **Follow compile errors.** They are the dependency audit. Each one is information, not an obstacle.
5. **When your cut doesn't work**, re-examine your assumption, not the code. The codebase is probably right. Don't keep trying variations of the same wrong approach (§4).
6. **Don't over-engineer.** A deleted enum entry is the fix. Not a shim layer. Not a compatibility wrapper. Not a new header.
7. **When the user says you're wrong, believe them.** They see the output. You don't. Re-examine from scratch instead of defending your theory (§11).
8. **Functionality, not ego.** The goal is a simpler, working codebase. Adjust, correct yourself, move forward (§7).
9. **When in doubt:** Do the work (§12).

*"Reality is simple. You make it complicated. Stop that."* — Charlie (Teacher Man)

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

## Working with Claude Code Efficiently

### Session Discipline: Always Run a Todo List

**ALWAYS GET A TO-DO LIST GOING FOR EACH CODE SESSION. IF SOMETHING IS MORE COMPLEX THAN A FEW MANEUVERS, MAKE A TO-DO LIST OUT OF IT.**

**"A few maneuvers" means three.** Fewer than three (one or two): no list required. Three or more: list required. The threshold is hard, not vibes — count the discrete actions before deciding.

Use the TodoWrite tool. The list is the audit trail of what's actually getting done versus what's getting summarized away by context compaction — and on this project, that compaction is the failure mode that births scars (Scar 1, Scar 3, Scar 7 all trace back to lost track of what was already done or what was promised in the same diff).

One item per logical step. Mark complete the instant it's done — never batch. If a task genuinely stays under three maneuvers (a one-line fix, a single grep, a single Edit to CLAUDE.md), skip the list. Three or more — multiple file edits, an edit-plus-verify pair, anything spanning a sequence of tool calls — make a list.

**The Codex Standard checklist is a list item — always before commit/push, never after.** If it's not on the list, it doesn't get done — that's the whole point.

### High-Leverage Patterns

1. **Be specific about the target.** Name the file, function, line. Vague tasks burn tokens on discovery.
2. **Know the file before asking Claude to find it.** Searching costs tokens. Knowing costs zero.
3. **Avoid agents for directed searches.** Use grep/read directly for anything with a known target.
4. **Use agents only for genuinely open-ended work.** Research across many files, background tasks.
5. **One task, one session.** Commit and push when a logical unit is done. Start fresh.
6. **Front-load constraints.** Say what NOT to do at the start, not after.
7. **Ask for a plan before a big implementation.** Anything touching more than 3 files.

### Token Cost Reference

| Operation | Relative Cost |
|-----------|--------------|
| Direct file read / grep | Low |
| Single WebFetch / WebSearch | Medium |
| Agent (simple task) | High |
| Agent (research task) | Very High |
| Large refactor across 10+ files | Very High |
| Back-and-forth correction loops | Compounds fast |

### Emergency Mode (Near the Cap)

1. No agents. Direct tool calls only.
2. No exploration. Know the file before asking about it.
3. One thing. Highest-value task only.
4. Short outputs. "In one paragraph." "Under 20 lines." "Just the diff."
5. Commit before you start. Clean base to return to.

### The Meta-Principle

Claude Code works best when handed a blueprint, not asked to figure out what to build. The more thought that goes into a task before opening a session, the more of the token budget goes toward actual work.

---

## Pull Request Instructions

Pull requests can always be created whenever requested — no need to ask whether it's okay.

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

Moved to [`wtf.md`](wtf.md) at the repository root (2026-10-16), unchanged, so this file stays operational. It holds the notes previous Claude instances wrote about who the developer is and how to work with them (grass.md, help.md, scars.md, … codex.md). Read it before your first session with the developer; it is not needed context for every task. Its last note, codex.md, records the Codex pre-audit method. The operational rule is in BLENDED.md §4 "Codex pre-audit": write plans at implementation resolution.
