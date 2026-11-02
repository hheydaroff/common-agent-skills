# Functions and secrets

Server-side TypeScript (`@microsoft/fabric-user-data-functions`) that runs in the Fabric runtime and is called from
the browser through a generated typed client. Read the guide's `functions/*` docs before writing (routing table at
the end); this file holds the decisions and traps.

## Function, connector or entity?
- Logic needs a secret, an external token, privileged access, server-side validation, or must not be tamperable: **function**. Otherwise do it in the browser.
- App OWNS the data model: **entity** (operational-apps.md). Data ALREADY lives in a Fabric SQL item or semantic model: **connector** (connectors.md). Source is not a connector type (OneLake files, Azure Blob, Fabric REST, Foundry, Azure DevOps) or you need per-request logic: **function with `ctx.Tokens.*`**. `fabric-sqlanalytics` cannot open `Files/`.
- A function cannot reach a semantic model (`AudienceType` has no member for it): use the `fabric-semanticmodel` connector.
- Browsers cannot call Fabric/Power BI REST (no CORS), GitHub, or run long-running-operation polling: use a function. Prefer typed Rayfin functions over a hand-published Python UDF; Python stays for APIs Rayfin has no audience for (Power BI admin scanner, some Kusto cases). Older templates disable functions with "UDF backend does not accept the TYPESCRIPT runtime": newer than that is 1.36. [VOLATILE]
- No unattended trigger or timer, no distributed lock in Rayfin Functions: sync is browser-tab-driven; never store or replay delegated tokens. [VOLATILE]

## Authoring rules
- Import `RayfinContext` and `UserDataFunctions`/`AudienceType` from `@microsoft/fabric-user-data-functions`, not `@microsoft/rayfin-functions`.
- Register every function: `udf.func(name, handler, [])`. Bare exported functions do not exist for the client. Always annotate the context parameter `RayfinContext<AppSchema, AudienceType.X | AudienceType.Y>`: the annotation registers the audiences (third argument stays `[]`) and is how typegen identifies the injected ctx; an unannotated ctx makes `ctx.Secrets.TYPO` compile (`any`).
- Audiences (exactly five): `Sql` (Lakehouse SQL endpoint, Warehouse, Fabric SQL DB, Mirrored DB, Azure SQL), `Storage` (OneLake files and Azure Blob/Table/Queue), `Fabric` (`https://api.fabric.microsoft.com/v1`), `AzureAI` (Foundry/OpenAI), `ADO`. Write `AudienceType.X` literally and keep a `tsconfig.json` in the functions project; without it the CLI reads the annotation syntactically, cannot resolve aliases, and warns (treat the warning as real). Declaring an audience guarantees nothing at runtime: if `ctx.Tokens.Sql` throws, check the owner's permissions and that `up` ran.
- `ctx.Tokens.*` = the app identity (the item OWNER) for external resources; `ctx.getDataClient()` = the CALLER for Rayfin DB access. `ctx.getToken()`/`ctx.getSecret()` are deprecated (`@typescript-eslint/no-deprecated`).
- `import type` for entity imports with a `.js` suffix; a runtime import pulls the decorator runtime into the bundle.
- Resource SDK packages go in `rayfin/functions/package.json`, not the project root.
- Resolve endpoints yourself, never ask the user to paste connection strings, never read them from `process.env`: `fab` CLI or Fabric MCP if present, else Fabric REST (`GET /workspaces/{ws}/items?type=Lakehouse|Warehouse|SQLDatabase`, then `/lakehouses/{id}` etc.; token via `az account get-access-token --resource https://api.fabric.microsoft.com`). Ask only on multiple matches, 403, or unknown workspace (`functions/connections/get-fabric-info.md`).
- Fabric SQL from a function: `mssql@^12.6.0` (older tedious <= 19.1.2 gives "socket hang up" against Fabric), `encrypt: true`, `authentication.type: 'azure-active-directory-access-token'` with `ctx.Tokens.Sql`; pass the item GUID as `database` for Lakehouse/Warehouse/Mirrored, `databaseName` for Fabric SQL DB.
- Validate inputs at the boundary against a closed grammar; take locations from secrets, not from the caller (auth-and-security.md).
- **Return failures as a value, do not throw.** A thrown error reaches the browser as a bare `500 "An internal error occurred."` naming nothing. Track a `step` variable and return `{ error: "<step>: <message>" }` with a union return type; the client turns `r.error` into a thrown Error. Never put a token or key in the message. Docs say a throw surfaces as `FunctionsError`; the field experience is the bare 500.
- Expected failures of an external call: return a bounded `{ok:true,value} | {ok:false,code,message}` union, never raw provider bodies or stack traces.
- A module-level cache (e.g. a catalog prefix Map) survives only while the instance is warm; correctness must not depend on it.
- Optional parameters need a defaulted nullable form (`correlationId: Uuid | null = null`) so typegen and runtime binding agree. Python UDF parameter names must be camelCase.
- Fabric data agents: call the PUBLISHED MCP endpoint `https://api.fabric.microsoft.com/v1/mcp/workspaces/{ws}/dataagents/{id}/agent` with `ctx.Tokens.Fabric` (sequence initialize, notifications/initialized, tools/list, tools/call; accept JSON, SSE and plain-text "Accepted"; tell the user it can take up to 10 minutes; isolate a dedicated client because the browser client timeout is client-wide).

