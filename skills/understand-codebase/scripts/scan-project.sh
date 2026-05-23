#!/usr/bin/env bash
# Scan a project directory and output a JSON manifest of files, languages, and frameworks.
# Usage: bash scan-project.sh <project-root>

set -euo pipefail

PROJECT_ROOT="${1:-.}"
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"

# Use git ls-files if in a repo, otherwise find
if git -C "$PROJECT_ROOT" rev-parse --is-inside-work-tree &>/dev/null; then
  FILES=$(git -C "$PROJECT_ROOT" ls-files --cached --others --exclude-standard 2>/dev/null)
else
  FILES=$(find "$PROJECT_ROOT" -type f \
    -not -path '*/.git/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/vendor/*' \
    -not -path '*/.venv/*' \
    -not -path '*/venv/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/dist/*' \
    -not -path '*/build/*' \
    -not -path '*/target/*' \
    -not -path '*/.next/*' \
    -not -path '*/coverage/*' \
    | sed "s|^$PROJECT_ROOT/||")
fi

# Filter out binary/irrelevant files
FILES=$(echo "$FILES" | grep -v -E '\.(png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot|mp3|mp4|pdf|zip|tar|gz|lock|min\.js|min\.css|map)$' \
  | grep -v -E '^(package-lock\.json|yarn\.lock|pnpm-lock\.yaml)$' \
  | grep -v -E '\.(DS_Store|gitkeep)$' \
  | sort)

TOTAL=$(echo "$FILES" | grep -c . || echo 0)

# Detect languages from extensions
LANGUAGES=""
detect_lang() {
  local ext="$1" lang=""
  case "$ext" in
    ts|tsx) lang="TypeScript" ;;
    js|jsx|mjs|cjs) lang="JavaScript" ;;
    py) lang="Python" ;;
    go) lang="Go" ;;
    rs) lang="Rust" ;;
    java) lang="Java" ;;
    kt) lang="Kotlin" ;;
    rb) lang="Ruby" ;;
    php) lang="PHP" ;;
    cs) lang="C#" ;;
    cpp|cc|cxx) lang="C++" ;;
    c|h) lang="C" ;;
    swift) lang="Swift" ;;
    scala) lang="Scala" ;;
    vue) lang="Vue" ;;
    svelte) lang="Svelte" ;;
    sql) lang="SQL" ;;
    tf|hcl) lang="Terraform" ;;
  esac
  if [ -n "$lang" ] && [[ ! "$LANGUAGES" == *"$lang"* ]]; then
    LANGUAGES="${LANGUAGES:+$LANGUAGES, }$lang"
  fi
}

while IFS= read -r file; do
  [ -z "$file" ] && continue
  ext="${file##*.}"
  detect_lang "$ext"
done <<< "$FILES"

# Detect frameworks from manifest files
FRAMEWORKS=""
if [ -f "$PROJECT_ROOT/package.json" ]; then
  deps=$(cat "$PROJECT_ROOT/package.json" 2>/dev/null || true)
  [[ "$deps" == *"\"next\""* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Next.js"
  [[ "$deps" == *"\"react\""* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }React"
  [[ "$deps" == *"\"vue\""* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Vue"
  [[ "$deps" == *"\"svelte\""* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Svelte"
  [[ "$deps" == *"\"express\""* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Express"
  [[ "$deps" == *"\"fastify\""* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Fastify"
  [[ "$deps" == *"\"@nestjs"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }NestJS"
  [[ "$deps" == *"\"angular"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Angular"
fi
if [ -f "$PROJECT_ROOT/pyproject.toml" ] || [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  pydeps=$(cat "$PROJECT_ROOT/pyproject.toml" "$PROJECT_ROOT/requirements.txt" 2>/dev/null || true)
  [[ "$pydeps" == *"django"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Django"
  [[ "$pydeps" == *"fastapi"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }FastAPI"
  [[ "$pydeps" == *"flask"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Flask"
fi
if [ -f "$PROJECT_ROOT/go.mod" ]; then
  gomod=$(cat "$PROJECT_ROOT/go.mod" 2>/dev/null || true)
  [[ "$gomod" == *"gin-gonic"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Gin"
  [[ "$gomod" == *"fiber"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Fiber"
fi
if [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
  cargo=$(cat "$PROJECT_ROOT/Cargo.toml" 2>/dev/null || true)
  [[ "$cargo" == *"actix"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Actix"
  [[ "$cargo" == *"axum"* ]] && FRAMEWORKS="${FRAMEWORKS:+$FRAMEWORKS, }Axum"
fi

# Get project name
PROJECT_NAME=$(basename "$PROJECT_ROOT")
if [ -f "$PROJECT_ROOT/package.json" ]; then
  pname=$(python3 -c "import json; print(json.load(open('$PROJECT_ROOT/package.json')).get('name',''))" 2>/dev/null || true)
  [ -n "$pname" ] && PROJECT_NAME="$pname"
fi

# Get git commit
GIT_HASH=$(git -C "$PROJECT_ROOT" rev-parse HEAD 2>/dev/null || echo "none")

# Format languages/frameworks as JSON arrays
fmt_array() {
  local input="$1"
  if [ -z "$input" ]; then echo "[]"; return; fi
  echo "$input" | awk -F', ' '{printf "["; for(i=1;i<=NF;i++){printf "\"%s\"", $i; if(i<NF) printf ", "} printf "]"}'
}

LANG_JSON=$(fmt_array "$LANGUAGES")
FW_JSON=$(fmt_array "$FRAMEWORKS")

# Output JSON
cat <<EOF
{
  "projectName": "$PROJECT_NAME",
  "projectRoot": "$PROJECT_ROOT",
  "gitCommitHash": "$GIT_HASH",
  "totalFiles": $TOTAL,
  "languages": $LANG_JSON,
  "frameworks": $FW_JSON,
  "files": [
EOF

FIRST=true
while IFS= read -r file; do
  [ -z "$file" ] && continue
  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    printf ',\n'
  fi
  # Get line count
  if [ -f "$PROJECT_ROOT/$file" ]; then
    lines=$(wc -l < "$PROJECT_ROOT/$file" 2>/dev/null | tr -d ' ')
  else
    lines=0
  fi
  printf '    {"path": "%s", "lines": %s}' "$file" "${lines:-0}"
done <<< "$FILES"

cat <<EOF

  ]
}
EOF
