# Leveraged Certificate Entry Framework

A data-validated system for timing entries on **Factor Certificates** (Faktor-Optionsscheine) and **Knock-Out Certificates** (Turbos) — leveraged structured products common on European brokers (Trade Republic, Scalable Capital, comdirect, DEGIRO). Also covers US options via IBKR.

Two complementary approaches:
1. **Oversold Bounce (3-Signal System)** — timing entries on beaten-down stocks with intact theses
2. **Catalyst-Event Trades** — binary event plays with known dates (earnings, summits, regulation)

## The Problem

Factor certificates amplify daily moves (2x–8x). A correct thesis with wrong timing = total loss:
- Stock drops -10% after entry → 4x certificate drops -40% → stopped out
- Stock eventually recovers +30% over 2 months → but your certificate is dead

**You need to be right on DIRECTION and TIMING simultaneously.**

## The 3-Signal Entry System

Backtested on 15 diverse stocks that hit RSI < 30 during 2025:

| # | Signal | What It Does | Where to Check |
|---|--------|-------------|----------------|
| 1 | **RSI < 30** | Identifies oversold candidates | TradingView → RSI(14) indicator |
| 2 | **MACD histogram turns positive** | Confirms momentum is turning UP | TradingView → MACD indicator |
| 3 | **S&P 500 above 50-day MA** | Confirms market isn't in crash mode | TradingView → SPY with 50 MA |

### Plus: Thesis filter (always applied first)

Before any technical signal matters, ask: **"Did the PRICE break, or did the BUSINESS break?"**

- Price broke (sector rotation, macro fear, profit-taking) → proceed with signals
- Business broke (CEO fraud, margin collapse, regulatory destruction) → walk away regardless of RSI

## Backtest Results (15 stocks, 2025)

### With all 3 signals + thesis filter:

| Metric | SPY > 50MA (healthy market) | SPY < 50MA (stressed market) |
|--------|---------------------------|------------------------------|
| Trades | 7 | 8 |
| **Survived -40% stop** | **7/7 (100%)** | 7/8 (87%) |
| **Win rate** | **71%** | 50% (coin flip) |
| **Avg 4x return (10 days)** | **+8.3%** | -2.1% (negative) |
| Worst 4x dip | -19.6% | -75.5% |

### Without market filter (MACD only):

| Metric | Result |
|--------|--------|
| Survival rate | 93% (14/15) |
| Win rate | 60% |
| Avg 4x return | +2.8% |

### Without MACD (RSI entry only):

Buying at RSI < 30 directly (no timing confirmation):
- TSLA: -38.6% drawdown before recovery → 4x certificate = wiped out
- Multiple stocks continued falling 10-20% after RSI < 30 signal

**Conclusion: MACD confirmation is essential. Market filter doubles the win rate and eliminates the worst losses.**

## Decision Tree

```
Stock drops hard →
│
├─ RSI < 30? ──── No → Not oversold enough. Ignore.
│    │
│    Yes
│    │
├─ Thesis intact? ── No → Walk away. (NKE margins collapsed, UNH CEO killed + DOJ)
│    │
│    Yes (price broke, business fine)
│    │
├─ SPY > 50-day MA? ── No → Buy STOCK only. No certificates.
│    │                        (Market gravity will drag you down even if stock is fine)
│    Yes
│    │
├─ MACD histogram > 0? ── No → WAIT. Check daily until it flips.
│    │
│    Yes (all 3 signals confirmed)
│    │
└─ ✅ ENTER CERTIFICATE
      → 4x leverage (default; 3x if uncertain, 6x only with very strong catalyst)
      → Max position: 1% of portfolio or €50-100
      → Hold limit: 10 trading days
      → Stop loss: -40% on certificate value
      → Take profit: +60-80%
```

## Why Each Signal Matters

### Signal 1: RSI < 30 (Candidate Identification)

RSI measures "how fast has this stock dropped recently" on a 0-100 scale:
- < 30 = sold off too fast, like a rubber band stretched → likely to snap back
- 30-70 = normal range
- > 70 = risen too fast → likely to pull back

**RSI < 30 alone is NOT a buy signal.** It only identifies candidates. Without thesis + timing filters, buying every RSI < 30 stock produces barely-positive returns (2025 backtest: average +2.8% at 4x, 60% win rate — not worth the risk).

### Signal 2: MACD Histogram Positive (Timing)

MACD (Moving Average Convergence Divergence) histogram measures momentum direction:
- Histogram crosses from negative to positive = selling pressure exhausted, buyers stepping in
- This is your "the bounce has STARTED" confirmation

