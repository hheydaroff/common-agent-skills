# Risk Classification — the full risk map

## The four tiers

```
UNACCEPTABLE → PROHIBITED (Art. 5)        — fundamental-rights intrusion, not controllable via oversight
HIGH         → HIGH-RISK (Art. 6 + I/III) — serious impact, but controllable via obligations
LIMITED      → TRANSPARENCY (Art. 50)     — chatbots, deepfakes → labelling only
MINIMAL      → NO obligations             — spam filters, spellcheck
```

**Decision heuristic:** Has the person a real choice?
- No → **Verboten** (power imbalance, non-avoidable, private sphere)
- Yes but high impact → **Hochrisiko** (credit, job, health)
- Yes, low impact → **Begrenzt** (chatbot) / **Minimal** (spam filter)

## Art. 5 — Prohibited practices (8 in the base text, lit. a–h)

> **Base text (Regulation 2024/1689, OJ 12.7.2024).** The Digital Omnibus adds one more prohibition (see note below).

| lit. | Practice | Key exception |
|------|----------|---------------|
| a | Subliminal / manipulative / deceptive techniques | — |
| b | Exploiting vulnerabilities (age, disability, specific social/economic situation) | — |
| c | Social scoring | — |
| d | Predictive policing (risk of a person committing a criminal offence, based **solely** on profiling/personality traits) | supporting **human** assessment already based on **objective, verifiable facts** |
| e | Facial-recognition databases via **untargeted scraping** of internet/CCTV | — |
| f | **Emotion inference in the workplace / education** | **medical or safety** purposes |
| g | **Biometric categorisation** of sensitive traits (race, political opinion, trade-union membership, religion, sex life, sexual orientation) | labelling/filtering of lawfully acquired biometric data; law-enforcement categorisation |
| h | **Real-time remote biometric identification** in public spaces for law enforcement | 3 narrow objectives (below) |

### The 3 exceptions to (h) — real-time remote biometric ID
1. Targeted search for specific **victims** (abduction, trafficking, sexual exploitation) / missing persons
2. Prevention of a **specific, imminent threat** to life/safety or genuine terrorist threat
3. Localisation/identification of a suspect of a **serious offence** (Annex II, ≥ 4 years max custody)

> Real-time remote biometric ID also requires: judicial / independent-authority **prior authorisation** (in duly justified urgency up to 24 h), a prior **fundamental-rights impact assessment (Art. 27)** and **EU-database registration (Art. 49)**.

### Digital Omnibus addition (applies 02.12.2026)
- **AI systems generating non-consensual sexual deepfakes and child sexual abuse material** — new prohibition, not yet reflected in the displayed Art. 5 text (which still shows a–h).

> Distinction that traps most learners: **Justice context, opposite result** — *predicting the future* (predictive policing, Art. 5(d)) = prohibited UNLESS it only supports a human assessment already based on objective/verifiable facts; *assessing evidence in an actual case* (e.g. credibility of witness testimony) = high-risk (Annex III, area 6).

## Art. 6 — High-risk (two routes)

1. **Annex I route (Art. 6 Abs. 1):** AI is a **safety component** of a regulated product (medical devices, vehicles) → requires third-party conformity assessment → applies **02.08.2028**
2. **Annex III route (Art. 6 Abs. 2):** AI in one of 8 areas (below) → applies **02.12.2027**

Exception: no *significant* risk to health/safety/fundamental rights — **but there is a counter-exception for profiling.** Art. 7 lets the Commission extend/shorten Annex III.

## Annex III — the 8 high-risk areas

| # | Area | Example |
|---|------|---------|
| 1 | Biometrics & remote ID | facial-access control |
| 2 | Critical (digital) infrastructure | power/gas/heat/water, road traffic |
| 3 | Education | automated exam grading |
| 4 | Employment & HR | **recruiting AI, CV filtering** |
| 5 | Essential services | **credit scoring**, health/life insurance pricing |
| 6 | Law enforcement | lie detector, witness credibility |
| 7 | Migration & asylum | document check, risk assessment |
| 8 | Administration of justice | AI in judicial decisions |

## Art. 6 → requirements for high-risk (Art. 9–15)

| Art. | Requirement |
|------|-------------|
| **9** | Risk-management system |
| **10** | Data & data governance (quality, bias detection/mitigation) |
| **11** | Technical documentation |
| **12** | Record-keeping (logging, traceability) |
| **13** | Transparency & information for deployers (instructions for use) |
| **14** | Human oversight |
| **15** | Accuracy, robustness, cybersecurity |

## Art. 50 — Transparency obligations (limited risk; apply 02.08.2026)

| Abs. | Who | Obligation |
|------|-----|-----------|
| 1 | Provider | Inform people they interact with an AI system |
| 2 | Provider | Label synthetic/manipulated content (machine-readable, hard to remove) |
| 3 | Deployer | Inform about emotion-recognition / biometric-categorisation systems |
| 4 | Deployer | Label deepfakes; disclose AI-generated public-interest texts (unless human editorial control) |

Exceptions: crime detection/prevention with appropriate safeguards; obvious AI (Abs. 1); non-substantive assistive functions (Abs. 2).

## GPAI (Art. 51–56) — brief

- Generic-purpose AI models (GPT, Llama, Gemini); systemic risk = **10²⁵ FLOP**
- Art. 52: provider informs the Commission within **2 weeks**
- Art. 53: technical documentation (training, data provenance, energy use) + trainable-content summary
- Art. 54: authorised representative for third-country providers (unless open-source without systemic risk)
- Art. 55: additional duties for systemic-risk models (adversarial testing, cybersecurity)