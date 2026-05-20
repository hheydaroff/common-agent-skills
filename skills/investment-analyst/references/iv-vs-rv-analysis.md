# Implied vs Realized Volatility Analysis

Assess whether options are cheap or expensive before recommending strategies. The vol premium (IV - RV) is the key metric.

## When to Use

- Before any options strategy recommendation in `/invest options`
- When user asks "are options cheap/expensive for X?"
- As a pre-check before earnings plays
- When deciding between shares vs. options for a trade

## Core Concept

**Vol Premium = Implied Volatility - Realized Volatility**

- **Positive premium (IV > RV)**: Options are "rich" — favor selling strategies (covered calls, iron condors, credit spreads)
- **Negative premium (IV < RV)**: Options are "cheap" — favor buying strategies (long calls/puts, debit spreads, straddles)
- **Near zero**: Fairly priced — strategy choice based on directional view, not vol view

## Data Collection

### Step 1: Get Current IV

```bash
# From Alpaca (preferred — includes Greeks)
uv run --with alpaca-py --with pandas python3 scripts/alpaca_data.py options_chain <TICKER>

# From yfinance (fallback)
uv run --with yfinance --with pandas --with numpy python3 scripts/market_data.py options <TICKER>
```

Extract ATM implied volatility for nearest monthly expiry.

### Step 2: Compute Realized Volatility

```bash
# Get 6 months of daily history
uv run --with yfinance --with pandas --with numpy python3 scripts/market_data.py history <TICKER> 6mo
```

Calculate close-to-close realized vol over multiple windows:
- **20-day RV** — compare to 1-month IV (short-term)
- **60-day RV** — compare to 3-month IV (medium-term)
- **90-day RV** — compare to 6-month IV (if available)

Formula: `RV = StdDev(daily log returns) × √252 × 100`

### Step 3: IV Percentile (Context)

Where is current IV relative to its own history?
- **IV Percentile > 80%**: IV is historically high → options expensive
- **IV Percentile 20-80%**: Normal range
- **IV Percentile < 20%**: IV is historically low → options cheap

Use 1-year lookback for IV percentile calculation.

## Output Format

```markdown
## Volatility Assessment: <TICKER>

| Window | Realized Vol | Implied Vol (matching) | Premium (IV-RV) | Signal |
|--------|-------------|------------------------|-----------------|--------|
| 20-day | X.X% | 1M ATM: X.X% | +/-X.X% | Rich / Cheap / Fair |
| 60-day | X.X% | 3M ATM: X.X% | +/-X.X% | Rich / Cheap / Fair |
| 90-day | X.X% | 6M ATM: X.X% | +/-X.X% | Rich / Cheap / Fair |

**IV Percentile (1Y):** X% — [Historically Low / Normal / Historically High]

### Vol Regime: [Low Vol / Normal / Elevated / Crisis]
### Trend: [Compressing / Stable / Expanding]
```

## Strategy Implications

| Vol Regime | Recommended Strategies | Avoid |
|-----------|----------------------|-------|
| IV >> RV (rich, >5% premium) | Covered calls, iron condors, credit spreads, short strangles | Long options, debit spreads |
| IV ≈ RV (fair, ±3%) | Directional strategies — pick based on view | Large premium plays either way |
| IV << RV (cheap, >5% discount) | Long calls/puts, debit spreads, straddles, calendars (long vega) | Selling naked premium |
| Pre-earnings spike | Avoid unless sizing for binary; consider post-earnings vol crush plays | Buying expensive ATM options |
| Post-earnings crush | Sell remaining elevated vol if no follow-through expected | Buying right after earnings |

## Pre-Earnings Vol Check

Before any earnings options play:

1. **Current IV vs 20-day RV**: How much "earnings premium" is baked in?
2. **Historical earnings moves**: Average absolute move over last 4-8 quarters
3. **Options-implied move**: Straddle price ÷ stock price for nearest weekly expiry
4. **Compare**: If implied move > average actual move → options expensive for earnings

```markdown
### Earnings Vol Setup
- Implied move (from straddle): ±X.X%
- Average actual move (last 8 Qs): ±X.X%
- Ratio: X.Xx — [Options pricing MORE / LESS move than typical]
- Recommendation: [Sell premium / Buy premium / Avoid]
```

## Integration

Run BEFORE any §2 options strategy. If options are expensive, bias toward selling strategies even with a bullish view. **Never recommend buying options when IV >> RV without explicitly flagging the vol headwind.**
