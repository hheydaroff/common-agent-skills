# Runtime observation

Use the product the way a user does, from your own account, and record what the client, network and responses show. This is the only rung that yields **[O]** evidence about behaviour. Keep every capture small and tied to one question.

Static (what the page ships) and runtime (what it does) answer different things. A bundle that contains a string proves the string shipped, not that the code path runs. Say which one you have.

## 0. Pick the canonical transaction

One unit of work, traced end to end, is the backbone of the teardown. Write it before you touch the product:

```
TRIGGER   user does what?                    (types a prompt, submits a search, pays)
INPUT     what data leaves the client?
PROCESS   what must happen for this to work? (unknown: fill from observation)
STATE     what is stored, where, for how long?
RESULT    what comes back, how fast, in what shape?
```

Examples: Gamma = prompt to generated deck; Airbnb = search to booking; Stripe = card entered to payout settled.

## 1. Drive the web app (browser-tools skill)

Chrome on `:9222` via `browser-tools`. Scripts live in `~/.agents/skills/browser-tools/`.

```bash
cd ~/.agents/skills/browser-tools
node browser-start.js                       # Chrome with remote debugging
node browser-nav.js https://target.example
node browser-screenshot.js                  # pixels when layout matters
node browser-content.js https://target.example/docs   # readable text
```

Prefer DOM and network evidence over screenshots.

### 1a. Initial-load requests (no hook needed)

```bash
node browser-eval.js 'JSON.stringify(performance.getEntriesByType("resource").map(e=>[e.initiatorType,e.name,Math.round(e.duration),e.transferSize]))'
```

Gives every script, XHR and image the first load fetched, with timing and size. Group by origin: first-party API hosts, CDN, analytics, auth, payments and model providers appear immediately.

### 1b. Capture API calls during interaction (fetch/XHR hook)

Install after the page loads, then interact **without a full reload** (a reload wipes the hook; re-install after each hard navigation):

```bash
node browser-eval.js '(()=>{const L=window.__cap=[];const F=window.fetch;window.fetch=async(i,n)=>{const t=performance.now();const r=await F(i,n);L.push({k:"fetch",u:String(i&&i.url||i),m:(n&&n.method)||"GET",s:r.status,ms:Math.round(performance.now()-t),b:n&&typeof n.body==="string"?n.body.slice(0,1500):null});return r};const O=XMLHttpRequest.prototype.open,S=XMLHttpRequest.prototype.send;XMLHttpRequest.prototype.open=function(m,u){this.__m=m;this.__u=u;return O.apply(this,arguments)};XMLHttpRequest.prototype.send=function(b){const x=this,t=performance.now();x.addEventListener("loadend",()=>L.push({k:"xhr",u:x.__u,m:x.__m,s:x.status,ms:Math.round(performance.now()-t),b:typeof b==="string"?b.slice(0,1500):null}));return S.apply(this,arguments)};return "hooked"})()'

# ... perform the canonical transaction in the browser, then:
node browser-eval.js 'JSON.stringify(window.__cap,null,1)'
```

Limits to state in the ledger: sees only calls the page's own JS makes after hooking; no WebSocket or SSE frames (add a `WebSocket` and `EventSource` wrapper if the product streams); no request initiator stack. LLM products usually stream; capturing the stream shape (SSE events, chunk cadence, final message) is itself a finding.

### 1c. Build the API surface table

From the captures, one row per endpoint. Group by method and path template (`/v1/decks/:id`):

| Method | Path template | Request keys | Response keys | Status seen | Inferred resource | Obs ID |
|---|---|---|---|---|---|---|

Keys, not values. This table is your reconstructed data model; the entities and their foreign keys fall out of it. Query-parameter names are observations; "required" is an inference.

### 1d. Mine the shipped client (static, still public)

```bash
node browser-eval.js 'JSON.stringify([...document.scripts].map(s=>s.src).filter(Boolean))'
curl -s https://target.example/_next/static/chunks/<name>.js | grep -oE '"/(api|v[0-9])/[a-zA-Z0-9_/:.-]+"' | sort -u
curl -sI https://target.example/_next/static/chunks/<name>.js.map   # 200 = source map is public
```

