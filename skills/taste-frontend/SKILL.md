---
name: taste-frontend
description: "Anti-slop frontend for landing pages, portfolios, and redesigns. Reads the brief, infers the design language, picks real design systems, and ships interfaces that do not look templated. Use when building marketing sites, landing pages, portfolios, or redesigning an existing site and avoiding generic AI-looking output is the priority. Triggers: 'build a landing page', 'design this site', 'make it not look AI-generated', 'redesign this', 'anti-slop', 'premium frontend', 'awwwards-style'."
license: MIT
metadata:
  version: "2.0.0"
  category: frontend
  upstream: "github.com/Leonxlnx/taste-skill (MIT, (c) Leonxlnx) — see ATTRIBUTION.md"
---

# Taste Frontend: Anti-Slop Frontend Skill

> Landing pages, portfolios, and redesigns. **Not** dashboards, data tables, or multi-step product UI (use Fluent / Carbon / Atlassian / Polaris for those).
> Every rule here is **contextual**. None fires automatically. First read the brief, then pull only what fits.

## Reference Files

| File | When to load |
|------|--------------|
| [references/design-systems.md](references/design-systems.md) | Picking a real design system, install commands, canonical docs |
| [references/ai-tells.md](references/ai-tells.md) | Full catalogue of production "AI tells" to avoid |
| [references/motion-gsap.md](references/motion-gsap.md) | GSAP sticky-stack / horizontal-pan / scroll-reveal skeletons + perf rules |
| [references/redesign.md](references/redesign.md) | Redesigning an existing site (audit-first protocol + detailed audit) |
| [references/liquid-glass.md](references/liquid-glass.md) | Honest web approximation of Apple Liquid Glass / glassmorphism |
| [references/aesthetic-minimalist.md](references/aesthetic-minimalist.md) | Brief is "minimalist / editorial / Notion-Linear" |
| [references/aesthetic-brutalist.md](references/aesthetic-brutalist.md) | Brief is "brutalist / Swiss / terminal / industrial" |
| [references/aesthetic-soft-highend.md](references/aesthetic-soft-highend.md) | Brief is "premium / Awwwards / $150k agency / soft luxury" |
| [references/output-enforcement.md](references/output-enforcement.md) | Model keeps truncating; need full unabridged output |

---

## 0. BRIEF INFERENCE (Read the Room First)

Before code or dials, infer what the user actually wants. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

**Read these signals:** page kind (landing / portfolio / redesign / editorial), vibe words used ("minimalist", "Linear-style", "brutalist", "premium", "playful"), reference URLs/screenshots/brands named, audience (B2B buyer vs design-conscious consumer vs recruiter), existing brand assets (logo/color/type), quiet constraints (accessibility-first, public-sector, regulated — these OVERRIDE aesthetic preference).

**Output a one-line "Design Read" before generating:**
> *"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."*

If the brief is ambiguous, ask **exactly one** clarifying question — never a multi-question dump. If you can confidently infer, do not ask.

**Anti-Default Discipline:** Do not default to AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism everywhere, infinite micro-animations, or Inter + slate-900. These are the LLM defaults. Reach past them deliberately.

---

## 1. THE THREE DIALS

After the design read, set three dials. Every layout/motion/density decision is gated by these.

* **`DESIGN_VARIANCE: 8`** — 1 = perfect symmetry, 10 = artsy chaos
* **`MOTION_INTENSITY: 6`** — 1 = static, 10 = cinematic / physics
* **`VISUAL_DENSITY: 4`** — 1 = art gallery / airy, 10 = cockpit / packed

**Baseline `8 / 6 / 4`** unless the design read overrides. Overrides happen conversationally, not by editing this file.

| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| minimalist / clean / Linear-style | 5-6 | 3-4 | 2-3 |
| premium consumer / Apple-y / luxury | 7-8 | 5-7 | 3-4 |
| playful / Awwwards / agency / experimental | 9-10 | 8-10 | 3-4 |
| landing / portfolio / marketing (default) | 7-9 | 6-8 | 3-5 |
| trust-first / public-sector / a11y-critical | 3-4 | 2-3 | 4-5 |
| redesign — preserve / overhaul | match / +2 | match+1 / +2 | match |

---

## 2. BRIEF → DESIGN SYSTEM (summary)

If the brief reads as an established product family (Microsoft, Google, IBM, Shopify, Atlassian, GitHub, UK/US public-sector, modern SaaS), **install and use the official package** — do not recreate its CSS by hand, do not override 90% of its tokens. **One system per project.** Default for indie/small-team builds: **Tailwind v4 utilities** (+ `dark:` variant) or **shadcn/ui** (own the code, never ship default state).

For aesthetics that are NOT a system (glassmorphism, bento, brutalism, editorial, dark-tech, aurora, kinetic type): build with native CSS + Tailwind, label borrowed inspiration honestly.

➡️ Full mapping table, install commands, and canonical docs: **[references/design-systems.md](references/design-systems.md)**.

---

## 3. DEFAULT ARCHITECTURE

