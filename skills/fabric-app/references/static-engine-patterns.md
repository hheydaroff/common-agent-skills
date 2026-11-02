# Static analytics apps: the browser is the engine

Pattern from djouallah/analytics-as-code (`front_end/fabric_app/iceberg/`): a Fabric app with no database and one
function. The page reads OneLake Iceberg/Parquet files directly with DuckDB-WASM; the function only tells the page
where each table is and signs a short read-only SAS. Use it when you need ad hoc SQL, repeated fast queries after a
one-time download, or no per-query capacity spend. Do NOT use it when you need row/column security (the SAS covers
a whole folder), a small first-visit cost (first visit downloaded 1.3 GB for one table), or browsers other than
Chrome/Edge 121+. Measured on one dataset and browser, 2026-10; numbers are illustrative. [VOLATILE]

## Choosing the engine
| | DuckDB-WASM + SAS | Semantic model via connector |
|---|---|---|
| Runs as | browser, over files | signed-in user, on capacity per query |
| Security | whole `Tables/` folder | model RLS flows through |
| Cost | download once, then free; ~4 GB tab memory ceiling | capacity per query |
| Needs | 1 function, workspace SAS setting, owner reads lakehouse | tenant switch, connector added at deploy |
| Features | ad hoc SQL ("Explore") | DAX only |
Keep both behind one page if the product needs both (below).

## One page, thin host adapters
The page is written once. Each host gives it one `storage/data.js`:
- `createDataSource({onStatus, onProgress, timeZone})` -> `init()` (sign in, locate, size; returns `{db}`), `query(sql, dax?, options)` returning an Arrow-shaped table (`numRows`, `schema.fields[].name`, `getChild(name)` with `length/nullCount/get(i)/toArray()`), `attachAgg()`, `ensureHistory()`, `has(view, column)`, `views()`, `needs()`.
- Absence of a member is the capability flag: a host with no SQL omits `needs`, and the page hides the Explore tab. Do not add a stub.
- `has()` answers "no data" for a table or column a deployed file lacks, so a page can ship before its data.
- Priority statement for multi-host products: say which host must never break (the public one), check shared changes there first, and let it win where hosts diverge.

