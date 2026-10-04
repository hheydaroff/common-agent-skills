#!/usr/bin/env python3
"""retro.py - deterministic pre-pass over pi session logs (stdlib only, no LLM).

  retro.py digest  [sel]            repo health + per-session signals + cross-session aggregate + previous-retro deltas
  retro.py excerpt SESSION [--kinds user,corrections,errors,blocks,nav,final] [--max 15]
  retro.py outcome [sel] [--window 3d]   what happened to edited files after each session (git)
sel: --cwd P (default $PWD) --last N (10) --since 7d|YYYY-MM-DD --worktrees --no-subdirs
     --all-projects --session ID[,ID] --include-current
Everything printed is secret-redacted.
"""
import argparse, collections, glob, hashlib, json, os, re, statistics, subprocess, sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.expanduser("~/.pi/agent/sessions")
NAV_RE = re.compile(r'(^|[;&|(]\s*)(rg|grep|egrep|find|ls|tree|fd|cat|head|tail|wc|git\s+ls-files|git\s+grep)\b')
SEARCH_RE = re.compile(r'(^|[;&|(]\s*)(rg|grep|egrep|find|fd|git\s+grep)\b')
TEST_RE = re.compile(r'\b(pytest|vitest|jest|mocha|go test|cargo test|npm (run )?test|pnpm (run )?test|yarn test|bun test|make test|unittest|playwright test)\b')
CHECK_RE = re.compile(r'\b(tsc|eslint|ruff|mypy|pyright|npm run (lint|typecheck|build)|pnpm (run )?(lint|typecheck|build)|cargo (check|clippy|build)|go (build|vet)|validate[-_a-z]*\.sh|bash -n|shellcheck)\b')
CODE_EXT = {'.py', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.go', '.rs', '.java', '.kt', '.rb', '.sh', '.sql', '.swift', '.c', '.cpp', '.cs', '.php'}
DOC_RE = re.compile(r'(?i)(^|/)(PRD|SPEC|AGENTS|CLAUDE|CONTEXT|README|ADR)[^/]*\.md$|(^|/)docs/')
SPEC_RE = re.compile(r'(?i)(^|/)(PRD|SPEC)[^/]*\.md$')
CORR_RE = re.compile(r"(?i)(\bno[,.!]|\bnope\b|\bwrong\b|not what i|that'?s not|\bi (said|told|asked|meant)\b|\bagain\b|\bstop\b|\bdon'?t\b|\bdo not\b|\binstead\b|\brevert\b|\bundo\b|why did you|you (forgot|missed|didn'?t|broke)|\bstill (not|broken|fail))")
GIT_COMMIT_RE = re.compile(r'\bgit\s+commit\b')
GIT_PUSH_RE = re.compile(r'\bgit\s+push\b')
SECRET_RES = [
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(-----END [A-Z ]*PRIVATE KEY-----|$)', re.S), '[REDACTED-KEY]'),
    (re.compile(r'\b(AKIA|ASIA)[A-Z0-9]{16}\b'), '[REDACTED-AWS]'),
    (re.compile(r'\b(sk|pk|rk)-[A-Za-z0-9_\-]{16,}\b'), '[REDACTED-KEY]'),
    (re.compile(r'\b(ghp|gho|ghs|github_pat|glpat|xox[baprs]|hf|tvly|npm)[_-][A-Za-z0-9_\-]{16,}'), '[REDACTED-TOKEN]'),
    (re.compile(r'(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}'), 'Bearer [REDACTED]'),
    (re.compile(r'\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{5,}'), '[REDACTED-JWT]'),
    (re.compile(r'(?i)\b([A-Z0-9_]*(secret|token|passw(or)?d|api[_-]?key|credential|private[_-]?key)[A-Z0-9_]*)\s*[=:]\s*["\']?[^\s"\']{6,}'), r'\1=[REDACTED]'),
    (re.compile(r'\b(?=[A-Za-z0-9+=_]*\d)(?=[A-Za-z0-9+=_]*[A-Za-z])[A-Za-z0-9+=_]{40,}\b'), '[REDACTED-LONG]'),
]


def redact(s, n=None):
    s = s if isinstance(s, str) else str(s)
    for rx, rep in SECRET_RES:
        s = rx.sub(rep, s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:n] + '…' if n and len(s) > n else s


def text_of(content):
    if isinstance(content, str):
        return content
    return ''.join(b.get('text', '') for b in content or [] if isinstance(b, dict) and b.get('type') == 'text')


def headtail(t, h=600, tl=300):
    return t if len(t) <= h + tl else t[:h] + ' … ' + t[-tl:]


# ---------- selection ----------
def header(path):
    try:
        with open(path) as f:
            d = json.loads(f.readline())
        return d if d.get('type') == 'session' else None
    except Exception:
        return None


def parse_since(s):
    if not s:
        return None
    m = re.fullmatch(r'(\d+)([dhw])', s)
    if m:
        return datetime.now(timezone.utc) - timedelta(**{{'d': 'days', 'h': 'hours', 'w': 'weeks'}[m[2]]: int(m[1])})
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def select(a):
    cwd = os.path.realpath(a.cwd)
    base = os.path.basename(cwd)
    prefix = '--' + cwd.strip('/').replace('/', '-')
    since = parse_since(a.since)
    want = set(filter(None, (a.session or '').split(',')))
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, '*'))):
        dn = os.path.basename(d)
        scoped = not a.all_projects and not want
        if scoped and not (dn.startswith(prefix) or (a.worktrees and f'.herdr-worktrees-{base}' in dn)):
            continue  # cheap dir-name prefilter; header cwd verified below
        for f in glob.glob(os.path.join(d, '*.jsonl')):
            if want and not any(w in os.path.basename(f) for w in want):
                continue
            h = header(f)
            if not h:
                continue
            c = os.path.realpath(h.get('cwd', ''))
            if scoped:
                ok = c == cwd or (not a.no_subdirs and c.startswith(cwd + '/'))
                if a.worktrees and re.search(r'/\.herdr/worktrees/' + re.escape(base) + r'(-|/)', c + '/'):
                    ok = True
                if not ok:
                    continue
            ts = datetime.fromisoformat(h['timestamp'].replace('Z', '+00:00'))
            if since and ts < since:
                continue
            # the session running /retro is still being written: skip unless asked
            if not a.include_current and not want and datetime.now().timestamp() - os.path.getmtime(f) < 120:
                continue
            out.append((ts, f, c))
    out.sort()
    return out if want else out[-a.last:]


