---
type: template
template: vendor-security-questionnaire
regulation: GDPR Art. 28 + EU AI Act (provider duties)
---

# AI Vendor Security & Compliance Questionnaire

Send to any prospective AI vendor (SaaS, model, or custom-build) before contract
signing. Ask for evidence, not confirmation. Tie every "yes" to a document link.

## 1. Company & product

| Question | Response |
|----------|----------|
| Legal entity, jurisdiction, contact | |
| Product name, version, hosting model (SaaS / hosted / on-prem) | |
| Underlying model(s) — own or third-party (name the model provider) | |
| AI-specific certifications (ISO/IEC 42001, etc.) | |

## 2. Data handling

- [ ] Where is model & customer data processed and stored? (regions)
- [ ] Full sub-processor list (esp. the LLM/model host — e.g. OpenAI, Google Vertex, Anthropic)
- [ ] Is any personal data used to train / fine-tune your model?
- [ ] Data retention per category; deletion on contract end
- [ ] Derived-data model: are source, model outputs, and human decisions separable?
- [ ] Third-country transfers → SCCs / adequacy / TIA in place?

## 3. Model & security

- [ ] Model card / technical documentation available?
- [ ] Training-data provenance and licensing documented?
- [ ] Bias / fairness evaluation performed? (per protected group)
- [ ] Accuracy & robustness metrics published?
- [ ] Security controls: OWASP LLM Top 10 coverage (prompt injection, data leakage, etc.)
- [ ] Penetration test / security audit report (recent)?

## 4. EU AI Act positioning

- [ ] AI Act risk classification of the product (Art. 6/Annex III) — written?
- [ ] Is the vendor provider or deployer for this deployment (Art. 25)?
- [ ] Transparency obligations (Art. 50) met — disclose AI interaction, label output?
- [ ] Automated decision-making (Art. 22 GDPR) — is there human review / override?

## 5. Contract & compliance

- [ ] GDPR DPA + Art. 28 clauses; any **AI Processing Annex** signed?
- [ ] EU AI Act conformity documentation / CE marking where high-risk
- [ ] Incident notification SLA (GDPR Art. 33/34, AI Act Art. 73)
- [ ] Audit / inspection rights for us
- [ ] Data-portability & exit provisions on termination

## 6. Verdict

| Criterion | Met / Partial / Gap | Evidence link |
|-----------|--------------------|---------------|
| | | |

**Risk rating & recommendation:** ______ (cleared / conditional / reject)