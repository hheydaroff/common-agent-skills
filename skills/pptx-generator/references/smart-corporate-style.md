# smart Corporate Style Guide

> Auto-extracted from: `smart PPT Template 2.0..pptx`
> Font source: `~/Documents/fonts/for_smart_collection_complete/`
> Date: 2026-04-17

---

## Brand Colors

### Theme Color Scheme ("smart color theme")

| Key | Hex | Role | Usage |
|-----|-----|------|-------|
| **primary** | `141414` | dk1 — Primary text, darkest | Titles, headings, emphasis text |
| **secondary** | `969DA3` | dk2 — Secondary gray | Subtitles, secondary text, muted labels |
| **accent** | `D7E600` | accent1 — **Electrifying Lime** ⚡ | Visual highlight ONLY — lime line bar, subtle accents. **Use sparingly** |
| **light** | `E9E9E9` | accent6 — Light gray | Card backgrounds, separators, light fills |
| **bg** | `FFFFFF` | lt1 — White | Slide backgrounds |
| lt2 | `595959` | lt2 — Dark gray | Body text, descriptions, captions |

### Additional Accent Colors

| Hex | Theme Slot | Name | Usage |
|-----|-----------|------|-------|
| `ACE6B7` | accent2 | Soft green | Charts, secondary data series |
| `7DCFE3` | accent3 | Sky blue | Charts, tertiary data, info highlights |
| `EA9C98` | accent4 | Warm pink | Charts, quaternary data, soft warnings |
| `F7BF31` | accent5 | Amber / gold | Charts, quinary data, warm callouts |
| `E9E9E9` | accent6 | Light gray | Borders, separators, disabled states |

### Color Rules

- **Electrifying Lime (`D7E600`) is ONLY used SUBTLY** — thin accent bars, bottom line, small highlights. Never as large backgrounds or text color.
- Primary text: `141414` (near-black)
- Body/description text: `595959` (dark gray)
- Muted/secondary text: `969DA3` (medium gray)
- Backgrounds: `FFFFFF` (white)
- Hyperlinks: `141414` (same as text — no blue links)

### PptxGenJS Theme Object

```javascript
const theme = {
  primary: "141414",    // dk1 — titles, headings
  secondary: "969DA3",  // dk2 — subtitles, muted text
  accent: "D7E600",     // accent1 — electrifying lime (USE SPARINGLY)
  light: "E9E9E9",      // accent6 — light gray, separators
  bg: "FFFFFF"          // lt1 — white backgrounds
};

// Extended palette for charts and data visualization
const chartColors = ["D7E600", "ACE6B7", "7DCFE3", "EA9C98", "F7BF31", "969DA3"];

// Text colors (use these, not theme keys, for text)
const text = {
  title: "141414",      // primary titles
  body: "595959",       // body text, descriptions
  muted: "969DA3",      // captions, secondary info
  onLime: "141414"      // text on lime background (always dark)
};
```

---

## Typography

### Font Family — FOR smart Collection

The complete corporate font collection with exact font names for PptxGenJS `fontFace`:

| Family | Weight | fontFace (PptxGenJS) | PostScript Name | File | Installed |
|--------|--------|---------------------|-----------------|------|:---------:|
| **FOR smart Sans** | Regular | `"FOR smart Sans"` | FORsmartSans-Regular | FORsmartSans-Regular.otf | ✅ |
| **FOR smart Sans** | Bold | `"FOR smart Sans"` + `bold: true` | FORsmartSans-Bold | FORsmartSans-Bold.otf | ✅ |
| FOR smart Sans | Thin | `"FOR smart Sans Thin"` | FORsmartSans-Thin | FORsmartSans-Thin.otf | ❌ |
| **FOR smart Next** | Regular | `"FOR smart Next"` | FORsmartNext-Regular | FORsmartNext-Regular.otf | ✅ |
| **FOR smart Next** | Bold | `"FOR smart Next"` + `bold: true` | FORsmartNext-Bold | FORsmartNext-Bold.otf | ✅ |
| FOR smart Sans Con | Regular | `"FOR smart Sans Con"` | FORsmartSansCon-Regular | FORsmartSansCon-Regular.otf | ❌ |
| FOR smart Sans Con | Bold | `"FOR smart Sans Con"` + `bold: true` | FORsmartSansCon-Bold | FORsmartSansCon-Bold.otf | ❌ |
| FOR smart Sans Con | Thin | `"FOR smart Sans Con Thin"` | FORsmartSansCon-Thin | FORsmartSansCon-Thin.otf | ❌ |

**CJK (Chinese) Fonts — Tsanger YunHei:**

