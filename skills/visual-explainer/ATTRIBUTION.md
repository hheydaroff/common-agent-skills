# Attribution

`visual-explainer` is adapted from the MIT-licensed
[visual-explainer](https://github.com/nicobailon/visual-explainer) by nicobailon.

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

## Not vendored
- `extension.ts` (Pi native tool) — this repo deploys skills only.
- Per-harness `configs/` and marketplace `.claude-plugin/` manifests.

## Upstream license
MIT © nicobailon. See the upstream repository for the full license text.
