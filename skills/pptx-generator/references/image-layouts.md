# Image Layout Framework

## Overview

When slides include images, the layout must match the image's aspect ratio to avoid awkward stretching, cropping, or wasted space. This reference provides concrete rules for mapping image dimensions to slide layouts.

---

## Aspect Ratio → Layout Mapping

### Landscape Canvas (16:9)

| Image Ratio | Category | Recommended Layout | Example |
|-------------|----------|-------------------|---------|
| > 2.0 | Ultra-wide (panoramic) | Top strip / bottom strip, full-width | Banner photos, panoramas |
| 1.5–2.0 | Wide landscape | Top-bottom split (image top, text bottom) | Landscape photos, screenshots |
| 1.2–1.5 | Standard landscape | Left-right split (image one side, text other) | Product shots, charts |
| 0.8–1.2 | Square | Left-right split (equal columns) | Social media images, logos |
| 0.5–0.8 | Portrait | Left-right split (image left, narrow; text right, wide) | Phone screenshots, portraits |
| < 0.5 | Tall portrait | Sidebar placement, or paired with text column | Infographics, mobile UI |

**Core principle**: The layout container's aspect ratio must closely match the image's original ratio. Never force a wide image into a square container or a portrait image into a narrow horizontal strip.

---

## Layout Templates

### Full-Bleed Background (any ratio, with overlay)

Best for: Cover slides, section dividers, atmosphere slides.

```javascript
// Image fills entire slide
slide.addImage({
  path: "images/bg.jpg",
  x: 0, y: 0, w: 10, h: 5.625,
  sizing: { type: "cover", w: 10, h: 5.625 }
});

// Gradient overlay for text readability
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: theme.primary, transparency: 40 }
});

// Text on top
slide.addText("Title", {
  x: 0.6, y: 2, w: 6, h: 1.2,
  fontSize: 48, color: "FFFFFF", bold: true
});
```

### Left-Right Split (landscape/square images)

Best for: Content slides with one image.

```javascript
// Image on left (45% width)
slide.addImage({
  path: "images/photo.jpg",
  x: 0.4, y: 0.8, w: 4.2, h: 3.8,
  sizing: { type: "cover", w: 4.2, h: 3.8 }
});

// Text on right (55% width)
slide.addText("Section Title", {
  x: 5.2, y: 0.8, w: 4.4, h: 0.8,
  fontSize: 28, bold: true, color: theme.primary
});

slide.addText("Description text...", {
  x: 5.2, y: 1.8, w: 4.4, h: 2.8,
  fontSize: 14, color: theme.secondary, valign: "top"
});
```

### Top-Bottom Split (wide images)

Best for: Wide screenshots, panoramic photos.

```javascript
// Image on top (60% height)
slide.addImage({
  path: "images/wide-shot.jpg",
  x: 0.4, y: 0.4, w: 9.2, h: 3.0,
  sizing: { type: "cover", w: 9.2, h: 3.0 }
});

// Text below
slide.addText("Caption or description", {
  x: 0.4, y: 3.7, w: 9.2, h: 1.5,
  fontSize: 14, color: theme.secondary, valign: "top"
});
```

### Half-Bleed (image flush to edge)

Best for: Modern, magazine-style layouts.

```javascript
// Image flush to right edge
slide.addImage({
  path: "images/hero.jpg",
  x: 5, y: 0, w: 5, h: 5.625,
  sizing: { type: "cover", w: 5, h: 5.625 }
});

// Content on left with padding
slide.addText("Title", {
  x: 0.6, y: 1.5, w: 4, h: 1,
  fontSize: 36, bold: true, color: theme.primary
});
```

### Gallery Grid (multiple images)

Best for: Portfolio, team photos, product showcase.

```javascript
// 2×2 grid with consistent spacing
const gap = 0.2;
const imgW = 4.3, imgH = 2.3;
const positions = [
  { x: 0.5, y: 0.8 },
  { x: 5.2, y: 0.8 },
  { x: 0.5, y: 3.3 },
  { x: 5.2, y: 3.3 }
];

images.forEach((img, i) => {
  slide.addImage({
    path: img.path,
    x: positions[i].x, y: positions[i].y,
    w: imgW, h: imgH,
    sizing: { type: "cover", w: imgW, h: imgH }
  });
});
```

---

## Image Sizing Modes

| Mode | Behavior | When to Use |
|------|----------|-------------|
| `contain` | Fit inside box, preserve ratio, may leave gaps | Icons, logos, diagrams |
| `cover` | Fill box, preserve ratio, may crop edges | Photos, backgrounds |
| `crop` | Cut specific portion of image | Focusing on detail |

**Default**: Use `cover` for photos, `contain` for diagrams/logos.

---

## Rounded Image Frames

```javascript
// Image inside a rounded container
// First: rounded background
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 0.8, w: 4, h: 3,
  fill: { color: "FFFFFF" },
  rectRadius: 0.15
});

// Then: image with rounding
slide.addImage({
  path: "images/photo.jpg",
  x: 0.5, y: 0.8, w: 4, h: 3,
  sizing: { type: "cover", w: 4, h: 3 },
  rounding: true  // Circular crop (use for avatars)
});
```

---

## Placeholder Images

When images aren't yet available, create visual placeholders:

```javascript
// Dashed border placeholder
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 4, h: 3,
  fill: { color: theme.bg },
  line: { color: theme.accent, width: 1.5, dashType: "dash" }
});

slide.addText("📷 Product Screenshot\n1920×1080", {
  x: 0.5, y: 0.8, w: 4, h: 3,
  fontSize: 12, color: theme.accent,
  align: "center", valign: "middle"
});
```

---

## Quality Rules

1. **Never stretch** — always use `sizing` with `cover` or `contain`
2. **Never distort** — image w/h ratio should approximate the container's w/h ratio
3. **Consistent frames** — if one image has rounded corners, all images on that slide should
4. **Credit sources** — add small caption text below images when source attribution is needed
5. **Resolution** — use images ≥ 1920px wide for full-bleed; ≥ 800px for half-slide
