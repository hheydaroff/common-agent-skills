# Exit Strategy Framework

Define your exit BEFORE entry. Every position needs a pre-committed exit plan with specific triggers, sizing rules, and monitoring cadence.

## The 4 Exit Types

```
1. THESIS KILL — The thesis is broken. Get out immediately (days).
2. TARGET HIT — Price reached fair value / Phase 3 repricing complete. Scale out.
3. TIME DECAY — Nothing happened. Thesis intact but no catalysts materializing. Redeploy.
4. PORTFOLIO TRIM — Position grew too large via appreciation. Rebalance mechanically.
```

## Exit Type 1: Thesis Kill (Emergency Exit)

**When:** The foundational reason you bought is DISPROVEN, not just challenged.

**Kill signals (exit 100% within 1-3 days):**

| Signal | Example | How to Monitor |
|--------|---------|----------------|
| Customer contract cancelled | Major customer switches to competitor | Earnings calls, 8-K filings, press releases |
| Regulatory reversal | Permits denied, legislation repealed, EU directive withdrawn | Government registers, TED, Federal Register |
| Structural demand disappeared | Technology obsoleted, substitute emerged | Trade publications, competitor product launches |
| Accounting fraud / restatement | Revenue recognition issues, auditor change | SEC filings, BaFin notices, short-seller reports |
| Insider selling surge | CEO/CFO selling >25% of holdings within 30 days | OpenInsider (US), Disclosyr (EU), Form 4 |
| Debt spiral | Credit downgrade + inability to refinance + covenant breach | Moody's/S&P alerts, bond spread widening |
| Supply advantage lost | Competitor built equivalent capacity, patent expired | Trade journals, competitor capex announcements |

**Rule:** If you can articulate a thesis kill scenario at entry, you MUST set an alert for it. No "I'll check later."

**Decision framework:**
```
Is my ORIGINAL thesis still valid?
├── YES → Hold (re-evaluate at next checkpoint)
├── UNCLEAR → Reduce by 50%, set 2-week deadline to resolve
└── NO → Full exit, no anchoring to cost basis
```

## Exit Type 2: Target Hit (Profit Taking)

**When:** The stock has repriced to reflect the thesis you identified in Phase 2.

### Phase-Based Exit Targets

| Entry Phase | Exit When | Typical Return | Action |
|-------------|-----------|----------------|--------|
| Early Phase 2 | Mid Phase 3 (analyst upgrades, ETF inclusion) | 100-300% | Scale out 50-75% |
| Mid Phase 2 | Late Phase 3 (media hype, retail piling in) | 50-150% | Scale out 75-100% |
| Late Phase 2 | Early Phase 3 (first re-rating) | 30-80% | Full exit or tight trail |

### Valuation-Based Targets (set at entry)

Calculate THREE targets before entering:

```
T1 (Conservative): Stock trades at sector median multiple
   → Action: Sell 33% of position
   
T2 (Base case): Stock trades at premium peer multiple  
   → Action: Sell another 33%
   
T3 (Euphoria): Stock trades above ANY reasonable fundamental justification
   → Action: Sell remainder OR set 15% trailing stop on rest
```

**How to calculate targets:**
- `market_data.py compare <TICKER>,<PEER1>,<PEER2>` — get current peer multiples
- T1 = Current EPS × Median sector P/E
- T2 = Forward EPS × Best-in-class peer P/E
- T3 = T2 × 1.5 (momentum/euphoria premium)

### Momentum-Based Exit (for Phase 3 runners)

When a position has exceeded T2 and you're letting it ride:

| Indicator | Exit Signal | Why |
|-----------|-------------|-----|
| RSI > 80 for 5+ days | Trim 25% | Extreme overbought, mean reversion likely |
| Volume spike > 3x average on red day | Trim 50% | Distribution — smart money exiting |
| 3 consecutive closes below 10-DMA after trend | Trailing stop triggered | Momentum exhaustion |
| MACD bearish crossover on weekly chart | Begin scaling out | Intermediate trend reversal |
| Bollinger Band width expansion + outside band close | Sell into strength | Volatility spike = potential reversal |

### Scaling Out Protocol

Never exit a full position at once (unless thesis kill). Scale out:

```
Position: 100 shares @ $50 entry

T1 hit ($75): Sell 33 shares → Lock $825 profit, cost basis drops
T2 hit ($100): Sell 33 shares → Lock $1,650 cumulative
T3 hit ($130+): Trail remaining 34 shares with 15% stop

Net result: Captured majority of upside, still participating in tail
```

## Exit Type 3: Time Decay (Thesis Timeout)

**When:** Nothing went wrong, but nothing went right either. Capital is dead.

### Time-Based Rules

