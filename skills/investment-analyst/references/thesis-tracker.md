# Thesis Tracker

Maintain persistent investment theses for portfolio positions and watchlist names. Track key data points, catalysts, and thesis milestones over time.

## When to Use

- `/invest thesis <TICKER>` — create or update a thesis
- "Is my thesis still intact?"
- "Add data point to [company]"
- "Review my positions"
- After any earnings or material event for a held position

## File Location

Store thesis files in the user's vault: `finance/thesis-<TICKER>.md`

## Creating a New Thesis

### Required Fields

```markdown
# Thesis: <COMPANY> (<TICKER>)
**Position:** Long / Short
**Entry Date:** YYYY-MM-DD
**Entry Price:** $X.XX
**Position Size:** X% of portfolio

## Core Thesis (1-2 sentences)
"Long ACME — margin expansion from pricing power + operating leverage as mix shifts to software"

## Key Pillars (3-5 supporting arguments)
1. [Pillar] — [Evidence] — Status: ✅ On Track / ⚠️ Watch / ❌ Broken
2. [Pillar] — [Evidence] — Status: ✅ / ⚠️ / ❌
3. [Pillar] — [Evidence] — Status: ✅ / ⚠️ / ❌

## Key Risks (3-5 thesis-killing scenarios)
1. [Risk] — Probability: Low/Med/High — Monitor: [how to detect]
2. [Risk] — Probability: Low/Med/High — Monitor: [how to detect]

## Catalysts
| Date | Event | Expected Impact | Status |
|------|-------|-----------------|--------|
| | | | Pending / Fired / Missed |

## Valuation
- Fair Value Estimate: $X–$Y
- Current Price: $Z
- Upside/Downside: +/-X%
- Exit Targets: T1 $X / T2 $X / T3 $X

## Conviction: High / Medium / Low
```

## Update Log

Every time new information arrives, append an entry:

```markdown
## Update Log

### YYYY-MM-DD — [Brief Title]
- **Data Point:** What changed (earnings beat, management departure, competitor move)
- **Pillar Impact:** Strengthens / Weakens / Neutralizes Pillar #X
- **Thesis Impact:** Intact / Challenged / Strengthened
- **Action:** No change / Add X% / Trim X% / Exit
- **Updated Conviction:** High / Medium / Low
- **Notes:** [context]
```

## Thesis Scorecard

Maintain a running scorecard (update with each new data point):

```markdown
## Scorecard

| Pillar | Original Expectation | Current Status | Trend | Last Updated |
|--------|---------------------|----------------|-------|-------------|
| Revenue growth >20% | On track | Q3 was 22% | ✅ Stable | 2026-05-15 |
| Margin expansion | Behind | Margins flat YoY | ⚠️ Concerning | 2026-05-15 |
| New product launch | Pending | Delayed to Q2 | ⚠️ Watch | 2026-05-15 |
```

## Falsifiability Check

A thesis MUST be falsifiable. For each thesis, define:

1. **What specific evidence would disprove this?** (not vague — concrete metrics)
2. **What is the time horizon?** (if nothing happens by X date, thesis is dead)
3. **What competitor action kills this?** (market share loss, price war, etc.)

If nothing could disprove the thesis, it's not a thesis — it's a hope.

## Portfolio Thesis Review

When reviewing all positions (`/invest thesis review`):

```markdown
# Portfolio Thesis Review — YYYY-MM-DD

| Ticker | Thesis Age | Conviction | Pillar Health | Next Catalyst | Action |
|--------|-----------|------------|---------------|---------------|--------|
| ACME | 4 months | High | 3/4 ✅ | Earnings 6/15 | Hold |
| XYZ | 8 months | Low | 1/3 ✅ | None near | Review for exit |

## Positions Needing Attention
- [TICKER]: [why — pillar broken, time decay, conviction drop]

## Thesis Kills Since Last Review
- [TICKER]: Exited on [date] because [specific trigger]
```

## Disconfirming Evidence Protocol

Track disconfirming evidence as rigorously as confirming:
- When you find bullish data: "Does this ACTUALLY support the thesis, or am I confirming my bias?"
- When you find bearish data: "Is this thesis-killing or temporary noise?"
- Rule: If 2+ pillars move to ⚠️ simultaneously, downgrade conviction to Low and set a time-bound review

## Integration with Other Workflows

- **After `/invest deep`**: Offer to create a thesis file
- **After `/invest earnings`**: Update the thesis with new data
- **During `/invest watchlist`**: Check thesis health for each position
- **During `/invest exit`**: Reference thesis kill triggers
- **During daily scan**: Flag news that impacts active theses
