# Performance Checklist

Quick reference for web application performance. Measure before optimizing — premature optimization adds complexity without improving what matters.

## Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## Where to Start Measuring (Decision Tree)

```
What is slow?
├── First page load
│   ├── Large bundle? → Measure bundle size, check code splitting
│   ├── Slow server response? → Measure TTFB in DevTools Network waterfall
│   │   ├── DNS long? → add dns-prefetch / preconnect for known origins
│   │   ├── TCP/TLS long? → Enable HTTP/2, check edge deployment
│   │   └── Waiting (server) long? → Profile backend, check queries and caching
│   └── Render-blocking resources? → Check network waterfall for CSS/JS blocking
├── Interaction feels sluggish
│   ├── UI freezes on click? → Profile main thread, look for long tasks (>50ms)
│   ├── Form input lag? → Check re-renders, controlled component overhead
│   └── Animation jank? → Check layout thrashing, forced reflows
├── Page after navigation
│   ├── Data loading? → Measure API response times, check for waterfalls
│   └── Client rendering? → Profile component render time, check N+1 fetches
└── Backend / API
    ├── Single endpoint slow? → Profile database queries, check indexes
    ├── All endpoints slow? → Check connection pool, memory, CPU
    └── Intermittent slowness? → Check for lock contention, GC pauses, external deps
```

## Frontend Checklist

### Images
- [ ] Images use modern formats (WebP, AVIF)
- [ ] Images are responsively sized (`srcset` and `sizes`)
- [ ] Images and `<source>` elements have explicit `width` and `height` (prevents CLS)
- [ ] Below-the-fold images use `loading="lazy"` and `decoding="async"`
- [ ] Hero/LCP images use `fetchpriority="high"` and no lazy loading

### JavaScript
- [ ] Bundle size under 200KB gzipped (initial load)
- [ ] Code splitting with dynamic `import()` for routes and heavy features
- [ ] Tree shaking enabled (verify dependency ships ESM and marks `sideEffects: false`)
- [ ] No blocking JavaScript in `<head>` (use `defer` or `async`)
- [ ] `React.memo()` on expensive components that re-render with same props
- [ ] `useMemo()` / `useCallback()` only where profiling shows benefit
- [ ] Long tasks (> 50ms) broken up to keep main thread available (main lever for INP)
- [ ] Non-critical work deferred out of event handlers (analytics, logging)
- [ ] Third-party scripts loaded with `async`/`defer`, audited for size

### CSS
- [ ] Critical CSS inlined or preloaded
- [ ] No render-blocking CSS for non-critical styles
- [ ] No CSS-in-JS runtime cost in production (use extraction)

### Fonts
- [ ] Limited to 2–3 font families, 2–3 weights each
- [ ] WOFF2 format only (smallest, universal support)
- [ ] Self-hosted when possible (third-party font CDNs add round-trips)
- [ ] LCP-critical fonts preloaded: `<link rel="preload" as="font" type="font/woff2" crossorigin>`
- [ ] `font-display: swap` (or `optional` for non-critical) to avoid FOIT
- [ ] Subsetted via `unicode-range` to ship only needed glyphs
- [ ] Fallback font metrics adjusted with `size-adjust`, `ascent-override` to reduce CLS

### Network
- [ ] Static assets cached with long `max-age` + content hashing
- [ ] API responses cached where appropriate (`Cache-Control`)
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] Resources preconnected for known origins
- [ ] No unnecessary redirects

### Rendering
- [ ] No layout thrashing (forced synchronous layouts)
- [ ] Animations use `transform` and `opacity` (GPU-accelerated)
- [ ] Long lists use virtualization (e.g., `react-window`)
- [ ] Off-screen sections use `content-visibility: auto`

## Performance Budget

```
JavaScript bundle:    < 200KB gzipped (initial load)
CSS:                  < 50KB gzipped
Images:              < 200KB per image (above the fold)
Fonts:               < 100KB total
API response time:   < 200ms (p95)
Time to Interactive: < 3.5s on 4G
Lighthouse score:    ≥ 90
```

## Common Anti-Patterns

| Anti-Pattern | Impact | Fix |
|---|---|---|
| N+1 queries | Linear DB load growth | Use joins/includes or batch loading |
| Unbounded queries | Memory exhaustion | Always paginate, add LIMIT |
| Layout thrashing | Jank, dropped frames | Batch DOM reads, then batch writes |
| Unoptimized images | Slow LCP, wasted bandwidth | WebP, responsive sizes, lazy load |
| Large bundles | Slow Time to Interactive | Code split, tree shake, audit deps |
| Blocking main thread | Poor INP, unresponsive UI | Chunk long tasks, offload to Workers |
| Memory leaks | Growing memory, crash | Clean up listeners, intervals, refs |
| Unnecessary re-renders | UI lag, wasted CPU | Profile first, then React.memo/useMemo |

## React-Specific Fixes

```tsx
// BAD: Creates new object every render, children always re-render
function TaskList() {
  return <TaskFilters options={{ sortBy: 'date', order: 'desc' }} />;
}

// GOOD: Stable reference
const DEFAULT_OPTIONS = { sortBy: 'date', order: 'desc' } as const;
function TaskList() {
  return <TaskFilters options={DEFAULT_OPTIONS} />;
}

// Route-level code splitting
const SettingsPage = lazy(() => import('./pages/Settings'));
function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <SettingsPage />
    </Suspense>
  );
}
```
