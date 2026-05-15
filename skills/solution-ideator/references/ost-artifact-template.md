# OST Artifact Template

Saved as `OST-[slug]-[YYYY-MM-DD].md` at repo root (or `~/solution-trees/` outside a repo).

```markdown
# Opportunity Solution Tree: [Outcome Statement]

**Date:** YYYY-MM-DD
**Mode:** discovery
**Research basis:** [interviews / analytics / surveys / hypothetical]

## Desired Outcome

[Single measurable outcome — metric, target, timeframe]

## Research Summary

[Brief summary of evidence sources: N interviews, analytics signals,
support ticket themes, etc. If no research: flag as hypothetical.]

## Opportunity Map

### 🔴 High Opportunity

#### Opportunity 1: "[Customer-perspective framing]"
- **Evidence:** [citation — interview quote, data point, ticket theme]
- **Importance:** [0–1 or High/Med/Low]
- **Satisfaction:** [0–1 or High/Med/Low]
- **Opportunity Score:** [calculated or qualitative tier]

#### Opportunity 2: "[Customer-perspective framing]"
- **Evidence:** [citation]
- **Importance:** [value]
- **Satisfaction:** [value]
- **Opportunity Score:** [value]

### 🟡 Medium Opportunity

#### Opportunity 3: "[Customer-perspective framing]"
- **Evidence:** [citation]
- **Opportunity Score:** [value]

### 🟢 Low Opportunity (parked)

#### Opportunity 4: "[Customer-perspective framing]"
- **Reason parked:** [already well-served / low importance / out of scope]

## Prioritized Opportunities

**Pursuing:** Opportunity 1, Opportunity 2
**Rationale:** [why these two — score, strategic fit, evidence strength]

## Solutions

### For Opportunity 1: "[framing]"

| # | Solution | Perspective | Notes |
|---|----------|-------------|-------|
| S1 | [description] | PM | [brief rationale] |
| S2 | [description] | Designer | [brief rationale] |
| S3 | [description] | Engineer | [brief rationale] |
| S4 | [description] | [any] | [brief rationale] |

### For Opportunity 2: "[framing]"

| # | Solution | Perspective | Notes |
|---|----------|-------------|-------|
| S5 | [description] | PM | [brief rationale] |
| S6 | [description] | Designer | [brief rationale] |
| S7 | [description] | Engineer | [brief rationale] |

## Experiments

### Experiment 1: Validate [Solution S1]

| Field | Content |
|-------|---------|
| **Assumption** | [riskiest assumption — Value/Usability/Viability/Feasibility] |
| **Hypothesis** | We believe [solution] will [outcome] for [segment] because [reason] |
| **Method** | [prototype test / fake-door / Wizard of Oz / concierge / data analysis] |
| **Metric** | [what you measure] |
| **Success threshold** | [minimum bar to proceed] |
| **Timeline** | [duration] |
| **Skin-in-the-game** | [Yes/No — does participant commit something real?] |

### Experiment 2: Validate [Solution S6]

| Field | Content |
|-------|---------|
| **Assumption** | [riskiest assumption] |
| **Hypothesis** | [statement] |
| **Method** | [method] |
| **Metric** | [measure] |
| **Success threshold** | [bar] |
| **Timeline** | [duration] |
| **Skin-in-the-game** | [Yes/No] |

## Full Tree Visualization

🎯 Outcome: [measurable outcome]
│
├── 🔴 Opportunity 1: "[framing]"  (Score: X.XX)
│   ├── S1: [solution] — Experiment: [method] → ≥[threshold]
│   ├── S2: [solution]
│   ├── S3: [solution] — Experiment: [method] → ≥[threshold]
│   └── S4: [solution]
│
├── 🔴 Opportunity 2: "[framing]"  (Score: X.XX)
│   ├── S5: [solution]
│   ├── S6: [solution] — Experiment: [method] → ≥[threshold]
│   └── S7: [solution]
│
└── 🟡 Opportunity 3: "[framing]"  (Score: X.XX)  [parked]

## Next Steps

- [ ] Run Experiment 1: [brief description] — [timeline]
- [ ] Run Experiment 2: [brief description] — [timeline]
- [ ] [Optional] Transition winning solution to Decision mode for
      technical approach selection

## Transition to Decision Mode (if applicable)

**Problem for Decision mode:** [reframed from opportunity + solution]
**Pre-seeded solutions:** [solutions that validated]
**Carry-forward constraints:** [anything discovered during experiments]
```
