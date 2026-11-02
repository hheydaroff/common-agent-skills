# Troubleshooting: symptom -> cause -> fix

Match on the exact string. `[V]` = volatile, re-check (platform-and-prereqs.md ledger). Always capture the
`RootActivityId` from a 403/500. First checks for any failure: CLI version (`npx rayfin --version`), who owns the
item (Settings > About), `~/.rayfin/logs/`, and whether a service-side rollout changed behaviour with no repo change.

**Which 500?** Function route (`/functions/<name>/invoke`; client `NetworkError: An internal error occurred.`) = SP-owned item or a handler that threw (return `{error}` to tell them apart). `/graphql` "Internal server error" = schema (`@text` without `max`). `/connectors` 401 = SP-owned item (Category A) or missing delegated permission.

## Deploy, ownership, tenant
| Symptom | Cause | Fix | Ref |
|---|---|---|---|
| `403 Forbidden ... Only AppBackend artifact owner can perform this operation` (also at "runtime settings sync", aborting `up` before static hosting) [V] | deploying an item another identity created; Edit permission is not enough | deploy as the creator, or a separate `--item-name`; portal shows you as owner yet still fails after "Take over": ask who CREATED it | deploy-and-ci |
| every function call `500` "An internal error occurred." / `PowerBIApiErrorResponse: "An internal execution error occured"`, deploy was green [V #89] | item owned by a service principal | human-owned item, laptop deploy; A/B repro in deploy-and-ci | deploy-and-ci |
| connector read `401 CONNECTOR_AUTH_FAILED` "Could not acquire the app owner's credentials" while `/graphql` is 200 [V #93] | Category A connector on SP-owned item | human-owned item. `connector inspect --entity` takes the TABLE name | connectors |
| `403 FeatureNotAvailable` creating an item as a SP [V #92]; `403 The feature is not available` on deploy [V #8] | SP creation gap; or tenant switch for Fabric apps is off | create as a human; ask the admin to enable "Fabric Apps (preview)" | platform-and-prereqs |
| "App (preview)" missing from New item | tenant setting off, not propagated, or user not in the scoped group | admin enables; wait minutes | platform-and-prereqs |
| `rayfin up --json` exit 0, `status: success`, a step failed [V] | overall status does not aggregate steps | parse `steps.*.status` | deploy-and-ci |
| `401/403` on `up` after it worked | expired session | `npx rayfin login`; then check ownership | deploy-and-ci |
| `No remote endpoint configured` / `Run 'npx rayfin up' first` | `secret *`, `up functions deploy`, `staticapp deploy` need a remote item | `npx rayfin up` once | functions-and-secrets |
| `up db apply` refuses | destructive change detected | review; `--force` only after approval | operational-apps |
| `up db apply` fails right after first deploy | services not healthy yet | wait, retry | operational-apps |
| `Dialect is required when Data module is enabled.` | data enabled without `dialect` | `dialect: mssql` | operational-apps |
| Unexpected capacity change | `--yes` approves capacity assignment and same-name reuse | omit `--yes`; use `--capacity-id` | deploy-and-ci |
| New item collides on name | default item name = rayfin.yml `id` | `--item-name` | deploy-and-ci |
| Deploy rejected for old CLI | tenant enforces static-hosting access control [V] | `npm i -g @microsoft/rayfin-cli@latest` | rayfin-project |
| Static deploy too large | ZIP > 100 MB | drop source maps/assets | deploy-and-ci |
| Login fails with keychain error (Linux, devcontainer, Codespaces) | no OS credential store | `rayfin login --encryption-fallback-enabled` (plaintext cache, dev only) | rayfin-project |
| Env var "not defined" in rayfin.yml | `${VAR}` unset with no default | `${VAR:-x}` or set in `rayfin/.env` (shell wins) | rayfin-project |
| Sign-in broken after deleting and recreating the app | new `*.webapp.fabricapps.net` origin, stale `.deployments.json` | delete the record, register the new origin | rayfin-project |
| First-deploy login handoff fails | hosting URL not in `allowedRedirectUris` (sources disagree on auto-add) | add the bare origin, redeploy | rayfin-project |
| Stale schema/config after edits | `rayfin/.temp/` cache | delete `rayfin/.temp/`, `rayfin up` | rayfin-project |
| `dev` "recursion" error | `"dev": "rayfin dev"` with no child script | add `"dev:frontend": "vite"` | rayfin-project |
| Node install rejected | odd Node major | LTS 20/22/24 | platform-and-prereqs |
| CI deploy refuses a function project / `npm ci` fails on the runner | `host.json` gitignored; lock names a private registry | commit `host.json`; regenerate lock against `registry.npmjs.org` | functions-and-secrets |

## Auth and hosting
| Symptom | Cause | Fix | Ref |
|---|---|---|---|
| popup blocked on Fabric sign-in | interactive call not inside a click handler | call `ensureSignedInWithFabric` synchronously from the click; `initEmbeddedAuth` on load | auth-and-security |
| `initEmbeddedAuth` returns `null` | not embedded, or `?fabricEmbedded=true` lost to client navigation before the module loaded | static-import the provider package in the entry module | auth-and-security |
| 5-minute timeout, handoff never arrives | `returnOrigin` differs from the real origin, or origin not in `allowedRedirectUris` | bare origin in the list | auth-and-security |
| "Page not accessible directly" at sign-in popup | page is cross-origin isolated (COOP/COEP, coi-serviceworker) | remove isolation; stay single-threaded | static-engine-patterns |
| embedded app shows another user's session | `initEmbeddedAuth` skipped or deferred | await it before restoring a stored user | auth-and-security |
| external embed falls back to popup | embed host registered after the iframe mounted, or origin not in `allowedOrigins` | `createEmbedHost` first; exact origin | auth-and-security |
| auth never completes, two clients | CDN client and auth-provider on different versions | pin both to one version | static-engine-patterns |
| `rayfin.config.json not found - deploy with rayfin up` | page served without the config `rayfin up` writes beside the site | run via `rayfin up`/dev flow | static-engine-patterns |
| email/password works locally, fails deployed | deployed Fabric is SSO only | `auth.fabric.enabled: true` | auth-and-security |
| `signInWithEntraToken` `EXCHANGE_NOT_ENABLED` / `AUTH_FAILED` / `INSUFFICIENT_PERMISSIONS` | `externalEntraExchange` off; wrong audience/tenant/scope; no Execute on item | fix per error; base URL absolute HTTPS incl. path | auth-and-security |
| `isSupported()` -> `undefined`, writes `NO_HOST_WINDOW` | not embedded, tenant lacks deep linking, or `targetOrigin` pinned | degrade quietly; remove `targetOrigin` | auth-and-security |
| shared link opens right page then jumps to default / navigation dead | sign-in redirect lost route, or router sync wrote pre-restore location; or `useNavigate()` identity in effect deps | carry `from`; hold sync until restore lands; navigate in a ref with empty deps | auth-and-security |
| `STATE_TOO_LARGE` / `INVALID_STATE` | > 4 KiB or non-JSON state | store server side, put an id in state | auth-and-security |
| promoted app hits new API but old auth workspace | baked `VITE_FABRIC_*` | `client.runtimeConfig` via `resolveRayfinConfig` | rayfin-project |
| frontend env empty/wrong after deploy | `.env.local` is generated | `rayfin env --framework vite`; hosting URL from `.deployments.json` | rayfin-project |
| OneLake `401` to the SAS | workspace setting "Authenticate with OneLake user-delegated SAS tokens" off, or owner cannot read the lakehouse | enable; grant owner read | static-engine-patterns |
| catalog-vended credentials `401` on reads | they are `sp=racwdl` [V] | sign your own `sp=r` SAS | static-engine-patterns |

## Entities and GraphQL
| Symptom | Cause | Fix | Ref |
|---|---|---|---|
| "Internal server error" from GraphQL after a green `up` | `@text()` without `max` -> NVARCHAR(MAX) | `@text({max:N})` everywhere, `up db apply --force` | operational-apps |
| list silently truncated at 100 | `.execute()` is one page | `.first(n).executePaginated()` loop | operational-apps |
| `count()`/`totalCount`/`.before()` fail | not supported | select ids, `results.length`, page forward | operational-apps |
| `unsupported UUID` | another service on the default port with a different dialect | stop stale services, rerun | operational-apps |
| `Reserved GraphQL type names detected` | entity named like a scalar/root type | rename class, keep `Source({table})` | connectors |
| `Expression expected` on `@entity()` | bundler target < ES2022 or swc plugin | esbuild target `es2022`, `@vitejs/plugin-react` | rayfin-project |
| decorator errors "fixed" via experimentalDecorators | wrong fix | never enable it | rayfin-project |
| `onAuthStateChange is not a function` | name does not exist | `auth.onSessionChange(cb)` | auth-and-security |
| per-user policy "works" in testing | one user owns every row; no `user_id` column | test with a second account | auth-and-security |
| app breaks after a portal edit of the SQL DB | schema is code-owned | change `rayfin/data/*.ts`, `up` | operational-apps |
| duplicate rows after a timeout | retried a mutation that had completed | client UUID + verify before retry | operational-apps |
| Data API saturated/hangs on bulk writes | 8 concurrent mutations, 30 s timeout | <= 2 concurrent, 120 s | operational-apps |
| form clears though save failed | wrappers resolve after handled errors | clear from explicit success state | operational-apps |

## Functions, secrets, connectors
| Symptom | Cause | Fix | Ref |
|---|---|---|---|
| bare `500`, no detail | function threw | return `{error: "<step>: ..."}` | functions-and-secrets |
| function misbehaves on first deploy | secret set after deploy | `secret set` then `up functions deploy` | functions-and-secrets |
| `ctx.Secrets.TYPO` compiles; new secret does not type-check | ctx not annotated; `secrets.generated.ts` stale | annotate `RayfinContext<...>`; rerun `secret set` | functions-and-secrets |
| `ctx.Tokens.Sql` compiles, throws at runtime | host did not deliver the audience | owner's permissions; `up` ran | functions-and-secrets |
| `types.ts` edits vanish; `client.functions.X` unknown | generated, closed type; function not registered | `udf.func(name, fn, [])`; rerun `dev functions apply` | functions-and-secrets |
| long call dies ~250 s [V] | host ceiling | split or stream | functions-and-secrets |
| local function calls `502` | Vite adapter active, local host down | `rayfin dev` | functions-and-secrets |
| mssql "socket hang up" against Fabric | tedious <= 19.1.2 | `mssql@^12.6.0` | functions-and-secrets |
| `Cannot find module '@microsoft/rayfin-connector-*'` | `connector add` installs nothing | run the printed pinned install | connectors |
| `connector add` "literal IDs required" | `${VAR}` passed | literals | connectors |
| `rayfin up` "does not support operation" | operations exceed the type allowlist or are bare strings | narrow; `- name: read` objects | connectors |
| `SELECTION_REQUIRED` | missing `.select()` or entity not registered | see connectors | connectors |
| `FEATURE_NOT_ENABLED` / 404 on `/connector-invoke/<name>` | workspace ConnectorFunction switch off | escalate for enablement | connectors |
| semantic model `Unauthorized` only in the deployed app | CLI probe used your identity | test with a non-owner user | data-apps-semantic-model |
| `connector invoke --file q.dax` fails before the connector | `--file` is JSON-parsed | `{"query": ...}` envelope | data-apps-semantic-model |
| `kusto` -> `Connector type "kusto" is not available` / `Unsupported connector type: kusto` | held in 1.36.2 | say so and stop | connectors |
| `secret set --describe "..."` rejected | space form | `--describe="..."` | functions-and-secrets |
| `ConnectorFunction invocation is not enabled for this workspace` | experimental connector not enabled; needs Rayfin >= 1.34 | fall back to host bridge/MSAL, or enable | data-apps-semantic-model |

## Semantic-model data apps
| Symptom | Cause | Fix | Ref |
|---|---|---|---|
| empty visuals / query errors for some users | Execute Queries tenant setting off, or no Build+Read on the model, or wrong DAX names | checklist; read `error.category/message` | data-apps-semantic-model |
| total off by 10^n | fixed-decimal returned as scaled integer | `CONVERT([M], DOUBLE)` | data-apps-semantic-model |
| KPI cards empty / Vega "Cannot convert a BigInt value to a number" in the Fabric host only; CLI, `validate:visual` and the data grid look fine | Arrow-decoded measure columns arrive as `bigint` (Union-typed `dataType`) | normalize rows to `Number` at one seam before visuals; add a bigint row to unit tests; confirm with the diagnostics panel (frontend-design-and-validation) [OBS, fix unconfirmed] | data-apps-semantic-model |
| millions of rows after "tidying" | BLANK replaced by 0 | leave BLANK | data-apps-semantic-model |
| page hangs on a huge result | no default row cap | `TOPN`/aggregate or `resultSetRowCountLimit` | data-apps-semantic-model |
| component renders nothing on failure | only `data.status` checked | check `error` AND `data.status` | data-apps-semantic-model |
| rows arrive unreadable | connector not in `connectorRuntimes` | add `fabricSemanticModel({})` | data-apps-semantic-model |
| hook never loads, no error | empty `connection` or `query` -> idle | check wiring | data-apps-semantic-model |
| missing column; `dataType: "unknown"` | names inferred from row 1 | every column in row 1; supply types | data-apps-semantic-model |
| `DatasetExecuteQueriesError` HTTP 400, app shows zeros (DirectQuery over KQL) | no bound credentials | take ownership, seed the gateway datasource, switch to end-user SSO | worked-example |
| `DirectLake_TableNotFound` right after recreating an Iceberg table | Direct Lake sees it minutes later | wait and retry | data-apps-semantic-model |
| REST `executeQueries` `401 PowerBINotAuthorizedException` for a SP | single-sign-on Direct Lake model | query by XMLA | deploy-and-ci |
| year axis shows ".905" | `temporal` on integer years | `quantitative` | frontend-design-and-validation |
| stack-trace card where a chart should be | top-level selection `params` in a multi-entry layer | declare in the owning layer | frontend-design-and-validation |
| squished chart, empty body | no definite height chain | full `h-full`/`flex-1 min-h-0` chain | frontend-design-and-validation |
| text size or colour class dropped | tailwind-merge `text-*` grouping | `text-[length:var(--text-300)]` | frontend-design-and-validation |
| `TS6305` on typecheck | unbuilt references; `tsc --noEmit` | `tsc -b` / `npm run typecheck` | operational-apps |
| portal iframe `chrome-error://chromewebdata/` | Local Network Access blocks public-to-localhost | launch flags + `Access-Control-Allow-Private-Network` | frontend-design-and-validation |

## Static engine apps
| Symptom | Cause | Fix | Ref |
|---|---|---|---|
| `LinkError ... mismatch in shared state of memory` | threaded duckdb-wasm + unshared-memory extension | `eh` single-thread bundle | static-engine-patterns |
| "Failed to open file" with no HTTP request | `forceFullHTTPReads` left on | set the three filesystem flags | static-engine-patterns |
| `INSTALL` of an extension fails in a worker | no home directory | `SET home_directory='/tmp'` first | static-engine-patterns |
| new HTML with old JS (`s.replace is not a function`) | cached module across deploy | stamp + `?v=` | static-engine-patterns |
| load in six sequential rounds | lazy module graph, ~0.7 s per request | modulepreload | static-engine-patterns |
| first query waits 35 s | downloads first-come across tables | `prioritize()`, smallest first | static-engine-patterns |
| queries wait while one engine idles | engine bound at send time | one shared queue | static-engine-patterns |
| browser re-downloads 70-100 MB files | HTTP cache will not keep them | OPFS whole-file store | static-engine-patterns |
| "no local store in this browser" | no OPFS writer answered in 30 s; browser lacks `readwrite-unsafe` | Chrome/Edge 121+; document support | static-engine-patterns |
| view fails "not readable as Parquet with position deletes" | equality deletes / deletion vector / empty | compact upstream; no fallback by design | static-engine-patterns |
| stale data from saved results | key lacked the data version | key = SQL + table metadata locations | static-engine-patterns |
| wrong "today" | session zone | `SET TimeZone`, needs icu | static-engine-patterns |
| BigInt/unscaled ints in results | duckdb-wasm result types | `castBigIntToDouble`, `castDecimalToDouble` | static-engine-patterns |
| npm `latest` of duckdb-wasm breaks OPFS | tag points at a bad dev build | pin an exact version | static-engine-patterns |
| deployed file never appears on the Pages repo | `git add --all` skips new files matching `.gitignore` | `git add -f` listed paths | deploy-and-ci |
| CI "succeeds" but the data is empty in a Fabric copy | public source answers 403 to Fabric IPs | expect near-empty test data; create facts empty so the model still deploys | worked-example |

## Things the sources do not cover (do not invent)
OneDrive-synced folders as a cause (a reporter had one; the same 403 reproduced outside OneDrive); Windows-only defects; a capacity-migration procedure (an existing recorded deployment keeps its capacity; `--capacity-id` applies to first deploys); per-row security for storage apps; viewer licences below F64; guest users; CU cost per call.
