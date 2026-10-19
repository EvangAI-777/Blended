---
name: runtime-audit
description: Run the Blended Phase 1 runtime audit loop — hand a finished CI build to the developer with its test list, then triage their hardware report (screenshots, blended_log.txt, crash log) into fixes, docs and the next build. Use when a Windows build finishes, when the developer reports a build's results or a crash, or when asked for a build's test list.
---

# Runtime audit loop

Phase 1 of 1.0.0: the developer runs each build on hardware and reports; Claude triages, fixes and
documents; the next build verifies. The reference for everything known so far is
[`docs/runtime-audit.md`](../../../docs/runtime-audit.md): the protocol, the open runtime checks,
Categories A–D and the build-by-build findings. Read it before triaging.

## 1. A build finished

1. Check the run (`mcp__github__actions_list`, `list_workflow_runs` for `build-windows.yml`):
   conclusion, the `Smoke test (headless)` step, and the commit it built. A red smoke test or build
   is triaged from the job logs before anything goes to the developer.
2. Give the developer a **short** test list in chat (the developer asked for simpler lists on
   2026-10-17, replacing the earlier "full list, nothing shortened" rule):
   - Setup in one compact block: the artifact link, unzip into a **new, empty** folder, `cmd` in
     the folder's address bar, `Blended.exe > blended_log.txt 2>&1`.
   - One line per test: what to do and what should happen. Cover every test not yet done inside
     Blended plus the new ones for this build; mark new tests "(new)". Group small related checks.
   - Name multi-window tests exactly: *two windows* is Window > New Window inside one running
     Blended; *second instance* is a second `Blended.exe`. They test different things
     (`docs/runtime-audit.md`, "Two windows and two instances are different tests").
   - End with one line each for the log search (`SyntaxError`, `Traceback`, `empty keymap`, and
     the strings the last fixes removed), renaming the log before a relaunch, and what to send
     back. Remind them the crash log keeps only the most recent crash.
3. Save the list to the scratchpad as `build<N>_test_list.md`, and post it verbatim as a comment
   (with the attribution footer) on each merged PR the build carries, the durable record of the
   build's testing. If a PR is open when a list is given, it also goes into that PR's Test Plan,
   "Build testing" (`.github/pull_request_template.md`).

## 2. A report came in

1. **Read all the evidence first** (Scar 6): every screenshot, `blended_log.txt`, the crash log.
   The screenshots and logs are the ground truth; if a report and the evidence seem to disagree,
   say exactly what the evidence shows and ask (Philosophy §11: believe what they see).
2. **Group the log by root cause**, not by line. One `SyntaxError` can produce hundreds of
   downstream errors (build 109).
3. **Trace each crash** from the backtrace into the source. Name the faulting read (`0x70`,
   `0x88`, …) and the call chain.
4. **Match each result to the test it reports.** A second instance is not a two-windows result
   (build 111). When a report could be either, ask which.
5. **Check `docs/runtime-audit.md`** before calling something new: Category A (expected),
   B (resolved), C (leaks), D (fixed crashes). A known item is reported as known.
6. **Look for the class, not just the instance.** The build 110 File > Open crash was every
   temporary-window close. Ask whether `tools/check_blended.py` could catch the class; if so, add
   the check in the same PR.

## 3. Fix and document

- Work on the session branch, checking first that it hasn't merged (CLAUDE.md, orphaned-commit
  trap). One commit per fix, pushed immediately (Scar 3). Local checks per the `steward` skill.
- Update `docs/runtime-audit.md`: mark the previous build's findings verified (with run ID and
  commit), add "Open — build N findings" with evidence, root cause and fix commit per finding, add
  Category D rows for crashes, and update the open runtime checks.
- Update the four mandatory docs (CLAUDE.md current-version line, CHANGELOG findings entry and
  contributor note, BLENDED.md status, `.github/README.md`), per the update matrix in `docs/codex-standard.md`
  (step 4) and `.claude/rules/docs.md` for placement.

## 4. Report in chat

Give the developer the full report: each finding with what they saw, the root cause and the fix
commit; what the build verified from the previous round; anything still unknown, as a direct
question (for example which tests they reached). Then follow the `steward` skill for the PR.
Merging and dispatching the next build happen only when the developer asks; after a dispatch,
schedule one check about 110 minutes out.