| Holding Period | Action | Rationale |
|----------------|--------|-----------|
| 6 months, no catalysts fired | Review position hard | Opportunity cost is real |
| 9 months, stock flat ±10% | Reduce by 50% | Thesis may be too early or wrong |
| 12 months, no phase progression | Exit fully | Your timing was off; redeploy |

### Re-evaluation Checklist (at 6-month mark)

Ask these questions:

1. **Has the catalyst timeline shifted?** (delayed ≠ dead, but delayed = expensive)
2. **Are commitment signals still accumulating?** (contracts, permits, capex)
3. **Has analyst coverage changed?** (more analysts = thesis getting noticed = good)
4. **Is the supply constraint TIGHTER or LOOSER?** (loosening = thesis weakening)
5. **Has a competitor solved the bottleneck?** (your moat may be eroding)
6. **Is there a better opportunity for this capital?** (always compare alternatives)

**Score each 0-2. If total < 6/12, exit. If 6-8/12, halve position. If > 8/12, hold/add.**

### Dead Money Indicators

- Revenue growth decelerating for 2+ quarters
- Backlog shrinking while peers grow
- Management stops mentioning the theme in earnings calls
- Insider buying has dried up completely
- No new contracts or commitments in 6 months

## Exit Type 4: Portfolio Trim (Mechanical Rebalancing)

**When:** Position has grown via appreciation and now violates portfolio rules.

### Position Size Limits

| Conviction Level | Max Single Position | Trim Trigger |
|-----------------|--------------------|--------------| 
| High (score 2.5+) | 8% of portfolio | At 10% |
| Medium (score 2.0-2.5) | 5% of portfolio | At 7% |
| Low (score 1.5-2.0) | 3% of portfolio | At 4% |
| Theme basket (total) | 20% of portfolio | At 25% |

**Rule:** When a position hits trim trigger, sell down to max target. No exceptions. This is MECHANICAL, not discretionary.

### Correlation-Based Trim

If 3+ positions are in the same theme and ALL rallying together:
- Your portfolio is MORE concentrated than you think
- Trim the weakest thesis in the basket, keep the strongest
- Calculate effective concentration: `sum of correlated positions × average correlation`

---

## What to Watch: Ongoing Monitoring Signals

### Weekly Monitoring Checklist (per position)

Run this every Friday or integrate into `/invest watchlist`:

```bash
# Quick health check
market_data.py technicals <TICKER> 3mo    # Trend intact?
market_data.py price <TICKER>             # Valuation stretched?
market_data.py recommendations <TICKER>   # Analyst sentiment shift?
```

| What to Watch | Tool/Source | Red Flag | Green Flag |
|---------------|-------------|----------|------------|
| Price vs 50-DMA | `technicals` | Below 50-DMA for 10+ days | Above, trending up |
| RSI | `technicals` | Divergence (price up, RSI down) | Confirming trend |
| Volume pattern | `technicals` / Alpaca bars | Distribution (high vol on down days) | Accumulation (high vol on up days) |
| Analyst revisions | `recommendations` | Downgrades, target cuts | Upgrades, initiations |
| Insider activity | OpenInsider / Disclosyr | CFO selling, multiple insiders selling | Cluster buying |
| Short interest | Finviz / MarketBeat | Rising >10% of float, increasing daily | Declining (shorts covering) |
| Earnings estimates | Yahoo Finance / MarketScreener | Revisions down | Revisions up |
| Sector relative strength | Compare vs sector ETF | Underperforming sector for 4+ weeks | Outperforming |
| Credit/debt market | Bond yields, CDS spreads | Widening spreads for company/sector | Stable/tightening |

### Monthly Deep Check (per position)

1. **Re-score the 7 signals** — has the score IMPROVED or DETERIORATED?
2. **Phase re-assessment** — has it moved from Phase 2 → Phase 3? (if yes, start scaling out)
3. **Thesis validation** — any DISCONFIRMING evidence this month?
4. **Opportunity cost** — is there a higher-scored opportunity waiting for this capital?

### Earnings Season Protocol

Before each earnings report for a held position:

1. **Pre-earnings decision:** Hold through or reduce before?
   - If position is >5% of portfolio → trim to 3% before earnings (risk management)
   - If position is <3% → hold through
   
2. **What to watch in the report:**
   - Revenue vs consensus (beat/miss)
   - Guidance direction (raised/maintained/lowered)
   - Backlog/bookings commentary
   - Margin trajectory
   - Any mention of your thesis keywords
   
3. **Post-earnings action framework:**