# ---------- parsing ----------
def events(path):
    """yield simplified events: (kind, ts, data)"""
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t, ts = d.get('type'), d.get('timestamp')
            if t == 'compaction':
                yield 'compaction', ts, {}
            elif t == 'model_change':
                yield 'model', ts, {'m': d.get('modelId')}
            elif t == 'message':
                m = d.get('message') or {}
                r = m.get('role')
                if r == 'user':
                    yield 'user', ts, {'text': text_of(m.get('content')), 'id': d.get('id')}
                elif r == 'assistant':
                    yield 'assistant', ts, {'usage': m.get('usage') or {}, 'model': m.get('model'), 'stop': m.get('stopReason'), 'text': text_of(m.get('content'))}
                    for b in m.get('content') or []:
                        if isinstance(b, dict) and b.get('type') == 'toolCall':
                            yield 'call', ts, {'id': b.get('id'), 'name': b.get('name'), 'args': b.get('arguments') or {}}
                elif r == 'toolResult':
                    yield 'result', ts, {'id': m.get('toolCallId'), 'name': m.get('toolName'), 'err': bool(m.get('isError')), 'text': headtail(text_of(m.get('content')))}


def cmd_of(call):
    return call['args'].get('command', '') if call['name'] == 'bash' else ''


def is_nav(c):
    return c['name'] in ('read', 'ffgrep', 'fffind', 'ls') or (c['name'] == 'bash' and NAV_RE.search(cmd_of(c)))


def is_search(c):
    return c['name'] in ('ffgrep', 'fffind') or (c['name'] == 'bash' and SEARCH_RE.search(cmd_of(c)))


