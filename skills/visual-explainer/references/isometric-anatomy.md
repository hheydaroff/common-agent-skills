# Isometric "anatomy" figures

Adapted from [`wheresryan22/anatomy`](https://github.com/wheresryan22/anatomy) (MIT, © 2026
Ryan), pinned at `be2fa9b` (v1.1.0). Upstream builds crafted, interactive isometric SVG
figures that explain a technical idea *as a real physical object*: a test rig, a dial
gauge, a pin-tumbler lock, a chest of drawers. This file is the router and the distilled
approach. The kit (iso projection, solids, parts library, SVG renderer, CSS), the deep
references (`craft.md`, `kit.md`, `motion.md`, `webgl.md`, `verify.md`, `3d.md`) and eight
complete examples live upstream and are fetched on demand with `scripts/anatomy-kit.sh`.

## When this rung applies

- Use it when the deliverable is a **crafted illustration**: a hero figure for docs, a
  blog post or a landing page; an interactive explainer; a "show how X works as a
  machine" request; or any ask for an isometric / premium / "Linear-style" technical
  drawing, even when the word *isometric* never appears.
- It is **not** the default for ordinary explanations. The ladder in `SKILL.md` still
  rules: pseudocode, call/component/file trees, `diff`, Mermaid and CSS-card pages come
  first. An anatomy figure is a deliberate, expensive artifact — apply the size gate
  below and say the estimate out loud before building.
- It composes with the rest of this skill: an anatomy figure is still a self-contained
  HTML page in `docs/diagrams/`, and the page-level invariants in `SKILL.md` (overflow,
  fonts, reduced motion, console-clean) still apply. Where this file and `SKILL.md`'s
  generic aesthetic rules disagree (palette, card chrome), this file wins inside the
  figure card, exactly like `smart-brand.md`.

## The one idea that matters

**The object is the explanation.** Don't draw boxes, arrows and labels. Invent a real,
well-made physical thing whose working *is* the concept:

| Concept | Object |
|---|---|
| One shared GPU context serving many canvases | A gantry plotter: one print head visiting 16 wells |
| A cache key that skips work when nothing changed | A pin-tumbler lock: when every pin matches, the plug turns |
| Seven render targets with different bytes per texel | A chest of seven drawers, each as deep as its bytes |
| A separable blur (49×49 taps vs 49+49) | A bed-of-nails stamp beside two combs on rails |
| A spring that presses and leans | A test rig with springs, a probe and a dial gauge |
| Light that depends on facing | A small photo studio: key and fill lamps around a turntable |

Two ways this fails, both seen in practice:

- **Too abstract.** Stacked plates, floating slabs or labelled boxes don't read as anything.
- **Too flat and bland.** One big slab with a few lines has no volume, no parts, nothing to discover.

The fix for both is the same: a recognisable machine, built from many small, precise,
purposeful parts. Every figure is highly detailed, however small the idea: at 1× it reads
as one clear machine; at 4× every region still has something true to find. A bare face or
an empty corner is unfinished work, not calm. Detail comes from parts that belong to the
mechanism — each sits on another part, ends on an edge, fades rather than stops.

## Size gate (say it before you build)

| Size | Scope | Estimate | Rule |
|---|---|---|---|
| Figure | one mechanism, 40–80 parts, ≤1 WebGL layer | 30–90 min | Build without asking |
| Hero | dense object, several WebGL layers or one 3D subject, 80–150 parts | 2–4 h | Say so, then build unless the user asked for something quick |
| Epic | whole vehicle/building/plant, many moving systems | 6 h+ | Do **not** start. Give the estimate, propose a Hero that keeps the core, list what the full version adds. Build only if the user chooses it |

Whatever the size: a working page that opens in the browser within the first hour, then
deepen. Run `date` at each step; when a step runs past twice its share of the estimate,
tell the user where it stands and what is left.

## Workflow (condensed)

1. **Truth first.** Collect the real numbers and behaviour: sizes, counts, thresholds,
   curves. The readout, motion and caption must all be true. Put the model in a small pure
   module (like `rig.ts` in the test-rig example) and drive everything from it.
