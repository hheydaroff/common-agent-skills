# Speaker Notes Generation

## Overview

Speaker notes transform slides from visual aids into a complete presentation system. Generate notes **after all slides are finalized** to ensure narrative coherence across the full deck.

---

## When to Generate

- **Always generate** speaker notes unless the user explicitly opts out
- Generate **after** all slide JS files are written and verified
- Create as a single pass to maintain narrative flow

---

## Notes Structure

### Master Document: `slides/notes/total.md`

```markdown
# 01 — Cover: Presentation Title

[Opening — establish context and hook the audience]

Welcome everyone. Today we're going to explore [topic] — a subject that directly impacts [audience concern]. By the end of this session, you'll have a clear understanding of [core takeaway].

Key points: ① Set context ② State purpose ③ Preview structure
Duration: 1 minute

---

# 02 — Agenda

[Transition] Before we dive in, let me walk you through our roadmap for today.

We'll cover four main areas: first [section 1], then [section 2], followed by [section 3], and we'll wrap up with [section 4]. [Pause] Let's start with the first topic.

Key points: ① Preview all sections ② Set expectations ③ Bridge to first section
Duration: 1 minute

---

# 03 — Section Title

[Transition] Now that we have the big picture, let's dig into [section topic].

This is important because [reason]. What I want you to take away from this section is [key insight]. Let me show you the data.

Key points: ① Why this matters ② Core insight ③ What to watch for
Duration: 2 minutes

---
```

### Per-Slide Files: `slides/notes/slide-01.md`

Split from `total.md` after writing. Each file contains the content for one slide **without** the `#` heading.

---

## Stage Direction Markers

Use markers to guide delivery rhythm:

| Marker | Purpose | When to Use |
|--------|---------|-------------|
| `[Pause]` | Silence after key content — let audience absorb | After statistics, key insights, surprising statements |
| `[Transition]` | Bridge from previous slide | Start of every slide except the cover |
| `[Interactive]` | Prompt audience engagement | Questions, polls, show of hands |
| `[Data]` | Direct attention to a specific chart/number | When referencing visual data on screen |
| `[Scan Room]` | Read the audience, adjust pace | After complex content, before moving on |

### Multi-Language Labels

When presentation content is non-English, localize all markers:

| English | 中文 | 日本語 | 한국어 |
|---------|------|--------|--------|
| `[Pause]` | `[停顿]` | `[間]` | `[멈춤]` |
| `[Transition]` | `[过渡]` | `[つなぎ]` | `[전환]` |
| `[Interactive]` | `[互动]` | `[問いかけ]` | `[상호작용]` |
| `[Data]` | `[数据]` | `[データ]` | `[데이터]` |
| `[Scan Room]` | `[观察]` | `[観察]` | `[관찰]` |
| `Key points:` | `要点：` | `要点：` | `핵심 포인트:` |
| `Duration:` | `时长：` | `所要時間：` | `소요 시간:` |

---

## Notes by Content Strategy Style

### General / Versatile Style

Conversational, energetic, story-driven.

```markdown
# 05 — Our Product in Action

[Transition] So you've seen the problem — now let me show you the solution.

[Interactive] How many of you have experienced [pain point]? I'm guessing most hands would go up. That's exactly why we built [product]. [Pause]

What makes this different is [differentiator]. Let me walk you through a real example. [Data] As you can see on screen, our users saw a 40% improvement in just 30 days.

Key points: ① Pain point resonance ② Product differentiator ③ Proof with data
Duration: 3 minutes
```

### Consulting / Analytical Style

Structured, evidence-based, methodical.

```markdown
# 05 — Market Analysis: Key Findings

[Transition] With the methodology established, let's examine what the data tells us.

[Data] Three findings stand out. First, the market grew 23% year-over-year — significantly above the 15% industry average. [Pause] Second, the top three players consolidated 68% of market share, up from 54% last year. Third, customer acquisition costs dropped 18% across the sector.

The implication: consolidation is accelerating, and efficiency gains are real. [Scan Room]

Key points: ① 23% YoY growth (vs 15% avg) ② Top-3 concentration at 68% ③ CAC down 18%
Duration: 3 minutes
```

