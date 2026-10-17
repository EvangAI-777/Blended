# Syncing with Upstream Blender

Blended is a fork of [Blender](https://www.blender.org/). This document describes
how to manually merge upstream Blender changes into Blended.

> *"Appreciate what already is."* — Development Philosophy §1, [`BLENDED.md`](../BLENDED.md) appendix
>
> Upstream Blender is the foundation we build on. Syncing is an act of
> appreciation — integrating the work of hundreds of contributors while
> preserving the Blended layer on top. Don't fight the upstream; be WITH it.

## One-Time Setup

Add the upstream Blender repository as a remote:

```bash
git remote add upstream https://projects.blender.org/blender/blender.git
```

Verify:

```bash
git remote -v
# origin    https://github.com/EvangAI-777/Blended.git (fetch)
# origin    https://github.com/EvangAI-777/Blended.git (push)
# upstream  https://projects.blender.org/blender/blender.git (fetch)
# upstream  https://projects.blender.org/blender/blender.git (push)
```

## Merge Workflow

### 1. Fetch upstream

```bash
git fetch upstream
```

### 2. Create a sync branch

```bash
git checkout main
git checkout -b sync/blender-v5.3-release
```

### 3. Merge the upstream release branch

```bash
git merge upstream/blender-v5.3-release
```

### 4. Resolve conflicts

See the "Conflict-Prone Files" section below for guidance on each file.

### 5. Update library submodules

```bash
python build_files/utils/make_update.py
```

### 6. Build and test

Verify the build succeeds and Blended-specific features still work:

- Window title shows "Blended 0.x.x"
- Splash screen shows "Blended" name and tagline
- `blended_rig_compat.py` loads — pre-5.0 Rigify rigs can access `action.fcurves`
- Update checker starts background thread on `load_post`

### 7. Open a PR

Push your sync branch and open a pull request against `main` for review.

## Fork Point

Blended forked from upstream `main` at `03de53b7` (2026-04-23, Blender 5.2 alpha), the last upstream commit before Blended's own history. It is an ancestor of upstream `blender-v5.2-release`. No upstream commits have been merged or cherry-picked since. When some are, record the last one here.

Upstream is reachable from cloud sessions through the GitHub mirror (`https://github.com/blender/blender.git`); `projects.blender.org` is blocked there.

## Conflict-Prone Files

These files are modified by Blended and will likely conflict on upstream merges.
For each, keep the Blended additions and integrate new upstream changes around them.

| File | Blended Changes |
|------|-----------------|
| `source/blender/blenkernel/BKE_blender_version.h` | `BLENDED_VERSION_MAJOR/MINOR/PATCH` defines, `BKE_blended_version_string()` declaration |
| `source/blender/blenkernel/intern/blender.cc` | `blended_version_string` buffer, `BKE_blended_version_string()` implementation, `blender_version_init()` call |
| `source/blender/windowmanager/intern/wm_window.cc` | Fallback title `"Blended"`, title suffix uses `BKE_blended_version_string()` |
| `source/blender/windowmanager/intern/wm_splash_screen.cc` | Splash version label, about dialog name/description, tagline `"Blender, simplified."` |
| `CMakeLists.txt` | `project(Blended)` at line ~81 |
| `build_files/cmake/config/blended_release.cmake` | Blended-only file — won't conflict, just preserve |
| `scripts/startup/blended_rig_compat.py` | Blended-only file — won't conflict, just preserve |
| `scripts/startup/blended_update_check.py` | Blended-only file — won't conflict, just preserve |
| `release/windows/icons/winblender.rc` | `CompanyName`, `FileDescription`, `LegalCopyright`, `ProductName` updated to Blended |
| `release/freedesktop/blender.desktop` | `Name`, `Comment`, `StartupWMClass`, `Keywords` updated to Blended identity |
| `.github/` | Workflows, README — Blended-only, won't conflict with upstream |
| `BLENDED.md` | Blended-only file |
| `CLAUDE.md` | Blended-only file |
| `CHANGELOG.md` | Blended-only file |
| `.gitignore` | Negations after upstream's `.*` rule that track `.github/`, `.claude/skills/` and `.claude/rules/` |
| Everything in the Divergence Register below | See the register |

## Divergence Register

Every place Blended deliberately differs from upstream Blender, one row per change: what it is, the main files, why (the `BLENDED.md` section that decides it), and when it could be dropped. Use it to triage each upstream merge: a conflict in a listed file is expected and resolved in Blended's favor; a conflict anywhere else is new and needs a look. Most rows say "never": the subtraction is the point. When a PR adds or removes a divergence, it updates this table.

| Change | Main files | Why | Drop when |
|--------|-----------|-----|-----------|
| Product identity and versioning | `BKE_blender_version.h`, `blender.cc`, `CMakeLists.txt` (`project`), `source/creator/CMakeLists.txt` (`OUTPUT_NAME Blended`, `Blended.exe`), `wm_window.cc`, `wm_splash_screen.cc`, `release/windows/icons/winblender.rc`, `release/freedesktop/blender.desktop` | §16 product identity | Never |
| Blended user folders | `GHOST_SystemPaths{Win32,Unix,Cocoa}` (`Blended\X.X`, `~/.config/blended/X.X`, `Application Support/Blended/X.X`), `appdir.cc` (cache folder, `BKE_appdir_user_dir_migrate_from_blender`), `creator.cc`, `preferences.cc` (`Documents/Blended/Assets`), PR #254 | Blended and Blender must not share add-ons, extensions, recent files or each other's preference files | Never |
| UI text names Blended | ~55 files: operator names and tooltips, RNA descriptions, reports and dialogs (`wm_files.cc`, `wm_operators.cc`, `rna_userdef.cc`, `rna_space.cc`, `io_*.cc`, `system_win32.cc`, `cpu_check.cc`, `render_view.cc`, `info_stats.cc`, `bl_ui`, `bl_operators`, the Cycles add-on), PR #254 | §16 identity. Rule: "Blended" where the text means the running application; "Blender" for Blender versions and compatibility, `.blend` as a Blender file, interop metadata, the Blender unit, preset names and Help links to blender.org | Never. An upstream merge brings back new "Blender" strings: re-run the grep (`docs/runtime-audit.md`, build 111 finding 4) |
| Launcher instead of the splash | `editors/space_blended_launcher/`, `rna_space.cc` (`SPACE_BLENDED_LAUNCHER`), `wm_init_exit.cc` (`WM_init_splash` is a no-op), launcher keymap in `blender_default.py` / `industry_compatible_data.py` / `keymap_hierarchy.py` | §11–12 launcher and mode lenses | Never |
| UI-state ID types removed (`ID_WS`, `ID_SCR`, `ID_WM`) | `workspace.cc`, `screen.cc`, `wm.cc` (`wm_add_default` builds the runtime Launcher UI), `wm_files.cc`, `blendfile.cc` (`kept_ui_*` remap), `screen_edit.cc`, `lib_id_delete.cc` (`id_free_runtime_screen`), `rna_ID.cc` (legacy codes → RNA types), `DNA_ID_enums.h`, `main.cc` (`which_libbase`), workspace operators and menus | §10 Bucket 4 | Never; the post-1.0 user-workspaces plan changes the workspace part |
| Fossil and deprecated ID types removed (`ID_CU_LEGACY`, `ID_GD_LEGACY`, `ID_CF`, `ID_PC`, `ID_SPK`, `ID_PA`, `ID_LS`, `ID_MB`, `ID_TE`) | `idtype.cc`, `main.cc` (kept listbases, `BKE_main_clear` drain), `DNA_ID_enums.h`, the Scar 10 allocators (`particle.cc`, `gpencil_legacy.cc`, `linestyle.cc`, `curve.cc`), `geometry_component_curves.cc`, depsgraph, outliner, animation channels, RNA, `intern/cycles/blender/addon/properties.py` | §10 Buckets 5–6 | Never |
| Runtime types folded down (`ID_LP`, `ID_PAL`, `ID_LT`, `ID_MSK`, `ID_VF`, `ID_BR`) | `lightprobe.cc`, `paint.cc`, `lattice.cc`, mask, vfont and `brush.cc`, plus their permanent homes (Light type flag, Brush embed, `LatticeModifierData`, compositor node tree, `OB_FONT` filepath) | §10 Bucket 3 | Never |
| `.blended` native format | `BLENDED` magic in read/write, `FILE_TYPE_BLENDED`, file browser filter/draw/sort, `wm_files*.cc`, `wm_operator_props.cc` (`filter_blended`), platform registration (Windows, Linux MIME, macOS UTI) | §5 file format | Never |
| `.blend` import | `versioning_520.cc` (502.23 `OB_SPEAKER` → `OB_EMPTY`, 502.31 `OB_MBALL` → `OB_EMPTY`), dropped-data manifest Text block | §5, 0.9.0 | Never |
| Python UI for removed types | `scripts/startup/bl_ui/` (outliner, dope sheet, topbar workspace menu), `bl_operators` | §10 | Never; review on every sync |
| Blended-only scripts | `scripts/startup/blended_rig_compat.py`, `scripts/startup/blended_update_check.py` | Rigify on pre-5.0 rigs; release updates | Rig compat: when Rigify stops reading `action.fcurves` |
| Release build configuration | `build_files/cmake/config/blended_release.cmake` (GPU binaries and Freestyle off) | Build size; Freestyle removed (`ID_LS`) | Never |
| Repository and tooling | `.github/`, `.claude/`, `docs/`, `tools/check_blended.py`, `tests/python/blended_smoke_test.py`, `AGENTS.md`, `CLAUDE.md`, `BLENDED.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `.gitignore` (negations for `.github/`, `.claude/`) | Blended's own process | Never |
| Upstream repository tooling removed | `.gitea/`, `.github/FUNDING.yml`, `.well-known/funding-manifest-urls` | Upstream identity and Gitea-only tooling (PR #252) | Never. **An upstream merge brings them back: delete them again.** |

## After Syncing: Version Bump Checklist

When syncing to a new Blender release (e.g., 5.2 to 5.3):

1. Check `BLENDER_VERSION` integer in `BKE_blender_version.h` matches the new upstream value
2. Consider bumping `BLENDED_VERSION_MINOR` or `BLENDED_VERSION_PATCH`
3. Update `.github/README.md` to reference the new upstream base version
4. Test that `.blend` file compatibility is maintained (`BLENDER_FILE_VERSION` tracks upstream)

---

## Cherry-Picking

Rather than doing a full merge, individual upstream commits can be cherry-picked
when they fix something Blended already touches or add a capability that fits
the project's goals without conflict risk.

### When to Cherry-Pick vs Full Merge

Cherry-pick when:
- The change is isolated to one or two files with no Blended overlap
- It's a bug fix in a subsystem Blended modifies (safer to pull in early)
- It's a feature directly relevant to animation or the pipeline identity

Full merge instead when:
- Many related commits need to land together to work correctly
- Dependency libraries (OpenVDB, OpenColorIO, etc.) are updated
- Python version is bumped (requires coordinated changes across many files)

### How to Verify a Cherry-Pick Candidate

```bash
# Find the commit on the upstream branch
git fetch upstream
git log upstream/blender-v5.3-release --oneline --grep="asset librar"

# Preview what the commit changes
git show <commit-sha> --stat

# Cherry-pick onto your sync branch
git cherry-pick <commit-sha>
```

If the cherry-pick conflicts with a Blended-modified file, resolve by keeping
the Blended addition and integrating the upstream change around it — same
strategy as a full merge conflict. See "Conflict-Prone Files" above.

---

## Lightweight Triage via Screenshots

Don't want to run the sync workflow or set up the upstream remote? Just take
screenshots of the upstream commit log and hand them to Claude.

**How:**

1. Go to `https://projects.blender.org/blender/blender/commits/branch/blender-v5.3-release`
2. Screenshot the commit list — one or more pages, however far back you need
3. Open a Claude Code session and drop the screenshots in
4. Say something like: *"here are the upstream commits since our last sync — sort through these and tell me what's worth cherry-picking for Blended"*

Claude will go through each commit, flag what's relevant to Blended's current
scope (animation, depsgraph, branding files, rig system, Python API, dependency
updates), and skip what isn't (WASM, platform-specific subsystems we don't ship,
features in Bucket 6 fossils, etc.). For anything worth pulling, it'll either
apply the cherry-pick directly or give you the SHA and rationale so you can
decide.

This works well for keeping up with upstream between full merges — catching bug
fixes and small improvements without the overhead of a full sync branch.

