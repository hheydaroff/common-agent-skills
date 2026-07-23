#!/usr/bin/env bash
# integration-check.sh — detect and run the assembled feature's integration/e2e
# suite, then fall back to a build+boot+critical-path smoke test.
#
# Usage: ./integration-check.sh [critical_path_url]
#   critical_path_url  optional URL to curl for the smoke-test critical path
#                      (default: http://localhost:3000)
#
# Exit 0 = green, non-zero = something failed. Prints what it ran so the
# agent knows whether it got a real integration run or just a smoke test.
#
# NOT set -e: we want to run the smoke fallback even after a detection miss.

URL="${1:-http://localhost:3000}"
BOOT_TIMEOUT="${INTEGRATION_BOOT_TIMEOUT:-30}"

have() { command -v "$1" >/dev/null 2>&1; }

# --- 1. Prefer an existing integration/e2e test command --------------------
run_existing() {
  if [[ -f package.json ]] && have node; then
    for s in test:e2e test:integration e2e integration; do
      if node -e "process.exit(require('./package.json').scripts?.['$s']?0:1)" 2>/dev/null; then
        echo "▶ npm run $s"
        npm run "$s"
        return $?
      fi
    done
  fi
  if [[ -f pyproject.toml || -f pytest.ini || -f setup.cfg ]] && have pytest; then
    if pytest --collect-only -m integration -q >/dev/null 2>&1; then
      echo "▶ pytest -m integration"
      pytest -m integration
      return $?
    fi
  fi
  if [[ -d e2e || -d tests/integration || -d tests/e2e ]] && have npx; then
    if have playwright || npx --no-install playwright --version >/dev/null 2>&1; then
      echo "▶ npx playwright test"
      npx playwright test
      return $?
    fi
  fi
  return 127  # nothing found
}

run_existing
rc=$?
if [[ $rc -ne 127 ]]; then
  [[ $rc -eq 0 ]] && echo "✅ integration suite passed" || echo "❌ integration suite failed (rc=$rc)"
  exit $rc
fi

# --- 2. Smoke test fallback: build + boot + one critical path --------------
echo "ℹ no integration suite found — running smoke test (build + boot + critical path)"

# build / typecheck if a build step exists
if [[ -f package.json ]] && have node; then
  for s in build typecheck; do
    if node -e "process.exit(require('./package.json').scripts?.['$s']?0:1)" 2>/dev/null; then
      echo "▶ npm run $s"
      npm run "$s" || { echo "❌ smoke: '$s' failed"; exit 1; }
    fi
  done
elif [[ -f Cargo.toml ]] && have cargo; then
  echo "▶ cargo build"
  cargo build || { echo "❌ smoke: cargo build failed"; exit 1; }
fi

# boot the app in the background, if we can find a start command
BOOT_PID=""
start_cmd=""
if [[ -f package.json ]] && have node; then
  for s in dev start; do
    if node -e "process.exit(require('./package.json').scripts?.['$s']?0:1)" 2>/dev/null; then
      start_cmd="npm run $s"; break
    fi
  done
fi

if [[ -n "$start_cmd" ]]; then
  echo "▶ booting: $start_cmd"
  $start_cmd >/tmp/integration-boot.log 2>&1 &
  BOOT_PID=$!
  trap '[[ -n "$BOOT_PID" ]] && kill "$BOOT_PID" 2>/dev/null' EXIT

  # wait for the critical path to answer
  ok=false
  for ((t=0; t<BOOT_TIMEOUT; t++)); do
    if curl -fsS -o /dev/null "$URL" 2>/dev/null; then ok=true; break; fi
    sleep 1
  done
  if $ok; then
    echo "✅ smoke: app booted and $URL responded"
    exit 0
  else
    echo "❌ smoke: $URL did not respond within ${BOOT_TIMEOUT}s"
    tail -20 /tmp/integration-boot.log
    exit 1
  fi
else
  echo "⚠ smoke: no start command found and no integration suite — cannot verify composition automatically."
  echo "   Boot the app manually and hit its critical path, or add a test:e2e script."
  exit 2
fi