def analyze(path, cwd):
    s = collections.defaultdict(int)
    calls, tools = {}, collections.Counter()
    reads, edits = collections.Counter(), collections.Counter()
    missing, blocks, skills = collections.Counter(), collections.Counter(), set()
    prompts, corr, models, bashcmds = [], [], set(), collections.Counter()
    first_ts = last_ts = None
    first_edit = None
    n_calls = nav_before = nav_total = test_runs = check_runs = code_edits = 0
    test_after_edit = check_after_edit = False
    prev_sig = None
    prev_err = False
    tok = collections.Counter()
    cost = 0.0
    docs_touched, spec_read_early = set(), False
    edited_files = []
    last_asst = ''
    last_user = ''
    for kind, ts, d in events(path):
        first_ts = first_ts or ts
        last_ts = ts or last_ts
        if kind == 'model':
            models.add(d['m'])
        elif kind == 'compaction':
            s['compactions'] += 1
        elif kind == 'user':
            t = d['text'].strip()
            if not t:
                continue
            s['user_msgs'] += 1
            if t == last_user:
                s['repeated_prompts'] += 1  # same message sent twice: input lost / agent stalled
            last_user = t
            if len(prompts) < 8:
                prompts.append(redact(t, 140))
            mm = re.match(r'/([a-z0-9][a-z0-9\-]+)', t) or re.match(r'<skill name="([^"]+)"', t)
            if mm:
                skills.add(mm[1])
            if s['user_msgs'] > 1 and CORR_RE.search(t[:400]):
                s['corrections'] += 1
                if len(corr) < 12:
                    corr.append({'id': d['id'], 'text': redact(t, 160)})
        elif kind == 'assistant':
            u = d['usage']
            cost += (u.get('cost') or {}).get('total', 0) or 0
            for k in ('input', 'output', 'cacheRead', 'cacheWrite'):
                tok[k] += u.get(k, 0) or 0
            if d['model']:
                models.add(d['model'])
            if d['stop'] in ('error', 'aborted'):
                s['aborted_or_error_turns'] += 1
            if d['text'].strip():
                last_asst = d['text']
        elif kind == 'call':
            n_calls += 1
            calls[d['id']] = dict(d, idx=n_calls)
            name, args = d['name'], d['args']
            tools[name] += 1
            p = args.get('path') or args.get('file_path') or ''
            if name == 'read':
                reads[(p, args.get('offset'))] += 1
                mm = re.search(r'/skills/([^/]+)/SKILL\.md$', p)
                if mm:
                    skills.add(mm[1])
                if n_calls <= 12 and SPEC_RE.search(p):
                    spec_read_early = True
            if name in ('edit', 'write') and p:
                edits[p] += 1
                edited_files.append(p)
                if DOC_RE.search(p):
                    docs_touched.add(os.path.relpath(p, cwd) if p.startswith(cwd) else p)
                if os.path.splitext(p)[1] in CODE_EXT:
                    code_edits += 1
                if first_edit is None:
                    first_edit = n_calls
                test_after_edit = check_after_edit = False
            if name == 'bash':
                cmd = args.get('command', '')
                bashcmds[re.sub(r'^(cd\s+\S+\s*(&&|;)\s*)+', '', re.sub(r'\s+', ' ', cmd.strip()))[:120]] += 1
                if GIT_COMMIT_RE.search(cmd):
                    s['git_commits'] += 1
                if GIT_PUSH_RE.search(cmd):
                    s['git_pushes'] += 1
                if TEST_RE.search(cmd):
                    test_runs += 1
                    test_after_edit = True
                if CHECK_RE.search(cmd):
                    check_runs += 1
                    check_after_edit = True
            if is_nav(d):
                nav_total += 1
                if first_edit is None:
                    nav_before += 1
            sig = hashlib.md5((name + json.dumps(args, sort_keys=True)).encode()).hexdigest()
            if sig == prev_sig and prev_err:
                s['retry_same_call_after_error'] += 1
            prev_sig = sig
        elif kind == 'result':
            c = calls.get(d['id'])
            prev_err = d['err']
            if d['err']:
                s['tool_errors'] += 1
            t = d['text']
            if 'BLOCKED by security' in t:
                s['security_blocks'] += 1
                blocks[redact(t.split('BLOCKED by security:')[-1], 70)] += 1
            for mm in re.finditer(r'([^\s:\'"`]+): No such file or directory|ENOENT[^\n]*?[\'"]([^\'"]+)[\'"]', t):
                missing[mm[1] or mm[2]] += 1
            if c and is_search(c):
                s['searches'] += 1
                body = t.strip()
                if (not body) or re.match(r'(?i)(no matches|0 (matches|results)|no files)', body) or (c['name'] == 'bash' and len(body) < 60 and 'exited with code 1' in body):
                    s['empty_searches'] += 1
    s = dict(s)
    rereads = sum(v - 1 for v in reads.values() if v > 1)
    hot = collections.Counter()
    for (p, _), v in reads.items():
        hot[p] += v
    inp = tok['input'] + tok['cacheRead'] + tok['cacheWrite']
    s.update({
        'id': os.path.basename(path)[-42:-6], 'file': path,
        'start': first_ts, 'end': last_ts, 'models': sorted(m for m in models if m),
        'tool_calls': n_calls, 'tools': dict(tools.most_common(8)),
        'cost': round(cost, 3), 'tokens': dict(tok), 'cache_hit': round(tok['cacheRead'] / inp, 2) if inp else None,
        'first_edit_at_call': first_edit, 'nav_before_first_edit': nav_before if first_edit else None, 'nav_total': nav_total,
        'rereads': rereads, 'hot_reads': [(redact(p, 90), v) for p, v in hot.most_common(5) if v > 1],
        'edit_churn': [(redact(p, 90), v) for p, v in edits.most_common(3) if v >= 4],
        'files_edited': len(edits), 'code_edits': code_edits,
        'test_runs': test_runs, 'check_runs': check_runs, 'code_edited_no_verify': code_edits > 0 and not (test_after_edit or check_after_edit),
        'spec_read_early': spec_read_early, 'docs_touched': sorted(docs_touched)[:6],
        'skills_seen': sorted(skills), 'security_block_reasons': dict(blocks.most_common(3)),
        'missing_paths': [redact(p, 90) for p, _ in missing.most_common(5)],
        'prompts': prompts, 'correction_samples': corr[:5],
        'final_assistant': redact(last_asst, 220),
        '_bash': bashcmds, '_hot': hot, '_missing': missing, '_edited': edited_files,
    })
    for k in ('corrections', 'compactions', 'tool_errors', 'security_blocks', 'empty_searches', 'searches', 'user_msgs', 'retry_same_call_after_error', 'git_commits', 'repeated_prompts'):
        s.setdefault(k, 0)
    return s


