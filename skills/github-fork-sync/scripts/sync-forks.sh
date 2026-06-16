#!/usr/bin/env bash
# Sync GitHub forks from their upstream parent's default branch.
#
# By default only forks that are strictly BEHIND (clean fast-forward, ahead==0)
# are synced. Diverged forks (you have local commits) are skipped unless --force.
#
# Usage:
#   sync-forks.sh                 # sync all clean-behind forks
#   sync-forks.sh --dry-run       # show what would be synced, change nothing
#   sync-forks.sh --include-diverged --force
#                                 # also hard-reset diverged forks (DESTRUCTIVE)
#   sync-forks.sh owner/repo ...  # only operate on the named forks
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

DRY=0; FORCE=0; INCLUDE_DIVERGED=0; TARGETS=()
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --force) FORCE=1 ;;
    --include-diverged) INCLUDE_DIVERGED=1 ;;
    -*) echo "unknown flag: $arg" >&2; exit 1 ;;
    *) TARGETS+=("$arg") ;;
  esac
done

in_targets() {
  [ "${#TARGETS[@]}" -eq 0 ] && return 0
  local x; for x in "${TARGETS[@]}"; do [ "$x" = "$1" ] && return 0; done
  return 1
}

synced=0; skipped=0; failed=0
while IFS=$'\t' read -r fork status behind ahead parent pbranch fbranch; do
  [ -z "$fork" ] && continue
  in_targets "$fork" || continue

  case "$status" in
    identical) echo "✓ up-to-date   $fork"; continue ;;
    ahead)     echo "↑ ahead only   $fork (you are $ahead ahead; nothing to pull)"; continue ;;
    unknown)   echo "? skip         $fork ($parent)"; skipped=$((skipped+1)); continue ;;
    diverged)
      if [ "$INCLUDE_DIVERGED" -eq 1 ] && [ "$FORCE" -eq 1 ]; then
        : # fall through to force-sync
      else
        echo "⚠ diverged     $fork (behind $behind, ahead $ahead) — skipped (needs --include-diverged --force)"
        skipped=$((skipped+1)); continue
      fi
      ;;
    behind) : ;;
    *) echo "? skip         $fork ($status)"; skipped=$((skipped+1)); continue ;;
  esac

  flags="--branch $fbranch"
  fmark=""
  if [ "$FORCE" -eq 1 ]; then flags="$flags --force"; fmark=" [force]"; fi

  if [ "$DRY" -eq 1 ]; then
    echo "→ would sync    $fork  (behind $behind, ahead $ahead)$fmark"
    continue
  fi

  err=$(gh repo sync "$fork" $flags 2>&1) && rc=0 || rc=$?
  if [ "$rc" -eq 0 ]; then
    echo "✓ synced       $fork (was behind $behind)"
    synced=$((synced+1))
  else
    case "$err" in
      *workflow\ scope*|*workflow\ changes*)
        echo "✗ scope        $fork — upstream changed CI workflows; run: gh auth refresh -s workflow" ;;
      *)
        echo "✗ FAILED       $fork — $(echo "$err" | head -1)" ;;
    esac
    failed=$((failed+1))
  fi
done < <(bash "$HERE/check-forks.sh" 2>/dev/null)

dmark=""
if [ "$DRY" -eq 1 ]; then dmark=" (dry-run)"; fi
echo "----"
echo "synced=$synced skipped=$skipped failed=$failed$dmark"
