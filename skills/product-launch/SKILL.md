---
name: product-launch
description: "Design a product launch / go-to-market strategy: beachhead segment, ideal customer profile (ICP), positioning and messaging, GTM motions, growth loops, launch timeline, and competitive battlecards. Use when planning a product launch, creating a GTM plan, choosing a first market segment, designing growth mechanics, or building an 'us vs competitor' battlecard."
---

# Product Launch

Go-to-market planning for a new product, feature, tier, or market expansion.
Three modes depending on the ask. Adapted from Paweł Huryn's pm-go-to-market
skills (Product Compass, MIT) — see [ATTRIBUTION.md](ATTRIBUTION.md).

## Mode 1: Full launch plan (default)

Trigger: "plan the launch", "GTM strategy", "how do we launch X", new market entry.

1. **Understand the launch**: what is launching (product / feature / tier /
   market expansion), stage (pre-launch planning, imminent launch, post-launch
   optimization), existing customers or starting from zero, timeline and hard
   deadlines, budget, team size.
2. Load [beachhead-segment.md](references/beachhead-segment.md) — score
   candidate segments and pick the single best first segment.
3. Load [ideal-customer-profile.md](references/ideal-customer-profile.md) —
   define the ICP from research, surveys, or customer data.
4. Load [gtm-strategy.md](references/gtm-strategy.md) — positioning, messaging,
   channels, metrics; produce the full GTM plan using its plan template.

Write the plan to `docs/GTM_<product>.md` (create `docs/` if missing).

## Mode 2: Growth strategy

Trigger: "growth stalled", "how do we get more users", "design growth loops",
choosing acquisition channels.

1. Ask: what is the product, current metrics (users, growth rate, channels),
   what's working, business model, team and budget for growth.
2. Load [growth-loops.md](references/growth-loops.md) — rank the 5 loop types,
   pick primary + secondary loops.
3. Load [gtm-motions.md](references/gtm-motions.md) — score the 7 motions,
   pick the motion stack.
4. Output using the Growth Strategy template at the end of
   [growth-loops.md](references/growth-loops.md) → `docs/GROWTH_<product>.md`.

## Mode 3: Battlecard

Trigger: "us vs competitor X", "battlecard", "why not competitor X?"

Load [competitive-battlecard.md](references/competitive-battlecard.md).
Research the competitor with web search; read any win/loss data, feature lists,
or sales call notes the user provides first. One battlecard per competitor →
`docs/BATTLECARD_<us>-vs-<them>.md`.

## Rules of thumb

- "Everyone" is not a segment — the tighter the beachhead, the faster you learn.
- The ICP should be specific enough that sales can identify a prospect in 30 seconds.
- Messaging uses the customer's language, not internal terminology.
- 2–4 complementary motions beat 7 scattered ones; loops compound, one-off campaigns don't.
- Flag projections where CAC exceeds ~1/3 of LTV.
- Pre-launch (waitlist, beta, early access) matters as much as launch day; the
  first 90 days after launch set the trajectory.
- Battlecards go stale quarterly; never trash the competitor — position on strengths.
- Win/loss data from real deals is worth 10x any analysis — ask for it.

## Follow-ups

After delivering any mode, offer the adjacent ones: another mode, marketing
copy for the top channel, a launch metrics dashboard, or positioning refinement.

## Reference Files

| File | When to load |
|------|--------------|
| [gtm-strategy.md](references/gtm-strategy.md) | Building the full launch plan: channels, messaging, metrics, timeline, GTM plan template |
| [beachhead-segment.md](references/beachhead-segment.md) | Choosing the first market segment |
| [ideal-customer-profile.md](references/ideal-customer-profile.md) | Defining the ICP from research/survey/customer data |
| [gtm-motions.md](references/gtm-motions.md) | Selecting acquisition channels / the GTM motion stack |
| [growth-loops.md](references/growth-loops.md) | Designing growth loops; also holds the combined Growth Strategy template |
| [competitive-battlecard.md](references/competitive-battlecard.md) | Creating a battlecard against a specific competitor |