# ---------- repo health ----------
PATH_TOKEN = re.compile(r'`([^`\s]+)`|\]\(([^)\s#]+)')


def repo_health(cwd):
    def ex(*p):
        return os.path.exists(os.path.join(cwd, *p))
    r = {'cwd': cwd, 'git': ex('.git')}
    agents = [n for n in ('AGENTS.md', 'CLAUDE.md', 'CONTEXT.md') if ex(n)]
    r['agent_docs_lines'] = {n: sum(1 for _ in open(os.path.join(cwd, n), errors='ignore')) for n in agents}
    r['readme'] = ex('README.md')
    r['docs_dir'] = sorted(os.listdir(os.path.join(cwd, 'docs')))[:25] if ex('docs') else None
    r['prd_spec'] = [os.path.relpath(p, cwd) for p in glob.glob(os.path.join(cwd, '**', '*.md'), recursive=True)
                     if SPEC_RE.search(p) and 'node_modules' not in p][:8]
    r['tests'] = [n for n in ('tests', 'test', '__tests__', 'spec') if ex(n)]
    r['ci'] = [n for n in ('.github/workflows', '.gitlab-ci.yml', 'bitbucket-pipelines.yml', '.circleci') if ex(n)]
    r['automation'] = [n for n in ('Makefile', 'justfile', '.pre-commit-config.yaml', '.husky', 'package.json', 'pyproject.toml', 'validate-skills.sh', 'deploy.sh') if ex(n)]
    stale = []
    for n in agents + (['README.md'] if r['readme'] else []):
        txt = open(os.path.join(cwd, n), errors='ignore').read()
        for m in PATH_TOKEN.finditer(txt):
            tk = m[1] or m[2]
            if re.search(r'^(https?:|mailto:|~|\$|/)|[<>*{}|=\s]|^\.\.?$', tk) or ('/' not in tk and not re.search(r'\.\w{1,5}$', tk)):
                continue
            if re.search(r'\.(com|io|org|dev|net|ai)$', tk) or not re.search(r'[A-Za-z]', tk):
                continue
            if not os.path.exists(os.path.join(cwd, tk.split('#')[0].rstrip(':,.'))):
                stale.append(f'{n}: {tk}')
    r['stale_pointers'] = sorted(set(stale))[:20]
    return r