| Family | Weight | fontFace (PptxGenJS) | PostScript Name | File | Installed |
|--------|--------|---------------------|-----------------|------|:---------:|
| 仓耳云黑 W03 | Light / Body | `"仓耳云黑 W03"` | TsangerYunHei-W03 | TsangerYunHei-W03.ttf | ❌ |
| 仓耳云黑 W04 | Medium / Heading | `"仓耳云黑 W04"` | TsangerYunHei-W04 | TsangerYunHei-W04.ttf | ❌ |
| 仓耳云黑 W07 | Bold / Display | `"仓耳云黑 W07"` | TsangerYunHei-W07 | TsangerYunHei-W07.ttf | ❌ |

> **Font source**: `~/Documents/fonts/for_smart_collection_complete/`
>
> To install missing fonts: double-click the .otf/.ttf file or copy to `~/Library/Fonts/`

### Font Roles

| Role | Primary Font | Fallback | When to Use |
|------|-------------|----------|-------------|
| **Titles / Headings** | FOR smart Sans Bold | Arial Bold | All slide titles, section headers |
| **Body / Content** | FOR smart Sans Regular | Arial | Body text, descriptions, lists |
| **Display / Hero** | FOR smart Next Bold | Arial Black | Cover titles, large statements, marketing |
| **Thin / Subtle** | FOR smart Sans Thin | Arial Light | Decorative, watermarks, large background text |
| **Condensed** | FOR smart Sans Con | Arial Narrow | Dense data, tables, space-constrained areas |
| **CJK Body** | 仓耳云黑 W03 | Microsoft YaHei | Chinese body text |
| **CJK Headings** | 仓耳云黑 W04 | Microsoft YaHei Bold | Chinese titles |
| **CJK Bold / Display** | 仓耳云黑 W07 | SimHei | Chinese emphasis, large display |

### Font Rules

- **FOR smart Sans is the ONLY default EN font** — use it everywhere
- **FOR smart Next** is the display/hero font — use for cover titles and large statements only
- If the recipient doesn't have smart fonts installed, **Arial** is the safe fallback
- For PptxGenJS: use `"FOR smart Sans"` as fontFace when targeting machines with the font installed; use `"Arial"` for broad compatibility
- Page numbers: 10pt, Regular weight, text color (`141414`)
- **Never mix** FOR smart Sans and FOR smart Next in the same text block

### Size Scale

| Element | Size (pt) | Font | Weight |
|---------|----------|------|--------|
| Cover title | 50 | FOR smart Sans / Next | Bold |
| Content title | 28 | FOR smart Sans | Bold |
| Subtitle / meta | 16–20 | FOR smart Sans | Regular |
| Body text | 16–18 | FOR smart Sans | Regular |
| Caption / source | 10–12 | FOR smart Sans | Regular |
| Condensed data | 10–14 | FOR smart Sans Con | Regular |
| Page number | 10 | FOR smart Sans | Regular |

---

## Layout Standards

### Slide Dimensions

| Property | Value |
|----------|-------|
| **Layout** | LAYOUT_WIDE (13.33" × 7.5") |
| **EMU** | 12192000 × 6858000 |
| **Ratio** | 16:9 |

> ⚠️ **This template uses LAYOUT_WIDE (13.33" × 7.5"), NOT the standard LAYOUT_16x9 (10" × 5.625").** All position values below are in LAYOUT_WIDE coordinates. Set `pres.layout = 'LAYOUT_WIDE'` in PptxGenJS.

### Key Positions (inches)

| Element | x | y | w | h | Notes |
|---------|---|---|---|---|-------|
| **Left margin** | 1.31 | — | — | — | All content starts here |
| **Title area** | 1.31 | 0.62 | 10.87 | 0.75 | Content slide titles |
| **Content area** | 1.31 | 1.82 | 10.87 | 4.57 | Main content zone |
| **Two-col left** | 1.31 | 1.82 | 5.35 | 4.57 | Left column |
| **Two-col right** | 6.96 | 1.82 | 5.21 | 4.57 | Right column |
| **Two-col gap** | — | — | 0.30 | — | Between columns (6.66 → 6.96) |
| **Picture (left)** | 1.31 | 1.76 | 6.24 | 4.63 | Image placeholder |
| **Text beside pic** | 7.88 | 1.76 | 4.30 | 4.63 | Text next to image |
| **Page number** | 12.40 | 6.83 | 0.45 | 0.23 | Bottom-right |
| **Lime accent bar** | 0.0 | 7.28 | 13.33 | 0.22 | Full-width, bottom edge |
| **Cover title** | 1.31 | 4.86 | 10.24 | 1.55 | Below hero image |
| **Cover subtitle** | 1.31 | 6.48 | 2.21 | 0.67 | Name, dept, date |
| **Cover image** | 0.0 | 0.0 | 13.33 | 4.69 | Top ~63% of slide (Layout A) |
| **Agenda image** | 7.20 | 0.0 | 6.13 | 7.28 | Right half |
| **Agenda content** | 1.31 | 1.80 | 5.31 | 4.59 | Left half list |
| **End logo** | 5.63 | 2.35 | 2.06 | 2.80 | Centered |

### Margin & Spacing

