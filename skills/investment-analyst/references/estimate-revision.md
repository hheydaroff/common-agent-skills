# Estimate Revision (Post-Earnings Update)

Update estimates after earnings or material events. Clean "old vs new" table + recalculated fair value.

## When to Use

- `/invest update <TICKER>` — after earnings release
- After guidance change (raised/lowered/withdrawn)
- After material event (M&A, restructuring, management change)
- After macro shift affecting model assumptions

## Step 1: Actual vs Estimate

```markdown
## Q[X] Results vs Estimates

| Line Item | Our Estimate | Actual | Delta | Notes |
|-----------|-------------|--------|-------|-------|
| Revenue | $X.XB | $X.XB | +$XXM (+X%) | [driver] |
| Gross Margin | XX.X% | XX.X% | +XXbps | [driver] |
| EPS (Adj) | $X.XX | $X.XX | +$X.XX | [driver] |
| FCF | $X.XB | $X.XB | +$XXM | [driver] |

### Key KPIs
| Metric | Expected | Actual | Implication |
|--------|----------|--------|-------------|
| [KPI] | X | X | [thesis impact] |
```

## Step 2: Forward Estimate Revision

```markdown
## Updated Estimates

| | FY25E (Old) | FY25E (New) | Change | FY26E (Old) | FY26E (New) | Change |
|---|-----------|-----------|--------|------------|------------|--------|
| Revenue | X.XX | X.XX | +X% | X.XX | X.XX | +X% |
| EBITDA Margin | XX.X% | XX.X% | +Xbps | XX.X% | XX.X% | +Xbps |
| EPS | $X.XX | $X.XX | +X% | $X.XX | $X.XX | +X% |

### Assumption Changes
| Assumption | Old | New | Reason |
|-----------|-----|-----|--------|
| Rev growth | X% | X% | [specific — "Q3 run-rate implies higher"] |
| Gross margin | X% | X% | [specific — "mix shift to services"] |
```

## Step 3: Valuation Impact

```markdown
## Updated Valuation

| Method | Old Fair Value | New Fair Value | Change |
|--------|---------------|---------------|--------|
| P/E (FY26E × target) | $XXX | $XXX | +X% |
| EV/EBITDA | $XXX | $XXX | +X% |
| **Blended** | **$XXX** | **$XXX** | **+X%** |

Current Price: $XXX — Upside: +X%
```

## Step 4: Thesis Impact

```markdown
## Thesis Assessment
- Core thesis: [Intact / Challenged / Strengthened]
- Pillars affected: [which ones, how]
- Rating: [Maintained / Upgraded / Downgraded] at $XXX target
- Action: [No change / Add / Trim / Exit]
- Updated exit targets: T1 $X / T2 $X / T3 $X
```

## Quick Template (inline quarter, no changes)

```markdown
## Quick Update: <TICKER> Q[X]
**Result**: Inline | **Guidance**: Maintained | **Estimates**: Unchanged
**Thesis**: Intact | **Action**: Hold | **Next catalyst**: [date]
```

## Integration

- Creates an update log entry in thesis tracker
- Updates exit targets if estimates moved >5%
- Links to catalyst calendar (mark event as "Fired" with outcome)
