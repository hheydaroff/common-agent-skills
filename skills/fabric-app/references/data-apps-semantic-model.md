# Data apps: a Fabric app over a semantic model

The app registers the model as a `fabric-semanticmodel` connector and sends DAX with `executeQuery`; Power BI runs
it as the signed-in user, so RLS and permissions flow through and the browser holds no Power BI token.
Two lineages exist; use the connector path.
- Connector path (Rayfin 1.34+; Learn page; `universal-app`): `rayfin.yml connectors`, `npx rayfin connector ...`, `useSemanticModelQuery`.
- Legacy path (the `dataapp` sample's client): `@microsoft/fabric-app-data`, `fabric.yaml`, `npx fabric-app-data`, postMessage to the Fabric host, embedded-only. Learn says that if the scaffold includes another semantic-model client, replace its calls with the connector client. Never keep two data paths in one app. Rules below tagged (legacy) apply only there.

## Setup order
1. Prereqs: Execute Queries tenant setting on; every user has Build + Read on the model (platform-and-prereqs.md).
2. Find the model: `npx rayfin connector search "<name>" --type fabric-semanticmodel --all-workspaces --json` (`--type` is required with `--workspace-id`/`--all-workspaces`). Named model: verify exactly one match; several: ask; none: ask. Never substitute sample data or another model. A local `.pbix` is unsupported: ask for the published model.
3. `npx rayfin connector add --type fabric-semanticmodel --workspace-id <id> --item-id <id> --name <alias> --operations executeQuery`. Literal ids only (no `${VAR}`). Install exactly the printed pinned packages in the right workspace (`npm install -w @rayfin-app/frontend <pkgs>` in universal-app); `connector add` installs nothing. Auth must be `delegated` (Category B; `rayfin up` rejects `application`).
4. Register the connector in BOTH `connectorConfigs` and `connectorRuntimes` (`fabricSemanticModel({})`): the runtime decodes the Arrow stream; without it rows are unreadable. The connector name must match in rayfin.yml, the schema type, the config option and the runtime map.
5. Probe before building UI: write `{"query":"EVALUATE TOPN(1, Sales)"}` to a `.query.json` and run `npx rayfin connector invoke <alias> executeQuery --file ./probe.query.json`. `--file` is JSON-parsed, so a bare `.dax` fails; prefer `--file` over `--input` (shells mangle apostrophes silently). Runs under your identity, works before any deploy.
6. A passing probe is necessary, not sufficient. The deployed app re-authorises as the signed-in user via the platform; it can still fail `Unauthorized`. Proven = the deployed app renders real rows for a non-owner user.
7. Connectors do not run under `rayfin dev`; verify after `rayfin up`. In CI the `connectors:` entry has workspace/item GUIDs: write it at deploy time by looking the model up by display name (deploy-and-ci.md).

## Proving per-user RLS
The app inherits the model's RLS; it cannot define it. Before promising per-user rows: ask who owns the model's roles and what each filters (INFO.VIEW may not expose roles or members; elevated INFO calls may fail). Test with at least two non-owner users in DIFFERENT roles and require different totals. Users with write/Edit rights on the model or Admin on the workspace are generally not subject to RLS in Power BI (general Power BI behaviour, not stated in the Rayfin docs), so an author or owner session proves nothing. Guest (B2B) users: whether their UPN (`...#EXT#...`) matches a role rule is undocumented; test one guest account on a pilot before promising anything. [INF]

## Discovery (progressive, never ask the user to describe the schema)
- Scope probe first: one `ROW(...)` of counts over `INFO.VIEW.TABLES/COLUMNS/MEASURES/RELATIONSHIPS`; then tables; then columns and measures of the relevant tables only; relationships only if needed; advanced metadata last.
- Use `INFO.VIEW.*` (read access). `INFO.*` (calc groups, calendars, UDFs, INFO.MODEL) may need elevated rights: after ONE permission failure on an elevated call, skip the rest for the session.
- Narrow with `SELECTCOLUMNS(FILTER(INFO.VIEW.X(), [Table]="T"), ...)`; probe an INFO function's columns with `TOPN(0, INFO.VIEW.COLUMNS())`; list INFO functions with `INFO.STORAGEFUNCTIONS()`.
- Pull `FormatString` for columns and measures now; it goes verbatim into `columnMetadata.format`. A dynamic format string: fetch it next to the value as `IGNORE([Measure Format String])`.
- Batch value probes: one `UNION` query per ~10 columns, `Promise.allSettled` with concurrency ~3, retry a failed batch column by column, skip columns over ~50,000 distinct values and RLS-protected ones.
- Execute Queries REST limits (when going through REST): ~100k rows, 1,000,000 values, ~120 req/min.

## Writing DAX
1. Test every query through the real runtime pipeline (rule 5 above) before app code uses it. Copy output column names verbatim as `columnMetadata` keys (`Products[Region]`, `[Total Revenue]`); never guess or "clean" them.
2. Prefer existing model measures to re-aggregating columns. Columns `'Table'[Column]` (quote tables: Product, Date, Order, Currency, Time, Calendar are keywords); measures `[Measure]` unqualified; variables start with `_` (short names like `d`, `m`, `r`, `step` fail to parse).
3. One `EVALUATE` per query, a TABLE expression (wrap scalars in `ROW("x", ...)`); one `DEFINE` block; strings escape quotes by doubling.
4. `SUMMARIZECOLUMNS` order is strict: group-by columns, filter tables, name/expression pairs. Filters are table expressions (`TREATAS({"A"}, 'T'[C])` or `FILTER(ALL(...))`), not `'T'[C]="A"`. With no measure and group-by columns from several tables use `VALUES`/`SUMMARIZE`/`SELECTCOLUMNS`.
5. `CALCULATE` boolean filters cannot reference two tables with `&&` (separate args), cannot contain measures (use a VAR). `KEEPFILTERS` to intersect existing filters.
6. NEVER turn BLANK into 0/""/"N/A" in the query (`+0`, `DIVIDE(a,b,0)`, `IF(ISBLANK..)`, `COALESCE` in a grouping query). `SUMMARIZECOLUMNS` drops rows where every measure is BLANK; a non-blank default makes every dimension combination non-empty and the result explodes. Render null in the cell renderer. Single sanctioned exception: aligned cross-highlight subset queries.
7. Time intelligence needs a contiguous, unique, marked Date table with an active relationship; use `'Date'[Date]`, not the fact column; derive "last year" from `YEAR(MAX(fact[date]))`, never hardcode.
8. Wrap currency/fixed-decimal measures in `CONVERT([Measure], DOUBLE)`. A fixed-decimal result can arrive as a scaled integer (2,613,203.85 as 26,132,038,531) and dividing a fixed-decimal column keeps 4 places. If CLI and UI differ by a power of ten, this is the cause. [VOLATILE: connector behaviour]
9. A filter set inside `CALCULATE` on one column of a dimension does not remove the query's filter on another column of it: `REMOVEFILTERS` on the dimension first.
10. Row bounds: there is no default row cap (connector and CLI). Aggregate or `TOPN`, or send `resultSetRowCountLimit` in the invoke envelope. Prefer the limit field when you want a guard: exceeding it FAILS with `overflow`, whereas `TOPN` silently returns a plausible partial answer. A non-positive-integer limit is silently dropped. (legacy CLI trims at 1000 rows with `_cliWarning`.) Treat `overflow` as failure, never as complete data.
11. Dates arrive as tz-less strings (`2024-01-15T10:30:00.000`); midnight timestamps are days; ints beyond `MAX_SAFE_INTEGER` return `category: "overflow"`. Column names are inferred from the FIRST row, so shape the query so every column is present in row 1; `dataType` is often `"unknown"`: supply types via `columnMetadata`.

## Query design
- DAX computes and fetches; TypeScript shapes; the visual renders. Aggregate to the visual's grain in DAX; never fetch lower-grain rows to roll up client-side. One grain per `.dax` file, separate files and hook calls per grain.
- Keep `ORDER BY` for stable diffs only; user-facing sort in TS/Vega-Lite/grid so re-sorting never re-queries.
- Return raw typed values. No `FORMAT()`, no stringified dates, no `SELECTCOLUMNS` just to rename (use `displayName`), no `CONCATENATEX` decoration, no `UNION` of detail and total.
- Grand totals: additive (SUM/COUNT/MIN/MAX) may be rolled up in TS; non-additive (DISTINCTCOUNT, ratios, AVERAGEX, any model measure) need a separate one-row `ROW(...)` query. "An extra round-trip is cheap; a wrong total is a silent data bug." Never sum grouped DISTINCTCOUNT. Provided DataGrid totals must be exactly ONE row and do not update on grid filtering: wire the filter callback into the summary factory (translate column ids to DAX predicates, never interpolate ids).
- Filter strategy: low-cardinality dimension (a few dozen values): widen the grain and filter client-side (instant). High-cardinality (dates, customers) or expensive measures: push into DAX with `TREATAS` and re-query. Estimate rows x columns against browser capacity.
- Missing members on an axis: two simple queries stitched in TS, or an "axis spine" dataset in the Vega-Lite spec. Avoid `GENERATE`/`CROSSJOIN`/`NATURALLEFTOUTERJOIN`. Bounded dimensions only.
- Cross-filtering shows LESS (re-query). Cross-highlighting keeps the dimmed baseline and overlays a bright aligned subset from a SEPARATE query `CALCULATETABLE(<same SUMMARIZECOLUMNS>, TREATAS(...))`; the subset needs a row for every baseline row (`COALESCE(...,0)` when 0 is right, `NATURALLEFTOUTERJOIN` when it must stay BLANK). Never client-filter the baseline.
- Many light queries beat one monolith. Batch independent queries concurrently; fold UI filters into `CALCULATETABLE(expr, filters)` only for a single safe `EVALUATE`.
- Poll by rescheduling after each response (`setTimeout` in `finally`), not `setInterval`; back off while signed out.
- The factory triple per query: `.dax` imported `?raw`, `.json` spec, `.ts` factory returning `{connection, query, columnMetadata, vegaLiteSpec}`; variants as separate `.dax` files chosen by a typed record; clone the spec before mutating.

## Runtime access (connector path)
- `useSemanticModelQuery({connection, query})` over `client.connectors.<name>.executeQuery({query})`. workspaceId/itemId are injected server-side; the app never sends them.
- Two disjoint failure channels: `error` (the connector THREW: wiring, transport, auth; `data` cleared) and `data.status === "error"` (Power BI answered with an error: category `query|overflow|api|network|unknown`). Check both; checking only one renders nothing for half the failures. Empty `connection`/`query` makes the hook idle, so a mis-wired call looks like "never loads".
- Value types differ by host. CLI probes return JSON, so numbers look like numbers; in the Fabric host rows are Arrow-decoded and measure columns can arrive as `bigint` with a Union-typed `dataType` (`Union<Int64|Decimal|...>`). Symptom: KPI cards empty (a `typeof value === 'number'` check fails), Vega throws "Cannot convert a BigInt value to a number", while a data grid still shows values. Neither the CLI nor `validate:visual` can reproduce it. Normalize at ONE seam between the connector result and every visual/KPI (convert `bigint` to `Number`; keep a bigint beyond 2^53 as a string or fix it in the measure) and keep a bigint/Union row fixture in the unit tests. Observed in one app (2026-10-29); the fix was not yet confirmed in the host when this was written. [OBS] [VOLATILE]
- Use a stale-response guard (monotonic request id) so a slow first query cannot overwrite a faster second one.
- Never replace a failed query with mock data. Permanent auth/permission/config/query errors render as actionable sanitized errors, never endless loading; retry only a documented transient condition, bounded.
- No process-global result cache without a per-principal key and TTL (it serves another user's rows after a sign-in change). (legacy SDK has its own 64-entry LRU.)
- Fixed-order transport choice when you cannot use the connector: (1) Fabric host `postMessage` bridge when embedded (official `@microsoft/fabric-app-data` + `-embed-client`/`-proxy`), (2) Rayfin connector, (3) direct Power BI REST `executeQueries` with MSAL for standalone. Read the host method from the message envelope, ignore messages whose source is not `window.parent`, 30 s timeout.

## Adapter shape when one page serves several engines (djouallah VertiPaq host)
`engine: 'dax'`; `init()` signs in then connects; `query(dax)` runs `executeQuery`, checks `r.status !== 'success'` and throws `${category}: ${message}`; adapt `{columns, rows}` to the page's table shape (strip `table[col]`/`[alias]` to the bare name; turn `YYYY-MM-DDT00:00:00` into the day); omit optional capabilities (no `needs` = no SQL/Explore tab). Queries run on capacity per call; no download, no function, no SAS.

## When you also own the model (djouallah's contract between app and model)
- A quantity is one measure, and the measure picks the table (a daily aggregate versus the 5-minute fact), so the same measure answers a day and a year. Direct Lake has no aggregation tables; the switch is DAX. Keep it on every quantity or the browser cannot call it over a long range.
- Put every rule in a model/measure, not in the page. A lint ("the page does no arithmetic") keeps it so.
- Direct Lake needs every named table and column to exist before deploy; a refresh right after a table was recreated answers `DirectLake_TableNotFound` for several minutes: wait and retry. A model deployed ahead of its tables stays broken until the next good deploy.
- Check a deployed model by XMLA (ADOMD.NET) when using a service principal: REST `executeQueries` answers `401 PowerBINotAuthorizedException` on a Direct Lake model with single sign-on. Details in deploy-and-ci.md.
- Authoring the model itself (TMDL, measures, Direct Lake binding) belongs to `semantic-model-authoring` (ecosystem.md).
