#!/usr/bin/env bash
# Bitbucket Cloud REST helper for the pr-create skill. Requires: curl, jq.
# Auth resolution: BITBUCKET_TOKEN env -> BITBUCKET_USERNAME+BITBUCKET_APP_PASSWORD env
#   -> ~/.pi/.secrets/bitbucket_token -> bitbucket_username+bitbucket_app_password files.
set -euo pipefail

API="https://api.bitbucket.org/2.0"
SECRETS="$HOME/.pi/.secrets"

die() { echo "ERROR: $*" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || die "jq is required (brew install jq)"

AUTH=()
setup_auth() {
  if [ -n "${BITBUCKET_TOKEN:-}" ]; then
    AUTH=(-H "Authorization: Bearer $BITBUCKET_TOKEN"); return
  fi
  local u="${BITBUCKET_USERNAME:-}" p="${BITBUCKET_APP_PASSWORD:-}"
  [ -z "$u" ] && [ -f "$SECRETS/bitbucket_username" ] && u=$(cat "$SECRETS/bitbucket_username")
  [ -z "$p" ] && [ -f "$SECRETS/bitbucket_app_password" ] && p=$(cat "$SECRETS/bitbucket_app_password")
  if [ -n "$u" ] && [ -n "$p" ]; then
    AUTH=(-u "$u:$p"); return
  fi
  if [ -f "$SECRETS/bitbucket_token" ]; then
    AUTH=(-H "Authorization: Bearer $(cat "$SECRETS/bitbucket_token")"); return
  fi
  die "no Bitbucket credentials. Set BITBUCKET_TOKEN or BITBUCKET_USERNAME+BITBUCKET_APP_PASSWORD (or files under $SECRETS). See references/bitbucket.md"
}

# request METHOD PATH [JSON_BODY] -> sets RESP_BODY, RESP_CODE
request() {
  local method="$1" path="$2" body="${3:-}"
  local args=(-s -w $'\n%{http_code}' -X "$method" -H "Accept: application/json")
  [ -n "$body" ] && args+=(-H "Content-Type: application/json" -d "$body")
  local out
  out=$(curl "${AUTH[@]}" "${args[@]}" "$API$path")
  RESP_CODE="${out##*$'\n'}"
  RESP_BODY="${out%$'\n'*}"
}

# parse_comment_flags [--body T | --body-file F | --path P | --from N | --to N]...
#   -> sets TEXT, INLINE_PATH, INLINE_FROM, INLINE_TO
parse_comment_flags() {
  TEXT=""; INLINE_PATH=""; INLINE_FROM=""; INLINE_TO=""; local bodyfile=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --body) TEXT="$2"; shift 2 ;;
      --body-file) bodyfile="$2"; shift 2 ;;
      --path) INLINE_PATH="$2"; shift 2 ;;
      --from) INLINE_FROM="$2"; shift 2 ;;
      --to) INLINE_TO="$2"; shift 2 ;;
      *) die "unknown flag: $1" ;;
    esac
  done
  if [ -n "$bodyfile" ]; then
    [ -f "$bodyfile" ] || die "body file not found: $bodyfile"
    TEXT=$(cat "$bodyfile")
  fi
  [ -n "$TEXT" ] || die "needs --body or --body-file"
}

# thread_root <comments_base_path> <comment_id> -> sets ROOT (the thread root,
# even when a child reply id was passed)
thread_root() {
  request GET "$1/$2"
  [ "$RESP_CODE" = "200" ] || die "no such comment $2 (HTTP $RESP_CODE): $RESP_BODY"
  ROOT=$(jq -r '.parent.id // .id' <<<"$RESP_BODY")
}