2. **Invent the object.** Pick a machine whose mechanism maps one-to-one onto the concept.
   Say in one sentence what moves and what that motion means. Never copy a reference
   image: take its finish, not its object.
3. **Parts list before geometry.** ≥40 parts, grouped: base (plate, feet, groove, corner
   screws, label plate, ruler strip), structure (posts, rails, end stops), mechanism
   (carriage, bushings, springs, plunger, needle), controls (knurled knob, thumb screw)
   and the subject — the one lit part. Each part sits on another part.
4. **Plan the world.** World units ≈ 1 px of the real thing; x,y on the floor, z up. Plans
   as rounded rectangles `{x, y, w, d, r}` and circles. Camera: azimuth 45° default
   (35–60° to show a long side), elevation 30° (higher, ~44°, to look into something open).
   Fit with `fitProjection(points, width, height, { pad, azimuth })`.
5. **Build geometry once.** Precompute every static path in a geometry module with the
   kit: `slabOf`, `cylinder`, `extrude`, `planOutline`, `topTicks`, `knurl`, `coil`,
   `radialTicks`. Round parts on any axis from `kit/lathe.mjs`; pipes and cables from
   `kit/tube.mjs`. Moving parts built once at rest, moved with `translateAlong`; only
   shape-changing parts rebuilt per frame.
6. **Paint back to front, bottom to top.** Sort with `depthOf`; split anything that wraps
   another part into a back and a front half (springs around a rod, frame bars around a
   carriage). Once a figure has pipes, cables or round parts, stop tuning keys by eye:
   record shapes with `A.recorder`, let `A.settle` measure true depth, end the build with
   `A.auditOrExit`. A stand-in shape that silences the audit is a bug.
7. **Frame it.** Card with `Fig n` top-left, short title top-right, interaction hint
   bottom-left, live readout bottom-right. Legend keys and a true caption under the card;
   words stay out of the drawing apart from at most one tiny engraved label.
8. **Make it live.** Calm time-based motion: exponential follow or real springs; an idle
   tour loops when nobody touches it. Respond to pointer and keyboard, stop when
   offscreen, go still under reduced motion. Write attributes on refs; never re-render
   per frame.
9. **Verify like a critic** (below). The owner finds faults by zooming in, so zoom in first.

## Craft rules (short form)

- **Solids, not wireframes.** Every part filled in paper colour, painted in order, so
  things in front hide things behind. No see-through edges, no dashed hidden lines.
- **Let the kit shade.** `extrude` returns four side tones by facing plus a lighter top.
  Keep it for anything with height; `flat` only for floors and inlays thinner than 1 unit.
- **Tone hierarchy.** Base and feet `lo`, structure `mid`, subject `hi`. Exactly one accent
  is `lit` (white in dark, black in light): the part the reader should watch. Grooves
  `faint`, minor ticks `lo`, major ticks `mid`, zero mark `hi`. Colour only when colour is
  the subject (e.g. RGB channels).
- **Small precise detail, never noise.** Bevels 0.4–1.6, grooves inset 3–5 from an edge,
  screws as 0.4–0.55 dots with a ring at plate corners, knurls on knobs, ruler ticks every
  4–5 units with a major every 5th, a label plate with three rule lines.
- **Lines resolve.** Every line ends on a face, another line or a terminal dot. Connectors
  are `Wire`s whose terminal dots land on objects. No leader lines, balloons, dimension
  arrows or labels floating in the air.
- **No pipe or cable passes through anything** — not at rest, not apart, not in any frame
  of an explode. ~1.5 radii clearance to everything but its own connection; lines run
  beside the structure, never across the subject's face; gap a pipe wherever a flange,
  band, bellows, clamp or valve wraps it. Parts meet flush, tangent or rim-on-surface,
  never sunk in.
- **Every crossing in true depth order**, proved by `A.settle` and the audit, not tuned by
  eye. Lines cross on straights, well apart in depth. A pair that can't be ordered
  interlocks; the fix is a cut or a tangent contact, never a key bias.
