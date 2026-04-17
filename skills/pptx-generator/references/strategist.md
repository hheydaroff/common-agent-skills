# Strategist Phase — Planning & Design Specification

## Overview

Before generating any slides, produce a **Design Specification** through structured planning. This phase ensures alignment between content, audience, and visual design — preventing costly rework later.

**Pipeline**: `Source Content → Strategist (this phase) → Slide Generation → QA`

---

## Eight Confirmations (MANDATORY)

Present professional recommendations for all eight items as a bundled package. Wait for user confirmation or modifications before proceeding.

> Once confirmed, proceed automatically through slide generation and QA — no additional questions or pauses.

### 1. Canvas Format

| Format | Dimensions | Ratio | Use Case |
|--------|-----------|-------|----------|
| PPT 16:9 | 10" × 5.625" | 16:9 | **Default** — presentations, webinars, screen sharing |
| PPT 4:3 | 10" × 7.5" | 4:3 | Printed handouts, older projectors |

Recommend based on delivery context (screen vs. print vs. social).

### 2. Page Count

Provide a specific recommendation based on source content volume:

| Content Volume | Recommended Pages | Typical Breakdown |
|---------------|-------------------|-------------------|
| Light (< 1000 words) | 6–8 | 1 cover + 1 TOC + 3–4 content + 1 summary |
| Medium (1000–3000 words) | 8–12 | 1 cover + 1 TOC + 2 dividers + 5–7 content + 1 summary |
| Heavy (3000+ words) | 12–18 | 1 cover + 1 TOC + 3–4 dividers + 7–12 content + 1 summary |

### 3. Target Audience & Key Information

Confirm:
- **Target audience** (executives, team, public, students, clients)
- **Usage occasion** (boardroom, conference, webinar, classroom, sales pitch)
- **Core message** (the one thing the audience should remember)

### 4. Content Strategy Style

| Style | Core Focus | Target Audience | When to Use |
|-------|-----------|----------------|-------------|
| **A) General / Versatile** | Visual impact first | Public, clients, trainees | Promotional, product launches, training, brand campaigns |
| **B) Consulting / Analytical** | Data clarity first | Teams, management | Progress reports, data analysis, market research |
| **C) Executive / Persuasive** | Logical persuasion first | Executives, board, investors | Strategic decisions, investment proposals, board presentations |

**Decision tree:**
```
Content characteristics?
  ├── Heavy imagery / promotional ──→ A) General
  ├── Data analysis / progress report ──→ B) Consulting
  └── Strategic decisions / persuading executives ──→ C) Executive

Audience?
  ├── Public / clients / trainees ────→ A) General
  ├── Teams / management ────────────→ B) Consulting
  └── Executives / board / investors → C) Executive
```

**Style capabilities:**

| Capability | General | Consulting | Executive |
|-----------|---------|------------|-----------|
| Full-bleed images + overlays | ✅ Primary | ⚠️ Selective | ❌ Rare |
| Free creative layouts | ✅ Yes | ⚠️ Grid-based | ⚠️ Framework-based |
| KPI dashboards | ❌ | ✅ Primary | ✅ Selective |
| Data-heavy charts | ⚠️ Simple | ✅ Detailed | ✅ With conclusions |
| Pyramid / framework diagrams | ❌ | ⚠️ Basic | ✅ Primary |
| Executive summary boxes | ❌ | ⚠️ Optional | ✅ Required (top of slide) |
| Action-oriented conclusions | ⚠️ Optional | ⚠️ End of section | ✅ Every slide |

### 5. Color Scheme

