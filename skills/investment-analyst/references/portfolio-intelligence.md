# Portfolio Intelligence Layer

The scan system finds new opportunities. This layer **tends existing positions** — detecting when to add, when to propagate signals, and when the thesis is strengthening faster than the price.

**Core principle:** Every position you own is a live sensor. Its data doesn't just inform itself — it illuminates your entire portfolio and watchlist.

---

## 1. Trajectory Check (Weekly)

For each holding, track the **direction** of fundamentals, not just the level.

### What to measure (quarterly data, refreshed after each earnings)

| Metric | Accelerating | Stable | Decelerating |
|--------|-------------|--------|--------------|
| Revenue growth QoQ | ↑ Each Q faster than prior | → Same rate | ↓ Slowing |
| Margin expansion | ↑ Operating margin widening | → Flat | ↓ Compressing |
| Earnings trajectory | ↑ Beats getting bigger | → In-line | ↓ Misses or shrinking beats |
| Guidance trend | ↑ Raising | → Maintaining | ↓ Lowering or hedging language |
| Backlog / bookings | ↑ Growing faster than revenue | → Matched | ↓ Shrinking |

### Decision Matrix

| Trajectory | Price Action | Action |
|-----------|-------------|--------|
| Accelerating | Consolidating/flat | **Add.** Market hasn't repriced yet. |
| Accelerating | Already running | **Hold/small add.** Momentum persists (Principle #14). |
| Accelerating | Pulling back | **Add aggressively.** Gift dip in a strengthening name. |
| Stable | Running up | Hold. Momentum may exhaust. |
| Stable | Flat | Hold. No edge. |
| Decelerating | Running up | **Trim.** Market is wrong or lagging. |
| Decelerating | Falling | Review kill trigger. |

### Profitability Inflection (Special Case)

When a growth company crosses from breakeven to sustainably profitable, the multiple re-rating is violent and persistent. Flag ANY holding that:
- Was marginally profitable or breakeven 2-3 quarters ago
- Now shows expanding margins + growing net income

This is the single highest-conviction "add" signal. The market systematically underprices this transition.

---

## 2. Signal Propagation (After Any Earnings/News)

When ONE holding reports results or material news, ask these three questions:

### Question A: "What does this confirm about my OTHER holdings?"

Example logic:
- DDOG crushes on AI observability demand → confirms MSFT Azure / GOOGL Cloud thesis
- HUBB beats on DC electrical equipment → confirms APH / ASML datacenter demand
- BTG misses on production → gold thesis intact but operator risk elevated
- MUV2 raises dividend → confirms reinsurance pricing cycle benefiting quality players

### Question B: "What does this tell me about my WATCHLIST?"

If a portfolio holding validates a theme, check if watchlist names in that theme should be upgraded:
- Move from "Researching" → "Entry signal strengthening"
- Move from Tier 2 → Tier 1
- Identify if the reporting company's customers/suppliers are investable

### Question C: "Does this reveal a NEW adjacent opportunity?"

A strong earnings report often names tailwinds in the call. Listen for:
- New customer segments mentioned for the first time
- Supply chain partners called out by name
- Capacity constraints mentioned (= upstream bottleneck = separate opportunity)
- Adjacent markets being entered

**Template (run after each portfolio holding reports):**
```
[TICKER] reported [date]. Key numbers: Rev $X (+Y% YoY), EPS $Z (beat/miss).

Signal propagation:
→ Confirms thesis for: [list other holdings benefiting from same demand]
→ Watchlist upgrade: [any watchlist name now higher conviction?]
→ New adjacency spotted: [anything mentioned in call worth researching?]
→ Portfolio action: [add/hold/trim this name based on trajectory]
```

---

## 3. Strength Recognition (Anti-Value Bias)

The value-oriented system has a bias: it's great at buying weakness (RSI oversold, beaten-down names) but systematically avoids buying strength. This is a mistake when fundamentals support the strength.

### When "Add on Strength" Is Correct

All three must be true:
1. **Fundamentals accelerating** (trajectory check positive)
2. **Secular tailwind confirmed** (not a one-quarter blip)
3. **Position is undersized** relative to conviction

If RSI is 60-75 but trajectory is accelerating, the correct move is a MEASURED add, not waiting for a pullback that may never come.

### When "Add on Strength" Is Wrong

Any one of these = don't chase:
- RSI > 80 (wait for consolidation)
- One-quarter spike without structural driver
- Position already at max allocation
- Earnings driven by one-time items, not operational improvement

### Position Sizing on Adds

- First entry (oversold/value): Full position (per strategy, typically 2-5% of portfolio)
- Add on trajectory confirmation: +50% of original position size
- Add on post-earnings gap + consolidation: +25-50% of original position size
- Never let any single name exceed portfolio max (currently ~10%)

---

## 4. Forward Catalyst Map (Monthly Update)

For every holding, maintain awareness of the NEXT material event. Not just earnings — anything that changes the narrative.

### Event Types to Track

| Type | Lead Time | Where to Find |
|------|-----------|---------------|
| Earnings date | 4-6 weeks | Yahoo Finance calendar, IR page |
| Analyst day / investor day | 2-4 weeks | IR page, press releases |
| Product launch / keynote | Varies | Company blog, industry conferences |
| Regulatory decision | Varies | FDA calendar, EU Commission, FCC |
| Contract renewal / award | Varies | SAM.gov, TED, company filings |
| Index inclusion / rebalance | 2 weeks | S&P, MSCI announcement dates |
| Insider lockup expiry | Fixed | SEC filings |
| Conference presentations | 1-2 weeks | Company IR page |

### Pre-Catalyst Checklist (5 Days Before Any Material Event)

1. What is consensus expecting? (revenue, EPS estimates)
2. What would a BEAT look like? (what specific metric proves thesis)
3. What would a MISS look like? (what breaks the thesis)
4. Is the stock priced for perfection or neglect?
5. Current position size — room to add if positive?
6. Options market: is IV elevated (expectations high) or low (surprise possible)?

If answers to 1-6 suggest asymmetric upside → consider pre-event add.
If IV is elevated and stock priced for perfection → hold, don't add (good news already priced).

---

## 5. Regime-to-Portfolio Mapping

When assessing market conditions (VIX, breadth, sector rotation), explicitly map to holdings.

### Regime Types & Portfolio Implications

| Regime | Signal | Portfolio Action |
|--------|--------|-----------------|
| Risk-on, narrow (AI/mega-cap led) | Low VIX + cap-weight >> equal-weight | OVERWEIGHT your AI/growth names (they're the leaders) |
| Risk-on, broad | Low VIX + cap-weight ≈ equal-weight | Hold balanced, small-caps catch up |
| Risk-off, defensive | High VIX + rotation to staples/utilities | UNDERWEIGHT growth, OVERWEIGHT MUV2/BTG/VWCE |
| Rotation / transitioning | Rising VIX + leadership change | Trim extended names, add to laggards with intact thesis |

### Weekly Question

> "Given current market regime, which of my holdings should I be ADDING to, and which are getting a free ride from beta that might reverse?"

If the market is rewarding AI/growth and you have 1 share of DDOG and 6.47 shares of PYPL, your sizing is BACKWARDS relative to the regime. Either:
- Accept it (value will catch up eventually)
- Or lean into what's working (add to strength while regime persists)

---

## 6. Integration: The "Tend" Loop

Run this alongside the thematic scan. Not instead of it — in addition.

### Weekly (10 minutes, same day as weekly ritual)

1. **Trajectory snapshot:** Which holdings are accelerating? Decelerating?
2. **Catalyst calendar:** Anything in next 2 weeks for any holding?
3. **Regime check:** Does current market favor my largest positions or my smallest?
4. **Propagation backlog:** Did any holding report since last check? Run signal propagation.

### After Any Portfolio Holding Reports Earnings

1. Run signal propagation template (Section 2)
2. Update trajectory assessment (Section 1)
3. Decision: Add / Hold / Trim (Section 3)
4. Update exit plan if thesis strengthened or weakened

### Monthly

1. Full trajectory table for all holdings (refresh from quarterly data)
2. Forward catalyst calendar (next 60 days)
3. Position sizing review vs. regime and trajectory
4. Ask: "Am I undersized in my highest-conviction accelerating names?"

---

## Common Traps This Layer Prevents

| Trap | How It Manifests | What This Layer Does |
|------|-----------------|---------------------|
| "Set and forget" | Own DDOG, never check its trajectory | Trajectory check flags acceleration |
| "Always hunting, never farming" | Spend all energy on new names | Forces weekly review of existing holdings |
| "Value bias in a momentum market" | Wait for pullback that never comes | Strength recognition permits adds on confirmation |
| "Siloed positions" | Treat each holding independently | Signal propagation connects the dots |
| "Surprised by earnings" | Holdings report and you react instead of anticipate | Catalyst map provides lead time |
| "Wrong sizing for regime" | Tiny position in market's favorite theme | Regime mapping highlights misallocations |
| "Miss the second move" | Catch the initial entry, miss the continuation | Trajectory + post-earnings add rules capture the rest |

---

## Anti-Patterns (Don't Do This)

- **Don't add to decelerating names** just because they're cheap. That's averaging down into a breaking thesis.
- **Don't add at RSI > 80.** Even with perfect trajectory, wait for consolidation. The entry might be 5% higher but the risk/reward is radically better.
- **Don't propagate signals from a single quarter.** One beat ≠ trend. Two beats + guidance raise = trend confirmation.
- **Don't oversize on conviction alone.** Max position limits exist for a reason. Even if you're 100% sure, you're sometimes wrong.
- **Don't check trajectory daily.** This is a quarterly data cycle overlaid on weekly/monthly review. Daily checking creates noise and overtrading.
