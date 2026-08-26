---
type: template
template: ai-contract-clauses
regulation: GDPR Art. 28, 35 + EU AI Act Arts. 16–27
---

# AI Procurement & Contract Clauses Checklist

Insert these clauses (as applicable) into contracts with AI vendors, model
providers, and custom-build suppliers. The goal is a contract that mirrors the
EU AI Act role split and GDPR processor duties — never rely on the vendor's
standard terms.

## 1. Roles & definitions

- [ ] Define provider vs deployer (AI Act Art. 25) and name who takes which role *for this deployment*
- [ ] Define the AI system, its intended purpose, and excluded uses
- [ ] Define "AI output", "training data", "derived data", "customer data"

## 2. Data protection (GDPR Art. 28)

- [ ] Data-processing agreement (controller↔processor) or SCCs (controller↔controller)
- [ ] **AI Processing Annex**: prohibit training / fine-tuning on our personal data without explicit written approval
- [ ] Sub-processors: prior written approval; full list; restriction that the model host (e.g. Google Vertex, OpenAI) is named
- [ ] Data locations, retention, and deletion on termination specified
- [ ] DPIA cooperation clause (vendor provides the info needed for our Art. 35 DPIA)

## 3. Intellectual property & data rights

- [ ] Who owns model outputs generated on our behalf?
- [ ] Ownership of any fine-tuned model weights / adaptations
- [ ] Prohibition on using our data to improve the vendor's general-purpose models
- [ ] Indemnity for IP-infringement claims arising from the model's training data

## 4. EU AI Act obligations

- [ ] Vendor supplies technical documentation / model card (Art. 11, Annex IV)
- [ ] Human-oversight and logging requirements (Art. 14, 12)
- [ ] Transparency duties (Art. 50): disclosure of AI interaction, output labelling
- [ ] Serious-incident reporting (Art. 73) and cooperation with market surveillance (Art. 20)
- [ ] Registration in the EU database where applicable (Art. 49 / 71)

## 5. Security & monitoring

- [ ] Security controls incl. OWASP LLM Top 10; audit rights
- [ ] Accuracy / performance / drift monitoring commitments + SLAs
- [ ] Right to audit, test, and inspect (including on changes to the model)

## 6. Liability, exit & termination

- [ ] Liability allocation for wrongful / biased / hallucinated outputs
- [ ] Exit: export of customer data and any fine-tuned assets in a usable format
- [ ] Suspension rights on material compliance breach
- [ ] Governing law & jurisdiction (note: AI Act applies to providers placing systems on the **EU market**, regardless of governing law)

---

See also `checklists/vendor-due-diligence-checklist.md` for the pre-signing review.