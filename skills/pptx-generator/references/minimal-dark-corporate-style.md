# Minimal Dark Corporate Style Guide

> **Style Identity**: Dark-first, ultra-clean corporate presentation style inspired by premium consulting/tech RFP decks. Maximum whitespace, minimal ornamentation, high-contrast text on deep black backgrounds. Professional without being sterile.
>
> **Best for**: RFP responses, technical proposals, enterprise pitches, capability decks, partnership proposals, B2B sales decks, consulting deliverables.
>
> **Source reference**: Valtech × smart RFQ Presentation (2026)

---

## Brand Colors

### Core Theme

| Key | Hex | Role | Usage |
|-----|-----|------|-------|
| **primary** | `0A0A0A` | dk1 — Near-black | Slide backgrounds (primary surface) |
| **secondary** | `1A1A1A` | dk2 — Elevated dark | Cards, panels, dark containers on dark bg |
| **accent** | `A3D900` | accent1 — Electric lime-green | Headings accent word, category labels, links. **Use sparingly** |
| **light** | `E5E5E5` | accent6 — Light gray | Horizontal rules, separators, subtle borders |
| **bg** | `0A0A0A` | lt1 — Background | Default slide fill (dark mode) |

### Extended Palette

| Hex | Name | Usage |
|-----|------|-------|
| `FFFFFF` | Pure white | Primary text on dark backgrounds |
| `B3B3B3` | Medium gray | Secondary text, captions, muted labels |
| `808080` | Mid gray | Tertiary text, footnotes, source citations |
| `2A2A2A` | Card dark | Elevated card/panel backgrounds, table cells |
| `333333` | Border dark | Subtle borders, divider lines on dark bg |
| `A3D900` | Lime green | Accent highlights — section letters, links, emphasis keywords |
| `8BC34A` | Soft green | Chart series 1, progress bars |
| `4CAF50` | Green | Chart series 2, success states |
| `66BB6A` | Light green | Chart series 3 |
| `AED581` | Pale green | Chart series 4 |

### Color Rules

- **Background is ALWAYS dark** (`0A0A0A` or `1A1A1A`) — this is a dark-mode-first design
- **Text is ALWAYS white or light gray** on dark backgrounds — never dark text on dark bg
- **Lime green (`A3D900`) is an accent only** — used for: section divider letters, first word of two-word headings, link text, category labels. **Never** as large fills or body text
- **No gradients** — flat, solid colors only
- **Cards and panels** use `1A1A1A` or `2A2A2A` to create subtle elevation on the `0A0A0A` background
- Horizontal separator lines: `333333` or `E5E5E5` at 1pt weight
- White-on-dark contrast is the primary visual mechanism

### PptxGenJS Theme Object

```javascript
const theme = {
  primary: "0A0A0A",    // dk1 — near-black backgrounds
  secondary: "1A1A1A",  // dk2 — elevated surfaces
  accent: "A3D900",     // accent1 — lime green (USE SPARINGLY)
  light: "E5E5E5",      // accent6 — light gray separators
  bg: "0A0A0A"          // lt1 — slide background
};

const chartColors = ["A3D900", "8BC34A", "4CAF50", "66BB6A", "AED581", "B3B3B3"];

const text = {
  title: "FFFFFF",       // white — all headings
  body: "E5E5E5",        // light gray — body text
  muted: "B3B3B3",       // medium gray — captions, secondary
  accent: "A3D900",      // lime green — emphasized words in titles
  onWhite: "0A0A0A"      // dark text if white panel ever used
};
```

---

## Typography

### Font Strategy

This style uses **system-safe fonts only** for maximum compatibility across machines. No custom font installation required.

