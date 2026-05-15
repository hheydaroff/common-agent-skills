# Short-Term Tactical Trading Framework

Capture 8-15%+ moves within 1-7 days using shares (primary) or leveraged certificates (when setup is exceptional). Designed to clear the 26.375% German Abgeltungssteuer and still deliver meaningful net gains.

## The Math Floor — Minimum Viable Trade

Before entering ANY short-term trade, verify it clears the floor:

```
Net gain = (Position × Expected Move × Leverage) × (1 - 0.26375) - Trading Costs

Minimum: Net gain > €50 for it to be worth your attention and risk.
```

| Position Size | Min Underlying Move (Shares) | Min Move (4x Cert) | Min Move (10x KO) |
|---------------|-----------------------------|--------------------|-------------------|
| €500 | 15% (€75 gross → €55 net) | 4% (€80 → €59) | 2% (€100 → €74) |
| €1,000 | 8% (€80 → €59) | 3% (€120 → €88) | 1.5% (€150 → €110) |
| €2,000 | 5% (€100 → €74) | 2% (€160 → €118) | 1% (€200 → €147) |
| €3,000 | 4% (€120 → €88) | 1.5% (€180 → €132) | 1% (€300 → €221) |

**Default instrument: SHARES.** Use certs only when: (a) conviction is very high, (b) time stop is ≤ 5 days, (c) stop loss is clear and tight.

---

## Five Trade Types

### Type 1: Breakout Momentum (Hold 3-7 days)

**What it is:** Stock compresses into a tight range for 2-4+ weeks, then explodes out on volume. You ride the expansion.

**Setup criteria:**
- Price consolidated for ≥ 14 days (ADX < 20, or Bollinger Band width in bottom 20th percentile of last 6 months)
- Volume on breakout day ≥ 2x the 20-day average
- Price closes above the upper boundary of the consolidation range
- RSI 55-70 (momentum starting, not exhausted)
- No earnings within 5 trading days

**Entry:** Buy the breakout close OR the first intraday pullback to the breakout level (now support). Do NOT chase if already >3% above breakout level.

**Target:** Measured move = width of consolidation range added to breakout point. Example: stock traded $48-$52 for 3 weeks, breaks above $52 → target $56.

**Stop:** Below the consolidation range midpoint. If stock traded $48-$52, stop at $50. Never more than -5% from entry.

**Time stop:** Exit by day 7 regardless of P&L. If the breakout hasn't followed through by then, it's failed.

**Best instrument:** Shares for most. 4x factor cert if the consolidation was very tight (>3 weeks) and the measured move is only 5-6% (amplified to 20-24%).

**Why it works:** Compressed volatility = institutional accumulation phase. The breakout on volume = institutions revealing their hand. Continuation follows because momentum buyers pile in for 3-7 days.

---

### Type 2: Earnings Gap Continuation (Hold 1-5 days)

**What it is:** Company beats estimates significantly, stock gaps up 5%+. You buy the gap and ride continuation as the market reprices.

**Setup criteria:**
- EPS beat ≥ 10% above consensus (the bigger the better)
- Revenue beat AND raised guidance (both, not just one)
- Gap up ≥ 5% on ≥ 3x average volume
- Stock was NOT already extended (should not have been >15% above 50MA pre-earnings)
- Post-gap RSI < 80 (still room to run)

**Entry:** NOT the open. Wait for the first 30-60 min pullback on the gap day, or buy the close of gap day. The opening 30 minutes is noise and market makers repricing.

**Target:** +8-15% from the gap close within 5 trading days. Historical studies show strong earnings gaps (beat + raise + volume) continue in the gap direction ~65% of the time over the next week.

**Stop:** Below the gap fill level (the pre-earnings close). If the gap fills completely on day 1-2, the reaction is negative despite the beat — exit immediately.

**Time stop:** Exit by day 5. The earnings repricing cycle is 3-5 days (analyst revisions, fund rebalancing, retail discovery). After that, edge dissipates.

**Best instrument:** Shares. Gaps are volatile — leveraged instruments can get stopped out intraday even when the trade is correct.

**Why it works:** Information diffusion lag. Not everyone processes the earnings on day 1. Analyst upgrades come 1-3 days later. Passive fund rebalancing takes days. Each wave creates new buying pressure.

---

### Type 3: Sector Rotation Catch (Hold 1-3 days)

**What it is:** A macro event creates sudden sector demand. The sector ETF moves first, but the highest-beta single names lag by hours to days. You buy the laggard within the winning sector.