**Why it matters for certificates:** Without MACD, you're catching a falling knife. TSLA dropped -38.6% AFTER hitting RSI < 30. MACD didn't turn positive until 28 days later, at the actual bottom. Entering at MACD confirmation = +78.7% at 4x in 10 days vs entering at RSI signal = wiped out.

**The tradeoff:** You "miss" the first few percent of the bounce by waiting. But you avoid the -20% to -40% drawdowns that kill leveraged positions. For certificates, timing matters more than catching the exact bottom.

### Signal 3: S&P 500 > 50-day MA (Market Health)

The overall market acts as gravity on individual stocks:
- SPY above 50MA = market in uptrend → individual bounces have "wind at their back"
- SPY below 50MA = market in downtrend → even good stocks get dragged down by macro

**The data is stark:**
- Market healthy: 100% survival, 71% win rate, +8.3% avg return
- Market sick: 87% survival, 50% win rate, -2.1% avg return (negative!)

**When SPY is below 50MA:** Do NOT use leveraged certificates. Buy the stock instead (can hold through storms). The April 2025 tariff crash demonstrated this — AMZN had perfect stock-level signals but the macro tsunami destroyed the trade.

## Product Selection Guide

European brokers offer Factor Certificates in 2x, 3x, 4x, 6x, 8x (availability varies by underlying):

| Factor | Use When | Max Hold | Stop Loss |
|--------|----------|----------|-----------|
| 2x | Learning / low conviction | 2-3 weeks | -50% |
| 3x | Moderate conviction, uncertain timing | 2 weeks | -45% |
| **4x** | **Default for confirmed setups** | **10 days** | **-40%** |
| 6x | Strong catalyst confirmed (earnings beat, deal news) | 5 days | -35% |
| 8x | Parabolic momentum, in-and-out same week | 3 days | -25% |

**Default to 4x.** Only upgrade to 6x/8x when a specific near-term catalyst adds urgency.

## Risk Management Rules

1. **Position size:** Never exceed 1% of total portfolio per certificate trade
2. **Max concurrent:** 2 leveraged positions maximum (prevents correlation blowup)
3. **Time limit:** Close by Day 10 regardless (volatility decay eats certificates over time)
4. **Stop loss:** Non-negotiable. If certificate hits -40%, exit. No exceptions.
5. **Profit rotation:** When trade wins, move 80% of profits to core ETFs. Keep 20% for next trade.
6. **Never average down:** If the certificate drops, that's the thesis failing in real-time. Cut it.

## Volatility Decay Warning

Factor certificates reset daily. In sideways markets, this creates decay:

```
Day 1: Stock +5%  → 4x cert: €100 → €120
Day 2: Stock -5%  → 4x cert: €120 → €96
Net: Stock at 99.75%. Certificate lost 4%.
```

This is why holding periods must be SHORT and the stock must be TRENDING (not choppy). The MACD confirmation helps ensure you're entering a trend, not a chop zone.

## When NOT to Use This System

- **Market below 50-day MA** → buy stocks, not certificates
- **Stock has thesis problems** → no amount of technical signals saves a broken business
- **Earnings within 3 days** → binary event can gap against you regardless of signals
- **Position would exceed 1% of portfolio** → reduce size, never increase it
- **You're emotionally tilted from a recent loss** → skip one cycle, reset

## Integration with Investment Workflow

This framework plugs into the broader investment process:

1. **Daily Scan** identifies stocks hitting RSI < 30
2. **Thesis assessment** (from deep dive, watchlist research) determines if business is intact
3. **This framework** determines IF and WHEN to enter a leveraged position
4. **Exit Strategy** framework determines when to close
5. **Profit Waterfall** routes wins back to core portfolio

The certificate trade is a short-term tactical overlay on a long-term strategic thesis. You can (and should) hold the STOCK in your active portfolio AND run a certificate trade on the same name — they serve different purposes with different time horizons.

## Tax Note (Germany)