# ---------- aggregate / trend ----------
def metrics_of(ss):
    n = len(ss) or 1
    navs = [s['nav_before_first_edit'] for s in ss if s['nav_before_first_edit'] is not None]
    ce = [s for s in ss if s['code_edits']]
    tc = sum(s['tool_calls'] for s in ss) or 1
    srch = sum(s['searches'] for s in ss) or 1
    ch = [s['cache_hit'] for s in ss if s['cache_hit'] is not None]
    return {
        'sessions': len(ss), 'cost_total': round(sum(s['cost'] for s in ss), 2), 'cost_per_session': round(sum(s['cost'] for s in ss) / n, 2),
        'nav_before_first_edit_median': statistics.median(navs) if navs else None,
        'corrections_per_session': round(sum(s['corrections'] for s in ss) / n, 2),
        'tool_error_rate': round(sum(s['tool_errors'] for s in ss) / tc, 3),
        'empty_search_rate': round(sum(s['empty_searches'] for s in ss) / srch, 3),
        'rereads_per_session': round(sum(s['rereads'] for s in ss) / n, 2),
        'unverified_code_rate': round(sum(s['code_edited_no_verify'] for s in ce) / len(ce), 2) if ce else None,
        'compactions_per_session': round(sum(s['compactions'] for s in ss) / n, 2),
        'security_blocks_per_session': round(sum(s['security_blocks'] for s in ss) / n, 2),
        'cache_hit_avg': round(sum(ch) / len(ch), 2) if ch else None,
    }


def aggregate(ss):
    hot, missing = collections.Counter(), collections.Counter()
    bcount, bsess = collections.Counter(), collections.defaultdict(set)
    pcount, psess = collections.Counter(), collections.defaultdict(set)
    blocks, cost_model = collections.Counter(), collections.Counter()
    for s in ss:
        for p in s['_hot']:
            hot[p] += 1
        for c, v in s['_bash'].items():
            bcount[c] += v
            bsess[c].add(s['id'])
            pre = ' '.join(c.split()[:2])
            pcount[pre] += v
            psess[pre].add(s['id'])
        for p in s['_missing']:
            missing[p] += 1
        for k, v in s['security_block_reasons'].items():
            blocks[k] += v
        for m in s['models'][:1]:
            cost_model[m] += s['cost']
    return {
        'metrics': metrics_of(ss),
        'files_read_in_multiple_sessions': [(redact(p, 100), n) for p, n in hot.most_common(12) if n >= 2],
        'repeated_commands_automation_candidates': [(c, bcount[c], len(bsess[c])) for c, _ in bcount.most_common(60)
                                                    if bcount[c] >= 3 and len(bsess[c]) >= 2 and not NAV_RE.search(c)][:10],
        'frequent_command_prefixes': [(p, pcount[p], len(psess[p])) for p, _ in pcount.most_common(8)],
        'paths_that_did_not_exist': [(redact(p, 90), n) for p, n in missing.most_common(8)],
        'security_block_reasons': dict(blocks.most_common(5)),
        'cost_by_model': {k: round(v, 2) for k, v in cost_model.most_common(5)},
        'sessions_5plus_files_edited_without_early_spec_read': [s['id'][:8] for s in ss if s['files_edited'] >= 5 and not s['spec_read_early']][:10],
        'top_cost_sessions': [(s['id'][:8], s['cost'], s['prompts'][:1]) for s in sorted(ss, key=lambda s: -s['cost'])[:3]],
    }


def previous_retro(cwd, cur):
    for f in reversed(sorted(glob.glob(os.path.join(cwd, 'docs', 'report_retro-*.md')))):
        m = re.search(r'<!-- retro-metrics: (\{.*?\}) -->', open(f, errors='ignore').read())
        rel = os.path.relpath(f, cwd)
        if not m:
            return {'file': rel, 'metrics': None}
        prev = json.loads(m[1])
        delta = {k: {'prev': prev[k], 'now': v} for k, v in cur.items()
                 if k != 'sessions' and isinstance(v, (int, float)) and isinstance(prev.get(k), (int, float))}
        return {'file': rel, 'metrics': prev, 'compare': delta}
    return None


def strip_private(s):
    return {k: v for k, v in s.items() if not k.startswith('_')}


def cmd_digest(a):
    cwd = os.path.realpath(a.cwd)
    ss = [analyze(f, c) for _, f, c in select(a)]
    agg = aggregate(ss) if ss else {}
    print(json.dumps({
        'selection': {'cwd': cwd, 'count': len(ss), 'all_projects': a.all_projects, 'worktrees': a.worktrees,
                      'span': [ss[0]['start'], ss[-1]['end']] if ss else None},
        'repo': None if a.all_projects else repo_health(cwd),
        'aggregate': agg,
        'previous_retro': previous_retro(cwd, agg['metrics']) if ss and not a.all_projects else None,
    }, indent=1, default=str))
    print('## sessions (one JSON per line)')
    for s in ss:
        print(json.dumps(strip_private(s), default=str))


