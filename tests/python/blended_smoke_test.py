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
- the file saves as `.blended` with the `BLENDED` magic and opens again.

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

    print("Blended smoke test passed")


main()
