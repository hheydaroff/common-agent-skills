# Aesthetic Direction: High-End Soft Luxury (Awwwards-Tier)

Load when the brief reads "premium / expensive / Awwwards / $150k agency / Apple-Linear-tier / soft luxury / cinematic". Engineer agency-level digital experiences with haptic depth, cinematic spatial rhythm, obsessive micro-interactions, and fluid motion. Never generate the same layout/aesthetic twice in a row.

## "Absolute Zero" anti-patterns (instant fail)
- **Banned fonts:** Inter, Roboto, Arial, Open Sans, Helvetica. Assume premium fonts available: Geist, Clash Display, PP Editorial New, Plus Jakarta Sans.
- **Banned icons:** thick-stroked Lucide, FontAwesome, Material Icons. Use ultra-light precise lines (Phosphor Light, Remix Line).
- **Banned borders/shadows:** generic 1px solid gray borders; harsh dark drops (`shadow-md`, `rgba(0,0,0,0.3)`).
- **Banned layouts:** edge-to-edge sticky navbars glued to the top; symmetrical 3-column Bootstrap grids without massive whitespace.
- **Banned motion:** `linear`/`ease-in-out` transitions; instant state changes without interpolation.

## Creative variance engine — silently pick ONE of each before coding

### Vibe & texture (pick 1)
1. **Ethereal Glass (SaaS/AI/tech):** deepest OLED black `#050505`, subtle radial mesh-gradient orbs, vantablack cards with heavy `backdrop-blur-2xl` + `white/10` hairlines, wide geometric Grotesk type.
2. **Editorial Luxury (lifestyle/real-estate/agency):** warm creams `#FDFBF7`, muted sage or deep espresso, high-contrast variable serif headings, subtle CSS film-grain (`opacity-[0.03]`).
3. **Soft Structuralism (consumer/health/portfolio):** silver-grey or white backgrounds, massive bold Grotesk type, airy floating components with ultra-soft diffused ambient shadows.

### Layout (pick 1)
1. **Asymmetrical Bento:** masonry-like grid of varying card sizes (`col-span-8 row-span-2` next to stacked `col-span-4`). Mobile: single-column `grid-cols-1`, `gap-6`, all spans reset.
2. **Z-Axis Cascade:** physical card stacking, slight overlap, varied depth, subtle `-2deg`/`3deg` rotation. Mobile: remove rotations + negative-margin overlaps below `768px`, stack vertically (overlaps cause touch-target conflicts).
3. **Editorial Split:** massive type on left `w-1/2`, scrollable horizontal image pills / staggered cards on right. Mobile: full-width vertical stack, type on top.

**Universal mobile override:** any asymmetric layout above `md:` aggressively falls back to `w-full`, `px-4`, `py-8` below `768px`. Never `h-screen` — always `min-h-[100dvh]`.

## Haptic micro-aesthetics

### Double-Bezel (nested architecture)
Never place a premium card/image/container flatly on the background — make it look like machined hardware.
- **Outer shell:** wrapper with subtle background (`bg-black/5` or `bg-white/5`), hairline border (`ring-1 ring-black/5` or `border border-white/10`), padding (`p-1.5`/`p-2`), large radius (`rounded-[2rem]`).
- **Inner core:** distinct background, inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), smaller concentric radius (`rounded-[calc(2rem-0.375rem)]`).

### Nested CTA / "Island" buttons
Fully rounded pills (`rounded-full`, `px-6 py-3`). Trailing arrow icon NEVER naked — nested in its own circle (`w-8 h-8 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center`), flush with the right inner padding.

### Spatial rhythm
Macro-whitespace: double standard padding (`py-24`-`py-40`). Eyebrow tags: microscopic pill (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em] font-medium`). (Respect the main SKILL.md eyebrow-count cap.)

## Motion choreography
Custom cubic-beziers only (e.g. `transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`).
- **Fluid Island nav:** floating glass pill detached from top (`mt-6 mx-auto w-max rounded-full`). Hamburger morphs fluidly to an X (`rotate-45`/`-rotate-45`). Menu opens as screen-filling overlay (`backdrop-blur-3xl bg-black/80` or `bg-white/80`). Links stagger-reveal (`translate-y-12 opacity-0` → in, `delay-100/150/200`).
- **Magnetic button physics:** `group` utility; `active:scale-[0.98]`; inner icon circle translates diagonally (`group-hover:translate-x-1 group-hover:-translate-y-[1px]`) and `scale-105`.
- **Scroll interpolation:** elements enter with heavy fade-up (`translate-y-16 blur-md opacity-0` → `translate-y-0 blur-0 opacity-100` over 800ms+). Use `IntersectionObserver` or `whileInView` — never `window.addEventListener('scroll')`.

## Performance guardrails
GPU-safe (`transform`/`opacity` only, `will-change` sparingly) · `backdrop-blur` only on fixed/sticky elements, never scrolling containers · grain/noise only on fixed `pointer-events-none` pseudo-elements · z-index discipline (systemic layers only).

## Pre-output checklist (in addition to SKILL.md Pre-Flight)
- [ ] No banned fonts/icons/borders/shadows/layouts/motion from "Absolute Zero".
- [ ] A vibe archetype AND a layout archetype consciously selected.
- [ ] Major cards/containers use Double-Bezel (outer shell + inner core).
- [ ] CTAs use Button-in-Button trailing icon where applicable.
- [ ] Section padding ≥ `py-24` — layout breathes.
- [ ] All transitions use custom cubic-bezier — no `linear`/`ease-in-out`.
- [ ] Scroll-entry animations present — nothing appears statically.
- [ ] Collapses below `768px` to single-column `w-full px-4`.
- [ ] Animations use only `transform`/`opacity`; `backdrop-blur` only on fixed/sticky.
- [ ] Overall impression reads "$150k agency build", not "template with nice fonts".
