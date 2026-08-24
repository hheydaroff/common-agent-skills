# Risk Classification Checklist

Walk every AI use case through this in order. Stop at the first tier that matches.

## Step 1 — Is it an AI system? (Art. 3 Nr. 1)

- [ ] Maschinengestützt (runs on computers)?
- [ ] Works with some degree of autonomy?
- [ ] Derives outputs (inference) from inputs?
- [ ] Outputs can influence physical or virtual environments?
- [ ] (Anpassungsfähigkeit / learning — *optional*, not required)

> If "no" to the core four → **not an AI system**; the AI Act does not apply.

## Step 2 — In scope? (Art. 2)

- [ ] Not national security / purely military?
- [ ] Not solely research & development?
- [ ] Placed on the EU market / used in EU / EU-established deployer?

## Step 3 — Prohibited? (Art. 5) — if ANY match → STOP (verboten)

- [ ] Subliminal / manipulative / deceptive techniques
- [ ] Exploits vulnerabilities (children, elderly, disability, poverty)
- [ ] Biometric categorisation of sensitive traits
- [ ] Social scoring (disproportionate / out-of-context)
- [ ] Real-time remote biometric ID in public spaces (no qualifying exception)
- [ ] Predictive policing (probability of future crime)
- [ ] Facial-recognition DB built by mass scraping
- [ ] Emotion recognition at workplace / education
- [ ] "Nudification" (non-consensual intimate images)

## Step 4 — High-risk? (Art. 6)

- [ ] **Annex I:** safety component of a regulated product (medical device, vehicle)? → high-risk (*applies 02.08.2028*)
- [ ] **Annex III** (applies 02.12.2027), any area:
  - [ ] Biometrics & remote ID
  - [ ] Critical (digital) infrastructure
  - [ ] Education / vocational training assessment
  - [ ] Employment / HR (recruiting, promotion, termination, monitoring)
  - [ ] Essential services (credit scoring, insurance pricing)
  - [ ] Law enforcement
  - [ ] Migration / asylum / border control
  - [ ] Administration of justice

> If an Annex III use case has **no significant risk** to health/safety/fundamental rights, it may be exempt — **but there is a counter-exception: profiling.** When in doubt, treat as high-risk.

## Step 5 — Limited risk? (Art. 50 transparency)

- [ ] Direct interaction with people (chatbot) → inform it's AI
- [ ] Synthetic/manipulated content → label (machine-readable)
- [ ] Emotion recognition / biometric categorisation → inform
- [ ] Deepfake / public-interest text → label (unless human editorial control)

## Step 6 — Minimal risk

- [ ] Spam filter, spellcheck, recommendation of non-critical content → no obligations

## Output

```
Use case: ______________________
AI system: yes / no
In scope:  yes / no
Tier: verboten / hochrisiko (Anhang I | III Nr. __) / begrenzt / minimal
Role(s): provider / deployer / quasi-provider / importer / distributor / n/a
Applies: 02.02.2025 / 02.08.2025 / 02.08.2026 / 02.12.2027 / 02.08.2028
Next step: ______________________
```