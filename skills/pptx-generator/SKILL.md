---
name: pptx-generator
description: "Generate, edit, and read PowerPoint presentations. Create from scratch with PptxGenJS (cover, TOC, content, section divider, summary slides), edit existing PPTX via XML workflows, or extract text with markitdown. Triggers: PPT, PPTX, PowerPoint, presentation, slide, deck, slides."
license: MIT
metadata:
  version: "2.0"
  category: productivity
  sources:
    - https://gitbrent.github.io/PptxGenJS/
    - https://github.com/microsoft/markitdown
---

# PPTX Generator & Editor

## Overview

This skill handles all PowerPoint tasks: reading/analyzing existing presentations, editing template-based decks via XML manipulation, and creating presentations from scratch using PptxGenJS. It includes a complete design system (color palettes, fonts, style recipes), structured planning workflow, speaker notes, and detailed guidance for every slide type.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Extract corporate style from template | See [Corporate Style Extraction](references/corporate-style.md) |
| Edit or create from template | See [Editing Presentations](references/editing.md) |
| Create from scratch | See [Creating from Scratch](#creating-from-scratch-workflow) below |

| Item | Value |
|------|-------|
| **Dimensions** | 10" x 5.625" (LAYOUT_16x9) |
| **Colors** | 6-char hex without # (e.g., `"FF0000"`) |
| **English font** | Arial (default), or approved alternatives |
| **Chinese font** | Microsoft YaHei |
| **Page badge position** | x: 9.3", y: 5.1" |
| **Theme keys** | `primary`, `secondary`, `accent`, `light`, `bg` |
| **Shapes** | RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE |
| **Charts** | BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR |

## Reference Files

| File | Contents |
|------|----------|
| [strategist.md](references/strategist.md) | **Planning phase** — Eight Confirmations, design spec, industry colors, content strategy styles |
| [slide-types.md](references/slide-types.md) | 5 slide page types (Cover, TOC, Section Divider, Content, Summary) + additional layout patterns |
| [design-system.md](references/design-system.md) | Color palettes, industry lookup, typography presets, font reference, style recipes |
| [visual-effects.md](references/visual-effects.md) | Shadows, gradient overlays, decorative elements, frosted cards |
| [image-layouts.md](references/image-layouts.md) | Aspect ratio → layout mapping, image sizing modes, gallery grids, placeholders |
| [speaker-notes.md](references/speaker-notes.md) | Speaker notes generation framework, stage markers, style-specific examples |
| [source-intake.md](references/source-intake.md) | Source document conversion (PDF/DOCX/URL → Markdown), content analysis |
| [corporate-style.md](references/corporate-style.md) | Extract corporate style guide from template PPTX — colors, fonts, layouts, logo |
| [editing.md](references/editing.md) | Template-based editing workflow, XML manipulation, formatting rules, common pitfalls |
| [pitfalls.md](references/pitfalls.md) | QA process, common mistakes, critical PptxGenJS pitfalls |
| [pptxgenjs.md](references/pptxgenjs.md) | Complete PptxGenJS API reference |

---

## Reading Content

```bash
# Text extraction (supports PDF, DOCX, PPTX, XLSX, HTML, URLs)
python -m markitdown presentation.pptx
```

---

## Creating from Scratch — Workflow

**Use when no template or reference presentation is available.**

**Pipeline**: `Source Intake → Strategist (plan) → Slide Generation → Speaker Notes → QA`

### Step 1: Source Content Intake

When the user provides source documents (PDF, DOCX, URL, etc.), convert them to Markdown first. See [Source Intake](references/source-intake.md) for details.

```bash
python -m markitdown source.pdf > source_content.md
```

If the user provides content directly in conversation, skip conversion and proceed to Step 2.

### Step 1b: Corporate Style Extraction (Optional)

If the user provides a corporate template PPTX or brand guidelines, extract a reusable style guide **before** the Strategist phase. See [Corporate Style Extraction](references/corporate-style.md).

This produces `corporate-style.md` which overrides the default design system — the Strategist phase will use brand colors, fonts, and layout standards instead of choosing from generic palettes.

### Step 2: Strategist Phase — Planning & Design Spec

**Read [references/strategist.md](references/strategist.md) before proceeding.**

If `corporate-style.md` exists, use it as the design foundation — skip color/font/style selection in the Eight Confirmations and use the brand values instead.

This is a **BLOCKING** step — present recommendations and wait for user confirmation.

Complete the **Eight Confirmations**:
1. Canvas format (16:9, 4:3, etc.)
2. Page count range
3. Target audience & key information
4. Content strategy style (General / Consulting / Executive)
5. Color scheme (use [Industry Color Reference](references/strategist.md#industry-color-reference))
6. Icon usage approach
7. Typography plan (preset + size baseline)
8. Image usage approach

**Output**: `slides/design_spec.md` — the single source of truth for all subsequent generation.

### Step 3: Select Visual Style

Use the [Style Recipes](references/design-system.md#style-recipes) to choose a visual style (Sharp, Soft, Rounded, or Pill) matching the confirmed tone. This determines corner radius, spacing, and component sizing.

### Step 4: Plan Slide Outline

Classify **every slide** as exactly one of the [5 page types](references/slide-types.md). Plan the content and layout for each slide. Ensure visual variety — do NOT repeat the same layout across slides.

For slides with images, consult the [Image Layout Framework](references/image-layouts.md) to match image aspect ratios to appropriate layouts.

For slides needing visual polish, consult the [Visual Effects Library](references/visual-effects.md) for shadow, overlay, and decorative techniques.

### Step 5: Generate Slide JS Files

Create one JS file per slide in `slides/` directory. Each file must export a synchronous `createSlide(pres, theme)` function. Follow the [Slide Output Format](#slide-output-format) and the type-specific guidance in [slide-types.md](references/slide-types.md). Generate up to 5 slides concurrently using subagents if available.

**Tell each subagent:**
1. File naming: `slides/slide-01.js`, `slides/slide-02.js`, etc.
2. Images go in: `slides/imgs/`
3. Final PPTX goes in: `slides/output/`
4. Dimensions: 10" x 5.625" (LAYOUT_16x9)
5. Fonts: Chinese = Microsoft YaHei, English = Arial (or approved alternative from design spec)
6. Colors: 6-char hex without # (e.g. `"FF0000"`)
7. Must use the theme object contract (see [Theme Object Contract](#theme-object-contract))
8. Must follow the [PptxGenJS API reference](references/pptxgenjs.md)
9. Must follow the [Visual Effects Library](references/visual-effects.md) for shadows and overlays
10. Use factory functions for shadow objects — never reuse option objects across calls

### Step 6: Compile into Final PPTX

Create `slides/compile.js` to combine all slide modules:

```javascript
// slides/compile.js
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const theme = {
  primary: "22223b",    // dark color for backgrounds/text
  secondary: "4a4e69",  // secondary accent
  accent: "9a8c98",     // highlight color
  light: "c9ada7",      // light accent
  bg: "f2e9e4"          // background color
};

for (let i = 1; i <= 12; i++) {  // adjust count as needed
  const num = String(i).padStart(2, '0');
  const slideModule = require(`./slide-${num}.js`);
  slideModule.createSlide(pres, theme);
}

pres.writeFile({ fileName: './output/presentation.pptx' });
```

Run with: `cd slides && node compile.js`

### Step 7: Generate Speaker Notes

**Read [references/speaker-notes.md](references/speaker-notes.md) before proceeding.**

After all slides are compiled:

1. Generate `slides/notes/total.md` — master document with notes for all slides
2. Split into per-slide files: `slides/notes/slide-01.md`, etc.
3. Optionally embed notes into slides using `slide.addNotes("...")`

Notes should include:
- Transition text (every slide after cover)
- Script text (2–5 sentences)
- Key points: ① ② ③
- Duration estimate

Adapt the notes style to match the confirmed Content Strategy Style (General / Consulting / Executive).

### Step 8: QA (Required)

See [QA Process](references/pitfalls.md#qa-process).

### Output Structure

```
slides/
├── design_spec.md       # Design specification (from Strategist phase)
├── slide-01.js          # Slide modules
├── slide-02.js
├── ...
├── compile.js           # Compilation script
├── imgs/                # Images used in slides
├── notes/               # Speaker notes
│   ├── total.md         # Master document
│   ├── slide-01.md      # Per-slide notes
│   └── ...
└── output/              # Final artifacts
    └── presentation.pptx
```

---

## Slide Output Format

Each slide is a **complete, runnable JS file**:

```javascript
// slide-01.js
const pptxgen = require("pptxgenjs");

const slideConfig = {
  type: 'cover',
  index: 1,
  title: 'Presentation Title'
};

// MUST be synchronous (not async)
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addText(slideConfig.title, {
    x: 0.5, y: 2, w: 9, h: 1.2,
    fontSize: 48, fontFace: "Arial",
    color: theme.primary, bold: true, align: "center"
  });

  // Speaker notes (optional — can also be added from notes/ files)
  slide.addNotes("Welcome everyone. Today we'll explore...");

  return slide;
}

// Standalone preview - use slide-specific filename
if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_16x9';
  const theme = {
    primary: "22223b",
    secondary: "4a4e69",
    accent: "9a8c98",
    light: "c9ada7",
    bg: "f2e9e4"
  };
  createSlide(pres, theme);
  pres.writeFile({ fileName: "slide-01-preview.pptx" });
}

module.exports = { createSlide, slideConfig };
```

---

## Theme Object Contract (MANDATORY)

The compile script passes a theme object with these **exact keys**:

| Key | Purpose | Example |
|-----|---------|---------|
| `theme.primary` | Darkest color, titles | `"22223b"` |
| `theme.secondary` | Dark accent, body text | `"4a4e69"` |
| `theme.accent` | Mid-tone accent | `"9a8c98"` |
| `theme.light` | Light accent | `"c9ada7"` |
| `theme.bg` | Background color | `"f2e9e4"` |

**NEVER use other key names** like `background`, `text`, `muted`, `darkest`, `lightest`.

---

## Page Number Badge (REQUIRED)

All slides **except Cover Page** MUST include a page number badge in the bottom-right corner.

- **Position**: x: 9.3", y: 5.1"
- Show current number only (e.g. `3` or `03`), NOT "3/12"
- Use palette colors, keep subtle

### Circle Badge (Default)

```javascript
slide.addShape(pres.shapes.OVAL, {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fill: { color: theme.accent }
});
slide.addText("3", {
  x: 9.3, y: 5.1, w: 0.4, h: 0.4,
  fontSize: 12, fontFace: "Arial",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

### Pill Badge

```javascript
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 9.1, y: 5.15, w: 0.6, h: 0.35,
  fill: { color: theme.accent },
  rectRadius: 0.15
});
slide.addText("03", {
  x: 9.1, y: 5.15, w: 0.6, h: 0.35,
  fontSize: 11, fontFace: "Arial",
  color: "FFFFFF", bold: true,
  align: "center", valign: "middle"
});
```

---

## Dependencies

- `pip install "markitdown[all]"` — text extraction (PDF, DOCX, PPTX, XLSX, HTML)
- `npm install -g pptxgenjs` — creating from scratch
- `npm install -g react-icons react react-dom sharp` — icons (optional)
