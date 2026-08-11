
# Extract PPTX Theme

## When to Use

- User provides a .pptx template file and wants to extract a theme from it
- Creating a new presentation theme from an existing corporate template
- Reverse-engineering a design system from PowerPoint
- Cataloging assets (photos, icons, logos) from a template for reuse

## Prerequisites

- Python 3 (for XML parsing)
- macOS `sips` command (for image dimension verification, optional)
- Target PPTX file accessible on local filesystem

## Steps

### 1. Extract the PPTX (it's a ZIP)

```bash
mkdir -p /tmp/pptx-extract
unzip -o "path/to/template.pptx" -d /tmp/pptx-extract
```

### 2. Parse Theme XML for Color Scheme

```bash
# Usually in ppt/theme/theme1.xml (may have theme2.xml, theme3.xml for variants)
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/pptx-extract/ppt/theme/theme1.xml')
root = tree.getroot()
# Get theme name
print(f'Theme: {root.attrib.get(\"name\")}')
# Get color scheme
clrScheme = root.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}clrScheme')
print(f'Scheme: {clrScheme.get(\"name\")}')
for child in clrScheme:
    tag = child.tag.split('}')[1]
    for color in child:
        val = color.get('val') or color.get('lastClr')
        print(f'  {tag}: #{val}')
"
```

**Color roles to extract:**
| XML Tag | Role |
|---------|------|
| dk1 | Dark text / dark background |
| lt1 | Light text / light background |
| dk2 | Secondary dark |
| lt2 | Secondary light |
| accent1-6 | Brand accent colors |
| hlink | Hyperlink color |
| folHlink | Followed hyperlink |

### 3. Parse Font Scheme

```python
fontScheme = root.find('.//{...}fontScheme')
majorFont = fontScheme.find('{...}majorFont/{...}latin')  # Heading font
minorFont = fontScheme.find('{...}minorFont/{...}latin')  # Body font
```

**Note:** Brand fonts (e.g., "FOR smart Next") need web-safe fallbacks (Montserrat, Inter, Arial).

### 4. Analyze Slide Master for Layout Grid

```python
# ppt/slideMasters/slideMaster1.xml — contains title, body, footer placeholders
# Key measurements (in EMU, divide by 914400 for inches):
# - Title position & size
# - Body/content area
# - Footer bar (if present)
# - Page number position
```

**Critical elements to find:**
- Master background color (often bg1 = scheme reference)
- Footer/decoration shapes (brand signature elements)
- Placeholder positions (title, body, slide number)

### 5. Catalog All Slide Layouts

```python
# ppt/slideLayouts/slideLayout*.xml — check each for:
# - Layout name (cSld[@name] attribute)
# - Background override (explicit bg vs inherited)
# - Placeholder types and positions
```

### 6. Extract & Categorize Images

```bash
# Count by type
find /tmp/pptx-extract/ppt/media -name "*.jpg" -o -name "*.jpeg" | wc -l  # Photos
find /tmp/pptx-extract/ppt/media -name "*.png" | wc -l                     # PNGs
find /tmp/pptx-extract/ppt/media -name "*.svg" | wc -l                     # Vectors
find /tmp/pptx-extract/ppt/media -name "*.emf" | wc -l                     # Windows vectors
```

**Categorization rules:**
| File type | Size threshold | Category |
|-----------|---------------|----------|
| JPG/JPEG | >200KB | Photos (hero images) |
| JPG/JPEG | <200KB | Small photos/thumbnails |
| PNG | >100KB | Illustrations/screenshots |
| PNG | 96×96px | Icon fallback (paired with SVG) |
| SVG | viewBox="0 0 24 24" | Icons |
| SVG | >10KB | Graphics/illustrations |
| EMF | >50KB | Vector graphics (maps, logos) |
| EMF | <5KB | Empty placeholders |

### 7. Identify Light vs Dark Slides

Check which slides override the master background:
```python
# If master bg1 = #FFFFFF → template defaults to LIGHT
# Slides with explicit #141414/#000000 fills = dark variant overrides
# If master bg1 = #141414 → template defaults to DARK
```

### 8. Create the Style Guide

Write `style-guide.md` with sections:
1. Brand Identity (name, style, tone, target)
2. Color Palette (primary, accent, structural)
3. Typography (fonts, size scale, color rules)
4. Layout System (grid, zones, margins)
5. Layout Patterns (per layout type)
6. Visual Elements (cards, badges, dividers, bullets)
7. Image Guidelines (photo style, placement, dimensions)
8. Shadows & Effects (or lack thereof)
9. Accessibility (contrast ratios)
10. Design Tokens (JSON for code consumption)
11. Example Slide Recipes (concrete position/size values)

### 9. Register the Theme

Add entry to the theme registry (e.g., `shared/themes.ts`) with:
- `id`: kebab-case identifier
- `name`: Display name
- `description`: Short tagline
- `preview`: Object with bg, accent, text, secondary hex colors
- `prompt`: Full style guide injected into LLM context

### 10. Create Example Deck JSON

Produce a 3-5 slide example showing:
- Title slide
- Chapter divider
- 4-card grid (signature layout)
- Content + chart
- Two-column layout

Validate all elements fit within slide bounds.

## Gotchas & Lessons Learned

1. **EMU to inches**: Divide by 914400. Coordinates in PPTX XML are in EMUs.
2. **bg1 ≠ always white**: Check `lt1` in the color scheme — that's what `bg1` resolves to.
3. **Multiple themes**: PPTX can contain 2-3 theme XMLs for light/dark variants.
4. **Logo EMFs are often empty**: Tiny (<1KB) EMFs are usually placeholder slots, not actual logos.
5. **96×96 PNGs**: These are icon fallback images paired with SVGs (for older PPT compatibility).
6. **Inherited positions**: Layouts inherit placeholder positions from the master — check master first.
7. **photo dimensions via JPEG headers are unreliable**: Use `sips` on macOS for accurate dimensions.
8. **Font fallbacks matter**: Brand fonts won't be installed; always provide web-safe alternatives.
9. **Footer bar is often a brand signature**: A rounded rect at the bottom present on ALL content slides.
10. **One accent highlight per slide**: Templates often use one "hero" colored card among neutral ones.

## Output Directory Structure

```
references/themes/<theme-name>/
├── style-guide.md              # Complete style guide
├── example-deck.json           # Reference slide examples
└── assets/
    ├── photos/                 # Hero photos (>200KB JPGs)
    ├── icons/                  # 24×24 SVG line icons
    ├── graphics/               # Large vector illustrations
    └── logos/                  # Brand marks (dark + white variants)
```
