# Aesthetic Direction: Premium Utilitarian Minimalism

Load when the brief reads "minimalist / editorial / clean / Notion-Linear / document-style". Warm monochrome palette, typographic contrast, flat bento grids, muted pastel accents. No gradients, no heavy shadows. Rejects standard generic SaaS design trends.

## Banned elements
- No "Inter", "Roboto", or "Open Sans".
- No generic thin-line icon libraries (Lucide, Feather, standard Heroicons).
- No Tailwind heavy drop shadows (`shadow-md/lg/xl`). Shadows must be near-invisible or ultra-diffuse, low opacity (< 0.05).
- No primary-colored backgrounds for large elements/sections.
- No gradients, neon, or 3D glassmorphism (beyond subtle navbar blurs).
- No `rounded-full` for large containers, cards, or primary buttons.
- No emojis anywhere — replace with icons or clean SVG primitives.
- No generic placeholder names ("John Doe", "Acme Corp", "Lorem Ipsum").
- No AI clichés ("Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve").

## Typographic architecture
Extreme typographic contrast + premium font selection drive the editorial feel.
- **Body/UI/buttons (sans):** `'SF Pro Display', 'Geist Sans', 'Helvetica Neue', 'Switzer', sans-serif`.
- **Hero headings & quotes (serif):** `'Lyon Text', 'Newsreader', 'Playfair Display', 'Instrument Serif', serif`. Tight tracking (`-0.02em` to `-0.04em`), tight line-height (`1.1`). (Note: this is one of the rare briefs where editorial serif is justified.)
- **Code/keystrokes/meta (mono):** `'Geist Mono', 'SF Mono', 'JetBrains Mono', monospace`.
- **Text colors:** never absolute black — off-black/charcoal (`#111111` or `#2F3437`), `line-height: 1.6`. Secondary muted gray (`#787774`).

## Color palette (warm monochrome + spot pastels)
Color is scarce, used only for semantic meaning or subtle accents.
- **Canvas/background:** `#FFFFFF` or warm bone `#F7F6F3` / `#FBFBFA`.
- **Cards:** `#FFFFFF` or `#F9F9F8`.
- **Borders/dividers:** ultra-light `#EAEAEA` or `rgba(0,0,0,0.06)`.
- **Accents (washed-out pastels only):** Pale Red `#FDEBEC` (text `#9F2F2D`), Pale Blue `#E1F3FE` (text `#1F6C9F`), Pale Green `#EDF3EC` (text `#346538`), Pale Yellow `#FBF3DB` (text `#956400`).

## Component specs
- **Bento grids:** asymmetrical CSS Grid; cards `border: 1px solid #EAEAEA`; radius `8px`-`12px` max; generous padding (`24px`-`40px`).
- **Primary CTA:** solid `#111111`, text `#FFFFFF`, radius `4px`-`6px`, no shadow; hover → `#333333` or `scale(0.98)`.
- **Tags/badges:** pill (`9999px`), `text-xs`, uppercase, wide tracking (`0.05em`), muted-pastel background.
- **Accordions (FAQ):** no container boxes — separate with `border-bottom: 1px solid #EAEAEA`, sharp `+`/`-` toggle.
- **Keystrokes:** `<kbd>` as physical keys (`border: 1px solid #EAEAEA`, radius `4px`, `background: #F7F6F3`, mono).
- **Faux-OS window chrome:** white top bar with three small light-gray circles.

## Iconography & imagery
- **Icons:** Phosphor (Bold/Fill) or Radix UI Icons — technical, slightly thicker stroke, standardized width.
- **Illustrations:** monochromatic continuous-line ink sketches on white, with a single offset geometric shape filled with a muted pastel.
- **Photography:** high-quality, desaturated, warm tone; subtle warm-grain overlay (`opacity: 0.04`). Never oversaturated stock. Use **real Pexels photos** (`https://images.pexels.com/photos/{id}/...` with attribution) when real assets aren't available — do not invent seed URLs.
- **Backgrounds:** avoid empty flat sections — subtle full-width imagery at low opacity, soft radial light spots (`radial-gradient`, warm, `opacity: 0.03`), or minimal geometric line patterns.

## Subtle motion
Motion should feel invisible — quiet sophistication, not spectacle.
- **Scroll entry:** fade in with `translateY(12px)` + `opacity: 0` over `600ms` `cubic-bezier(0.16, 1, 0.3, 1)`. Use `IntersectionObserver`, never `window.addEventListener('scroll')`.
- **Hover:** ultra-subtle shadow shift (`0 0 0` → `0 2px 8px rgba(0,0,0,0.04)` over `200ms`); buttons `scale(0.98)` on `:active`.
- **Staggered reveals:** `animation-delay: calc(var(--index) * 80ms)`. Never mount everything at once.
- **Ambient:** optional single slow-drifting radial gradient blob (`20s+`, `opacity: 0.02-0.04`) on a `position: fixed; pointer-events: none` layer. Never on scrolling containers.
- **Performance:** `transform`/`opacity` only; `will-change` sparingly.

## Execution
1. Establish macro-whitespace first (`py-24`/`py-32` between sections). 2. Constrain typography to `max-w-4xl`/`max-w-5xl`. 3. Apply the type hierarchy + monochrome variables immediately. 4. Every card/divider/border obeys `1px solid #EAEAEA`. 5. Scroll-entry animation on all major blocks. 6. Give sections visual depth (imagery/ambient gradients/textures) — no empty flat backgrounds.
