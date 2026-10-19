# Blended Design Art Source

**repo:** EvangAI-777/Blended  
**branch:** main  
**path:** (N/A — design artifacts, not codebase recreation)

## Last sync

**date:** 2026-09-04T17:00:00Z  
**commit:** (N/A — design-only project)

### Updated in this project

- Launcher home screen (complete UI from §11 Pipeline spec) — sidebar file chrome + main pipeline scroll
- Branding system package (logo, color palette, typography, icons, splash screen, usage guidelines)
- Pipeline diagram (Creative → Post flow with animation engine) — visual representation of §11
- GitHub Pages landing page (marketing site for Phase 2 deliverable)

## Screen map

| Screen | Source Reference |
|--------|------------------|
| Launcher.dc.html | BLENDED.md §11 — Launcher Architecture (visual lineage from Adobe CC + Blender splash; pipeline scroll, dark 3-layer hierarchy, Inter typography, 8px spacing, 130ms hover transitions) |
| Branding.dc.html | BLENDED.md §11 Launcher aesthetic; §0.7.x branding complete (accent #ff7f00, dark surface hierarchy #1d1d1d–#e0e0e0, Inter font stack, color tokens) |
| Pipeline Diagram.dc.html | BLENDED.md §11 Pipeline as UX; §2 One engine, two substrates (Creative: Storyboarding → 2D Animation → 3D Animation → Game → Design; Post: Finalizing → Compositing → Audio) |
| GitHub Pages Landing.dc.html | Phase 2 deliverable: marketing site + tech demo scaffold (hero, what is Blended, pipeline overview, key features, scope, status, footer) |

---

## Notes

All four screens are Design Components (`.dc.html`) — single-file, streaming templates. No external dependencies except Google Fonts (Inter). All colors, spacing, and typography hardcoded per BLENDED.md §11 locked specs. Ready for GitHub Pages static hosting or further iteration.
