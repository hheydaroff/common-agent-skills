# Rayfin project: docs-first protocol, scaffold, layout, config

## Docs-first (the rule the official skills insist on)
Rayfin packages ship version-matched docs inside the install. Remembered APIs are routinely wrong against the
installed version, so read before writing.
1. `node_modules/@microsoft/<pkg>/package.json` -> field `rayfinDocs.dir` (always `assets/docs`) -> read `index.md` -> follow links.
2. `@microsoft/rayfin-cli` has no docs root; CLI, deploy and workflow questions are answered by `@microsoft/rayfin-guide`.
3. When the index does not say which file: `npx rayfin docs search '<topic>'`; for a package you lack: `npx rayfin docs discover '<topic>'`. Same via MCP (`search_docs`, `get_doc`) if installed. Run from the project root so the project's node_modules wins; else `npx -y @microsoft/rayfin-cli docs ...`.
4. Being unable to read these is the only block. Do not offer "a general approach" or sample code from memory instead.

| Question | Read (under `node_modules/@microsoft/`) |
|---|---|
| Decorators, field options, reserved entity names, policy DSL | `rayfin-core/assets/docs/{decorators,permissions}.md` |
| What the platform will not do (read before designing entities) | `rayfin-guide/assets/docs/known-limitations.md` |
| Entity overview, relationships, per-user policy | `rayfin-guide/.../data/{overview,permissions,graphql,validation}.md` |
| Typed client queries, paging, nullability | `rayfin-data/assets/docs/` |
| rayfin.yml fields, tsconfig/Vite needs, `.env*` roles | `rayfin-guide/.../getting-started/project-structure.md` |
| Auth client, Fabric SSO, embed host, Entra token sign-in | `rayfin-guide/.../auth/{overview,fabric,external-embed-host,direct-entra-auth}.md` |
| Static hosting, redirect URIs, 100 MB limit | `rayfin-guide/.../hosting/index.md` |
| What `rayfin up` does, CI login, dry run, capacity, status exit codes | `rayfin-guide/.../app-backend/deploy.md` |
| Item permissions, endpoint | `rayfin-guide/.../app-backend/index.md` |
| Promotion dev->test->prod | `rayfin-guide/.../app-backend/deployment-pipelines.md` |
| Deep links | `rayfin-guide/.../app-backend/deep-linking.md` and `rayfin-app-state-fabric/assets/docs/` |
| Functions, secrets, connections | see functions-and-secrets.md routing table |
| Connectors | see connectors.md routing table |
| Env vars, precedence, `${VAR:-default}` | `rayfin-guide/.../cli/{environment-variables,env-interpolation,env-migration}.md` |
| Local auth in Vite | `rayfin-local-dev/assets/docs/` |
| Deprecation warnings `[RAYFIN_DEP_*]` | `rayfin-guide/.../deprecations.md` |

## Scaffold (agent mode, non-interactive)
- Already a Rayfin project (has `rayfin/rayfin.yml` or a `@microsoft/rayfin-*` dependency)? Continue in place. Never create a nested or sibling project, even when the user says "build a new app".
- Non-Rayfin app present: `npx rayfin init` in place (`npx -y -p @microsoft/rayfin-cli@latest rayfin init --project-name <n>` if the CLI is not installed).
- Empty directory: `npx -y @microsoft/create-rayfin@latest --project-name <name> --template universal-app`. `--project-name` is required without a TTY; `npm create` mangles piped stdin and flags. It creates a child directory: `cd` into it. Template ids: `todoapp`, `dataapp`, `blankapp` (= hidden `universal-app`); list with `npx rayfin init --list-templates`. Windows drops `--`: use `npm.cmd create ... -- --template x`.
- Which template: Microsoft's agent stance is `universal-app` (lean base; its capability router enables services and skills on demand; connector-native). The Learn-documented path for semantic-model apps is `--template dataapp` (visuals, data grid, validation kit) followed by `connector add`; the published sample still ships the older `@microsoft/fabric-app-data` client, which Learn says to REPLACE with the connector client rather than keep two data paths. Default to `universal-app`; choose `dataapp` only if you want its kit and will replace the client in the same change.
- After scaffold, read the project's `AGENTS.md` and `.agents/skills/rayfin/SKILL.md` (generated, `rayfin-managed: true`, version-locked) and follow them over this skill where they are more specific. Plan before building; confirm the plan with the user.
- Prereqs (platform-and-prereqs.md) first; `git` and `gh` are expected by the starter flow.

