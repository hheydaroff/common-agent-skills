# Motion & GSAP Skeletons

Load when implementing scroll-driven motion. These are tools, not defaults — none fires automatically. Use when the design read calls for them.

## Context-aware proactivity

* **Liquid Glass / Glassmorphism:** premium consumer / Apple-adjacent / media-overlay vibes. Inappropriate for dashboards or "boring B2B". Go beyond `backdrop-blur`: add `border-white/10` and `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`. Solid-fill fallback under `prefers-reduced-transparency`. (See references/liquid-glass.md.)
* **Magnetic micro-physics:** `MOTION_INTENSITY > 5` AND premium/playful/agency. Implement with `useMotionValue`/`useTransform` outside the React render cycle — never `useState`.
* **Perpetual micro-interactions** (pulse, typewriter, float, shimmer): `MOTION_INTENSITY > 5` AND the section benefits. Not every card needs an infinite loop. Spring physics (`type: "spring", stiffness: 100, damping: 20`), no linear easing.
* **"Motion claimed, motion shown."** If `MOTION_INTENSITY > 4`, the page must actually move (hero entry, scroll-reveal on key sections, hover physics on CTAs). If you cannot ship working motion, drop the dial to 3 and ship clean static. Never half-build motion that breaks.
* **Motion must be motivated:** every animation communicates hierarchy, storytelling, feedback, or state transition. "It looked cool" is invalid. If you can't articulate the reason in one sentence, drop it.
* **Marquee max-one-per-page.**

## Forbidden animation patterns

* **`window.addEventListener("scroll", ...)`** — banned. Use `useScroll()`, GSAP `ScrollTrigger`, `IntersectionObserver`, or CSS `animation-timeline: view()`.
* **Custom scroll-progress via `window.scrollY` in React state** — banned (re-renders every frame).
* **`requestAnimationFrame` loops touching React state** — use motion values instead.
* **`layout`/`layoutId`** — for real visible state changes (reordering, expanding modals, shared elements), not wrapped around static content "for safety".
* **Staggered orchestration** — `staggerChildren` (Motion) or CSS `animation-delay: calc(var(--index) * 100ms)`. For `staggerChildren`, parent `variants` and children must share the same Client Component tree.

---

## Sticky-Stack — canonical skeleton

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center">
          {card}
        </div>
      ))}
    </div>
  );
}
```

Critical: `start: "top top"`, `pin: true`, every card except the last is pinned, the scale/opacity transform is driven by the NEXT card's scroll trigger. Common failure: trigger fires halfway through scroll — fix with `start: "top top"` not `"top center"`/`"top 80%"`.

## Horizontal-Pan — canonical skeleton

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">{children}</div>
    </section>
  );
}
```

Critical: `start: "top top"`, `pin: true`, `end: "+=${distance}"`, `scrub: 1`. Common failure: animation starts before the section is pinned — same fix.

## Scroll-Reveal Stagger — lighter alternative (no pinning)

Prefer Motion's `whileInView` over GSAP for simple "enter on scroll" — lighter, no ScrollTrigger:

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

Use for feature lists, testimonial grids, logo walls. Save GSAP for actual pin/scrub work.

---

## Performance & accessibility guardrails

* **Hardware acceleration:** animate ONLY `transform` and `opacity`. Never `top`/`left`/`width`/`height`. `will-change: transform` sparingly, only on elements that animate.
* **Reduced motion (mandatory):** any motion above `MOTION_INTENSITY > 3` honors `prefers-reduced-motion`. Wrap with `useReducedMotion()` or gate CSS behind `@media (prefers-reduced-motion: no-preference)`. Infinite loops, parallax, scroll-hijack, magnetic physics collapse to static.
* **Library isolation:** never mix GSAP/Three.js with Motion in the same component tree (they fight over frames). R3F lives in an isolated `<Canvas>` with its own `'use client'`. Lazy-load Lottie, GSAP, Three.js.
* **Core Web Vitals:** LCP < 2.5s (hero image `priority`/preloaded), INP < 200ms, CLS < 0.1.
* **DOM cost:** grain/noise filters only on fixed `pointer-events-none` pseudo-elements — never on scrolling containers.
* **Z-index restraint:** no arbitrary `z-50`/`z-[9999]` spam. Reserve for systemic layers (sticky nav, modals, overlays, grain).
* **Cleanup:** every `useEffect` with GSAP/observers returns `() => ctx.revert()`.

## Dial definitions (technical)

* **DESIGN_VARIANCE** 1-3 symmetrical grid · 4-7 offsets, varied aspect ratios, left-aligned headers · 8-10 masonry, fractional grids, massive empty zones. Mobile override: 4-10 collapse to single-column `< 768px`.
* **MOTION_INTENSITY** 1-3 CSS hover/active only · 4-7 `transition`/`animation-delay` cascades, transform+opacity · 8-10 scroll-triggered reveals, parallax, ScrollTrigger.
* **VISUAL_DENSITY** 1-3 lots of whitespace (`py-32`-`py-48`) · 4-7 standard app spacing (`py-16`-`py-24`) · 8-10 tight, 1px line separators, `font-mono` for numbers.
