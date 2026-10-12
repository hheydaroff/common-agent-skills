#!/usr/bin/env bash
# Fetch (or reuse) the pinned anatomy kit used by references/isometric-anatomy.md.
# Prints ANATOMY=<cache dir>; import the kit from $ANATOMY/kit and $ANATOMY/scripts.
set -euo pipefail

SHA="be2fa9b47a7e4b05dec468be9ffc42e830c2101c"   # wheresryan22/anatomy v1.1.0 (MIT)
URL="https://github.com/wheresryan22/anatomy.git"
CACHE="${ANATOMY_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/visual-explainer/anatomy-$SHA}"

STATUS=fetched
if [ -d "$CACHE/kit" ] && [ "$(git -C "$CACHE" rev-parse HEAD 2>/dev/null || true)" = "$SHA" ]; then
  STATUS=cached
else
  mkdir -p "$CACHE"
  git -C "$CACHE" init -q
  git -C "$CACHE" fetch -q --depth 1 "$URL" "$SHA"
  git -C "$CACHE" checkout -q --detach FETCH_HEAD
fi
# Line 1 is machine-readable: ANATOMY=<path> (no suffix).
echo "ANATOMY=$CACHE"
echo "status: $STATUS · kit: $CACHE/kit · scripts: $CACHE/scripts · deep docs: $CACHE/references · examples: $CACHE/examples"