## Layout (what Rayfin wants where)
```
rayfin/rayfin.yml            committed; id/name/version, services.*, secrets[], connectors[]
rayfin/data/<Entity>.ts      one entity per file; ALL registered in rayfin/data/schema.ts
rayfin/data/schema.ts        data disabled? still required: export type BlankAppSchema = {}; export const schema = []
rayfin/tsconfig.json         keep Rayfin's TS config isolated from the app's
rayfin/functions/            src/function_app.ts; types.ts + secrets.generated.ts GENERATED; host.json COMMIT
rayfin/connectors/<n>/       metadata.json, schema.ts (Category B schema.ts is @generated)
rayfin/.env  .env.example  .deployments.json  .temp/   env (ignored), example (committed), deploy record (ignored), cache (ignored)
```
- `.gitignore`: `**/rayfin/.env*`, `**/rayfin/.deployments.json`, `**/rayfin/.temp/`, `.agents/`, `.mcp.json` (Rayfin regenerates agent context locally). Delete `rayfin/.temp/` when schema or config looks stale, then redeploy.
- TC39 Stage 3 decorators: never enable `experimentalDecorators` or `emitDecoratorMetadata`; bundler target ES2022 (`@vitejs/plugin-react`, not `-swc`, per the guide). Entity files use `.js` in relative imports.
- Several apps sharing one CLI (djouallah): one `package.json` with `@microsoft/rayfin-cli` as devDependency, `npm ci` once, run `npx rayfin` inside each app folder (cwd decides the project). Shared build script via `staticHosting.buildCommand: node ../common/build.mjs`.
- Universal-app workspaces use `packages/{frontend,data,shared,functions}` and `npm run pack:add -- <connectors|analytics|visuals|data-modeling|functions>`. Run packs one at a time, serially; a "preserved file" report means stop and tell the user; `--force-seeds` only with approval. Never run `npx rayfin functions init` there (it writes a legacy `rayfin/functions`).

## rayfin.yml keys that matter
`services.auth.{enabled, fabric.enabled, fabric.externalEntraExchange, password.enabled, allowedRedirectUris[]}`,
`services.data.{enabled, dialect: mssql}` (dialect is mandatory when data is enabled),
`services.staticHosting.{enabled, folder, buildCommand, indexDocument, assetAccess: protected|public}`,
`services.functions.{enabled, buildCommand, auth.type: application}`, `secrets: [{name, description}]`, `connectors`.
- `assetAccess` is missing from the guide's option table (it appears in templates and CLI code). Non-interactive deploys without the key record `protected`. Choose it on purpose (auth-and-security.md).
- `allowedRedirectUris`: bare origins. Localhost ports you add yourself; the deployed hosting URL is appended by `rayfin up` (one template README says add it by hand: check after the first deploy and add if missing). A deleted-and-recreated app gets a new `*.webapp.fabricapps.net` origin; delete the stale `.deployments.json`.
- `${VAR}` / `${VAR:-default}` interpolation works in rayfin.yml; unset without a default is a hard error; shell beats `.env`.
- Change rayfin.yml, then restart `rayfin dev` or `rayfin up`. Toggling auth needs a backend restart.

## Env and scripts
- `.env.local` is generated (`npx rayfin env --framework vite`); never hand-edit. Only `RAYFIN_PUBLIC_*` reaches the frontend (`RAYFIN_PUBLIC_API_URL -> VITE_RAYFIN_API_URL`, `..._PUBLISHABLE_KEY`, `..._ITEM_ID -> VITE_FABRIC_ITEM_ID`, `..._WORKSPACE_ID`, `..._PORTAL_URL`, `..._FUNCTIONS_URL`). Publishable keys (`pk-*`) are safe in client code; service secrets and connection strings are not.
- If the app may be promoted through deployment pipelines, build the client with `resolveRayfinConfig(...)` and read Fabric coordinates from `client.runtimeConfig`, never from `VITE_FABRIC_*` at call sites (promoted bundles are byte-identical; baked values keep pointing at the source stage).
- Inner loop is `npx rayfin dev` / `npm run dev`. It provisions or reuses a real Fabric AppBackend (needs login, capacity, tenant switch); it never publishes static content. Docker provider is preview behind `RAYFIN_FEATURE_FLAGS=docker-local-dev`. Connectors do not run under `rayfin dev`.
- `"dev": "rayfin dev"` with no `dev:frontend` child gives a recursion error: add `"dev:frontend": "vite"`.
- Demo/offline mode (copy it): ship the app so it runs with zero Fabric config. One seam, not scattered `if (demo)`: `bootstrapAuth()` returns `null` when any required value (API URL, publishable key, workspace/item id, portal URL) is blank or an all-zero GUID; a `DataSource {label, fetch}` interface with a static and a Fabric adapter; a visible "demo data" banner. Keep `npm run dev` free of rayfin pre-hooks (put `rayfin env`/`rayfin up` in `dev:fabric`), or demo mode dies before Vite starts. Agents without a tenant can then run, test and screenshot the app.
- Publishing a project as a template: `.templateignore` is a publication boundary (always exclude `rayfin/.env*`, `rayfin/.deployments.json`, `.env.local`, `dist/`, tenant-bound item definitions); audit bytes for GUID/endpoint/key regexes, not file lists. Keep dir name == `package.json template.name` == `manifest.json templateId` == `rayfin.yml id`; generate `rayfin-template.yml` with the gallery script, do not hand-edit.

## Agent files
`npx rayfin init ai-files install` writes AGENTS.md (one time, never overwritten) and skills carrying a `rayfin-managed: true` sigil. Remove the sigil to opt a skill out of updates; `--force <id>` replaces one. `install -n --json` previews; exit 3 = success with warnings.