| Role | Font | Fallback | Weight | When to Use |
|------|------|----------|--------|-------------|
| **Titles / Headings** | `"Arial"` | Helvetica | Regular (not bold) | Slide titles — clean, light weight |
| **Body / Content** | `"Arial"` | Helvetica | Regular | Body text, descriptions, lists |
| **Display / Hero** | `"Arial"` | Helvetica | Regular | Cover titles, section dividers — size does the work |
| **Bold emphasis** | `"Arial"` | Helvetica | Bold | Key phrases, names, bold callouts |
| **Monospace** | `"Courier New"` | Courier | Regular | Code snippets, technical values |

### Font Rules

- **Titles are NOT bold by default** — they rely on large size + white-on-black contrast for impact
- **Bold is used selectively** — for names, key terms, category headings within body text
- **Italic is used for** — quotes, testimonials, subtitle emphasis (large italic for hero quotes)
- **No decorative fonts** — Arial/Helvetica only for the entire deck
- **Letter-spacing**: default (no manual tracking adjustments)
- **Line height**: ~1.3× for body text, ~1.1× for titles

### Size Scale

| Element | Size (pt) | Weight | Color |
|---------|----------|--------|-------|
| Cover title (hero) | 44–50 | Regular | `FFFFFF` |
| Cover subtitle / italic tagline | 28–36 | Regular Italic | `FFFFFF` |
| Section divider title | 54–64 | Regular | `FFFFFF` |
| Section divider letter | 72–96 | Regular | `FFFFFF` (top-right) |
| Content slide title | 28–36 | Regular | `FFFFFF` |
| Subtitle / section label | 12–14 | Regular | `B3B3B3` (muted) |
| Body text | 14–16 | Regular | `E5E5E5` |
| Bullet text | 13–15 | Regular | `E5E5E5` |
| Caption / source | 9–10 | Regular | `808080` |
| Stat / big number | 44–56 | Bold | `FFFFFF` or `A3D900` |
| Stat label | 10–12 | Regular | `B3B3B3` |
| Page number | 10 | Regular | `B3B3B3` |

---

## Layout Standards

### Slide Dimensions

| Property | Value |
|----------|-------|
| **Layout** | LAYOUT_WIDE (13.33" × 7.5") |
| **EMU** | 12192000 × 6858000 |
| **Ratio** | 16:9 |

> ⚠️ Use `pres.layout = 'LAYOUT_WIDE'` — this is the 13.33" × 7.5" format, NOT the standard 10" × 5.625".

### Key Positions (inches)

| Element | x | y | w | h | Notes |
|---------|---|---|---|---|-------|
| **Left margin** | 0.80 | — | — | — | Content starts here |
| **Header bar** | 0.00 | 0.00 | 13.33 | 0.60 | Top bar with logo + nav text + date + page# |
| **Header separator** | 0.00 | 0.60 | 13.33 | 0.01 | Thin line below header |
| **Title area** | 0.80 | 0.90 | 11.73 | 1.20 | Content slide title zone |
| **Content area** | 0.80 | 2.20 | 11.73 | 4.80 | Main content zone |
| **Two-col left** | 0.80 | 2.20 | 5.60 | 4.80 | Left column |
| **Two-col right** | 6.80 | 2.20 | 5.73 | 4.80 | Right column |
| **Two-col gap** | — | — | 0.40 | — | Between columns |
| **Three-col each** | — | — | 3.60 | — | Each of three columns |
| **Four-col each** | — | — | 2.65 | — | Each of four columns |
| **Page number** | 12.60 | 0.15 | 0.50 | 0.30 | In header bar, right |
| **Logo icon** | 0.40 | 0.12 | 0.36 | 0.36 | Small icon/asterisk in header, top-left |
| **Nav text left** | 1.00 | 0.15 | 3.00 | 0.30 | "Company x Partner" in header |
| **Nav text center** | 4.50 | 0.15 | 4.33 | 0.30 | Section name, centered |
| **Nav text right** | 9.00 | 0.15 | 3.00 | 0.30 | Date (e.g. "March 2026") |

### Margin & Spacing

