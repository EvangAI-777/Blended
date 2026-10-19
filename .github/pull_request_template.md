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

<!-- Every kind of testing this PR needs, in one place. Fill in each part, or write "None" and why.
     Say plainly what has not been run yet. -->

### Automated

<!-- What ran and its result: `python3 tools/check_blended.py`, actionlint, syntax checks, and any
     smoke-test (`tests/python/blended_smoke_test.py`) changes, with the build they first run in. -->

### Build testing

<!-- The hardware tests this change needs on the next Windows build, written before merge in the
     same form as the chat list: the setup block, then one line per test. The build runs only
     after merge; when it is handed to Charles, the full chat list is posted verbatim as a
     comment on each merged PR it carries. "None" if the PR doesn't change the built program. -->

### Developer testing

<!-- What Charles should try hands-on beyond the build list: design or UX calls,
     screenshots to take, behavior to judge by eye. -->

### User testing

<!-- If applicable or necessary: what outside users should try, and what feedback to collect.
     "Not needed" otherwise. -->

## Substantive Changes

<!-- Anything beyond mechanical edits that needs review: logic changes, design decisions,
     broken links fixed, placeholders resolved, structural changes and their reasoning.
     If most of the diff is mechanical and a little is substantive, say so. -->

## Deliberately Preserved

<!-- Things that look like mistakes but aren't: unusual patterns, ASCII art, all caps,
     lowercase where normal English has caps, wording left verbatim. Say why so the
     next person doesn't "fix" them. Delete this section if nothing applies. -->

## Verification Checklist

### Every PR
- [ ] The project owner is named "Charles", not "the developer", wherever the person is meant; "developer testing" stays as a role (`docs/codex-standard.md` 1.4)
- [ ] Every claim in this description is checked against its source: what changed against the diff; what ran against its output; build numbers, verified findings and dates against the CHANGELOG and `docs/runtime-audit.md`; quotes against the actual words. Anything not verified says so (`docs/codex-standard.md` 1.4)

### Code PRs
- [ ] `python3 tools/check_blended.py` passes (also runs on the PR)
- [ ] Builds locally: `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -C build_files/cmake/config/blended_release.cmake && cmake --build build --target install`
- [ ] No new warnings introduced
- [ ] Follows coding conventions (SPDX header, `snake_case`, 2-space indent for C/C++)
- [ ] If touching branding/version files, checked the `docs/upstream-sync.md` conflict-prone list and divergence register

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

---

_Generated with [Claude Code](https://claude.ai/code)_
