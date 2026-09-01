# Technical Signal Interpretation Guide

Interpret technical indicators **contextually** based on market regime. The same signal means different things in different environments.

## Step 0: Identify the Regime FIRST

Before interpreting any technical signal, classify the regime:

| Regime | How to Identify | Indicator Toolkit |
|--------|----------------|-------------------|
| **Trending Up** | Price > 50MA > 200MA, golden cross, higher highs/lows | Trend-following: ride momentum, buy dips to MAs |
| **Trending Down** | Price < 50MA < 200MA, death cross, lower highs/lows | Mean-reversion on bounces, or stay out |
| **Range-Bound** | Price oscillating between support/resistance, MAs flat/intertwined | Mean-reversion: sell overbought, buy oversold |
| **Transitioning** | Cross of MAs happening, breakout from range, regime change underway | Wait for confirmation, reduce size |

**Rule: State the regime explicitly before interpreting any oscillator or price signal.**

---

## RSI Interpretation by Regime

### In Uptrends (Trending Up)

| RSI Reading | Meaning | Action |
|-------------|---------|--------|
| > 70 | **Description of strength**, not a sell signal | Hold. Trail stop. Do NOT sell just because RSI is high. |
| 50–70 | Healthy trend, normal state | Continue holding, add on dips |
| 40–50 | Pullback within trend — potential entry | Buy opportunity if thesis intact |
| < 40 | Unusual weakness — check if trend is breaking | Reduce if 50MA breaks, otherwise hold |

**Key insight:** In strong secular uptrends, RSI can remain > 70 for weeks or months. NVIDIA stayed "overbought" through most of 2023-2024 and kept running. Selling at RSI 70 in a trending market is the most expensive mistake in technical analysis.

**The ONLY bearish RSI signal in an uptrend:** Bearish divergence — price makes a new high but RSI makes a LOWER high. This suggests momentum is fading. Even then, it's a "watch" signal, not a sell signal, until price confirms by breaking below support.

### In Downtrends (Trending Down)

| RSI Reading | Meaning | Action |
|-------------|---------|--------|
| > 60 | Oversold bounce — potential short entry | Fade the rally if trend structure intact |
| 30–50 | Normal state in downtrend | Stay short or stay out |
| < 30 | Extreme selling — watch for reversal signals | Only buy with MACD confirmation + thesis intact |

### In Range-Bound Markets

| RSI Reading | Meaning | Action |
|-------------|---------|--------|
| > 70 | Near top of range — mean-reversion likely | Trim or hedge at resistance |
| 30–70 | Mid-range, no edge | Wait |
| < 30 | Near bottom of range — mean-reversion likely | Buy at support |

**Key insight:** RSI mean-reversion strategies ONLY work reliably in range-bound markets. Applying them in trending markets produces systematic losses.

---

## 52-Week High Interpretation

### Academic Evidence (George & Hwang, 2004)

> "Stocks with the highest ratios of current price to 52-week high outperform those with the lowest ratios over the subsequent 6-12 months."

> "Future returns based on 52-week high do NOT reverse in the long run, unlike reversals observed in many momentum studies."

### Interpretation Rules

| Context | 52-Week High Means | Action |
|---------|-------------------|--------|
| **Earnings growth accelerating + secular theme** | Breakout — new range forming | Bullish. Hold or add on pullbacks. |
| **Growth decelerating + multiple expanding** | Euphoria risk — check if deserved | Caution. Verify PEG and growth trajectory. |
| **ETF in strong sector rotation** | Sector momentum intact | Hold until rotation reverses. |
| **Low volume breakout, no fundamental catalyst** | Suspect — needs confirmation | Wait for volume or earnings proof. |

**Default stance:** 52-week high with fundamental support = BULLISH until proven otherwise. The burden of proof is on the bear case.

---

## Volume Interpretation

| Signal | In Trending Market | In Range-Bound Market |
|--------|-------------------|----------------------|
| Rising volume + rising price | Trend confirmation — strong | Breakout attempt — watch for follow-through |
| Declining volume + rising price | Normal consolidation (uptrend); distribution risk (range) | Weak rally — likely to fail |
| Rising volume + falling price | Selling climax (potentially bullish if at support) | Breakdown |
| Declining volume + falling price | Orderly pullback — healthy | Declining interest |

