# Prediction Ledger — every directional call, scored

The single highest-leverage habit for stopping wrong bets: write the call down with
its evidence and its falsifier, then score it when the fact comes in. A call you
can't score is a guess.

## Why this exists

The recurring failure mode is a confident call that rests on the wrong signal — e.g.
a "thesis broken" verdict built from a falling chart while the fundamentals were never
pulled. The ledger does two things:

1. Makes the **evidence explicit *before* the verdict**, so the Bear/Conviction Gate
   can't be skipped.
2. Makes the **track record visible *after***, so systematic bias gets caught instead
   of repeated. "We follow up and find the bet was wrong" becomes a scored dataset,
   not a feeling.

## When to write an entry

For EVERY directional call: **buy, add, trim, exit, "thesis broken," short-term
tactical.** Not for "hold" or "watch-only" notes (those are decisions to defer, not
bets).

## Entry format (one block per call)

```
- Date + ticker
- Call: [BUY / ADD / TRIM / EXIT / BROKEN / TACTICAL] + direction + size
- Confidence: [high/med/low] — must match evidence BREADTH, not conviction strength
- Timeframe: when the thesis is expected to resolve
- Evidence: the specific data pulled (fundamentals + technicals) WITH numbers
- Falsifier: the ONE metric/price that proves me wrong + its threshold
- Thesis on file: [yes — quote it / NO — flagged]
```

**Rule: no falsifier → no call.** If you can't name the single thing that would prove
the call wrong, you don't have a thesis — you have a feeling. Downgrade to
"watch-only" and state what data you're waiting for.

## Scoring (run at next scan, after earnings, or on monthly review)

For each outstanding entry, mark **RIGHT / WRONG / TBD** and say why — which evidence
bit held, which failed. Then feed the misses back into the Bear/Conviction Gate: a
wrong bet is almost always a gate field that wasn't actually filled in. Track the
dominant failure mode (e.g. "technical called fundamental") and let it drive the next
revision of the skill.

## The meta-loop

| Step | Action |
|------|--------|
| Before call | Fill the gate, log the call with evidence + falsifier |
| At scan/earnings | Score the call RIGHT/WRONG/TBD |
| On review | Count misses by failure mode; if one mode dominates, tighten the gate |

The ledger is not a journal of intentions — it's how the skill learns which of its
own signals are load-bearing. That's the difference between "backed up" and "we
follow up and find the bet was wrong."