
# smart Corporate-Light PPTX Deck

## When to Use
Any slide deck for smart / smart Europe that should look on-brand: white background, **electric-lime `#D7E600`** as a *sparing* accent, **warm-gray `#F1F0EE`** cards, **Montserrat** headings + **Inter** body, the `>` brand bullet, a footer bar, numbered grey badges, and a **flat** aesthetic (zero shadows/gradients). Built with pptxgenjs on the brand canvas (13.33×7.5 = `LAYOUT_WIDE`, which matches the smart master exactly).

For a generic (non-smart) deck or full strategist workflow, use `pptx-generator`. This skill is the smart-brand harness on top of it.

## The Build Kit
`smart-deck-kit.js` (in this references dir) exports the theme tokens + helpers. Copy it next to your `compile.js` and `require("./smart-deck-kit")`. It gives: `newDeck()`, `helpers(pres)` → `{ footer, title, card, badge, accent, NL }`, and `T` (tokens).

Minimal slide:
```js
const kit = require("./smart-deck-kit");
const pres = kit.newDeck();
const h = kit.helpers(pres);
const s = pres.addSlide(); s.background = { color: kit.T.bg };
h.title(s, "Slide title", "optional subtitle");
h.card(s, 0.5, 2, 6, 4);
s.addText(h.NL(["First point", "Second point"]), { x:0.85,y:2.3,w:5.3,h:3, fontFace:kit.BODY, fontSize:13, color:kit.T.body });
h.footer(s, 2);
pres.writeFile({ fileName: "output/deck.pptx" });
```

## Tokens (smart light)
Canonical palette, full FOR smart font collection, and exact slide positions live in [smart-corporate-style.md](smart-corporate-style.md). The build kit's `T` mirrors it, with two deliberate deltas for a portable, text-first deck:
- **Cards/containers** `F1F0EE` + **border** `DFE2E5` — warmer neutrals than the master's `E9E9E9`.
- **Fonts** Montserrat (head) / Inter (body) — web-safe stand-ins for FOR smart Sans/Next when the brand fonts aren't installed.

Core (same as style guide): bg `FFFFFF`, title `141414`, body `595959`, muted `969DA3`, hero accent `D7E600`. Canvas `LAYOUT_WIDE` 13.33×7.5.

## The #1 rule: lime is a THIN accent, not a fill
**Do NOT fill cards/columns/rows with lime.** That reads as "random green boxes" and breaks the brand. Lime is allowed ONLY as:
- the standing **title underline rule** (auto via `title()`),
- the **cover side-band** + cover rule,
- the **deep-dive/section divider** (dark `#141414` bg + lime band/eyebrow),
- **one** thin `accent()` left-bar per content slide to highlight a single element,
- small column-header underline tabs (a few thin `0.05"` rules, symmetric — fine).
All cards stay `#F1F0EE`. All body text stays `#595959`. If you catch yourself passing `T.lime` as a `fill` on a big shape, stop.

## Recurring slide patterns (proven)
- **Cover**: white bg, 0.35" lime left band, big Montserrat title, lime rule under it, audience + date lines.
- **Section divider**: bg `T.primary` (dark), lime eyebrow text + lime left band, white 46pt title.
- **Cards row** (3 or 4 across, 13.33 canvas): 4-col `w≈2.857 gap 0.3 x:0.5,3.66,6.81,9.97`; 3-col `w≈3.843 gap 0.4 x:0.5,4.74,8.99`.
- **Funnel "at a glance"**: 4 narrowing centered rounded-rect bands (e.g. w 7.0/5.6/4.2/2.8 at cx≈4.05, h0.85 step1.0), one `accent()` on the filter band, a downward `ISOSCELES_TRIANGLE` (rotate 180) into a dark "endpoint" chip, numbered legend column on the right aligned row-by-row.
- **Risk/tier table**: full-width stacked rounded-rect rows; highlight the key row with a single `accent()` left-bar (not a lime fill).
- Page badge: this kit puts the number in the **footer bar** (right side) — every slide except the cover and dark dividers gets `footer(s, n)`.

## Gotchas (all hit and solved)
- **pptxgenjs is installed GLOBALLY**, not in the vault/cwd. Run with `NODE_PATH=/opt/homebrew/lib/node_modules node compile.js`, else `Cannot find module 'pptxgenjs'`.
- **Shape names**: there is **no `TRIANGLE`**. Use `ISOSCELES_TRIANGLE` (point down via `rotate:180`). Valid arrows: `DOWN_ARROW`, `RIGHT_ARROW`, `CHEVRON`, etc. The reliable basics are `RECTANGLE`, `ROUNDED_RECTANGLE`, `OVAL`, `LINE`. Probe with a tiny script in cwd: `node -e` requiring pptxgenjs is fine but write it to a file in cwd (inline `-e` with the absolute NODE_PATH string can trip path guards).
- **No markitdown / no LibreOffice** on this machine for QA. Verify the build by unzipping: `cd output && unzip -q deck.pptx -d _qa && ls _qa/ppt/slides/slide*.xml | wc -l` and `grep -l "some phrase" _qa/ppt/slides/*.xml`. Then `rm -rf _qa`.
- **`addNotes`** per slide for speaker notes; one notesSlide is generated per slide — count them in QA to confirm.
- **Renumbering when inserting a slide**: footer numbers are literal `footer(s, N)` calls. Edits match the original text, so remap each (6→7, 8→9, …) in one edit call; safe because each `footer(s, N)` string is unique.
- Dividers use dark bg and intentionally get **no footer** (or a muted one).

## Output layout
```
<deck-dir>/slides/
  smart-deck-kit.js   # copied from this skill
  compile.js          # builds all slides, one IIFE per slide
  output/deck.pptx
```
Build: `cd slides && NODE_PATH=/opt/homebrew/lib/node_modules node compile.js`

## Provenance
Tokens extracted from `TEMPLATE_smart_PowerPoint_Master_2024.pptx` (see vault memory `slaide-smart-corporate-light-complete` / `slaide-smart-theme-extraction`). Image assets (smart photos, line icons, logo SVGs) live in the slaide repo's `pptx-generator/references/themes/smart-corporate-light/assets/` and are NOT on every machine — this kit is text/diagram-first and renders the lowercase **smart** wordmark as text when no logo asset is present.
