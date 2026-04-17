# Corporate Style Extraction

## Overview

Extract a reusable corporate style guide from an existing template PPTX. This produces a `corporate-style.md` file that captures your brand's colors, fonts, spacing, and layout patterns — which then overrides the default design system for all future presentations.

**When to use**: The user provides a corporate template PPTX (or brand guidelines) and wants all future decks to match their brand identity.

**Pipeline**: `Template PPTX → Unpack → Analyze XML → Generate corporate-style.md → Use in Strategist phase`

---

## Step 1: Unpack the Template

```bash
cp /path/to/corporate-template.pptx template.pptx
python -m markitdown template.pptx > template-content.md
```

Then unpack the PPTX to access raw XML:

```python
import zipfile, os

with zipfile.ZipFile('template.pptx', 'r') as z:
    z.extractall('unpacked')
```

---

## Step 2: Extract Theme Colors

Read the theme file to get the corporate color palette:

```bash
# Theme file contains all master colors
cat unpacked/ppt/theme/theme1.xml
```

Look for these elements in the theme XML:

| XML Element | Purpose | Maps to Theme Key |
|------------|---------|-------------------|
| `<a:dk1>` | Dark 1 (usually black/near-black) | `primary` |
| `<a:dk2>` | Dark 2 (dark accent) | `secondary` |
| `<a:lt1>` | Light 1 (usually white) | `bg` |
| `<a:lt2>` | Light 2 (light gray) | `light` |
| `<a:accent1>` | Primary accent | `accent` |
| `<a:accent2>` – `<a:accent6>` | Additional accents | Document as extras |

Extract hex values from `<a:srgbClr val="XXXXXX"/>` or `<a:sysClr val="..." lastClr="XXXXXX"/>`.

Also check the slide master for additional colors used in shapes:

```bash
cat unpacked/ppt/slideMasters/slideMaster1.xml | grep -o 'srgbClr val="[^"]*"' | sort -u
```

---

## Step 3: Extract Fonts

```bash
# From theme
grep -o 'typeface="[^"]*"' unpacked/ppt/theme/theme1.xml | sort -u
```

Look for:

| XML Element | Purpose |
|------------|---------|
| `<a:majorFont>` → `<a:latin typeface="..."/>` | Heading / title font |
| `<a:minorFont>` → `<a:latin typeface="..."/>` | Body / content font |
| `<a:ea typeface="..."/>` | East Asian font (Chinese/Japanese/Korean) |

Also scan slide content for actually used fonts:

```bash
grep -rho 'typeface="[^"]*"' unpacked/ppt/slides/ | sort | uniq -c | sort -rn
```

---

## Step 4: Extract Layout Patterns

Analyze the slide layouts to understand recurring structures:

```bash
# List all layouts
ls unpacked/ppt/slideLayouts/

# Check what each layout contains
for f in unpacked/ppt/slideLayouts/*.xml; do
  echo "=== $(basename $f) ==="
  grep -o 'type="[^"]*"' "$f" | head -5
  grep -o '<p:sp>' "$f" | wc -l | xargs echo "  Shapes:"
done
```

Document these patterns:
- **Title slide layout** — title position, subtitle position, background style
- **Content layout** — title bar height, content area boundaries, margin sizes
- **Section divider** — accent elements, number placement
- **Two-column** — column widths, gap between columns

### Extract Spacing and Positions

```bash
# Get common positions (EMU → inches: divide by 914400)
grep -o 'x="[0-9]*" y="[0-9]*"' unpacked/ppt/slideLayouts/slideLayout1.xml
```

Convert EMU to inches: `inches = EMU / 914400`

---

## Step 5: Extract Logo and Brand Assets

```bash
# Find embedded images
ls unpacked/ppt/media/

# Check which slides reference which images
grep -l "image1\|image2\|logo" unpacked/ppt/slides/_rels/*.rels
```

Note logo placement (position, size) from the slide master or layouts — logos placed in the slide master appear on every slide.

---

## Step 6: Generate Corporate Style Guide

Produce `corporate-style.md` with all extracted values:

