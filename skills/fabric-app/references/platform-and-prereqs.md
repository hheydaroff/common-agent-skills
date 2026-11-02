# Platform, prerequisites and what to promise

Fabric apps (item type "App (preview)", product name Rayfin) are web apps hosted by Fabric: static hosting, Fabric
SSO (Entra), an optional managed SQL DB behind GraphQL, optional server functions, optional connectors to other
Fabric items. You define it in code (`rayfin/rayfin.yml`, `rayfin/data/*.ts`, `rayfin/functions`) and ship it with
`npx rayfin up`. There is no designer. Everything here is preview-era: items marked [VOLATILE] must be re-checked
before you assert them.

## Three shapes (pick one before writing code)

| Shape | Backend | Pick it when | Read |
|---|---|---|---|
| Operational app | managed SQL DB, entities, GraphQL | the app owns data: write-back, workflow, per-user records | operational-apps.md |
| Data app | `fabric-semanticmodel` connector, DAX | custom UX over an existing semantic model, queries run as the signed-in user | data-apps-semantic-model.md |
| Static analytics app | one signing function + files in OneLake | heavy or ad hoc SQL in the browser, no per-query capacity spend, you control the engine | static-engine-patterns.md |

They combine (one project may hold entities and a connector). Ownership is per item, not per part: functions and application-auth connectors run as the item OWNER, while entity policies and delegated connectors run as the CALLER, so a mixed app needs both answers (auth-and-security.md). `fabric-sqlanalytics|warehouse|sqldatabase`
connectors cover data that already lives in Fabric SQL items (connectors.md). A function covers secrets, external
APIs, Fabric REST, OneLake files (functions-and-secrets.md).

## Do not build a Fabric app when
- The need is a standard report with self-service, cross-filtering, accessibility for free: a Power BI report is more mature. A data app trades that baseline for bespoke UX and code someone must own.
- Write-back from inside an existing report: translytical task flows (GA since 2026-03) are the stabler foundation. [VOLATILE]
- External users (clients, partners, citizens). Deployed apps use Fabric SSO only, for users with workspace/item access; the docs are silent on guests, there is no app-owns-data mode. Route external analytics to Power BI Embedded or a portal. If the user asks for "3 external auditors" anyway: ask whether they are B2B guests in the tenant, say guest access is undocumented, propose the app for internal staff plus a Power BI report for the auditors, or a time-boxed pilot with one guest account; never promise it.
- Multi-step transactions / stored procedures, or a custom auth provider beyond Fabric SSO.
- "Org apps" and "workspace apps" are distribution containers for reports, not Fabric apps. Ask which one is meant.

## Prerequisites: confirm all four before scaffolding
Each fails differently and late.
1. Tenant setting on: "Fabric Apps (preview)" (some tenants label it "Enable Fabric App Items (preview)"). Only a tenant admin can set it; it can be scoped to security groups and takes a few minutes to propagate. Until then "App (preview)" is missing from New item. Tell the user; you cannot do it.
2. Workspace on an F-SKU or trial capacity, in a region that has Fabric apps (whether a Pro/PPU/Premium-only workspace can host the app item is unverified: see powerbi-only-profile.md). UK South/West did not at Aug 2026; 18 regions were excluded at 2026-09-25. [VOLATILE] Check the region before buying capacity. Functions and Storage carry extra per-region/tenant gates.
3. The account can create items in that workspace (Contributor/Member/Admin).
4. Data-app extras: tenant setting "Semantic Model Execute Queries REST API" on, and every user holds Build + Read on the model. SAS-based apps: workspace setting "Authenticate with OneLake user-delegated SAS tokens" on (default off) and the item owner can read the lakehouse.

Rayfin CLI >= 1.34 for the semantic-model connector path (the experimental connector also needs a workspace-level switch). Node: LTS only (20, 22, 24; odd majors unsupported). Pausing an F-SKU when idle saves money; a paused capacity shows as capacity errors in the app.

## Who can open an app, what it costs
- Viewers need item permission "Run and interact" (workspace members get it by default). Deploying needs the owner (see deploy-and-ci.md), whatever the docs say about Edit.
- Semantic-model apps inherit the model's RLS and measures per user (delegated). A wrong RLS rule or measure reaches every surface.
- Entity apps enforce `@role` policies in the backend. Category B connectors (semantic model, KQL) rely on the source's own security.
- Do not build a licensing case on "Pro/PPU get Fabric apps free up to 1 GB". It was announced, not in Learn at 2026-10, and viewer needs below F64 are undocumented. Tell the user to test in their tenant. [VOLATILE]
- No CU-per-call numbers exist anywhere; services draw from the assigned capacity.

## Preview-era limits to tell the user up front
No ALM, no workspace outbound access protection, no private links, no built-in multi-environment management (as of 2026-10). Deployment-pipeline promotion of the SPA exists (app-backend/deployment-pipelines.md) but functions and secrets are out of scope. Microsoft marketing says GA, Learn says preview; trust Learn's newer wording for the item. Authors who built with Claude Code advise "build and learn, production after GA".

## Volatile ledger (re-verify; state at 2026-10)
| Item | State |
|---|---|
| microsoft/rayfin#61 owner-only 403 on `rayfin up` | open; owner-after-transfer fix "rolling out soon" (2026-09-01) |
| #89 functions return opaque 500 on service-principal-owned item | open, assigned, repro 1.36.0-1.36.2 |
| #93 Category A connector 401 `CONNECTOR_AUTH_FAILED` on SP-owned item | open |
| #92 SP gets 403 FeatureNotAvailable creating an AppBackend | title only, body unverified |
| #8 `403 The feature is not available` | tenant switch for Fabric apps was off |
| Anonymous data access | preview, off by default, tenant-admin switch |
| Functions | GA in 1.36 per rayfin.ai but "not available in every region or tenant"; Storage experimental; Kusto connector held |
Check `gh issue view <n> -R microsoft/rayfin` or the page before relying on any row. Capture the `RootActivityId` from every 403/500 for a support ticket (Microsoft asks for region, item id, activity id).

## Pinning
Exact-pin anything that talks to a preview service or reaches into internals (fabric-cicd, Azure SDKs, a dev build of an engine). Commit lockfiles, install with `npm ci`. Do not take npm `latest` for a dev-channel package without checking what the tag points at (duckdb-wasm `latest` was a build that breaks OPFS). Keep the Rayfin client, auth-provider and connector packages on the same version (a CDN-loaded pair on different versions yields two Auth instances and a session that never completes).
