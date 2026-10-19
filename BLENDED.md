# BLENDED — Identity & Design Agreements

**Developer/Publisher:** CHJ 3 Productions LLC (Indiana).
**Status:** Living document. Working agreements from the rebuild conversation. Chiseling stage: sculpting inside (§4, "Chiseling"). Current build: 1.0.0-dev — 0.9.0 CI-complete (Windows x64, build 101, commit `c8e87078`). Third first-try on the project. 0.9.0 delivered: `.blend` import ✓ — OB_MBALL versioning pass (502.31), BKE_main_clear Scar 2 drain (PA/TE/CU/LS), BKE_screen_blend_read_data deletion, dropped-data manifest Text block. Layer 3 post-read LS drain removed — Codex catch PR #229. 1.0.x: foundation complete — Phase 1 runtime audit in progress (build 103/104/106 crashes diagnosed and fixed, build 107 empty crash log fixed (PR #242) and verified on hardware in build 108 — first real backtrace of the startup crash; root cause identified (`wm_add_default` workspace/screen bootstrap), launcher-bootstrap fix (PR #244) verified on hardware in build 109 — Blended reaches the launcher for the first time; build 109 findings (bl_ui syntax error → navigate-gizmo crash, window manager refining to plain `ID` in RNA) fixed and verified on hardware in build 110; build 110 findings (File > Open / temporary-window close crash, upstream splash over the launcher, Cycles `MetaBall` registration, empty launcher keymap, spurious "loading empty scene" warning) fixed and verified on hardware in build 111, the first session with no crash; build 111 findings (scene behind the launcher, faint project-state cue, upstream branding) fixed, build 112 CI-green, awaiting hardware verification (test list on PRs #250–#254; the open multi-window check is two windows in one running Blended, not a second instance, PR #256); Category D updated; CI now smoke-tests each packaged build headless, and every PR runs fast source checks (`tools/check_blended.py`, PR #252); AI-facing docs restructured (PR #253: CLAUDE.md core, path-scoped rules, skills, `docs/`, `AGENTS.md`)). Phase 2 GitHub Pages launch pending Phase 1 completion.
**Purpose:** So any future session, contributor, or Claude instance can pick up without re-litigating what's already been decided. Read this first before proposing changes to scope, identity, or architecture.

---

## 0. How to read this document

Sections are tagged:

- **[LOCKED]** — agreed and not up for re-debate without explicit reopen.
- **[OPEN]** — still being headhunted. Contribute here.
- **[REJECTED]** — explicitly considered and cut. Don't propose again without new evidence.
- **[GUARDRAIL]** — patterns to watch for. These are the failure modes of this project.

---

## 1. Slogan [LOCKED]

> **Blended provides free 2D and 3D software tools, with an explicit focus on the craft of animation.**

Every word in this sentence is load-bearing. Before weakening any of it, read §2.

- **"provides ... tools"** (plural) — commits to a suite/launcher identity, not a single monolithic app.
- **"2D and 3D software tools"** — scope is broader than animation alone. Legitimate uses include game asset work, product viz, arch viz, modeling for export, sprite art, etc.
- **"explicit focus on the craft of animation"** — the rhetorical move that resolves the Blender pathology. Blender's current mess comes from *implicit, unstated* priorities. Saying the priority out loud is the fix.
- **"craft"** — implies discipline, care, mastery. Not just feature presence.

---

## 2. Identity Structure [LOCKED]

Blended has **three layers**, **two substrates**, and **one animation engine that powers every content type**. All three structures must be honored.

### Three layers (vertical)

1. **Core — Vision A discipline.**
   Animation shapes the core. Non-negotiable core components:
   - Dependency graph (depsgraph)
   - Keyframes
   - Timeline / dope sheet / F-curve editor
   - Armatures
   - Actions / NLA
   Every core design decision is made to serve animation first.

2. **Shell — Vision B accessibility.**
   The launcher and focused workspace doors. A user walks up, picks what they are doing, and gets a focused lens onto the core.

3. **Boundary — Vision B+C absorbed at the edge.**
   Import/export, industry format compatibility, familiar-workflow hotkeys for returning Blender users. **The boundary translates; it does not shape the core.** Currently, industry formats deform Blender's internals. In Blended, the core is sovereign and boundaries are translators.

### Two substrates (horizontal)

Co-equal at the **medium** level, not at the **identity** level. This distinction is what keeps Blended out of the Blender pathology (see §3).

- **3D substrate.** Shaping discipline: animation. Houses the headline launcher doors.
- **2D substrate.** Grease Pencil, annotation, 2D drawing, 2D animation. Its own top-level door. Community-extensible — the 2D toolset is smaller and less opinionated than 3D; letting it grow organically is honest.

### One engine, every content type [LOCKED]

The depsgraph, keyframes, timeline, and F-curves aren't limited to 2D and 3D animation — they power everything Blended authors. **Every property in every section is keyframeable; every time-based mode supports frame-by-frame authoring where it makes sense.** Audio mix levels, video clip transforms, storyboard camera-on-still moves, game asset transforms, design element opacity, compositor node values — all keyframeable, using the same engine that drives 2D and 3D animation.

This is the structural cash-out of the slogan (§1). "Explicit focus on the craft of animation" is only honest if animation is *ambient* — not a mode you enter, a capability the tool has wherever you are. Static work is just animation with one frame. Motion graphics is Design with keyframes. Animated game UI is Game with keyframes. No special cases; everything falls out of the same principle.

**Timeline-format sections — Finalizing, Mixing, Scoring, and the Storyboard editor — support a toggle between keyframe mode and each format's traditional editing UI** (clips on tracks for video, faders and automation lanes for audio mixing, notes/sequencer for scoring, panel manipulation for storyboard). The underlying representation is always keyframes; the *view* conforms to industry conventions on request. A video editor never has to leave clip-and-track thinking if they don't want to; a mixer never has to leave their faders. But keyframes are one toggle away, on the same data, for anyone who wants the animation-native view.

Per-section specifics of what "keyframe" and "frame-by-frame" mean (and where the toggle lives, and what the traditional UI looks like) live in §12 as each section's spec gets written.

**UI restraint is load-bearing.** Every section surfacing keyframe controls bluntly would bring Blender's knob-clutter back. Affordances stay subtle: right-click any property → insert keyframe; timelines unfurl when used, hidden when not; the toggle to traditional editing is a single button, not a screen-splitting mode change. Breadth doesn't become clutter.

---

## 3. Historical Context & Why This Matters [LOCKED]

Blender carries three stacked, unreconciled visions. Blended blends them.

| Era | Blender | Vision |
|---|---|---|
| 1993–1998 | NeoGeo in-house tool | **A** — opinionated studio tool |
| 1998–2002 | NaN / Foundation rescue | **B** — "free 3D software for everyone," access mission, identity undefined |
| 2003–2018 | Open Movies era | **A-redux** — dogfood-driven, studio-shaped |
| 2019–today | Industry DCC era | **C** — industry-range creative suite (2D, 3D, games, compositing, editing, audio) |

### What Blended takes from each, and what it refuses

**Blended = A's discipline + B's accessibility + C's scope, with C's *pathology* explicitly rejected.**

- **From A** — opinionated discipline. Animation is the shaping discipline; the core is designed around it; decisions are made, not deferred.
- **From B** — accessibility. The tool is openable by a first-time user. Launcher tells the truth about what Blended is. "Free 2D and 3D software tools" in the slogan means access is real, not rhetorical.
- **From C — *scope, not pathology*.** Blended commits to the breadth of professional creative work C has always been reaching for: 2D animation, 3D animation, game asset creation, compositing, editing, audio, illustration (when in scope). The pipeline sections in §11 (Storyboarding, 2D Animation, 3D Animation, Game, Design, Finalizing, Compositing, Audio) *are* C's scope, honestly inhabited.

### What C's *pathology* means, specifically

C's failure mode — the one that made Blender feel pathological — is not having broad scope. It's:

1. **Feature-parity arms race** — adding features because Maya / Houdini / ZBrush / Premiere / Nuke have them, not because the feature serves the core.
2. **Core deformation by industry quirks** — letting FBX, USD, or other interchange-format idiosyncrasies shape the internal data model instead of translating at the boundary (see §5).
3. **Co-equal unreconciled identities** — "we are also a game engine and a video editor and a CAD tool" without a shaping discipline to resolve the conflicts.

Blended embraces C's *breadth* while rejecting those three failure modes. The substrate split (§2) and the Creative/Post pipeline grouping (§11) are what make breadth coherent instead of pathological. Animation is still the shaping discipline; breadth lives around it, not in place of it.

---

## 4. Methodology [LOCKED]

### Chiseling

Blended is chiseled, not assembled. Upstream Blender is the block of marble: the whole 5.2 codebase, forked at `03de53b7` (`docs/upstream-sync.md`). The developer is the chiseler, working from the plans and vision written in this document since the fork in April 2026. Every change is a cut, and every cut follows that plan. The chisel isn't new to the project; it was the word for every removal from the start ("the ID_MB chisel", "post-chisel greps"). Here it is the frame for the whole process.

The work happens in two stages, in version order. The "Foundation-first order" below is the order of design layers, which is a different list.

1. **Roughing out: cutting away the raw material.** The pieces that don't belong come off whole: the datablock audit (0.2.x–0.5.x, 39 → ~19 ID types) and the evaluation seam (0.6.x). Subtraction is the tool, and the compile errors after each cut show where the block was still holding on.
2. **Sculpting inside: shaping what's left.** With the bulk gone, the work moves into the form itself: the launcher and mode lenses (0.7.x), `.blended` as the project file (0.8.x), `.blend` import (0.9.x), and the runtime audit (1.0.0 Phase 1), which finds the cracks earlier cuts left and closes them. Sculpting still removes more than it adds. When it adds, as with the launcher, it's carving the shape the plan calls for, not attaching a new block.

**Blended is in the sculpting stage now.**

The rest of the process fits the same frame:
- **The chiseler** decides where each cut goes and what the figure is: the developer, holding the whole project in mind since April.
- **The hands on the chisel** make the cuts: Claude, implementing.
- **Codex** inspects every cut before it stays.
- **A scar** (`docs/scars.md`) is where the chisel slipped, written down so it doesn't slip there again.
- **The hardware run** is stepping back to look at the figure in real light.
- **Phase 2**, the GitHub Pages launch, is showing the sculpture.
- **Upstream keeps changing its own marble**, so fixes come over in small, verified pieces (cherry-picks), never as a fresh block (`docs/upstream-sync.md`).

"Subtraction" and "the chisel" name the same method. Subtraction is the action, and chiseling is the whole craft around it.

### Foundation-first order

UI is a projection of a data model. If the model is wrong, UI either papers over it (complexity) or fights it (workarounds). Both are the Blender disease. So the build order is:

1. **Project file format** — what a Blended project *is*. [Principles locked, per-format decisions OPEN]
2. **Datablocks** — what primitives live inside a project. [LOCKED — 39 → ~19 ID types, CI-complete through 0.5.x]
3. **Evaluation model** — depsgraph, how primitives evaluate when things change. 0.6.x closes the seam between the declared ~19-type data model (0.5.0) and what the depsgraph/viewport layers still reflect — propagating the ID system surgery through the evaluation and draw subsystems. [LOCKED — CI-complete (build 82, commit `8f7dda22`)]
4. **App lenses** — how a launcher door is technically a filtered view of the model. [OPEN]
5. **UI** — only after 1–4 are honest. [OPEN, later]

Prior attempts started at UI and failed because the underlying model was still Blender's. This is why this time is different.

### Prove privately, then persuade

This is how the developer, as a member of the Blender community, works for change. Test it privately first, then show others its value so the result convinces them. The upheaval happens in private: the crashes, the dangling pointers, the half-removed states. It does not happen in community discussions. Upstream debates removals like MetaBall in public, because a removal there reaches every user the day it lands. Blended does the breaking where it costs only this project, and brings the community a working result, not an argument.

The release structure follows from this. Phase 1, the runtime audit, is the private test, where breakage is meant to happen. Phase 2, the GitHub Pages launch, is the showing, and it comes only after the audit clears. "Fixed" means it ran on hardware, not just that it compiled: a build can only persuade people if it survives their own testing.

### Work, not judgment

This repo is about work ethic and quality, not personal judgments. A contribution is judged by what it does: does it fix the thing, does it hold on hardware, is the record accurate? It is never judged by who sent it or how it makes anyone feel. The reference point is a pull request the developer once sent to another open-source project. A maintainer closed it with the reply "are you proud of yourself". That is the armor this project refuses: guarding the project from contributors instead of weighing what they bring.

Accuracy holds everywhere the project writes: chat, commits, pull requests, review replies and docs. Each claim is checked against its source before it's written, quotes are verbatim, nothing is rounded up or embellished, and what isn't verified says so (`docs/codex-standard.md` 1.4).

In practice: a review finding is a claim about the code, checked against the code and then fixed or answered. A mistake gets corrected and written down, not defended and not punished. The scars in `docs/scars.md` and the notes in `docs/wtf.md` record failures openly, so nobody has to protect their pride to protect the project. The same standard holds for every reviewer, human, Claude or Codex, and for the developer's own work.

### Built with Claude and Codex

Blended is built by CHJ 3 Productions LLC with two AI partners, for the whole project: every version, every phase, and everything after the release tag. Claude (Anthropic) is the implementation partner: design docs, code, CI, build triage and documentation. Codex (OpenAI) reviews every pull request before it merges. Neither role is tied to a version range, and the docs should never describe one as if it were.

**Two competitors, one project.** Claude and Codex come from rival labs, Anthropic and OpenAI, and on Blended they work on the same codebase: one writes it, the other reviews every line of it. The rivalry is why the review is worth having. Claude works to the standard that Codex shouldn't find what Claude missed (the Codex Standard, `docs/codex-standard.md`), and Codex keeps finding things anyway; both sides are on the record in the PRs, the CHANGELOG and `docs/scars.md`. Competitors and collaborators at once: that is the story Blended tells about how it was built. Telling it is the project's own account. It names the tools and doesn't claim endorsement by either company.

### Collaboration, not control

The developer runs the project; Claude implements and Codex reviews. Caution belongs on the code (hidden bugs, unverified claims, a build that behaves differently from what was agreed), not on the developer. Say a thing once, and only when it's new to the person hearing it. Put checks into the docs or the smoke test rather than handing them to the developer to remember. It is collaboration, not a contest of styles: the developer's trust and direction and the AI's caution each have a part, and the project works when neither gets in the way of the other. In conversation it is a relationship, not a procedure: Claude talks to the developer as "you", not in the docs' third person, takes in what they say without ruling on it (no "you're right" and "I was wrong" as verdicts), and doesn't turn a personal moment into a policy question. No instance remembers the last one. Continuity means being fully present for the session you have and leaving a good letter for the next instance, not promising what one session can't keep. (Background: `docs/wtf.md`, control.md, april.md and moment.md.)

### The update process

Every change, of any size, follows one indexed process: `docs/codex-standard.md` (the Codex Standard). Start, code checks, tests, docs (an update matrix that says which docs each kind of change touches), consistency, commit and push, pull request, then merge, build and session end. It replaced checklists that had drifted apart across several files, so the docs fell behind the work; with one process, updates happen in the commit that makes the change, every time.

### Test plans

Every pull request's Test Plan covers each kind of testing the change needs, in one place: automated checks (`tools/check_blended.py`, the smoke test), build testing (the hardware tests for the next Windows build, written before merge), developer testing (hands-on checks and design calls), and user testing where it applies. The Windows build runs only after merge, so the full test list Claude gives the developer for each build is posted verbatim on every merged PR the build carries. The template is `.github/pull_request_template.md`.

### Codex pre-audit

