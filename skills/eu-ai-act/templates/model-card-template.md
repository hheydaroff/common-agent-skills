---
type: template
template: model-card
regulation: EU AI Act Art. 11 + Annex IV
---

# Model Card / Technical Documentation

Providers of high-risk AI systems must draw up technical documentation before
placing the system on the market or putting it into service (Art. 11 + Annex IV).
This model card is the human-readable working record that also supports
deployer due diligence — fill one per model release.

## 1. Identity & intended use

| Field | Detail |
|-------|--------|
| Model name / ID / version | |
| Owner / team | |
| Intended purpose (who uses it, what for) | |
| Foreseeable misuse | |
| Risk class (Art. 6) + rationale | |

## 2. Training & data (Annex IV)

- [ ] Training / fine-tuning data: source, provenance, licensing
- [ ] Data-governance measures (Art. 10): bias examination, representative coverage, gaps
- [ ] Any personal data used / synthetic data used
- [ ] Data and label quality, known limitations

## 3. Performance & evaluation

| Metric | Value / result | Conditions |
|--------|---------------|------------|
| Accuracy / precision / recall | | |
| Robustness (out-of-distribution) | | |
| Bias / fairness metrics (per group) | | |
| Safety / refusal behaviour | | |

## 4. Limitations & human oversight

- [ ] Known failure modes and where the model should not be relied on
- [ ] Human-oversight measures (Art. 14): who reviews, when, with what tooling
- [ ] Confidence / uncertainty signals shown to the operator

## 5. Logging, monitoring & cybersecurity

- [ ] Automatic logging of events (Art. 12) — what is logged, retention
- [ ] Cybersecurity measures (Art. 15): model/subversion, poisoning, prompt-injection
- [ ] Drift / quality monitoring plan (accuracy, fairness, relevance)

## 6. Transparency & downstream

- [ ] Art. 50 transparency: is interaction disclosed? output labelled?
- [ ] Instructions for use handed to the deployer
- [ ] Registration in the EU database (Art. 49 / 71) where required

---

**Release history** (version, changes, date, sign-off): keep a running table here.