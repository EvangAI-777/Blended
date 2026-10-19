# SPDX-FileCopyrightText: 2026 CHJ 3 Productions LLC
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Second smoke-test run: preferences saved by `blended_smoke_test.py` load on the next start.
Until build 111, Blended wrote `userpref.blend` but never read it back.

Usage (without --factory-startup, so preferences are read):
  Blended.exe --background --python-exit-code 1 --python tests/python/blended_prefs_check.py
"""

import bpy

scale = bpy.context.preferences.view.ui_scale
if abs(scale - 1.25) > 1e-6:
    raise RuntimeError("Smoke test failed: saved preference not loaded (ui_scale = {})".format(scale))
print("ok: saved preference loaded on the next start (ui_scale = {})".format(scale))
