---
name: pr-create
description: "Write and raise a pull request on GitHub or Bitbucket Cloud: detects the provider from the git remote, drafts a convention-aware title and body from the diff, gets user approval, then pushes and opens the PR via gh CLI or the Bitbucket REST API. Use when the user says 'create/open/raise a PR', 'pull request', 'submit this for review', 'open a PR against GitHub/Bitbucket'."
---

# PR Create

Write a good PR and open it on GitHub or Bitbucket Cloud.

**Remote side effects**: this pushes a branch and creates a PR. Always show the
drafted title + body and get explicit user confirmation before pushing or creating.

## Step 0 — Detect provider & prerequisites

```bash
git remote get-url origin
```

| Remote contains | Provider | Tooling |
|---|---|---|
| `github.com` | GitHub | `gh` CLI |
| `bitbucket.org` | Bitbucket Cloud | `scripts/bb.sh` — load [references/bitbucket.md](references/bitbucket.md) first |
| anything else | unsupported | tell the user and stop |

GitHub prerequisites:
- `gh --version` — if missing: install with `brew install gh` (or https://cli.github.com)
- `gh auth status` — if not authenticated: ask user to run `gh auth login`

## Step 1 — Branch & base

```bash
git branch --show-current
git fetch origin --quiet
git remote show origin | sed -n 's/.*HEAD branch: //p'   # base branch
```

- On the default branch (main/master)? Stop and ask the user for a feature branch.
- Nothing ahead of base (`git rev-list --count origin/<base>..HEAD` = 0)? Stop.
- Uncommitted changes (`git status --short`)? Ask: commit them into this PR, leave them out, or stash. Do not guess.
- Branch targets something other than the default branch (stacked branch)? Ask which base to use.

## Step 2 — Gather context

```bash
git log origin/<base>..HEAD --format='%h %s'
git diff --stat origin/<base>...HEAD
git diff origin/<base>...HEAD          # skim; read changed files selectively for big diffs
```

Convention checks:
- PR template: `.github/pull_request_template.md` — if present, its structure is the source of truth for the body.
- Recent merged PRs:
  - GitHub: `gh pr list --state merged --limit 5 --json title,body`
  - Bitbucket: `scripts/bb.sh list <workspace> <repo_slug> MERGED 5`

## Step 3 — Draft title & body

**Title**
- Imperative mood, ≤72 chars, no trailing period.
- Copy the repo's convention from merged PRs/commits (`feat: ...`, `[PROJ-123] ...`, plain) — don't invent prefixes the repo doesn't use.

**Body**
- Lead with *why*: the problem and the decisions a reviewer can't reconstruct from the diff (rejected alternatives, scope dropped, constraints). The diff already shows *what* — don't restate it.
- Include how it was tested (commands, CI evidence). Link issues: `Closes #N` / `Fixes #N`.
- Follow the repo PR template when present. Default to prose; add `##` sections only when length earns them.
- No AI/bot attribution trailers unless the user asks.

## Step 4 — Confirm with user

Show the full title + body. Ask for approval (or edits) and whether it should be a draft. Only proceed after explicit yes.

## Step 5 — Push & create

```bash
git push -u origin HEAD
```

Write the body to a temp file first (branch name in the filename to avoid collisions), then:

**GitHub:**
```bash
gh pr create --title "..." --body-file /tmp/pr-body-<branch>.md [--draft] [--base <base>]
```

**Bitbucket Cloud** (see [references/bitbucket.md](references/bitbucket.md)):
```bash
scripts/bb.sh create <workspace> <repo_slug> \
  --title "..." --body-file /tmp/pr-body-<branch>.md \
  --source <branch> --dest <base> [--close-source-branch]
```

Report the PR number and URL. If creation fails, show the error and stop — do not retry blindly.

## Reference Files

| File | When to load |
|------|--------------|
| [references/bitbucket.md](references/bitbucket.md) | Remote is bitbucket.org — auth setup, script usage, API errors |
