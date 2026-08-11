# Redesign Protocol

Load when upgrading an existing site/app. Misclassifying the mode is the biggest source of bad redesign output. Works with any framework or vanilla CSS — do not migrate stacks.

## 1. Detect the mode (first action)

* **Greenfield** — no existing site, or full overhaul approved. Use the dial baseline from SKILL.md §1.
* **Redesign — Preserve** — modernise without breaking the brand. Audit first, extract brand tokens, evolve gradually.
* **Redesign — Overhaul** — new visual language over existing content. Treat as greenfield for visuals; preserve content and IA.

If ambiguous, ask **once**: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*

## 2. Audit before touching

Document the current state before proposing changes:
* **Brand tokens** — primary/accent colors, type stack, logo treatment, radii.
* **Information architecture** — page tree, primary nav, key conversion paths.
* **Content blocks** — what exists, what's working, what's filler.
* **Patterns to preserve** — signature interactions, recognisable hero, copy voice.
* **Patterns to retire** — AI-slop tells, broken layouts, dead links, generic stock, perf traps.
* **Dial reading of the existing site** — infer current VARIANCE/MOTION/DENSITY; that's your starting point, not the baseline.
* **SEO baseline** — ranking pages, meta titles, structured data, OG cards. **SEO migration is the #1 redesign risk.**

## 3. Preservation rules

* Do **not** change information architecture unless asked. Keep slugs, anchor IDs, nav labels stable for SEO and muscle memory.
* Extract brand colors before applying the LILA RULE — a brand that is already purple stays purple.
* Preserve copy voice unless asked for a rewrite. Visual modernisation ≠ content rewrite.
* Honor existing a11y wins (focus states, alt text, keyboard nav, contrast).
* Respect existing analytics events — don't rename buttons, fields, section IDs downstream tracking depends on.

## 4. Modernisation levers (priority order — stop when the brief is satisfied)

1. **Typography refresh** — biggest visual lift per unit of risk.
2. **Spacing & rhythm** — increase section padding, fix vertical rhythm.
3. **Color recalibration** — desaturate, unify neutrals, keep brand accent.
4. **Motion layer** — add dial-appropriate micro-interactions to existing components.
5. **Hero & key-section recomposition.**
6. **Full block replacement** — only when the existing block is unsalvageable.

## 5. Targeted evolution vs full redesign

* IA, content, SEO sound → **targeted evolution** (levers 1-4). ~70% of value at ~40% of risk.
* Visual debt is structural (broken IA, no design system, broken mobile) → **full redesign** with strict content preservation.
* Brand itself is changing → **greenfield**.

## 6. What never changes silently

URL structure / route slugs · primary nav labels · form field names or order (breaks analytics + autofill) · brand logo/wordmark · existing legal/consent/cookie copy. Never modify these without explicit approval.

---

# Detailed Audit Checklist

Run through every category; list each generic pattern, weak point, and missing state, then fix in place.

## Typography
Browser-default fonts or Inter everywhere → swap for a font with character (Geist/Outfit/Cabinet Grotesk/Satoshi) · headlines lack presence → bigger display, tighter tracking, lower line-height · body too wide → ~65ch, more line-height · only 400/700 weights → add 500/600 · numbers in proportional font → tabular-nums/mono · missing tracking adjustments · all-caps subheaders everywhere · orphaned words → `text-wrap: balance`/`pretty`.

## Color & surfaces
Pure `#000` background → off-black/charcoal · oversaturated accents → < 80% saturation · more than one accent → pick one · mixing warm and cool grays → one family · purple/blue "AI gradient" → neutral base + one considered accent · generic `box-shadow` → tinted to background hue · flat with zero texture → subtle noise/grain/micro-pattern · perfectly even gradients → radial/noise/mesh · inconsistent lighting direction · random dark section in a light page (or vice versa) → commit to one theme · empty flat sections → add background imagery (blurred/overlaid/masked), patterns, or ambient gradients. Source real images from **pexels.com** (use a genuine photo URL `https://images.pexels.com/photos/{id}/...` with attribution) when assets aren't provided — do not invent seed URLs.

## Layout
Everything centered/symmetrical → break symmetry · three equal card columns → 2-col zig-zag/asymmetric/scroll/masonry · `height: 100vh` → `min-height: 100dvh` · complex flexbox % math → CSS Grid · no max-width container → ~1200-1440px · forced equal card heights → variable/masonry · uniform border-radius → vary by hierarchy · no overlap/depth → negative margins for layering · symmetrical vertical padding → optical adjustment (bottom often larger) · dashboard always left-sidebar → try top nav / command menu · missing whitespace → double spacing · buttons not bottom-aligned in card groups · feature lists starting at different Y positions · misaligned baselines in side-by-side elements · mathematically-centered-but-optically-wrong elements → 1-2px optical nudges.

## Interactivity & states
No hover states → add background shift/scale/translate · no active/pressed feedback → `scale(0.98)`/`translateY(1px)` · instant transitions → 200-300ms · missing focus ring (a11y requirement) · no loading states → skeletons not spinners · no empty states → composed "getting started" · no error states → inline messages, no `alert()` · dead links (`#`) · no current-page indicator in nav · scroll jumping → `scroll-behavior: smooth` · animations on `top`/`left`/`width`/`height` → `transform`/`opacity`.

## Content
Generic names ("John Doe") · fake round numbers (`99.99%`, `$100.00`) → organic data · placeholder brand names ("Acme", "Nexus") · AI clichés ("Elevate", "Seamless", "Unleash", "Delve", "Tapestry", "In the world of...") · exclamation marks in success messages · "Oops!" errors → direct ("Connection failed. Please try again.") · passive voice → active · identical blog dates · same avatar reused · Lorem Ipsum → real draft copy · Title Case On Every Header → sentence case.

## Component patterns
Generic card (border+shadow+white bg) → remove border or use spacing only · always one filled + one ghost button → add text/tertiary styles · pill "New"/"Beta" badges → square/flag/plain · accordion FAQ → side-by-side list / searchable · 3-card carousel testimonials with dots → masonry wall / single rotating quote · 3-tower pricing → highlight recommended with color not just height · modals for everything → inline edit / slide-over · avatar circles only → squircles · sun/moon toggle → dropdown / system preference · 4-column footer link farm → simplify.

## Iconography
Lucide/Feather exclusively → Phosphor/Heroicons/custom · rocketship for "Launch", shield for "Security" → less obvious metaphors · inconsistent stroke widths → standardize · missing favicon · stock "diverse team" photos → real/candid/consistent illustration.

## Code quality
Div soup → semantic HTML · inline styles mixed with classes · hardcoded pixel widths → relative units · missing/empty alt text · arbitrary `z-index: 9999` → clean scale · commented-out dead code · import hallucinations → check `package.json` · missing meta tags (`title`, `description`, `og:image`).

## Strategic omissions (what AI forgets)
No legal links · no "back" navigation · no custom 404 · no form validation · no "skip to content" link · no cookie consent where required.

## Fix priority (max impact, min risk)
1. Font swap · 2. Color cleanup · 3. Hover/active states · 4. Layout & spacing · 5. Replace generic components · 6. Loading/empty/error states · 7. Typography scale polish.

**Rules:** work with the existing stack, don't break functionality (test after each change), check dependencies before importing, check Tailwind v3 vs v4 before editing config, keep changes small and reviewable over big rewrites.
