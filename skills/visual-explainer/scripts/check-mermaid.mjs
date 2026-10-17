#!/usr/bin/env node
// Parse every Mermaid block in .md/.html files against the PINNED Mermaid major (11) and lint
// style invariants that parse() misses. Exit 1 on any failure.
//   node scripts/check-mermaid.mjs docs/diagram.html references/foo.md
// Extracts: ```mermaid fences, <pre class="mermaid">, <script type="text/plain" class="diagram-source">.
// First run installs mermaid + jsdom into ~/.cache/visual-explainer/mmcheck (needs npm + network once).
// Limits: parse OK proves the keyword and grammar, NOT that the sample means what you intend
// (a malformed venn-beta line parsed OK once) and NOT that the render looks good: still screenshot it.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const MERMAID = process.env.MERMAID_VERSION || '11';
const dir = path.join(process.env.XDG_CACHE_HOME || path.join(os.homedir(), '.cache'), 'visual-explainer', 'mmcheck');
const files = process.argv.slice(2);
if (!files.length) { console.error('usage: check-mermaid.mjs <file.md|file.html>...'); process.exit(2); }

if (!fs.existsSync(path.join(dir, 'node_modules', 'mermaid'))) {
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'package.json'), '{"name":"mmcheck","private":true,"type":"module"}');
  execFileSync('npm', ['install', '--silent', `mermaid@${MERMAID}`, 'jsdom'], { cwd: dir, stdio: 'inherit' });
}
const req = createRequire(path.join(dir, 'x.js'));
const { JSDOM } = req('jsdom');
const dom = new JSDOM('<!doctype html><html><body></body></html>', { pretendToBeVisual: true });
for (const k of ['window', 'document', 'HTMLElement', 'SVGElement', 'Element', 'Node', 'getComputedStyle', 'requestAnimationFrame'])
  if (dom.window[k] !== undefined) try { globalThis[k] = dom.window[k]; } catch {}
try { Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true }); } catch {}
const mermaid = (await import(pathToFileURL(req.resolve('mermaid')).href)).default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

const decode = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const extract = text => [
  ...[...text.matchAll(/```mermaid\s*\n([\s\S]*?)```/g)].map(m => m[1]),
  ...[...text.matchAll(/<pre[^>]*class="[^"]*\bmermaid\b[^"]*"[^>]*>([\s\S]*?)<\/pre>/g)].map(m => decode(m[1])),
  ...[...text.matchAll(/<script[^>]*class="[^"]*diagram-source[^"]*"[^>]*>([\s\S]*?)<\/script>/g)].map(m => decode(m[1])),
].map(b => b.trim()).filter(Boolean);

// Style invariants parse() cannot see.
const lint = b => {
  const out = [];
  if (/\\n/.test(b)) out.push('literal "\\n" in a label: use <br/>');
  if (/^\s*radar\s*$/m.test(b)) out.push('bare "radar": the keyword is radar-beta');
  return out;
};

let total = 0, fails = 0;
for (const f of files) {
  const blocks = extract(fs.readFileSync(f, 'utf8'));
  console.log(`\n== ${f}: ${blocks.length} block(s)`);
  for (const b of blocks) {
    total++;
    const label = b.split('\n')[0].slice(0, 30);
    const problems = lint(b);
    try { await mermaid.parse(b); } catch (e) { problems.push('parse: ' + String(e?.message || e).replace(/\s+/g, ' ').slice(0, 140)); }
    if (problems.length) { fails++; console.log(`   FAIL  ${label}\n         ${problems.join('\n         ')}`); }
    else console.log(`   OK    ${label}`);
  }
}
console.log(`\n${total} block(s), ${fails} failure(s)`);
process.exit(fails ? 1 : 0);
