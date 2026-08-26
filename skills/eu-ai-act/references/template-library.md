# Template Library — AI-Officer working kit (index)

Original working templates and guides, drafted from the EU AI Act, GDPR, and
standard AI-governance practice. These are **fill-in artefacts** — the thing you
produce or complete for a specific system, vendor, or decision — complementing
the law references (`references/*`) and decision checklists (`checklists/*`).

**Layout**
- `templates/` — fill-in documents and registers (open, fill, send/keep).
- `references/` — consultation guides on security controls and data governance.

---

## Quick map to smart Europe's known gaps (MSXi/ClaimsGenie — Aug 2026)

| Vendor assessment gap | Original template that closes it |
|-----------------------|----------------------------------|
| Missing AI Processing Annex (DPA §1.1) | `templates/ai-contract-clauses.md` (+ Data protection section) |
| No DPIA delivered pre-go-live | `templates/ai-dpia-template.md` |
| No model card / accuracy evidence | `templates/model-card-template.md` |
| Prompt-injection / OWASP Top 10 evidence missing | `references/llm-security-controls.md` |
| Google (Gemini/Vertex) not in subprocessor list | `templates/vendor-security-questionnaire.md` |
| No EU AI Act risk classification, Art. 22 unresolved | `checklists/risk-classification-checklist.md` + `templates/fria-template.md` |
| Bias / data-governance (Art. 10) not evidenced | `references/data-governance-and-bias.md` |

## smart Europe weave-in (governance redesign, June 2026)

- **Front door (IBR intake → smart.AI eval):** `templates/tool-approval-request.md`
- **DP ∥ InfoSec lanes:** DP → `templates/ai-dpia-template.md` + `templates/fria-template.md`; InfoSec → `references/llm-security-controls.md` + `templates/agent-deployment-checklist.md`
- **Buy path (Procurement):** `templates/vendor-security-questionnaire.md` + `templates/ai-contract-clauses.md`
- **Post-deployment monitoring (high-risk):** `templates/ai-risk-register.md` + `templates/ai-system-inventory.md` + `templates/compliance-tracker.md`
- **Agentic builds (AWS AgentCore):** `templates/agent-deployment-checklist.md`

---

## Template index

### Assess (impact & documentation)
- `templates/ai-dpia-template.md` — DPIA (GDPR Art. 35), AI-focused
- `templates/fria-template.md` — Fundamental Rights Impact Assessment (Art. 27)
- `templates/model-card-template.md` — technical documentation / model card (Art. 11, Annex IV)

### Procure (vendor & contract)
- `templates/vendor-security-questionnaire.md` — DD questionnaire for AI vendors
- `templates/ai-contract-clauses.md` — contract clauses + AI processing annex checklist

### Govern (operating records)
- `templates/ai-risk-register.md` — scored, owned risk register
- `templates/ai-system-inventory.md` — register of all AI systems in use
- `templates/compliance-tracker.md` — multi-framework posture (AI Act + GDPR + ISO/NIST)
- `templates/agent-deployment-checklist.md` — go-live gate for autonomous/agentic AI
- `templates/tool-approval-request.md` — intake / buy-build-don't routing form

### Communicate (people)
- `templates/acceptable-use-policy.md` — employee acceptable-use rules

### Consult (guides)
- `references/llm-security-controls.md` — OWASP LLM Top 10 controls as an InfoSec baseline
- `references/data-governance-and-bias.md` — Art. 10 data governance + bias testing + data classification for AI

---

## Notes

- These are original drafts grounded in the regulation; have counsel / DPO review
  before external use, and localise placeholders `[ORGANIZATION NAME]`, `[DATE]`, etc.
- Registers/trackers (`risk-register`, `system-inventory`, `compliance-tracker`)
  export naturally to a spreadsheet when they outgrow Markdown — maintain one
  canonical copy.