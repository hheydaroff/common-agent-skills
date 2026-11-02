# IDML XML edit recipes

Specific edits beyond plain text replacement, each verified against a real InDesign
round-trip by the upstream author. Read `SKILL.md` first for the unpack/pack commands
and the "edit inside `<Content>` runs" rule.

Adapted from **mindboard/indesign-extendscript-plugins** (`skills/idml`, MIT).
Where upstream said "do this in the `indd` skill", that sibling skill is not vendored
here — it drives a live InDesign app via ExtendScript. Do those steps in InDesign
manually, or import it from the same repo.

**Adding a line / paragraph.** A forced line break is a `<Br />` element *between*
`<Content>` runs inside one `CharacterStyleRange`; a new paragraph is a sibling
`<ParagraphStyleRange>`. To add a line, insert `<Br /><Content>…</Content>` before the
closing `</CharacterStyleRange>` — reusing the surrounding style so the new line
inherits formatting (verified: grew a 3-line body to 4 lines this way).

**Emphasising part of a line (bold/italic run).** Split the run into sibling
`CharacterStyleRange` elements and give the emphasised one a different `FontStyle`
(e.g. `FontStyle="Bold"` / `"W6"`), keeping the same `<AppliedFont>`:
```xml
<CharacterStyleRange ... FontStyle="W3"><Content>当店は</Content></CharacterStyleRange>
<CharacterStyleRange ... FontStyle="Bold"><Content>港町「海の家」の干物</Content></CharacterStyleRange>
<CharacterStyleRange ... FontStyle="W3"><Content>を使用。</Content></CharacterStyleRange>
```
(Verified: rendered the middle run bold within the same family.)

**Swapping a linked image.** Placed images are *referenced*, not embedded. In the
relevant `Spreads/Spread_*.xml` find the `<Link … LinkResourceURI="file:/abs/old.jpg" …>`
and change the URI to the new absolute path. InDesign relinks on open (verified). The
other `<Link>` attributes (`LinkResourceSize`, `LinkImportStamp`, modification times)
can be left pointing at the old file — InDesign reconciles them on open; you only need to
change the URI.

**Almost always re-fit after a swap — not just on aspect-ratio change.** The image's
scale is baked into the parent `<Image>`'s `ItemTransform`, computed from the *old*
file's pixel size. A replacement with **different pixel dimensions — even at the identical
aspect ratio — renders at the wrong scale** (e.g. a 2420×1760 photo dropped onto a frame
sized for a 220×160 one shows only a tiny crop). So after relinking, **re-fit in
InDesign** (ExtendScript, or Fit > Fill Frame Proportionally in the UI):
```javascript
frame.fit(FitOptions.FILL_PROPORTIONALLY);
frame.fit(FitOptions.CENTER_CONTENT);
```
Matching the aspect ratio just means the re-fit fills cleanly with no awkward crop; it
does **not** remove the need to re-fit. (Verified: same 1.375 aspect, 11× larger pixels,
required the re-fit.)

**Applying a paragraph style.** Styles live in `Resources/Styles.xml`
(`<ParagraphStyle Self="ParagraphStyle/body" …>`); a story applies one via
`AppliedParagraphStyle="ParagraphStyle/body"` on its `ParagraphStyleRange`. Creating or
restyling paragraph styles, reflowing frames, and **building tables** (`<Table>`/`<Cell>`
markup is extremely verbose to hand-author) are far easier in InDesign than by
hand — do structural/layout changes there and edit text/links here.

**Vertical Japanese text (縦書き / `vertical-rl`).** The writing axis is a **per-story**
attribute on the `<StoryPreference>` element inside each `Stories/Story_*.xml`. Set
`StoryOrientation="Vertical"` (the default is `"Horizontal"`) to turn that story 縦書き:

```xml
<StoryPreference … StoryOrientation="Vertical" StoryDirection="LeftToRightDirection" />
```

The neighbouring `StoryDirection` is the **bidi** axis (LTR/RTL for Hebrew/Arabic) and
stays `LeftToRightDirection` — it does **not** control vertical vs horizontal, so don't
touch it for Japanese. Orientation only changes how text flows *inside* the frame; frame
geometry/position in `Spreads/Spread_*.xml` is unaffected, and `vertical-rl`'s
right-to-left column order is implied by the vertical orientation (no extra attribute).
Each frame's story carries its own setting, so flip it on **every** story you want
vertical. (Verified: round-tripping the vertical `pokemon_b.idml` shows
`StoryOrientation="Vertical" StoryDirection="LeftToRightDirection"` on every vertical
story.)