### Executive / Persuasive Style

Conclusion-first, action-oriented, decisive.

```markdown
# 05 — Strategic Recommendation

[Transition] Based on the analysis, here is our recommendation.

We should proceed with Option B — the phased expansion into APAC markets. [Pause] The reason is straightforward: the risk-adjusted ROI is 2.3x compared to 1.4x for the domestic-only scenario.

[Data] On the left you'll see the three-year NPV comparison. On the right, the key risk factors and our mitigation plan for each. [Pause]

The ask today: approve the $4.2M Phase 1 budget for Q3 execution.

Key points: ① Recommend Option B (phased APAC) ② 2.3x risk-adjusted ROI ③ Approval request: $4.2M
Duration: 2 minutes
```

---

## Duration Guidelines

| Slide Type | Typical Duration | Notes |
|-----------|-----------------|-------|
| Cover | 0.5–1 min | Brief welcome, set context |
| Table of Contents | 0.5–1 min | Preview structure |
| Section Divider | 0.5 min | Transition moment |
| Content (light) | 1.5–2 min | 3–5 talking points |
| Content (data-heavy) | 2–3 min | Charts need explanation time |
| Content (interactive) | 3–5 min | Q&A, discussion |
| Summary / Closing | 1–2 min | Recap + call to action |

**Rule of thumb**: Total presentation = page count × 1.5–2 minutes.

---

## Implementation

### Step 1: Generate Master Document

After all slides are finalized, create `slides/notes/total.md`:

```javascript
// In compile.js or as a separate step
const fs = require('fs');
const path = require('path');

// Read all slide configs to get titles
const slides = [];
for (let i = 1; i <= SLIDE_COUNT; i++) {
  const num = String(i).padStart(2, '0');
  const mod = require(`./slide-${num}.js`);
  slides.push({ num, config: mod.slideConfig });
}

// Generate notes template (fill in manually or with AI)
let notes = '';
slides.forEach(s => {
  notes += `# ${s.num} — ${s.config.type}: ${s.config.title}\n\n`;
  notes += `[Transition] ...\n\n`;
  notes += `...\n\n`;
  notes += `Key points: ① ... ② ... ③ ...\n`;
  notes += `Duration: X minutes\n\n---\n\n`;
});

fs.mkdirSync('notes', { recursive: true });
fs.writeFileSync('notes/total.md', notes.trim());
```

### Step 2: Split Into Per-Slide Files

```bash
# Simple split script
cd slides/notes
csplit -z total.md '/^# /' '{*}'
# Or let the AI generate individual files directly
```

### Step 3: Embed in PPTX (Optional)

PptxGenJS supports slide notes:

```javascript
function createSlide(pres, theme) {
  const slide = pres.addSlide();
  // ... slide content ...

  // Add speaker notes
  slide.addNotes("Welcome everyone. Today we'll explore...\n\nKey points:\n1. Context\n2. Purpose\n3. Structure");

  return slide;
}
```

---

## Output Structure

```
slides/
├── notes/
│   ├── total.md           # Master document (full narrative)
│   ├── slide-01.md        # Per-slide notes
│   ├── slide-02.md
│   └── ...
├── slide-01.js
├── slide-02.js
└── ...
```

---

## Quality Checklist

- [ ] Every slide has notes (except cover may be minimal)
- [ ] Every slide after cover starts with `[Transition]`
- [ ] Key points use ① ② ③ format (3 items)
- [ ] Duration is specified for each slide
- [ ] Total duration matches expected presentation length
- [ ] Narrative flows logically across slides (read total.md end-to-end)
- [ ] Data references match actual chart/stat content on slides
- [ ] Language matches presentation content language
