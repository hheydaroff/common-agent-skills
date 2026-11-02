#!/usr/bin/env node
// rayfin-lint.mjs - static checks for a Rayfin / Fabric app project. Node 18+, no dependencies.
// Usage: node rayfin-lint.mjs [dir=.] [--json]
// Finds every rayfin/rayfin.yml under dir (skips node_modules, .git, dist) and checks the mechanical traps
// listed in the fabric-app skill. Exit 1 if any ERROR. WARN = verify, may be intentional.
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { execFileSync } from "node:child_process";

const args = process.argv.slice(2);
const asJson = args.includes("--json");
const root = resolve(args.find(a => !a.startsWith("--")) ?? ".");
const findings = [];
const add = (level, file, msg) => findings.push({ level, file: relative(root, file) || ".", msg });
const read = p => { try { return readFileSync(p, "utf8"); } catch { return ""; } };
const SKIP = new Set(["node_modules", ".git", "dist", ".temp", ".next"]);

function find(dir, depth = 0, out = []) {
  if (depth > 6) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name)) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) find(p, depth + 1, out);
    else if (e.name === "rayfin.yml" && dir.endsWith("rayfin")) out.push(dir);
  }
  return out;
}

// services.<name>: block text (indent-aware, no YAML dependency)
function block(yml, name) {
  const m = yml.match(new RegExp(`^(\\s*)${name}:[^\\n]*\\n((?:\\1\\s+[^\\n]*\\n?|\\s*\\n)*)`, "m"));
  return m ? m[0] : "";
}
const enabled = b => /^\s*enabled:\s*true\b/m.test(b);

const RESERVED = new Set(["String", "Int", "Float", "Boolean", "ID", "Query", "Mutation", "Subscription"]);
const LIKELY = new Set(["Date", "DateTime", "Time", "Long", "Decimal", "Byte", "Short", "UUID", "Guid", "Any", "JSON"]);