- **Curved surfaces shade smoothly, never in a staircase.** Mark curved knots smooth
  (`[s, r, 1]`); `lathe` shades from one monotone curve that also draws the outline; cut
  long bodies with `G.bandsOf`; `G.sphereOf` for balls. Tone bands taper to nothing; seams
  go under the outline.
- **A texture ends on a real edge or fades.** Ribs, bolt circles, rule lines, seams and
  grooves never stop mid-surface (`ribsOf`/`dotsOf` take `fade`; a rib row ends on its
  seams; a seam on a box wraps its corners; ticks hang from a ruler strip's edge). A
  texture on a pipe follows its cross-section through every chunk joint
  (`tubePieces(…, { rings })`), never a dashed stroke down the centreline.
- **Things on faces fit them.** Text a machine displays fits its window at its widest
  string and is clipped to it; content seen through an opening is clipped by the opening
  as well as by its own plane, with the recess walls drawn.
- **Volume and composition.** Real thickness; things stand on other things; a soft halo
  under the base and under anything lifted. Centre the figure, let it fill ~55–65% of the
  card, keep a consistent scale across a set, and make sure it still reads at 390 px wide.
- **WebGL only for what lines can't draw** (fire, water and caustics, real lamp light,
  steam). Three layers: back SVG, canvas (`pointer-events: none`), front SVG. World space
  in the figure's own camera; every uniform rides an envelope with attack and decay; no
  hard cut-offs; the SVG must still read without WebGL. Read upstream
  `references/webgl.md` before writing any shader.

## Get the kit

```bash
bash <skill-dir>/scripts/anatomy-kit.sh        # prints the cached kit root, clones if absent
```

The script caches the pinned upstream commit under `~/.cache/visual-explainer/anatomy-<sha>`.
Line 1 of its output is machine-readable — `ANATOMY=<path>` with no suffix — so:
`ANAT=$(bash <skill-dir>/scripts/anatomy-kit.sh | head -1 | cut -d= -f2)`. Use it from a Node
build script:

```js
// the cache path is dynamic, so import it dynamically
const ANAT = process.env.ANAT; // exported from the shell line above
const k = await import(`${ANAT}/kit/iso-kit.mjs`);              // core: camera, solids, parts, SVG, CSS
const { kitScript } = await import(`${ANAT}/scripts/inline-kit.mjs`); // inline the kit into a standalone page
```

| File | Use |
|---|---|
| `kit/iso-kit.mjs` | The whole core: `cameraOf`, `iso`, `depthOf`, `fitProjection`, `extrude`, `slabOf`, `cylinder`, `knurl`, `coil`, ticks, `solidSvg`/`lineSvg`/`dotsSvg`/`wireSvg`/`faceTextSvg`, `figureSvg`, `plateHtml`, `pageHtml`, `ISO_CSS` |
| `kit/iso.css` | `ISO_CSS` written out; put `class="iso"` (+ `data-theme="light"`) on the wrapper |
| `kit/lathe.mjs` | Round parts on any axis: `lathe`, `solidOf`, `disc`, `ringBand`, `sphereOf`, `saddleOf`, `bandsOf`, `ribsOf`, `dotsOf`, `rodOut`, `fillet` |
| `kit/tube.mjs` | `tubePieces` (depth-sortable chunks, `gaps` under collars, `rings` for braid/corrugation), `tubeSvg`, `crossingsOf` |
| `kit/audit.mjs` | `recorder` / `settle` / `auditOrExit` — proves clearances, terminals, folds, depth order; the `--audit` hook |
| `kit/gl.mjs`, `kit/gl-shared.mjs` | The WebGL layer inside the drawing (`GLSL_ISO`, `glCamera`, `glLayer`, envelopes `smooth`/`burst`/`settle`) |
| `kit/react/draw.tsx`, `kit/react/live.tsx` | Server-safe React components + `"use client"` hooks (`useReadout`, `useLoop`, `useEased`, `useInView`, `useStillness`) |
| `scripts/capture.mjs` | Headless-Chrome screenshots, close-ups, hover/key states, console + sideways-scroll check |
| `scripts/drive.mjs` | Scripted Chrome: move, click, key, slow motion, contact sheets, `--no-webgl` |
| `scripts/lines.mjs` | The line-end check: every texture line must end on a stroke, a dot or an outline |