| Property | Value |
|----------|-------|
| Left content margin | 0.80" |
| Right content margin | 0.80" |
| Content width | 11.73" (13.33 - 0.80 - 0.80) |
| Header height | 0.60" |
| Title → content gap | 0.10"–0.20" |
| Bottom safe zone | 7.00" |
| Inter-card gap | 0.20"–0.30" |

---

## Header Bar Pattern

Every content slide (not cover or section divider) has a **persistent header bar** at the top:

```
┌──────────────────────────────────────────────────────────┐
│ ✳  Company x Partner       Section Name        Date   ## │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   (slide content below)                                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

```javascript
// Header bar background (slightly lighter than slide bg)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 13.33, h: 0.60,
  fill: { color: "0A0A0A" }
});

// Header separator line
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.60, w: 13.33, h: 0.01,
  fill: { color: "333333" }
});

// Small logo/asterisk icon (top-left)
slide.addText("✳", {
  x: 0.40, y: 0.12, w: 0.36, h: 0.36,
  fontSize: 14, fontFace: "Arial",
  color: "A3D900", align: "center", valign: "middle"
});

// Left nav text
slide.addText("Company x Partner", {
  x: 1.00, y: 0.15, w: 3.00, h: 0.30,
  fontSize: 10, fontFace: "Arial",
  color: "B3B3B3", valign: "middle"
});

// Center nav text (section name)
slide.addText("Section Name", {
  x: 4.50, y: 0.15, w: 4.33, h: 0.30,
  fontSize: 10, fontFace: "Arial",
  color: "B3B3B3", align: "center", valign: "middle"
});

// Right nav text (date)
slide.addText("March 2026", {
  x: 9.00, y: 0.15, w: 3.00, h: 0.30,
  fontSize: 10, fontFace: "Arial",
  color: "B3B3B3", align: "right", valign: "middle"
});