**Setup criteria:**
- Clear macro/geopolitical catalyst (policy announcement, regulation, conflict, data release)
- Sector ETF moves ≥ 2% on the day, on above-average volume
- Identify 2-3 single names within that sector that are flat or lagging vs the ETF move
- The lagging names have no stock-specific negative news (they're just slow, not broken)
- The lagging names have higher beta or more direct exposure to the catalyst

**Entry:** Buy the laggard same day or next morning. The spread between the sector ETF move and the single name = your expected catchup.

**Target:** The laggard catches up to the ETF move within 1-3 days. If sector ETF is +5% and your name is +1%, the expected move is +3-4% catchup.

**Stop:** If the sector ETF reverses its move within 24h, exit immediately. The catalyst wasn't strong enough.

**Time stop:** Exit by day 3. If catchup hasn't happened by day 3, the lag is structural (stock-specific issue), not just slow information diffusion.

**Best instrument:** Shares for the catchup play. KO certificate only if the expected catchup is 2-3% (amplify to meaningful gain).

**Why it works:** ETFs reprice via creation/redemption and arbitrage (fast, algorithmic). Single stocks reprice via human portfolio managers making decisions (slow, 1-3 days). The lag is structural and repeatable.

**Common rotation pairs:**
- Defense spending announcement → defense contractors (Rheinmetall, BAE Systems, Lockheed)
- AI infrastructure news → semis (NVDA, AMD), cloud (AMZN, MSFT), energy (VST, CEG)
- Rate cut signal → REITs, growth tech, homebuilders
- Oil supply disruption → energy (XOM, Shell), tankers
- China stimulus → luxury (LVMH, Hermès), commodities (BHP, Rio Tinto)

---

### Type 4: News Catalyst Momentum (Hold 1-3 days)

**What it is:** A material announcement (FDA approval, government contract, M&A, partnership, product launch) drives a 5%+ move. You ride the momentum for 1-3 days as the news propagates.

**Setup criteria:**
- Identifiable, material catalyst (not just flow, gamma squeeze, or meme activity)
- Price move ≥ 5% intraday on ≥ 2x average volume
- Market cap > $5B (ensures liquidity for exit, avoids pump-and-dumps)
- The news has FOLLOW-ON implications (not a one-time event) — e.g., FDA approval → revenue ramp, contract win → future orders
- Stock NOT already at all-time high before the news (some room for repricing)

**Entry:** Buy on day 1 pullback (after initial spike) OR buy the close of day 1 if holding above the VWAP. Never chase more than 3% above the initial spike high.

**Target:** +5-10% additional move over days 2-3 as:
- Retail discovers the news (day 1-2)
- Analysts publish notes (day 2-3)
- Short covering adds fuel (day 1-3)

**Stop:** If price gives back 50%+ of the day-1 move on day 2, the momentum is dead — exit.

**Time stop:** Exit by day 3. News momentum has a half-life. By day 4-5, everyone who's going to react has reacted.

**Best instrument:** Shares. News trades are fast and volatile — certs get knocked out on intraday noise.

**Why it works:** Information diffusion across investor classes. Day 1 = algos + active managers. Day 2 = analysts + retail. Day 3 = passive rebalancing + short covering. Each wave adds incremental demand.

---

### Type 5: Short Setups (Hold 3-7 days via shares, KO Put, or inverse cert)

**What it is:** A stock breaks down — below major support, below key MAs, or gaps down on bad news. You short it and ride the panic.

**Setup criteria (breakdown short):**
- Stock breaks below 50-day MA AND a clear support level on ≥ 2x volume
- Failed bounce attempt: stock tried to reclaim the level and was rejected (lower high)
- RSI < 45 and falling (momentum confirms the break)
- No upcoming catalyst that could reverse it (no earnings, no product launch)

**Setup criteria (earnings miss short):**
- EPS miss ≥ 10% AND/OR guidance cut
- Gap down ≥ 5% on ≥ 3x volume
- Stock was expensive going in (Forward P/E in top quartile of sector)
- The miss reveals structural issue, not one-time charge

**Entry:** Short (or buy KO Put / inverse cert) on the failed bounce (breakdown) or end of day 1 (earnings miss). For breakdown shorts, the broken support level becomes your stop — if it reclaims, you're wrong.

**Target:** Next major support level, typically -8-15% below breakdown point.

**Stop:** Above the broken support level (breakdown) or above the pre-gap close (earnings miss). Max -5% on shares.

**Time stop:** Exit by day 7. Stocks bounce. If the short thesis hasn't played out in a week, cover and move on.

**Best instrument:**
- Direct short selling (IBKR — requires margin, unlimited risk in theory)
- KO Put certificate (Trade Republic, capped loss at cert value, 8-12x leverage)
- Inverse factor cert (2x-4x daily inverse, for 3-5 day holds only due to decay)

**Why it works:** Stocks fall faster than they rise — panic selling accelerates as stop losses cascade. Institutional selling takes 3-5 days to fully execute (they can't dump a full position in one day).

---

## Daily Scan Methodology

Run every trading morning (or evening prior). Two phases: **Watchlist Scan** + **Discovery Scan**.

### Phase 1: Watchlist Scan (Names You Know)

Screen your existing watchlist + related names for:

```
BREAKOUT CHECK:
- Has any watchlist name broken out of a 2+ week consolidation?
- Volume today vs 20d avg?
- Is the breakout above a clear resistance level?

MOMENTUM CHECK:
- Any watchlist name up/down >5% today?
- What's the catalyst? (Earnings? News? Sector rotation?)
- Does it meet entry criteria for Type 2/3/4/5?

TECHNICAL DETERIORATION (short candidates):
- Any watchlist name breaking below 50MA on volume?
- Any that reported earnings and missed?
```

### Phase 2: Discovery Scan (New Names from Reddit/News/Screener)

Sources to check daily:

| Source | What to Look For | URL / Method |
|--------|-----------------|--------------|
| Reddit r/wallstreetbets | Unusual ticker mentions, DD posts with >500 upvotes | Monitor top posts, look for tickers with volume confirmation |
| Reddit r/stocks | Earnings reaction threads, sector rotation discussions | Quality filters: ignore pure memes, look for thesis + data |
| Reddit r/options | Unusual flow alerts, big bets | Confirm via actual volume data before acting |
| Financial news (Reuters, Bloomberg) | M&A, FDA, contracts, policy changes | Look for the SECOND-ORDER beneficiary, not the obvious one |
| European: r/Finanzen, r/mauerstrassenwetten | German/EU-specific catalysts, DAX movers | |
| TradingView screener | Custom filters for breakout/volume criteria | Pre-built scans for each trade type |
| Unusual Whales / Barchart | Options flow, institutional positioning | Smart money confirmation |

**Discovery filter — must pass ALL:**
1. Market cap > $5B (liquidity)
2. Average daily volume > 1M shares (can exit without slippage)
3. Not a meme/penny stock (no < $10 stocks, no SPACs)
4. Clear, identifiable catalyst (not just "it's going up")
5. Expected move > the math floor for your position size

### Phase 3: Score & Rank

For each candidate that passes the filter:

| Criterion | Score 1-3 | Weight |
|-----------|----------|--------|
| Catalyst strength (material, quantifiable) | | 30% |
| Technical confirmation (volume, breakout, momentum) | | 25% |
| Risk/reward ratio (target ÷ stop distance) | | 25% |
| Timing (how early are we — day 1-2 = good, day 4+ = late) | | 20% |

**Take the top 1-2 scoring candidates.** Never more than 3 active short-term positions.

---

## Exit Rules (Non-Negotiable)

| Rule | Applies To | Why |
|------|-----------|-----|
| **Time stop: Day 7 max** (Day 3 for catalyst/rotation) | All trades | Short-term edge decays exponentially. After the window, you're gambling. |
| **Profit target: Sell 50% at first target, trail rest** | All trades | Lock in gains. Trailing stop = 50% of open profit or below prior day's low. |
| **Stop loss: -5% on shares, -30% on certs** | All trades | Small losses, big wins. A 5% loss needs a 5.3% gain to recover. A 30% loss needs 43%. |
| **No holding through earnings** | All except Type 2 | Binary risk destroys short-term edge. Close or reduce before the report. |
| **No averaging down** | All trades | In a 7-day trade, if price moves against you, your timing is WRONG. Cut it. |
| **Close at math floor** | All trades | If unrealized gain hits the minimum (€50+ net), and momentum stalls, take it. Don't let a cleared floor become a loss. |
| **Friday rule** | Trades entered Thu-Fri | If entered late in week and not clearly working by Friday close, exit. Weekend gap risk is uncompensated. |

---

## Position Sizing & Portfolio Rules

| Parameter | Rule |
|-----------|------|
| Max per trade (shares) | 3% of portfolio |
| Max per trade (certificates) | €100-200 |
| Max concurrent short-term positions | 3 |
| Max total short-term exposure | 10% of portfolio at any time |
| Correlation rule | No more than 2 positions in the same sector |
| Loss limit (daily) | If 2 trades stopped out same day, no new entries for 24h |
| Loss limit (weekly) | If down >2% of portfolio from short-term trades in a week, pause for the rest of the week |

---

## Instrument Selection Decision Tree

```
Expected underlying move in timeframe?
│
├─ > 8% → SHARES (simple, no decay, no KO risk)
│
├─ 4-8% → CHOICE:
│   ├─ High conviction + tight stop available → 3-4x Factor Cert
│   └─ Moderate conviction or loose stop → SHARES
│
├─ 2-4% → LEVERAGED INSTRUMENT REQUIRED
│   ├─ Hold ≤ 5 days + clear stop → KO Certificate (8-12x)
│   └─ Hold 5-7 days → 4x Factor Cert (less KO risk)
│
└─ < 2% → SKIP (not enough meat, even with leverage)

For SHORTS:
├─ Have IBKR + margin → Direct short sell
├─ No margin / prefer capped risk → KO Put certificate
└─ Short-term (3 days) sector bet → Inverse factor cert (2-3x)
```

---

## Journal & Review

Track every short-term trade:

```markdown
| Date | Ticker | Type | Entry | Exit | Days | Gross % | Net € | Notes |
|------|--------|------|-------|------|------|---------|-------|-------|
```

Weekly review questions:
- Which trade types are working? (Shift allocation toward winners)
- Am I holding past time stops? (Discipline check)
- Am I chasing entries? (Should only enter in first 1-2 days of move)
- Net P&L this week after tax — is it worth the time?

---

## Anti-Patterns

| Mistake | Why It Kills You |
|---------|-----------------|
| Chasing day 3+ of a move | You're buying someone else's exit liquidity |
| Holding past time stop because "it'll come back" | Short-term trades DON'T come back. They either work fast or they don't. |
| Taking 2-3% gains on shares (below math floor) | After tax = ~1.5% net. Not worth the risk capital and attention. |
| Trading illiquid names (vol < 500K/day) | Can't exit when you need to. Slippage eats the gain. |
| More than 3 concurrent positions | Attention dilution → miss exit signals |
| Entering without a stop written down | You WILL freeze during volatility |
| Shorting into strength ("it's too high") | Momentum persists. Only short confirmed breakdowns. |
| Holding short-term trade that "becomes a long-term investment" | This is the #1 retail rationalization for bag-holding losses |

---

## Integration With Long-Term Framework

The short-term tactical book and long-term portfolio are SEPARATE:

| | Long-Term (70%) | Short-Term (30%) |
|-|-----------------|-----------------|
| Horizon | 6 months – 3+ years | 1-7 days |
| Analysis | Fundamentals, moat, DCF | Technicals, catalyst, momentum |
| Position size | 3-5% of portfolio | 1-3% of portfolio |
| Stop loss | Thesis kill (may be -20%) | -5% hard stop |
| Instrument | Shares, ETFs | Shares, KO/Factor certs |
| Tax strategy | Hold >0 days (no benefit in Germany anyway) | Accept the 26.375% tax as cost of doing business |
| Compounding | Dividends + appreciation | Rotational — wins fund next trades |

**You CAN have both a long-term position AND a short-term trade on the same name.** Example: Long NVDA shares (long-term, 5% portfolio) AND a 4x factor cert on NVDA breakout (short-term, €100, 5-day hold). They serve different purposes with different exit rules.

---

## Output Format: Short-Term Tactical Scan

When running this scan, output:

```markdown
# Short-Term Tactical Scan — [Date]

## Market Context
- SPY regime: [trending/range-bound]
- VIX: [level] — [implication for short-term trades]
- Key events this week: [earnings, FOMC, data releases to avoid]

## Active Opportunities

### [TICKER] — [Trade Type]
- **Catalyst:** [what's driving this]
- **Setup:** [technical pattern + where we are in it]
- **Entry:** $X (or "already triggered" / "watch for pullback to $X")
- **Stop:** $X (-Y%)
- **Target:** $X (+Z%)
- **Time limit:** [N days]
- **Instrument:** Shares / [specific cert if applicable]
- **Position size:** €X (Y% of portfolio)
- **Math check:** Expected gross €X → net after tax €X → above floor? ✅/❌
- **Confidence:** High / Medium
- **Source:** [watchlist / Reddit / news / screener]

## Watchlist Alerts
- [Names approaching breakout or breakdown levels]

## Passed On (and why)
- [TICKER]: [reason — too late, below math floor, unclear catalyst, etc.]
```
