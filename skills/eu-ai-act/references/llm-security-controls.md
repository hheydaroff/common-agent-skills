---
type: reference
topic: llm-security
source: OWASP LLM Top 10 (open licence, summarised)
---

# LLM & Agentic Security Controls

Security controls for systems that call or embed an LLM. The ten classes below
follow the OWASP LLM Top 10 consensus (an openly-licensed list); the mitigation
notes are specific to our stack. Use as the InfoSec test baseline for any LLM
vendor or in-house build — evidence each control, don't just tick it.

| # | Threat | What it is | Core mitigations |
|---|--------|-----------|------------------|
| 1 | Prompt injection | Untrusted input hijacks the model's instructions | Treat prompt content as untrusted; separate instructions from data; validate/sandbox outputs; least privilege on tools |
| 2 | Insecure output handling | LLM output is pasted into code/DB/UI unvalidated | Validate & sanitise outputs; no direct execution; escape before render |
| 3 | Training data poisoning | Corrupted training/fine-tuning data | Provenance + integrity of datasets; vet fine-tuning sources |
| 4 | Model denial of service | Resource exhaustion via long/crafted prompts | Rate limiting, token caps, timeouts, auth on the API |
| 5 | Supply chain | Vulnerable model/plugin dependencies | Pin & audit model and library versions; scan dependencies |
| 6 | Sensitive info disclosure | Model leaks secrets/training data | No secrets in prompts; filter output; redact & encrypt |
| 7 | Insecure plugin/tool design | Agent tools accept free-form input | Strict tool schemas, input validation, allow-lists |
| 8 | Excessive agency | Agent has too much autonomy | Least privilege, human-in-the-loop for consequential actions, scope limits |
| 9 | Over-reliance | Humans trust output blindly | Confidence signals, mandatory review for consequential decisions, training (Kl-Kompetenz) |
| 10 | Model theft | Unauthorised copying/distillation of the model | Access control, API auth, monitoring for unusual query volumes |

## Testing checklist

- [ ] Prompt-injection fuzz tests on any agent (see `templates/agent-deployment-checklist.md`)
- [ ] Output-handling tests (script/data injection)
- [ ] Data-leakage test: can the model echo secrets or training data?
- [ ] Rate-limit / DoS test
- [ ] Audit of tool permissions (least privilege) before go-live

---

Pair with `checklists/vendor-due-diligence-checklist.md` when the LLM is
third-party, and ask the vendor to attest to these controls in
`templates/vendor-security-questionnaire.md`.