**ETF vs. Individual Stock:** Volume patterns in ETFs are less reliable than in individual stocks. ETF volume is driven by creation/redemption and arbitrage, not pure buyer/seller conviction. Weight volume signals lower for ETF analysis.

---

## Price Level Map (Pivot Zones + Fibonacci)

Run `market_data.py levels <TICKER> [period]` for a mechanical map: pivot-based support/resistance zones (fractal pivots clustered within 1.5%, touch-counted) and Fibonacci retracements of the period's major swing.

**Framing rule: levels are context zones, NOT signals.**

| Use | How |
|-----|-----|
| Place T1/T2/T3 exit targets | Anchor at nearby resistance zones, not round numbers guessed from thin air |
| Place stops / kill levels | Below the nearest multi-touch support zone, not at an arbitrary % |
| Judge pullback depth | 38.2–50% retrace of the major swing = normal pullback; > 61.8% = structure at risk |
| Size reactions | A bounce AT a zone still needs regime + volume confirmation before it means anything |

**Rules:**
1. Zones with more touches matter more than single-pivot levels.
2. The regime (Step 0) decides how a level behaves — in downtrends support zones get cut, in uptrends they hold. Never quote a level without the regime.
3. Fibonacci levels have no independent predictive evidence; use them only as widely-watched convergence points where other traders may act.
4. A level never overrides a kill trigger. Thesis kill conditions are fundamental; levels are geometry.

---

## Growth-Adjusted Valuation Gate

Before flagging a "high P/E" as a concern, run this check:

```
1. Calculate PEG ratio = Forward P/E ÷ Expected EPS growth rate
2. Check revenue acceleration: Is YoY revenue growth increasing quarter over quarter?
3. Compare to sector — is this premium justified by superior growth?
```

| PEG | Interpretation |
|-----|---------------|
| < 1.0 | Cheap relative to growth — P/E is NOT a concern |
| 1.0–2.0 | Fair — P/E is context-appropriate, not a flag |
| 2.0–3.0 | Getting expensive — mention as moderate concern |
| > 3.0 | Genuinely expensive — flag as significant concern |

**Rule:** Never flag "P/E is X" as a standalone concern without growth context. Always present it as P/E relative to growth (PEG) and relative to sector peers.

---

## The One-Liner

> "The most common mistake is confusing the speedometer for the brake pedal. RSI tells you how fast you're going — it doesn't tell you to stop."

---

## Common Biases to Avoid

| Bias | What It Looks Like | The Fix |
|------|-------------------|---------|
| **Mean-Reversion in Trends** | "RSI 78, overbought, due for pullback" in a secular uptrend | Identify regime first. In trends, overbought = strong. |
| **Anchoring to 52-Wk High** | "At all-time high, stretched" without checking fundamentals | 52-wk high + growth = bullish per George & Hwang (2004). |
| **Conservatism Bias** | Failing to update thesis when growth data contradicts "expensive" | When new data arrives, revise aggressively. Growth changes everything. |
| **Regime Blindness** | Using one toolkit for all market conditions | State regime → apply appropriate framework. |
| **Ignoring Trend Persistence** | "It's gone up X% in Y days, must reverse" | Momentum factor is among the most robust in finance. Trends persist longer than expected. |

---

## Integration With Other Workflows

- **Stock Deep Dive:** Regime identification goes BEFORE technical analysis interpretation
- **Exit Strategy:** RSI divergence matters; RSI level alone does not trigger exits in trends
- **Certificate Entry:** RSI < 30 + MACD + market filter already regime-aware (good)
- **Watchlist Check:** "Technical: Improving/Stable/Deteriorating" must be regime-contextualized
- **Bear Case Research:** High RSI is NOT a bear case unless accompanied by divergence + fundamental deterioration
- **Exit Strategy / Levels:** Anchor T1/T2/T3 and stops on `levels` pivot zones; see Price Level Map above
