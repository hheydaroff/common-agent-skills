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
  [--draft | --ready] [--close-source-branch] [--reviewer <account-uuid>]...
# draft is the DEFAULT; pass --ready only for a final (review-requested) PR
scripts/bb.sh update <workspace> <repo_slug> <pr_id> [--title T] [--body-file F] [--reviewer UUID]...
scripts/bb.sh draft  <workspace> <repo_slug> <pr_id>   # mark open PR as draft
scripts/bb.sh ready  <workspace> <repo_slug> <pr_id>   # publish a draft for review
scripts/bb.sh merge <workspace> <repo_slug> <pr_id> [merge_commit|squash|fast_forward]

# Review threads
scripts/bb.sh comments <workspace> <repo_slug> <pr_id>
scripts/bb.sh comment  <workspace> <repo_slug> <pr_id> (--body T | --body-file F) [--path P] [--from N] [--to N]
scripts/bb.sh reply    <workspace> <repo_slug> <pr_id> <comment_id> (--body T | --body-file F)
scripts/bb.sh resolve  <workspace> <repo_slug> <pr_id> <comment_id>
scripts/bb.sh reopen   <workspace> <repo_slug> <pr_id> <comment_id>
scripts/bb.sh delete   <workspace> <repo_slug> <pr_id> <comment_id>
```

### Review threads

`comments` prints one block per thread: `[id] OPEN|RESOLVED  <file:line|general>  author  date`,
then the text, then each reply as `+--[id] author date: text`. The `[id]` is what
`reply`/`resolve`/`reopen`/`delete` take — a reply id works too, both commands walk up
to the thread root first.

- `comment` starts a thread. With `--path` it is anchored to the PR diff:
  `--from N` = line in the **source** branch version, `--to N` = line in the **destination**
  version (added lines → `--from`, removed lines → `--to`). Without `--path` it is a
  general PR comment.
- `reply` inherits the thread's position; it takes no `--path`/`--from`/`--to`.
- `resolve` / `reopen` toggle the thread's resolution (409 if it is already in that state).
- `delete` blanks a comment. Bitbucket keeps it as a tombstone when it still anchors a
  live reply; `comments` hides tombstones that anchor nothing.
- Resolving threads does **not** clear a reviewer's "changes requested" state — only that
  reviewer re-approving does. Say so instead of implying the review is finished.

### Comment API gotchas (all verified against REST 2.0)

| Do | Not |
|---|---|
| Reply = `POST .../pullrequests/{id}/comments` with `{"parent":{"id":<root>}}` | `POST .../comments/{comment_id}` — not a route; returns 403 "This endpoint does not support token-based authentication" |
| Resolve = `POST .../comments/{id}/resolve` (reopen = `DELETE` same path) | `PUT .../comments/{id}` with `{"resolved":true}` — 400 `extra keys not allowed` |
| Read resolution from the comment's **`resolution`** object (absent/null = open) | a `resolved` boolean — the API never returns one |

Resolve works on general comments as well as inline ones. Workspace/project access tokens
can do all of the above.

- `create` prints `PR #<id> (DRAFT|ready for review): <url>` on success, error JSON on failure (non-zero exit). It sends `draft: true` unless `--ready` is given.
- If `create` fails with **409**, an open PR already exists for that source→destination — find it with `list ... OPEN`, then `view`/`update` it instead of creating a new one.
- `update` fetches the current PR, applies only the provided fields, and PUTs back.
- `draft`/`ready` send only `{"draft": <bool>}`; a `PUT` omitting a field leaves that field unchanged (verified: omitting `draft` does not clear it), so `update` never disturbs draft state. `view`/`list` print a `[DRAFT]` marker.
- `merge` without a strategy uses the repo's default; 409 = conflict or checks not passed.
- Reviewers need **account UUIDs** (not usernames). Look up via
  `GET https://api.bitbucket.org/2.0/workspaces/<ws>/members` if the user insists;
  otherwise skip — reviewers can be added in the UI.
- `--close-source-branch` sets Bitbucket's "Close source branch after merge" flag.

### Draft pull requests (verified against REST 2.0)

| Do | Not |
|---|---|
| Create with `"draft": true` in the POST body | a separate `/draft` create route — there is none |
| Toggle with `PUT .../pullrequests/{id}` and `{"draft": true}` / `{"draft": false}` | `PATCH` — Bitbucket takes `PUT` here |
| Read state from the PR object's **`draft`** boolean | inferring readiness from `state` (a draft is still `state: OPEN`) |

A `PUT` that omits `draft` preserves the stored value, so `update` (title/body/reviewers)
never silently publishes a draft. Unticking "Draft" in the UI is the same PUT.

Deleting a probe/test PR is **not** possible with a `pullrequest:write` token —
`DELETE .../pullrequests/{id}` returns 403. Use `POST .../pullrequests/{id}/decline`
instead (200), which leaves a DECLINED PR in the list; the UI delete button needs the
"admin" permission on the repo.

## API error triage

| Symptom | Cause / fix |
|---|---|
| 401 | Wrong username with app password (must be Bitbucket username, not email); or expired token |
| 403 | Token/app password missing `pullrequest:write` scope — or you tried `DELETE .../pullrequests/{id}` (repo-admin only; use `/decline` + UI delete) |
| 404 on create | Source branch not pushed, or wrong workspace/slug |
| 409 | A PR already exists for that source→destination pair — find it with `list ... OPEN`. On `resolve`/`reopen`: the thread is already in that state |
| 403 "does not support token-based authentication" | Wrong route (e.g. `POST .../comments/{id}` for a reply) — see the gotchas table above |
| 429 | Rate limited — wait ~1 min and retry once |

Note: `GET /2.0/user` fails with workspace/repo access tokens (tokens have no user
identity) — that's why `auth-check` hits the repository endpoint instead.

## Out of scope

Bitbucket **Server / Data Center** uses a different API
(`/rest/api/1.0/projects/{key}/repos/{slug}/pull-requests`, personal access token
as Bearer). If the remote is not `bitbucket.org`, tell the user this skill covers
Cloud only.