Unless a real design system is chosen:

* **Framework:** React/Next.js, Server Components default. Any component using motion/scroll/pointer physics is an isolated `'use client'` leaf. Server Components render static layout only.
* **Styling:** Tailwind v4 (v3 only if the project demands). For v4 use `@tailwindcss/postcss` or the Vite plugin, never the `tailwindcss` PostCSS plugin.
* **Animation:** Motion (`import { motion } from "motion/react"`). `framer-motion` is a legacy alias.
* **State:** NEVER use `useState` for continuous values (mouse, scroll, pointer physics). Use `useMotionValue` / `useTransform` / `useScroll`.
* **Icons:** Phosphor / HugeIcons / Radix / Tabler (one family per project). Lucide only on explicit request. NEVER hand-roll SVG icon paths. Standardize `strokeWidth` globally.
* **Emoji:** Discouraged by default; replace with icon glyphs. Allow only for explicitly playful/social briefs.
* **Layout:** `max-w-[1400px] mx-auto` or `max-w-7xl`. Hero uses `min-h-[100dvh]`, NEVER `h-screen`. Use CSS Grid, never flex percentage math (`w-[calc(33%-1rem)]`).
* **Dependency check:** Before importing any 3rd-party lib, check `package.json`. If missing, output the install command first.

For deeper directives (typography, color calibration, layout discipline, hero rules, content density, quotes) the core gates are in the Pre-Flight Check below; the full production-tell catalogue lives in **[references/ai-tells.md](references/ai-tells.md)**.

---

## 4. ASSET STRATEGY (Pexels fallback)

Landing pages and portfolios are **visual products**. Text-only pages with fake-screenshot divs are slop.

**Priority order:**
1. **Image-generation tool first.** If ANY image-gen tool is available in the environment (`generate_image`, MCP image tool, IDE-integrated gen, etc.) you MUST use it to create section-specific assets (hero, product shots, textures, mood images) at the right aspect ratio.
2. **Real Pexels photos second.** When no gen tool is available, use **real, specific Pexels image URLs** that fit the page topic — format `https://images.pexels.com/photos/{id}/{slug}.jpg?auto=compress&cs=tinysrgb&w=1600`. You cannot invent a working Pexels URL the way you can with seed services; use a genuine photo you have identified for the subject, and **credit the photographer** (alt text or a small caption). No API key assumed.
3. **Last resort: TODO slots.** If neither is possible, leave clearly-labeled placeholder slots (`<!-- TODO: hero product photo, 1600x1200, source from pexels.com -->`) and tell the user which images the page needs. Do NOT fill the page with hand-rolled SVG illustrations or div-based fake screenshots.

**Even minimalist sites need real images** (2-3 minimum: hero + one product/lifestyle + one supporting). **Real logos** for social proof (Simple Icons `https://cdn.simpleicons.org/{slug}/{color}`, devicon, or a generated monogram SVG) — never plain text wordmarks. Logo wall = logos only, no category labels. **Div-based fake screenshots are banned.**

---

## 5. EM-DASH BAN (non-negotiable)

**Em-dash (`—`) and en-dash separator (`–`) are COMPLETELY banned** in everything visible to the user: headlines, eyebrows, labels, pills, button text, body copy, quotes, attribution, captions, nav, alt text. No "limited use" allowance. This is the #1 AI visual tell.

Replace with: a period, a comma, parentheses, a colon, a line break, columns, or a regular hyphen `-`. Date/number ranges use a hyphen (`2018-2026`, `€40-80k`). The only permitted dash characters are the regular hyphen and a math minus. **A single `—` or `–` anywhere visible = Pre-Flight fail; rewrite it.**

---

## 6. FINAL PRE-FLIGHT CHECK

Run every box before outputting code. If any box fails, the output is not done.

