#!/bin/bash
# Screenshot that cannot fail silently.
#   usage: bash shot.sh <out.png> [max-px=1700]
#   env:   SHOT_WRAP="sh tools/lanes/tmo 30"   optional prefix that bounds the peekaboo call
# Prints "<out.png> <W>x<H>" and exits 0 only when a non-empty image exists on disk.
# Exit 1 = capture failed after 3 tries (the reason is on stderr). Do not `read` the path unless this exits 0.
# Why: `peekaboo see ... >/dev/null 2>&1; echo ok` printed "ok" for captures that never wrote a file,
# and the next `read` of the path then failed with ENOENT (15 times in one session).
# Facts baked in (PowerPoint 16.114, macOS 27, Peekaboo 4.6.0): --mode screen is the only capture mode
# that works; --no-remote goes after the leaf command; the file can appear a moment after the command returns.
OUT=${1:?usage: shot.sh <out.png> [max-px]}
MAX=${2:-1700}
mkdir -p "$(dirname "$OUT")" || exit 1
rm -f "$OUT"
LAST=""
for TRY in 1 2 3; do
  # shellcheck disable=SC2086
  LAST=$($SHOT_WRAP peekaboo see --no-remote --capture-engine cg --mode screen --path "$OUT" 2>&1)
  for _ in 1 2 3 4 5; do
    [ -s "$OUT" ] && break 2
    sleep 0.4
  done
  sleep 1
done
if [ ! -s "$OUT" ]; then
  echo "shot.sh: no image at $OUT after 3 tries. Last peekaboo output:" >&2
  echo "$LAST" | tail -5 >&2
  exit 1
fi
sips -Z "$MAX" "$OUT" >/dev/null 2>&1
DIMS=$(sips -g pixelWidth -g pixelHeight "$OUT" 2>/dev/null | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{print w"x"h}')
case "$DIMS" in
  x|0x*|*x0) echo "shot.sh: $OUT is not a readable image" >&2; exit 1;;
esac
echo "$OUT $DIMS"