| Property | Value |
|----------|-------|
| Left/right content margin | 1.31" |
| Right edge (content end) | 12.18" (1.31 + 10.87) |
| Title → content gap | 0.20" (title bottom 1.37 → content top 1.82) |
| Bottom safe zone | 6.39" (content area bottom) |
| Lime bar top | 7.28" |
| Page number baseline | 6.83" |

---

## Slide Type Patterns

### Cover Slides (3 variants)

| Variant | Background | Lime Bar | Logo |
|---------|-----------|----------|------|
| **A** — White logo | Hero image (top 63%), white below | No | White logo on image |
| **B** — Black logo | Hero image (top 63%), white below | No | Black logo on image |
| **C** — Lime line | Full-bleed hero image | Yes (bottom 0.22") | White logo on image |

**Cover layout**: Image fills top portion → title at y=4.86" → subtitle at y=6.48" (name, department, date)

### Agenda Slide

- Right half: full-height image (x=7.20, w=6.13)
- Left half: numbered list (x=1.31, w=5.31)
- Title floats on image: x=7.87, y=0.62, text="Agenda"
- Lime accent bar at bottom
- Page number bottom-right

### Content Slides

| Variant | Layout |
|---------|--------|
| **Title & Text** | Full-width title + content area |
| **Title & Text + lime** | Same + lime bottom bar |
| **Two Columns** | Title + two equal content columns |
| **Picture & Text** | Image left (6.24" wide) + text right (4.30" wide) |
| **Two Pictures & Texts** | Two image+text pairs |
| **Title Only** | Title bar, rest is custom |
| **Custom** | Blank canvas with margins |

### End Slides

- Centered smart logo (x=5.63, y=2.35, w=2.06, h=2.80)
- No other content
- Clean white background

---

## The Lime Accent Bar

The signature smart design element: a full-width `D7E600` (electrifying lime) rectangle at the very bottom of the slide.

```javascript
// Lime accent bar — use on slides that need the accent (not all)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 7.28, w: 13.33, h: 0.22,
  fill: { color: "D7E600" }
});
```

**Rules**:
- Use on title slides (variant C) and select content slides
- Do NOT use on every slide — it's an accent, not a default
- Do NOT use lime as text color or large background — only thin bars and small highlights

---

## Page Number

```javascript
// Page number — bottom right, subtle
slide.addText(String(slideIndex), {
  x: 12.40, y: 6.83, w: 0.45, h: 0.23,
  fontSize: 10, fontFace: "Arial",
  color: "141414",
  align: "right", valign: "middle"
});
```

---

## Embedded Media Assets

| File | Size | Purpose |
|------|------|---------|
| image6.png | 2,076 KB | Template preview / example |
| image7.png | 1,672 KB | Template preview / example |
| image8.png | 4,051 KB | Background / hero image |
| image9.png | 2,132 KB | Background / hero image |
| image15.jpeg | 576 KB | Example photo |
| image11.png, image13.png | ~3 KB each | Logo assets |

---

## Quick Start — PptxGenJS with smart Style

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';  // 13.33" × 7.50" — MUST use WIDE, not 16x9

const theme = {
  primary: "141414",
  secondary: "969DA3",
  accent: "D7E600",
  light: "E9E9E9",
  bg: "FFFFFF"
};

const text = {
  title: "141414",
  body: "595959",
  muted: "969DA3"
};

// Font configuration — toggle based on target audience
const FONT = {
  // Use these when recipients HAVE smart fonts installed:
  sans: "FOR smart Sans",       // primary — all titles & body
  next: "FOR smart Next",       // display — cover titles, hero text
  con:  "FOR smart Sans Con",   // condensed — tables, dense data
  cjk:  "仓耳云黑 W04",            // CJK headings
  cjkBody: "仓耳云黑 W03",         // CJK body

  // Use these for BROAD COMPATIBILITY (safe fallbacks):
  // sans: "Arial",
  // next: "Arial Black",
  // con:  "Arial Narrow",
  // cjk:  "Microsoft YaHei",
  // cjkBody: "Microsoft YaHei",
};

// Content slide with smart layout
const slide = pres.addSlide();
slide.background = { color: theme.bg };

// Title — uses FOR smart Sans Bold
slide.addText("Slide Title Here", {
  x: 1.31, y: 0.62, w: 10.87, h: 0.75,
  fontSize: 28, fontFace: FONT.sans,
  color: text.title, bold: true, margin: 0
});

// Content area — uses FOR smart Sans Regular
slide.addText("Body content goes here.", {
  x: 1.31, y: 1.82, w: 10.87, h: 4.57,
  fontSize: 16, fontFace: FONT.sans,
  color: text.body, valign: "top", margin: 0
});

// Lime accent bar (optional)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 7.28, w: 13.33, h: 0.22,
  fill: { color: theme.accent }
});

// Page number
slide.addText("1", {
  x: 12.40, y: 6.83, w: 0.45, h: 0.23,
  fontSize: 10, fontFace: "Arial",
  color: text.title, align: "right", valign: "middle"
});
```
