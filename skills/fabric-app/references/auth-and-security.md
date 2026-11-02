# Auth and security

## Identity model (get this right before designing anything)
| Runs as | What | Notes |
|---|---|---|
| Signed-in user | semantic-model connector (delegated), `ctx.getDataClient()` DB access, Category A connector if `auth.type: delegated` | their RLS, their permissions |
| App identity = the OWNER of the app item | `ctx.Tokens.*` in functions, Category A connector with `application` | whatever the owner can reach; grant the owner access, declaring an audience grants nothing |
| Browser | nothing privileged | holds a Rayfin session plus at most a short read-only credential minted server-side |

Consequences: the owner is a data-access decision, not only a deploy detail. A developer who can reach a resource
proves nothing about the deployed identity. Never return a raw token from a function; return a derived, scoped
artifact (a SAS) or the data.

## Sign-in
- Deployed apps: Fabric SSO (Entra) only. Email/password is local dev only; turning auth off makes deploy fail. Keep `auth.fabric.enabled: true`.
- Pick the flow by context:
  - inside the Fabric portal iframe: `initEmbeddedAuth()` on every page load, before restoring a stored user or rendering authenticated content (a stored session may be another user's). Statically import `@microsoft/rayfin-auth-provider-fabric` in the entry module so it captures `?fabricEmbedded=true` at load.
  - standalone tab: `ensureSignedInWithFabric()` called synchronously from a click handler (popups need a gesture). Silent first, interactive only on click; show a "Sign in with Fabric" button.
  - your own portal embedding the app: parent uses `@microsoft/rayfin-embed-host` `createEmbedHost` BEFORE mounting the iframe; origins exact (scheme+host+port).
  - Node/script acting as a user: `signInWithEntraToken()` (needs `fabric.externalEntraExchange: true`, delegated token with `Item.Execute.All`, user needs Execute on the item).
- One auth gate owns sign-in and nothing else knows about it (djouallah `auth.js`): draws a full-page overlay at load, `signIn()` resolves and removes it, `client()` re-checks the session. The page has no auth code.
- A kept, still-valid server answer can let the app start without a session (a `ready()` hook); the first call needing the server then demands a real session ("signed out: reload"). Good for latency; make sure the failure message is visible.
- Inside Fabric, MSAL redirect gets `X-Frame-Options: DENY` and popups land in another storage partition: acquire silently, and on failure render a Sign-in button using `prompt: 'select_account'` (the portal identity often differs from other cached accounts, causing 401).
- Cross-origin isolation (COOP/COEP, `coi-serviceworker`) breaks Fabric's sign-in popup ("Page not accessible directly"). Never enable it in a Fabric app.
- `isSupported()` / deep links: leave `targetOrigin` unset; restore launch state exactly once; do not sync router location back before the restore navigation lands; shared-link recipients are usually signed out, so carry the requested route through sign-in and validate it (same-origin app path, never the sign-in route). State <= 4 KiB JSON, never secrets, untrusted input.

## Hosting posture
`assetAccess: protected` (default: only users with item permission fetch assets) or `public` (anyone with the link gets the files).
- Either way keep the in-app auth gate. Public assets do not make GraphQL, auth or functions anonymous.
- Put nothing sensitive in the bundle in any posture (model JSON, endpoints, keys). Public is acceptable when all data sits behind the SAS function or the signed-in connector (djouallah chose public).
- Validate each posture separately in a clean browser (public: signed-out screen then sign-in; protected: restore and stale-session replacement; embedded: real host handoff). Local `autoLogin` cannot prove the signed-out screen.
- Anonymous data access (`@anonymous`) needs the tenant switch "Enable anonymous data access for Fabric Apps" (preview, off by default), applies to the app's own entities only, and is not an embedding substitute. [VOLATILE]

## Permissions on entities
- Every entity carries an explicit permission decorator (`@authenticated`, `@anonymous`, or `@role`). The CLI skill says omission silently grants full CRUD to every signed-in user; the guide's permission docs do not state the default, one vendored skill says "inaccessible". Treat omission as fail-open and never rely on it. `scripts/rayfin-lint.mjs` flags it.
- Only `anonymous` and `authenticated` roles exist. Prefer `@authenticated(...)`/`@anonymous(...)` over `@role('authenticated', ...)` (docs examples still use `@role`). Different field visibility per action = separate decorators with single actions.
- Per-user rows: a `user_id` `@text({max})` column plus `policy: (claims, item) => claims.sub.eq(item.user_id)`. Key policies on the immutable `sub`; email only as a label or `sub AND email`. Only claims `sub`, `email`, `role` exist; operators `.eq`, `.and`, `.or`. Test with a second account: the single author sees everything and the policy looks fine. How `user_id` is populated on create is not documented; verify against `rayfin-core` docs before asserting.
- UI roles are not authorization. A template with dispatcher/technician screens but `@role('authenticated','*')` everywhere lets any signed-in user read and write everything. Copy the UI, not the access model.
- Env-driven policy constants must throw at module load when missing (an empty `claims.sub.eq("")` is a silently broken boundary).
- No per-user read policy on a shared catalog is a legitimate choice only if documented: the app audience is then the disclosure boundary.
- Privileged functions: gate with a server-checked sentinel, not a client flag. Run the gate before any app-identity call (app-identity calls bypass the caller's own Fabric rights): e.g. read/create a fixed-UUID authority row that only the configured subject's row policy lets through, return a fixed message on denial.
- Storage-type apps (SAS over a folder) have no row or column security: the SAS covers the whole `Tables/` folder, and already-downloaded data in OPFS/localStorage cannot be revoked. Say so to the user.

## Functions and secrets as security boundaries
- Anything in the bundle is inspectable. Use a function for secrets, external tokens, privileged access, server-side validation.
- Function inputs come from an untrusted browser: validate against a closed grammar (e.g. `^[A-Za-z0-9_]+\.[A-Za-z0-9_]+$`), de-duplicate, take locations from app settings (secrets), never from the caller. Do not accept browser tokens, arbitrary URLs or arbitrary queries; use fixed `https://api.fabric.microsoft.com/v1/...` path patterns, reject redirects, cap pages/records/bytes, set a deadline, honour `Retry-After`, return fixed error codes without upstream bodies.
- DAX/KQL user values are not parameter-bound: allow-list identifiers, escape string literals (double `"`, `]]` in brackets, doubled `'` in table names).
- Store metadata, not content; collectors use allowlists and unexpected fields are not persisted.
- Secret values only through `npx rayfin secret set NAME` in an interactive masked prompt (or `--stdin` in CI). Never via chat, args, YAML, env files committed, logs. The `secrets:` block in rayfin.yml holds names and descriptions only. It is also the only per-item settings channel, so a non-credential setting (a catalog URL) lives there too.
- Never log tokens, prompts, bodies or keys. Error messages must contain no token or key.
- Do not pass a user's token in a JSON body to a shared-audience function (a pbi-fixer pattern acceptable only for a delegated-user tool); use `ctx.Tokens.*`.
- Do not use the Iceberg catalog's vended credentials (`X-Iceberg-Access-Delegation`): OneLake vends `sp=racwdl` (read-write-delete). Sign your own `sp=r` SAS (static-engine-patterns.md).

## Sharing and capacity facts
Item permissions: "Run and interact" (open the app and call its APIs), "Edit" (docs say deploy; the service enforces owner), "Reshare" (workspace admin). Workspace roles do not supersede item permissions. Always test the deployed app with a second, non-owner user who has only workspace Viewer plus "Run and interact"; owner-only and delegated paths behave differently from the author's session and `connector inspect` runs under your own token.
