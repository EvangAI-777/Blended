## Summary

<!-- What this PR changes and why, in a few sentences. Lead with the actual thing. -->

## What Changed

<!-- For code PRs: describe the functional changes and what they affect.
     For doc/content PRs: table of destinations, before/after counts, structural changes. -->

| Item | Details |
|------|---------|
|      |         |

## Why This Change

<!-- Problem being solved, architectural decision, or design rationale. -->

## Test Plan

<!-- How to verify this works: reproduction steps, test commands, what to look for. -->

## Substantive Changes

<!-- Anything beyond mechanical edits that needs review: logic changes, design decisions,
     broken links fixed, placeholders resolved, structural changes and their reasoning.
     If most of the diff is mechanical and a little is substantive, say so. -->

## Deliberately Preserved

<!-- Things that look like mistakes but aren't: unusual patterns, ASCII art, all caps,
     lowercase where normal English has caps, wording left verbatim. Say why so the
     next person doesn't "fix" them. Delete this section if nothing applies. -->

## Verification Checklist

### Code PRs
- [ ] Builds locally: `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -C build_files/cmake/config/blended_release.cmake && cmake --build build --target install`
- [ ] No new warnings introduced
- [ ] Follows coding conventions (SPDX header, `snake_case`, 2-space indent for C/C++)
- [ ] If touching branding/version files, checked `UPSTREAM_SYNC.md` conflict-prone list

### Doc/Content PRs
- [ ] All links (internal and external) verified
- [ ] Formatting consistent with repo style (em-dashes, bold labels, etc.)
- [ ] If new directory: nav entry in `_layouts/default.html`, breadcrumb if needed
- [ ] If new `.md`: Jekyll front matter present (`layout: default`, `title: "..."`)
- [ ] Related indices updated (`README.md`, `index.md`, etc.)

## Notes

<!-- What reviewers should know: corrections made during review, what's still open,
     false starts that were reworked, anything unexpected. An accurate record beats
     a clean one. -->