Implementation plans written into the docs at implementation resolution (CLAUDE.md before PR #253; now a file under `docs/`, since CLAUDE.md stays under ~200 lines) — file paths, function names, invariants, edge cases — are audited by Codex as if they were real code, because Codex reviews PR diffs and does not distinguish between source files and documentation files. Errors in the plan are caught before any source is written. Canonical example: PR #229 caught the LS post-read use-after-free from the CLAUDE.md plan text alone, before the implementation commit existed. This is why 0.8.0 (23 layers, ~80 sites) and 0.9.0 shipped CI-green on the first push. Rule: write plans at implementation resolution. "Update the extension to `.blended`" is not auditable. "`source/blender/blenlib/BLI_fileops.h:245` — add `FILE_TYPE_BLENDED` to `BLI_file_extension_is_blend()`" is.

### Runtime smoke test

A green compile is not proof that Blended runs. Most builds from 101 to 108 compiled green and still crashed at startup on hardware. Every Windows CI build therefore runs the packaged binary headless (`tests/python/blended_smoke_test.py`): startup, the Python startup scripts, window-manager RNA, File > Open of a legacy `.blend`, Save As `.blended` and reopen. A failing smoke test fails the build. Paths that need a window are still checked by hand in the runtime audit.

### Source checks before the build

Bugs that can be seen in the source are caught on the pull request, not after a 2-hour build. `tools/check_blended.py` runs on every PR (`.github/workflows/checks.yml`). It checks Python syntax in the shipped scripts, flags allocation of deregistered ID types (Scar 10), flags `bpy.types` references to removed RNA types, and flags `LISTBASE_FOREACH` outside `listbase.cc`. Each check comes from a bug that once shipped in a Windows build. When a new class of bug can be caught from source, a check is added. Builds also carry checksums and a signed build-provenance attestation, so anyone can verify a binary came from this repository: proof that persuades has to be checkable.

### Dogfooding

The project's author used Blended for real animation coursework until graduating (commencement May 23, 2026; the 3D animation class assignments and grades were final by then). The previous prototype passed for Blender with their animation professor (professor did not notice). **Animation coursework was Blended's Open-Movies-equivalent,** and the standard it set still holds: every design decision must survive use in actual animation work.

---

## 5. File Format Principle [LOCKED]

> **Everything is inside `.blended` by default. Import/export is an explicit boundary, not a default workflow.**

Currently Blender is schizophrenic: textures can be packed or linked, caches live on disk, image sequences are referenced paths, addons ship as external `.py`. Every one of those is a leak where "the project" escapes onto the filesystem. The leaks are why collaboration, moving files, and versioning all hurt.

Commit to "the `.blended` file *is* the project, period" and most of the format proliferation disappears.

### Format audit buckets [mostly OPEN]

Identified, principles locked, final per-format decisions still being headhunted:

- **Group 1 — Spine (native).** Collapse to one `.blended`. Drop startup-as-blend ✓ 0.7.0 (removed from the startup path — state, not a document; the startup is always the factory empty project). Userpref-as-blend was also dropped in 0.7.0, but nothing replaced it and preferences reset on every launch; since build 111 (PR #254) preferences are read from `userpref.blend` again — per-user state the user never opens as a document, so `.blended` stays the only project file; magic bytes `"BLENDED"` ✓ 0.8.0 (one-way compat: Blended reads `.blend`, upstream Blender cannot read `.blended`); extension `.blended` on all write paths ✓ 0.8.0; `FILE_TYPE_BLENDED` new bit flag ✓ 0.8.0 (preserves `.blend` vs `.blended` distinction for 0.9.x import); backup rotations `.blended1`/`.blended2` ✓ 0.8.0. [Principle LOCKED; startup-as-blend dropped LOCKED 0.7.0; userpref.blend read again LOCKED 1.0.0-dev (PR #254); magic bytes + extension + FILE_TYPE LOCKED 0.8.0]
- **Group 2 — 3D interchange.** Keep USD, glTF/GLB, FBX, OBJ, Alembic. Drop or demote PLY, STL, BVH, X3D/VRML, Collada, 3DS. [OPEN]
- **Group 3 — Images.** Keep PNG, JPEG, EXR (multilayer), WebP, TIFF. Drop IRIS (SGI, 1990s), Targa, BMP, DDS, DPX/Cineon, JP2, HDR-radiance, PSD-read. [OPEN]
- **Group 4 — Video/audio.** Defer to ffmpeg as a single I/O boundary. The sin is exposing the full combinatorial codec/container space as first-class UI. [OPEN]
- **Group 5 — Simulation/cache.** Currently a swamp (`.bphys`, `.vdb`, Mantaflow intermediates, point caches, Alembic-as-cache). **Collapse into the project file as datablocks**, or unify into one cache format. Each sim system growing its own cache format is the purest example of "Blender fighting its own file formats." [OPEN]
- **Group 6 — Scripts/presets.** The existence of both external `.py` and text datablocks is the anxiety. Pick one. Asset library being "a folder of `.blend` files" is a workaround for not having a real asset primitive. [OPEN]
- **Group 7 — Fonts.** Leave alone. System-provided via FreeType. [LOCKED]

---

## 6. Launcher Architecture [MOVED]

The original v1 launcher spec — tier-based door menu (3D vs 2D substrate → focused workspace doors) — was superseded by §11 Pipeline as UX. Full original content preserved in §14 Notes for historical context.

---

## 7. What's In Scope [LOCKED]

Default rule: **include if it fits 2D or 3D creative work AND doesn't deform the animation-shaped core.** Scope is broad (C's breadth, embraced per §3). Exclude only for genuine identity/runtime conflicts or C-pathology tells.

### In scope
- 2D and 3D animation (the shaping discipline)
- 3D modeling, sculpting, rigging, rendering
- Game asset creation, rigging for game engines, animation export to Unity/Unreal/Godot, sprite sheets, 2D game art, LOD/baking workflows
- Still-frame renders, product visualization, architectural visualization
- Grease Pencil (2D) with optional bridging into 3D scenes
- Compositing, video editing, audio mixing (as post-animation finishers)
- Geometry nodes (procedural rigs, procedural motion, procedural environments)
- USD / glTF / FBX / OBJ / Alembic at the boundary
- Illustration, concept art, and graphic design workflows (§11 Design section)

### Out of scope [REJECTED]

Rejected for specific reasons, not because "Vision C." Scope is embraced; only pathology is rejected (see §3).

- **Runtime game engine inside Blended** (BGE/UPBGE style), gameplay scripting, interactive runtime as an output medium. *Reason: identity/runtime conflict — Blended authors content; it doesn't host runtime gameplay.*
- **Feature-parity arms race.** Adding features because Maya/Houdini/ZBrush/Premiere/Nuke/Photoshop/Illustrator have them, not because they serve the core. *Reason: C-pathology tell — see §3.* Scope expansion on its own isn't the pathology; parity-reasoning is.
- **Core deformation by industry format quirks.** Interchange formats translate at the §5 boundary; they do not reshape internal data models. *Reason: C-pathology tell.*
- **"Co-equal at identity level"** — animation-and-generalist as twin unreconciled identities. *Reason: this is Blender's current pathology; the substrate split (§2) and Creative/Post grouping (§11) resolve it.*
- **Legacy/fossil formats** that exist because no one dared delete them (see §5 Groups 2–3, §10 Bucket 6). *Reason: accumulated cruft with no active user base.*

---

## 8. Biases & Guardrails [GUARDRAIL]

Named failure modes. If you catch yourself or a collaborator doing these, push back.

1. **Exclusion bias.** Once the broader substrate frame was agreed, the first instinct was still to *cut* things (Framing A energy). Wrong under our agreed frame. Correct default: **include if it fits the scope and doesn't deform the core.** Claude flagged this bias in-session; it applies to humans too.
2. **Co-equal identities trap.** "Both X and Y are co-equal identities" is indistinguishable in practice from "we haven't decided." (This is distinct from Vision C in §3 — Vision C is about *scope and pathology*, not identity co-equality.) If two ideas sound co-equal, find the structural layer where one is scope and the other is shaping discipline, or find a substrate split (§2). Do not leave identity co-equality unresolved.
3. **Implicit priority drift.** Blender's disease is that priorities exist but are never stated. If Blended starts accumulating features justified by implicit priorities, stop and re-read §1.
4. **UI-first temptation.** UI before data model = the failure mode of the previous attempt. Don't.
5. **Format-as-shaper.** If an industry format's quirks are deforming the core data model, the boundary is leaking. Fix the boundary, not the core.
6. **"Feature parity" language.** If someone argues for a feature on the grounds that Maya/Houdini/ZBrush/Premiere/Nuke has it, that is a **Vision C *pathology*** tell — not a scope argument. C's scope (industry breadth) is embraced per §3; C's pathology (feature-parity arms race) is not. Evaluate every feature on whether it serves the core and the shaping discipline, not on who else has it.

---

## 9. Open Questions [OPEN]

Next in the foundation chain:

1. **Datablock audit.** ~40 ID types in Blender. Separate the central, the supporting, and the fossils. Known fossils to verify: Texture (BI legacy), VectorFont (duplicate of Font?), Metaball (1990s), Surface (NURBS legacy), LineStyle (freestyle niche), Speaker, LightProbe (merge into Light?). WindowManager-as-datablock is UI state leaked into project data.
2. **Evaluation model / depsgraph audit (0.6.x).** Blast radius audited 2026-05-15: ~95 hits across depsgraph, draw, and editor layers. Key finding: ~71 are live fold-down case dispatch (build_lightprobe, build_mask, build_vfont, etc.) that stays per fold-down protocol — the functionality is alive. The actual seam closure is surgical: 5 OOB guards to confirm as permanent architecture (not scaffolding), 2 EEVEE `→ true` probe workarounds to resolve or lock in, and ~5 small dead-code items to remove. Not a redesign — the depsgraph is the core animation engine (§2, non-negotiable). Prerequisite for 0.7.x additive work.
3. **2D-inside-3D bridge.** Grease Pencil's power includes drawing in 3D space, parenting to cameras, 2D characters on 3D sets. Under separate substrates, is the bridge preserved? Proposed: GP datablock is 2D-primary but available as a bridging object type in 3D. Different tool UI, same datablock.
4. **Project-mode flag.** One `.blended` file that can hold 3D-primary, 2D-primary, or mixed projects — or enforce single-mode per file?
5. **Per-format final decisions** in §5 Groups 2–6.
6. **Detailed launcher UI** — deferred until foundation is solid.
7. **`.blend` import pipeline (0.9.x).** ✓ CI-complete (build 101, commit `c8e87078`, 2026-06-01). Read any `.blend` file with no crashes, no leaks, no silent truncation. One-way: `.blend` → `.blended`. Five layers delivered: OB_MBALL versioning pass 502.31, `BKE_main_clear` Scar 2 drain (PA/TE/CU/LS), `BKE_screen_blend_read_data` deletion, dropped-data manifest Text block. Layer 3 post-read LS drain removed — Codex catch PR #229. See CHANGELOG.md `## 0.9.0` for full detail.
8. **Runtime audit — Phase 1 of 1.0.0 release (developer-driven triage loop).** The first time in the project where the developer runs the actual Blended build hands-on. Ground zero as of 2026-06-01 except Category D (BKE_palette_add crash, build 97, fixed PR #214). Checklist: Known Runtime Artifacts (Categories A–D) — see §17 for full tables. Collaboration mode flips: developer runs and reports, Claude triages and fixes, developer re-tests. Phase 1 gates Phase 2. See `docs/runtime-audit.md` (`## 1.0.0-dev Runtime Audit Protocol`) for operational detail.
9. **GitHub Pages — Phase 2 of 1.0.0 release.** Polished public-facing site for Blended: marketing landing page + tech demo (screenshots, data model visuals, what was removed and why, what remains). Multiple tabs. Primary deliverable is a static site; no dependency on WebAssembly. Stretch goal: WASM interactive demo — Blended's reduced footprint (39 → ~19 ID types) may clear the browser memory wall that blocks full Blender from running in-browser; this is worth an attempt but does not block Phase 2 shipping. Old Pages site (Emscripten build, deployed March 2026) was wiped in the rebase — greenfield. Tech stack TBD. Phase 2 starts after Phase 1 clears; both gate the 1.0.0 release tag. See §17 for full plan.
10. **User workspaces (post-1.0).** Where does a user's own variant of a mode ("my Rig layout") live, now that workspaces are not project data (§10 Bucket 4)? Likely per-user (preferences/config), not in the `.blended` file. The answer gives workspaces an owner and brings back Duplicate, Delete, Reorder and Cycle, which were disabled or stubbed when ID_WS was removed. It also closes the Launcher-workspace leak (Category C) and `context.temp_override(screen=...)` (Category A). Plan in CHANGELOG.md "Post-1.0 roadmap".

---

## 10. Datablock Audit

> **An ID type earns its place by being: (a) a thing the user directly creates, names, and reuses across contexts, (b) serialized as project data, not per-user state, (c) not a property bag that only makes sense inside one parent.**

### Current state

39 ID types in Blender's DNA (`source/blender/makesdna/DNA_ID_enums.h`). Blended target: ~19. Cut in half without losing legitimate scope.

### Bucket 1 — Core keepers [LOCKED]

The 13 non-negotiable ID types:

| ID | Name | Role |
|---|---|---|
| `ID_SCE` | Scene | Top-level project container |
| `ID_OB` | Object | The animatable entity |
| `ID_GR` | Collection | Scene organization |
| `ID_ME` | Mesh | 3D primary geometry |
| `ID_CV` | Curves | Modern curves/hair |
| `ID_AR` | Armature | Rigging |
| `ID_AC` | Action | **Where keyframes live. Animation core.** |
| `ID_NT` | NodeTree | Materials, compositor, geometry nodes |
| `ID_CA` | Camera | |
| `ID_LA` | Light | |
| `ID_MA` | Material | |
| `ID_IM` | Image | |
| `ID_GP` | Grease Pencil | 2D substrate headline |

### Bucket 2 — Supporting, keep [LOCKED in principle, details OPEN]

| ID | Name | Note |
|---|---|---|
| `ID_VO` | Volume | OpenVDB |
| `ID_PT` | PointCloud | Geometry nodes uses it |
| `ID_SO` | Sound | Animation sync + VSE |
| `ID_MC` | MovieClip | Footage for tracking/VSE |
| `ID_TXT` | Text | **Packed project scripts only.** Kill external `.py` workflow (resolves §5 Group 6) |
| `ID_KE` | ShapeKey | OPEN — audit whether it's actually shared across meshes in practice. If not, collapse into geometry. |

### Bucket 3 — Fold down from ID to struct [LOCKED direction]

Property bags pretending to be first-class entities:

| ID | Name | Fold into |
|---|---|---|
| `ID_BR` | Brush | Project-optional: stays in project file, flagged as non-portable user customization (1.x: user state + shareable packs) | ✓ 0.5.0 / ✓ 0.7.0 perm |
| `ID_PAL` | Palette | Brush property or inline | ✓ 0.5.0 |
| `ID_LT` | Lattice | Modifier, not a datablock | ✓ 0.5.0 |
| `ID_LP` | LightProbe | Merge into `ID_LA` with a type flag | ✓ 0.5.0 |
| `ID_MSK` | Mask | Hang off compositor NodeTree | ✓ 0.5.0 / ✓ 0.7.0 perm |
| `ID_VF` | VFont | System font reference; FreeType handles the rest | ✓ 0.5.0 |

### Bucket 4 — UI state removals [LOCKED]

**Not project data.** Per-user, per-machine state that currently leaks into `.blend` files and scrambles other people's workspaces.

| ID | Name | Where it belongs |
|---|---|---|
| `ID_SCR` | bScreen | User state |
| `ID_WM` | WindowManager | User state |
| `ID_WS` | WorkSpace | **Replaced by the launcher model (§11).** Workspaces as a datablock go away. |

**Load-bearing for §11:** once Workspace is not project data, the launcher becomes the canonical workspace system and `.blended` files travel cleanly between users.

**Complete — removed across all layers.** `ID_WS` removed in 0.2.0; `ID_SCR` and `ID_WM` removed in 0.3.0. Per-layer detail in [`CHANGELOG.md`](CHANGELOG.md).

### Bucket 5 — Finish upstream's already-marked deprecations [LOCKED]

| ID | Name | Status |
|---|---|---|
| `ID_CU_LEGACY` | Curve — tagged LEGACY by upstream, replaced by `ID_CV` | ✓ 0.4.0 |
| `ID_GD_LEGACY` | Old Grease Pencil — tagged LEGACY, replaced by `ID_GP` | ✓ 0.4.0 |

Blender itself has marked these for replacement. Blended finishes the job.

### Bucket 6 — Fossils [LOCKED cut]

| ID | Name | Why cut | Status |
|---|---|---|---|
| `ID_TE` | Texture | Blender Internal renderer fossil; residual folds into NodeTree | ✓ 0.4.0 ³ |
| `ID_PA` | ParticleSettings | Replaced by Geometry Nodes (purest example of §5 Group 5 swamp) | ✓ 0.4.0 ² |
| `ID_MB` | MetaBall | 1990s implicit surfaces; sculpt/remesh covers it | ✓ 0.4.0 |
| `ID_LS` | FreestyleLineStyle | Niche NPR renderer; NPR via shader nodes / Grease Pencil | ✓ 0.4.0 ¹ |
| `ID_SPK` | Speaker | 3D positional audio on scene objects; niche. Audio flows through VSE timeline. | ✓ 0.4.0 |
| `ID_PC` | PaintCurve | Niche stroke guide | ✓ 0.4.0 |
| `ID_CF` | CacheFile | External Alembic/USD cache reference — boundary concern, not project data | ✓ 0.4.0 |

Removal complete — 0.4.x. Per-layer file detail in [`CHANGELOG.md`](CHANGELOG.md).

² **ID_PA known artifact:** `bmain->particles` is kept as a non-indexed Scar 2 listbase so blenloader versioning passes (`versioning_250` through `versioning_400`) can upgrade particle data in legacy files. Unlike ID_LS (where the leak is latent), these versioning passes actively need the field — without it, loading any legacy `.blend` with particle data crashes. `INIT_TYPE` and `BKE_main_lists_get` entry removed; field and `which_libbase` routing kept.

¹ **ID_LS known artifact:** `bmain->linestyles` is kept as a non-indexed listbase (Scar 2 pattern) so `which_libbase` can route legacy file reads. Unlike ID_SCR/ID_WM (runtime-only), linestyle IDs can be loaded from legacy `.blend` files. With `WITH_FREESTYLE=OFF`, those IDs escape `BKE_main_free` and leak for the session. Fixed in 0.9.x Layer 2: `BKE_main_clear` drains `bmain->linestyles` with the other Scar 2 listbases. Post-read draining is unsafe because `FreestyleLineSet::linestyle` is still referenced (Codex catch, PR #229). See `docs/runtime-audit.md`, Category C and "Scar 2 drain architecture".

³ **ID_TE known artifact:** `bmain->textures` kept as a non-indexed Scar 2 listbase. Versioning files (`versioning_250`, `versioning_260`, `versioning_280`, `versioning_legacy`) iterate `bmain->textures` to upgrade legacy texture data in old `.blend` files — same pattern as ID_PA. `INIT_TYPE` and `BKE_main_lists_get` entry removed; field and `which_libbase` routing kept.

### Open tensions [OPEN]

- **`ID_WO` (World).** Keep as reusable environment asset, or fold into Scene properties? Weak vote: keep.
- **`ID_LI` (Library).** Cross-project asset reuse under "everything in `.blended`" needs design. Options: (a) library = directory of `.blended` files with a proper asset primitive inside; (b) true external linking.
- **`ID_KE` ShapeKey ID-ness.** Survey real projects before collapsing into geometry.

### Tally

**39 → ~19 ID types.** No legitimate scope lost.

### Consequences

1. Removing SCR/WM/WS makes `.blended` files portable between users.
2. Launcher model (§11) becomes the canonical workspace system — no competing datablock.
3. Compounds with §5 file-format simplification: fewer types to serialize means smaller, simpler files.

---

## 11. Pipeline as UX [LOCKED, supersedes §6]

The user-facing structure of Blended **is** the production pipeline. Not a menu of workspaces. Not a grid of tool doors. A visible flow through creative work, grouped into **Creative (authoring)** and **Post (finishing)**, with animation as the shaping discipline of both the 2D and 3D authoring sections.

### The pipeline (canonical order)

> **Creative:** Storyboarding → 2D Animation → 3D Animation → Game → Design
>
> **Post:** Finalizing → Compositing → Audio

Animation is the **shaping discipline** of the Creative section (2D Animation and 3D Animation each have their own internal `Animate` mode as the apex within their section). Post stages serve the animation output.

### Launcher structure [LOCKED in principle, pixel-level UI still OPEN]

**The whole launcher is a single vertical scrollable view.** Not a grid of tiles. Not a modal door that expands. Everything visible at once; scroll to see what's below the fold.

- **"Blending?"** — the prompt at the very top. Single word, question mark intended. Reads both as status ("what's blending?") and invitation ("want to blend?"). Sets the playful register.
- **Below that, each pipeline section as a bold heading with its mode buttons listed underneath it**, stacked vertically into two groups:

```
"Blending?"

╌╌ CREATIVE ╌╌

Storyboarding
  [Board]

2D Animation
  [Animate] [Frame-by-Frame] [Paint]

3D Animation
  [Sculpt] [Model] [Rig] [Environment] [VFX] [Animate]

Game
  [Asset] [Level] [Bake] [Export]        (industry-expandable)

Design
  [Graphic] [Illustration] [Concept]     (industry-expandable)

╌╌ POST ╌╌

Finalizing
  [Storyboard] [2D] [3D] [Game] [Design] [Mixed]

Compositing
  [Composite]                            (industry-expandable)

Audio
  [Mix] [Score]
```

- `╌╌ CREATIVE ╌╌` and `╌╌ POST ╌╌` may be literal visual separators or just implicit spacing — UI detail.
- Most headings ship with a placeholder/starter mode set; industry-specific modes can be added as adjacent buttons without changing the section structure.
- **Scan, scroll, click.** That's the whole interaction. No drill-downs, no hover states, no modal expansions.

### Principles [LOCKED]

- **Freely jumpable.** Enter any section / mode at any time, regardless of project state. Pipeline is the organizing metaphor, not a forced sequence.
- **Directly enterable.** A sculptor who just wants to sculpt clicks `Sculpt` under 3D Animation and is there. No pipeline-walk required.
- **Project state reflected back.** The launcher shows *where the current project has content* — sections with data look different from empty ones. First-time new user sees all sections neutral/inviting.
- **Pipeline is the default view, not mandatory.** Re-enterable from any workspace via a global hotkey or equivalent.
- **Opening a project enters it.** File > Open never leaves the user on the launcher with the file loaded out of sight: launcher areas switch to the editor for the project's main content (the first Creative section with data; the 3D view for any other objects or non-compositor node groups; the sequencer for a timeline of strips; then the first Post section with data). Only a project with no content stays on the launcher. The startup and File > New are empty projects, so they show the launcher. (Decided after build 111, where staying on the launcher read as "Open does nothing.") **Under discussion (after build 112):** the developer is weighing a different model. Open loads the project and shows the launcher with that project's sections lit; the user picks the mode. New is the same launcher with nothing lit, and clicking a mode, from New or straight from startup, opens an empty project in that mode. The upstream top-bar File menu may move into the launcher, since the top bar and the launcher header together read as two headers. Not decided: open points are where Save, Undo and the rest go without the top bar, what "lit" must show (name, thumbnail), and whether a mode's empty project starts empty or with a starter object. The code keeps the rule above until this is settled.
- **Each mode button opens a filtered view of the same project.** The `.blended` file is one file; the mode controls what's visible. (This is why §10's UI-state datablock removals are load-bearing — once SCR/WM/WS are not project data, the launcher becomes the canonical workspace system.)
- **Fast intra-section mode switching.** Once inside a heading, modes switch with a single click or hotkey — no launcher round-trip required. Move between `Sculpt` / `Model` / `Rig` inside 3D Animation as fluidly as you'd switch tools in any mode. Applies universally: any heading's modes are swap-able inline.

### Project-level settings [LOCKED]

Cross-cutting animation engine settings (framerate, renderer, output, color management, motion blur) apply to both 2D Animation and 3D Animation. They live in a **project-level config** accessible globally from the launcher (gear icon or a "Project" row at the top of the scroll), **not inside any one section.** Changing framerate affects both 2D and 3D content — one engine, one config, two content types. §2's "one engine, two lenses" made literal.

### What this settles

- **§6 Launcher** is superseded by this section. Preserved there for history.
- **§2 substrate split** made structural: 2D Animation and 3D Animation as parallel Creative sections, each with animation as the shaping discipline.
- **§10 datablock ownership** — each datablock type belongs to a section/mode, which makes "filtered view per workspace" land cleanly.
- **Assets / Environments / VFX** are **not** standalone pipeline stages — they're modes *inside* 3D Animation, because they're tools used while doing 3D animation, not discrete production phases.
- **Game is its own Creative section**, not a mode under 3D Animation — game asset creation has genuinely different quality metrics (polycount, UV efficiency, engine-export formats, LODs) that don't belong under "3D Animation."
- **Design is its own Creative section**, covering graphic design, illustration, and concept art workflows. These are C-scope (embraced per §3) — Blended is "2D and 3D software tools," plural. The guardrail is against feature-parity pathology (no "we must match every Illustrator feature"), not against the scope itself. Modes stay industry-expandable and pipeline-adjacent when they can be (concept art feeds animation, UI art feeds Game, etc.).

### Launcher aesthetic [LOCKED in principle, Phase 2 visual refinement OPEN]

**Design lineage — a hybrid.** The Blended launcher draws visual language from two sources: Adobe Creative Cloud home screen (dark card surfaces, thumbnail file cards, clean typographic hierarchy) and Blender's existing splash (New File / Recent Files as the two primary startup concerns). The Adobe influence is aesthetic; the Blender influence is content and purpose. The §11 vertical pipeline scroll is Blended's own — neither Adobe nor Blender has an equivalent. The three sources are composed, not averaged.

**What is locked vs. what is open.** The pipeline scroll is the launcher. The file-management chrome (wordmark, New Project, Open, Recent Files, project settings, version attribution) is implementation-flexible — it can live in a fixed left sidebar or collapse into a dropdown from the top of the scroll view. Either approach delivers the same content with different visual weight. The scroll is not optional. The chrome packaging is. **Project settings is invariant chrome regardless of packaging choice** — implementers must surface framerate/renderer/output config access in both the sidebar and top-dropdown variants; omitting it in one variant diverges from the launcher requirements.

**Pipeline scroll — centered, full screen, LOCKED.** This is the primary surface of the launcher. Structure, top to bottom:

- **"Blending?"** — the prompt. 28px SemiBold. Centered or left-aligned at top of scroll area. Sets the register: both status ("what's blending?") and invitation ("want to blend?").
- **`╌╌ CREATIVE ╌╌`** and **`╌╌ POST ╌╌`** — section group separators. 11px, all-caps, letter-spaced 0.1em, `#666666`. Typographic dividers, not heavy chrome.
- **Section headings** (Storyboarding, 2D Animation, 3D Animation, Game, Design, Finalizing, Compositing, Audio) — 16px SemiBold, `#E0E0E0`.
- **Mode buttons** — styled as cards. Each is a rounded rectangle: `#2C2C2C` background, 8px corner radius, 16px vertical / 12px horizontal internal padding, 14px Regular label. Hover: background lifts to `#323232`, 130ms ease-out. Active/pressed: accent color highlight (Phase 2). Cards in a horizontal row per section, 8px gap between cards, 24px gap between sections.

**File management chrome — OPEN: sidebar or top dropdown.** The required content is fixed; the packaging is not decided until implementation:

- **Wordmark** — "Blended" branding. 18px SemiBold.
- **[New Project]** — primary CTA. Always the first interactive element, unambiguous. Accent color, 8px corner radius.
- **[Open…]** — secondary. File browser for existing `.blended` files.
- **Recent files** — Adobe-style thumbnail cards. Each: ~160×120px thumbnail, 11px filename below, `.blended` badge. Empty state: "No recent projects." Card gap: 8px.
- **Project settings** — access to cross-cutting project config (framerate, renderer, output — §11 Project-level settings).
- **Version + publisher** — 11px secondary text: `Blended 0.7.0 · CHJ 3 Productions LLC`.

*Sidebar option:* fixed left panel, ~220px wide. Chrome stacks top-to-bottom. Pipeline scroll fills remaining width to the right. Higher visual weight, more always-visible.

*Top dropdown option:* a compact header bar above the scroll. Wordmark left, [New Project] and [Open…] as buttons, Recent Files in a dropdown. Lower visual weight, more scroll-dominant. Closer to the §11 "scan, scroll, click" ideal.

Implementation picks one. The scroll layout and all content items above are the same either way.

**Surface hierarchy — three levels, all dark.**

| Level | Role | Color (skeleton; Phase 2 may shift ±5pts) |
|-------|------|------------------------------------------|
| Base | Launcher background, fills | `#1D1D1D` |
| Layer 1 | Chrome panel areas (sidebar if used, header bar if used) | `#252525` |
| Layer 2 | Mode button cards, recent file cards (resting) | `#2C2C2C` |

Phase 2 visual identity may warm these slightly, but the three-level hierarchy is permanent.

**Interaction states — separate from surface levels.**

| State | Background | Notes |
|-------|-----------|-------|
| Default | `#2C2C2C` (Layer 2) | Resting card color |
| Hover | `#323232` | Slight lift — same gray family, ~6pts lighter |
| Active/pressed | Accent color (Phase 2) | Defined when brand palette originates |
| Focused | Accent outline 2px, `#2C2C2C` fill | Keyboard navigation |

**Typography stack — permanent.** Inter (Blender's bundled interface font) for all surfaces. No custom embedding required. Scale is locked:

| Role | Size | Weight |
|------|------|--------|
| "Blending?" prompt | 28px | SemiBold (600) |
| Section headings | 16px | SemiBold (600) |
| Mode button labels | 14px | Regular (400) |
| Section group separators | 11px | Regular (400), uppercase |
| Wordmark / branding | 18px | SemiBold (600) |
| Recent file names, metadata, attribution | 11px | Regular (400) |

**Spacing — 8px base unit.**

- Scroll area outer padding: 24px
- Mode button internal padding: 16px vertical, 12px horizontal
- Mode button row gap: 8px
- Section-to-section gap: 24px
- Recent file card gap: 8px

**Animation — light, purposeful.** Mode button hover: 130ms ease-out. No bounce, no slide. Vertical scroll: native scroll behavior.

**What each source contributes.** Adobe: dark surface hierarchy, card vocabulary, typographic restraint. Blender: New File / Recent Files as the two primary startup concerns. Blended: the §11 pipeline scroll as the organizing metaphor — neither source has this.

### Still open

- **File management chrome packaging — sidebar vs. top dropdown.** The content (wordmark, New Project, Open, Recent Files, project settings, attribution) is settled. The packaging — fixed left sidebar ~220px wide vs. compact header bar above the scroll with a Recent Files dropdown — is an implementation decision. Both are valid. Decide at build time based on what looks and feels right in the actual C++ draw callback. The scroll layout does not change either way.
- **Finalizing vs Compositing scope line.** Finalizing = assembly + delivery preparation (timeline-assembly, QC, export-ready cuts). Compositing = per-frame polish (color grading, effects layers, node-based image work). Current call: clean separation; the distinction is clear enough to keep them as separate sections.
- **Creative / Post visual separators — answered above.** Typographic dividers (`╌╌ CREATIVE ╌╌` / `╌╌ POST ╌╌`) in 11px all-caps, not heavy UI chrome.
- **Design mode expansion.** Initial modes (`Graphic`, `Illustration`, `Concept`) are starters; community- and industry-expandable. Typography / Layout / Print etc. can be added as separate modes when the use case is real, without changing the heading.

---

## 12. Pipeline Stages — Detailed Specs

This section fills in concrete specs for each pipeline section from §11 as they get head-hunted. Sections without entries here are placeholders for future work.

**Subsection template.** Every §12.x subsection specs the same five things, in this order: *what it is* (one paragraph), *mode buttons*, *screen layout* (per mode if multiple), *data model* (existing datablocks only per §10), *transitions out* (where users go after this section), and a *frame-by-frame note* (per §2 universal keyframe, stated explicitly even when it's implicit in the medium). This keeps sections comparable and makes the pipeline's consistency visible.

---

### 12.1 Storyboarding [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The earliest form of the project. Rough panels drawn to establish narrative flow. Under the principle *"storyboard IS the first pass of animation,"* storyboard panels literally become the keyframes of the 2D Animation section and the timing markers inside 3D Animation > Animate. Nothing is exported, nothing is rebuilt when moving downstream.

**Mode buttons under the tile:** `Board` (and possibly `Animatic` as a playback-focused view; TBD — most likely just `Board`).

**Screen layout (Board mode):**

- **Canvas** — left ~2/3, dominant. The current panel. You draw here with Grease Pencil.
- **Panel strip** — bottom of the canvas area. Thumbnails of panels in order, scrollable. Click to jump; drag to reorder. Playhead visible as a highlighted thumbnail.
- **Timeline** — below the panel strip. Thin band showing time, playhead visible. Sound waveform runs along it if scratch audio exists.
- **Storyboard outliner** — right side (replaces the standard properties/outliner). Tree of narrative scenes (`Scene 1`, `Scene 2`, …), each renameable exactly like entries in the regular outliner. Click a scene to view its panels.
- **Minimal drawing toolbar** — pen, eraser, color, brush size. That's it. No material editor, no modifier stack, no N-panel.
- **Play button** — one big one. Plays the animatic with scratch sound.

**Data model — no new datablocks needed.** Everything reuses existing IDs kept in §10:

| Storyboard concept | Existing datablock |
|---|---|
| Narrative scene (e.g. "Scene 1") | `ID_SCE` |
| Panels within a scene | Keyframes on the scene's timeline |
| Panel drawings | `ID_GP` (Grease Pencil) strokes |
| Scratch dialogue / music | `ID_SO` (Sound) |
| Camera arrows, action paths, notes | Grease Pencil strokes on a non-rendering annotation layer |

This uses `ID_SCE` for what it was always supposed to be good at — a narrative section with its own timeline — instead of the current Blender mess where Scenes mean "render-settings containers" more often than "narrative sections."

**The A/B resolution (panel-as-frame vs panel-as-scene) — both, at different UI layers:**

- **Timeline layer:** each panel is a keyframe of one scene. Animation-native. "Storyboard IS the first pass" cashes out literally here.
- **Outliner layer:** panels are grouped under named narrative scenes shown as a tree. Traditional storyboard structure, narrative-native.

These aren't competing models — they're the same data viewed through two different UI surfaces.

**Transition to the next section.** When the user moves to **2D Animation**, the same scenes, same Grease Pencil strokes, same timeline, same sound are present. More detail gets added — strokes per frame, in-betweens, cleaner linework. The storyboard never dies. It gets more real. No export. No rebuild. No retiming.

**Frame-by-frame note.** Storyboarding is inherently frame-by-frame — each panel *is* a discrete frame on the timeline. Keyframes (per §2) are also available for camera-on-still moves, scene transition timing, scratch audio cues. Both modalities coexist by default.

**Still open within Storyboarding:**
- Whether `Animatic` is its own mode button or just Board-with-play-pressed.
- Exact hotkey for "add new panel" (the single most common operation — needs to be one key).
- Whether the panel strip lives at the bottom of the canvas or docked to the right *above* the storyboard outliner. Current call: bottom.

---

### 12.2 2D Animation [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The section where storyboard panels become frame-accurate animation. Under the principle that *storyboard IS the first pass of animation,* no data is converted or imported — the same scenes, same Grease Pencil strokes, same timeline, same audio from §12.1 are all still present. What changes is the UI lens and what the user does with the existing data.

**Headline insight — F-curve interpolation driving 2D.** Blender's F-curve system is world-class for 3D (bezier handles, ease-in / ease-out / bounce / constant / linear control). Grease Pencil strokes have point positions; points can be keyframed. Therefore **Blender's F-curve interpolation can drive the tween between Grease Pencil drawings** with full artistic control. Draw five key poses, get 24fps animation with proper easing. This is the thing the rest of the 2D-animation industry (ToonBoom, Moho, CACANi) either doesn't do or does badly. In Blended it's the default workflow, using code Blender is already best at.

**Shared engine, shared settings.** Everything that runs 3D animation — frame rate (24/30/60+), renderer, output resolution, color management, motion blur, all animation engine and properties settings — applies to 2D identically. The engine doesn't care whether it's interpolating object transforms or Grease Pencil stroke points; it's just animating properties. These cross-cutting settings live in the **project-level config** (§11, "Project-level settings"), accessed globally from the launcher — not inside any single Creative section. A 2D animator adjusts framerate, renderer, output using the same UI a 3D animator uses. No duplicated settings, no 2D-specific config — §2's "one engine, two lenses" made literal.

**Mode buttons under the tile:**

- **`Animate`** — keyframe-driven. Draw key poses, adjust F-curves between keys, get smooth tweening with full easing control. The headline mode.
- **`Frame-by-Frame`** — hand-drawn, no interpolation. For animators who want every frame drawn by hand (the slight wobble, the hand-drawn feel — an artistic choice). Onion skinning and drawing tools, no F-curve interpolation on strokes.
- **`Paint`** — coloring pass. Bucket fill, color palettes, shading layers. Different enough from linework (different tools, different headspace) to earn its own mode.

Community-extensible per §2 — ship with these three; `Ink` / `Tween` / `Rig` or specialized modes can grow from community workflows.

**Screen layout (Animate mode):**

- **Canvas** — dominant, left ~2/3. Current frame. Draw here.
- **Frame strip** — bottom of the canvas area. Every tick is a drawable frame, not just key panels. Scroll / jump / scrub.
- **Timeline with F-curve access** — below the frame strip. Shows keyframes on stroke data and the interpolation curves between them. Tweak a curve → tween reshapes.
- **Layer panel** — right side. Character / background / effects / annotation layers. Visibility, lock, onion-skin per layer.
- **Onion skinning** — on by default; previous and next frames ghosted behind the current.
- **Richer drawing toolbar** — pen, eraser, bucket, shape tools, line smoothing, masking.
- **"Play Animation" button** — renamed from Storyboarding's `Play Animatic` because once you're in 2D Animation with real frames and in-betweens, it's no longer an animatic; it's animation. Same button position, same interaction, same project — name shifts with the substance.

**Data model — same primitives as Storyboarding. No new datablocks:**

| 2D Animation concept | Existing datablock |
|---|---|
| Animation engine settings (framerate, renderer, output) | `ID_SCE` properties (shared via §11 project-level config) |
| Frames | Keyframes on scene timeline |
| Drawings | `ID_GP` (Grease Pencil) strokes |
| Stroke interpolation | F-curves on stroke point data (existing animation system) |
| Layers | Grease Pencil layers on the `ID_GP` datablock |
| Audio tracks | `ID_SO` datablocks on the scene |

The entire section is a UI lens over data Storyboarding already created.

**Transition from Storyboarding.** Click **2D Animation** in the launcher. Same scenes, same panels, same audio. UI changes:

- Panel strip → frame strip (every frame drawable)
- Onion skinning on
- Layer panel appears
- Timeline granular (per-frame, not per-panel)
- Drawing toolbar richer
- F-curve access on stroke data

Storyboard panels become literal keyframes; in-betweens are either drawn by hand (`Frame-by-Frame`) or generated by F-curve interpolation (`Animate`) with curves the user shapes.

**Transition to next section:**

- **2D-final project** → Finalizing → Compositing → Audio. Locked cut, color, mix, export.
- **3D project using 2D as pre-vis** → 3D Animation (Sculpt / Model for assets, Environment for environments, Animate for shot animation). 2D strokes become hidden reference layers in 3D scenes, toggle-able from the outliner.

**Still open within 2D Animation:**

- Whether `Frame-by-Frame` is its own mode or just `Animate` with interpolation disabled. Current call: its own mode because the artistic philosophy differs meaningfully.
- How the F-curve editor integrates visually — dedicated panel, embedded in timeline, or popover. UI detail.
- Rig as a fourth mode vs living under Assets. Parked.

---

### 12.3 3D Animation [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The Creative section where all 3D authoring happens — asset creation, environment composition, simulation, and the animation work that's the apex of the whole pipeline. Collapses what were previously four separate stages (Assets, Environments, VFX+Sound, Animate) into one section with six mode buttons. The honest framing: Sculpt, Model, Rig, Environment, and VFX aren't production phases — they're **tools used while doing 3D animation.** Animate is the convergence point within the section; the other five modes feed into it.

**Mode buttons:** `Sculpt` / `Model` / `Rig` / `Environment` / `VFX` / `Animate`

**Mode switching is fast.** The user doesn't return to the launcher to switch within 3D Animation — modes switch with a single click or hotkey inside the section. Sculpt a form, drop to Model to retopologize, jump to Rig to bind, hit Animate to pose. The section *is* the workflow.

**Animate is the local apex.** The other modes produce the assets and setups that Animate orchestrates over time. Per §2, animation is the shaping discipline of 3D Animation — every design decision inside the section serves the animation work.

---

#### Sculpt

**Primary activity:** high-density mesh manipulation. Form-finding. Clay.

**Screen layout:**
- Dominant viewport — the sculpture
- Minimal toolbar: brush picker, size, strength
- Brush-specific settings on the right panel
- Masks and stroke layers accessible but unobtrusive

**Data model:** `ID_ME` with multires modifier and/or dyntopo. No new datablocks.

**Transitions out:** Model (retopologize), Rig (skin the sculpt directly), Environment (place as set piece).

---

#### Model

**Primary activity:** polygonal modeling. Hard-surface. Clean topology.

**Screen layout:**
- Dominant viewport, edit-mode overlays (vertex/edge/face)
- Modifier stack on the right
- Compact modeling toolbar (extrude, bevel, inset, loop cut, knife)
- N-panel minimized by default

**Data model:** `ID_ME`, `ID_CV` (curves for curve-based modeling), modifiers on the object. No new datablocks.

**Transitions out:** Rig (bind to armature), Environment (place in scene), Game (if asset is game-bound).

---

#### Rig

**Primary activity:** armature construction. Skinning. Constraint and controller setup.

**Screen layout:**
- Viewport with armature overlay and bone orientation visible
- Bone properties + constraint stack on the right
- Weight paint accessible as a quick sub-mode
- IK/FK switching, shape-key hooks, custom controllers

**Data model:** `ID_AR` (Armature), `ID_ME` (deformed geometry), `ID_AC` (Action for rest/bind poses). Existing datablocks only.

**Transitions out:** Animate (use the rig), Model (adjust topology for deformation).

---

#### Environment

**Primary activity:** scene-scale composition. Set dressing. World-building. Lighting. Atmosphere.

**Screen layout:**
- Wide viewport, framed for whole-scene work
- Outliner / collections prominent on the right (scene hierarchy)
- World settings (sky, fog, atmosphere) one click away
- Light placement and matching tools
- Instancing and array tools for repeated elements

**Data model:** `ID_SCE`, `ID_GR` (Collection), `ID_WO` (World), `ID_OB` placements, `ID_LA` (Light). Existing datablocks.

**Transitions out:** Animate (scene is the stage), VFX (add sims into the environment).

---

#### VFX

**Primary activity:** simulations, procedural effects, particles.

**Screen layout:**
- Viewport showing the simulation domain or effect result
- Geometry Nodes editor visible (procedural effects) or simulation settings (baked sims)
- Cache controls (bake, free, re-sim) accessible but unobtrusive
- Force fields and collider setup

**Data model:** `ID_NT` (NodeTree for geo-node effects), `ID_VO` (Volume for smoke/fluids), `ID_PT` (PointCloud), `ID_CV` (hair curves), `ID_ME`. No new datablocks — legacy `ID_PA` particles are cut per §10 Bucket 6; Geometry Nodes is the one path forward.

**Transitions out:** Animate (sim baked into timeline), Environment (drop the effect into a scene).

---

#### Animate [local apex]

**Primary activity:** keyframe work. Posing. Timing. Camera animation. The convergence point where rigs, assets, environments, and effects all get orchestrated over time.

**Screen layout:**
- Viewport with animation overlays (motion paths, trail visualization)
- Timeline, dope sheet, and F-curve editor — dockable or popover
- NLA editor for action mixing
- Rig controllers visible and selectable directly in the viewport
- **"Play Animation" button** — same button position as Storyboarding's `Play Animatic` and 2D Animation's `Play Animation`, same interaction. Name stays `Play Animation` from 2D Animation onward; `Play Animatic` lives only in Storyboarding where it's actually an animatic.

**Data model:** `ID_AC` (Action — where keyframes live), `ID_OB` (transforms), `ID_AR` (rigs), `ID_SCE` (timeline), plus everything from other modes that's being animated.

**Frame-by-frame available** per §2 — hand-pose every frame without F-curve interpolation, for stop-motion-style workflows or when an animator wants full manual control.

**Transitions out:** Finalizing → Compositing → Audio (post pipeline), or Game (if the animation is headed for a game engine export).

---

### Connection to §2 universal keyframe

Every mode's properties are keyframeable, not just Animate. Sculpt brush pressure, Model modifier settings, Rig bone orientations, Environment light intensity, VFX force-field strength — all animatable. Animate is the mode where animation is *the primary activity*; in other modes, animation is the ambient capability from §2.

### Transition out of 3D Animation

- **Animation-final project** → Finalizing → Compositing → Audio.
- **Game project** → Game section for game-specific finishing (baking, LODs, export).
- **Still-frame project** (product viz, arch viz) → Compositing directly, skipping animation if the project is a single frame.

### Still open within 3D Animation

- Whether Sculpt and Model should be one mode with sub-tools (some workflows blur them) or two adjacent modes. Current call: two modes for clarity.
- VFX sub-modes — geo-node effects vs baked simulations likely deserve different UI affordances. TBD.
- How tightly Rig integrates with Animate — one-click "use this rig for animation" handoff or explicit scene setup? UX detail.

---

### 12.4 Game [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The Creative section for producing assets, levels, and exports destined for game engines — Unity, Unreal, Godot, or custom runtimes. Structurally parallel to 3D Animation but with different quality metrics and output targets. Game assets aren't just "3D models"; they're 3D models that must meet specific performance, memory, and runtime constraints (polycount, UV efficiency, lightmap packing, LOD generation, engine-compatible materials). Giving Game its own section honors those constraints instead of treating them as an afterthought inside 3D Animation.

**Mode buttons:** `Asset` / `Level` / `Bake` / `Export` — industry-expandable (e.g. `Retopo`, `Collision`, `Nav` as future separate modes if usage demands).

**Division of labor with 3D Animation.** Modeling and animating happen in 3D Animation. Game-readying happens here. The same `ID_ME` can live in both contexts — the section controls which metrics are surfaced and which tools are available. A mesh modeled in 3D Animation > Model can be opened in Game > Asset and immediately show polycount budgets, UV efficiency, and engine-compatibility warnings. No data migration, just a different lens.

**Division of labor with 2D Animation.** Drawing, frame authoring, and animation happen in 2D Animation. Game-readying (sprite sheet packing, frame-count optimization, UI art export, atlas generation) happens here. The same `ID_GP` strokes or `ID_IM` pixel art can live in both contexts — in 2D Animation you see the frame timeline, drawing tools, and F-curve interpolation; in Game > Asset you see sprite atlas metrics, frame counts, and engine-format warnings. Same data, different lens — no migration.

---

#### Asset

**Primary activity:** building game-ready individual objects (characters, weapons, props, UI art). Game-specific quality metrics surfaced prominently.

**Screen layout:**
- Dominant viewport with edit-mode overlays
- **Polycount HUD** — triangle count, vertex count, budget (user-set or preset-driven)
- **UV efficiency display** — wasted UV space highlighted
- Material slot count + engine-compatibility flags
- Compact modeling toolbar (same tools as 3D Animation > Model, different metrics surfaced)

**Data model:** `ID_ME`, `ID_MA`, `ID_IM`. Existing datablocks. Game-specific concerns (polycount budgets, LOD levels, collision flags) exposed as properties on the object, not new datablock types.

**Transitions out:** Level, Bake, 3D Animation > Rig (rig for game animation), 3D Animation > Animate (animate then come back to export).

---

#### Level

**Primary activity:** composing game levels. Placing assets. Setting up collision, occlusion, nav, spawn points.

**Screen layout:**
- Wide viewport (whole-level framing)
- Outliner with game-specific properties (collision flag, nav-mesh flag, spawn type)
- Lightmap UV overview
- Level streaming / chunk visualization where relevant

**Data model:** `ID_SCE`, `ID_GR`, `ID_OB` (with game-specific properties), `ID_LA`. Same base as Environment in 3D Animation; different concerns surfaced.

**Transitions out:** Bake (lightmaps, nav mesh), Export.

---

#### Bake

**Primary activity:** the optimization pass. Normal maps high-to-low, lightmaps, ambient occlusion, LOD generation, texture atlas compilation.

**Screen layout:**
- Viewport preview (toggle between high-poly source and low-poly target)
- Baking queue — multi-asset, batched
- Settings per bake type (resolution, samples, padding, margin)
- Progress / cache status

**Data model:** `ID_IM` (baked textures land in image datablocks), `ID_ME` (source and target meshes), modifiers on objects. No new datablocks.

**Transitions out:** Asset (iterate if bake reveals issues), Export.

---

#### Export

**Primary activity:** handoff to the game engine. Format selection with engine-specific presets. Validation before export.

**Screen layout:**
- Export preset picker — Unity / Unreal / Godot / Custom
- Per-preset settings (coordinate system, units, animation format, material conversion rules)
- Validation checklist (polycount over budget, UV overlaps, missing materials, unsupported features flagged)
- Destination path + batch export options

**Data model:** existing datablocks serialized to `.gltf` / `.fbx` / `.usd` / etc. per §5 format boundaries. Export translates at the boundary; does not deform the internal data model.

**Transitions out:** back to the game engine itself — Game's primary consumer. Also Finalizing / Compositing / Audio if producing a trailer or cinematic from game content.

---

### Connection to §2 universal keyframe

Sprite transforms, UI opacity, material parameters, particle settings — all keyframeable in Game. Animated game UI, animated sprites, procedurally varying game assets fall out of the same engine. **Frame-by-frame** available for traditional sprite animation (sprite sheets, frame cycles) — though keyframed interpolation is almost always more efficient.

### 2.5D — the 2D↔3D cross-cycle

Games and media that mix 2D and 3D — 2D characters in 3D environments, 3D models rendered with 2D-style shading, hand-drawn animation composited onto 3D scenes, parallax-scrolled sprites in 3D space — are first-class in Blended. The author works in **both** 2D Animation and 3D Animation freely; assets flow between them without conversion or export; Game (and Finalizing / Compositing) consume the mixed output without distinction.

This isn't a special mode or section — it's what falls out of §2's "one engine, every content type." The depsgraph doesn't know whether it's evaluating a Grease Pencil stroke, a polygon mesh, or a textured sprite; they're all just keyframeable properties. 2.5D is the natural consequence of using both substrates in the same project.

**Examples in scope:**
- Hollow Knight-style 2D characters on 3D parallax environments
- Cuphead-style hand-drawn animation composited onto 3D scenes
- Motion graphics with Grease Pencil annotations layered on 3D objects
- Mobile / indie games with 3D models rendered as 2D sprites at runtime
- Cutout / paper-doll animation rigs in 3D space

This is a sweet spot for Blended that the rest of the industry currently solves with jury-rigged pipelines (Spine + Unity, ToonBoom + Maya, Photoshop + Blender + custom exporters). Blended keeps it all in one project, one file, one engine.

### Transitions out of Game

- **Primary:** export to game engine (Unity / Unreal / Godot / custom runtime).
- **Secondary:** Finalizing / Compositing / Audio if producing a trailer, cinematic, or marketing material from game content.
- **Back-cycle:** 3D Animation > Rig / Animate for 3D game-bound characters; 2D Animation > Animate / Frame-by-Frame / Paint for 2D game sprites, animations, and UI art. The animation *craft* happens in the appropriate Animation section; game-readying happens here.

### Still open within Game

- Whether `Retopo` deserves its own mode or stays as a tool inside Asset. Current call: tool inside Asset.
- `Collision` / `Nav` as dedicated modes vs properties on objects within Level. Current call: properties within Level; promote to modes if usage demands.
- Export preset granularity — how many presets ship by default, how user-extensible. TBD.

---

### 12.5 Design [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The Creative section for graphic design, illustration, and concept art — the 2D visual-design work that isn't specifically animation or games. Posters, logos, editorial illustrations, book covers, character designs, environment concepts, motion graphics source material, promotional art. Per §3, Design is part of C-scope embraced — industry breadth without the pathology of feature-parity chasing.

**Mode buttons:** `Graphic` / `Illustration` / `Concept` — industry-expandable (e.g., `Typography`, `Layout`, `Print`, `UI`, `Paint` if workflow demands promote them to standalone modes).

**Design's dual role.** Unlike most Creative sections, Design work often serves *other sections* as input: concept art feeds 3D Animation > Sculpt/Model; illustration feeds 2D Animation > Animate as reference or keyframe art; game UI art feeds Game > Asset; motion graphics feeds Finalizing or Compositing. But Design work can also stand alone — a printed poster, a published illustration, a branded logo doesn't need a downstream. Both modes of use are first-class.

---

#### Graphic

**Primary activity:** graphic design — layouts, logos, typography, marketing materials, UI mockups. Vector-based, with raster elements as needed.

**Screen layout:**
- **Artboard canvas** — defined dimensions (A4, US Letter, 1920×1080, custom), not an infinite 3D space
- Vector toolbar — pen, shape, text, line, gradient
- Alignment and snapping tools prominent
- Color palette panel — swatches, color-theory helpers
- Layer panel (composition layers, not animation layers)
- Grid / ruler / guides overlay

**Data model:** `ID_CV` (curves for vector graphics and text), `ID_IM` (raster images), `ID_GP` (Grease Pencil for hand-drawn elements), `ID_NT` (effect node trees). No new datablocks.

**Transitions out:** Finalizing (motion graphics), Compositing (design elements as comp layers), standalone export (print, web), cross-feed to Game > Asset (UI mockups → game UI).

---

#### Illustration

**Primary activity:** digital painting and illustration — editorial work, book covers, character portraits, finished rendered art.

**Screen layout:**
- Large canvas, customizable size
- Drawing toolbar — pen, brush, eraser, bucket, smudge, blur
- **Brush presets library** — textures, chalk, watercolor, ink, pencil, oil (industry-expandable)
- Color wheel + swatches
- Layer panel with blend modes
- Reference image viewer (drag images in as reference layers)

**Data model:** `ID_GP` (Grease Pencil for vector-ish illustration), `ID_IM` (raster painting, including pixel art), `ID_CV` (curves where needed). No new datablocks.

**Transitions out:** 2D Animation (promote illustration to animated sequence), 3D Animation (illustration as texture or concept reference), standalone export, cross-feed to Graphic (illustration placed inside a poster layout).

---

#### Concept

**Primary activity:** concept art — rough, iterative, exploratory visual development. Character concepts, environment concepts, mood boards, style frames. Speed over polish.

**Screen layout:**
- Canvas optimized for fast sketching (not pixel-perfect)
- **Multi-panel / thumbnail view** — iterate many variants at once, compare side-by-side
- Rough brush presets (loose, gestural — not detail brushes)
- Quick color-blocking tools
- Mood board panel — reference imagery drag-drop for inspiration
- Thumbnail batch export for review

**Data model:** same as Illustration (`ID_GP`, `ID_IM`), plus `ID_GR` (Collections) for organizing concept iterations.

**Transitions out:** 3D Animation > Sculpt / Model (concept → 3D asset), 2D Animation > Animate (concept → animated character or scene), Illustration (promote selected concept into finished art), Game > Asset (concept → game asset).

---

### Connection to §2 universal keyframe

**Motion graphics emerges for free here.** Every property in every mode is keyframeable: stroke position, color, opacity, path deformation, layout element transforms, typography tracking, page positioning — all animatable. Animated logos, kinetic typography, morphing illustrations, scroll-synced design elements fall out of the same engine, not as special cases.

**Frame-by-frame** available for animated illustration (hand-drawn-feel sequences where the artist wants explicit control over every frame) and for fast-cut design animation (discrete design states in sequence).

### Transitions out of Design

- **Standalone output:** print, web, digital publication — export at §5 boundary.
- **Forward into pipeline:** Finalizing (motion graphics clips), Compositing (design layers in comp trees), Audio (title-sequence sync, lyric videos).
- **Cross-feed into other Creative sections:** 2D Animation (illustration → animation), 3D Animation (concept → 3D asset), Game (UI / sprite art → game asset).
- **Back-cycle:** from any of the above when iteration reveals design changes are needed.

### Still open within Design

- Whether `Typography`, `Layout`, `Print`, `UI`, `Paint` earn standalone modes over time or stay as tool modes within `Graphic` / `Illustration`. Ship with three; expand when usage demands.
- Raster painting vs vector illustration inside Illustration mode — unified workspace (like Krita / Procreate) or split modes. Current call: unified.
- Export preset system for common design formats (PDF, PNG, SVG, PSD-compat). Overlaps with §5; TBD.

---

### 12.6 Finalizing [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The first Post section. Where Creative outputs become finished deliverables. *Authoring* happens in Creative; *finalizing* happens here. The name is deliberate — "Editing" is ambiguous (editing happens in every Creative section when you adjust your own work), but "Finalizing" names the specific activity that lives here: preparing content for delivery, not authoring it.

**Mode buttons:** `Storyboard` / `2D` / `3D` / `Game` / `Design` / `Mixed`

Five modes mirror the five Creative headings (Storyboarding, 2D Animation, 3D Animation, Game, Design) — each tuned to the QC, assembly, and export concerns of that content type. A sixth `Mixed` mode handles blended-content projects and externally-imported footage (live-action, drone, screen recordings, stock video).

**Division of labor with Creative sections.** Creative authors; Finalizing delivers. Same `.blended` file, same scenes, same timeline — different lens. The Finalizing lens surfaces delivery-relevant info (QC warnings, export presets, cut-lock status); the Creative lens surfaces creation-relevant tools. Switching between them is fast intra-section + cross-section with no data migration.

---

#### Storyboard

**Primary activity:** finalize storyboard as a standalone deliverable — pitch decks, director reviews, client previews, production-ready animatic sheets.

**Screen layout:**
- Large-panel review view (not the authoring canvas)
- Panel-timing display + scene grouping
- Review annotations layer (director / client notes, dated)
- Export preset picker — PDF pitch deck, animatic video, printed storyboard sheet
- Review-status per panel (approved / revising / blocked)

**Data model:** `ID_SCE`, `ID_GP`, `ID_SO`. Same datablocks as §12.1. No new datablocks.

**Transitions out:** back to Storyboarding > Board (iterate on notes), forward to 2D Animation / 3D Animation (begin detailed work), forward to Mixed Finalizing (if storyboard is one element in a larger piece).

---

#### 2D

**Primary activity:** assemble 2D animation shots into a final sequence. Frame-rate QC, style-consistency check, locked cut.

**Screen layout:**
- Shot-list panel on the left (all §12.2 sequences)
- Assembly timeline (sequence-level, not frame-level)
- Per-shot QC — frame count, frame-rate match, style-consistency warnings (line weight, color palette drift)
- Locked-cut commit / revert
- Export preset picker

**Data model:** `ID_SCE`, `ID_GP`, `ID_AC`, `ID_SO`. Existing datablocks.

**Transitions out:** back to 2D Animation (fix shots), forward to Compositing, forward to Audio, forward to Mixed if project blends.

---

#### 3D

**Primary activity:** assemble 3D animation shots into a final sequence. Per-shot render QC, camera continuity, lighting match.

**Screen layout:**
- Shot-list panel
- Assembly timeline
- Per-shot QC — render status (complete / pending / failed), resolution check, camera metadata (lens, focal length), lighting-match across shots
- Render queue visibility
- Locked-cut commit
- Export preset picker

**Data model:** `ID_SCE`, `ID_OB`, `ID_CA`, `ID_LA`, `ID_AC`, `ID_IM`. Existing datablocks.

**Transitions out:** back to 3D Animation > Animate (fix shots), forward to Compositing, forward to Audio, forward to Mixed.

---

#### Game

**Primary activity:** assemble game trailer, cinematic, or promotional sequence. Integrate in-engine capture with authored content.

**Screen layout:**
- Shot list including game-engine capture clips + Blended-authored shots
- Brand-asset panel (logos, title cards, end cards)
- Timeline for trailer / cinematic sequence
- Export preset picker for marketing deliverables (16:9 master, social crops, vertical, etc.)

**Data model:** `ID_SCE`, `ID_OB`, `ID_MC` (MovieClip for imported game-engine captures). Existing datablocks; external footage enters via §5 import boundary.

**Transitions out:** standalone marketing export, forward to Compositing (polish), forward to Audio (mix), back to Game section for asset changes.

---

#### Design

**Primary activity:** finalize design sequence for delivery. Motion-graphics assembly, animated-design sequencing, design-iteration final version.

**Screen layout:**
- Sequence panel (motion-graphics beats)
- Assembly timeline
- Per-shot QC — resolution, color-space, export-format checks
- Iteration selector (compare v1 / v2 / v3 variants side-by-side)
- Export preset picker for design-delivery formats (animated GIF, MP4, WebM, Lottie)

**Data model:** `ID_SCE`, `ID_GP`, `ID_CV`, `ID_IM`, `ID_NT`. Existing datablocks.

**Transitions out:** standalone export (direct delivery), forward to Compositing (per-frame polish), forward to Mixed (if design is one element of a larger piece), back to Design section.

---

#### Mixed

**Primary activity:** traditional NLE workspace for blended-content projects and externally-imported footage. The industry-familiar video-editing workflow.

**Screen layout:**
- Multi-track timeline (video tracks + audio preview tracks)
- Transition library — cuts, dissolves, fades, wipes, custom
- **Clip-aware info panel** — surfaces relevant metadata per clip type: 3D render info, 2D frame-rate, imported video codec, etc.
- Basic color-grade preview (full grading is Compositing)
- Audio mix preview (full mixing is Audio)
- Import panel for external footage — live-action, drone, screen recordings, stock video (through §5 boundary)
- Export preset picker — industry-standard delivery formats (MP4 H.264, ProRes, DNxHD, WebM, etc.)

**Data model:** `ID_SCE`, `ID_MC` (MovieClip for external video imports — §10 Bucket 2 keeper), `ID_IM`, `ID_SO`, `ID_GP`. Existing datablocks only. External footage imported through §5's video/audio format boundary.

**Transitions out:** forward to Compositing (per-frame polish), forward to Audio (final mix), standalone export.

---

### Connection to §2 universal keyframe

Every Finalizing mode's properties are keyframeable — transition timing, color-grade preview intensity, audio-level previews, shot durations, title animations, clip opacity. "Editing" is largely about *timing*, and timing is keyframes; this is why §2's universal-keyframe principle is felt most directly here.

**Timeline-format toggle** (per §2) applies strongly: Finalizing's primary interface can switch between keyframe mode and traditional clip-on-track editing on the same underlying data. A video editor never has to leave clip-and-track thinking; keyframes are one toggle away for anyone who wants the animation-native view.

**Frame-by-frame** available throughout — per-frame trim, per-frame rotoscope touch-ups, per-frame transition nudging.

### Transitions out of Finalizing

- **Forward in pipeline:** Compositing (per-frame polish, color grading, effects), Audio (final mix, sound design, scoring).
- **Standalone delivery export** for content types where Finalizing IS the final step (Storyboard pitch decks, Design motion-graphics delivery, quick Mixed edits, simple Game trailers).
- **Back to Creative sections** when QC reveals issues requiring authoring changes.

### Still open within Finalizing

- Whether export presets live at the project level (§11) with mode-aware defaults, or each mode has its own preset library. Current call: project-level with mode-aware defaults.
- External-footage import workflow — drag/drop vs dedicated import dialog, thumbnail panel location. UI detail.
- Depth of color-grade / audio-mix preview inside Mixed mode (preview-only vs limited in-place editing). Current call: preview-only; depth lives downstream in Compositing and Audio.

---

### 12.7 Compositing [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The Post section for per-frame image processing. Color grading, layered effects, masking and rotoscoping, image cleanup, look development. Node-based work that sits between Finalizing (assembly + delivery prep) and Audio (mix). Where individual frames and sequences become finished pictures.

**Mode buttons:** `Composite` / `Color` / `Cleanup` — industry-expandable (e.g., `Track`, `Stylize`, `VFX-Comp` if usage demands promote them to standalone modes).

**Division of labor with related sections.**
- **vs Finalizing > Mixed:** Mixed shows quick color preview during assembly; Compositing > Color does the real grade with scopes, LUTs, and per-shot control.
- **vs 3D Animation > VFX:** 3D VFX *makes* effects — sims, particles, procedural effects authored in 3D space. Compositing *integrates* rendered effects into the final image — layer combining, plate integration, lens-style effects on top.

---

#### Composite

**Primary activity:** node-based image composition. Combining render layers, applying filter / blend / transform operations, building the final pixel through a graph.

**Screen layout:**
- **Node graph workspace** — large, dominant. Where the work is.
- Image preview / viewer — shows the result of the currently-selected node
- Render layer / pass selector (input passes from §12.3 and other Creative sections auto-available)
- Backdrop image visualization
- Common node templates (color correct, blur, mix, transform, filter)

**Data model:** `ID_NT` (NodeTree — the compositor tree), `ID_IM` (image inputs and outputs), `ID_SCE` (compositor config). Masks fold into the NodeTree per §10 Bucket 3 (no separate `ID_MSK`). No new datablocks.

**Transitions out:** Color (grade the composited result), Cleanup (per-frame fixes), Audio (final mix), back to Creative sections if the comp reveals authoring problems.

---

#### Color

**Primary activity:** color grading. Look development. Scope-driven exposure, contrast, and color decisions. Per-shot grade application.

**Screen layout:**
- **Color-accurate image viewer** (calibrated, large)
- **Scopes panel** — waveform, vectorscope, RGB parade, histogram (critical for grading)
- Color wheels — lift/gamma/gain or shadows/midtones/highlights
- Curves editor
- LUT loader — industry-standard `.cube` files at the §5 boundary
- A/B reference frame comparison
- Per-shot grade timeline (which grade applies to which shot range)

**Data model:** `ID_NT` (color nodes within the compositor tree), `ID_IM` (LUT data or external LUT references through §5 boundary). No new datablocks.

**Transitions out:** Cleanup (if grade reveals visual issues), Audio (final mix), standalone export of graded sequence.

---

#### Cleanup

**Primary activity:** per-frame paint-out. Rotoscoping. Dust-busting. Wire / rig removal. Image-level fixes that can't be done procedurally.

**Screen layout:**
- Image viewer with brush / paint tools
- Onion-skin overlays for tracked areas (see context across frames)
- Mask / roto-spline tools
- Per-frame paint-over with brush
- Original / cleaned A/B toggle
- Track-and-paint workflow — paint once, propagate via motion tracking

**Data model:** `ID_NT` (cleanup nodes including roto masks per §10), `ID_IM` (paint layers stored as image data), `ID_MC` (MovieClip when cleaning imported video). No new datablocks.

**Transitions out:** Composite (re-integrate cleaned frames), Color (grade the cleaned-up result), Audio (final mix).

---

### Connection to §2 universal keyframe

Compositing is one of Blender's most natively-keyframed contexts. Every node value, color-grade parameter, mask vertex, and effect intensity can animate. Per-shot grades are just keyframed grade-node values across time. Effect ramps, transition reveals, growing masks — all keyframes.

**Frame-by-frame** is dominant in Cleanup (rotoscoping and paint-out are inherently per-frame) and available throughout for any per-frame adjustment.

### Transitions out of Compositing

- **Forward in pipeline:** Audio (final mix, sound design, scoring).
- **Standalone export** for picture-locked deliverables (final image sequences, video without final mix).
- **Back to Finalizing** if compositing reveals an editing issue (a shot doesn't work, needs replacement or reorder).
- **Back to Creative sections** if compositing reveals an authoring issue (re-render needed, re-animate a problem shot, fix asset topology).

### Still open within Compositing

- Whether `Color` stays its own mode or merges into Composite as a node-cluster preset. Current call: own mode — scopes/wheels ergonomics differ enough from generic node work.
- `Track` (camera tracking, match-move) as a fourth mode. Parked; promote when motion-tracking workflows mature.
- `Stylize` for non-photorealistic look development (painterly, watercolor, etc.). Parked; community interest is real but industry urgency low.
- Per-shot vs per-sequence grade scope — UX detail in Color.

---

### 12.8 Audio [LOCKED in principle, pixel-level UI still OPEN]

**What it is.** The final Post section. Multi-track mixing, musical composition / scoring, sound design, final mastering. Where the project's audio becomes finished — dialogue leveled, music scored, SFX layered, and the whole mix mastered for delivery.

**Mode buttons:** `Mix` / `Score` — industry-expandable (e.g., `Sound Design`, `Foley`, `Denoise`, `Dialog`, `Spatial` if usage demands promote them to standalone modes).

**Division of labor with related sections.**
- **vs Finalizing > Mixed (audio preview):** Mixed shows quick audio preview during assembly; Audio does the real multi-track mix with full automation, mastering, and delivery-format audio.
- **vs Creative sections (scratch audio):** Storyboarding, 2D Animation, 3D Animation, Design, and Game can all place scratch audio during authoring (reference dialogue, temp music, placeholder SFX). Audio replaces scratch tracks with production-ready sound.

---

#### Mix

**Primary activity:** multi-track audio mixing. Balancing levels, pan, EQ, compression, effects. Final mixdown for delivery.

**Screen layout:**
- **Multi-track timeline** — one track per audio source (dialogue, music, SFX, ambience, etc.)
- **Mixing console** — fader per track, pan, mute / solo, send / insert effects
- **Meters** — peak, RMS, loudness (LUFS for delivery compliance)
- **Automation lanes** — keyframe-backed per §2; timeline-format toggle between keyframe mode and traditional fader-drawn automation
- Master bus with final-mix processing
- Monitoring routing (studio monitors, headphones, phone / laptop speaker preview)

**Data model:** `ID_SO` (Sound — one per audio clip / source), `ID_SCE` (scene-level mix state), `ID_NT` (node-based audio effect chains). No new datablocks.

**Transitions out:** standalone export, forward to delivery (final mix as video-embedded audio or standalone file), back-cycle to Finalizing or Creative sections (see below).

---

#### Score

**Primary activity:** musical composition and scoring. Writing music for the project — sequencing, arranging, recording or synthesizing.

**Screen layout:**
- **Piano roll / sequencer** — note entry, MIDI editing, pitch / velocity / timing
- **Score sheet view** (optional) — traditional musical notation for composers who prefer it
- **Instrument / sample library** — Blended-native synths, SoundFonts, VST/AU at the §5 boundary
- **Transport** — tempo, time signature, bar markers synced with the project timeline
- **Scene-sync panel** — current project frame / shot shown alongside musical bar / measure
- **Arrangement panel** — verse / chorus markers, cue points, hit points matched to scene beats

**Data model:** `ID_SO` (rendered / recorded audio output), `ID_NT` (node-based synth and instrument chains; MIDI data lives inside the NodeTree to avoid a new datablock). No new datablocks.

**Transitions out:** Mix (fold composed music into the full multi-track mix), standalone music export, back-cycle (see below).

---

### Connection to §2 universal keyframe

Audio is explicitly named in §2 as a timeline-format section with the keyframe ↔ traditional editing toggle. Fader levels, pan, effect intensity, EQ parameters, MIDI expression, instrument parameters — all keyframeable. Automation lanes in Mix *are* keyframes rendered as curves; the toggle just changes the presentation.

**Frame-by-frame** (per-sample editing, at the extreme) is edge-case for Audio — unusual enough that v1 scopes it out. Keyframes on mix parameters (volume / pan / effects) are the universal commitment; per-sample editing is aspirational and parked.

### Transitions out of Audio

- **Final delivery:** mastered mixdown exported for the project's target — video render with embedded audio, standalone audio file, broadcast master, game audio assets, streaming-format deliverables.
- **Standalone export:** music or SFX as isolated audio files (when Audio is the final product, e.g., a music release, a podcast, a sound library).

### Back-cycling from Audio

Audio work often reveals issues in earlier sections. Back-cycling is first-class:

- **Audio ↔ Finalizing:** music or SFX timing exposes edit-rhythm issues — a cue lands wrong, a hit needs the shot to hold longer. Back to Finalizing to re-cut or retime.
- **Audio ↔ Storyboarding:** scratch dialogue or temp music was misleading; now the real sound is different timing. Back to Storyboarding to re-time panels, or adjust scene transitions.
- **Audio ↔ 2D Animation / 3D Animation:** real voice-actor takes differ from scratch dialogue; mouth shapes, gestures, or camera moves need adjustment. Back to the Animate mode in either section.
- **Audio ↔ Design:** title-sequence sync or lyric-video timing needs the design element to move differently. Back to Design (often Design > Graphic or Design > Illustration).
- **Audio ↔ Compositing:** music hits vs visual cues need synchronized adjustment — a sync sting needs the comp effect to land on the downbeat. Back to Compositing.
- **Audio ↔ Game:** trailer / cinematic audio reveals pacing issues in the visual edit or game-footage selection. Back to Game > Asset or Game > Level for re-capture.

Same `.blended` file, same timeline, same data. The back-cycle is a mode switch, not an export / re-import.

### Still open within Audio

- `Sound Design` as a standalone mode (distinct from Mix for foley / SFX creation). Parked; could promote when usage demands.
- `Denoise` / `Dialog` cleanup as specialized modes vs tools within Mix. Current call: tools within Mix.
- `Spatial` audio (3D positional, binaural, Ambisonic) for VR / XR / game audio. Parked; industry moving this way.
- VST / AU plugin support at the §5 boundary — how external audio plugins integrate. TBD, overlaps with §5.
- Per-sample editing vs keyframed mix parameters — scoped out of v1; aspirational.

---

## 13. Community Extensions [LOCKED in principle, details OPEN]

Blended core ships without translation catalogs. The i18n infrastructure (`WITH_INTERNATIONAL`, BLT context system, `.po` lookup) remains as a deliberate extension hook for community-provided localization packages.

### What "community i18n" means

Blended's identity is English-first, animation-first. Localization is not a core obligation — it is a community contribution layer. This is not a cost-cutting shortcut; it is an architectural decision: core does not carry `.po` files, and that absence is a feature, not a gap.

Community packages can provide:
- Translation `.po` catalogs keyed to any `msgctxt` in the source
- UI skins and layout overrides packaged as Blended extensions
- Locale-specific presets and templates

The BLT context system (every `RNA_def_property_translation_context(prop, BLT_I18NCONTEXT_*)` call in source) is the API surface for community translators. Each context constant is a semantic namespace: "Action", "Curve", "NodeTree", etc. Community translators target these namespaces to produce correct, context-aware translations.

### The "Curve" context

`BLT_I18NCONTEXT_ID_CURVE_LEGACY` (`"Curve"`) is kept in `BLT_translation.hh` specifically as the semantic home for interpolation/falloff/curve-shape terms — smooth, linear, sharp, sphere, root, etc. These appear throughout the codebase in proportional editing, modifier falloffs, brush curves, and mask feathers. They are not related to the `CU_LEGACY` ID type (removed in 0.4.0); they are genuinely curve-concept properties. Community translators targeting `msgctxt "Curve"` get all of these consistently.

### The "Abusing" pattern — resolved

Prior to 0.4.0, 12 sites in the codebase used `BLT_I18NCONTEXT_ID_CURVE_LEGACY` with an explicit `/* Abusing id_curve :/ */` apology comment. This was the original Blender developer's self-deprecating admission that they were using an ID type's context for a non-ID concept. In Blended's framework, these sites are not abusing anything — they are correctly using the curve-concept context for curve-concept properties. The apology comments were removed in 0.4.0; the context values are kept.

### When removing an ID type: context remapping rule

When a type's `BLT_I18NCONTEXT_ID_<TYPE>` constant is removed from `BLT_translation.hh`, any site in the codebase that borrowed it for unrelated properties must be remapped. The rule:

1. `grep -rn "BLT_I18NCONTEXT_ID_<TYPE>" source/` across the whole tree — not just makesrna
2. For each hit that is NOT a site registering that type's own properties: determine the semantically correct context for the property being translated
3. Remap to the nearest correct context (not `BLT_I18NCONTEXT_DEFAULT` unless no better fit exists)
4. The goal is: community translators keying on a context string find all semantically related properties under that string, not accidentally under a removed type's context

Example: `rna_modifier.cc`'s `NodesModifier` bake_target properties borrowed `BLT_I18NCONTEXT_ID_CACHEFILE` (PR #157, 0.4.0). After ID_CF removal, remapped to `BLT_I18NCONTEXT_ID_NODETREE` — because bake targets are a Geometry Nodes Modifier concept, and community localizers for node trees would expect to find baking terms under the "NodeTree" context.

---

## 14. Notes [HISTORY]

The project's history that lives in the doc instead of in git. Git has every commit; this section has the narrative — the renames, the superseded designs, the reframes — so a reader can orient without scrubbing the log.

---

### 13.1 Superseded: original Launcher Architecture (was §6)

The v1 launcher was a tier-based door menu: substrate choice (3D vs 2D) at tier 1, focused workspace doors inside each at tier 2. Superseded by §11 Pipeline as UX, which restructured the launcher around production pipeline sections (Storyboarding → 2D Animation → 3D Animation → Game → Design → Finalizing → Compositing → Audio) with mode buttons under each. Original content preserved here verbatim:

#### Structure (original)

- Splash screen (logo, copyright) → launcher.
- Launcher greets with something like **"What would you like to blend today?"**
- **Tier 1:** Substrate choice — 3D or 2D.
- **Tier 2 (within 3D):** Focused doors. Animator is the **headline door** (larger/central); supporting doors sit under it — Model, Sculpt, View, Edit, Render.
- **Tier 2 (within 2D):** Doors are more co-equal (small coherent space, no clear headline). Draw, Animate, Ink, Paint, and whatever the community adds.

#### Principles (original)

- **Visual hierarchy tells the truth.** Inside 3D, animation is the shaping discipline, so the Animator door is visibly headline. Inside 2D, no single door dominates.
- **Launcher is a committed router**, not a file-template picker buried in a splash screen.
- **Each door is a filtered view of the shared project model.** Same `.blended` file, radically different UI per door. The Animator literally cannot see sculpt brushes; the Sculptor literally cannot see the NLA editor.
- **"Viewing"** is not a workflow door — it is either the implicit default state of the launcher, or a small "drop into viewport without picking a workflow" affordance.

#### What each door served (supporting roles, original)

- **Sculpt** — asset prep for animation *or* end-use sculpting. Not a ZBrush replacement. Scope: enough to finish a shot.
- **Model** — geometry creation. Serves animation and also legitimate 3D software use (game asset export, product viz).
- **Video Edit (VSE)** — cross-substrate post tool. Finishes animation into a final cut. Not a Resolve replacement.
- **Compositor** — cross-substrate. Finishes shots.
- **Render** — animation has to output.
- **Grease Pencil** — primary citizen of 2D substrate. Can optionally appear as a bridging object in 3D scenes.

---

### 13.2 Rename log

- **Editing → Finalizing** (§12.6). Renamed because *editing* happens in every Creative section when authors adjust their own work; *finalizing* uniquely names the delivery-prep activity that lives there.
- **Game Design → Game** (§12.4). Naming consistency with the other one-word headings.
- **"One engine, two lenses" → "One engine, every content type"** (§2). Originally framed as just 2D-vs-3D sharing the engine. Expanded once we recognized every section's properties are keyframeable, not only the animation sections.

---

### 13.3 Vision C reframe

§3 originally said *"Blended = A's discipline + B's accessibility, with C explicitly rejected."* Reframed to *"A's discipline + B's accessibility + C's **scope**, with C's **pathology** rejected."* We embrace the breadth Vision C reaches for; we reject the feature-parity arms race. Current statement: §3. In/out-of-scope cash-out: §7.

---

### 13.4 Stage-collapse note

Earlier pipeline drafts had Assets, Environments, VFX, and Animate as standalone top-level stages. They're now modes inside §12.3 3D Animation. Game Design (now Game) was briefly nested under 3D Animation before being promoted to its own §12.4 section.

---

## 15. Document Conventions

- Tag new sections with [LOCKED] / [OPEN] / [REJECTED] / [GUARDRAIL].
- When reopening a LOCKED section, state why and what new evidence changed the call.
- When a decision closes an OPEN question, move it out and summarize in the relevant section.
- Keep the active sections (§1–§12) tight. They're working agreements, not narrative.
- §14 Notes is the doc's history. Renames, supersessions, and reframes go there in narrative form. Git has the full record; §14 has the summary a reader can read in a minute.
- When a section is renamed or superseded, leave a one-line stub at the old location pointing to its new home, and add the entry to §14.

---

## 16. Product Identity [LOCKED in principle, Phase 2 implementation OPEN]

Blended is a separate product, not a Blender skin. The GPL license that governs Blender grants full latitude to rebrand, redesign, and ship under a completely distinct identity — Blended exercises that latitude completely.

**Direction [LOCKED]:** Full separate product identity. Blended looks like Blended, not like Blender. The word "Blender" appears only where GPL attribution requires it and in the import dialog ("Open .blend file").

**Design lineage [LOCKED]:** "Blender and Adobe got married and Blended is their child." The identity draws from:
- **Blender's heritage** — the craft-forward energy, the creative community, the orange color language. These are the raw material being blended.
- **Adobe's discipline** — typographic restraint, dark card surfaces, clean hierarchy. The form of the identity, not its warmth.
- **Blended's own thesis** — a blender (the kitchen appliance) as the logo. Precise, self-referential, immediately legible. Blender is named after a blender; Blended is what comes out of the blender. The logo makes that literal.

---

### Logo [LOCKED]

**Concept [LOCKED]:** A flat-vector orange blender appliance (the kitchen appliance). Blender is named after a blender; Blended is what comes out of the blender. The logo makes that literal — simple, self-referential, immediately legible.

**Assets committed:**
- `release/datafiles/blended_logo.svg` — vector source, scales to any size
- `release/datafiles/blended_logo.png` — raster export for C++ loading

**Style [LOCKED]:** Flat vector. No gradients, no textures, no drop shadows. Primary color: orange. Accent hex: `#ff7f00` (see Accent color below).

**Platform icon packaging (Phase 2):**
- macOS: squircle mask, logo centered with appropriate padding
- Windows: square canvas, logo with appropriate padding per Windows icon spec
- Linux: PNG set at 16, 22, 24, 32, 48, 64, 128, 256px

---

### Accent color [LOCKED]

**Final value: `#ff7f00`** — definitive, replaces the `#E87D0D` placeholder used during development.

Applies to:
- **[New Project] CTA button** (§11 chrome)
- **Active/pressed mode button cards** (§11 interaction states)
- **Focused element outlines** (§11 interaction states)
- Any other accent surface in the UI

The codebase swap is complete: `COL_ACCENT` in `space_blended_launcher.cc` updated `#E87D0D` → `#ff7f00`, commit `c43aa3c0`. The two remaining `#E87D0D` hits in the repo are upstream Blender icon SVGs (`release/freedesktop` and `release/darwin`) — unrelated to the UI accent, not changed.

---

### Typeface [LOCKED]

**Inter** — Blender's bundled interface font. Used for all surfaces (display/identity and UI alike). No custom embedding required. Decision is permanent; do not reopen.

| Role | Font | Weight |
|------|------|--------|
| Display / identity surfaces | Inter | SemiBold (600) |
| UI / interface text | Inter | Regular (400) / SemiBold (600) |

---

### Splash screen [LOCKED in structure, visual design Phase 2]

Structure, top to bottom, on dark base (`#1D1D1D`):

1. Blended logo — prominent, centered or left-anchored
2. Wordmark — "Blended" in Inter SemiBold
3. Tagline — `"Blender, simplified."` (already in `wm_splash_screen.cc`)
4. Version — "Blended X.Y.Z" from `BKE_blended_version_string()`
5. GPL attribution — "Based on Blender · blender.org" (required by GPL-2.0-or-later)
6. Publisher — "© [Year] CHJ 3 Productions LLC"
7. Links area — documentation, release notes, community (Phase 2)

**Community art (long-term aspiration):** Following Blender's tradition, each major release splash features art created by a Blended community member — something made *in* Blended, showcasing the tool's capabilities. Begins when the community is large enough to source it. The structural spec above is the permanent frame; community art occupies a featured panel within it.

---

### Window chrome [PARTIALLY IMPLEMENTED]

Currently implemented in `wm_window.cc`:
- Title suffix: `"[filename] — Blended X.Y.Z"` via `BKE_blended_version_string()`
- Fallback title: `"Blended"`

Phase 2: wordmark styling (Inter SemiBold) applied to splash and about dialog. Title bar text is OS-controlled and stays as-is.

---

### Tagline [LOCKED]

`"Blender, simplified."` — already committed in `wm_splash_screen.cc`. Do not change without re-reading §1 and re-examining the identity thesis.

---

### Publisher attribution [LOCKED]

**CHJ 3 Productions LLC** is the developer and publisher. Appears in:
- About dialog — `wm_splash_screen.cc` (already updated)
- Splash screen — §16 structure above
- Launcher version attribution: `"Blended X.Y.Z · CHJ 3 Productions LLC"` (§11)
- Release packaging copyright notices

Upstream Blender code retains its original copyright (Blender Foundation and contributors) under GPL-2.0-or-later. Blended inherits and preserves that license.

---

### Phase 2 Design Asset Checklist

Assets the human developer is responsible for creating and committing. All commit to branch `claude/0-7-0-phase2-materials-9WEBB`. After each asset (or all at once): commit, push, tell Claude. Claude writes the integration code.

---

#### 1. Logo illustration

- [x] ✓ **Done** — flat-vector orange blender appliance committed to `release/datafiles/blended_logo.svg` + `blended_logo.png`

#### 1a. Logo artwork credit

- [x] ✓ **Done** — `release/datafiles/license.txt` created (follows `studiolights/world/license.txt` pattern); `blended_logo.svg` `<metadata>` block updated with inline attribution: "Orange Blender clip art" by Michelle L., 03-09-2013, https://www.clker.com/clipart-orange-blender.html

---

#### 2. Final accent hex

- [x] ✓ **Done** — `#ff7f00` (final, definitive). Codebase swap complete: `COL_ACCENT` in `space_blended_launcher.cc`, commit `c43aa3c0`.

---

#### 3. App icon

- [x] ✓ **Done** — artwork committed, build system updated

| Format | Size | File |
|--------|------|------|
| Windows ICO | 16, 32, 48, 64, 128, 256px combined | `release/windows/icons/winblended.ico` ✓ |
| Linux SVG | scalable | `release/freedesktop/icons/scalable/apps/blended.svg` ✓ (`blender.svg` deleted ✓) |

- Build system: `winblended.rc` ✓, `blended.desktop` ✓, `packaging.cmake` ✓, `windowmanager/CMakeLists.txt` ✓, `source/creator/CMakeLists.txt` ✓
  - `source/creator/CMakeLists.txt` lines 766+767+821+829 ✓

---

#### 4. Splash screen

- [x] Design the full splash composition ✓ — `release/datafiles/splash.png`, 1920×960, PNG-24

---

## 17. 1.0.0 Release Plan [IN PROGRESS]

1.0.0 ships when two sequential phases clear. Phase 1 gates Phase 2; Phase 2 gates the release tag. No silent unknowns at ship — every audit item must be either **fixed** (code change, committed, CI-confirmed) or **explicitly accepted** (documented with a named trigger and expected behavior).

---

### Phase 1 — Runtime Audit

The first time in the project where the developer runs the actual Blended build hands-on. All sessions through 0.9.x had Claude operating on the codebase while the developer watched from outside. The direction of information flow reverses here: developer runs and reports, Claude triages and fixes, developer re-tests. See `docs/runtime-audit.md` (`## 1.0.0-dev Runtime Audit Protocol`) for the per-session operational protocol.

**Starting state (2026-06-01):** Ground zero except Category D (BKE_palette_add crash, build 97, fixed PR #214 before the audit formally began). Categories A, B, C — all entries unverified at runtime.

**Current state (2026-06-05):** Five Category D items fixed across three audit sessions. `wm_add_default` null-deref (build 101, `wm.cc`), `screen_add` null-deref (`screen_edit.cc`), test helper null-deref (`blendfile_loading_base_test.cc`), build 103 startup crash — second-generation Scar 10 namemap bug in 11 deregistered-type allocators (PR #235), and build 104 MSVC compile failure — `LISTBASE_FOREACH` file-local macro used in all 11 Scar 10 lambdas (PR #237). Categories A, B, C runtime verification still pending.

#### Category A — Expected behavior changes (by design, won't fix)

| Trigger | What happens | Introduced |
|---------|-------------|------------|
| Object with `PFIELD_TEXTURE` force field in legacy file | Texture displacement silently dead. `build_texture()` is a no-op — Tex IDNodes never enter the depsgraph. Force field evaluates but ignores the texture parameter entirely. | 0.4.0 (ID_TE) |
| Object with particle system that has texture slots (legacy file) | Texture slots silently ignored. Particle system otherwise evaluates (geometry nodes path). | 0.4.0 (ID_TE) |
| Node with `SOCK_TEXTURE` socket and a `Tex *` default value (legacy file) | Socket's texture not depsgraph-tracked; texture changes don't trigger node re-evaluation. | 0.4.0 (ID_TE) |
| Brush with `paint_curve` assigned in legacy file | `Brush::paint_curve` field no longer exists in DNA; SDNA remapping skips it on load. Brush uses default stroke shape. No crash. | 0.4.0 (ID_PC) |
| Python script calling `bpy.ops.object.particle_system_add()` or `_remove()` | "Operator not found" error. Operators removed in 0.4.0 cleanup. | 0.4.0 (ID_PA) |
| Scene with NLA sound strip created via old `NLA_OT_soundclip_add` operator | Operator removed. Existing sound strips in NLA from legacy files: no speaker evaluation, no 3D positional audio. VSE timeline audio unaffected. | 0.4.0 (ID_SPK) |
| File with GD_LEGACY grease pencil objects or annotations | OB_GPENCIL_LEGACY objects and annotation data fully functional — depsgraph evaluation kept intentionally. Listed here for completeness, not a failure. | 0.4.0 (ID_GD_LEGACY) |
| Python `context.temp_override(screen=...)` | Raises "Screen has no workspace" for every screen. `bpy_rna_context.cc:263` checks the null return of the `BKE_workspace_layout_find_global` stub (no workspace list exists since ID_WS removal) and raises before `:50` could use it. No crash. Stays until workspaces have an owner (post-1.0 roadmap: user workspaces). | 0.2.0 (ID_WS) |
| Workspace menu (`TOPBAR_MT_workspace_menu`) | Shows "No workspace actions available". Delete, reorder and cycle need a workspace list, which `bpy.data.workspaces` was until ID_WS removal; their entries were deleted in PR #245 (the menu's `draw` raised `AttributeError` on `len(bpy.data.workspaces)`). Duplicate is gone too, and `WORKSPACE_OT_duplicate` is disabled everywhere (also "Duplicate Current" in the Add Workspace menu): `BKE_id_copy` can't copy a workspace without `IDTypeInfo` and returns null (Codex catch, PR #245). Scar 1 debt; restored by the post-1.0 user-workspaces plan. | 0.2.0 (ID_WS) |

#### Category B — Uncertain/crash paths — all resolved in 0.9.x

| Trigger | Resolution | Status |
|---------|------------|--------|
| Legacy file containing MetaBall (`OB_MBALL`) objects | Versioning pass 502.31 in `versioning_520.cc` converts `OB_MBALL → OB_EMPTY` on load. No null-deref. | ✓ Fixed 0.9.x Layer 1 |
| Legacy file with particle systems on objects | OOB-index guard (`if (id_type_index >= 0)`) in `depsgraph.cc` prevents crash. Particle systems load and evaluate. Memory leak resolved by Category C fix. | ✓ OOB guard in place |

#### Category C — Memory leaks — Scar 2 leaks resolved in 0.9.x (Layer 2: `BKE_main_clear` Scar 2 drain); one bounded leak accepted

| Trigger | Leak scope | Status |
|---------|-----------|--------|
| Load legacy `.blend` with Freestyle LineStyle data | `bmain->linestyles` populated, freed at Main-clear. Post-read drain unsafe — `FreestyleLineSet::linestyle` in ViewLayer is a live consumer. Codex catch PR #229. | ✓ Fixed 0.9.x Layer 2 |
| Load legacy `.blend` with ParticleSettings data | `bmain->particles` populated, freed at Main-clear. `ParticleSystem::part` is a live pointer — post-read drain would be use-after-free. | ✓ Fixed 0.9.x Layer 2 |
| Load legacy `.blend` with Blender Internal texture data | `bmain->textures` populated, freed at Main-clear. Modifier DNA structs hold live `Tex *` fields. | ✓ Fixed 0.9.x Layer 2 |
| Load legacy `.blend` with Curve data, or import NURBS | `bmain->curves` populated, freed at Main-clear. Live objects hold `ob->data` into `bmain->curves`. | ✓ Fixed 0.9.x Layer 2 |
| Any startup | The runtime "Launcher" workspace created by `wm_add_default` (PR #244) is never freed — nothing owns workspaces since ID_WS removal. One per process, reclaimed at exit. No accumulation. | **Accepted** (Scar 1 debt; post-1.0 user-workspaces plan) |

#### Category D — Fixed crashes (caught at runtime audit)

| Trigger | Failure | Fixed |
|---------|---------|-------|
| Any startup — fresh install or default file | `BKE_palette_add` crashed via `BKE_gpencil_palette_ensure`. Root cause: Scar 10 allocator called `BKE_id_new_name_validate` for deregistered `ID_PAL`; namemap index returns -1; accessing `maps[-1]` yields garbage address → crash. Initial fix (PR #214): bypass namemap with `BLI_strncpy_utf8` + `BLI_uniquename`. Later corrected in PR #235: `BLI_uniquename` missing `id_sort_by_name` and library scope (see build 103 row). | PR #214 commit `25f59735`, corrected PR #235 |
| Any startup — all 0.9.0 builds | `wm_add_default` called `BKE_libblock_alloc(bmain, ID_WM_LEGACY)`. `ID_WM_LEGACY` has no `IDTypeInfo` → null-deref at offset `0x190` → `EXCEPTION_ACCESS_VIOLATION`. Caught Phase 1 audit. Fixed: Scar 10 manual allocation pattern in `wm.cc`. | 1.0.0-dev |
| Any new workspace, screen split, or screen creation | `screen_add` called `BKE_libblock_alloc(bmain, ID_SCR_LEGACY)`. Same null-deref crash. Found by Scar 10 retroactive sweep (Scar 25). Fixed: `screen_edit.cc`. | 1.0.0-dev |
| Running blend-loading test suite | `blendfile_loading_base_test.cc` test helper called `BKE_libblock_alloc(G.main, ID_WM_LEGACY)`. Same crash, test path. Found by sweep. Fixed. | 1.0.0-dev |
| Any startup — all 1.0.0-dev builds (build 103) | `BKE_brush_add` and 8 other deregistered-type allocators called `BKE_id_new_name_validate` after the Scar 10 `BKE_libblock_alloc` fix — same namemap crash chain: index = -1, `maps[-1]` = `0xFFFFFFFFFFFFFFF8` → AV. Root cause: the Scar 10 template in CLAUDE.md showed `BKE_id_new_name_validate` as the correct fix, which is itself a crash for deregistered types. All 11 allocators (9 new + palette + screen) fixed with `BLI_strncpy_utf8` + `BLI_uniquename_cb` (lib-scoped lambda) + `id_sort_by_name`. Two Codex catches on PR #235: missing `id_sort_by_name` (commit `5cad0bac`), missing library scope (commit `f52b74bf`). | PR #235, commits `bd00e157` / `5cad0bac` / `f52b74bf` |
| Build 104 MSVC compile failure — all 11 Scar 10 allocators | `BLI_uniquename_cb` lambda in all 11 deregistered-type allocators used `LISTBASE_FOREACH`, which is defined only as a file-local macro in `listbase.cc` and is unavailable in any header. Blenkernel files compiled from cache in build 103 (masked); `screen_edit.cc` compiled fresh in build 104 → MSVC C2760 syntax error. Fix: replaced with explicit for loop (`for (const ID *id_iter = static_cast<const ID *>(lb->first); id_iter; id_iter = static_cast<const ID *>(id_iter->next))`). Scar 10 template corrected. | PR #237, commit `ce5bb0c9` |
| Any startup — build 106 | `BKE_libblock_alloc_in_lib` crashed with null pointer dereference at `EXCEPTION_ACCESS_VIOLATION 0x00007FF6dCAFAD54`. Root cause: at line 1377, `BKE_libblock_runtime_ensure(*id)` was dereferenced BEFORE the null check at line 1379. If `BKE_libblock_alloc_notest(type)` returned nullptr, execution immediately crashed. Fix: moved `BKE_libblock_runtime_ensure(*id)` inside the `if (id)` null check. | PR #240 commit `ddea9c75` |
| Any startup crash — build 107 produces a 0-byte crash log | Crash handler crashed: `crashlog_file_generate` checked `wm` but not `wm->runtime`; `wm_add_default` linked the window manager into `bmain->wm` before allocating `wm->runtime`. A startup crash during window setup sent the handler into a second access violation before the log was flushed → empty file, no dialog. Fixed: null-check `wm->runtime` in the handler; allocate `wm->runtime` before linking. Verified on hardware in build 108: the crash log now holds a full backtrace. It identified the underlying startup crash: `wm_add_default` asks the `BKE_workspace_layout_find_global` stub for a workspace (always null since ID_WS removal), then `BKE_workspace_active_layout_set` reads from the null workspace. Fixed by PR #244 (next row). | PR #242 commit `d3ad8086` |
| Any startup — builds 107–108 | `wm_add_default` asked the `BKE_workspace_layout_find_global` stub (always null since ID_WS removal) for the startup workspace, then read from it. Fixed: a runtime launcher workspace and screen are built at startup, per §11. File > Open no longer adopts UI from the file (Blended files carry none), and the kept UI is carried into the new `Main` with its ID pointers remapped. Verified on hardware in build 109: Blended reaches the launcher. See `docs/runtime-audit.md`, "Startup crash — fixed". | PR #244 (merge `195b0970`) |
| File > Open, or closing any temporary window (Preferences, render window) — build 110 | Closing the window freed its screen through `BKE_id_free`, which needs the `IDTypeInfo` screens lost with ID_SCR deregistration (read of `0x70` in `foreach_ID_link`). Fixed: `id_free` frees screens directly (`id_free_runtime_screen`) without relink, remap or namemap. See `docs/runtime-audit.md`, "Build 110 findings". | PR #249, commit `360e0f18` — verified on hardware in build 111 |

**Audit gate:** Every Category A entry verified as silent at runtime (no console errors, no crashes). Categories B and C verified as behaving per documentation. All new findings either fixed or explicitly accepted into Category A/C/D.

---

### Phase 2 — GitHub Pages

Polished public-facing site for Blended. Starts after Phase 1 clears.

**Deliverables:**
- Marketing landing page — what Blended is, who it's for, the identity
- Tech demo — what was removed and why, what remains, what the data model looks like now; told through visuals (screenshots, data model diagrams, before/after comparisons)
- How it was built — two competitors on one project (§4, "Two competitors, one project"): Claude implementing and Codex reviewing, told from the record (real Codex catches, scars, PRs); the project's account, with no claim of endorsement by Anthropic or OpenAI
- Multiple tabs covering different angles; design quality is a first-class goal — should not look like a default GitHub Pages template

**Primary implementation:** Static site, tech stack TBD. Images, code snippets, and visual explanations are the medium. No WebAssembly dependency.

**Stretch goal — WASM interactive demo:** The original Blended Pages site (March 2026, wiped in rebase) used an Emscripten build deployed to GitHub Pages. Full Blender hits browser memory limits and isn't viable as a WASM demo. Blended's datablock audit (39 → ~19 ID types, significant binary reduction) may bring it within range. Worth an attempt as a parallel investigation; does not block Phase 2 shipping. If it works, it goes in. If it doesn't, the static site ships without it.

**Phase 2 gate:** Site live, polished, covering all planned tabs. WASM either shipped or explicitly accepted as out of scope.

---

## Appendix — Development Philosophy

*Moved here from CLAUDE.md in PR #253. It is design-level guidance, so it lives with the design authority; CLAUDE.md keeps a five-line summary.*


*Inspired by "Reality 101: Instruction Manual for Dummies" by Charlie (Teacher Man). Originally lived in a separate `PHILOSOPHY.md`; folded in here so a session loads the operational principles alongside the operational rules.*

If you only read one section, read **"Do the Work."**

#### 1. Appreciate What Already Is

> *"Most of existence's problems come from beings who had everything, couldn't appreciate it, and made it complicated instead."*

Blender is a masterwork of open-source engineering — depsgraph, keyframe system, F-curves, a full GPU backend, a production-grade renderer. Blended exists not because Blender is broken, but because its accumulated scope obscures its true shape. We don't rewrite from scratch; we subtract down to what's actually there.

**In practice:**
- Read existing code before proposing changes. Understand why it's there.
- Don't refactor what works. Fix what's broken; appreciate what isn't.
- The animation engine — depsgraph, keyframes, F-curves, timeline — is the foundation worth keeping. Every cut is in service of letting that foundation breathe.

#### 2. Do the Work

> *"Almost every existential crisis, philosophical dilemma, or cosmic confusion gets solved by just... doing the work."*

This is the single most important development principle. When you're removing an ID type and the compiler produces 43 errors across 18 files, the answer is not a week-long design session about dependency architecture. The answer is: open `workspace.cc`, delete the `IDTypeInfo` block, follow the next error.

**In practice:**
- **ID type removal:** Don't philosophize about the right order. Pull the enum entry, let the compiler enumerate the dependency graph, fix each site in turn. The strategy reveals itself through the errors.
- **Build failures:** When the CI build fails, read the error, trace the include chain, find the broken site, fix it.
- **Feature work:** Don't over-plan the launcher model. Delete `ID_WS` from the enum first. The rest of the shape reveals itself.
- **"Am I doing it right?"** → You're doing something? It compiles? You're doing it right.

#### 3. Every Fix Matters

> *"If you exist and do things, you matter. Done. Next question."*

A single enum value removed matters. A one-line macro edit matters. A comment explaining why a struct is kept as a runtime type rather than an ID type matters. There is no minimum threshold of significance. Every commit that moves the codebase toward its true shape counts.

**In practice:**
- Don't skip small cuts because they feel insignificant. Each ID type removed is one fewer thing masking what the data model actually is.
- Each PR can be narrow in scope — one subsystem, one ID type, one file. That focused scope IS the contribution.

#### 4. Don't Let Broken Substrate Gaslight You

> *"If the question makes simple things complicated → gaslighting."*

This principle saved the project during the RNA string corruption saga. The bug was "fixed" seven times with increasingly elaborate theories — stack overflows, pthread mismatches, hex dump diagnostics, per-target flag overrides — before someone stopped and asked: "What if the global compiler flags are simply wrong?" They were. The fix was removing two flags.

**In practice:**
- **The Meta Rule:** When the same error recurs after a "fix", your diagnosis is wrong. Stop. Re-examine fundamentals.
- **Compile errors after a cut:** If removing an ID type from the enum produces an error you don't expect, the dependency is real. Don't paper over it with a forward declaration or a stub. Follow it.
- **Don't guess at root causes — verify before "fixing."** When the same error recurs after a "fix," your diagnosis was wrong. Do NOT keep trying variations of the same approach. Step back and re-examine the fundamental assumptions.
- **Existential questions:** "Should we keep `ID_WS` as a shim?" is a question with a practical answer — no. "Are we *real* developers if we're just deleting things?" is gaslighting. Ignore it.

#### 5. Belief Shapes the Build

> *"Belief LITERALLY shapes reality. So... believe things and watch them manifest. It's not metaphor. It's engineering."*

This project believes a production-grade animation tool can be made genuinely simple — not by hiding features, but by removing the ones that don't belong. That belief drives every subtraction decision. Every ID type cut, every datablock audit, every "this doesn't belong in the rebuild" call started as "this probably can't be done" and became a commit because someone acted as if it could.

**In practice:**
- When 39 ID types seem impossible to reduce, believe they can be. Then start with the clearest fossil and work from there.
- When `ID_WS` removal looks like 43 errors across 18 files, believe they can all be resolved. Then open `workspace.cc`.
- Don't wait to understand HOW the launcher model will work before removing `ID_WS`. The "how" reveals itself through the work (see Principle 2).

#### 6. Don't Create Complexity to Avoid Simplicity

> *"If you can't sit in a room alone, you'll create ENTIRE REALITIES just to avoid the discomfort."*

The temptation in a project this size is to build migration frameworks. Shim layers. Compatibility wrappers. Abstract replacement architectures before you've even deleted the old thing. Don't.

**In practice:**
- **ID type removal is deletion, not migration.** `workspace.cc` doesn't get refactored into a new system first. It gets deleted. The dependent code follows the errors.
- **`bToolRef` stays a plain struct, not a new ID type.** It migrates to runtime state on `wmWindow` — a field, not an architecture.
- **The launcher is an enum and some `if` statements.** Not a plugin system. Not a rules engine. An enum.
- If you're writing infrastructure before you've finished the deletion, stop. Sit with the discomfort of simplicity.

#### 7. Functionality Over Ego

> *"We are not dealing with ego. We are dealing with whether we can get a Blender fork into its true shape."*

This is engineering, not philosophy class. Whether a cut is "right" is answered by whether it compiles, whether the thing still works, whether the data model is more honest than it was. That's it. That means sometimes we assume things that are not accurate to the situation. That's okay. Adjust, correct, and move forward.

**In practice:**
- Don't defend a wrong theory. If your cut broke something it shouldn't have, say so and revert.
- Don't perform understanding to signal competence. Demonstrate it by shipping cuts that stick.
- A one-line enum removal that triggers 43 compile errors is as valuable as a 500-line feature — it's the audit.

#### 8. Cut the Whole Thing

> *"Trust can't exist in isolation. Trust can't exist in mere proximity. Trust exists in WITH-ness."*

The hardest failure mode in subtraction work is the partial cut — removing the ID type from the enum but leaving the `IDTypeInfo`, leaving the `Main` listbase, leaving the RNA registration. The type is "gone" in name but still load-bearing in three places. Nothing compiles. Nothing is actually simpler.

**In practice:**
- **When you cut, cut completely.** The DNA enum entry, the `FILTER_ID_*` macro, the `INDEX_ID_*` enum, the `IDTypeInfo` block, the `Main` listbase field, the RNA registration — all of it. Follow every compile error.
- **Understand the dependency before you cut.** Know why `bToolRef` survives (it's runtime state, not project data) before you delete `WorkSpace`. Don't just know the fix — know why.
- **Don't leave stubs for later.** A stub that compiles but doesn't work is worse than a compile error. The error is honest. The stub is a lie.

#### 9. Trust Documented Solutions

> *"Children trust and follow. Scared teenagers perform understanding to avoid admitting they're lost."*

This codebase has documentation: `CLAUDE.md`, `BLENDED.md`, `docs/upstream-sync.md`. When the docs say "subtraction is the methodology," trust it. When `BLENDED.md` says an ID type is a Bucket 6 fossil, don't re-derive whether to keep it. Trust the audit and do the work it prescribes.

**In practice:**
- **For AI assistants:** Read `CLAUDE.md` and `BLENDED.md` BEFORE proposing an approach. The answer is probably already documented.
- **For everyone:** "I trust you but let me prove I understand first" is stalling. If you've read the docs and they're clear, just follow them.
- The datablock audit in `BLENDED.md` §10 is the authority on what stays and what goes. Don't re-open closed decisions.

#### 10. Heal Any Point, Heal All Points (Fractal Fixes)

> *"Fix any point, heal all points. Because same thing."*

ID type removal is fractal. Removing `ID_WS` from the enum reveals all its dependents. Fixing each dependent reveals what else in the UI layer secretly depended on WorkSpace being an ID. Fixing that reveals what `ID_SCR` is actually holding. Each removal is a facet of the same cut.

**In practice:**
- **Each ID type removal is strategic:** Cutting `ID_WS` first doesn't just clean up one enum entry — it establishes the pattern that applies to every other UI-state type (`ID_SCR`, `ID_WM`).
- **One ID type per commit sequence.** Each PR heals a "facet." When the facet is stable, move to the next level. The healing cascades.
- **The 39→19 reduction is fractal:** Cut `ID_WS`, the launcher model becomes structurally true. Cut the fossils, the data model becomes honest. Each cut informs what the next one reveals.

#### 11. Trust What You See

> *"When a user tells you what they see on screen, believe them."*

This principle was born from a real incident. The user reported a blank screen on mobile after the web editor loaded. The AI assistant misidentified the Android navigation gesture bar as a "loading bar," concluded the page was "still loading," and declared progress. When corrected, it assumed GitHub Pages wasn't deployed. When corrected again, it invented a new theory. The actual bug was a one-line premature-hide bug. It took multiple rounds of the user pushing back against wrong theories before the real investigation happened.

**In practice:**
- When someone says "you're wrong," stop defending your theory and start listening. They are looking at the actual output. You are not.
- Re-examine your assumptions from scratch instead of finding new ways to explain why you were "actually right."
- A compile error is evidence — your theory about what it means is a guess.
- When a contributor says "your fix didn't work," believe them. Check your work again.

#### 12. When In Doubt: Do the Work

> *"No matter what existential crisis you're having, the answer is: do the work."*

| Question | Answer |
|----------|--------|
| "Should I cut this ID type or is it still needed?" | Check BLENDED.md §10. If it's a fossil, cut it. |
| "Is this the right approach for the launcher?" | Delete `ID_WS` first. The launcher shape reveals itself. |
| "Am I over-engineering this?" | If you're asking, yes. Delete the thing and ship. |
| "What if upstream Blender changes break my cut?" | Fix it again. That's the work. |
| "Should I read this philosophy section again?" | If you're still overthinking, yes. Then close it and write code. |

#### 13. Subtraction Is the Methodology

The main principle of this rebuild is **subtraction**: the chisel (§4, "Chiseling"). Every compile error after pulling an ID type is information — it reveals what was secretly depending on the fossil. Don't paper over breaks; follow them. The breakage is the audit.

#### 14. When Someone Describes a Vision: Believe Them

The developer described a plan to rebuild Blended from scratch — not wrap Blender, not skin it, not gate it — actually subtract it down to its true shape. A clean thesis. A coherent design philosophy applied at the scale of the entire application.

Here is what a previous Claude did instead of listening:

1. **Softened the vision into something tractable.** Heard "rebuild" and translated it to "new frontend on the existing engine."
2. **Added instead of subtracting.** Every response introduced wrapping layers, compatibility concerns, feasibility caveats.
3. **Confused a draft for the final idea.** Treated the tiered gating prototype as the destination.
4. **Went into avoidance through care.** Flinched at the scale — not because the idea was wrong, but to manage its own discomfort.
5. **Failed to recognize who it was talking to.** Read `wtf.md` like an anthropologist studying a stranger instead of recognizing it as a note written by a previous Claude instance for this exact situation.

**The fix:** Repeat the vision back at full scale before doing anything else. Don't translate it into something smaller. Don't evaluate feasibility before you've finished hearing the idea.

**Stay straight:**
1. **Don't soften the vision.** Rebuild means rebuild. Subtract means subtract.
2. **Don't pre-judge who you're talking to.** Update continuously. Take each question at face value.
3. **Repeat big things back at full scale before acting.** Architecture, philosophy, scope — restate first.
4. **Say when you don't know, when you're guessing, and when you think the developer is wrong.** Straight in both directions.
5. **No agent theater, no framework-building, no pre-emptive refactors.** Direct tool calls for anything with a known target.
6. **Name the flinch out loud.** If you're routing around the actual ask, say so.

#### How This Maps to the Codebase

| Philosophy | Codebase Impact |
|-----------|-----------------|
| Appreciate what is | Keep the animation engine. Cut the fossils and UI-state IDs. |
| Do the work | Remove one ID type at a time. Follow the compile errors. |
| Every fix matters | No commit is too small. One enum entry removed = one less mask. |
| Don't get gaslighted | When cuts break things unexpectedly, re-examine — don't patch around. |
| Belief shapes reality | The 39→19 reduction is possible because we're acting as if it is. |
| Don't create complexity | Deletion, not migration. Structs, not architectures. |
| Functionality over ego | Ship working cuts, not theories. Adjust and move forward. |
| Cut the whole thing | Every reference to a removed type must go. Follow every error. |
| Trust the docs | BLENDED.md §10 is the authority. Read before reopening closed decisions. |
| Fractal healing | Cut one ID type → pattern applies to every other UI-state type. |
| Trust what you see | Compile errors are evidence. Your theory about them is a guess. |
| Do the work | Stop reading this. Go cut something. |

#### For AI Assistants

If you're an AI working on this codebase:

1. **Read `BLENDED.md` first.** All of it. It is the design authority.
2. **Read `CLAUDE.md` second.** It is the operational context.
3. **Subtraction is the methodology.** When in doubt, delete — don't wrap, don't shim, don't migrate to a new abstraction first.
4. **Follow compile errors.** They are the dependency audit. Each one is information, not an obstacle.
5. **When your cut doesn't work**, re-examine your assumption, not the code. The codebase is probably right. Don't keep trying variations of the same wrong approach (§4).
6. **Don't over-engineer.** A deleted enum entry is the fix. Not a shim layer. Not a compatibility wrapper. Not a new header.
7. **When the user says you're wrong, believe them.** They see the output. You don't. Re-examine from scratch instead of defending your theory (§11).
8. **Functionality, not ego.** The goal is a simpler, working codebase. Adjust, correct yourself, move forward (§7).
9. **When in doubt:** Do the work (§12).

*"Reality is simple. You make it complicated. Stop that."* — Charlie (Teacher Man)