```markdown
# Corporate Style Guide — [Company Name]

> Auto-extracted from: corporate-template.pptx
> Date: YYYY-MM-DD

## Brand Colors

| Key | Hex | Usage | Source |
|-----|-----|-------|--------|
| **primary** | `XXXXXX` | Titles, emphasis | theme dk1 |
| **secondary** | `XXXXXX` | Body text, subtitles | theme dk2 |
| **accent** | `XXXXXX` | Highlights, CTAs, links | theme accent1 |
| **light** | `XXXXXX` | Light backgrounds, cards | theme lt2 |
| **bg** | `XXXXXX` | Slide backgrounds | theme lt1 |
| accent2 | `XXXXXX` | Secondary accent | theme accent2 |
| accent3 | `XXXXXX` | Tertiary accent | theme accent3 |

### Additional Colors Found in Slides
| Hex | Where Used | Suggested Purpose |
|-----|-----------|-------------------|
| `XXXXXX` | Slide 1 header bar | Header/footer bars |
| `XXXXXX` | Slide 3 chart | Chart color 1 |

## Typography

| Role | Font | Size (pt) | Weight | Source |
|------|------|-----------|--------|--------|
| **Title** | [Font Name] | XX | Bold | majorFont |
| **Body** | [Font Name] | XX | Regular | minorFont |
| **CJK** | [Font Name] | — | — | ea typeface |

## Layout Standards

| Element | Value | Notes |
|---------|-------|-------|
| Slide dimensions | 10" × 5.625" | LAYOUT_16x9 |
| Page margin (left) | X.X" | From content edge |
| Page margin (top) | X.X" | Title top edge |
| Title bar height | X.X" | If title bar exists |
| Content area | x: X.X", y: X.X", w: X.X", h: X.X" | Main content zone |
| Footer area | y: X.X" | Bottom strip |
| Logo position | x: X.X", y: X.X", w: X.X", h: X.X" | From slide master |

## Visual Style

| Property | Value | Notes |
|----------|-------|-------|
| Corner radius | X.X" | From shapes in template |
| Shadow style | [described] | If shadows present |
| Line weights | X pt | From separators/borders |
| Accent bar width | X.X" | If left-accent bars used |

## Logo & Brand Assets

| Asset | File | Position | Size |
|-------|------|----------|------|
| Primary logo | media/imageX.png | x: X.X", y: X.X" | w: X.X", h: X.X" |

## Theme Object (for PptxGenJS)

```javascript
const theme = {
  primary: "XXXXXX",
  secondary: "XXXXXX",
  accent: "XXXXXX",
  light: "XXXXXX",
  bg: "XXXXXX"
};
```

## Slide Type Patterns

### Cover Slide
- Background: [solid color / image / gradient]
- Title: [position, size, font]
- Subtitle: [position, size, font]
- Logo: [position]

### Content Slide
- Title bar: [position, background color]
- Content area: [boundaries]
- Footer: [elements, position]

### Section Divider
- Style: [full-color bg / accent block / etc.]
- Number style: [large transparent / circled / none]
```

---

## Step 7: Use in Future Presentations

Once `corporate-style.md` exists, the Strategist phase uses it instead of choosing from the default palettes:

1. **Skip color selection** — use brand colors from corporate-style.md
2. **Skip font selection** — use brand fonts from corporate-style.md
3. **Apply layout standards** — margins, positions, logo placement from corporate-style.md
4. **Apply visual style** — corner radius, shadows, line weights from corporate-style.md

In the design spec, reference the corporate style:

```markdown
## IV. Color Scheme
> Using corporate style guide: corporate-style.md
- Primary: [from guide]
- Secondary: [from guide]
...
```

The theme object in `compile.js` uses the extracted values directly.

---

## Quick Extraction Script

For a fast extraction, run this all-in-one analysis:

```python
import zipfile, re, os
from collections import Counter

def extract_style(pptx_path):
    with zipfile.ZipFile(pptx_path, 'r') as z:
        # Colors from theme
        theme = z.read('ppt/theme/theme1.xml').decode('utf-8')
        colors = re.findall(r'srgbClr val="([A-Fa-f0-9]{6})"', theme)
        print("=== Theme Colors ===")
        for c in dict.fromkeys(colors):
            print(f"  #{c}")

        # Fonts from theme
        fonts = re.findall(r'typeface="([^"]+)"', theme)
        print("\n=== Theme Fonts ===")
        for f in dict.fromkeys(fonts):
            print(f"  {f}")

        # All colors used across slides
        all_colors = Counter()
        for name in z.namelist():
            if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                content = z.read(name).decode('utf-8')
                slide_colors = re.findall(r'srgbClr val="([A-Fa-f0-9]{6})"', content)
                all_colors.update(slide_colors)

        print("\n=== Most Used Colors (across all slides) ===")
        for color, count in all_colors.most_common(15):
            print(f"  #{color}  ({count}x)")

        # Fonts across slides
        all_fonts = Counter()
        for name in z.namelist():
            if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                content = z.read(name).decode('utf-8')
                slide_fonts = re.findall(r'typeface="([^"]+)"', content)
                all_fonts.update(slide_fonts)

        print("\n=== Most Used Fonts (across all slides) ===")
        for font, count in all_fonts.most_common(10):
            print(f"  {font}  ({count}x)")

        # Media files
        media = [n for n in z.namelist() if n.startswith('ppt/media/')]
        if media:
            print("\n=== Embedded Media ===")
            for m in media:
                info = z.getinfo(m)
                print(f"  {os.path.basename(m)}  ({info.file_size // 1024} KB)")

extract_style('template.pptx')
```

---

## Both Approaches Supported

| Approach | When to Use | How |
|----------|-------------|-----|
| **A) Provide template PPTX** | You have an existing branded deck | Follow this guide to extract → `corporate-style.md` |
| **B) Provide style rules directly** | You have brand guidelines (PDF/doc/text) | Skip extraction, write `corporate-style.md` manually from the provided specs |

Either way, the output is the same `corporate-style.md` file that feeds into the Strategist phase.
