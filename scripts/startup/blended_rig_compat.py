# SPDX-FileCopyrightText: 2025 Blended Authors
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Backward-compatibility shims for pre-5.0 rig scripts.

Blender 5.0 replaced the legacy action.fcurves API with a layered action
system (layers -> strips -> channelbags -> fcurves). Rig files generated
with Rigify before Blender 5.0 -- such as CGCookie Vonnbots rigs -- embed
Python scripts that access action.fcurves directly. That attribute no
longer exists on bpy.types.Action, so operators like IK/FK bake silently
fail or raise AttributeError.

This module adds action.fcurves as a read-compatible Python property that
flattens FCurves from all channelbags, restoring the iteration / find()
interface that old embedded scripts expect. The property is added only if
Action does not already expose fcurves (i.e. if upstream ever re-adds it,
we step aside).

Limitations: write operations (fcurves.new, fcurves.remove) are not
emulated. They are not used by the Rigify IK/FK snap or bake operators,
which are the operations that actually broke.
"""

import bpy


class _FCurvesCompat:
    """Proxy that flattens FCurves from all channelbags in all layers/strips.

    Supports the subset of the old action.fcurves interface that pre-5.0
    Rigify embedded scripts rely on: iteration, len(), indexed access, and
    the find() method used by ActionCurveTable.
    """

    __slots__ = ('_curves',)

    def __init__(self, action):
        self._curves = [
            fc
            for layer in action.layers
            for strip in layer.strips
            for cb in strip.channelbags
            for fc in cb.fcurves
        ]

    def __iter__(self):
        return iter(self._curves)

    def __len__(self):
        return len(self._curves)

    def __getitem__(self, index):
        return self._curves[index]

    def find(self, data_path, index=0):
        for fc in self._curves:
            if fc.data_path == data_path and fc.array_index == index:
                return fc
        return None


def _action_fcurves_get(self):
    return _FCurvesCompat(self)


_patched = False


def register():
    global _patched
    # Step aside if upstream ever re-adds Action.fcurves as an RNA property.
    if not _patched and 'fcurves' not in bpy.types.Action.bl_rna.properties:
        # Blender's RNA metaclass setattro allows plain Python descriptors to
        # be set on bpy.types.* when the attribute is not an existing RNA
        # property. On attribute lookup, pyrna_struct_getattro falls through to
        # PyObject_GenericGetAttr when RNA doesn't own the name, so our
        # property descriptor is found in the class dict and invoked normally.
        bpy.types.Action.fcurves = property(_action_fcurves_get)
        _patched = True


def unregister():
    global _patched
    if _patched:
        # The RNA metaclass __delattr__ frees a runtime RNA property of that
        # name if there is one; Action has no RNA fcurves, so it falls through
        # to the standard type deletion. type.__delattr__ can't be used here:
        # Python refuses to apply it to a metaclass that defines its own
        # __setattr__ (TypeError at quit, build 111 log).
        del bpy.types.Action.fcurves
        _patched = False
