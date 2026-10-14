# Evidence channels

Route each question to the cheapest channel that can answer it. Climb the ladder only when the lower rung leaves a specific gap. Never repeat an identical search; change the query or the channel.

## The ladder

| Rung | Channel | Proves | Cannot prove |
|---|---|---|---|
| 0 | **The product itself** (see [runtime-observation.md](runtime-observation.md)) | actual behaviour, API shape, latency, limits | internals behind the API, intent |
| 1 | **Vendor's own words**: docs, API reference, changelog, status page, pricing, trust/security page | intended behaviour, components named in incidents, plan limits | that it behaves that way; marketing is aspirational |
| 1 | **Privacy policy, DPA, subprocessor list** | the real vendor stack (cloud, CDN, LLM provider, analytics, payments, support tooling) | what each subprocessor is used for |
| 1 | **Store listings**: App Store "App Privacy", Play "Data safety", permissions | what data the app collects and links to identity | how it is processed |
| 2 | **Engineering signals**: job posts, eng blog, conference talks, podcasts, postmortems | stack, scale numbers, what they are building next, past failures | current state; talks are curated |
| 2 | **Code they published**: GitHub org, npm/PyPI SDKs, OpenAPI specs, Terraform providers | API contracts, auth model, retry and idempotency semantics, supported entities | server internals |
| 2 | **Files the site serves**: `robots.txt`, `sitemap.xml`, `/.well-known/*`, `llms.txt`, `security.txt`, `openapi.json`, source maps | route map, public API, sometimes near-full client source | anything not served |
| 3 | **Formal records**: SEC filings (S-1, 10-K risk factors), patents, court filings, certifications (SOC 2 scope, ISO) | stated architecture, revenue concentration, dependencies, algorithms claimed | that the patent is what ships |
| 3 | **Third parties**: other teardowns, StackShare, BuiltWith, G2 and store reviews, HN/Reddit | weak spots, user-visible failure modes, stack guesses | anything verified; mark `[S-low]` |
| 4 | **Closest OSS equivalents** | the shape of the solution space, a reference implementation to bound effort | that the target does it that way |

## What to extract where (high-yield spots)

- **Status page component list**: the vendor's own decomposition of its system (API, Dashboard, Webhooks, Search, Payments, Model inference). Incident write-ups name root causes.
- **Subprocessor list**: the stack in one table. A list containing a model provider, vector DB and queue tells you more than the marketing site.
- **Changelog cadence and content**: what ships weekly is cheap; what shipped once after six months is the hard part.
- **Pricing and limits**: back-compute unit cost. Per-seat vs per-credit vs per-token reveals what scales their costs. A free tier with a hard cap tells you COGS per user is meaningful.
- **Job posts**: "experience with Temporal, ClickHouse, pgvector" is stack evidence; the number of open roles per function is org shape. Tag `[S]` with date; posts lag reality.
- **Patents**: describe a mechanism the company thought was valuable. Read claims, not abstract. Tag `[S]` and note that it may not be what ships.
- **SDK source**: retry logic, idempotency keys, pagination style, error taxonomy, webhook signature scheme. Often the best free API spec there is.
- **Store reviews, 1-star first**: a map of what the product has not solved.

## Search tools that work in this environment

Run these in the **main session**. Subagents (including `researcher`) have no web tools and fall back to training-cutoff recall labelled "unverified"; do not fan web research out to them.

| Need | Command |
|---|---|
| Semantic search | `cd ~/.agents/skills/exa && ./scripts/search.sh '{"query":"...","numResults":8}'` |
| Fetch a page as text | `cd ~/.agents/skills/exa && ./scripts/contents.sh '{"urls":["..."],"text":{"maxCharacters":8000}}'` |
| Find pages like this one | `./scripts/find-similar.sh '{"url":"...","numResults":8}'` (exa) |
| Keyword search, site-scoped | `cd ~/.agents/skills/tavily && ./scripts/search.sh '{"query":"...","include_domains":["github.com"],"max_results":8}'` |
| Whole docs site | `cd ~/.agents/skills/tavily && ./scripts/crawl.sh '{"url":"https://docs...","max_depth":2,"limit":50}' ./out` |
| Long doc / SPA page | `web_fetch_exa` via the docker-gateway MCP (`{urls:[...], maxCharacters}`); beats Tavily extract on long pages |
| PDF (filing, whitepaper) or YouTube talk | the `summarize` skill; if its default path fails, `tavily/scripts/extract.sh` returns `raw_content` for PDFs |
| GitHub repo facts | `curl -s https://api.github.com/search/repositories?q=<name>+<topic>\&sort=stars` then `raw.githubusercontent.com/<o>/<r>/main/README.md` |

Gotchas seen here:
- If a script exits silently with no output, the key or quota is the cause. Switch tools; do not debug the script.
- `web_search_exa` via MCP accepts only `{query, numResults}`. Put recency in the query text ("news from the last month about X"); Exa returns `publishedDate` so you can verify.
- Some doc sites return a JS shell (e.g. `developers.openai.com/api/docs/*`). Record "unverified", move on.
- GitHub API through a cache layer can be stale. Cross-check a star or date claim on a second endpoint.
- Never run a skill's `.py` directly; Python goes through `uv run python`.

## Query patterns that earn their keep

```
<target> architecture                      <target> engineering blog
<target> "how we built"                    <target> postmortem OR incident
<target> subprocessors                     <target> SOC 2 OR "security whitepaper"
<target> careers backend OR infrastructure site:<jobs host>
<target> openapi OR "api reference"        <target> sdk site:github.com
<target> alternative open source           <target> vs <competitor> teardown
<target> patent <core mechanism>           <target> S-1 "risk factors"
```

## Source quality and the ledger

Each fact entering the ledger gets a source grade next to its tag:

- **A**: primary and first-hand (the product, its API, its own SDK or filing).
- **B**: vendor claim (docs, blog, talk). Intent, not proof.
- **C**: third-party analysis or interview. Plausible, check against A.
- **D**: forum, review, rumour. Pointer for where to look, never a basis for the blueprint.

Two independent B/C sources agreeing is still only [S]. Promote to [O] by checking the claim against the running product.
