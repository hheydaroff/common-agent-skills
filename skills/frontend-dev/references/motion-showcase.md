# Motion Showcase (design → animated loop → MP4/GIF)

Load when the request is to **animate a static design** — a Figma frame, screenshot, dashboard, card set, app screen, or a UI on a photo background — or when a section needs product-mockup motion (bento/feature cards with a visual) or the page needs a moving `demo-preview.mp4` / loopable hero video.

> **Source:** adapted from [elayadesign/ai-design-skills](https://github.com/elayadesign/ai-design-skills) `skills/design-to-motion` (MIT, © 2026 Elaya — see bottom). Upstream is a 3-part system for pixel-exact Figma animation; this file keeps the motion, verification and export core and compresses the Figma-API layer surgery into §A2. Local patches marked **[adapted]**, mostly scoping so it cannot contradict the parent `SKILL.md`.

**The contract:** exact frame → empty state → smooth load → every visual acts out its story → seamless repeat.

**Precedence.** A framework default loses to this file. The parent `SKILL.md` wins over this file. The user's explicit prompt wins over both.

## Scope

**Not for** interaction motion inside a shipping product — hovers, menus, toasts, scroll reveals. Use the parent skill §2 and `motion-recipes.md` for those; this file owns *the animation of a designed artifact*, not UI feedback.

## Two contexts — decide first

| | **Showcase** (a design to animate) | **Website** (motion inside our page) |
|---|---|---|
| Trigger | "animate this design", a Figma link/dashboard/card set and nothing else | Building or editing a page, or the request names one |
| Animated | The whole frame | Only sections that contain a visual |
| Start | Page load, from the empty state | Section scrolls into view, once |
| After intro | Stories run, frame dissolves back to empty, cycle repeats | Stories run until the section leaves the viewport; no dissolve |
| Text | Exported layers, so the frame is pixel exact **[adapted]** acceptable *only* inside the recorded artifact | Live HTML text — SEO and accessibility win |
| Ship | The page + `-x.mp4`, `-loop.gif`, `-800x500.gif` | The animated sections in our code; exports only when asked |

Inside a site's codebase assume **website**; with only a design and no site assume **showcase**. If still unclear, ask once.

### Website: which sections get what

| Section | Apply |
|---|---|
| Bento / feature cards (text + a visual: chart, list, flow, calendar, prompt, player) | Card intro on scroll (`card` kind, text included), then a story loop on the card's visual. Main use |
| Product or dashboard mockup hero | Loading intro on scroll: surfaces stay, contents load. **Ask** before adding stories after load — never add them unasked |
| Logo rows, integrations | Marquee, or a gentle light-up story |
| Text-only sections: headline blocks, testimonials, FAQ, pricing, CTA, footer | **Not this file.** Parent §2 reveals / `landing-page-design.md` B7 |

Website rules: `IntersectionObserver` at ~30% visibility, play once, never a scroll listener. Pause the clock when the section leaves the viewport. Stagger in reading order *inside* the section only. Use the site's own tokens, radii and fonts — fidelity is compared section by section. `prefers-reduced-motion: reduce` renders each section in its final state, no stories.

---

# Part A — Fidelity

## A1. Source of truth

Best to worst: Figma node link → flat screenshot → verbal description. Note the frame's absolute origin; every layer position is `absolute bounds − origin`. Render the reference PNG at 2x/3x and compare against it — that image, not your memory of it, is the truth. If the source is a flat image, say plainly which parts cannot be separated before animating them; never fake fidelity by animating a screenshot as one block.

## A2. Layer export (compressed)

Export every element that will move as its own PNG at **3x**, batched ~20 ids per call (Figma `/v1/images`). Read the token from an env var or keychain — never print, echo, or commit it.

| Case | Placement |
|---|---|
| PNG size == render bounds (text always) | Place at the render bounds |
| PNG larger than the render bounds (parent clipped, even overhang) | Centre it: `x = bbox.x − (pngW − bbox.w) / 2` |
| Uneven overhang (arrowheads, single square cap) | Use `strokeGeometry` / `fillGeometry` bounds instead of a formula |
| Blurred blobs, arcs, donuts, oversized patterns, zero-size strokes | Export with `use_absolute_bounds=true`, then crop to the surface where needed |
| Instance children (`I12:34;56:78`) | Often null — export the parent instance |
| Photo baked into a bigger layer | Export the photo node separately too; cover the baked one with a skeleton, put the separate photo on top for the `photo` resolve |

Frame-exactness rules:

- **Keep the source z order.** Static layers may sit between animated ones.
- **Frame strokes draw above children.** Render a card's stroke as a separate overlay above its clipped content, then verify — a glow inside the card can tint the stroke.
- **Containers whose children move separately must be rebuilt in CSS** from node data (fills, radii, inside strokes, effects) — any frame export bakes its children in.
- **Shadows:** Figma blur `R` → `box-shadow` blur `R` on one element, or `filter: drop-shadow()` blur `≈ R / 2` on a group. A shadow on a *group of joined surfaces* must be one `drop-shadow()` on the union, otherwise neighbours darken where surfaces overlap. Separate cards carry their own shadow inside their unit so it moves with them.
- Skip `visible: false` layers and stray layers under opaque shapes.
- **Drawing a line on:** Figma outlines strokes, so there is no centreline — write one yourself as a `<path>` in a mask (`pathLength="1"`, `stroke-dasharray/offset` 1 → 0) over the exported PNG, wide stroke to cover antialiasing. Read corner radii from `strokeGeometry`: centreline radius = inner radius + half stroke.

## A3. Background is sacred

When the design sits on a photo or texture, that background is part of the design.

- **It never changes** — not in the intro, the loop, the dissolve, or any zoom. Never moves, blurs, scales, fades or recolours.
- Every variant keeps it. Never swap in a flat colour silently; if it cannot be reproduced, say so before building.
- **Export the original image**, not a render; apply its scale mode / transform as `background-size` and `background-position`.
- **Frosted panels must see the photo:** a `backdrop-filter` surface is its own element, a *sibling* above the background — never inside an ancestor with `filter` or `opacity < 1`. Headless Chrome only renders it with `transform: translateZ(0)` and a `z-index`.
- Photos as high-quality JPEG/WebP, not PNG.

## A4. Layout: app frame or separate cards

**App frame** — joined surfaces (sidebar + body, often overlapping a few px) forming one unit. Only this layout gets *static* surfaces: they are present, opaque and still from the first frame and never fade/slide/blur in; only the contents load. Keep the stacking where they meet so neither surface can draw over the other.

**Separate cards** — bento grids, card sets, widgets with gaps: **not** joined. Each card rises in with blur (`card` kind), staggered in reading order, contents following inside it. Empty state is the background alone.

Both: each container clips its own contents to its exact radii (nothing overflows onto a neighbour); photo-shaped surfaces get an average-colour placeholder that the photo loads into; trays/toolbars/inner panels load like any other element.

```html
<div class="clip" style="left:113px;top:138px;width:305px;height:907px;border-radius:16px 0 0 16px">
  <div class="cin" style="left:-113px;top:-138px"><!-- units in stage coordinates --></div>
</div>
```
```css
.clip { position: absolute; overflow: hidden; isolation: isolate; }
.cin  { position: absolute; width: var(--stage-w); height: var(--stage-h); }
```

---

# Part B — Motion system

## B1. Start empty

The first frame of every load and every export is the **empty state**. Never open on the finished frame.

- App frame → background + static joined surfaces only.
- Separate cards → the background alone.

## B2. Loading choreography

Elements **rise from below and resolve from blur to sharp**, staggered. Slow, soft, never bouncy.

| Kind | Use for | From |
|---|---|---|
| `card` | Separate cards as a whole, with their shadow | `translateY(24px)`, `scale(0.985)`, `blur(6px)`, opacity 0 |
| `up` | Text, headers, values, rows | `translateY(10px)`, `blur(4px)`, opacity 0 |
| `down` | Top toolbars, top bars | `translateY(-8px)`, `blur(4px)` |
| `left` | Sidebar items, list rows, labels | `translateX(-10px)`, `blur(4px)` |
| `pop` | Icons, badges, avatars, buttons, dots | `scale(0.82–0.88)` from own centre, `blur(4px)` |
| `photo` | Images | shimmer skeleton, then `blur(14px) saturate(0.6)` → sharp |
| `wipe` | Bars, fills, highlights | left→right `clip-path` in pixels on the full-stage unit (§C1): right inset `stageW − x` → `stageW − (x + w)` |
| `line` / `grow` | Rules, ticks, timelines | `scaleX(0)` / `scaleY(0)` from the start edge |
| `donut` | Rings, gauges | conic mask sweeping clockwise from 12 o'clock |
| `tray` / `rise` | Sheets, trays, folders | slide up 40px from inside the container's bottom edge, clipped by it |
| `fade` | Layers under another layer | opacity only |

- **Order:** containers in reading order 80–90ms apart; inside a container header → labels → values → visuals; group items 30–80ms apart.
- **Never `scale(0)`** on an object — only lines and bars grow from zero, because they draw.
- **Covered layers arrive last and leave first** (weeks under a meeting tray): they appear after their cover lands and exit faster in the dissolve, so they never ghost through.
- Skeleton geometry matches the real shape and sits 1px inside it, so no halo shows.
- Full-frame intro ≈ 2–2.5s.

## B3. Bars fill like progress

Data bars, meters, highlights = left→right `clip-path` wipe with the in-out curve, 0.7–1.1s. **Never add loading lines** or any shape that is not in the design — only shapes that exist in the design animate.

## B4. Story loops — the main act

A frame that loads in and then sits with a few pulses is unfinished. Every visual **acts out what it does**, looping. Write the story in one sentence per visual *before* building: "a new lead lands on top and the older ones settle back".

| Visual | Story |
|---|---|
| Stack of items (leads, notifications, files) | A new item lands on top with a blur, the others step back one slot, the last leaves |
| Line / area chart | A scrubber glides across, dots ride the curves, the tooltip value counts. Or the line redraws, a marker pops, numbers count with it |
| Bar chart, equalizer, cell grid | Bars breathe like a live feed and settle back to the design heights; a dot and tooltip ride the active bar |
| Donut, gauge | Segments ease outward one at a time and back. Or the ring sweeps again clockwise |
| Table, list | A cursor inspects rows one by one, the row highlights, a preview loads. Or a soft highlight steps down |
| Calendar, scheduler | A highlight searches for an open slot, the event glides into it, then back |
| Flow, connectors, pipeline | Pulses travel in the flow direction, nodes light as a pulse passes, dashed lines march |
| AI, prompt, form | The prompt deletes and retypes, chips evaluate one by one, the result appears with a blur |
| Counters, KPIs | Numbers count up together with the chart that drives them |
| Profile, long content | Content scrolls slowly inside its clip, then returns |
| Logo row | Continuous marquee moving exactly one full set per loop, so it repeats seamlessly |
| Media player | Handle and progress advance while the play button pulses |

**Rules**

- **Start and end on the exact design.** Leave the frame, act, return. At rest the frame equals `?still`.
- **Use the design's own elements.** Helpers a story needs (cursor, duplicate stack items, extra pulses) must match the design's style and be hidden in `?still`.
- **Change text only when that is the point** — counters, typing, tooltip values.
  - **Typing** reveals the exported text layer **glyph by glyph**, never as a smooth wipe: find glyph boundaries from empty alpha columns of the text PNG, step one glyph every 45–70ms, caret at the edge blinking 1s while idle; deleting runs the same steps backwards, a little faster.
  - **Counters** need live text in the design's font at exact size and weight, landing on the design's exact text at rest.
- **Obvious, not busy.** Every card with a story shows a clear action every 1–2s. If a viewer cannot tell it is animated within two seconds, the stories are too timid. Calm screens (document dashboards) may rest after load — ask once.
- **Text-only cards get no story.** They rise in with their card and rest. Not every card needs to move; every *visual* does.
- **Readable at the smallest export.** If a moving element is under ~4px in the 800×500 GIF, enlarge it within the design's style, add a halo, or pick a bigger story.
- **Offset the cards** so attention travels around the frame in reading order; never unison.
- One story per card, 3–8s; a short story may repeat inside the cycle, and a second run may vary a beat. Every run ends at rest before the dissolve.

Stories are eased keyframe tracks on the JS clock, so capture stays deterministic:

```js
// [[time, value], ...] eased per segment; values may be numbers or arrays
function track(keys, t, ease = easeInOut) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t1, v1] = keys[i], [t0, v0] = keys[i - 1];
    if (t <= t1) {
      const k = ease(Math.min(1, (t - t0) / (t1 - t0 || 1)));
      return Array.isArray(v0) ? v0.map((v, j) => v + (v1[j] - v) * k) : v0 + (v1 - v0) * k;
    }
  }
  return keys[keys.length - 1][1];
}
```

**Accents** sit on top of stories, never instead of them:

| Accent | Use for | Values |
|---|---|---|
| Pulse ring | Status dots, live indicators, play buttons | 1.8–2.2s period, ring scale 1 → 2.6, opacity 0.55 → 0 |
| Heartbeat | Hearts, likes, sparkles | +20% over 0.35s, every 3s |
| Gentle bob | Floating objects (folders, devices, cards in cards) | ±2.6px, 2.8s sine |
| Sheen sweep | Photos, bars, buttons | band 38% of element width, peak 34% white, 1.5s pass every 3.4s. Invisible on light grey — use a refill story instead |
| Skeleton glimmer | Placeholder lines inside the design | 2.4s shimmer |

Stories and accents start when the intro has landed (~2.4s); accents and helpers fade in over 0.6s.

## B5. The cycle (showcase only)

| Phase | Default |
|---|---|
| Build in | 0 → 2.4s |
| Stories | 2.4 → 11.0s |
| Dissolve | 11.0 → 11.6s (opacity 0.5s) |
| Empty beat | 11.6 → 12.0s |

- The story phase holds **at least one full story of every card** — lengthen the cycle rather than cutting a story short.
- Dissolve back to the empty state (B1): for an app frame only the contents dissolve, the joined surfaces stay; separate cards dissolve too; the background never dissolves.
- **Reset everything.** One frame with transitions disabled resets the CSS, but every JS-driven value (masks, tracks, helpers, typed text, pulses) must be reset too, or it ghosts through the empty beat. End of cycle must equal its start.
- A website has no cycle: intro plays once on scroll, stories run until the section leaves the viewport.

## B6. Easing and timing

Use the parent skill's curves (§2.5) for transforms/opacity; this file's `--io` curve `cubic-bezier(0.65, 0, 0.35, 1)` for wipes, fills, sweeps and camera moves; `linear` only for constant motion (shimmer, playback). Never default `ease`.

| Element | Value |
|---|---|
| Transform entrance | 1.05s with `cubic-bezier(0.16, 1, 0.3, 1)` |
| Opacity / blur | 0.7–0.8s with `cubic-bezier(0.33, 1, 0.68, 1)` |
| Wipe | 0.7s; slow bars 1.1s |
| Card rise | 24px, `scale(0.985)`, `blur(6px)`, 0.9s transform, 0.6s opacity |

**[adapted] Timing exception, tightly scoped.** Showcase motion is slower than product UI on purpose, so the parent's "micro-interactions under 300ms" rule does **not** apply inside a showcase recording or a section's intro. It still governs every interaction on the live page — hovers, buttons, menus. Never cite this exception for product UI.

## B7. Camera

**No zoom, no pan** by default; the user has to ask. When asked: only the app frame scales toward the items, the background never moves (§A3), moves use `--io`, and the frame returns to rest before the dissolve. **[adapted]** This does not lower the parent's MOTION_INTENSITY dial for the page itself — it only says a fidelity-driven showcase must not invent camera moves the design does not have.

## B8. Performance and accessibility

Animate `transform`, `opacity`, `filter`, `clip-path` only — never `top`, `left`, `width`, `height`. Animated blur ≤ 14px (static `backdrop-filter` is fine). CSS transitions for the intro; the JS clock only for time-based effects. `prefers-reduced-motion: reduce` renders the still frame.

---

# Part C — Recording and export

## C1. Page architecture (showcase)

One self-contained HTML file: a fixed stage at the frame's exact size, scaled to fit the viewport; images inline as base64, deduplicated; wait for `<img>` decode only (CSS gradients are not images).

- **Modes:** `?still` exact frame, no motion (also the reduced-motion rendering) · `?loop` repeats the cycle · `?capture` disables `requestAnimationFrame` and exposes `window.__start()`, `window.__tick(dt)`, `window.__lt`.
- **Units:** every animated element wraps in a full-stage `.u` with its delay `--d`; the intro is CSS transitions keyed on `.stage.in`. Because a unit covers the whole stage, percentages in `clip-path`/`transform-origin` refer to the stage — use pixel values from the element's rectangle.
- **Static layers stay composited:** give clips and stroke overlays `transform: translateZ(0)`, or a 1px edge flickers at every cycle start.
- **One JS clock** drives everything time-based (masks, sweeps, stories, accents), driven from loop time and never wall clock.

## C2. Deterministic capture

Never screen-record in real time. Step a fake clock and screenshot every frame:

```js
await page.clock.install({ time: 0 });
await page.goto(url + '?capture', { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.clock.pauseAt(10000);
for (let i = 0; i < frames; i++) {
  // whole-ms steps averaging exactly 1000/60 (17,17,16,...); runFor(1000/60) drifts
  const dt = Math.round((i + 1) * 1000 / 60) - Math.round(i * 1000 / 60);
  await page.clock.runFor(dt);
  await page.evaluate(([i, PRE, dt]) => {
    if (i === PRE) window.__start();          // start inside the same evaluate as the seek
    if (i >= PRE) window.__tick(dt / 1000);   // page clock advances here, never through rAF
    const now = performance.now();
    for (const a of document.getAnimations()) {  // CSS transitions follow the fake clock
      a.__m ??= window.__mark;                   // keep the mark each was created under
      a.pause(); a.currentTime = Math.max(0, now - a.__m);
    }
  }, [i, PRE, dt]);
  await page.screenshot({ path: `${out}/${String(i).padStart(5, '0')}.png` });
}
```

Page side: every change of the stage's state classes (`in`, `out`, reset) sets `window.__mark = performance.now()`; `__tick(dt)` advances loop time, runs the phases, draws stories/accents and sets `__lt`. Endless loops (shimmer, marquee) must be driven by the JS clock — infinite CSS keyframes get restarted by the seek.

`PRE` is ~15 settle frames before the start. Viewport = frame size, `deviceScaleFactor = min(1920 / W, 1200 / H)`; screenshots may come out one pixel odd, so the even-dimension crop in C3 handles it. The export window starts at frame `PRE − 1` (loop time 0) and spans exactly `cycle × 60` frames; record ≥10 frames past it for the seam check.

## C3. Formats

| File | Spec |
|---|---|
| `<name>-x.mp4` | H.264, `yuv420p`, 60fps, CRF 14–15, preset slow, `+faststart`, max 1920×1200, even dimensions |
| `<name>-loop.gif` | 960px wide, 15–20fps, ~2–3MB, for the page |
| `<name>-800x500.gif` | Always delivered. Wide empty borders → crop to content with ~40px margin at exactly 1.6:1. Content fills the frame → fit and pad with the page background. On a photo background always crop, so no flat band sits beside the photo. 20fps, 12fps if heavy |

```bash
ffmpeg -start_number $A -framerate 60 -i frames/%05d.png -frames:v $N \
  -vf "crop=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -preset slow -crf 15 \
  -pix_fmt yuv420p -movflags +faststart name-x.mp4

ffmpeg -start_number $A -framerate 60 -i frames/%05d.png -filter_complex \
  "trim=end_frame=$N,fps=20,scale=960:-2:flags=lanczos,split[a][b];\
   [a]palettegen=max_colors=192:stats_mode=diff[p];\
   [b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" -loop 0 name-loop.gif
```

For 800×500 add `scale=800:500:force_original_aspect_ratio=decrease,pad=800:500:(ow-iw)/2:(oh-ih)/2:color=<page bg>` before `split`. Keep bayer dithering whenever a photo is in frame or photos band. If a GIF is too heavy, cut frame rate or colours before size.

---

# Verification

**Still (before any motion work).** Render `?still` at 2x, compare with the reference: PSNR after a light blur (`gblur sigma≈1.2`) so sub-pixel antialiasing does not dominate — above 35 dB overall, 30 dB per container (text-heavy containers sit near 30 dB because 3x layers resample to 2x; retest at `sigma≈2.5` if lower). Look at a blurred, amplified difference image for structural errors: glow too high, wrong stacking, missing stroke, shifted shadow. **Do not chase sub-pixel offsets** — measuring at 2x cannot resolve them and "corrections" overshoot.

**Motion (on recorded frames, before encoding).**

- **Overflow** — test with real container shapes, radii included: render a mask of the page's containers (solid white, exact radii, plus shadow area) on black, grow 2px to skip antialiasing, compare black pixels only, at the capture device scale (not the 2x of the still check). App frame: every pixel outside the joined surfaces must equal the empty first frame in every cycle frame (PSNR `inf`). Separate cards: outside the cards (and shadows) every pixel must equal `?still` during the story phase — intro frames excluded, because the cards' own rise moves pixels there.
- **Seam** — the first frame of the export window equals the frame one cycle later.
- **Empty beat** — every empty-beat frame equals the frame before `__start`. The seam check cannot catch un-reset JS state, because both its frames sit at loop time 0; this one can.
- **Rest** — the last frame before the dissolve equals `?still`, proving every story came back.
- **Contact sheet** — tile empty / mid-intro / landed / several story points / mid-dissolve / end, and look for overflow, ghosting, pops, and stories too timid to notice.

# Output format

State before building: **context** (showcase or website, and per-section what it gets), **layout** (app frame vs separate cards, clip shapes), **background** (kept exactly, or what cannot be reproduced), **choreography** (load order, kind per element group), **stories** (one sentence per visual, plus accents), **cycle** (length and phases).

Report after building: still fidelity (overall + worst surface PSNR), overflow and seam results, the three files with size/dimensions/frame rate/duration, and anything not reproduced exactly, named plainly.

# Quick checklist

**Fidelity** — reference frame rendered · every moving element exported with text · z order kept, strokes above children, group shadow on the union · background is the original image, positioned by its transform, verified · every variant keeps the background, frosted panels blur the photo · still matches structurally

**Layout** — app frame's joined surfaces present, opaque and still in the empty state · separate cards rise in themselves, empty state is the background alone · each container clips to its exact radii · overflow check passes

**Motion** — starts empty · rise + blur to sharp, staggered in reading order · bars fill like progress, no invented loading lines · every visual tells a story, starting and ending on the design, text cards rest · stories readable at 800×500 · obvious, offset between cards, only counters/typing change text · covered layers last in, first out · no camera moves unless asked · dissolve resets everything · seam, empty-beat and rest checks pass

**Export** — whole-ms steps averaging 1000/60, start and tick inside the seek, no real-time recording · all three files delivered · token never printed or committed

---

# Source and license

Adapted from `skills/design-to-motion` in [elayadesign/ai-design-skills](https://github.com/elayadesign/ai-design-skills) by Elaya.

Local modifications (all marked **[adapted]** above): landing-page redirection points at the parent `SKILL.md` §2 / `landing-page-design.md` instead of an external product-motion skill; Part A's Figma-API layer-surgery table condensed to §A2; text-as-exported-layers restricted to the recorded showcase artifact (live HTML on the website); the showcase timing exception scoped so it cannot override the parent's product-UI durations; the no-zoom no-pan default scoped so it does not lower the page's MOTION_INTENSITY; easing tokens defer to the parent §2.5 where they overlap; checks and export specs kept intact.

Upstream credits a few general motion rules, adapted not copied, from MIT-licensed [emilkowalski/skills](https://github.com/emilkowalski/skills) (cheap properties only, small blur, never grow from zero, reduced motion), [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) (skeletons shaped like real content, staggered entrances), and [dylantarre/animation-principles](https://github.com/dylantarre/animation-principles) (offsetting sibling loops, loops whose last frame flows into the first).

```
MIT License

Copyright (c) 2026 Elaya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```