# Contributing to Blended

Blended is a fork of Blender 5.2 being rebuilt from the foundation up, published by
CHJ 3 Productions LLC under GPL-2.0-or-later. Read [`BLENDED.md`](BLENDED.md) first: it is the
design authority and records the decisions that are locked.

## Work, not judgment

This repo is about work ethic and quality, not personal judgments
([`BLENDED.md`](BLENDED.md) §4). A contribution is judged by what it does: does it fix the thing,
does it hold on hardware, is the record accurate? It is never judged by who sent it. Reviews talk
about the code, not the person, and that applies to every reviewer, human or AI. A mistake gets
corrected and written down, not defended.

## Reporting a problem

Use the **Runtime report** issue form. It asks for the build, what you were doing, what you
expected, what happened, and the console and crash logs. To capture the console log, run
`Blended.exe > blended_log.txt 2>&1` from a Command Prompt in the Blended folder.

Some behavior changes are deliberate consequences of removing Blender features. Check the Known
Runtime Artifacts tables in [`docs/runtime-audit.md`](docs/runtime-audit.md) before reporting.

For security problems, see [`SECURITY.md`](SECURITY.md).

## Pull requests

- Branch from `main` and open the pull request against `main`. Fill in the template.
- The Test Plan covers every kind of testing the change needs: automated checks, build testing
  (the hardware tests for the next Windows build, written before merge), developer testing, and
  user testing where it applies. The full test list for each build is posted on the merged pull
  requests it carries.
- Subtraction is the method: when removing something, remove it completely and follow the compile
  errors ([`BLENDED.md`](BLENDED.md) §4 and its "Appendix — Development Philosophy").
- Follow the update process in [`docs/codex-standard.md`](docs/codex-standard.md): checks, tests,
  the docs each kind of change updates, consistency, commit and pull request.
- Run the fast checks before pushing. They also run on every pull request:

  ```
  python3 tools/check_blended.py
  ```

- Follow the coding conventions in [`CLAUDE.md`](CLAUDE.md): SPDX headers, `snake_case`,
  2-space C/C++ indentation, 99-column lines.
- A change that alters behavior updates the docs in the same pull request: `CLAUDE.md`,
  `CHANGELOG.md`, `BLENDED.md` and `.github/README.md`.
- Blended is built with Claude (Anthropic) as implementation partner and Codex (OpenAI) as reviewer, across the whole project (`BLENDED.md` §4). Every pull request is reviewed by Codex and by the maintainer. The full Windows build runs on
  manual dispatch and on release tags, and includes a headless smoke test of the packaged build.

## Building

See "Build Commands" in [`CLAUDE.md`](CLAUDE.md). The release configuration is
`build_files/cmake/config/blended_release.cmake`.
