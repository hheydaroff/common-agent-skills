# Frontend design and validation

Applies to any Fabric app UI; chart/DAX specifics assume the data-app path. Template-specific file paths differ
(`src/queries/` vs `packages/frontend/src/queries/`; spacing tokens `p-l gap-m` vs `p-400 gap-300`): read the target's
`global.css` and `AGENTS.md` before copying a rule.

## Build order
1. Resolve the data source first (never from words like "dashboard"); then a runnable honest shell early (title, final layout regions, loading states) while discovery continues. Never put invented numbers in the shell; run each real query before writing code that consumes its columns.
2. Hero slice first: one real chart end to end, then widen. Deploy only at milestones: `rayfin up` is a slow round trip. A headless preview (spec + DAX file -> PNG + JSON report with `ok`, `dataRows`, `diagnostics`) is far cheaper; `dataRows: 0` means the encoding names do not match the mapped keys. Never ship an empty tile.
3. Delegation: parallelise only substantial independent work with a clear interface; keep small coupled apps cohesive; never run pack/install/typecheck builds concurrently.
4. Mock data only when the user asked for a mock-up, labelled visibly in the UI. (Older Microsoft sample says "NEVER"; the newer template allows labelled samples on request.) A failed query never falls back to sample data.

## Visuals (`@microsoft/fabric-visuals`, `@microsoft/fabric-datagrid`)
- `VegaVisual` for charts and `DataGrid` for tables, fed `toDataTable(data.table, columnMetadata)` and `theme={useCssTheme()}`. Anything else: ask the user first; if refused, hand-build.
- `columnMetadata` per column: `name` (key with `. [ ] \ " '` stripped, used in Vega-Lite fields), `displayName`, `format` (omit for text). Do not hardcode `format` in Vega-Lite JSON; the visual applies it to axes, legends, labels, tooltips. `cellRenderer` disables the column format (the renderer must format).
- Specs: a unit spec OR `layer`, never `mark` with `layer` at the same level. A `params` selection belongs to ONE mark: declare it inside the owning layer, not top-level of a multi-entry layer. Integer years are `quantitative` (`temporal` reads numbers as epoch ms: axis ".905"). Do not paste a full `config` block (breaks the token cascade); use `configVegaLite`. No `interpolate` on line/area; dual-Y = one nested layer per axis. Type every spec with `VisualizationSpec`; specs live in `.json`/factories, never inline in components.
- Named multi-dataset `data={{ detail, summary }}` with layers binding `{"data":{"name":"detail"}}`; fields must match in name and type across bound tables.
- Colour: legend only when more than one series; shared categorical map with `scale.domain` and `scale.range` of EQUAL length from discovered distinct values; custom data colours >= 3:1 contrast against the chart background and alternating so neighbours differ. Zero baseline: always keep zero on bars; a line-chart zero rule is unsettled between templates.
- Chart containers: spec `width/height: "container"`; constrain the dashboard wrapper's max-width, not each chart. Complete height chain (grid cell -> card `h-full` -> `flex-1 min-h-0` -> wrapper -> VegaVisual); never a fixed-height wrapper; standalone sections need explicit `height`, not only `minHeight`; DataGrid's parent needs `overflow-auto flex-1 min-h-0`. Chart titles as card headings, not spec `title`.
- Design: choose one-word tone + a signature detail; set tokens in `global.css` first (colours in `@theme` AND `.dark`, radius, fonts; avoid Arial/Inter/Roboto), then build; no raw colours/px/fonts in components; min text `text-200`; light/dark via `useAppTheme`; keyboard focus and disabled states. tailwind-merge groups every `text-*`: use `text-[length:var(--text-300)]` inside `cn()` or the size or colour class is silently dropped. `font-family: inherit` on form controls.
- Every async region needs loading, empty and error. Permanent errors surface as actionable sanitized messages, never endless loading.
- "Unknown" is a state: show N/A, never 0 (a room with no calendar is grey, not 0%). Insight kernels stay deterministic with evidence; never rank an aggregate against its own finer series; balances carry a directionality flag so they never read favourable/unfavourable; outliers need >= 6 points.

## Patterns worth copying from community apps
- Config-driven shell: add a page = push a `PageDef`; add a chart = return another spec; engine opt-in per visual with a dependency-free fallback so heavy SDKs can be dropped.
- Real exports: zero-dependency `.xlsx` (numbers stay numeric); CSV with a formula-injection neutraliser (cells starting `= + - @ \t \r` get a leading `'`); PPTX via dynamic import; print stylesheet for PDF.
- Accessibility baseline: SVG charts with an sr-only data table and keyboard traversal; `role="img"` with spoken `aria-label` on micro-visuals; focus-trapped mobile sheet; >= 36 px targets; reduced-motion aware animation; Playwright + `@axe-core/playwright` failing on serious/critical for wcag2a/2aa/21a/21aa.
- Fail-closed release lever: one config file read by both the app and the build; an unknown or missing value withholds the feature.
- Provenance stamps on numbers (`measured` / `derived` / `synthetic`); refuse questions the data cannot answer honestly.
- Lazy-load heavy SDKs behind a memoized dynamic import; size-budget script in CI.

