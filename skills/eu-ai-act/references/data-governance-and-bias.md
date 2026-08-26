---
type: reference
topic: data-governance-bias
regulation: EU AI Act Art. 10 + GDPR Art. 5, 9
---

# Data Governance & Bias (Art. 10) + Data Classification for AI

Two concerns that usually surface together when you introduce AI into a
workflow: **what data may an AI tool touch**, and **is the training/input data
fair and representative enough** that the system won't discriminate.

## 1. Data governance (EU AI Act Art. 10)

For high-risk systems, providers must apply training/validation-data practices
covering design choices, collection, preparation, and assumptions about what the
data represents. Deployers get value from demanding the same evidence.

- [ ] **Provenance** — where does the data come from; is its use lawful (licence, GDPR basis)?
- [ ] **Relevance & representativeness** — does the data match the intended context; which groups are under-represented?
- [ ] **Bias examination** — how are discrimination risks (Art. 9 GDPR protected grounds) checked and measured?
- [ ] **Gaps & limitations** — documented, including known biases that can't be removed
- [ ] **Personal data** — minimised; special-category data only with a lawful basis + DPIA

## 2. Bias & fairness testing

Run before go-live and re-run on drift:

| Check | Method | Result |
|-------|--------|--------|
| Disaggregated metrics | accuracy/precision/recall per protected group | |
| Disparate impact | compare selection/score rates across groups | |
| Failure modes | which subgroups see worse errors | |
| Human review | is there a competent human override? | |
| Re-test trigger | on model update, new data, or quarterly | |

Record findings in the model card (`templates/model-card-template.md`) and,
for personal-data systems, feed them into the DPIA.

## 3. Data classification for AI use

A 4-level rule for what may be entered into which AI tool:

| Level | Examples | Allowed in |
|-------|----------|-----------|
| Public | published marketing, public web data | any tool |
| Internal | org-only docs, process notes | approved internal/enterprise AI tools |
| Confidential | financials, strategy, customer contracts | approved tools with contractual protection; no public models |
| Secret / personal | credentials, personal data of customers/staff | only with DP sign-off + DPIA; enterprise-grade, EU-hosted where required |

**Rule of thumb:** if you wouldn't put it in a public forum, don't put it in a
public model. See `templates/acceptable-use-policy.md` for the employee-facing
version and `templates/vendor-security-questionnaire.md` for evaluating whether
a vendor's tool counts as "approved".