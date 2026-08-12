# Bitbucket Cloud — PR Creation Reference

Bitbucket has no first-party CLI for PRs; this skill uses the Cloud REST API 2.0
via `scripts/bb.sh` (resolve paths against this skill directory).

## Auth setup (one-time)

Two options, in order of preference:

1. **Workspace or repository access token** (Bearer) — narrow scope, revocable.
   Create in Bitbucket: Workspace settings → Apps and features → Access tokens
   (repo tokens: repo settings → Access tokens). Scopes needed: **Pull requests: Write**, **Repositories: Read**.
   Store: `echo '<token>' > ~/.pi/.secrets/bitbucket_token`
2. **App password** (HTTP Basic) — simplest. Personal settings → App passwords,
   scopes: `pullrequest:write`, `repository:read`.
   Store:
   ```bash
   echo '<bitbucket-username>' > ~/.pi/.secrets/bitbucket_username
   echo '<app-password>'       > ~/.pi/.secrets/bitbucket_app_password
   ```
   The username is the **Bitbucket username** (Personal settings → Account info), not the email.

Env overrides: `BITBUCKET_TOKEN`, or `BITBUCKET_USERNAME` + `BITBUCKET_APP_PASSWORD`.

Verify: `scripts/bb.sh auth-check <workspace> <repo_slug>`

## Workspace & repo slug

Derive from the git remote:
- `git@bitbucket.org:WS/SLUG.git` → workspace `WS`, slug `SLUG`
- `https://bitbucket.org/WS/SLUG(.git)` → same

## Script usage

```bash
scripts/bb.sh auth-check <workspace> <repo_slug>
scripts/bb.sh list <workspace> <repo_slug> [STATE] [LIMIT]    # STATE: MERGED|OPEN|DECLINED (default MERGED)
scripts/bb.sh view <workspace> <repo_slug> <pr_id>
scripts/bb.sh create <workspace> <repo_slug> \
  --title "..." --body-file /tmp/pr-body.md \
  --source <branch> --dest <base> \
  [--close-source-branch] [--reviewer <account-uuid>]...
scripts/bb.sh update <workspace> <repo_slug> <pr_id> [--title T] [--body-file F] [--reviewer UUID]...
scripts/bb.sh merge <workspace> <repo_slug> <pr_id> [merge_commit|squash|fast_forward]
```

- `create` prints `PR #<id>: <url>` on success, error JSON on failure (non-zero exit).
- If `create` fails with **409**, an open PR already exists for that source→destination — find it with `list ... OPEN`, then `view`/`update` it instead of creating a new one.
- `update` fetches the current PR, applies only the provided fields, and PUTs back.
- `merge` without a strategy uses the repo's default; 409 = conflict or checks not passed.
- Reviewers need **account UUIDs** (not usernames). Look up via
  `GET https://api.bitbucket.org/2.0/workspaces/<ws>/members` if the user insists;
  otherwise skip — reviewers can be added in the UI.
- `--close-source-branch` sets Bitbucket's "Close source branch after merge" flag.

## API error triage

| Symptom | Cause / fix |
|---|---|
| 401 | Wrong username with app password (must be Bitbucket username, not email); or expired token |
| 403 | Token/app password missing `pullrequest:write` scope |
| 404 on create | Source branch not pushed, or wrong workspace/slug |
| 409 | A PR already exists for that source→destination pair — find it with `list ... OPEN` |
| 429 | Rate limited — wait ~1 min and retry once |

Note: `GET /2.0/user` fails with workspace/repo access tokens (tokens have no user
identity) — that's why `auth-check` hits the repository endpoint instead.

## Out of scope

Bitbucket **Server / Data Center** uses a different API
(`/rest/api/1.0/projects/{key}/repos/{slug}/pull-requests`, personal access token
as Bearer). If the remote is not `bitbucket.org`, tell the user this skill covers
Cloud only.
