# Design Engineering Directives & AI Tells

The full catalogue of bias-correction directives and forbidden "AI tell" patterns. The highest-value gates are already in SKILL.md's Pre-Flight Check; this is the encyclopedic detail behind them. Each rule has a context-aware override path — none fires automatically.

## Typography

* **Display/headlines:** default `text-4xl md:text-6xl tracking-tighter leading-none`. **Body:** `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Sans default:** Inter is discouraged as default — prefer Geist, Outfit, Cabinet Grotesk, Satoshi, or a brand-appropriate face. Inter is OK only for explicit neutral/Linear-style or public-sector/a11y briefs.
* **Pairings:** Geist + Geist Mono, Satoshi + JetBrains Mono, Cabinet Grotesk + Inter Tight, GT America + IBM Plex Mono.
* **SERIF DISCIPLINE (very discouraged as default):** "creative brief = serif" is the single most-tested AI tell. Serif is acceptable only when the brand names a serif, OR the family is genuinely editorial/luxury/publication/heritage AND you can articulate why this specific serif fits. Default to sans display (Geist Display, ABC Diatype, Cabinet Grotesk Display, PP Neue Montreal, Inter Display). **Banned as defaults:** Fraunces and Instrument_Serif. If a serif is justified, rotate (do not reuse across consecutive projects): PP Editorial New, GT Sectra, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, Canela, Domaine Display.
* **Emphasis rule:** to emphasize a word in a headline, use italic/bold of the SAME font. Do NOT inject a random serif word into a sans headline. Mixed-family emphasis is amateur.
* **Italic descender clearance:** italic display words with `y g j p q` need `leading-[1.1]` min + `pb-1`/`mb-1` reserve or descenders clip.

## Color Calibration

* Max 1 accent color, saturation < 80% by default.
* **THE LILA RULE:** AI-purple/blue glow is discouraged. Use neutral bases (Zinc/Slate/Stone) with a high-contrast singular accent (Emerald, Electric Blue, Deep Rose, Burnt Orange). Override only if the brand explicitly asks for purple — then execute with intent.
* **Color Consistency Lock:** once an accent is chosen, use it on the WHOLE page. No surprise blue CTA in section 7 on a warm-grey site.
* **Premium-consumer palette ban:** for cookware/wellness/artisan/luxury/heritage/DTC briefs, the LLM default is warm beige/cream + brass/clay/oxblood/ochre + espresso text. Banned hex families as defaults — backgrounds `#f5f1ea`/`#f7f5f1`/`#fbf8f1`/`#efeae0`/`#ece6db`; accents `#b08947`/`#b6553a`/`#9a2436`/`#9c6e2a`; text `#1a1714`/`#1a1814`. Rotate alternatives: Cold Luxury (silver-grey/chrome), Forest (deep green/bone/amber), Black-and-Tan, Cobalt+Cream, Terracotta+Slate, Olive+Brick+Paper, monochrome + single saturated pop. Do not ship the same warm-craft palette twice in a row.

## Layout Diversification

* **Anti-center bias:** centered hero/H1 avoided when `DESIGN_VARIANCE > 4`. Force split-screen (50/50), left-content/right-asset, asymmetric white-space, or scroll-pinned. Override OK for editorial/manifesto/launch briefs.
* **Cards** only when elevation communicates real hierarchy; otherwise group with `border-t`, `divide-y`, or negative space. For `VISUAL_DENSITY > 7`, generic card containers are banned.
* **Shape Consistency Lock:** one corner-radius scale per page (all-sharp, all-soft 12-16px, or all-pill for interactive). Mixed only with a documented rule applied everywhere.
* **Shadows:** tint to the background hue; no pure-black drop shadows on light backgrounds.

## Interactive UI States

