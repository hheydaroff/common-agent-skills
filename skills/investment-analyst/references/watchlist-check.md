# Watchlist Check (`/invest watchlist`)

For a user-provided watchlist or theme, run a systematic check.

## Process

### 1. For each ticker on the watchlist:

- `market_data.py price <TICKER>` — current valuation snapshot
- `market_data.py technicals <TICKER> 6mo` — trend and momentum
- `market_data.py recommendations <TICKER>` — analyst sentiment changes

### 2. Cross-reference with triggers:

- Has anything changed since last check? (price breakout, volume surge, analyst upgrade)
- Any new catalysts? (Exa search for recent news on each ticker)
- Any red flags triggered? (earnings miss, dilution, regulatory setback)

### 3. Score each position:

- Technical: Improving / Stable / Deteriorating
- Fundamental: Accelerating / Steady / Decelerating
- Catalyst proximity: Near-term / Medium-term / Distant
- Exit signals: None / Approaching T1 / Thesis challenged / Time decay
- Action: Add / Hold / Trim / Exit

## Output Format

```markdown
# Watchlist Check — <DATE>

| Ticker | Price | Δ Since Last | Technical | Fundamental | Next Catalyst | Exit Signal | Action |
|--------|-------|-------------|-----------|-------------|---------------|-------------|--------|

## Exit Alerts
- [Any positions approaching T1/T2/T3 targets]
- [Any thesis kill triggers approaching]
- [Any time decay positions (>9 months, flat)]
- [Any positions exceeding size limits]

## Alerts
- [Any triggered thresholds, unusual volume, news events]

## Theme Health
- Is the overall thesis still intact?
- Any macro/regime changes that affect the basket?
```
