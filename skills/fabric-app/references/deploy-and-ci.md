# Deploy, ownership and CI

## The deploy loop (laptop)
```
npx rayfin login                       # Entra; --select / -t <tenant> to pick
npx rayfin up -n                       # dry run; add --workspace-id <g> on a machine with no .deployments.json
npx rayfin up --output json            # builds static, syncs settings, applies schema + connectors, deploys functions
npx rayfin up status --json            # exit 0 ok, 1 config/command error, 2 check failed/auth/cancelled
```
Then validate in a real browser (below). "Make it live" means run the workflow yourself, not hand the user steps.
`rayfin up` writes `rayfin/.deployments.json` (per-workspace record: item id, hosting URL, publishable key; `active` = last deployed) and appends the hosting URL to `allowedRedirectUris`. New items: `--item-name <n>` (default is the project `id`, which collides), `--workspace-id`, `--capacity-id` (never together with `--workspace*`). Do not add `--yes` unless the item name and workspace are pinned on the command line (it also approves capacity assignment and reuse of a same-named item); CI pins both and uses `--yes` on purpose so later runs reuse the item without asking. Do not add `--force` unless the user asked.
Narrow commands: `up db apply` (schema only), `up staticapp deploy [--skip-build]`, `up functions deploy`, `up connector apply`, `up --exclude-services staticHosting` (what `dev` uses). Static ZIP limit 100 MB: drop source maps and large assets.

