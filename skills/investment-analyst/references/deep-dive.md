# Stock Deep Dive (`/invest deep <TICKER>`)

## Script Sequence

1. `alpaca_data.py snapshot <TICKER>` — real-time price + daily bar (US only; skip for EU tickers)
2. `market_data.py price <TICKER>` — valuation metrics & fundamentals (works for US + EU)
3. `market_data.py financials <TICKER>` — 3 statements
4. `market_data.py technicals <TICKER> 1y` — trend & momentum
5. `market_data.py recommendations <TICKER>` — Street consensus
6. `alpaca_data.py news <TICKER>` — latest headlines (US only; for EU use Exa/Tavily)
7. Exa search: `"<COMPANY> earnings outlook analyst"` (category: financial report)
8. Tavily search: `"<TICKER> risks catalysts 2025"` (time_range: month)

**For European tickers:** Use exchange suffix (e.g., `ASML.AS`, `RHM.DE`, `MC.PA`). Steps 1 and 6 require Alpaca (US-only); substitute with `market_data.py price` and Exa/Tavily news search. For filings, use Investegate (UK), Bundesanzeiger (DE), or AMF (FR) instead of SEC EDGAR.

## Output Format

```markdown
# Investment Analysis: <COMPANY> (<TICKER>)
Date: <today>

## Executive Summary
- Current Price: $X | Fair Value Estimate: $Y–$Z
- Rating: STRONG BUY / BUY / HOLD / SELL / STRONG SELL
- Confidence: High / Medium / Low

## Valuation
### Growth-Adjusted Assessment
- PEG ratio: X (Forward P/E ÷ EPS growth rate)
- Revenue acceleration: [accelerating / steady / decelerating]
- Verdict: ["Multiple justified by growth" or "Multiple stretched vs growth" — never flag P/E alone]

### DCF Model
- Revenue growth assumptions (3 scenarios)
- Terminal growth rate & WACC
- Implied share price range

### Relative Valuation
- P/E, P/S, EV/EBITDA vs peers
- Historical multiple range
- PEG ratio

## Fundamental Analysis
### Income Statement Trends
### Balance Sheet Health
### Cash Flow Quality
- FCF yield, capex intensity, working capital trends

## Technical Analysis
### Regime Classification
- **Current Regime:** Trending Up / Trending Down / Range-Bound / Transitioning
- **Evidence:** [price vs 50MA vs 200MA, higher highs/lows pattern, golden/death cross]
- **Implication:** [which indicator framework applies — trend-following vs mean-reversion]

### Trend & Levels
- Trend: Uptrend / Downtrend / Range-bound
- Key levels: Support $X, Resistance $Y
- Moving averages: 50/200 DMA positioning, golden/death cross status

### Momentum (interpreted within regime)
- RSI: X — [interpretation given the regime, e.g., "strong trend" not "overbought"]
- MACD: [signal line cross, histogram direction, divergence check]
- Volume: [confirmation or divergence from price action]
- **Bearish divergence check:** Does RSI make a lower high while price makes a higher high? [Yes/No]

## Moat & Competitive Position
- Sources of moat (network effects, switching costs, IP, scale, brand)
- Porter's Five Forces summary
- Threat assessment

## Risk Factors
- Bull case / Base case / Bear case with probabilities
- Key risks ranked by likelihood × impact
- Earnings quality flags

## Catalysts & Timeline
- Upcoming: earnings date, product launches, regulatory
- 3-month / 6-month / 12-month outlook

## Position Sizing Suggestion
- Based on conviction level and volatility (Kelly fraction simplified)

## Exit Plan
- T1 (sell 33%): $X — sector median multiple applied
- T2 (sell 33%): $X — premium peer multiple applied
- T3 (trail 34%): $X — 15% trailing stop
- Thesis Kill Triggers: [2 specific scenarios that disprove the thesis]
- Time Limit: 12 months without catalyst progression
- Weekly Watch: [3 key indicators to monitor]
```
