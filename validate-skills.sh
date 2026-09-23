#!/usr/bin/env bash
# validate-skills.sh — validate every skills/*/SKILL.md before deploy.
#
# Catches the two most common skill-loading failures:
#   1. Invalid YAML frontmatter (unquoted description containing ':' etc.)
#   2. Duplicate / missing 'name', over-long or missing 'description'.
#
# Uses the same `yaml` parser pi uses (eemeli/yaml) when it can be found,
# so validation matches pi's actual loader. Falls back to a strict manual
# check otherwise.
#
# Usage: bash validate-skills.sh   (exits non-zero on any problem)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

# Locate a real `yaml` parser, so we validate exactly like pi does.
# Repo-local node_modules first (that's what CI installs), then pi's bundled copy
# on macOS (Homebrew) and Linux (~/.local/lib).
# The `|| true` guards against `find` exiting non-zero when some paths don't exist.
YAML_PKG="$(find \
  "$REPO_DIR/node_modules" \
  /opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent \
  /home/"$USER"/.local/lib/node_modules/@earendil-works/pi-coding-agent \
  ~/.pi/agent/npm \
  2>/dev/null -type d -path '*node_modules/yaml' | head -1 || true)"

# Fail closed when a real parser is required but missing. Without this the script
# silently drops to the naive regex fallback below, which by its own admission
# catches unquoted-colon frontmatter errors "poorly" — i.e. the exact bug class
# this check exists to catch. A green run that validated nothing is worse than a
# red one, so refuse instead of degrading.
if [ -z "$YAML_PKG" ] && [ "${REQUIRE_YAML_PKG:-0}" = "1" ]; then
  echo "ERROR: REQUIRE_YAML_PKG=1 but no 'yaml' parser was found." >&2
  echo "       Refusing to fall back to the naive parser — it misses unquoted-colon" >&2
  echo "       frontmatter errors, which is the whole point of this check." >&2
  echo "       Fix: npm install --no-save yaml   (creates $REPO_DIR/node_modules/yaml)" >&2
  exit 1
fi

node - "$SKILLS_DIR" "$YAML_PKG" <<'NODE'
const fs = require("fs");
const path = require("path");
const [, , skillsDir, yamlPkg] = process.argv;

let YAML = null;
if (yamlPkg) { try { YAML = require(yamlPkg); } catch {} }

function parseFrontmatter(text) {
  if (!text.startsWith("---")) throw new Error("missing frontmatter (no leading ---)");
  const end = text.indexOf("\n---", 3);
  if (end === -1) throw new Error("unterminated frontmatter (no closing ---)");
  const fm = text.slice(3, end);
  if (YAML) return YAML.parse(fm);
  // Fallback: naive key: value; will still catch unquoted-colon issues poorly,
  // so prefer having the yaml package available.
  const obj = {};
  for (const line of fm.split("\n")) {
    const m = line.match(/^([A-Za-z0-9_-]+):\s?(.*)$/);
    if (m) obj[m[1]] = m[2];
  }
  return obj;
}

const dirs = fs.readdirSync(skillsDir, { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name);

const errors = [];
const names = new Map(); // declared name -> [dirs]

for (const dir of dirs) {
  const file = path.join(skillsDir, dir, "SKILL.md");
  if (!fs.existsSync(file)) { errors.push(`${dir}: no SKILL.md`); continue; }
  let data;
  try {
    data = parseFrontmatter(fs.readFileSync(file, "utf8"));
  } catch (e) {
    errors.push(`${dir}: YAML frontmatter parse failed — ${e.message.split("\n")[0]}`);
    continue;
  }
  if (!data || typeof data !== "object") { errors.push(`${dir}: frontmatter not a mapping`); continue; }
  if (!data.name) errors.push(`${dir}: missing 'name'`);
  if (data.name && data.name !== dir) errors.push(`${dir}: name '${data.name}' != directory name`);
  if (!data.description) errors.push(`${dir}: missing 'description'`);
  else if (String(data.description).length > 1024)
    errors.push(`${dir}: description ${String(data.description).length} chars (>1024)`);
  if (data.name) {
    if (!names.has(data.name)) names.set(data.name, []);
    names.get(data.name).push(dir);
  }
}

for (const [name, where] of names) {
  if (where.length > 1) errors.push(`duplicate skill name '${name}' in: ${where.join(", ")}`);
}

if (errors.length) {
  console.error("\x1b[31m✗ skill validation failed:\x1b[0m");
  for (const e of errors) console.error("  - " + e);
  if (!YAML) console.error("  (note: bundled 'yaml' parser not found — install pi for exact validation)");
  process.exit(1);
}
console.log(`\x1b[32m✓\x1b[0m validated ${dirs.length} skills (frontmatter + names OK)`);
NODE
