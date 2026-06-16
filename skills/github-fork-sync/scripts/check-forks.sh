#!/usr/bin/env bash
# List every GitHub fork owned by the authenticated user and how far it is
# behind / ahead of its upstream parent's default branch.
#
# Output: one TSV row per fork to stdout (and an aligned table to stderr).
#   fork<TAB>status<TAB>behind<TAB>ahead<TAB>parent<TAB>parent_branch<TAB>fork_branch
#
# status is one of: behind | diverged | ahead | identical | unknown
#
# Usage:
#   check-forks.sh              # all forks
#   check-forks.sh --json       # emit JSON array instead of TSV
set -euo pipefail

JSON=0
[ "${1:-}" = "--json" ] && JSON=1

command -v gh >/dev/null || { echo "gh CLI not found" >&2; exit 1; }
command -v jq >/dev/null || { echo "jq not found" >&2; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh not authenticated (run: gh auth login)" >&2; exit 1; }

ME=$(gh api user -q .login)

FORKS=$(gh api "user/repos?type=owner&per_page=100" --paginate \
  -q '.[] | select(.fork==true) | .full_name')

[ -z "$FORKS" ] && { echo "No forks found for $ME" >&2; exit 0; }

results=""
printf "%-48s %-10s %8s %8s  %s\n" "FORK" "STATUS" "BEHIND" "AHEAD" "PARENT" >&2

while IFS= read -r repo; do
  [ -z "$repo" ] && continue
  info=$(gh api "repos/$repo" \
    -q '[.parent.full_name, .parent.default_branch, .default_branch] | @tsv' 2>/dev/null) || info=""
  parent=$(printf '%s' "$info" | cut -f1)
  pdef=$(printf '%s' "$info" | cut -f2)
  fdef=$(printf '%s' "$info" | cut -f3)

  if [ -z "$parent" ] || [ "$parent" = "null" ]; then
    status="unknown"; behind=0; ahead=0; parent="(no upstream)"
  else
    powner=${parent%%/*}
    cmp=$(gh api "repos/$parent/compare/$powner:$pdef...$ME:$fdef" \
      -q '[.behind_by, .ahead_by, .status] | @tsv' 2>/dev/null) || cmp=""
    if [ -z "$cmp" ]; then
      status="unknown"; behind=0; ahead=0
    else
      behind=$(printf '%s' "$cmp" | cut -f1)
      ahead=$(printf '%s' "$cmp" | cut -f2)
      raw=$(printf '%s' "$cmp" | cut -f3)
      case "$raw" in
        behind) status="behind" ;;
        ahead) status="ahead" ;;
        identical) status="identical" ;;
        diverged) status="diverged" ;;
        *) status="$raw" ;;
      esac
    fi
  fi

  printf "%-48s %-10s %8s %8s  %s\n" "$repo" "$status" "$behind" "$ahead" "$parent" >&2
  if [ "$JSON" -eq 1 ]; then
    row=$(jq -nc --arg f "$repo" --arg s "$status" --argjson b "${behind:-0}" \
      --argjson a "${ahead:-0}" --arg p "$parent" --arg pb "${pdef:-}" --arg fb "${fdef:-}" \
      '{fork:$f,status:$s,behind:$b,ahead:$a,parent:$p,parent_branch:$pb,fork_branch:$fb}')
    results="${results}${row}
"
  else
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$repo" "$status" "$behind" "$ahead" "$parent" "${pdef:-}" "${fdef:-}"
  fi
done <<EOF
$FORKS
EOF

if [ "$JSON" -eq 1 ]; then
  printf '%s' "$results" | jq -s '.'
fi