// Page number (far right)
slide.addText(String(slideIndex), {
  x: 12.60, y: 0.15, w: 0.50, h: 0.30,
  fontSize: 10, fontFace: "Arial",
  color: "B3B3B3", align: "right", valign: "middle"
});
```

---

## Slide Type Patterns

### 1. Cover Slide

Full-bleed dark cinematic hero image covering the entire slide. White text overlaid.

| Element | Position | Style |
|---------|----------|-------|
| Hero image | Full bleed: x=0, y=0, w=13.33, h=7.5 | Dark, cinematic photography. Semi-transparent dark overlay if needed |
| Company badge | x=0.80, y=0.80 | Small white text: "Company ✳ Partner" |
| Main title (bold) | x=0.80, y=2.50, w=10.00 | 44–50pt, white, regular weight. First line is bold keyword |
| Italic tagline | x=0.80, y=3.50, w=10.00 | 36pt, white, italic. Multi-line flowing statement |
| Subtitle | x=0.80, y=5.60, w=8.00 | 14pt, white/gray, regular. "Technical description" |
| Partner logos | x=0.80, y=6.60, w=3.00 | Small white logos, bottom-left |
| Date | x=11.00, y=6.80 | 10pt, white, bottom-right |

**Key rule**: The cover image should be dark/moody (dusk, night, dark interiors). Text sits on the image with no box or overlay needed if image is dark enough.

### 2. Section Divider Slide

Full-bleed cinematic image with large white title text at bottom-left. Section letter at top-right.

| Element | Position | Style |
|---------|----------|-------|
| Hero image | Full bleed: x=0, y=0, w=13.33, h=7.5 | Cinematic, related to section topic |
| Small asterisk icon | x=0.50, y=0.40 | White ✳, 14pt |
| Section letter | x=12.00, y=0.30, w=1.00 | 72–96pt, white, regular weight. "A", "B", "C", etc. |
| Section title | x=0.50, y=4.50, w=10.00 | 54–64pt, white, regular weight. Large, lower-left |

**Key rule**: Section dividers have NO header bar. The image fills edge-to-edge. Title text sits on the bottom portion where the image is darkest.

### 3. Content Slide — Full Width

Standard workhorse slide. Dark bg, header bar, title + content area.

| Element | Position | Style |
|---------|----------|-------|
| Header bar | (see Header Bar Pattern above) | Standard nav |
| Subtitle label | x=0.80, y=0.90, w=5.00 | 12pt, `B3B3B3`, muted label (e.g. "Our understanding") |
| Title | x=0.80, y=1.10, w=11.73 | 28–36pt, white. Accent word in `A3D900` |
| Horizontal rule | x=0.80, y=2.10, w=11.73, h=0.01 | `333333` separator (optional) |
| Body content | x=0.80, y=2.30, w=11.73 | 14–16pt, `E5E5E5` |

### 4. Content Slide — Two Column

| Element | Position | Style |
|---------|----------|-------|
| Left column | x=0.80, y=2.20, w=5.60 | Text, bullet lists, descriptions |
| Right column | x=6.80, y=2.20, w=5.73 | Text, bullet lists, descriptions |
| Vertical divider (optional) | x=6.60, y=2.20, h=4.80 | 1pt, `333333` |

### 5. Content Slide — Multi-Column Cards (3 or 4 columns)

Used for capability grids, service offerings, pillar layouts.

| Element | Position | Style |
|---------|----------|-------|
| Card background | Per column | `1A1A1A` or `2A2A2A` fill, no border |
| Card heading | Top of card | 16–18pt, `A3D900` (lime green) |
| Card body | Below heading | 13pt, `E5E5E5` |
| Card gap | Between cards | 0.20"–0.30" |

**Key rule**: Cards are flush rectangles with no rounded corners and no shadow. Dark-on-dark elevation only.

### 6. Content Slide — Left Text + Right Image

Split layout: text on the dark left half, image on the right half.

| Element | Position | Style |
|---------|----------|-------|
| Left panel | x=0, y=0.60, w=6.50, h=6.90 | `0A0A0A` bg |
| Left content | x=0.80, y=1.00, w=5.30 | Title + body text + bullets |
| Right image | x=6.50, y=0.60, w=6.83, h=6.90 | Cinematic photo, edge-to-edge on right side |
| Dashed category label (optional) | On left panel | Dashed-border box with `A3D900` text inside |

### 7. Team / People Slide

| Element | Position | Style |
|---------|----------|-------|
| Title | x=0.80, y=1.00 | 36pt, white, e.g. "Here with you today" |
| Horizontal rule | Below title | `333333`, full content width |
| Profile photos | Row at ~y=3.50 | Circular crop, ~1.2" diameter, evenly spaced |
| Name | Below each photo | 14pt, white, bold |
| Role/title | Below name | 11pt, `B3B3B3` |

### 8. Contents / TOC Slide

| Element | Position | Style |
|---------|----------|-------|
| Title ("Contents") | x=0.80, y=1.20, w=4.00 | 36pt, white |
| TOC list | x=5.00, y=1.60, w=7.50 | Each item in its own row |
| Section letter | Left of each row | 16pt, `A3D900` (lime green). "A", "B", "C" |
| Section name | Right of letter | 18pt, white |
| Row background | Alternating | `1A1A1A` / `0A0A0A` for zebra stripe effect |

### 9. Stats / Key Figures Slide

| Element | Position | Style |
|---------|----------|-------|
| Large number | Prominent placement | 44–56pt, white or `A3D900`, bold |
| Stat label | Below number | 10–12pt, `B3B3B3` |
| Source citation | Bottom-left | 9pt, `808080`, italic |

### 10. Quote Slide

Full dark background, large italic quote text.

| Element | Position | Style |
|---------|----------|-------|
| Quote text | x=0.80, y=1.20, w=10.00 | 28–36pt, white, **italic**. Include quotation marks |
| Horizontal rule | Below quote | Short line, ~3", `333333` |
| Attribution name | Below rule | 14pt, `A3D900`, bold |
| Attribution title | Below name | 12pt, `B3B3B3` |

### 11. Letter / Message Slide

Three-column layout: photo+name on left, letter text in center+right columns.

| Element | Position | Style |
|---------|----------|-------|
| Left column (narrow) | x=0.80, w=2.50 | Title, circular photo, name, role |
| Center column | x=3.80, w=4.50 | Letter body text, 14pt |
| Right column | x=8.50, w=4.00 | Letter body continued |
| Greeting | Top of center column | 14pt, white. "Dear [Team]," |
| Bold emphasis line | After greeting | `A3D900`, 14pt, bold. Key message hook |

### 12. Timeline / Phases Slide

Horizontal phased layout, no header bar.

| Element | Position | Style |
|---------|----------|-------|
| Phase columns | Equal width across slide | Side by side |
| Phase header | Top of each column | `1A1A1A` bg, white text: "Phase 1 | Weeks 1-4" |
| Focus section | Below header | `2A2A2A` bg, "Focus" label, bullet items |
| Deliverables section | Below focus | `1A1A1A` bg, "Deliverables" label, bullet items |

### 13. Thank You / End Slide

Split layout: image left, dark panel right.

| Element | Position | Style |
|---------|----------|-------|
| Left image | x=0, y=0, w=6.50, h=7.50 | Cinematic hero photo |
| Right panel | x=6.50, y=0, w=6.83, h=7.50 | `0A0A0A` bg |
| "Thank you." text | On right panel, centered vertically | 50pt, white, regular |
| Contact info | Below thank you | Name, role, email in white/green |
| Partner logos | Bottom of right panel | Small white logos |

---

## Visual Elements & Rules

### Separator Lines

```javascript
// Horizontal separator — thin, subtle
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.80, y: 2.10, w: 11.73, h: 0.01,
  fill: { color: "333333" }
});
```

### Dashed Category Labels

Used to tag content areas (e.g. "Operational Excellence"):

```javascript
// Dashed border category label
slide.addText("Category Name", {
  x: 0.80, y: 5.80, w: 2.80, h: 0.40,
  fontSize: 12, fontFace: "Arial",
  color: "A3D900", align: "center", valign: "middle",
  border: { type: "dash", pt: 1, color: "A3D900" }
});
```

### Card / Panel Elevation

```javascript
// Dark elevated card on dark background
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.80, y: 2.50, w: 3.60, h: 4.00,
  fill: { color: "1A1A1A" },
  // NO shadow, NO border, NO rounded corners
});
```

### Circular Profile Photos

```javascript
// Circular photo crop (approximation — use rounding option)
slide.addImage({
  path: "photo.jpg",
  x: 1.50, y: 3.20, w: 1.20, h: 1.20,
  rounding: true  // Circular crop
});
```

### Progress / Accent Bars

Thin colored bars used below headings in card layouts:

```javascript
// Green progress bar under card heading
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.80, y: 3.40, w: 3.60, h: 0.06,
  fill: { color: "8BC34A" }
});
```

---

## What NOT to Do

| ❌ Don't | ✅ Do Instead |
|----------|--------------|
| Use white or light slide backgrounds | Always use `0A0A0A` dark bg |
| Use bold for all titles | Titles are regular weight — size creates hierarchy |
| Use gradients anywhere | Flat, solid colors only |
| Use shadows on shapes | Elevation via dark-shade difference only |
| Use rounded corners on cards | Sharp rectangular edges |
| Use lime green as text color for body | Lime only for accent words, labels, links |
| Use lime green as large fills | Lime only for thin bars and small highlights |
| Put colored backgrounds on content | Dark gray cards (`1A1A1A`) for elevation |
| Use decorative fonts | Arial only, everywhere |
| Skip the header bar on content slides | Always include on content slides (not on cover/divider) |
| Crowd the slide with content | Generous whitespace (dark space) around all elements |

---

## Quick Start — PptxGenJS with Minimal Dark Corporate Style

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';  // 13.33" × 7.50"

const theme = {
  primary: "0A0A0A",
  secondary: "1A1A1A",
  accent: "A3D900",
  light: "E5E5E5",
  bg: "0A0A0A"
};

const text = {
  title: "FFFFFF",
  body: "E5E5E5",
  muted: "B3B3B3",
  accent: "A3D900"
};

const FONT = "Arial";

// === Helper: Add header bar to content slides ===
function addHeader(slide, { leftText, centerText, rightText, pageNum }) {
  // Header background
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.33, h: 0.60,
    fill: { color: theme.primary }
  });
  // Separator line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0.60, w: 13.33, h: 0.01,
    fill: { color: "333333" }
  });
  // Asterisk icon
  slide.addText("✳", {
    x: 0.40, y: 0.12, w: 0.36, h: 0.36,
    fontSize: 14, fontFace: FONT,
    color: theme.accent, align: "center", valign: "middle"
  });
  // Left text
  slide.addText(leftText || "", {
    x: 1.00, y: 0.15, w: 3.00, h: 0.30,
    fontSize: 10, fontFace: FONT,
    color: text.muted, valign: "middle"
  });
  // Center text
  slide.addText(centerText || "", {
    x: 4.50, y: 0.15, w: 4.33, h: 0.30,
    fontSize: 10, fontFace: FONT,
    color: text.muted, align: "center", valign: "middle"
  });
  // Right text (date)
  slide.addText(rightText || "", {
    x: 9.00, y: 0.15, w: 3.00, h: 0.30,
    fontSize: 10, fontFace: FONT,
    color: text.muted, align: "right", valign: "middle"
  });
  // Page number
  slide.addText(String(pageNum || ""), {
    x: 12.60, y: 0.15, w: 0.50, h: 0.30,
    fontSize: 10, fontFace: FONT,
    color: text.muted, align: "right", valign: "middle"
  });
}

// === Cover Slide ===
const cover = pres.addSlide();
cover.background = { color: theme.bg };
// Add dark hero image as full-bleed background
// cover.addImage({ path: "hero.jpg", x: 0, y: 0, w: 13.33, h: 7.5 });
cover.addText("Company ✳ Partner", {
  x: 0.80, y: 0.80, w: 5.00, h: 0.40,
  fontSize: 16, fontFace: FONT,
  color: "FFFFFF"
});
cover.addText([
  { text: "Project Title\n", options: { fontSize: 48, color: "FFFFFF", breakType: "none" } },
  { text: "Compelling Tagline That\nSpans Multiple Lines", options: { fontSize: 36, color: "FFFFFF", italic: true } }
], {
  x: 0.80, y: 2.50, w: 10.00, h: 3.00,
  fontFace: FONT, valign: "top"
});

// === Content Slide ===
const content = pres.addSlide();
content.background = { color: theme.bg };
addHeader(content, {
  leftText: "Company x Partner",
  centerText: "Executive Summary",
  rightText: "March 2026",
  pageNum: 5
});
// Muted subtitle label
content.addText("Our understanding", {
  x: 0.80, y: 0.90, w: 5.00, h: 0.30,
  fontSize: 12, fontFace: FONT,
  color: text.muted
});
// Title with accent word
content.addText([
  { text: "How we understand the ", options: { color: text.title } },
  { text: "smart.AI", options: { color: text.accent } },
  { text: " mission", options: { color: text.title } }
], {
  x: 0.80, y: 1.20, w: 11.73, h: 0.80,
  fontSize: 32, fontFace: FONT
});
// Body text
content.addText("Body content goes here. Clean, well-spaced typography on a dark canvas.", {
  x: 0.80, y: 2.50, w: 11.73, h: 4.00,
  fontSize: 15, fontFace: FONT,
  color: text.body, valign: "top"
});
```