- [ ] **Brief inference** declared (one-line Design Read)?
- [ ] **Dial values** explicit and reasoned, not silently baseline?
- [ ] **Design system** chosen if applicable, or aesthetic labeled honestly? One system per project (no Material + shadcn mixed)?
- [ ] **Redesign mode** detected and audit performed (if applicable — see references/redesign.md)?
- [ ] **ZERO em-dashes (`—`/`–`)** anywhere visible (Section 5)?
- [ ] **Page Theme Lock**: ONE theme (light/dark/auto) for the whole page, no section flips mid-page?
- [ ] **Color Consistency Lock**: one accent color used identically across all sections (saturation < 80%, no AI-purple by default)?
- [ ] **Shape Consistency Lock**: one corner-radius system applied consistently?
- [ ] **Button Contrast Check**: every CTA text readable against its background (WCAG AA 4.5:1, no white-on-white)?
- [ ] **CTA Button Wrap**: no CTA label wraps to 2+ lines at desktop (3 words max for primary)?
- [ ] **Form Contrast Check**: inputs, placeholders, focus rings, labels all pass WCAG AA? Label above input, error below, no placeholder-as-label?
- [ ] **Serif discipline**: sans-serif display is the default; serif only with explicit brand/editorial justification, and NOT Fraunces or Instrument_Serif?
- [ ] **Premium-consumer palette check**: if cookware/wellness/artisan/luxury, palette is NOT the AI-default beige+brass+oxblood+espresso family?
- [ ] **Italic descender clearance**: every italic word with `y g j p q` has `leading-[1.1]` min + `pb-1` reserve?
- [ ] **Hero fits the viewport**: headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines, CTA visible without scroll, font scale planned around the asset?
- [ ] **Hero top padding** ≤ `pt-24` at desktop; hero content does not float halfway down?
- [ ] **Hero stack discipline**: max 4 text elements (eyebrow OR brand strip, headline, subtext, CTAs)? No tagline below CTAs, no trust micro-strip inside the hero?
- [ ] **Eyebrow count (mechanical)**: instances of `uppercase tracking` micro-labels ≤ ceil(sectionCount / 3)? Hero counts as 1?
- [ ] **Split-Header Ban**: no "left big headline + right small explainer paragraph" section header (stack vertically instead)?
- [ ] **Zigzag Alternation Cap**: no 3+ consecutive sections with the same image+text-split layout?
- [ ] **No Duplicate CTA Intent**: no two CTAs with the same intent ("Get in touch" + "Let's talk" = fail)?
- [ ] **Logo wall = logos only**, lives UNDER the hero, uses real SVG logos or generated marks (no plain-text wordmarks, no category labels)?
- [ ] **Bento Background Diversity**: ≥ 2-3 cells have real visual variation (image/gradient/pattern), not all white-on-white text? Bento has rhythm AND exact cell count (N items → N cells, no empty cells)?
- [ ] **Copy Self-Audit**: every visible string re-read; no grammatically-broken or AI-hallucinated phrases?
- [ ] **Motion motivated**: every animation justified in one sentence (hierarchy / storytelling / feedback / state transition)? If `MOTION_INTENSITY > 4`, page actually moves; if you can't ship working motion, drop the dial to 3 and ship clean static?
- [ ] **Marquee max-one-per-page**?
- [ ] **Navigation on ONE line** at desktop, height ≤ 80px?
- [ ] **Section-Layout-Repetition**: no layout family repeats (≥ 4 different families across 8 sections)?
- [ ] **Long lists** (> 5 items) use the right UI (2-col split, card grid, tabs/accordion, scroll-snap, carousel) — NOT a default `<ul>`/`divide-y`? No `border-t` + `border-b` on every row?
- [ ] **Real images used** (gen-tool → real Pexels URL → TODO slot) — NO div-based fake screenshots, NO hand-rolled decorative SVGs, NO pure-text minimalism?
- [ ] **No pills/labels overlaid on images**, no photo-credit-as-decoration, no version footers (`v1.4.2`), no decoration text strip at hero bottom, no floating top-right sub-text in section headings?
- [ ] **No locale/city/time/weather strips** unless genuinely place-focused? **No scroll cues** (`Scroll`, `↓`)? **No version labels in hero** (V0.6, BETA) unless a launch? **No section-numbering eyebrows** (`00 / INDEX`, `001 · Capabilities`)? **No decorative status dots** (only real semantic state)?
- [ ] **Content density** sane: no 20-row data tables, no fake-precise specs without justification, ≤ 25-word sub-paragraphs by default? Quotes ≤ 3 lines, attribution clean?
- [ ] **GSAP sticky-stack / horizontal-pan** per references/motion-gsap.md (`start: "top top"`, `pin: true`, correct scrub)? **No `window.addEventListener('scroll')`** — use `useScroll()` / ScrollTrigger / IntersectionObserver / CSS scroll-driven only?
- [ ] **Reduced motion** honored for everything `MOTION_INTENSITY > 3`? Animate only `transform`/`opacity`?
- [ ] **Dark mode** tokens defined and tested in both modes (off-black/off-white, never pure `#000`/`#fff`)?
- [ ] **Mobile collapse** explicit per section (`w-full`, `px-4`) for high-variance layouts? Viewport stable (`min-h-[100dvh]`)?
- [ ] **`useEffect` animations** have strict cleanup (`return () => ctx.revert()`)? Motion isolated in `'use client'` leaves?
- [ ] **Empty / loading / error** states provided (skeletons matching layout, not generic spinners)?
- [ ] **Icons** from an allowed library only? **Core Web Vitals** plausible (LCP < 2.5s, INP < 200ms, CLS < 0.1)?

If a single box cannot be honestly ticked, the page is not done. Fix it before delivering.

---

## 7. OUT OF SCOPE

Dashboards / dense product UI / admin panels, data tables, multi-step forms/wizards, code editors, native mobile, realtime collab UIs. If the brief is one of these, say so, point to the right tool, and apply only the marketing/about/landing parts of this skill where they fit.

---

*React/Next.js, Tailwind CSS, Motion (Framer Motion), GSAP/GreenSock, Three.js, and all other product names are trademarks of their respective owners. This skill is adapted from the MIT-licensed taste-skill by Leonxlnx — see ATTRIBUTION.md.*
