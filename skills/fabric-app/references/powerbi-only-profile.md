# Profile: Power BI semantic model only

Use when the user says: the only data source is a Power BI semantic model, no other Fabric item (no lakehouse,
warehouse, SQL DB, OneLake, notebook, pipeline), runs on a Power BI workspace. This file narrows the skill. It
overrides the shape table in SKILL.md; everything else still applies.

## What this profile means
- Shape = **data app** only: `fabric-semanticmodel` connector, DAX through `executeQuery`, delegated auth. Queries run as the signed-in user, so the model's RLS and measures apply.
- OUT of scope, do not scaffold, do not load: entities / managed SQL DB (`services.data` off), functions and secrets (`services.functions` off, no `secrets:`), Storage, Category A connectors, static DuckDB/OneLake engine, `openCatalog` patterns.
- That removes most traps: SP-owned-item bugs #89 (functions) and #93 (Category A) do not apply; no secret ordering; no SAS; no OneLake settings. What is left: owner-only deploy, tenant/workspace prerequisites, the connector, DAX, RLS, sign-in, validation.
- Reference files to load: `data-apps-semantic-model.md` (core), `connectors.md` (Category B rows only), `auth-and-security.md` (sign-in, hosting posture), `deploy-and-ci.md` (ownership, `up` loop), `frontend-design-and-validation.md`, `troubleshooting.md` (connector, 403, sign-in rows). Skip the rest.

## "Purely on a Power BI workspace": what is and is not established
A Fabric app is still a Fabric item (an AppBackend created by `rayfin up`) and is not a Power BI artifact.
- Established (Learn, data-apps-template): the model may be "hosted on Fabric or Power BI capacity"; needs the Semantic Model Execute Queries REST API tenant setting and Build + Read for each user. [VOLATILE]
- Still required: the tenant admin enables "Fabric apps (preview)"; the deployer has Contributor/Member/Admin in the target workspace; Node LTS.
- NOT established: whether the app item itself can be created in a workspace on a Pro/PPU/Premium (non-Fabric) licence mode. Learn's create flow says "select Fabric capacity", and the Pro/PPU extension was announced but is not in Learn (2026-10). Do not assume it. First action in this profile: have the user try `npx rayfin up -n` and then a real `rayfin up` with a throwaway app in the target workspace, and read the error. If it fails, the options are a Fabric trial or F-SKU workspace for the APP item only, while the model stays in its Power BI workspace (the connector takes `--workspace-id` and `--item-id` of the model, so app and model may live in different workspaces). Verify that split on a pilot too. [INF]
- If the user's real goal is "no Fabric at all", say plainly that Rayfin cannot give that; alternatives are a Power BI report, a custom visual, or Power BI Embedded.

## Model checks before building
1. Storage mode: Import or DirectQuery keeps the profile pure. A **Direct Lake** model silently depends on a Fabric lakehouse/warehouse, so it breaks the "no other Fabric component" premise. Ask.
2. RLS: does the model define roles, who is in each, what does each filter? The app only inherits it (`data-apps-semantic-model.md`, "Proving per-user RLS"). The model owner/author and workspace admins are normally exempt from RLS, so test with non-owner users in different roles.
3. Every user has Build + Read on the model; the Execute Queries tenant setting is on and scoped to them.
4. Query limits of the Power BI Execute Queries REST API apply underneath (row/value caps, per-user request rate). Not verified in this research; read the current REST docs before sizing visuals and set a `resultSetRowCountLimit`. [INF]
5. DirectQuery with SSO to a source, or a Live-connected AAS model, may not work through Execute Queries; test one query early. [INF]

## Compact operating loop
1. Confirm: workspace licence mode, model storage mode, RLS yes/no, internal users only, who deploys. Ask what is missing.
2. Pilot deploy of an empty app to the target workspace (see above). Stop and report if it fails.
3. Scaffold `universal-app`, read the project's own docs, `connector search` the model (exactly one match), `connector add --type fabric-semanticmodel ... --operations executeQuery`, keep auth `delegated`.
4. Discover schema progressively (INFO.VIEW.*); design queries as measures; probe each through the CLI.
5. Build; `rayfin-lint.mjs`; deploy with `up -n` then `up --output json`; require a `generate[]` entry for the connector.
6. Verify on the deployed URL as two non-owner users in different RLS roles (totals must differ), plus a user with no model access (needs a clear error, not endless loading).
7. Document the owner and deployer in the README. A CI deploy of a pure Category B app is plausible but unverified end to end: pilot it before committing to CI-only ownership, and keep a human able to take over.

## rayfin.yml shape for this profile
```yaml
services:
  auth: { type: fabric }          # keys per your CLI version; check the in-project docs
  data:  { enabled: false }
  functions: { enabled: false }
  staticHosting: { enabled: true, buildCommand: npm run build, assetAccess: protected }
connectors:
  - { name: sales, type: fabric-semanticmodel, auth: { type: delegated } }   # GUIDs added by `connector add`
```
Key names are indicative only: the lint and the in-project docs are authoritative. Run `rayfin-lint.mjs`; it warns when a Category B connector is not `delegated`.
