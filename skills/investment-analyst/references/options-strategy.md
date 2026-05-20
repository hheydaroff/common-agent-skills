# Options Strategy (`/invest options <TICKER> <VIEW>`)

Views: bullish, bearish, neutral, volatile, income

## Script Sequence

1. `alpaca_data.py snapshot <TICKER>` — real-time price
2. `alpaca_data.py options_chain <TICKER>` — full chain with Greeks (preferred)
3. `market_data.py options <TICKER>` — fallback if Alpaca options unavailable
4. `market_data.py technicals <TICKER> 3mo` — near-term trend
5. `alpaca_data.py bars <TICKER> 1Day 6mo` — daily bars for historical vol calc

## Analysis & Recommendation

- Strategy selection (vertical spread, iron condor, PMCC, straddle, covered call, etc.)
- Strike selection rationale
- Max profit / max loss / breakeven
- Probability of profit (based on IV and historical moves)
- Greeks exposure (delta, theta, vega, gamma)
- Entry timing and exit rules
- Position sizing (max % of portfolio at risk)