Recommend a palette based on content characteristics and industry. Use the [Industry Color Reference](#industry-color-reference) below. Follow the **60-30-10 rule**: primary 60%, secondary 30%, accent 10%.

Rules:
- Text contrast ratio ≥ 4.5:1
- No more than 4 colors per slide
- Provide specific hex values

### 6. Icon Usage Approach

| Option | Approach | Suitable Scenarios |
|--------|----------|-------------------|
| **A** | react-icons (rendered to PNG via sharp) | **Default** — professional, high-quality, 50,000+ icons |
| **B** | Emoji text | Casual, playful, social media |
| **C** | No icons | Data-heavy reports, minimal design |
| **D** | Custom / user-provided | Has brand icon assets |

### 7. Typography Plan

Select a **font preset** and **size baseline**:

#### Font Presets

| Preset | Header Font | Body Font | Best For |
|--------|------------|-----------|----------|
| **P1** Modern Business | Arial | Calibri | Tech, startup, SaaS |
| **P2** Classic Corporate | Georgia | Calibri | Finance, consulting, legal |
| **P3** Bold & Impactful | Arial Black | Arial | Marketing, launches, keynotes |
| **P4** Elegant & Editorial | Cambria | Calibri | Culture, arts, editorial |
| **P5** Clean & Versatile | Trebuchet MS | Calibri | Education, training, general |

#### Size Baseline (by content density)

| Content Density | Body Size (pt) | Title | Subtitle | Caption |
|----------------|----------------|-------|----------|---------|
| **Relaxed** (3–5 items/slide) | 16 | 36–44 | 20–24 | 10–12 |
| **Dense** (6+ items/slide) | 14 | 28–36 | 18–22 | 10–11 |

### 8. Image Usage

| Option | Approach | When to Use |
|--------|----------|-------------|
| **A** | No images | Data reports, process docs |
| **B** | User-provided images | Has existing assets |
| **C** | Stock / placeholder descriptions | Images to be sourced later |
| **D** | Decorative shapes only | Abstract, minimal design |

When **B** is selected, list each image with:
- Filename, dimensions, aspect ratio
- Purpose (cover background, illustration, photo, diagram)
- Recommended layout (full-bleed, half-bleed, card, thumbnail)

---

## Industry Color Reference

Use alongside the palette reference in [design-system.md](design-system.md):

| Industry | Primary | Accent | Characteristics | Recommended Palette # |
|----------|---------|--------|----------------|----------------------|
| Finance / Banking | `003366` | `D4AF37` | Stable, trustworthy, premium | #2, #9, #18 |
| Technology / SaaS | `0077B6` | `FFB703` | Innovative, energetic | #7, #15, #18 |
| Healthcare / Pharma | `006D77` | `E29578` | Professional, reassuring | #1, #11 |
| Education | `264653` | `E9C46A` | Clear, logical, warm | #10, #17 |
| Government / Public | `2B2D42` | `EF233C` | Authoritative, dignified | #2, #4 |
| Legal / Consulting | `22223B` | `9A8C98` | Sophisticated, serious | #14, #2 |
| Real Estate | `3A5A40` | `DDA15E` | Grounded, premium | #3, #11 |
| Food & Beverage | `335C67` | `E09F3E` | Rich, appetizing | #13, #8 |
| Fashion / Luxury | `4A5759` | `EDAFB8` | Muted, elegant | #12, #14 |
| Energy / Environment | `588157` | `A3B18A` | Natural, sustainable | #11, #3 |
| Sports / Fitness | `023047` | `FB8500` | High energy, dynamic | #7, #17 |
| Creative / Design | `CDB4DB` | `BDE0FE` | Playful, inspiring | #5, #16 |
| Automotive | `001D3D` | `FFC300` | Deep, powerful, luminous | #9, #7 |
| Hospitality / Travel | `0081A7` | `F07167` | Refreshing, inviting | #16, #1 |

---

## Design Specification Output

After user confirms the Eight Confirmations, produce `design_spec.md` in the slides directory:

```markdown
# Design Specification

## I. Project Information
- **Topic**: [presentation topic]
- **Audience**: [target audience]
- **Purpose**: [inform / persuade / inspire / instruct / report]
- **Delivery**: [screen / projector / print / webinar]

## II. Canvas & Format
- **Layout**: LAYOUT_16x9 (10" × 5.625")
- **Page count**: [N] slides

## III. Content Strategy Style
- **Style**: [General / Consulting / Executive]
- **Tone**: [formal / conversational / inspirational]

## IV. Color Scheme
- **Primary**: [hex] — [usage]
- **Secondary**: [hex] — [usage]
- **Accent**: [hex] — [usage]
- **Light**: [hex] — [usage]
- **Background**: [hex] — [usage]

## V. Typography
- **Preset**: [P1–P5]
- **Header font**: [font name]
- **Body font**: [font name]
- **Size baseline**: [relaxed / dense]

## VI. Visual Style
- **Style recipe**: [Sharp / Soft / Rounded / Pill]
- **Icon approach**: [react-icons / emoji / none / custom]
- **Image approach**: [none / user-provided / placeholder / shapes only]

## VII. Slide Outline
| # | Type | Title | Subtype | Key Content |
|---|------|-------|---------|-------------|
| 1 | Cover | ... | — | ... |
| 2 | TOC | ... | — | ... |
| ... | ... | ... | ... | ... |

## VIII. Speaker Notes Requirements
- **Total duration**: [N] minutes
- **Notes style**: [formal / conversational / interactive]
- **Include**: transitions, key points, duration per slide

## IX. Image Resource List
| Filename | Purpose | Layout | Status |
|----------|---------|--------|--------|
| ... | ... | ... | [existing / placeholder] |
```

---

## Next Steps After Confirmation

1. Proceed to [Slide Generation](../SKILL.md#creating-from-scratch-workflow) (Step 5+)
2. Use the Design Spec as the single source of truth for all slide modules
3. Pass the confirmed theme object to all `createSlide()` functions
