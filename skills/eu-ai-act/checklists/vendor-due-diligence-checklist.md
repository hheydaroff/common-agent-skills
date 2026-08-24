# Vendor Due-Diligence Checklist (AI procurement)

Use before adopting any third-party AI tool (SaaS, API, model, add-in).

## 1. What are we buying?

- [ ] AI system, GPAI model, or embedded AI in a product?
- [ ] Our role after adoption? (betreiber / quasi-anbieter if we modify / provider if we rebrand)
- [ ] Risk tier if we adopt it? (→ risk-classification checklist)

## 2. Legal & regulatory

- [ ] Does the vendor state its own AI-Act role and compliance status?
- [ ] For high-risk: can the vendor supply **technical documentation**, **CE/conformity evidence**, **EU-DB registration**, **instructions for use**?
- [ ] Data-processing agreement (**AVV**, Art. 28 GDPR) — and where is data processed (EU / third country, SCCs, transfer impact assessment)?
- [ ] Legal basis for processing (Art. 6 GDPR); special categories (Art. 9)?
- [ ] Training on our data — opt-out available? (confidentiality / IP)

## 3. Data protection & security

- [ ] What input data is sent, stored, logged, used for training?
- [ ] Retention & deletion commitments? · Sub-processors list?
- [ ] Encryption in transit/at rest · access controls · audit trail?
- [ ] Incident/breach notification commitments (Art. 33/73)?
- [ ] Data residency / transfer mechanism?

## 4. IP & output

- [ ] Who owns outputs? · Usage rights (commercial use allowed)?
- [ ] Indemnity for IP infringement in output?
- [ ] Copyright / training-data provenance disclosed?

## 5. Oversight & operational

- [ ] Can a human always review/override/reject outputs (Art. 14 spirit)?
- [ ] Bias/fairness & accuracy documentation?
- [ ] System transparency: can we explain decisions (Art. 86 right-to-explanation)?
- [ ] Availability/SLA + exit/offboarding (data export & deletion)?

## 6. Governance & sign-off

- [ ] Approved by: DPO / CISO / compliance / works council (where required)
- [ ] Logged in the central AI register with tier + role + data mapping
- [ ] Re-review trigger (contract change, model change, high-risk shift)?

## Verdict

```
Vendor/tool: ________________
Tier: verboten / hochrisiko / begrenzt / minimal
Nous role: betr / quasi / anbieter / händler / einführer
Data: personal? special categories? third country? training opt-out?
Decision: approve / conditional / reject
Conditions: ________________________________
Review date: __________
```