| Result | Revenue | Guidance | Action |
|--------|---------|----------|--------|
| Bull | Beat >5% | Raised | Hold / add on pullback |
| Okay | Beat 0-5% | Maintained | Hold, monitor |
| Caution | Miss | Maintained | Reduce 25-50% |
| Bear | Miss | Lowered | Exit 75-100% |
| Disaster | Miss + restatement | Withdrawn | Exit immediately |

---

## Exit Timing: When to Act

### Market Regime Considerations

| Regime | How It Affects Exits |
|--------|---------------------|
| Bull (VIX < 15, breadth expanding) | Let winners run, use wider trailing stops (20%) |
| Normal (VIX 15-25) | Standard exit rules apply (15% trails) |
| Elevated vol (VIX 25-35) | Tighten stops to 10%, take profits faster |
| Crisis (VIX > 35) | All positions to survival mode — exit anything below conviction High |

### Time-of-Day/Week Rules

- **Don't exit in the first 30 minutes** of trading (noise, gap fills)
- **Best exit windows:** 10:30-11:30 AM or 2:00-3:30 PM (most stable liquidity)
- **Avoid Friday afternoon exits** unless urgent (low liquidity, wide spreads)
- **Earnings day:** If exiting post-earnings, wait at least 30 min for price discovery

### Tax Considerations (awareness, not advice)

- Track holding periods: >1 year = long-term capital gains rate
- If you're 10 months into a position with 20%+ gain, consider waiting 2 months for LTCG
- Harvest losses in December if holding thesis-killed positions at a loss
- Consider specific lot identification for partial sales (sell highest-cost lots first)

---

## Exit Plan Template (Fill at Entry)

For every new position, write this BEFORE buying:

```markdown
## Exit Plan: <TICKER>

**Entry date:** YYYY-MM-DD
**Entry price:** $X
**Position size:** X% of portfolio
**Thesis in one sentence:** "..."

### Targets
- T1 (conservative): $X (based on: ...)
- T2 (base case): $X (based on: ...)  
- T3 (euphoria): $X (trailing stop: 15%)

### Thesis Kill Triggers (exit 100%)
1. [Specific scenario that disproves thesis]
2. [Specific scenario that disproves thesis]

### Time Limit
- 6-month review date: YYYY-MM-DD
- Maximum hold without catalyst: 12 months

### Scaling Plan
- At T1: Sell ___ shares
- At T2: Sell ___ shares
- At T3: Trail remainder with ___% stop

### What I'm Watching Weekly
- [ ] Indicator 1
- [ ] Indicator 2
- [ ] Indicator 3
```

---

## Anti-Patterns: Common Exit Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| "I'll sell when it gets back to even" | Anchoring to cost basis, not thesis | Ask: "Would I buy this TODAY at this price?" If no, sell. |
| "It might come back" | Hope is not a strategy | Pre-commit to thesis kill triggers |
| "I'll sell when it doubles" | Arbitrary target disconnected from valuation | Use DCF/multiple-based targets |
| Never taking profits | Riding positions from +100% back to +10% | Pre-commit to T1/T2/T3 scaling |
| Panic selling on one bad day | Noise ≠ signal, especially with volatile small-caps | Check: Is thesis KILLED or just TESTED? |
| Selling winners, holding losers | Disposition effect (cognitive bias) | Mechanical rules: trim by SIZE, not by gain |
| Ignoring opportunity cost | "It's not losing money" but it's flat for 12 months | Time decay exit at 12-month mark |

---

## Integration with Entry Workflows

### At Entry (from Deep Dive, Laggard Scan, or Early Opportunity):
1. Complete the Exit Plan Template above
2. Set price alerts for T1, T2, and thesis kill levels
3. Add to watchlist with next review date
4. Note the specific Phase you're entering at

### Ongoing (from Watchlist Check):
1. Run weekly monitoring signals
2. Flag any RED indicators
3. Score deterioration vs improvement
4. Trigger exit type if thresholds breached

### At Exit:
1. Document: Why exiting, what type, what happened
2. Post-mortem: Was the thesis right? Was timing right? What would I do differently?
3. Redeploy: Where does this capital go now? (Cash is a valid position)

---

## Key Principles

1. **Define the exit before the entry** — if you can't articulate when you'd sell, don't buy
2. **Thesis kill > stop loss** — fundamental thesis break matters more than arbitrary % drawdowns
3. **Scale out, don't time the top** — selling in thirds captures more upside than trying to nail the peak
4. **Opportunity cost is real cost** — dead money for 12 months is a failed trade even if breakeven
5. **Mechanical rebalancing prevents concentration** — don't let a winner become your whole portfolio
6. **Weekly monitoring prevents surprises** — 5 min per position per week catches deterioration early
7. **Document everything** — exit post-mortems build judgment for next time
8. **Cash is a position** — after exit, "wait for the next Phase 2" is a valid allocation