usage() {
  cat >&2 <<'EOF'
Usage:
  bb.sh auth-check <workspace> <repo_slug>
  bb.sh list <workspace> <repo_slug> [STATE] [LIMIT]
  bb.sh view <workspace> <repo_slug> <pr_id>
  bb.sh create <workspace> <repo_slug> --title T --body-file F --source S --dest D
               [--close-source-branch] [--reviewer UUID]...
  bb.sh update <workspace> <repo_slug> <pr_id> [--title T] [--body-file F] [--reviewer UUID]...
  bb.sh merge <workspace> <repo_slug> <pr_id> [merge_commit|squash|fast_forward]
  bb.sh comments <workspace> <repo_slug> <pr_id>
  bb.sh comment <workspace> <repo_slug> <pr_id> (--body T | --body-file F)
                [--path P] [--from N] [--to N]     # inline on the PR diff
  bb.sh reply <workspace> <repo_slug> <pr_id> <comment_id> (--body T | --body-file F)
  bb.sh resolve <workspace> <repo_slug> <pr_id> <comment_id>
  bb.sh reopen <workspace> <repo_slug> <pr_id> <comment_id>
  bb.sh delete <workspace> <repo_slug> <pr_id> <comment_id>
EOF
  exit 2
}

cmd="${1:-}"; shift || true
[ -n "$cmd" ] || usage
setup_auth

