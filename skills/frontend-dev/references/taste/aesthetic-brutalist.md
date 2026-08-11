# Aesthetic Direction: Industrial Brutalism & Tactical Telemetry

Load when the brief reads "brutalist / Swiss / terminal / industrial / blueprint / military / declassified". Synthesizes mid-century Swiss typographic print, industrial manufacturing manuals, and retro-futuristic aerospace/military terminals. Rigid modular grids, extreme type-scale contrast, utilitarian color, programmatic analog degradation (halftones, scanlines, dithering). Deliberately discards consumer UI patterns.

## Visual archetypes — pick ONE per project, commit; never mix both modes

### Swiss Industrial Print
1960s corporate identity + heavy machinery blueprints. High-contrast light modes (newsprint/off-white substrates), monolithic heavy sans-serif type, unforgiving grids with visible dividing lines, aggressive asymmetric negative space punctuated by oversized viewport-bleeding numerals, heavy primary red as alert/accent.

### Tactical Telemetry & CRT Terminal
Classified databases, legacy mainframes, aerospace HUDs. Dark mode exclusivity, high-density tabular data, dominant monospace, technical framing devices (ASCII brackets, crosshairs), simulated hardware limits (phosphor glow, scanlines, low bit-depth).

## Typographic architecture
Typography is the primary structural and decorative infrastructure. Imagery is secondary. Extreme variance in scale, weight, spacing.

- **Macro (structural headers):** Neo-Grotesque/Heavy Sans — Neue Haas Grotesk Black, Inter Extra Bold/Black, Archivo Black, Monument Extended. Massive fluid scale (`clamp(4rem, 10vw, 15rem)`), tight negative tracking (`-0.03em` to `-0.06em`), compressed leading (`0.85`-`0.95`), uppercase.
- **Micro (data/telemetry):** Monospace — JetBrains Mono, IBM Plex Mono, Space Mono, VT323, Courier Prime. Fixed small scale (`10px`-`14px`), generous tracking (`0.05em`-`0.1em`), uppercase, for all metadata/nav/IDs/coordinates.
- **Textural contrast (high-contrast serif):** Playfair Display, EB Garamond, Times New Roman — used exceedingly sparingly, heavily post-processed (halftone/1-bit dither) to degrade vector perfection.

## Color system — choose ONE substrate per project, never mix light/dark
Gradients, soft drop shadows, and modern translucency are prohibited. Colors simulate physical media or primitive emissive displays.

**Swiss Industrial Print (light):** background `#F4F4F0` / `#EAE8E3` (matte documentation paper); foreground `#050505`-`#111111` (carbon ink); accent `#E61919` / `#FF2A2A` (aviation/hazard red) — the ONLY accent, for strike-throughs, structural dividers, vital highlights.

**Tactical Telemetry (dark):** background `#0A0A0A` / `#121212` (deactivated CRT, avoid pure `#000`); foreground `#EAEAEA` (white phosphor); accent same hazard red; optional Terminal Green `#4AF626` for ONE specific element only — never as general text.

## Layout & spatial engineering
Must appear mathematically engineered.
- **Blueprint grid:** strict CSS Grid; elements anchored to tracks/intersections, never floating.
- **Visible compartmentalization:** solid borders (`1px`/`2px solid`) delineating zones; full-width `<hr>` segregating units.
- **Bimodal density:** oscillate between extreme data density (packed monospace metadata) and vast calculated negative space framing macro-type.
- **Geometry:** absolute rejection of `border-radius` — all corners 90°.

## UI components & symbology
- **Syntax decoration:** ASCII framing — `[ DELIVERY SYSTEMS ]`, `< RE-IND >`; directional `>>>`, `///`.
- **Industrial markers:** `®`/`©`/`™` as structural geometric elements, not legal text.
- **Technical assets:** crosshairs (`+`) at grid intersections, barcode vertical lines, thick horizontal warning stripes, randomized string data (`REV 2.6`, `UNIT / D-01`).

## Textural / post-processing effects
Engineer simulated analog degradation via CSS/SVG to avoid a purely digital feel.
- **Halftone / 1-bit dithering:** continuous-tone images or large serif type → dot-matrix; `mix-blend-mode: multiply` + SVG radial dot patterns.
- **CRT scanlines:** `repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)`.
- **Mechanical noise:** global low-opacity SVG static/noise on the DOM root.

## Web engineering directives
1. **Grid determinism:** `display: grid; gap: 1px;` with contrasting parent/child backgrounds → razor-thin dividing lines without complex borders.
2. **Semantic rigidity:** `<data>`, `<samp>`, `<kbd>`, `<output>`, `<dl>` to reflect the technical nature.
3. **Typography clamping:** `clamp()` for macro-type so it scales aggressively while keeping structural integrity.

Note: this aesthetic intentionally overrides several global defaults (it uses uppercase, mono everywhere, hazard red, sharp corners). When it conflicts with the main SKILL.md design directives, the brutalist direction wins **for this brief only** — but the em-dash ban, reduced-motion, and a11y contrast rules still apply.