## The function (`openCatalog`)
1. Input: closed grammar (`schema.table`), de-duplicated; the lakehouse location comes from the `CATALOG_URL` secret (`https://onelake.table.fabric.microsoft.com/iceberg/<ws id>/<lakehouse id>`), never from the caller.
2. Server side with `ctx.Tokens.Storage`: `GET {endpoint}/v1/config?warehouse=<ws>/<lh>` for the catalog prefix (cache per warm instance), then `GET /v1/{prefix}/namespaces/{ns}/tables/{name}` per table (parallel) -> `metadata-location`; 404 = `missing` (page shows no data, does not fail). In parallel, `POST https://onelake.blob.fabric.microsoft.com/?restype=service&comp=userdelegationkey` (`x-ms-version: 2022-11-02`).
3. Window for both: `start = now - 5 min`, `expiry = now + 55 min` (OneLake caps at 1 h and does NOT cap the key at the storage token's expiry, so a nearly expired token must not shorten it).
4. HMAC-SHA256 (base64-decoded key value) over the string to sign for a DIRECTORY SAS on `/<ws>/<lh>/Tables`:
```
[sp=r, st, se, `/blob/onelake/${ws}/${lh}/Tables`, skoid, sktid, skt, ske, sks, skv,
 '', '', '', '',                      // saoid suoid scid sip: unsupported by OneLake
 'https', '2022-11-02', 'd', '', '', '', '', '', '', ''].join('\n')
query: sp=r st se skoid sktid skt ske sks skv spr=https sv=2022-11-02 sr=d sdd=<folders below the workspace; <lh>/Tables -> 2> sig
```
5. Return `{metadata, missing, sas, expiresOn, catalogMs}` or `{error: "<step>: ..."}`. Never return a token.
6. Workspace setting "Authenticate with OneLake user-delegated SAS tokens" must be on (off: 401); the owner must read the lakehouse. Do not use catalog-vended credentials (read-write-delete).
7. The client keeps the answer in localStorage until `expiresOn - 2 min`, so a reload calls no function; a tab open longer renews before expiry and retries after 60 s on failure. Views read the local store, so a new SAS changes no view.

## Rules for the browser side
1. **The browser never holds a token or anything that can write.** The SAS is the only credential; strip query strings from everything logged; keep the SAS out of DuckDB entirely: the page downloads with the SAS and hands whole files to a local store; DuckDB sees only `store.local` names registered with `registerFileURL`. No httpfs, no SECRET, no SAS in any view, EXPLAIN or log.
2. **Control egress inside the worker, not with a CSP.** The repo has no CSP; a classic script (`blockcache.js`) prepended to every DuckDB worker patches `XMLHttpRequest`: `https://store.local/...` answers from OPFS (404 if not held), DuckDB extension URLs pass, everything else gets a synthetic 403. Reason: duckdb-wasm's own HTTP file system would fetch any `https://` URL even without httpfs, so SQL typed in Explore could exfiltrate. Fabric static hosting's response headers and CSP-meta support are unknown.
3. **Single-threaded, no cross-origin isolation.** Isolation breaks the Fabric sign-in popup ("Page not accessible directly"); every published `wasm_threads` extension imports unshared memory (`LinkError ... mismatch in shared state of memory`); the threaded build cannot load ICU or pass OPFS handles to pthreads and gains ~1.4x on 4 threads. Use the `eh` bundle (`selectBundle(getJsDelivrBundles())`).
4. **Scale with a pool of engines** (default 2; 3 measured no faster: a third WASM compile slows start, queries ran ~15% slower sharing CPU; `?engines=N` to compare) fed by ONE queue: a free engine takes the next job, preferring the engine with more of the query's tables open; `early` before normal before `later`; a job whose `stale()` is true when its turn comes is dropped unrun. Never bind a query to an engine when it is sent (queries waited 14-16 s behind an 18 s scan while the other engine idled). Only setup and background-open jobs are pinned.
5. **Plan the table in the page, not the engine.** `planTable` reads metadata.json -> manifest list -> manifests with a small Avro reader (codecs null, deflate), keeps live data and position-delete files with sizes; a view is `read_parquet([literal local names])`. Position deletes: read delete files once per session into `__deletes_<table>` and `ANTI JOIN` on file and row. Equality deletes, deletion vectors or no data file: fail loudly, no fallback, on purpose. Reason: `iceberg_scan` re-plans per query at ~0.6-0.7 s per request and the Azure/iceberg extensions were unavailable or unsigned in WASM. Manifests are immutable: cache by path in Cache Storage.
6. **Open tables lazily.** A table opens when a query first names `v_<table>`; the rest open after first paint, small first, at the back of each queue. Tables <= 32 MB are copied into each engine's memory; larger are read in place. (Cold load: 70-79 s with every view up front, 48 s lazy only, 14-17 s with snapshot records + whole-file store + extension warm-up.)
7. **Key every persistent cache by identity of the data, never by time**: snapshot record -> metadata.json location (each commit writes a new one); manifest -> its path; stored file -> OneLake path without SAS (immutable); saved result -> SQL + the metadata location of every table it names; function answer -> expiry; extensions -> DuckDB version in the URL. New data = new key; nothing to invalidate. Do not cache queries reading the clock (`current_date|now()|random()`), non-reads, or results > 8 MB; LRU past 256 MB; wrap localStorage/IndexedDB/Cache Storage in try/catch (private mode must not break the page).
8. **Do not rely on the browser HTTP cache for big files** (it does not keep 70-100 MB responses): download whole files, write them to OPFS in 256 KB blocks (cap 8 GB, then start over). Download six at a time (OneLake is HTTP/1.1); each request costs ~0.6 s whatever its size, so serve downloads table by table with `prioritize(...)` for the table a query is about to open (first query went from 35 s to 7 s).
9. **OPFS**: every worker opens both store files `createSyncAccessHandle({mode:'readwrite-unsafe'})` (Chrome/Edge 121+; `read-only` fails while a `readwrite` handle is open). Exactly one writer, the holder of Web Lock `blockcache-writer` (`ifAvailable`, held for the worker's lifetime); readers re-read the index on a miss; when the writer dies the next worker handed a file takes the lock. Page<->store protocol over `BroadcastChannel('blockcache')`. Serve HEAD (206 with Content-Length if a Range header is present) and range GET so duckdb-wasm's HTTP fs works. First index line carries a version; another version resets. If no writer answers in 30 s, stop with a clear error ("no local store in this browser").
10. duckdb-wasm options this design needs: `db.open({ filesystem: { reliableHeadRequests: true, allowFullHTTPReads: false, forceFullHTTPReads: false }, query: { castBigIntToDouble: true, castDecimalToDouble: true } })`. All three filesystem flags are required; with `forceFullHTTPReads` on, a file opens with no request and fails ("Failed to open file"). Per engine: `SET home_directory='/tmp'` before `INSTALL` (no home in WASM); `INSTALL/LOAD parquet`, `icu`; `SET parquet_metadata_cache=true; SET TimeZone='<tz>'` (needs icu; otherwise `CURRENT_DATE` follows the wrong zone). Pin an exact duckdb-wasm dev version, not the `latest` tag. Extension URLs sit under the version, so the browser keeps them; warm-fetch them all at once on first load. Register the plain filename for `ATTACH`, not `opfs://` (it also opens `<file>.wal`). Writers and readers must agree on the DuckDB on-disk format version.
11. **Warm up independent work while the heavy bundle loads**: start model fetch -> catalog open -> sizing without awaiting while the engines instantiate.

## Build, stamp, preload
No bundler; `staticHosting.buildCommand: node ../common/build.mjs` (cwd = project; output `dist/`). Order: remove `dist` -> stage the shared page -> copy shared `common/site` -> copy the project's `site` over it -> stamp -> modulepreload -> copy files that must not be stamped last.
- `BUILD = <sha>[-dirty].<yyyymmdd-hhmm UTC>` (URL-safe; dirty is computed over the paths that go into dist only). Replace `__BUILD__` and add `?v=<BUILD>` to every static relative import. Reason: the host sends `max-age=600`; without it a browser runs the new page with cached old modules for up to 10 minutes (`s.replace is not a function`). The regex rewrites static `from "./x.js"` only: propagate the stamp yourself to dynamic imports, workers, `importScripts` and `fetch` (`new URL('./x.js' + new URL(import.meta.url).search, import.meta.url)`).
- A harness importing a module from a stamped build must use the same `?v=` or it gets a second instance.
- `<link rel="modulepreload">` for every statically imported module (followed transitively) plus `preload as=fetch crossorigin` for any JSON a top-level `await` reads. The Fabric static host answers each request in ~0.7 s whatever its size, so ~37 unpreloaded modules arrived in six rounds (2.0 s to 7.65 s).
- Lazy-load heavy SDKs with a memoized dynamic `import()` (clear the memo on failure so the next call retries); gate with a size-budget script.

## Logs tab as the debugging record (build it on day one)
A memory-only event log (cap 5,000; nothing stored or uploaded; a Copy button is the only way out) holding: build stamp, function call, catalog answer, each PLAN/OPEN/download, every query with SQL + `wait` (queue) + `ms` (run) + engine, each worker HTTP request (shim posting over a BroadcastChannel), page-load navigation timings and resources >= 200 ms, one summary line for main-thread long tasks >= 100 ms in the first 20 s, store size and files. The owner pastes one artifact and an agent can see cold vs cached, stale bundle, slow table, stuck engine. Time queries in the host when your queue is not single-worker (a perf wait model that assumes one worker misreads a pool).

## Minimal rayfin.yml of a no-database static app with one function
```yaml
services:
  auth:    { enabled: true, fabric: { enabled: true }, allowedRedirectUris: [http://localhost:5173, http://127.0.0.1:5173] }
  data:    { enabled: false }
  staticHosting: { enabled: true, folder: dist, buildCommand: node ../common/build.mjs, indexDocument: index.html, assetAccess: public }
  storage: { enabled: false }
  functions: { enabled: true, buildCommand: npm run build, auth: { type: application } }
secrets:
  - name: CATALOG_URL
    description: OneLake Iceberg catalog, https://onelake.table.fabric.microsoft.com/iceberg/<workspace id>/<lakehouse id>
```
`data/schema.ts` stays as `export type BlankAppSchema = {}; export const schema = [];` so the function context type resolves.

## Honest caveats
The SAS lives in localStorage (`rayfin_catalog`) for ~55 minutes and downloaded data persists in OPFS/IndexedDB; no clear-on-sign-out code was found. Say "no per-row/column security, no revocation of downloaded data" to stakeholders. The main page is unrestricted and loads libraries from jsDelivr without integrity hashes (supply-chain surface). Unverified: whether the function is callable by any signed-in user or only users the app is shared with.