Always implement full cycles, not just the static success state:
* **Loading:** skeletons matching final layout shape — not generic spinners.
* **Empty:** composed, indicates how to populate.
* **Error:** inline (forms) or contextual (toasts for transient only).
* **Tactile:** `:active` → `-translate-y-[1px]` or `scale-[0.98]`.
* **Button contrast (a11y):** every CTA text readable vs its background (WCAG AA 4.5:1 body, 3:1 large). White-on-white, transparent-over-photo with no scrim — banned.
* **CTA wrap ban:** button text fits one line at desktop (3 words max for primary, ideally 1-2).
* **No duplicate CTA intent:** "Get in touch" + "Let's talk" + "Start a project" = one intent → one label everywhere.
* **Form contrast (a11y):** inputs, placeholders, focus rings, helper/error text all pass WCAG AA. Label ABOVE input, error BELOW, `gap-2`. No placeholder-as-label, ever.

## Layout Discipline (hard rules)

* **Hero fits the initial viewport:** headline ≤ 2 lines desktop, subtext ≤ 20 words AND ≤ 3-4 lines, CTAs visible without scroll. A 4-line hero headline is a font-size error, not a copy-length error. Default scale `text-4xl md:text-5xl lg:text-6xl`; `text-6xl md:text-7xl` only for 3-5 word headlines.
* **Hero top padding** ≤ `pt-24` desktop.
* **Hero stack discipline (max 4 text elements):** eyebrow OR brand strip (zero or one), headline, subtext, CTAs (1 primary + max 1 secondary). Banned in hero: tagline below CTAs, trust micro-strip, pricing teaser, feature bullets, avatar row. "Used by / Trusted by" logo wall belongs UNDER the hero.
* **Navigation:** single line at desktop, height ≤ 80px (default 64-72px).
* **Bento:** rhythm not one-sided repetition; EXACTLY as many cells as content (N items → N cells, no empty cells); ≥ 2-3 cells with real visual variation (image/gradient/pattern), not all white-on-white text.
* **Section-Layout-Repetition ban:** each layout family appears at most once; ≥ 4 different families across 8 sections.
* **Zigzag alternation cap:** max 2 consecutive image+text-split sections; the 3rd is a fail.
* **Eyebrow restraint (#1 violated rule):** an eyebrow is the small uppercase wide-tracking label above a section headline. **Max 1 eyebrow per 3 sections** (hero counts as 1). Mechanical check: count `uppercase tracking` labels; if > ceil(sectionCount/3), fail. Default: drop it — the headline alone is enough.
* **Split-header ban:** "left big headline + right small explainer paragraph" as a section header is banned by default; stack vertically (headline, then body ≤ 65ch). Use split only when the right column carries a real visual/interactive element.
* **Mobile collapse explicit per section:** declare the `< 768px` fallback in the same component. No "Tailwind handles it" assumptions.

## Content Density

* **Default per section:** short headline (≤ 8 words) + sub-paragraph (≤ 25 words) + one visual OR one CTA.
* **No data-dump sections.** A 20-row table / 30-row award list / giant pricing matrix on a marketing page is the wrong layout. Use top 3-5 + "view full list", marquee/carousel, or a different page.
* **Long lists (> 5 items) need a different component, not a longer list:** 2-col split, card grid, tabs/accordion, scroll-snap pills, carousel, or marquee. A 10-row spec table with a hairline under every row is the worst default — group into 2-3 clusters or move to card-per-spec.
* **Copy self-audit (before ship):** re-read every visible string. Flag/rewrite anything grammatically broken, with unclear referents, that sounds like AI hallucination (cute-but-wrong wordplay, forced metaphors), or that reads like an LLM trying to sound thoughtful. If unsure, replace with a plain functional sentence.
* **Fake-precise numbers** (`92%`, `4.1×`, `13.4 lb`) are flagged unless from real data or explicitly labeled mock.
* **One copy register per page.**

## Quotes & Testimonials

* Max 3 lines of quote body. No em-dash inside quotes (see SKILL.md §5). Attribution = name + role + (optionally) company, never name only. Use real typographic quotes ( " " ) or none — not straight ASCII.

## Page Theme Lock

One theme per page. If dark, ALL sections dark — no warm-paper section sandwiched between dark sections. Section-level tints within the same family are fine (`bg-zinc-950` next to `bg-zinc-900`); flipping to `bg-amber-50` mid-dark-page is broken. With themed systems (Radix, shadcn `<Theme>`) set theme once in the root, never per-section. Exception: a deliberate one-time "color block story" / theme switch on scroll, once per page.

---

# Production-Test Tells (banned outright)

Signatures the model defaults to when trying to "look designed." Hard bans unless the brief explicitly calls for one.

## Visual & CSS
No neon/outer glows by default · no pure black (`#000000`) · no oversaturated accents · no excessive gradient text on large headers · no custom mouse cursors · mathematically perfect padding (no awkward floating gaps) · **no 3-column equal feature cards**.

## Hero & top-of-page
No version labels in the hero (`V0.6`, `BETA`, `INVITE-ONLY`, `ALPHA`) unless the brief is a launch · no "Brand · No. 01" sub-eyebrows.

## Section numbering & micro-labels
No section-number eyebrows (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`) · no `01 / 4` pagination on images/tiles · no `Scroll · 001` scroll cues · no "Index of Work, 2018-2026" range eyebrows.

## Separators & dots
Middle-dot (`·`) rationed to max 1 per metadata line; not the default separator for everything · no decorative colored status dots on every list/nav/badge (only real semantic state, sparingly).

## Typography flourishes
No em-dash anywhere (SKILL.md §5) · no `<br>`-broken-and-italicized headlines as a default move · no vertical rotated text unless explicitly agency/experimental · no crosshair/hairline grid lines as pure decoration.

## Fake product previews
No div-based fake product UI in the hero (fake task list / terminal / dashboard from styled divs) — the #1 LLM design tell · no fake version footers inside fake screenshots.

## Marketing-copy tells
No "Quietly in use at" / "Quietly trusted by" · no "From the field" / "Field notes" / "Currently on the bench" poetic sidebar labels · no "We respect the French ones" mock-humble references · no weather/locale strips unless place-focused · no micro-meta-sentences under eyebrows · no generic step labels ("Stage 1/2/3", "Phase 01/02/03") — use the verb directly.

## Pills, labels, version stamps
No pills/labels/tags overlaid on images · no photo-credit captions as decoration (real photographer credit only) · no version footers on marketing pages (`v1.4.2`, `Build 0048`) · no "Reservation 412 of 800" live-stock counters unless real data.

## Decoration text strips
No decoration text strip at hero bottom (`BRAND. MOTION. SPATIAL.`, `DESIGN · BUILD · SHIP`) unless it carries real navigable links/status · no floating top-right sub-text in section headings.

## Lists, dividers, scoring
No `border-t` + `border-b` on every row of a long list/spec table · no scoring/progress bars with filled background tracks as comparison visuals on a landing page.

## Locale, time, scroll cues
Locale/city/time/weather strips banned for 99% of briefs (a single footer contact address is fine) · scroll cues banned (`Scroll`, `↓ scroll`, `Scroll to explore`, animated mouse-wheel) · zero decorative status dots by default.

## Content & data ("Jane Doe" effect)
No generic names ("John Doe", "Sarah Chan") · no generic avatars (SVG egg, Lucide user) · no fake-perfect numbers (`99.99%`, `50%`, `1234567`) — use organic data (`47.2%`) · no startup-slop brand names ("Acme", "Nexus", "SmartFlow", "Cloudly") · no filler verbs ("Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize").

## External resources & components
No hand-rolled SVG icons (use Phosphor/HugeIcons/Radix/Tabler) · hand-rolled decorative SVGs strongly discouraged · no div-based fake screenshots · no broken Unsplash links (prefer a real Pexels URL or a TODO slot) · shadcn/ui never in default state.
