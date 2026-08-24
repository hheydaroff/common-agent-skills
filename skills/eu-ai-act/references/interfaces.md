# Interfaces — DSGVO, Urheberrecht, Haftung, KI-Ethik

## DSGVO ↔ AI Act

**Core rule:** GDPR protects **personal data** regardless of technology; the AI Act regulates **AI systems** regardless of whether personal data is processed. Both apply **cumulatively** when an AI system processes personal data.

| Topic | GDPR | AI Act |
|-------|-------|--------|
| Legal basis | **Art. 6 Abs. 1 lit. f** (legitimate interest) usually the closest for AI | — |
| Purpose change | **Art. 6 Abs. 4 GDPR** is the test | **Art. 59** eases re-use inside an AI regulatory sandbox |
| Automated decisions | **Art. 22** — right *not* to be subject to solely-automated decision with legal/significant effect | Art. 14 (human oversight) + Art. 26 Abs. 11 (inform affected persons) |
| Impact assessment | **Art. 35 DSFA** (DPIA) | **Art. 27** fundamental-rights impact assessment |
| Incident reporting | **Art. 33** (72h) | **Art. 73** (15 days / 2 days) |
| Records | Art. 30 (record of processing) | Art. 18/19 (docs/logs) |

**Art. 22 GDPR detail:** applies when a decision is (1) **solely** automated, (2) has **legal or similarly significant effect**, (3) on a natural person. Exceptions: contract (Abs. 2 a), law (b), explicit consent (c). **CJEU SCHUFA (C-634/21):** even scoring falls under Art. 22 if it strongly influences a downstream human decision; "human review" must be real — the reviewer needs access, time, and authority to deviate.
**Art. 9 GDPR** special categories can be used for high-risk training **only** to detect/correct bias (Art. 10 Abs. 5 AI Act) with strict safeguards (pseudonymisation, no third-party access, deletion after correction).

## Urheberrecht (copyright) ↔ AI

- **Protected:** personal intellectual creations (texts, images, code); facts & ideas NOT protected
- **Training:** copies during training can infringe; EU text-&-data-mining exception (**§ 44b UrhG**) **with opt-out**; broader exception for research
- **Output:** no automatic protection for purely machine-generated works; protection only with **human creative input** (prompting + curation, "Gestaltungshöhe")
- **Liability:** the *user* can be liable for infringements in output; check the provider's ToS/licence (usage rights, indemnities, opt-outs)

## Haftung (liability)

- Public-law fines via Art. 99; civil damages claims for breaches; representative actions (Art. 110, VDuG)
- EU product-liability & AI-liability framework supplements the AI Act

## KI-Ethik — 7 HLEG principles (recital 27)

1. **Human agency and oversight**
2. Technical robustness and safety
3. **Privacy and data governance**
4. **Transparency**
5. **Diversity, non-discrimination and fairness**
6. Societal and environmental well-being
7. **Accountability**

> Non-binding, but transposed into legal norms for risky AI in the AI Act. Voluntary frameworks: White House Voluntary AI Commitments · G7 Guiding Principles · OECD AI Principles · EU AI Pact.

## Bias & discrimination (practical)

- Bias sources: unbalanced training data, historical discrimination, feature selection, feedback loops in continuously-learning systems
- Mitigations: diverse/representative data, audits, fairness metrics, human oversight, bias correction (Art. 10)