**Standalone page recipe** (the `examples/dial-indicator/build.mjs` shape, ~300 lines): a
Node script imports `kit/iso-kit.mjs`, assembles strings with `solidSvg`/`lineSvg`/
`dotsSvg`/`wireSvg`/`faceTextSvg`, wraps with `figureSvg` + `plateHtml`, writes the page
with `pageHtml({ script: kitScript() + live })` — plus `glScript()` when it has a shader.
Build `--light` too. For a lone `.svg` file use `figureSvg({ standalone: "dark" })`.

**React/Next:** copy `kit/` into the project (e.g. `components/iso/`), keep geometry in
plain `.ts` modules, build the static art in a server component with `draw.tsx`, pass it
as element props to one `"use client"` live component. Upstream `references/react.md`
covers the split and a large-payload key-warning trap.

**Offline fallback (no network, no kit).** Hand-roll the same look with plain SVG and the
eight rules that carry it: (1) project with azimuth 45°, elevation 30°:
`X = ox + (x·sinA − y·cosA)·k`, `Y = oy + ((x·cosA + y·sinA)·sinE − z·cosE)·k`, `k = scale·√1.6`;
(2) depth-sort with `d = (x·cosA + y·sinA)·cosE + z·sinE`, paint back to front; (3) four
side tones by facing + a lighter top, base `lo` / structure `mid` / subject `hi` / one
`lit` accent; (4) solids only, no wireframes; (5) every line ends on something; (6) parts
sit on parts, flush or tangent, never sunk in; (7) card frame with Fig n, title, hint,
readout; (8) capture a PNG and read it. Expect a Figure, not a Hero, without the kit.

## Verify like a critic

Read every PNG you make; a check you didn't look at didn't run.

```bash
node $ANATOMY/scripts/capture.mjs page.html --out shots/desk.png
node $ANATOMY/scripts/capture.mjs page.html --out shots/phone.png --width 390
node $ANATOMY/scripts/capture.mjs page.html --out shots/hover.png --hover 0.6,0.5
node $ANATOMY/scripts/capture.mjs page.html --out shots/motion.png --times 400,1200,3000
node $ANATOMY/scripts/lines.mjs   page.html --out shots/lines.png   # must print "line ends: 0"
node build.mjs --audit                                                # must end "audit passed"
```

- Capture prints the clip box, the live readout text, console errors and whether the page
  scrolls sideways — all four must be clean.
- **Run the audit to zero** when the figure has pipes, cables or round parts: clearance at
  rest, apart and mid-flight, terminals, loose ends, folds, self-overlap, crowding,
  stand-in shapes, support, wobble, saddles, depth order. Fix an interlock in the
  geometry, never with a key bias.
- **Run the line check to zero**, on the dark and the `-light` page and in every resting
  pose. Read the ringed PNG.
- **4× close-ups of every junction in both themes**, assembled and apart: every flange,
  tee, elbow, clamp, valve, band and crossing; every curved body (no tone staircase);
  every place a texture ends; every sliding rod at rest and at full stroke.
  `capture.mjs --zoom x,y,w,h --zoom-scale 4` makes the crops.
- **Shaders:** a contact sheet slowed with `drive.mjs` `["slow", 0.05]` across every
  transition; nothing pops, no colour switch. In light, ink per frame must follow the
  light monotonically.
- Put your PNG next to upstream's `examples/*/shots` and ask: is it instantly a real
  object, rich in small parts with volume, every line ending on something? Rewarding at
  4× with no bare face? Iterate until yes. The full checklist is upstream
  `references/verify.md`; the design walkthrough of the test rig is `references/walkthrough.md`.

## Not taken from upstream

- The 3D "figures that turn" mode (`kit/turn*.mjs`, `references/3d.md`) — beta upstream;
  fetch it from the same cache only if the user explicitly asks for a turning 3D subject.
- `scripts/publish.mjs` and the community gallery — never push a figure for the user.
- The eight `examples/` (10 MB of built HTML) — read them in the cache, don't copy them.
