#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 CHJ 3 Productions LLC
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
Fast source checks for Blended, run on every pull request (`.github/workflows/checks.yml`).

Each check targets a class of bug that once shipped in a Windows build and was only found on
hardware (CLAUDE.md, Category D). None of them needs a build:

- Python syntax in the shipped scripts. A single `SyntaxError` in `bl_ui` crashed build 109.
- Allocation of a deregistered ID type through `BKE_libblock_alloc` / `BKE_id_new`. Without
  `IDTypeInfo` the allocation returns null and the caller dereferences it (Scar 10).
- `bpy.types` references to RNA types removed with their ID type. `bpy.types.MetaBall` stopped
  Cycles from registering in build 110.
- `LISTBASE_FOREACH` outside `listbase.cc`, where it is a file-local macro. It broke the
  build 104 compile (Scar 24).

Usage: python3 tools/check_blended.py   (from the repository root; exit code 1 on any failure)
"""

import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

PYTHON_DIRS = (
    "scripts",
    os.path.join("intern", "cycles", "blender", "addon"),
    os.path.join("tests", "python"),
)

# `#define ID_*` codes in DNA_ID_enums.h that are not ID types at all.
NON_ID_CODES = {
    "ID_LINK_PLACEHOLDER", "ID_SCRN", "ID_SEQ", "ID_CO", "ID_PO", "ID_NLA", "ID_FLUIDSIM",
}

# RNA types removed together with their ID type (BLENDED.md §10).
REMOVED_RNA_TYPES = ("MetaBall", "Speaker", "PaintCurve", "CacheFile")

SOURCE_EXTENSIONS = (".c", ".cc", ".cpp", ".h", ".hh")


def read(path):
    with open(path, encoding="utf-8", errors="surrogateescape") as fh:
        return fh.read()


def walk(subdir, extensions):
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, subdir)):
        dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git"}]
        for name in sorted(filenames):
            if name.endswith(extensions):
                yield os.path.join(dirpath, name)


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def strip_c_comments(text):
    """Blank out comments, keeping newlines so line numbers stay right."""
    def blank(match):
        return re.sub(r"[^\n]", " ", match.group(0))
    pattern = r"//[^\n]*|/\*.*?\*/|\"(?:\\.|[^\"\\\n])*\""
    return re.sub(pattern, lambda m: m.group(0) if m.group(0).startswith('"') else blank(m), text,
                  flags=re.DOTALL)


def check_python_syntax():
    errors = []
    for subdir in PYTHON_DIRS:
        for path in walk(subdir, (".py",)):
            try:
                compile(read(path), path, "exec", dont_inherit=True)
            except SyntaxError as ex:
                errors.append("{}:{}: SyntaxError: {}".format(rel(path), ex.lineno, ex.msg))
    return errors


def deregistered_id_codes():
    registered = set(re.findall(
        r"INIT_TYPE\((ID_[A-Z_]+)\)",
        read(os.path.join(ROOT, "source", "blender", "blenkernel", "intern", "idtype.cc"))))
    defined = set(re.findall(
        r"^#define (ID_[A-Z_]+) MAKE_ID2",
        read(os.path.join(ROOT, "source", "blender", "makesdna", "DNA_ID_enums.h")),
        flags=re.MULTILINE))
    if not registered or not defined:
        raise RuntimeError("could not read the ID type registry (idtype.cc / DNA_ID_enums.h)")
    return sorted(defined - registered - NON_ID_CODES)


def check_deregistered_allocation():
    codes = deregistered_id_codes()
    pattern = re.compile(
        r"\b(BKE_libblock_alloc(?:_in_lib)?|BKE_id_new(?:_nomain)?)\s*(?:<[^>]*>)?\s*\(([^;]*?)\)\s*;",
        flags=re.DOTALL)
    code_pattern = re.compile(r"\b(" + "|".join(codes) + r")\b")
    errors = []
    for path in walk("source", SOURCE_EXTENSIONS):
        text = strip_c_comments(read(path))
        for match in pattern.finditer(text):
            code = code_pattern.search(match.group(2))
            if code:
                errors.append("{}:{}: {} with deregistered {} (no IDTypeInfo, returns null; "
                              "use the Scar 10 manual allocation)".format(
                                  rel(path), line_of(text, match.start()), match.group(1),
                                  code.group(1)))
    return errors


def check_removed_rna_types():
    pattern = re.compile(r"\bbpy\.types\.(" + "|".join(REMOVED_RNA_TYPES) + r")\b")
    errors = []
    for subdir in PYTHON_DIRS:
        for path in walk(subdir, (".py",)):
            text = read(path)
            for match in pattern.finditer(text):
                errors.append("{}:{}: bpy.types.{} no longer exists (removed ID type)".format(
                    rel(path), line_of(text, match.start()), match.group(1)))
    return errors


def check_listbase_foreach():
    allowed = "source/blender/blenlib/intern/listbase.cc"
    pattern = re.compile(r"\bLISTBASE_FOREACH\w*\s*\(")
    errors = []
    for path in walk("source", SOURCE_EXTENSIONS):
        if rel(path) == allowed:
            continue
        text = strip_c_comments(read(path))
        for match in pattern.finditer(text):
            errors.append("{}:{}: LISTBASE_FOREACH is file-local to listbase.cc; "
                          "use an explicit for loop".format(rel(path), line_of(text, match.start())))
    return errors


CHECKS = (
    ("Python syntax", check_python_syntax),
    ("Deregistered ID allocation", check_deregistered_allocation),
    ("Removed RNA types", check_removed_rna_types),
    ("LISTBASE_FOREACH outside listbase.cc", check_listbase_foreach),
)


def main():
    failed = False
    for name, check in CHECKS:
        errors = check()
        print("{}: {}".format(name, "FAIL" if errors else "ok"))
        for error in errors:
            print("  " + error)
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