def cmd_excerpt(a):
    sel = select(argparse.Namespace(cwd='.', last=1, since=None, worktrees=False, no_subdirs=False,
                                    all_projects=True, session=a.session, include_current=True))
    if not sel:
        sys.exit('no session matches ' + a.session)
    path = sel[-1][1]
    kinds = set(a.kinds.split(','))
    out, calls, first_user, last = collections.defaultdict(list), {}, True, ''
    for kind, ts, d in events(path):
        hm = (ts or '')[11:19]
        if kind == 'user' and d['text'].strip():
            t = d['text'].strip()
            if 'user' in kinds:
                out['user'].append(f'[{hm}] {redact(t, 300)}')
            if 'corrections' in kinds and not first_user and CORR_RE.search(t[:400]):
                out['corrections'].append(f'[{hm}] {redact(t, 300)}')
            first_user = False
        elif kind == 'assistant' and d['text'].strip():
            last = d['text']
        elif kind == 'call':
            calls[d['id']] = d
        elif kind == 'result':
            c = calls.get(d['id'])
            desc = f"{d['name']} {redact(json.dumps(c['args']), 140) if c else ''}"
            if d['err'] and 'errors' in kinds:
                out['errors'].append(f"[{hm}] {desc} -> {redact(d['text'], 220)}")
            if 'BLOCKED by security' in d['text'] and 'blocks' in kinds:
                out['blocks'].append(f"[{hm}] {desc} -> {redact(d['text'], 160)}")
            if 'nav' in kinds and c and is_search(c) and len(d['text'].strip()) < 60:
                out['nav'].append(f"[{hm}] {desc} -> {redact(d['text'], 60) or '(empty)'}")
    if 'final' in kinds:
        out['final'].append(redact(last, 600))
    print('session:', path)
    for k in ('user', 'corrections', 'errors', 'blocks', 'nav', 'final'):
        if out[k]:
            print(f'\n## {k} ({len(out[k])})')
            for x in out[k][:a.max]:
                print('-', x)


def git(cwd, *cmd):
    return subprocess.run(['git', '-C', cwd, *cmd], capture_output=True, text=True).stdout


def cmd_outcome(a):
    days = int(re.match(r'\d+', a.window)[0])
    analyzed = [analyze(f, c) for _, f, c in select(a)]
    print(f'# outcome window={a.window} (only meaningful for sessions older than the window)')
    for s in analyzed:
        files = [p for p in dict.fromkeys(s['_edited']) if os.path.exists(p)]
        if not files or not s['end']:
            continue
        root = git(os.path.dirname(files[0]), 'rev-parse', '--show-toplevel').strip()
        if not root:
            continue
        end = datetime.fromisoformat(s['end'].replace('Z', '+00:00'))
        until = (end + timedelta(days=days)).isoformat()
        log = git(root, 'log', f'--since={(end + timedelta(minutes=5)).isoformat()}', f'--until={until}', '--format=%h|%s',
                  '--', *[os.path.relpath(p, root) for p in files[:60]])
        subs = [l.split('|', 1) for l in log.splitlines() if '|' in l]
        later = [o['id'][:8] for o in analyzed if o is not s and o['start'] and s['end'] < o['start'] < until and set(o['_edited']) & set(files)]
        print(json.dumps({
            'session': s['id'][:8], 'start': s['start'], 'prompt': s['prompts'][:1], 'files_edited': len(files),
            'followup_commits': len(subs), 'reverts': [x[1][:80] for x in subs if re.match(r'(?i)revert', x[1])],
            'fixes': [x[1][:80] for x in subs if re.search(r'(?i)^(fix|hotfix)|\bfix(es|ed)?\b', x[1])][:4],
            'followup_sessions_touching_same_files': later[:5]}))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest='cmd', required=True)

    def sel(x):
        x.add_argument('--cwd', default=os.getcwd())
        x.add_argument('--last', type=int, default=10)
        x.add_argument('--since')
        x.add_argument('--worktrees', action='store_true')
        x.add_argument('--no-subdirs', action='store_true')
        x.add_argument('--all-projects', action='store_true')
        x.add_argument('--session')
        x.add_argument('--include-current', action='store_true')
    d = sp.add_parser('digest'); sel(d); d.set_defaults(f=cmd_digest)
    e = sp.add_parser('excerpt'); e.add_argument('session'); e.add_argument('--kinds', default='user,corrections,errors,blocks,nav,final'); e.add_argument('--max', type=int, default=15); e.set_defaults(f=cmd_excerpt)
    o = sp.add_parser('outcome'); sel(o); o.add_argument('--window', default='3d'); o.set_defaults(f=cmd_outcome)
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