Factor certificates are taxed as **Kapitalerträge** (26.375% Abgeltungssteuer including Soli). No 12-month tax-free holding period applies (unlike Xetra-Gold 4GLD.DE or crypto). Losses can offset other capital gains within the same year, capped at €20,000 annual deduction for derivatives (since 2021).

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│  CERTIFICATE ENTRY CHECKLIST (Oversold Bounce)  │
│                                                 │
│  □ RSI < 30          (stock is oversold)        │
│  □ Thesis intact     (business fine, price not) │
│  □ SPY > 50-day MA   (market healthy)           │
│  □ MACD histogram >0 (momentum confirmed)       │
│                                                 │
│  ALL FOUR = GO. Any missing = WAIT or NO.       │
│                                                 │
│  Entry: 4x factor certificate, max €50-100      │
│  Stop: -40%  |  Target: +60-80%  |  Max: 10d   │
└─────────────────────────────────────────────────┘
```

---

# Part 2: Catalyst-Event Trades

How to structure leveraged derivative trades (knock-out certificates, turbos, options) for **catalyst-driven** short-term plays with small capital (€100–€1000).

## When to Use This (Instead of 3-Signal System)

- A clear catalyst with a **known date** (earnings, summit, regulation decision, product launch)
- Asymmetric setup: binary outcome where upside > downside probability
- Small capital where shares alone won't move the needle
- Timeframe: 1 day to 4 weeks
- RSI may NOT be < 30 — stock may be range-bound waiting for the event

## The Catalyst Analysis Sequence

### Step 1: Identify the Catalyst & Direct Beneficiaries

Ask: "What specific company gets a CONCRETE outcome from this event?"

Rank by directness:
1. **Primary:** Company with tangible deal/order/contract on the table
2. **Secondary:** Sector/basket that benefits from sentiment shift
3. **Tertiary:** Leveraged proxy (3x ETFs, indices)

Prefer primary. Only go secondary/tertiary if primary is already priced in.

### Step 2: Technical Setup Check (per candidate)

Run for each candidate and **eliminate** those that fail:

| Check | Tool | Pass Criteria | Fail = Skip |
|-------|------|---------------|-------------|
| RSI | `technicals <TICKER> 3mo` | < 70 (not overbought) | RSI > 70 = rally already happened |
| MACD | Same | Bullish or neutral | Bearish + diverging = don't fight it |
| Position vs MAs | Same | Above 20MA preferred | Below both MAs = weak, needs reversal first |
| Recent move | 20d/60d return | < +15% in 20d | Already ripped = you're late |
| Volume | Same | At or above average | Low volume breakout = unreliable |
| Distance to resistance | Support/resistance | Room to run (>5% to resistance) | Sitting at multi-year high = crowded |

**Best setup:** RSI 45-65, MACD bullish, above 20MA, recent pullback (-5% to -15% over 60d), approaching but NOT at resistance.

### Step 3: Valuation Sanity Check

Don't buy leveraged exposure to something that's already expensive:

| Metric | Acceptable Range | Why |
|--------|-----------------|-----|
| Forward P/E | < sector median × 1.5 | Overvalued stocks have less upside |
| 52-week position | Not within 5% of 52w high | Near ATH = limited catalyst upside |
| Analyst targets | Current price < median target | Street still sees upside |

### Step 4: Select the Instrument

#### For Knock-Out Certificates (Trade Republic, DEGIRO, Flatex, Scalable):

| Parameter | Guideline |
|-----------|----------|
| Direction | Long (Bull) for bullish catalyst |
| KO level | 8-12% below current price (balance: leverage vs. safety) |
| Leverage | 8-15x for catalyst trades (not higher) |
| Type | Open-End preferred (no time decay) |
| Ratio | Note it — typically 0.1 (10:1) for US stocks |
| Issuer | HSBC, Société Générale, Goldman (most liquid) |

**KO level guidelines:**

| Buffer % | Leverage | Use When |
|----------|----------|----------|
| 5-7% | 15-20x | Very high conviction, tight stop, known date |
| 8-12% | 8-15x | Standard catalyst trade (RECOMMENDED) |
| 12-18% | 5-8x | Longer hold, uncertain timing |
| 20%+ | 3-5x | Might as well buy shares |

**KO level must be:**
- Below the 20-day low (minimum)
- Below the nearest technical support level
- At a level that would require a genuine trend reversal, not just noise

#### For US Options (IBKR):

| Expiry | Use When |
|--------|----------|
| 7-14 DTE | Binary catalyst with known date, maximum leverage |
| 21-30 DTE | Catalyst + potential follow-through period |
| 45-60 DTE | Thesis plays where timing is uncertain |

**Strike selection:**
- **Slightly OTM (5-10% above current):** Best risk/reward for catalyst trades
- **ATM:** Higher probability but more expensive
- **Deep OTM (>15%):** Lottery ticket only, low probability

**Checklist before buying:**
- [ ] Open Interest > 500 (liquidity)
- [ ] Bid-ask spread < 20% of mid price
- [ ] IV not at 52-week highs (expensive premium)

### Step 5: Position Sizing & Portfolio Construction

#### Budget Allocation (for small accounts €100-€1000):

| # of positions | Allocation | When |
|----------------|-----------|------|
| 1 (concentrated) | 100% | Single obvious catalyst, very high conviction |
| 2 (barbell) | 60-70% primary + 30-40% secondary | Recommended default |
| 3+ (diversified) | Equal weight | Multiple uncorrelated catalysts |

**The Barbell Rule:** Put the majority on your highest-conviction direct beneficiary. Add a smaller position on the most beaten-down reversion candidate.

#### Sizing Math for KO Certificates:

```
Certificate price ≈ (Current price - KO level) / Ratio
# Example: BA at $235, KO at $215, ratio 0.1
# Cert price = ($235 - $215) × 0.1 = €2.00 (adjust for EUR/USD)

