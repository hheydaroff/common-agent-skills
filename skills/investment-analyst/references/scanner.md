# Early Opportunity Scanner (`/invest scan <THEME>` or `/invest early`)

Find investment opportunities in Phase 2 (committed but not yet repriced) before the market prices them in.

## The Phase Framework

```
Phase 1: Research/patents/pilots         → TOO EARLY (no catalyst, no timeline)
Phase 2: Permits/contracts/VC rounds      → SWEET SPOT (real commitment, not yet priced)
Phase 3: Analyst upgrades/ETF inclusion   → TOO LATE (already repriced, momentum only)
```

## Process

### 1. Identify structural demand drivers (not hype)

- Exa search: `"<THEME> construction permit contract signed procurement 2026"` (category: news, time: month)
- Exa search: `"<THEME> series B series C funding raised 2026"` (category: news, time: month)
- Tavily search: `"<THEME> regulatory approval legislation passed"` (time_range: month)
- **EU-specific:** Tavily search: `"<THEME> EU regulation directive approved"` (time_range: month)
- **EU-specific:** Tavily search: `"<THEME> European Investment Bank EIB funding"` (time_range: month)

### 2. Find the bottleneck suppliers (picks-and-shovels)

- Exa search: `"<THEME> supply chain bottleneck supplier shortage"`
- Ask: "Who are the companies that EVERY player in this theme must buy from?"
- **EU-specific:** Check European mid-caps (often sole-source, under-followed)

### 3. Check if still under-followed

- `market_data.py recommendations <TICKER>` — look for < 10 analysts covering
- If 3-5 analysts → very early. If 15+ → market already knows.

### 4. Verify valuation hasn't already moved

- `market_data.py price <TICKER>` — check 52-week change
- `market_data.py technicals <TICKER> 1y` — if up >100% already, likely Phase 3
- Compare forward P/E to sector peers

### 5. Confirm commitment signals (not just talk)

- **US:** Permits filed or issued (NRC, FERC, DOE, EPA)
- **EU:** TED contracts (ted.europa.eu), EU Commission directives, national procurement
- Customer contracts signed (not MOUs or "exploring")
- Capex announced in earnings calls
- **US:** Insider buying (Form 4 via openinsider.com)
- **EU:** Insider dealing (Disclosyr.com, Investegate.co.uk RNS, BaFin register)
- Hiring surges in specific technical roles

## "Be Early" Principles

1. **Track commitment signals, not headlines** — permits > press releases, contracts > MOUs, capex > guidance
2. **Find the bottleneck** — in any theme, ONE input is constrained. The company that owns it wins.
3. **Under-followed = edge** — if <10 analysts cover a $2-20B company, the market may be mispricing it
4. **Convergence > single signal** — regulation + capital + customers all pointing same direction = high conviction
5. **Size for uncertainty** — early bets get 2-5% allocation each, never YOLO
6. **Define the exit before entry** — what specific event proves the thesis wrong?
7. **The best time to buy is when it's boring** — if nobody's talking about it but commitments are real, that's the setup

## Output Format

```markdown
# Early Opportunity Scan: <THEME>

## Phase Assessment: [1 / 2-Early / 2-Late / 3]

## Structural Demand Driver
- What's causing this? (regulation, tech shift, demographics)
- Is it reversible? (if yes → skip)

## Commitment Signals Found
- [list concrete evidence: permits, contracts, funding, capex]

## Bottleneck Map
- Who supplies the constrained input?
- Who can't be routed around?

## Candidate Stocks
| Ticker | What They Do | Analyst Count | 52w Return | Fwd P/E | Phase |

## Timing & Catalysts
- What specific event moves this from Phase 2 → Phase 3?
- Expected timeline

## Risk: What Kills This Thesis?
- Single biggest risk
- How to monitor it
```
