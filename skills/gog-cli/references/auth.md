# gog auth: setup and troubleshooting

## One-time GCP setup (per Google account owner, shared by all mailboxes)

1. console.cloud.google.com: new project, then **APIs & Services, Library: enable the API** (Gmail API for mail; add Calendar/Drive as needed).
2. **Google Auth Platform**: Get started, app name + support email, Audience **External** (consumer `@gmail.com` cannot use Internal), contact email.
3. **Audience, Test users: add every Gmail address you will authenticate.** Missing address = `Error 403: access_denied`.
4. Don't add scopes in the console; gog requests them.
5. **Clients, Create client, Desktop app**, download the JSON. It holds a secret: don't commit or paste it. Delete it after step below (gog keeps its own copy).

```bash
gog auth credentials set ~/Downloads/client_secret_*.json
gog auth credentials list
gog auth setup <email>        # interactive walkthrough of the above, if preferred
```

## Add / inspect / remove accounts

```bash
gog auth add a@gmail.com --services gmail --gmail-scope readonly
gog auth add b@gmail.com --services gmail --gmail-scope readonly
gog auth list                 # accounts, client, services, created time
gog auth list --check         # validates each refresh token
gog auth doctor               # ok/fail per check: keyring.open, tokens, credentials
gog auth alias set shop b@gmail.com     # then: gog -a shop ...
```
The consent page for read-only must show only a read permission. If it mentions modify, send or delete, abort and rerun with `--gmail-scope readonly`. Other scope flags: `--drive-scope full|readonly|file`, `--extra-scopes URI,...`.

Multiple OAuth clients (e.g. work vs personal GCP project): `gog --client work auth credentials set work.json`, `gog --client work auth add ...`. Tokens are isolated per client.

No browser available: `gog auth add ... --manual` (open the printed URL elsewhere, paste the redirect URL back) or `--remote` for server flows.

Revoke: https://myaccount.google.com/permissions, remove the app. Local removal: `gog auth remove <email>`.

## Failure to fix map

| Symptom | Cause | Fix (user runs it) |
|---|---|---|
| `invalid_grant`, "expired or revoked", works for a week then stops | App is **External + Testing**: Google expires refresh tokens after ~7 days | `gog auth add <addr> --services gmail --gmail-scope readonly --force-consent`. Permanent fix: Auth Platform, Audience, **Publish app** (In production; stays unverified, click through the warning), then re-auth with `--force-consent` so the new token is minted under the new status |
| `403 access_denied` at login | Address not in Test users | Add it under Audience, Test users |
| "Google hasn't verified this app" | Normal for unverified personal apps | Advanced, Continue |
| `403`/"API has not been used" | Gmail API not enabled in the project | Enable it in Library |
| Keychain prompt loops, or empty token after `auth add` over SSH | macOS login Keychain locked in a headless session (gogcli issue 206) | Run auth from a GUI terminal, or use the file backend below |
| Keyring password prompts under launchd/systemd/cron | Service env lacks the variables your shell has | Set both variables in the **service** environment |
| `Insufficient Permission` on a write | Token was issued read-only | Intentional. Re-auth without `--gmail-scope readonly` only if the user approves the write |

## Headless / non-interactive keyring

```bash
gog auth keyring file                      # switch backend
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD='<passphrase>' # exactly this name; older aliases are ignored
gog auth doctor --check --no-input         # run from the agent's own entrypoint, not just your shell
```
Docker: `ghcr.io/steipete/gogcli:latest` with the same two variables. Config root override: `--home` / `GOG_HOME`.

## Diagnosis order

1. `gog auth doctor --check --no-input` from the same environment the agent uses.
2. `gog auth list --check` to see which account's token is dead.
3. Re-auth that account with `--force-consent`.
4. If still failing, check the account is in Test users and the API is enabled.