function lintProject(rdir) {
  const yml = read(join(rdir, "rayfin.yml"));
  const proj = join(rdir, "..");
  const f = join(rdir, "rayfin.yml");
  const data = block(yml, "data"), hosting = block(yml, "staticHosting"), fns = block(yml, "functions"), auth = block(yml, "auth");

  if (enabled(data) && !/^\s*dialect:\s*\S+/m.test(data)) add("ERROR", f, "services.data enabled without dialect (use dialect: mssql)");
  if (enabled(fns) && !/type:\s*application\b/.test(fns)) add("ERROR", f, "services.functions enabled without auth.type: application");
  if (enabled(hosting) && !/assetAccess:/.test(hosting)) add("WARN", f, "staticHosting.assetAccess not set; non-interactive deploys record 'protected'. Choose it on purpose");
  if (enabled(hosting) && /assetAccess:\s*public/.test(hosting)) add("WARN", f, "assetAccess: public - nothing sensitive may be in the bundle; data must be gated server side");
  if (enabled(auth) && !/fabric:\s*\n\s+enabled:\s*true/.test(auth)) add("WARN", f, "auth.fabric.enabled is not true; deployed apps support Fabric SSO only");
  const conn = yml.split(/^connectors:\s*$/m)[1] ?? "";
  for (const c of conn.split(/\n\s*-\s+name:/).slice(1)) {
    if (/fabric-semanticmodel|kusto/.test(c) && /type:\s*application\b/.test(c)) add("WARN", f, "a Category B connector (semantic model/kusto) must use auth.type: delegated");
  }
  if (/\$\{[A-Z_]+\}/.test(yml)) add("WARN", f, "${VAR} without :-default is a hard error when unset");

  // entities
  const ddir = join(rdir, "data");
  if (existsSync(ddir)) {
    const schema = read(join(ddir, "schema.ts"));
    for (const name of readdirSync(ddir)) {
      if (!name.endsWith(".ts") || name === "schema.ts") continue;
      const p = join(ddir, name), src = read(p);
      const re = /export\s+class\s+(\w+)/g; let m, prev = 0;
      while ((m = re.exec(src))) {
        const head = src.slice(prev, m.index); prev = m.index + m[0].length;
        if (!/@entity\b/.test(head)) continue;
        const cls = m[1];
        if (!/@(authenticated|anonymous|role)\b/.test(head)) add("ERROR", p, `entity ${cls} has no permission decorator (omission is fail-open for signed-in users)`);
        if (schema && !new RegExp(`\\b${cls}\\b`).test(schema)) add("WARN", p, `entity ${cls} is not referenced in rayfin/data/schema.ts (unregistered = invisible)`);
        if (RESERVED.has(cls) || cls.startsWith("__")) add("ERROR", p, `entity name ${cls} is a reserved GraphQL name`);
        else if (LIKELY.has(cls)) add("WARN", p, `entity name ${cls} may be reserved; check rayfin-core docs 'Reserved entity names'`);
      }
      for (const t of src.matchAll(/@text\(([^)]*)\)/g)) if (!/\bmax\s*:/.test(t[1])) { add("WARN", p, "@text without max becomes NVARCHAR(MAX): GraphQL 'Internal server error' after a green deploy"); break; }
    }
  }

  // decorators config
  for (const ts of ["tsconfig.json", "../tsconfig.json", "../tsconfig.app.json"]) {
    if (/"experimentalDecorators"\s*:\s*true|"emitDecoratorMetadata"\s*:\s*true/.test(read(join(rdir, ts)))) add("ERROR", join(rdir, ts), "experimentalDecorators/emitDecoratorMetadata must stay off (TC39 decorators)");
  }

  // functions
  const fdir = join(rdir, "functions");
  if (existsSync(fdir)) {
    if (enabled(fns) && !existsSync(join(fdir, "host.json"))) add("ERROR", fdir, "host.json missing (scaffold .gitignore omits it; deploy refuses without it)");
    const lock = read(join(fdir, "package-lock.json"));
    const bad = [...lock.matchAll(/"resolved":\s*"(https?:\/\/[^"]+)"/g)].map(x => x[1]).find(u => !u.startsWith("https://registry.npmjs.org/"));
    if (bad) add("ERROR", join(fdir, "package-lock.json"), `lockfile resolves from ${new URL(bad).host}; CI runners cannot read a private feed`);
    const sdir = join(fdir, "src");
    if (existsSync(sdir)) for (const name of readdirSync(sdir)) {
      if (!name.endsWith(".ts") || /^(types|secrets\.generated)\.ts$/.test(name)) continue;
      const p = join(sdir, name), src = read(p);
      if (/from\s+['"]@microsoft\/rayfin-functions['"]/.test(src)) add("ERROR", p, "import RayfinContext from @microsoft/fabric-user-data-functions, not @microsoft/rayfin-functions");
      if (/\bctx\.(getSecret|getToken)\(/.test(src)) add("WARN", p, "ctx.getSecret/getToken are deprecated; use ctx.Secrets / ctx.Tokens");
      if (/process\.env\./.test(src)) add("WARN", p, "process.env in a function; use ctx.Secrets (declared in rayfin.yml secrets:)");
      if (/async\s*\(\s*ctx\s*[,)]/.test(src)) add("WARN", p, "ctx parameter is not annotated RayfinContext<...>; typegen and ctx.Secrets typing depend on it");
      if (/^import\s+\{[^}]*\}\s+from\s+['"][^'"]*\/data\//m.test(src)) add("WARN", p, "runtime import from data/ pulls decorator runtime into the functions bundle; use `import type`");
      if (/udf\.func\(/.test(src) && /throw\s+new\s+Error/.test(src) && !/\{\s*error\s*:/.test(src)) add("WARN", p, "handler throws; a thrown error reaches the browser as a bare 500. Return { error: '<step>: ...' }");
    }
  }

  // git hygiene
  const tracked = args2 => { try { return execFileSync("git", ["ls-files", ...args2], { cwd: proj, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim(); } catch { return ""; } };
  const t = tracked(["--", "rayfin/.env", "rayfin/.env.local", "rayfin/.deployments.json", ".env.local"]);
  if (t) add("ERROR", rdir, `tracked files that must be ignored: ${t.split("\n").join(", ")}`);
  let gi = ""; for (let d = proj, i = 0; i < 4; d = join(d, ".."), i++) gi += read(join(d, ".gitignore"));
  if (gi && !/\.deployments\.json/.test(gi)) add("WARN", join(proj, ".gitignore"), "does not ignore rayfin/.deployments.json");
  if (gi && !/rayfin\/\.env|\.env/.test(gi)) add("WARN", join(proj, ".gitignore"), "does not ignore rayfin/.env*");
}

if (!existsSync(root) || !statSync(root).isDirectory()) { console.error(`not a directory: ${root}`); process.exit(2); }
const projects = find(root);
if (!projects.length) { console.error(`no rayfin/rayfin.yml under ${root}`); process.exit(2); }
projects.forEach(lintProject);
const errors = findings.filter(x => x.level === "ERROR").length;
if (asJson) console.log(JSON.stringify({ projects: projects.map(p => relative(root, p) || "."), findings }, null, 2));
else {
  for (const x of findings) console.log(`${x.level.padEnd(5)} ${x.file}: ${x.msg}`);
  console.log(`${projects.length} project(s), ${errors} error(s), ${findings.length - errors} warning(s)`);
}
process.exit(errors ? 1 : 0);