## Generated files (never hand-edit)
`rayfin/functions/src/types.ts` (the closed `AppFunctionsSchema`; must not import Node packages because the frontend compiler resolves it), `secrets.generated.ts`, `runtimemetadata.json`. They regenerate through `npx rayfin dev functions apply` (typegen watcher) or `secret set`. A fresh clone has stale or missing types: add a root `postinstall: npm ci --prefix rayfin/functions`. Keep `npm run dev` running while signatures change. Never cast the functions client (`as any`). Commit `host.json` (the scaffold's `.gitignore` omits it and the deploy refuses without it) and a lockfile that resolves from `registry.npmjs.org`.

## Secrets
- Declare names in `rayfin.yml` `secrets:` (with a description of the value's shape). `npx rayfin secret set NAME` stores the value; `ctx.Secrets.NAME` reads it. Never hard-code a name string; not `process.env` in production code.
- Order for a new item (secrets need a remote item): `npx rayfin up` -> `secret set` -> `npx rayfin up functions deploy`. The first deploy shipped before the secret existed; redeploy the function to see it. Guard in CI with `npx rayfin secret list | grep -q NAME` so re-runs do not redeploy; `echo -n "$VAL" | npx rayfin secret set NAME --stdin` (the `-n` avoids a trailing newline).
- Flags: `--describe="text"` (the space form is rejected); `--env-file` and name, or `--env-file` and `--stdin`, are mutually exclusive; `secret list` shows names and timestamps only. Local secrets go in `local.settings.json` `Values` (gitignored; `dev` merges its own keys).
- After changing `services.functions.auth.type`, do a FULL `npx rayfin up`; `up functions deploy`, `dev functions apply` and `up staticapp deploy` neither validate nor apply the auth mode. Enabled functions require `auth.type: application` (the scaffold sets it; older apps must set it by hand).

## Calling from the browser
`client.functions.<name>.invoke(input, {timeoutMs})` (no input: `invoke(undefined, {timeoutMs})`). The host aborts at ~250 s whatever `timeoutMs` says: split work or stream results. [VOLATILE]
Local: leave `functionsBaseUrl` undefined so the SDK uses `/functions/<name>/invoke` and the Vite adapter (`rayfinLocalDev()` from `@microsoft/rayfin-local-dev/vite`) forwards to the local host. If the host is down you get a 502 (no fallback to deployed code). Never expose a local Functions URL in production. Bind Vite to loopback; the `/.rayfin` proxy is reachable wherever Vite is. The doc and the older skill disagree on the local path (`/.rayfin/api/<name>` vs `/functions/<name>/invoke`): do not hard-code either.
Local host: Node >= 20 and Azure Functions Core Tools; port 7071 (shifts), inspector 9229; add `"build:watch": "tsc --build --watch"` or the host starts without the compiler watcher.

## Commands
```
npx rayfin functions init [dir] [--force]     scaffold, deps, build, typegen
npx rayfin dev                                frontend + functions together (preferred)
npx rayfin dev functions apply [--port 7071] [--no-debug]   function host alone
npx rayfin up functions deploy [-v] [--skip-build] [--json]
npx rayfin secret set|list|delete NAME [--stdin] [--describe="..."]
```

## Pattern: mint a scoped credential, return only that (djouallah `openCatalog`)
Take `ctx.Tokens.Storage`, call the OneLake Iceberg REST catalog for each table's current `metadata-location`, request a OneLake user-delegation key, HMAC-sign a read-only directory SAS, return `{metadata, missing, sas, expiresOn}`. The browser never sees a token. Details and string-to-sign in static-engine-patterns.md.

## Question -> doc (under `node_modules/@microsoft/rayfin-guide/assets/docs/`)
| Question | File |
|---|---|
| Need a function? app identity vs caller; `auth.type` | `functions/index.md` |
| `udf.func`, `RayfinContext`, entity import | `functions/writing-functions.md` |
| How `types.ts` is generated | `functions/typegen.md` |
| Secrets | `functions/secrets.md`, `cli/secrets.md` |
| Which audience; alias rules; Azure SDK adapter | `functions/connections/index.md` |
| SQL / OneLake / Fabric REST recipe | `functions/connections/add-fabric-resource.md` |
| Blob, Foundry, Azure DevOps | `add-azure-resource.md`, `add-foundry.md`, `add-ado.md` |
| Find server / GUID / OneLake path | `functions/connections/get-fabric-info.md` |
| Frontend `invoke`, timeouts, Vite adapter | `functions/invoking-from-frontend.md` |
| Scaffold, local host, deploy flags | `cli/functions/{init,dev-apply,deploy}.md` |

Limits not documented: payload size, memory, concurrency, cold start. Do not invent them.
