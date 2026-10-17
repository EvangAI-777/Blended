# Fork Reference

Reference detail moved verbatim from CLAUDE.md in PR #253: where Blended's branding lives, the rig-compatibility and update-checker modules, the completed 0.8.0 and 0.9.0 layers, and the datablock audit result. CLAUDE.md keeps a one-line summary of each.

## Fork-Specific Patterns

### Branding

**Publisher:** Blended is developed and published by **CHJ 3 Productions LLC**, an Indiana-registered LLC. This is the legal entity behind the fork. All Blended-specific design decisions, the product identity, and fork-specific code additions are the work of CHJ 3 Productions LLC. Upstream Blender code retains its original copyright (Blender Foundation and contributors) under GPL-2.0-or-later — Blended inherits and preserves that license.

**Code locations:**
- `CMakeLists.txt:81` — `project(Blended)`
- `source/blender/blenkernel/BKE_blender_version.h` — `BLENDED_VERSION_MAJOR/MINOR/PATCH` defines (bump procedure: the `version-bump` skill), plus `BKE_blended_version_string()` declaration
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

## Completed Layers

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

## Datablock Audit

### Datablock Audit — Complete (BLENDED.md §10)
Result: 39 → ~19 ID types. All buckets closed.
- **Bucket 4 (UI state, remove):** `ID_WS` ✓ (0.2.0), `ID_SCR` ✓ (0.3.0), `ID_WM` ✓ (0.3.0)
- **Bucket 5 (upstream deprecations, finish):** `ID_CU_LEGACY` ✓ (0.4.0), `ID_GD_LEGACY` ✓ (0.4.0)
- **Bucket 6 (fossils, cut):** `ID_CF` ✓ (0.4.0); `ID_PC` ✓ (0.4.0); `ID_SPK` ✓ (0.4.0); `ID_PA` ✓ (0.4.0); `ID_LS` ✓ (0.4.0); `ID_MB` ✓ (0.4.0); `ID_TE` ✓ (0.4.0)
- **Bucket 3 (runtime types, fold-down then permanent home):** `ID_LP` ✓ (0.5.0 fold-down → 0.7.0 Light type flag), `ID_PAL` ✓ (0.5.0 → 0.7.0 Brush embed), `ID_LT` ✓ (0.5.0 → 0.7.0 LatticeModifierData), `ID_MSK` ✓ (0.5.0 → 0.7.0 compositor NodeTree), `ID_VF` ✓ (0.5.0 → 0.7.0 OB_FONT filepath), `ID_BR` ✓ (0.5.0 → 0.7.0 project-optional flag)

---
