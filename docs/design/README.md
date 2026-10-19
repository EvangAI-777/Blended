# Design art — older version

**These files are an older version of Blended's design documents. They are reference art, not the
current spec.** Where they differ from the repository, the repository wins: `BLENDED.md` (§11
the launcher, §16 product identity, §17 Phase 2), the launcher code
(`source/blender/editors/space_blended_launcher/`) and the shipped branding assets.

The developer made them with Claude Design and added them in PR #259. The design project's own
manifest, `github.md`, records its last sync as 2026-09-04. They're kept as they were exported,
unedited, as a starting point for the Phase 2 site and as a record of how the design looked at
that point.

| File | What it is |
|------|------------|
| `Launcher.dc.html` | The launcher home screen: "Blending?" prompt, Creative and Post sections with their modes, a header with "+ New" and "Open…", and a Recent Projects sidebar |
| `Pipeline_Diagram.dc.html` | Creative → Post, with the shared Animation Engine every section runs through |
| `Branding.dc.html` | Wordmark, palette and tokens, type scale, icons, splash, usage guidelines |
| `GitHub_Pages_Landing.dc.html` | A draft of the Phase 2 marketing page |
| `github.md` | The Claude Design project's manifest (screen map, sources, last sync) |
| `support.js` | The Claude Design runtime the pages load (`./support.js`). It loads React 18.3.1 and Babel 7.29.0 from unpkg to render them |

## Where they differ from the repository

Checked against the repo when the files were added. Fix these in any version that ships, and
don't copy them from here:

- **Landing, status:** "Latest build: January 2026". The project began with the fork in April
  2026; the latest build when these were added was build 112 (October 2026).
- **Landing, "Explicitly Not":** "Foundation rebuilt from scratch". Blended is chiseled from
  upstream Blender, not built from scratch (`BLENDED.md` §4, "Chiseling").
- **Landing, "Fast & Lightweight":** smaller builds, faster startup and lower memory have not been
  measured.
- **Landing, pipeline graphic:** leaves out Audio. Post has three sections: Finalizing,
  Compositing, Audio (`BLENDED.md` §11). `Pipeline_Diagram.dc.html` includes it.
- **Launcher, Compositing:** shows one mode. The code has three: Composite, Color, Cleanup.
- **Post blue `#0066cc`** (landing, pipeline diagram) is not in the branding palette.
- **Branding, app icon and splash:** a placeholder gradient square and a gradient splash. Blended
  already has its own logo, app icon and splash from 0.7.x (`release/`, `CHANGELOG.md` 0.7.0).
- **Branding, "Never" rule:** "use Layer 2 neutral gray (#323232)" is garbled; `#323232` is the
  hover color, and Layer 2 is `#2c2c2c`.
- **Manifest (`github.md`):** "Ready for GitHub Pages static hosting". Nothing is hosted; the Phase
  2 site is still to be built. It also says the screens have "No external dependencies except Google
  Fonts", but every page loads `support.js`, which loads React, ReactDOM and Babel from unpkg.
- **Pipeline, sequence:** the diagram's subtitle ("Two sequential stages") and the landing page's
  "Work flows through Creative → Post" read as a fixed order. In Blended every section and mode is
  freely enterable; the pipeline is an organizing metaphor, not a forced sequence (`BLENDED.md` §11).
- **Launcher, version attribution:** the mockup has none. `BLENDED.md` §11 lists version
  attribution as part of the launcher's file-management chrome (only its placement is open).
- **Launcher, hover states:** the mockup uses inline `onmouseover`/`onmouseout` strings.
  `support.js` passes them to React as strings, not functions, so the hover states don't fire when
  the page renders through it. (The landing page uses CSS `:hover`, which works.) A shipped
  version uses CSS `:hover` or real handlers.

The launcher mockup's header ("+ New", "Open…") and its Recent Projects sidebar are one picture of
the file-open model under discussion (`BLENDED.md` §11, "Opening a project enters it"). That model
isn't decided.