## Never trust the green
- `rayfin up --json` can exit 0 with `"status":"success"` while `steps.dbConfig.status` is `error` (reported at 1.34). Parse `steps.*.status`, fail on any `error`.
- Connector apps: require one `generate[]` entry per declared connector (inspect your CLI version's JSON first, e.g. `jq '.generate'`; the path is not documented in what was read); missing or `status:"error"` blocks; `skipped` is acceptable only for a documented Category B `non-graphql-connector`; ignore `skippedConnectors`.
- A function deploy reporting `Complete`/`Ready` does not mean invocation works.
- Frontend and backend deploy separately: verify the RUNNING system (hosting URL), not the build. Persist-then-reload for app-owned records (create, reload, update, delete).
- Validate per posture on the deployed URL in a clean session, with a second non-owner user (auth-and-security.md). Local `autoLogin` and `rayfin dev` prove nothing about the deployed signed-out and restore paths.
- `npm run build` in some templates is `tsc -b --noCheck`: it does not prove types. Run typecheck, build, lint, test once, serially, before deploy. Do not start the backend or frontend for the user unprompted; the starter flow tells the user to run the app when ready.

## Ownership decides everything
`rayfin up` is OWNER-ONLY: only the identity that created the app item can deploy backend changes (`403 Forbidden ... Only AppBackend artifact owner can perform this operation`). Docs say Edit permission suffices; the service enforces owner (one reporter says the original CREATOR, even after "Take over"). The owner is also the identity functions and Category A connectors run as.
- Decide ONE owner/deployer per item and write it in the README. Laptop and CI cannot share an item: give CI its own item names (djouallah: CI deploys `vertipaq` and `iceberg`, the human deploys `nem` with `--item-name nem` in another workspace). In the exemplar the CI-deployed `iceberg` item is known dead for the #89 reason (its function returns 500) and is kept only to exercise the deploy path; only the laptop item works.
- How to tell who owns an item: portal Settings > About shows the owner; an item first created by a workflow using `azure/login` with a client id or `rayfin login --service-principal` is SP-owned. "Take over" is unreliable (one reporter stayed locked out). Migration off an SP-owned item that needs functions: create a NEW item under a human with a new `--item-name`, point users to it, retire the old one in the portal (who may delete it is unverified).
- A service-principal-owned item: functions return opaque `500` on every call (#89) and Category A connectors return `401 CONNECTOR_AUTH_FAILED` (#93, reported for both `application` and `delegated` auth). Deploy and CI succeed, the app is dead. Until fixed, apps with functions or Category A connectors must be human-owned and deployed from a laptop. Static-only apps are safe from CI. A semantic-model (Category B, delegated) app is deployed from CI in the exemplar, but no source verifies it working end to end afterwards: test it with a non-owner before relying on it. [VOLATILE]
- There is no supported API or UI to assign a service principal as owner or to transfer to or from one. SP creation of an AppBackend has hit `403 FeatureNotAvailable` (#92).
- Prove host vs code failures by A/B: two throwaway items, same workspace, same code, one human-owned, one SP-owned; a handler that catches everything and returns its failing step. If no step name returns, the handler never ran (host side). `Missing required header 'x-ms-rayfin-info'.` on the public invoke route proves the worker starts.

## CI recipe (GitHub Actions, no stored secrets)
```
permissions: { contents: read, id-token: write }
- uses: azure/login@v2        # federated OIDC; allow-no-subscriptions: true (Fabric-only tenants have none)
- run: |
    TOKEN=$(az account get-access-token --resource https://api.fabric.microsoft.com --query accessToken -o tsv)
    echo "::add-mask::$TOKEN"; echo "RAYFIN_TOKEN=$TOKEN" >> "$GITHUB_ENV"
- run: npm ci                                  # one install of the CLI
- run: npx rayfin up --item-name <n> --workspace-id "$WS_ID" --yes --output json
```
- `RAYFIN_TOKEN` replaces interactive login; `rayfin login --service-principal --client-id --client-secret --tenant` is the alternative. Mask the token.
- Ids (tenant, client, workspace, lakehouse) go in repo variables (public identifiers). Pin the federated credential subject to the ref: `repo:<owner>/<repo>:ref:refs/heads/main`. One Entra app per tenant, selected by an expression on the tenant input; fail the first step naming the tenants that have one.
- The SP needs membership (Contributor+) in the workspace; the workspace must be on a capacity in a region that has Fabric apps.
- Commit `rayfin/functions/host.json`; lockfiles must resolve from `registry.npmjs.org` (a laptop-generated lock may name a private feed the runner cannot read); `npm ci --prefix rayfin/functions` before `up`.
- Connector with ids: not committed. Run `connector add` BEFORE `rayfin up` so the deploy ships it. The exemplar keeps no generated connector files: its page sends raw DAX, so only the alias must match the client code (`connectors: { nem: ... }`). For templates with generated `rayfin/connectors/<name>/` files, whether to commit or regenerate them in CI is unverified; run `connector add` in a scratch checkout and see what changes. For local development add the entry locally and do not commit it. At deploy time look the item up by name and add it (keep `--operations executeQuery`):
  `MODEL_ID=$(curl -sf -H "Authorization: Bearer $RAYFIN_TOKEN" https://api.fabric.microsoft.com/v1/workspaces/$WS_ID/semanticModels | jq -r '.value[] | select(.displayName=="nem") | .id')` then `npx rayfin connector add --type fabric-semanticmodel --workspace-id "$WS_ID" --item-id "$MODEL_ID" --name nem --yes`. Leave a comment in rayfin.yml saying the entry is deliberately absent. Fail with `::error::` naming the prior step that creates a missing dependency. Print the block with GUIDs masked.
- New item + secret: `up`, then `if ! npx rayfin secret list | grep -q NAME; then echo -n "$VAL" | npx rayfin secret set NAME --stdin; npx rayfin up functions deploy; fi`.
- Independent apps: `if: ${{ !cancelled() && inputs.<app> }}` on every step after the first app (default `success()` skips later apps after one failure; `!cancelled()` still honours a manual cancel). Put the app expected to fail last.
- Also in the deploy workflow: wrap `rayfin up --json`, fail on any `steps.*.status == "error"`, and capture `RootActivityId` from any 403/500.
- Production gate: use a GitHub Environment with required reviewers and bind the federated credential subject to `environment:<name>` instead of the branch ref [INF: standard GitHub OIDC practice, not shown in the exemplar]. In a monorepo set `working-directory` to the folder that holds `rayfin/`.
- `up -n` needs `--workspace-id` on a fresh runner (there is no `.deployments.json`); a dry-run step in CI is optional.
- Dispatch-only for anything that creates Fabric items or runs a pipeline; `concurrency: { group: deploy-fabric-<workspace>, cancel-in-progress: false }` (cancelling mid-publish leaves half-deployed items). One boolean input per part, default ON for correctness parts and OFF for cost parts (hourly schedule).
- Default the target to a TEST workspace: `WS_ID: ${{ inputs.workspace_id || vars.TEST_WS_ID }}`; production is an explicit input. Turn pipeline schedules OFF in test (a scheduled pipeline burns capacity forever). A deploy must not assume a workspace it did not create: it installs its own copy of the stack.

## Whole-stack deploy order (app + data + model)
items (lakehouse, notebook, pipeline) -> upload code -> run the pipeline once and wait -> semantic model -> app connector/secret -> app deploy. The model names tables a first run creates; a model deployed before its tables stays broken until the next good deploy.
- Publish items with `fabric-cicd` `publish_all_items` (create-or-update, idempotent); give each item a stable `.platform` `logicalId`; generate derived artefacts (e.g. `model.bim` from a YAML) into a temp dir at deploy, never commit them; substitute `{WS_ID}`/`{LH_ID}` placeholders at deploy (Direct Lake has no parameter for them).
- Upload code from `git archive HEAD`, not the working tree, delete the target folder first, and write a `COMMIT` file; laptop and CI then ship identical bytes.
- Poll async Fabric jobs from the `Location` header of the job POST every 30 s until `Completed|Failed|Cancelled|Deduped`; on failure print the last ~80 lines of a log the job wrote to OneLake (`Files/logs/run.log`); wrap the log fetch in try/except.
- Contract-check after every model deploy: refresh, a row count per table, each measure over a recent window, one query per measure so one bad measure fails alone; exit 1 on any failure. Retry the first query ~8x at 30 s for a newly created model (OneLake access propagates late). Query by XMLA (ADOMD.NET under pythonnet, data source `powerbi://api.powerbi.com/v1.0/myorg/<workspace NAME>`, token as password); REST `executeQueries` answers 401 to a service principal on a single-sign-on Direct Lake model. [VOLATILE]
- Dispatched data workflows can be cancelled by the next scheduled run queuing behind them (one concurrency group): read the conclusion before deploying a model on its strength.
- Token resources: Fabric `https://api.fabric.microsoft.com`, Power BI/XMLA `https://analysis.windows.net/powerbi/api`, OneLake/ADLS `https://storage.azure.com/`.

## Test ladder (cheap to expensive)
1. Lint on every push for rules in the architecture ("the page does no arithmetic").
2. `node --test` of compiler/queries on made-up deterministic fixtures; no capacity.
3. Engine-vs-engine parity on deployed files (two clients, same questions, rows compared; blocks the deploy; an explicit `deploy_anyway` override that still runs the check, not a disabled gate).
4. A/B of the previous commit vs this one in the same session (`git worktree add --detach`), rows compared, time reported not judged; alternate old/new, 10 ms deltas are noise.
5. The deployed model as reference, asked the same DAX, dispatch only because it spends capacity. Compare with tolerance (a cent, 1e-6 relative); skip oversized queries and list them (computing a huge result throttled the capacity for ~20 s on every later query). Skip re-asking queries whose content key (DAX + SQL with dates stripped + DAX of every measure reached) is unchanged since the last green parity run.

## Promotion
Dev -> test -> prod via Fabric deployment pipelines is documented for the static bundle (`resolveRayfinConfig`, see rayfin-project.md); functions and secrets are out of scope today. Whether pipelines or Git integration support the app item type is unverified. Two deployments in one project coexist in `.deployments.json`; `up list` / `up switch <name>` move between them.

## Publishing a static site next to Fabric (djouallah, Pages)
Blobless depth-1 no-checkout clone; `git add -f` the published paths (a deploy repo's `.gitignore` silently skips NEW files under `git add --all`); retry the whole publish (5 x, back-off); concurrency group; a weekly history squash if a file is redeployed hourly. Details in worked-example-analytics-as-code.md.