case "$cmd" in
  auth-check)
    [ $# -eq 2 ] || usage
    request GET "/repositories/$1/$2"
    if [ "$RESP_CODE" = "200" ]; then
      jq -r '"OK: repo \(.full_name), main branch: \(.mainbranch.name // "unknown")"' <<<"$RESP_BODY"
    else
      die "auth check failed (HTTP $RESP_CODE): $RESP_BODY"
    fi
    ;;

  list)
    [ $# -ge 2 ] || usage
    ws="$1"; slug="$2"; state="${3:-MERGED}"; limit="${4:-5}"
    request GET "/repositories/$ws/$slug/pullrequests?state=$state&pagelen=$limit"
    [ "$RESP_CODE" = "200" ] || die "list failed (HTTP $RESP_CODE): $RESP_BODY"
    jq -r '.values[] | "#\(.id) \(.title)\n  by \(.author.display_name) | dest \(.destination.branch.name)\n\((.description // "") | .[0:300])\n"' <<<"$RESP_BODY"
    ;;

  create)
    [ $# -ge 2 ] || usage
    ws="$1"; slug="$2"; shift 2
    title=""; bodyfile=""; source=""; dest=""; close=false; reviewers=()
    while [ $# -gt 0 ]; do
      case "$1" in
        --title) title="$2"; shift 2 ;;
        --body-file) bodyfile="$2"; shift 2 ;;
        --source) source="$2"; shift 2 ;;
        --dest) dest="$2"; shift 2 ;;
        --close-source-branch) close=true; shift ;;
        --reviewer) reviewers+=("$2"); shift 2 ;;
        *) die "unknown flag: $1" ;;
      esac
    done
    [ -n "$title" ] && [ -n "$bodyfile" ] && [ -n "$source" ] && [ -n "$dest" ] || usage
    [ -f "$bodyfile" ] || die "body file not found: $bodyfile"
    json=$(jq -n --arg title "$title" \
                 --rawfile desc "$bodyfile" \
                 --arg src "$source" --arg dst "$dest" \
                 --argjson close "$close" \
                 --argjson reviewers "$(printf '%s\n' "${reviewers[@]:-}" | jq -R 'select(length>0) | {uuid: .}' | jq -s .)" \
           '{title:$title, description:$desc, close_source_branch:$close,
             source:{branch:{name:$src}}, destination:{branch:{name:$dst}}, reviewers:$reviewers}')
    request POST "/repositories/$ws/$slug/pullrequests" "$json"
    case "$RESP_CODE" in
      200|201) jq -r '"PR #\(.id): \(.links.html.href)"' <<<"$RESP_BODY" ;;
      *) die "PR creation failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  view)
    [ $# -eq 3 ] || usage
    request GET "/repositories/$1/$2/pullrequests/$3"
    [ "$RESP_CODE" = "200" ] || die "view failed (HTTP $RESP_CODE): $RESP_BODY"
    jq -r '"PR #\(.id) [\(.state)] \(.title)\n  \(.source.branch.name) -> \(.destination.branch.name), by \(.author.display_name)\n  \(.links.html.href)\n\n\(.description // "(no description)")"' <<<"$RESP_BODY"
    ;;

  update)
    [ $# -ge 3 ] || usage
    ws="$1"; slug="$2"; prid="$3"; shift 3
    title=""; bodyfile=""; reviewers=()
    while [ $# -gt 0 ]; do
      case "$1" in
        --title) title="$2"; shift 2 ;;
        --body-file) bodyfile="$2"; shift 2 ;;
        --reviewer) reviewers+=("$2"); shift 2 ;;
        *) die "unknown flag: $1" ;;
      esac
    done
    request GET "/repositories/$ws/$slug/pullrequests/$prid"
    [ "$RESP_CODE" = "200" ] || die "fetch current PR failed (HTTP $RESP_CODE): $RESP_BODY"
    cur="$RESP_BODY"
    desc=""; hasdesc=false
    [ -n "$bodyfile" ] && { [ -f "$bodyfile" ] || die "body file not found: $bodyfile"; desc=$(cat "$bodyfile"); hasdesc=true; }
    hasrev=false; [ ${#reviewers[@]} -gt 0 ] && hasrev=true
    json=$(jq --arg title "$title" --arg desc "$desc" --argjson hasdesc "$hasdesc" \
             --argjson hasrev "$hasrev" \
             --argjson newrev "$(printf '%s\n' "${reviewers[@]:-}" | jq -R 'select(length>0) | {uuid: .}' | jq -s .)" \
        '{title, description, source, destination, close_source_branch}
         + (if has("reason") then {reason} else {} end)
         + {reviewers: ((.reviewers // []) | map({uuid}))}
         | if $title != "" then .title = $title else . end
         | if $hasdesc then .description = $desc else . end
         | if $hasrev then .reviewers = $newrev else . end' <<<"$cur")
    request PUT "/repositories/$ws/$slug/pullrequests/$prid" "$json"
    case "$RESP_CODE" in
      200) jq -r '"Updated PR #\(.id): \(.links.html.href)"' <<<"$RESP_BODY" ;;
      *) die "PR update failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  merge)
    [ $# -ge 3 ] || usage
    ws="$1"; slug="$2"; prid="$3"; strategy="${4:-}"
    body="{}"
    [ -n "$strategy" ] && body=$(jq -n --arg s "$strategy" '{merge_strategy: $s}')
    request POST "/repositories/$ws/$slug/pullrequests/$prid/merge" "$body"
    case "$RESP_CODE" in
      200) jq -r '"Merged PR #\(.id): \(.links.html.href)"' <<<"$RESP_BODY" ;;
      409) die "merge conflict or PR not ready (HTTP 409): $RESP_BODY" ;;
      *) die "merge failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  comments)
    [ $# -eq 3 ] || usage
    ws="$1"; slug="$2"; prid="$3"
    all="[]"; url="/repositories/$ws/$slug/pullrequests/$prid/comments?pagelen=100"
    while [ -n "$url" ]; do
      request GET "$url"
      [ "$RESP_CODE" = "200" ] || die "comments failed (HTTP $RESP_CODE): $RESP_BODY"
      all=$(jq -c --argjson new "$(jq -c '.values // []' <<<"$RESP_BODY")" '. + $new' <<<"$all")
      url=$(jq -r '.next // ""' <<<"$RESP_BODY"); url="${url#"$API"}"
    done
    jq -r '
      def loc: if .inline then "\(.inline.path):\([.inline.from, .inline.to] | map(select(. != null)) | unique | join("-"))" else "general" end;
      def when: ((.created_on // "")[0:10]);
      def txt: ((.content.raw // "") | if . == "" then "(deleted)" else . end);
      # Deleted comments stay in the API as blanked tombstones; drop them unless they
      # still anchor a live reply (Bitbucket keeps such roots on purpose).
      . as $all0
      | ($all0 | map(select(.deleted != true))) as $live
      | ([ $live[] | select(has("parent") | not) | .id ]
         + [ $live[] | select(has("parent")) | .parent.id ] | unique) as $rootids
      | "PR comments: \($rootids | length) threads (\($live | length) comments)\n",
        ( $rootids[] as $rid
        | ($all0 | map(select(.id == $rid)) | .[0]) as $r
        | "\n[\($r.id)] \(if $r.resolution != null then "RESOLVED" else "OPEN" end)  \($r | loc)  \($r.user.display_name // "?")  \($r | when)\n  \(($r | txt) | gsub("\n"; "\n  "))",
          ( $live | map(select((.parent.id? // null) == $rid)) | sort_by(.created_on) | .[]
          | "  +--[\(.id)] \(.user.display_name // "?") \(. | when): \((. | txt) | gsub("\n"; "\n       "))" ) )
      ' <<<"$all"
    ;;

  comment|reply)
    [ $# -ge 3 ] || usage
    [ "$cmd" = "comment" ] || [ $# -ge 4 ] || usage
    ws="$1"; slug="$2"; prid="$3"; shift 3
    cid=""
    if [ "$cmd" = "reply" ]; then
      cid="$1"; shift
      case "$cid" in --*) die "reply needs a numeric <comment_id>, got: $cid" ;; esac
    fi
    parse_comment_flags "$@"
    base="/repositories/$ws/$slug/pullrequests/$prid/comments"
    if [ -n "$cid" ]; then
      if [ -n "$INLINE_PATH$INLINE_FROM$INLINE_TO" ]; then
        die "a reply inherits the thread position; --path/--from/--to only apply to a new comment"
      fi
      thread_root "$base" "$cid"; cid="$ROOT"
    fi
    request POST "$base" \
      "$(jq -n --arg t "$TEXT" --arg cid "$cid" \
             --arg p "$INLINE_PATH" --arg f "$INLINE_FROM" --arg o "$INLINE_TO" '
         {content:{raw:$t}}
         + (if $cid != "" then {parent:{id:($cid|tonumber)}} else {} end)
         + (if $p != "" then {inline: ({path:$p}
              + (if $f != "" then {from:($f|tonumber)} else {} end)
              + (if $o != "" then {to:($o|tonumber)} else {} end))} else {} end)')"
    case "$RESP_CODE" in
      200|201)
        if [ -n "$cid" ]; then jq -r --arg cid "$cid" '"Replied [\(.id)] in thread \($cid)"' <<<"$RESP_BODY"
        else jq -r --arg prid "$prid" '"Comment [\(.id)] on PR #\($prid)"' <<<"$RESP_BODY"; fi ;;
      *) die "$cmd failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  resolve)
    [ $# -eq 4 ] || usage
    ws="$1"; slug="$2"; prid="$3"; cid="$4"
    base="/repositories/$ws/$slug/pullrequests/$prid/comments"
    thread_root "$base" "$cid"
    # Response is a comment_resolution object, not the comment.
    request POST "$base/$ROOT/resolve"
    case "$RESP_CODE" in
      200|201|204) echo "Resolved thread [$ROOT]" ;;
      409) die "thread [$ROOT] is already resolved" ;;
      *) die "resolve failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  reopen)
    [ $# -eq 4 ] || usage
    ws="$1"; slug="$2"; prid="$3"; cid="$4"
    base="/repositories/$ws/$slug/pullrequests/$prid/comments"
    thread_root "$base" "$cid"
    request DELETE "$base/$ROOT/resolve"
    case "$RESP_CODE" in
      200|204) echo "Reopened thread [$ROOT]" ;;
      409) die "thread [$ROOT] is not resolved" ;;
      *) die "reopen failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  delete)
    [ $# -eq 4 ] || usage
    request DELETE "/repositories/$1/$2/pullrequests/$3/comments/$4"
    case "$RESP_CODE" in
      204|200) echo "Deleted comment [$4]" ;;
      *) die "delete failed (HTTP $RESP_CODE): $RESP_BODY" ;;
    esac
    ;;

  *) usage ;;
esac
