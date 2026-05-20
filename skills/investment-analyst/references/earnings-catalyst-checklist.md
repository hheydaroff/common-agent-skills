# Earnings Catalyst Checklist

Pre-earnings analysis framework: identify the 3-5 things that will determine the stock's reaction, build scenario tables, and compare implied vs historical moves.

## When to Use

- `/invest earnings <TICKER>` — enhanced with this framework
- "What should I watch for [company] earnings?"
- Pre-positioning before any binary event

## Core Insight

Earnings reactions are driven by **3-5 key items**, not by the overall beat/miss. A company can beat EPS by 5% and drop 10% if the ONE thing the market cared about disappointed.

## Step 1: Sector-Specific KPIs

**Tech/SaaS:** ARR, Net Revenue Retention, RPO, AI revenue/bookings
**Retail/Consumer:** Same-store sales (traffic vs ticket), inventory levels, promo guidance
**Industrials:** Backlog, book-to-bill, price vs volume, geographic mix
**Financials:** NIM trajectory, credit quality (NCOs), fee income growth
**Healthcare:** Patient volumes, pipeline updates, reimbursement commentary
**Semiconductors:** Gross margin guidance, end-market demand, lead times

## Step 2: Ranked Catalyst Checklist

```markdown
## Earnings Catalyst Checklist: <TICKER> Q[X] YYYY

1. **[Most Important]** — consensus: [X] — Why: [explanation]
   - Bull trigger: [what = stock up]
   - Bear trigger: [what = stock down]

2. **[Second Most Important]** — consensus: [X]
   - Bull/Bear triggers

3. **[Guidance Item]** — buy-side expects: [X]

4. **[Narrative/Strategic]** — watching for: [X]
```

## Step 3: Scenario Table

```markdown
| Scenario | Revenue | EPS | Key Driver | Prob. | Stock Reaction |
|----------|---------|-----|------------|-------|----------------|
| **Bull** | +X% beat | +X% beat | [what goes right] | 25% | +X% to +X% |
| **Base** | inline | inline | [meets expectations] | 50% | -2% to +3% |
| **Bear** | -X% miss | -X% miss | [what goes wrong] | 25% | -X% to -X% |
```

## Step 4: Implied Move vs Historical

```markdown
### Move Analysis
- **Implied move** (straddle ÷ price): ±X.X%
- **Avg actual move** (last 8 Qs): ±X.X%
- **Ratio** (implied ÷ actual): X.Xx
  - >1.2x: Market pricing MORE uncertainty → options expensive
  - <0.8x: Market pricing LESS uncertainty → options cheap
  - 0.8-1.2x: Fairly priced

### Historical Earnings Moves
| Quarter | EPS Surprise | 1-Day Move | Direction |
|---------|-------------|-----------|-----------|
| Q[X] | +X% | +X.X% | Beat = Up |
| Q[X] | +X% | -X.X% | Beat but guided down |
```

## Step 5: Positioning Recommendation

```markdown
## Pre-Earnings Summary
**Top 3 Things That Matter:**
1. [Item] — Market expects: [X] — Our view: [Y]
2. [Item] — Market expects: [X] — Our view: [Y]
3. [Item] — Market expects: [X] — Our view: [Y]

**Positioning:** [Hold through / Trim before / Add after / Options play / Avoid]
```
