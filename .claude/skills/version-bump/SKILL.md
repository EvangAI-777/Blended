---
name: version-bump
description: Bump the Blended version (BLENDED_VERSION_MAJOR/MINOR/PATCH) and update the four mandatory docs together. Use when a layer goes CI-green, a new dev cycle starts, a release tag is planned, or the developer asks to bump the version.
---

# Version bump

Moved verbatim from CLAUDE.md "Version Management" in PR #253.


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

2. **`CLAUDE.md`** — update the "Current version" line at the top:
   - For a new dev-cycle start: `Blended X.Y.0-dev — [layer description] in progress`
   - For a CI-complete milestone: `Blended X.Y.0-dev — X.(Y-1).0 base: CI-complete (Windows x64, build N, commit XXXXXXX)`

3. **`CHANGELOG.md`** — add a version bump note to the active *Unreleased* section (or the completed version section):
   - One line: which define changed, old value → new value, what triggered it, commit reference.
   - If CI just went green: also add a CI-complete note with build number and commit hash.

4. **`BLENDED.md`** — update the **Status** line at the top of the file to match.

5. **`.github/README.md`** — update the version/status sentence under the repo description.

**Quick checklist (run after any CI-green milestone or new dev-cycle start):**
```
□ BKE_blender_version.h — MINOR or PATCH bumped
□ CLAUDE.md — "Current version" line updated; roadmap table row updated
□ CHANGELOG.md — version bump note + CI-complete note added; grep all sections for stale version refs
□ BLENDED.md — Status line updated; grep all sections for stale version refs
□ .github/README.md — version/status sentence updated
□ All five changes in one commit, pushed to the working branch
```
**Note:** The four mandatory docs each contain multiple sections that reference version state — roadmap tables, mid-document planning blocks, subsection headers. A headline-only pass misses them. `grep -n "0\\.X" <file>` (replace X with the version) before staging each doc.
