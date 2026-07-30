# smart Europe brand theme (optional)

Use this palette **only when the user wants smart / smart Europe branding**
(internal decks, governance docs, exec briefs, "in our brand"). It is a
deliberate brand identity, so it overrides the generic anti-default guidance in
SKILL.md — the Inter body font and single-accent palette are intentional here.

For any non-smart request, ignore this file and use the generic aesthetic
directions in the SKILL.

## Design tokens

```css
:root {
  --bg:        #FFFFFF;   /* white canvas */
  --surface:   #F1F0EE;   /* warm-gray cards / containers */
  --border:    #DFE2E5;
  --text:      #141414;   /* near-black, brand's intentional dark */
  --text-dim:  #595959;   /* body (WCAG AA 5.9:1) */
  --muted:     #969DA3;   /* badges, captions, footer */
  --accent:    #D7E600;   /* electric lime — HERO accent, use sparingly */
  /* secondary accents (use at most one per page, for charts/status) */
  --mint:  #ACE6B7;
  --sky:   #7DCFE3;
  --coral: #EA9C98;
  --amber: #F7BF31;
}
```

Fonts: **Montserrat** (headings) + **Inter** (body). Load from Google Fonts.
Brand bullet character: `>` (distinctive — use for list markers where it reads
well).

## The #1 rule: lime is a thin accent, not a fill

Do **not** fill cards, columns, table rows, or big shapes with `--accent`. That
reads as "random green boxes" and breaks the brand. Lime is allowed only as:

- a title underline rule / left band,
- a section-divider band (on a dark `#141414` background),
- **one** thin left-bar highlighting a single element per section,
- small column-header underline tabs.

All cards stay `#F1F0EE`. All body text stays `#595959`.

## Aesthetic

Flat: **no shadows, no gradients, no 3D**. White background, generous
whitespace, warm-gray cards with ~8px radius, numbered `#969DA3` badges, and a
footer bar (warm-gray rounded rect). Section dividers invert to a dark
`#141414` background with a lime eyebrow + band and white title.

## Mermaid themeVariables (smart light)

```js
theme: 'base',
themeVariables: {
  fontFamily: 'Inter, sans-serif',
  background: '#FFFFFF',
  primaryColor: '#F1F0EE',
  primaryTextColor: '#141414',
  primaryBorderColor: '#DFE2E5',
  lineColor: '#969DA3',
  secondaryColor: '#FFFFFF',
  tertiaryColor: '#F1F0EE'
}
```

Use lime (`#D7E600`) only to `classDef` a single highlighted node, never as the
default node fill.

Provenance: tokens extracted from `TEMPLATE_smart_PowerPoint_Master_2024.pptx`
(same source as the `smart-pptx-deck` skill).
