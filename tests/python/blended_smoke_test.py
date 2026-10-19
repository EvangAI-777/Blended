# SPDX-FileCopyrightText: 2026 CHJ 3 Productions LLC
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Headless smoke test for a packaged Blended build, run by the Windows CI workflow.

A green compile has shipped builds that crashed at startup (docs/runtime-audit.md, Category D).
This script checks the runtime paths those crashes broke:

- startup completes and the startup scripts (`bl_ui`, `bl_operators`) import;
- Python operators register (the navigate gizmo needs `WM_OT_context_toggle`);
- the window manager refines to `WindowManager` in RNA (keymaps depend on it);
- a legacy `.blend` with UI data opens (File > Open with the kept window manager);
- the file saves as `.blended` with the `BLENDED` magic and opens again;
- the launcher keymap survives the Python keyconfig (build 110), Cycles loads, File > New gives
  an empty project and rendering it reports the missing camera (build 111);
- in CI (`BLENDED_SMOKE_CI=1`): the first-run copy from a seeded Blender folder, and a saved
  preference that `blended_prefs_check.py` reads back in a second run (build 111).

Usage:
  Blended.exe --background --factory-startup --python-exit-code 1 \\
      --python tests/python/blended_smoke_test.py -- <legacy.blend> <output-dir>

Any failed check raises, which `--python-exit-code 1` turns into exit code 1.
A crash exits with a non-zero code on its own.
"""

import os
import sys

import bpy


def check(condition, message):
    if not condition:
        raise RuntimeError("Smoke test failed: " + message)
    print("ok:", message)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) != 2:
        raise RuntimeError("expected arguments: <legacy.blend> <output-dir>")
    legacy_blend, output_dir = argv

    check("bl_ui" in sys.modules, "startup module bl_ui imported")
    check("bl_operators" in sys.modules, "startup module bl_operators imported")
    # Raises if the operator type is not registered.
    bpy.ops.wm.context_toggle.get_rna_type()
    check(True, "Python operator WM_OT_context_toggle registered")

    wm = bpy.context.window_manager
    check(wm is not None, "window manager exists")
    check(wm.bl_rna.identifier == "WindowManager", "window manager refines to WindowManager in RNA")
    check(hasattr(wm, "keyconfigs"), "window manager exposes keyconfigs")
    # Blended keeps its own user and cache folders, apart from Blender's (build 111 finding 5).
    user_dir = os.path.normpath(bpy.utils.resource_path('USER'))
    check(os.path.basename(os.path.dirname(user_dir)).lower() == "blended",
          "user folder is Blended's: " + user_dir)
    check("blender foundation" not in user_dir.lower(), "user folder is not under Blender Foundation")
    check("blended" in os.path.normpath(bpy.app.cachedir).lower(), "cache folder is Blended's: " + bpy.app.cachedir)
    # The General startup is an empty project: nothing behind the launcher (build 111).
    check(len(bpy.data.objects) == 0, "factory startup has no objects (got {})".format(len(bpy.data.objects)))

    # Background mode skips the Python keyconfig; load it the way a windowed start does. Its
    # refill wiped the launcher items added in C until they moved into blender_default.py (build 110).
    bpy.utils.keyconfig_init()
    launcher_km = wm.keyconfigs.default.keymaps.get("Blended Launcher")
    check(launcher_km is not None and len(launcher_km.keymap_items) > 0,
          "launcher keymap has items after the Python keyconfig")

    import addon_utils
    check(addon_utils.check("cycles")[1], "Cycles add-on is loaded")

    if os.environ.get("BLENDED_SMOKE_CI") == "1":
        # The workflow seeds the Blender user folder before the first run.
        bookmarks = os.path.join(user_dir, "config", "bookmarks.txt")
        check(os.path.isfile(bookmarks), "first run copied bookmarks from the Blender folder")
        with open(bookmarks, encoding="utf-8", errors="replace") as fh:
            check("blended-smoke-marker" in fh.read(), "copied bookmarks are the seeded ones")
        # Read back by blended_prefs_check.py in a second process.
        bpy.context.preferences.view.ui_scale = 1.25
        check(bpy.ops.wm.save_userpref() == {'FINISHED'}, "saved preferences")

    # blended_rig_compat adds Action.fcurves; unregistering it raised TypeError at quit (build 111).
    rig_compat = sys.modules.get("blended_rig_compat")
    check(rig_compat is not None, "startup module blended_rig_compat imported")
    check(hasattr(bpy.types.Action, "fcurves"), "rig compat adds Action.fcurves")
    rig_compat.unregister()
    check(not hasattr(bpy.types.Action, "fcurves"), "rig compat removes Action.fcurves")
    rig_compat.register()
    check(hasattr(bpy.types.Action, "fcurves"), "rig compat re-adds Action.fcurves")

    check(os.path.isfile(legacy_blend), "legacy .blend exists: " + legacy_blend)
    result = bpy.ops.wm.open_mainfile(filepath=legacy_blend)
    check(result == {'FINISHED'}, "opened legacy .blend")
    check(len(bpy.data.scenes) > 0, "legacy .blend has a scene")
    scene_names = sorted(scene.name for scene in bpy.data.scenes)

    os.makedirs(output_dir, exist_ok=True)
    blended_path = os.path.join(output_dir, "smoke_test.blended")
    result = bpy.ops.wm.save_as_mainfile(filepath=blended_path, compress=False)
    check(result == {'FINISHED'}, "saved .blended")
    with open(blended_path, "rb") as fh:
        magic = fh.read(7)
    check(magic == b"BLENDED", "saved file starts with BLENDED magic (got {!r})".format(magic))

    result = bpy.ops.wm.open_mainfile(filepath=blended_path)
    check(result == {'FINISHED'}, "reopened .blended")
    check(sorted(scene.name for scene in bpy.data.scenes) == scene_names, "scenes survive the round trip")

    # File > New > General passes an empty template name.
    check(bpy.ops.wm.read_homefile(app_template="") == {'FINISHED'}, "File > New > General")
    check(len(bpy.data.objects) == 0, "new General project has no objects (got {})".format(len(bpy.data.objects)))
    try:
        bpy.ops.render.render()
        rendered = True
    except RuntimeError as ex:
        rendered = False
        check("camera" in str(ex).lower(), "render of the empty project reports no camera: " + str(ex).strip())
    check(not rendered, "render of the empty project does not run")

    print("Blended smoke test passed")


main()