Greppable gold in bundles: endpoint paths, feature-flag names, model identifiers (`claude-`, `gpt-`, `gemini-`), env-style keys, i18n strings (they list every state and error the product has), enum values, route tables. Source maps, when public, give near-full client source: read them as `[O]` for the client only.

### 1e. Stack fingerprint (headers, cookies, error pages)

```bash
curl -sI https://target.example | head -30
curl -s -o /dev/null -w '%{http_code} ttfb=%{time_starttransfer}s total=%{time_total}s\n' https://target.example/some-404
```

| Signal | Suggests |
|---|---|
| `server: cloudflare`, `cf-ray`, `__cf_bm` cookie | Cloudflare edge/bot management |
| `x-vercel-id`, `/_next/static/` | Next.js on Vercel |
| `x-amz-cf-id`, `via: CloudFront` | CloudFront |
| `server: envoy`, `x-envoy-upstream-service-time` | Envoy/Istio service mesh; the header is upstream latency |
| `grpc-status`, `application/grpc-web` | gRPC-web backend |
| `x-request-id` format (UUID vs ULID vs `req_...`) | ID scheme; prefixed IDs (`req_`, `ch_`) imply typed resource model |
| `x-ratelimit-*`, `retry-after` | limits and window; token-bucket vs fixed window by behaviour |
| `__Host-`/`next-auth`/`sb-` cookies | auth stack (NextAuth, Supabase) |
| default framework 404 or validation error shape | Express, FastAPI, Rails, Django, Spring |
| `set-cookie` for analytics (`ajs_`, `_ga`, `amp_`, `ph_`) | Segment, GA, Amplitude, PostHog |

These are inferences until a second signal agrees. Tag [I] and name the signals.

### 1f. Error and limit mining

Cheap, high-yield, safe if you stay on your own account:
- Submit an empty or malformed input through the UI. Read the validation message and the 4xx body: they reveal field names, constraints and framework.
- Hit an obviously unsupported option (a 10,000-word prompt, a 200 MB file). The error states the limit.
- Watch for `429`. Stop at the first one and record the headers.
- Read the empty states, loading states and failure copy: they enumerate the system's states.

### 1g. Timing as architecture evidence

Repeat the canonical transaction 5 times and record time-to-first-byte and total time. Large first-call vs warm-call gap suggests cold start or queue; long flat time suggests batch or generation; streaming first-token latency vs total separates model call from post-processing. Record n, spread, region and time of day. One sample is an anecdote.

### 1h. Account and funnel

Sign up. Note the fields asked, verification steps, what onboarding makes you do first (that is the activation event they optimise), what is gated behind payment, what a free account is capped at. Plans and limits tell you what costs them money.

## 2. Mobile and desktop apps

In scope: **what the app shows and says**, not its binary.
- Store listing: version history ("What's new"), permissions, App Privacy labels, Data safety section, screenshots, size, minimum OS, SDK mentions in the description.
- If the user has it installed: drive the UI with `computer-use-peekaboo`, record screens and flows, compare features to the web app.
- Out of scope: unpacking, decompiling or disassembling the app. Say it is out of scope and use the web client and API instead, which are almost always the same backend.

## 3. Discovery endpoints

Fetch only what the site itself publishes:

```bash
for p in robots.txt sitemap.xml .well-known/security.txt llms.txt openapi.json swagger.json .well-known/openid-configuration; do
  printf '%s -> ' "$p"; curl -s -o /dev/null -w '%{http_code}\n' "https://target.example/$p"; done
```

A public OpenAPI file or OIDC discovery document is a primary source ([O], grade A). GraphQL introspection counts only if the endpoint is publicly documented; do not use it against a product whose ToS forbids it.

## 4. Record observations

Give every capture an ID (`O1`, `O2`, ...) and log how it was produced (command, account tier, date, region) so it can be repeated:

```
O7  2026-10-14  free tier, EU  POST /api/generate  200  streamed SSE, 14 events, first token 1.9s, total 41s
    produced by: fetch hook, prompt "10 slide deck about X". Raw: docs/teardown/O7.json (tokens redacted)
```

Raw captures go in `docs/teardown/` (redacted); the report cites IDs, never pastes bulk payloads.

## 5. Limits of this rung

Say so in the report whenever true: single account tier, single region, single day, UI-triggered calls only, server internals invisible, features behind a paywall not observed. A feature you could not reach is **unknown**, not absent.
