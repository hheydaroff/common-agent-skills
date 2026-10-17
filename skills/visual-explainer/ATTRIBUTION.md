# Attribution

`visual-explainer` is adapted from the MIT-licensed
[visual-explainer](https://github.com/nicobailon/visual-explainer) by nicobailon.

The smallest-view-first ladder and the inline code-shape sketches
(`references/inline-shapes.md`, plus the ladder in `SKILL.md`) are adapted from
the MIT-licensed [`show-me`](https://github.com/humanlayer/skills/tree/main/plugins/show-me)
skill by [humanlayer](https://humanlayer.dev).

The isometric "anatomy" approach (`references/isometric-anatomy.md`) is adapted from the
MIT-licensed [`anatomy`](https://github.com/wheresryan22/anatomy) skill by Ryan, pinned at
commit `be2fa9b` (v1.1.0).

The semantic-pattern catalogue, complexity budgets, remove test, and static-frame rule
(`references/diagram-grammars.md`) are adapted from the MIT-licensed
[`diagram-design`](https://github.com/cathrynlavery/diagram-design) skill by Cathryn Lavery
(v2.6.110), specifically its `references/semantic-patterns.md` and
`references/layout-budget.md`.

## Vendored verbatim
- `references/css-patterns.md`, `references/libraries.md`,
  `references/responsive-nav.md`, `references/slide-patterns.md`
- `templates/architecture.html`, `templates/data-table.html`,
  `templates/mermaid-flowchart.html`, `templates/slide-deck.html`

## Local modifications
- `SKILL.md` frontmatter rewritten to repo convention ("Use when…" + triggers)
  and reference routing table repointed at `references/`.
- Default output path changed from `~/.agent/diagrams/` to `docs/diagrams/`
  inside the current repo (falls back to `~/.agent/diagrams/` when there is no
  project). Applied in `SKILL.md` and `references/workflows.md`.
- Upstream slash-command prompt templates folded into `references/workflows.md`
  (the native-tool `visual_explainer.prepare/render` reference was removed since
  that Pi extension is not vendored).
- Added `references/smart-brand.md` — an optional smart Europe brand theme
  (tokens from `TEMPLATE_smart_PowerPoint_Master_2024.pptx`).
- Added `references/inline-shapes.md` and the "Smallest view first" ladder in
  `SKILL.md` — chat-first shapes (pseudocode, call/component/file trees, `diff`)
  that gate when an HTML file is worth writing at all. From humanlayer/show-me.
- Added `references/isometric-anatomy.md` — the anatomy approach distilled (object-is-the-
  explanation, size gate, workflow, craft rules, card frame, verify-by-reading-PNGs) plus
  an offline fallback. The kit, deep references and examples are fetched on demand at the
  pinned commit by the new `scripts/anatomy-kit.sh`, not vendored.
- Added a "capture PNGs and read every one" bullet to the final checklist, harvested from
  anatomy's verification loop and applied to all pages, not just anatomy figures.
- Added `references/diagram-grammars.md` — nine behaviour-first patterns (required elements,
  budget, anti-patterns, static frame), universal and per-shape complexity caps with the
  split rule, the remove test, the static-frame rule, and a meaning-side anti-pattern table.
  Each pattern's "nearest visual type" was re-targeted from upstream's SVG layout grammars to
  Mermaid / HTML `<table>` / CSS cards, and the Mermaid samples in it were parse-verified
  against `mermaid@11.17.2`. Adds a "Pattern before representation" subsection, a routing
  row, two representation rows, a Mermaid-keyword invariant, and two checklist items to
  `SKILL.md`.
- Extended `references/libraries.md` "Which Mermaid Diagram Type?" from 7 to 31 rows and added
  a "Keyword exactness" subsection. This is **our own finding, not upstream content**: the
  type list, `-beta` suffix rules (`radar-beta` only; `sankey`/`sankey-beta` both), and
  `flowchart-elk` were established by parsing samples against the pinned `mermaid@11` build
  (11.17.2), after the upstream review showed our docs covered only 7 of the types it registers.
  The existing `C4Context` guidance is kept — it is a theming preference, not a capability
  claim, and C4 does parse in 11.17.2.

## Not vendored
- `extension.ts` (Pi native tool) — this repo deploys skills only.
- Per-harness `configs/` and marketplace `.claude-plugin/` manifests.
- From anatomy: `kit/` (~700 KB of projection/solid/audit code), the eight `examples/`,
  the beta 3D "figures that turn" mode, and `scripts/publish.mjs` (community gallery).
  All reachable in the on-demand cache; nothing is published on the user's behalf.
- From diagram-design: the hand-authored SVG engine and its 45 per-type layout grammars
  (`type-*.md`, which are canvas coordinates and connector geometry for that renderer), the
  Python `verify-*.py` / `lint-skin.py` / `self_check.py` toolchain, the pinned editorial skin
  (`style-guide.md`, paper/ink/coral), draw.io / Excalidraw import and PNG/SVG export,
  `output-spec.md`, and the SHA-256-pinned motion controller (ADR 0001).
  **Deliberately not adopted:** upstream's rule that diagrams are static and script-free by
  default conflicts with this skill's mandated zoom/pan/expand controls, and its anti-pattern
  "reproducing Mermaid's renderer layout" conflicts with this skill being Mermaid-first. Only
  the renderer-agnostic discipline was ported.

## Upstream license
MIT © nicobailon. See the upstream repository for the full license text.
anatomy: MIT © 2026 Ryan. See the upstream repository for the full license text.
diagram-design: MIT © 2025 Cathryn Lavery. See the upstream repository for the full license text.
