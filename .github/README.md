<!--
Keep this document short & concise,
linking to external resources instead of including content in-line.
See 'release/text/readme.html' for the end user read-me.
-->

Blended
=======

**Blender, simplified.**

Blended is a fork of [Blender](https://www.blender.org) being chiseled from the foundation up (upstream Blender is the marble; the raw material is cut away, and the work is now sculpting inside) around one stated identity: **free 2D and 3D software tools, with an explicit focus on the craft of animation.**

Currently at 1.0.0-dev — 0.9.0 CI-complete (Windows x64, build 101, commit `c8e87078`). Third first-try on the project. 0.9.0 delivered: `.blend` import ✓ — OB_MBALL versioning pass 502.31, `BKE_main_clear` Scar 2 drain (PA/TE/CU/LS), `BKE_screen_blend_read_data` deletion, dropped-data manifest Text block. 1.0.x: foundation complete — Phase 1 runtime audit in progress (build 103/104/106 crashes fixed, build 107 empty crash log fixed (PR #242) and verified on hardware in build 108 — first real backtrace of the startup crash; root cause identified (`wm_add_default` workspace/screen bootstrap), launcher-bootstrap fix (PR #244) verified on hardware in build 109 — Blended reaches the launcher for the first time; build 109 findings fixed and verified on hardware in build 110; build 110 findings (File > Open crash, splash over the launcher, Cycles, launcher keymap) fixed and verified in build 111, the first session with no crash; build 111 findings (scene behind the launcher, launcher project-state cue, branding) fixed, build 112 CI-green, awaiting hardware verification (test list on PRs #250–#254; the open multi-window check is two windows in one Blended, not a second instance); Category D updated; every PR runs fast source checks, and Windows builds carry checksums and signed build provenance; contributor and AI-agent docs restructured: `AGENTS.md`, `docs/`). Phase 2 GitHub Pages launch pending Phase 1 completion. Release tag when both clear.

What Blended Is
---------------

Blender carries three stacked, unreconciled visions from three different eras. Blended resolves them:

- **Studio-tool discipline** — animation is the shaping principle; design decisions serve it.
- **Access mission** — openable by a first-time user. Free means free.
- **Full creative scope** — 2D animation, 3D animation, game assets, compositing, audio. The breadth is real. The feature-parity pathology is not.

One animation engine — depsgraph, keyframes, F-curves, timeline — powers every content type. See [`BLENDED.md`](../BLENDED.md) for the full design document, architecture, and pipeline specs.

What's Different
----------------

- **Branding** — "Blended X.Y.Z" in window titles, splash, and about dialog. Tagline: *Blender, simplified.*
- **Simplified data model** — 39 → ~19 ID types. Fossils, UI-state types, and upstream deprecations removed through the datablock audit (0.2.x–0.5.x). Remaining types have a permanent home in the data model, not just tolerance.
- **`.blended` project format** — magic bytes `"BLENDED"`, `.blended` extension, `FILE_TYPE_BLENDED` flag, platform integration (Windows registry, Linux MIME, macOS UTI). Import from `.blend` is one-way with a dropped-data manifest.
- **Pre-5.0 rig compatibility** — `blended_rig_compat.py` restores `action.fcurves` for pre-Blender-5.0 Rigify rigs.
- **Update notifications** — Background GitHub Releases check at startup with top-bar notification when an update is available.
- **CI** — Windows x64 portable builds via GitHub Actions, on manual dispatch and `v*` tags (tags also publish a GitHub Release). Each build is smoke-tested headless: startup, opening a `.blend`, saving and reopening a `.blended`.

Foundation Layers
-----------------

Six foundation layers — one minor version each, 1.0 when all six are honest.

| Version | Layer | Status |
|---------|-------|--------|
| 0.4.x | Datablock audit — 9 fossil removals (Bucket 5+6) | ✓ CI-complete (build 70) |
| 0.5.x | Datablock audit — Bucket 3 fold-downs complete; 39 → ~19 ID types | ✓ CI-complete (build 81) |
| 0.6.x | Evaluation model — depsgraph/draw/editor seam closure | ✓ CI-complete (build 82, commit `8f7dda22`) |
| 0.7.x | App lenses — launcher + all 28 mode lenses + full product identity | ✓ CI-complete (build 99, commit `2ddd1dd0`) |
| 0.8.x | File format — `.blended` magic, extension, platform integration | ✓ CI-complete (build 100, commit `99e20b96`) |
| 0.9.x | `.blend` import — seamless read, dropped-data manifest | ✓ CI-complete (build 101, commit `c8e87078`) |
| 1.0.0 | Foundation complete — Phase 1: runtime audit → Phase 2: GitHub Pages launch | In progress |

After 1.0, minor versions follow the post-1.0 roadmap in [`CHANGELOG.md`](../CHANGELOG.md). The first entry is user workspaces (your own saved variants of a mode).

Full version history in [`CHANGELOG.md`](../CHANGELOG.md).

Building from Source
--------------------

Blended builds the same way as Blender on all platforms:

- [Build Instructions](https://developer.blender.org/docs/handbook/building_blender/)

For CI / release builds:

```sh
cmake -S . -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -C build_files/cmake/config/blended_release.cmake
cmake --build build --target install
```

`blended_release.cmake` inherits the full Blender release config and turns off GPU binary pre-compilation. Everything else — EEVEE, Cycles, Cycles GPU via runtime compilation, USD, Alembic, OSL — ships.

Contributors
------------

Blended is developed and published by **CHJ 3 Productions LLC** (Indiana).

This repo is about work ethic and quality, not personal judgments: contributions and reviews are judged by what the work does, never by who did it (see [`BLENDED.md`](../BLENDED.md) §4, "Work, not judgment"). Every pull request's Test Plan covers automated checks, the hardware tests for the Windows build, developer testing and, where it applies, user testing (§4, "Test plans"). Every change follows one update process, [`docs/codex-standard.md`](../docs/codex-standard.md).

Built by CHJ 3 Productions LLC with two AI partners, across the whole project — every version, every phase, from the first fork commit to the release tag and after: [Claude](https://anthropic.com) (Anthropic) writes and fixes the code, the CI and the documentation, and triages each hardware build; [Codex](https://openai.com) (OpenAI) reviews every pull request before it merges. Two competitors from rival labs, collaborating on one project, with every catch on the record. The developer runs the project and makes the calls; it is collaboration, not control, and a working relationship rather than a procedure (`BLENDED.md` §4). Per-release detail in [`CHANGELOG.md`](../CHANGELOG.md).

Upstream Blender Resources
--------------------------

- [Blender Website](https://www.blender.org)
- [Reference Manual](https://docs.blender.org/manual/en/latest/index.html)
- [Developer Documentation](https://developer.blender.org/docs/)

License
-------

Blended, like Blender, is licensed under the GNU General Public License, Version 3.
Individual files may have a different but compatible license.

See [blender.org/about/license](https://www.blender.org/about/license) for details.
