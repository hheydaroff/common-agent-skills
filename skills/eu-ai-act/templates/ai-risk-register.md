---
type: template
template: risk-register
---

# AI Risk Register

Single source of truth for every AI-related risk: described, scored, owned,
tracked to resolution. Maintain continuously; review at each governance triage.

## Scoring

- **Likelihood** 1–5 (rare → almost certain) · **Severity** 1–5 (negligible → critical)
- **Score = Likelihood × Severity** · **Rating:** 1–6 low · 8–12 medium · 15–20 high · 25 critical

| ID | Risk | Category | L | S | Score | Owner | Mitigations | Status | Review |
|----|------|----------|---|---|-------|-------|-------------|--------|--------|
| AI-001 | | | | | | | | | |

## Starter risk categories (add your own)

- **Data protection** — personal data leakage, unlawful profiling, Art. 22 automated decisions
- **Accuracy & bias** — hallucination, discriminatory output, stale/misleading results
- **Security** — prompt injection, model poisoning, data exfiltration, supply-chain
- **Vendor / third-party** — sub-processor changes, training on our data, contract gaps
- **Agentic autonomy** — agent takes harmful action, scope creep, no human override
- **Intellectual property** — training-data infringement, ownership of outputs
- **Transparency** — undisclosed AI interaction, unlabecked synthetic content
- **Operational** — over-reliance, deskilling, unmonitored drift

## Fields (per row)

- **Mitigations:** concrete controls with owner + due date
- **Status:** open / in-treatment / accepted / closed
- **Review:** date + owner for re-scoring

---

Export to a spreadsheet when it outgrows this page; keep a single canonical copy.