Number of certs = Budget / Cert price
# €130 / €1.85 = ~70 certificates

Profit if target hit = (Target - Current) × Certs × Ratio  
# ($260 - $235) × 70 × 0.1 = $175 ≈ €150
```

### Step 6: Scenario Table (MANDATORY)

Every catalyst trade needs this before entry:

```markdown
| Scenario | Probability | Underlying Price | P&L | Return |
|----------|-------------|-----------------|-----|--------|
| Bull (deal announced) | X% | $XXX | +€XXX | +XXX% |
| Base (positive tone, no deal) | X% | $XXX | +/-€XX | +/-XX% |
| Neutral (nothing burger) | X% | $XXX | -€XX | -XX% |
| Bear (negative surprise) | X% | $XXX | -€XXX | -100% |
```

**Expected value = Σ (probability × P&L)**

Only enter if EV is positive AND the bull case offers **>3:1** reward vs. the base case loss.

### Step 7: Exit Rules (Pre-commit)

| Trigger | Action | Timing |
|---------|--------|--------|
| Target hit (+80-150%) | Sell 50-100% | Immediately on the spike |
| Catalyst delivered, positive | Sell half, trail rest | Within hours of announcement |
| Catalyst day passes, no news | **Sell everything** | End of catalyst day |
| Underlying drops to within 3% of KO | Sell manually | Immediately (save 30% vs. KO) |
| 3+ days after catalyst, flat | Sell | Don't hold waiting |

**Critical rule for dated catalysts:** If the event produces nothing by EOD of the event, EXIT. Don't hope for "delayed reaction." The trade is over.

---

## Anti-Patterns (Both Approaches)

| Mistake | Why It Fails |
|---------|-------------|
| KO too tight (< 5% buffer) | Normal volatility knocks you out before catalyst |
| Buying AFTER +10% move on the news | You're buying someone else's profit-taking |
| Holding past the catalyst date | Theta/time kills you; the edge was the event |
| All-in on one certificate | One gap-down = total wipeout |
| Ignoring RSI > 70 | "Already overbought" means the easy money is gone |
| Choosing highest leverage available | 30x+ leverage = 3% noise kills you |
| No exit plan written down | You'll freeze during volatility and make emotional decisions |
| Averaging down on a certificate | If it's dropping, that's the thesis failing in real-time |
| Holding factor certs >10 days | Volatility decay eats returns in sideways markets |
| Using certs when SPY < 50MA | 50% win rate with negative returns — not worth the risk |

---

## Platform-Specific Notes

### Trade Republic / Scalable Capital
- Search: Underlying → Derivate → Knock-Out → Long (for KO) or Faktor (for factor certs)
- Sort by Hebel (leverage) or KO-Schwelle (knock-out level)
- Prefer Open-End (no expiry) for KO certificates
- Fee: €1 per trade (negligible on €100+ positions)
- Issuers: HSBC, SocGen, Goldman, Citi — all fine for liquidity

### DEGIRO
- Similar selection under "Turbo's" or "Sprinters"
- May have wider spreads than Trade Republic

### Interactive Brokers (IBKR)
- Full US options chain access
- Better for precise strike/expiry selection
- Commission: ~$0.65/contract (cheapest for US options from Europe)

### Comparison: KO Certs vs. Factor Certs vs. US Options

| Feature | KO Certificates | Factor Certificates | US Options |
|---------|----------------|--------------------|-----------|
| Time decay | None (open-end) | Volatility decay (daily reset) | Yes (theta) |
| Leverage control | Fixed by KO level | Fixed factor (2x-8x) | Varies by strike/expiry |
| Max loss | 100% (KO event) | 100% (gradual or stop) | 100% of premium |
| Best timeframe | 1-14 day catalysts | 3-10 day trends | 14-60 day thesis trades |
| Risk of total wipe | Gap through KO = instant | Slow bleed if wrong | Expiry worthless |
| European access | Easy (any broker) | Easy (any broker) | Requires IBKR or similar |
| Holding cost | ~0.01-0.03€/day | Implicit in daily reset | None (paid upfront) |
| Best for | Event-driven with known date | Oversold bounce with confirmed momentum | Longer thesis plays |
