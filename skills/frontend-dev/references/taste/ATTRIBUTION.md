# Attribution

The `taste-frontend` skill is adapted from **taste-skill** by **Leonxlnx**.

- Upstream: https://github.com/Leonxlnx/taste-skill
- License: MIT
- Copyright (c) 2026 Leonxlnx

## What was adapted

- `SKILL.md` — condensed from the upstream `taste-skill` (v2) flagship: brief inference, the three dials, design-system summary, em-dash ban, and the full pre-flight check.
- `references/design-systems.md` — upstream §2 + Appendices A/B (install commands, canonical docs).
- `references/ai-tells.md` — upstream §4 (design engineering directives) + §9 (production AI tells).
- `references/motion-gsap.md` — upstream §5 canonical GSAP/Motion skeletons + §6/§7 perf and dial definitions.
- `references/redesign.md` — upstream §11 redesign protocol merged with the standalone `redesign-skill`.
- `references/liquid-glass.md` — upstream Appendix C (honest Apple Liquid Glass web approximation).
- `references/aesthetic-minimalist.md` — adapted from `minimalist-skill`.
- `references/aesthetic-brutalist.md` — adapted from `brutalist-skill`.
- `references/aesthetic-soft-highend.md` — adapted from `soft-skill`.
- `references/output-enforcement.md` — adapted from `output-skill`.

## Local modifications

- **Asset policy:** upstream recommends `picsum.photos` seed URLs as the no-gen-tool fallback. This adaptation replaces that with **real Pexels photo URLs** (`images.pexels.com/photos/{id}/...`) plus photographer attribution, falling back to TODO placeholder slots. The "image-generation tool first" priority is preserved.
- Frontmatter, install/`npx skills add` chatter, and cross-skill links from the source variant skills were removed; they are plain reference docs here.
- `gpt-tasteskill`, `stitch-skill`, `image-to-code-skill`, and the three image-generation skills (`imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit`) were intentionally not vendored.

## Upstream MIT License

```
MIT License

Copyright (c) 2026 Leonxlnx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