## Keeping the page dumb
Enforce it with a CI lint rather than prose: scan the page and query files for arithmetic on query results (`+ - * /` on fields, `reduce`, `Math.`) and fail; every figure is a model measure. `scripts/rayfin-lint.mjs` does not check data-app wiring (connector in both maps, error channels, `?raw` queries); verify those in review or add your own lint.

## Tests that mean something
Assert rendered state, not flags (pixels from the canvas, not `aria-pressed` or `.visible`; a shader failure leaves `visible===true`). Pair each "withheld" test with a "still offered" mirror. Sabotage-check a new guard (break the code, watch the test fail). Derive fixtures from real column shapes. Put reconciliation invariants under unit test. Specs for pure `src/lib` utilities and query factories (assert query string, metadata, spec changes); no coverage-padding tests. Fixture-drift guard: a test that fails printing the expected digest when a base starter changes.

## Failures that only happen in the Fabric host
Local dev shows "Not running inside a Fabric iframe" for embedded data apps, the CLI returns JSON not Arrow, and `validate:visual` renders fixtures, so some defects (BigInt, CSP, first-render nulls) appear only after `rayfin up` inside the portal. Recipe:
1. Add a temporary diagnostics panel (memory-only, rendered in the page) that logs per query: column names with `dataType`, `typeof` of row 0 per column, status/error category, row count, and the chart `onEvent` errors.
2. Ask the user to redeploy and paste the PANEL text. Never ask for the raw console (noisy, third-party errors).
3. Fix the one thing the panel shows, redeploy, repeat. Do not stack speculative fixes (an unproven CSP theory changed a visual import without evidence; revert such guesses if they make no difference).
4. Remove the panel and its logging hooks before committing; then typecheck, test and build again.

**Definition of done for a data app:** one real load in the Fabric host (or the deployed URL per posture) showing every KPI, chart and map with real values, not just green gates. Say "deployed and verified" only after that.

## Validate in a real browser, not by build success
1. Static gates once, serially: typecheck, build, lint, test, plus pack validators (`validate:visual`: `complete | incomplete | failed`, coverage `none|partial|complete`; zero schemas checked + runtime-built specs -> nonzero exit unless `validate:visual:preview`; partial still needs the browser). `validate:functions` must list every `udf.func()` in `AppFunctionsSchema`.
2. Browser on the DEPLOYED hosting URL in a fresh session, per posture (auth-and-security.md), and the Fabric host if embedded. Legacy embedded-only sample: only inside the Fabric portal embed, never directly on localhost (`npm run test:fabric`).
3. Checks: regions render; loading settles; own console errors only (filter by source URL `http://localhost:5173`; ignore `js.monitor.azure.com`, `fabric.microsoft.com/.../powerbiportal.`, `.pbi*.powerbi.com/static/js/`); computed padding/gap non-zero (zero = invalid token class); chart canvas height (< ~100 px suspicious, < ~50 px squished); chart background equals card background; bar/arc stroke equals card background; consistent axis label colours; no auto data labels on multi-series bars; compare fontSize/fontFamily/colour across toolbar controls via `page.evaluate`; keyboard focus, contrast, reduced motion; desktop and mobile widths (an invisible delete button on touch was caught this way).
4. Data accuracy: trace one displayed value to the source by invoking the exact query file through the connector and explaining every transform; check dates, currency, percentages, grids and custom cards independently. Power-of-ten difference = fixed-decimal scaling (data-apps-semantic-model.md).
5. Playwright: `initial_wait: 1` (20-40 s once for the first portal open), accessibility `snapshot` rather than screenshots unless asked; never automate or mock the real Entra sign-in: use a persistent profile and let the user sign in once. Portal-in-localhost iframe needs the Local Network Access flags: launch Edge with `--disable-features=BlockInsecurePrivateNetworkRequests,PrivateNetworkAccessRespectPreflightResults,LocalNetworkAccessChecks` and have Vite send `Access-Control-Allow-Private-Network: true` (`chrome-error://chromewebdata/`, `net::ERR_BLOCKED_BY_LOCAL_NETWORK_ACCESS_CHECKS` otherwise). Embed URL: `<portal>/groups/<ws>/appbackends/<item>?experience=power-bi&devUri=<urlencoded http://localhost:5173>` (double-quote it because of `&`).
6. For two-engine products, add the parity/A-B ladder (deploy-and-ci.md) and a self-describing debugging record (static-engine-patterns.md, Logs tab).
