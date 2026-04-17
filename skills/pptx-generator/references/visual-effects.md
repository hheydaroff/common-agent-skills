# Visual Effects Library

## Overview

Elevate slides beyond flat shapes with shadows, overlays, and gradient effects. All techniques below are compatible with PptxGenJS and produce reliable output in PowerPoint.

---

## Shadows

### Standard Card Shadow

Best for: Content cards, panels, elevated elements.

```javascript
const makeCardShadow = () => ({
  type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15
});

slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 4, h: 2.5,
  fill: { color: "FFFFFF" },
  shadow: makeCardShadow()
});
```

### Subtle Lift Shadow

Best for: Minimal elevation, badges, tags.

```javascript
const makeLiftShadow = () => ({
  type: "outer", color: "000000", blur: 3, offset: 1, angle: 135, opacity: 0.08
});
```

### Deep Shadow

Best for: Hero cards, featured content, call-to-action buttons.

```javascript
const makeDeepShadow = () => ({
  type: "outer", color: "000000", blur: 12, offset: 4, angle: 135, opacity: 0.20
});
```

### Colored Shadow

Best for: Accent elements, branded cards, CTA buttons. Use the element's own color family.

```javascript
// Shadow matches the card's accent color
const makeColoredShadow = (color) => ({
  type: "outer", color: color, blur: 8, offset: 3, angle: 135, opacity: 0.25
});

slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 3.5, y: 3.8, w: 3, h: 0.6,
  fill: { color: theme.accent },
  rectRadius: 0.15,
  shadow: makeColoredShadow(theme.accent)
});
```

### Upward Shadow (for footer bars)

Best for: Bottom bars, footer elements, sticky panels.

```javascript
const makeUpwardShadow = () => ({
  type: "outer", color: "000000", blur: 6, offset: 2, angle: 270, opacity: 0.12
});
```

> **Never use negative offset values** — they corrupt the file. Use `angle: 270` for upward shadows.

### Shadow Quick Reference

| Scenario | blur | offset | opacity | angle |
|----------|------|--------|---------|-------|
| Subtle lift | 3 | 1 | 0.08 | 135 |
| Standard card | 6 | 2 | 0.15 | 135 |
| Deep/hero | 12 | 4 | 0.20 | 135 |
| Colored accent | 8 | 3 | 0.25 | 135 |
| Upward (footer) | 6 | 2 | 0.12 | 270 |

> **Always use factory functions** (e.g., `makeShadow()`) — never share shadow objects between calls. PptxGenJS mutates options in-place.

---

## Gradient Overlays (via layered shapes)

PptxGenJS doesn't support native gradient fills, but you can simulate them with layered semi-transparent shapes.

### Dark Overlay on Images

Best for: Text readability over photos.

```javascript
// Background image
slide.addImage({
  path: "images/bg.jpg", x: 0, y: 0, w: 10, h: 5.625,
  sizing: { type: "cover", w: 10, h: 5.625 }
});

// Dark overlay (60% opacity)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "000000", transparency: 40 }
});
```

### Brand Color Overlay

Best for: Establishing brand identity over images.

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: theme.primary, transparency: 30 }
});
```

### Bottom Fade Bar

Best for: Cover slides with title at bottom.

```javascript
// Lighter overlay on top portion
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 3.5,
  fill: { color: "000000", transparency: 85 }
});

