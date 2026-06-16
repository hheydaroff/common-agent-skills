---
name: github-fork-sync
description: "Find every GitHub fork you own, detect which are behind their upstream parent, and fast-forward them. Use when the user says 'update my forks', 'sync my forks', 'which forks are behind', 'my forks are out of date', or wants to bulk-update GitHub forks from upstream."
---

# GitHub Fork Sync

Audit and update all forks owned by the authenticated GitHub user. Detects how
far each fork is behind/ahead of its upstream parent's default branch, then
fast-forwards the safe ones via `gh repo sync`.

## Prerequisites

- `gh` CLI installed and authenticated: `gh auth status` (needs `repo` scope).
- `jq` installed (used for JSON assembly).
- For forks whose **upstream changed CI workflow files**, syncing needs the
  `workflow` token scope. If you see "scope" errors, run once:
  ```bash
  gh auth refresh -s workflow
  ```

## Workflow

**1. Always check first.** Show the user what's behind before changing anything:
```bash
bash scripts/check-forks.sh
```
Prints an aligned table: fork, status, behind, ahead, parent. Status is one of
`behind` (clean fast-forward candidate), `diverged` (you have local commits),
`ahead`, `identical`, or `unknown` (no upstream / API error).

**2. Dry-run the sync** so the user sees exactly what will change:
```bash
bash scripts/sync-forks.sh --dry-run
```

**3. Sync.** By default only **clean-behind** forks are updated; diverged forks
(where you'd lose your own commits) are skipped:
```bash
bash scripts/sync-forks.sh
```

Operate on specific forks only by passing names:
```bash
bash scripts/sync-forks.sh owner/repo1 owner/repo2
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check-forks.sh` | List all forks + behind/ahead status. `--json` for machine output. TSV on stdout, table on stderr. |
| `scripts/sync-forks.sh` | Sync behind forks. Flags below. Reads `check-forks.sh` internally. |

`sync-forks.sh` flags:
- `--dry-run` — report only, change nothing.
- `--include-diverged --force` — **destructive**: hard-resets diverged forks to
  upstream, discarding your local commits. Both flags required together. Never
  use without explicit user confirmation.
- `owner/repo …` — restrict to named forks.

## Safety Rules

- **Never** use `--force` / `--include-diverged` unless the user explicitly
  confirms they want to discard their own commits on diverged forks.
- Diverged forks (`ahead > 0`) are skipped by default — surface them to the user
  so they can decide (open a PR upstream, rebase, or force-reset).
- Always run `check-forks.sh` (or `--dry-run`) and show the result before a real
  sync, especially when run unattended/scheduled.

## Gotchas (validated)

- **Parent name ≠ fork name.** Upstream may be renamed (e.g. your
  `awesome-python` → `vinta/awesome-python`, `awesome-chatgpt-prompts` →
  `f/prompts.chat`). Scripts read `parent.full_name` from the API, not the fork
  name.
- **Default branches can differ** between fork and parent (`main` vs `master`).
  The compare uses the parent's default branch as base and the fork's default
  branch as head; `gh repo sync` targets the fork's branch.
- **`workflow` scope.** `gh repo sync` refuses when upstream commits modify
  `.github/workflows/**` unless the token has the `workflow` scope. The script
  reports these as `✗ scope` rows with the exact fix command — they are not
  hard failures, just a one-time `gh auth refresh -s workflow`.
- **Rate limits.** Each fork costs ~2 API calls (repo detail + compare). Fine
  for dozens of forks; for hundreds, expect it to take a bit.

## Scheduling (optional)

To keep forks current automatically, schedule a daily check and report. Run the
check (not a blind force-sync) and let the user review diverged forks:
```bash
bash scripts/sync-forks.sh --dry-run
```
Wire this into a cron/scheduled task that messages the summary.