// Darker overlay on bottom portion
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 3.5, w: 10, h: 2.125,
  fill: { color: "000000", transparency: 30 }
});
```

### Side Fade (for half-bleed images)

Best for: Text on one side, image on other.

```javascript
// Three graduated strips for smooth transition
slide.addShape(pres.shapes.RECTANGLE, {
  x: 3.5, y: 0, w: 1.5, h: 5.625,
  fill: { color: theme.bg, transparency: 70 }
});
slide.addShape(pres.shapes.RECTANGLE, {
  x: 4.5, y: 0, w: 0.8, h: 5.625,
  fill: { color: theme.bg, transparency: 40 }
});
slide.addShape(pres.shapes.RECTANGLE, {
  x: 5.0, y: 0, w: 0.5, h: 5.625,
  fill: { color: theme.bg, transparency: 10 }
});
```

---

## Decorative Elements

### Accent Bar

Best for: Left-side accent on cards, section indicators.

```javascript
// Vertical accent bar
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.0, w: 0.06, h: 1.2,
  fill: { color: theme.accent }
});
```

### Decorative Circle Cluster

Best for: Background decoration, visual interest.

```javascript
// Large semi-transparent circle
slide.addShape(pres.shapes.OVAL, {
  x: 7.5, y: -0.5, w: 3, h: 3,
  fill: { color: theme.accent, transparency: 90 }
});

// Medium circle
slide.addShape(pres.shapes.OVAL, {
  x: 8.5, y: 0.5, w: 1.5, h: 1.5,
  fill: { color: theme.light, transparency: 80 }
});

// Small solid circle
slide.addShape(pres.shapes.OVAL, {
  x: 9.0, y: 2.0, w: 0.3, h: 0.3,
  fill: { color: theme.accent, transparency: 50 }
});
```

### Horizontal Divider Line

Best for: Separating title from content, section breaks.

```javascript
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 1.6, w: 2, h: 0,
  line: { color: theme.accent, width: 2.5 }
});
```

### Dashed Separator

Best for: Subtle section breaks, placeholder borders.

```javascript
slide.addShape(pres.shapes.LINE, {
  x: 0.5, y: 3.0, w: 9, h: 0,
  line: { color: theme.light, width: 1, dashType: "dash" }
});
```

### Corner Accent (geometric decoration)

Best for: Slide corner decoration, modern feel.

```javascript
// Top-right corner decoration
slide.addShape(pres.shapes.RECTANGLE, {
  x: 9.2, y: 0, w: 0.8, h: 0.08,
  fill: { color: theme.accent }
});
slide.addShape(pres.shapes.RECTANGLE, {
  x: 9.92, y: 0, w: 0.08, h: 0.8,
  fill: { color: theme.accent }
});
```

---

## Frosted / Glassmorphism Cards

Simulate frosted glass effect over images using semi-transparent cards:

```javascript
// Background image first
slide.addImage({
  path: "images/bg.jpg", x: 0, y: 0, w: 10, h: 5.625,
  sizing: { type: "cover", w: 10, h: 5.625 }
});

// Dark overlay
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "000000", transparency: 50 }
});

// "Frosted" card (white, semi-transparent, with shadow)
const makeFrostShadow = () => ({
  type: "outer", color: "000000", blur: 8, offset: 2, angle: 135, opacity: 0.20
});

slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1.5, y: 1, w: 7, h: 3.5,
  fill: { color: "FFFFFF", transparency: 80 },
  rectRadius: 0.15,
  line: { color: "FFFFFF", width: 0.5 },
  shadow: makeFrostShadow()
});

// Text on top of frosted card
slide.addText("Content Title", {
  x: 2, y: 1.5, w: 6, h: 0.8,
  fontSize: 28, bold: true, color: "FFFFFF"
});
```

---

## Quick Reference — When to Use What

| Scenario | Technique | Key Setting |
|----------|-----------|-------------|
| Card elevation | Standard shadow | blur: 6, opacity: 0.15 |
| CTA button | Colored shadow | Match button fill color |
| Footer bar | Upward shadow | angle: 270 |
| Text over photo | Dark overlay | transparency: 40–60 |
| Brand identity slide | Brand color overlay | transparency: 30 |
| Cover bottom title | Bottom fade bar | Graduated transparency |
| Section indicator | Accent bar | 0.06" width, accent color |
| Visual interest | Circle cluster | 3 circles, varying opacity |
| Modern divider | Dashed separator | dashType: "dash" |
| Premium feel | Frosted card | White, transparency: 80 |
