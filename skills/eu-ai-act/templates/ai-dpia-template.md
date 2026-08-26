---
type: template
template: dpia
regulation: GDPR Art. 35
---

# AI Data Protection Impact Assessment (DPIA)

Record every AI processing that is "likely to result in a high risk to the rights
and freedoms of natural persons" (GDPR Art. 35(1)). AI systems cross this
threshold more often than most processing: they are new technology by
definition, frequently evaluate or score people, and process personal data at
scale during training, fine-tuning, retrieval, and inference.

## 1. Screening — is a DPIA required?

Check all that apply:

- [ ] Systematic and extensive evaluation of personal aspects, including profiling (Art. 35(3)(a))
- [ ] Large-scale processing of special categories (Art. 9) or criminal-offence data (Art. 10)
- [ ] Systematic monitoring of a publicly accessible area on a large scale
- [ ] Innovative technology / novel deployment ("new technologies" trigger)
- [ ] Automated decision-making with legal or similarly significant effect (Art. 22)
- [ ] Processing of vulnerable data subjects (employees, children, patients)

Any box checked → proceed. None checked → document the decision not to run a
DPIA and the reasoning (Art. 35(5) cumulative screen).

## 2. System description

| Field | Detail |
|-------|--------|
| Name / version | |
| Purpose (intended use) | |
| Provider / deployer role | |
| AI capability (classification, generation, scoring, agentic) | |
| Human oversight model | |
| Deployment date / owner | |

## 3. Data flows

- [ ] Describe the data: categories, sources, data subjects, volume, retention.
- [ ] Map each stage — collection, training/fine-tuning, inference, feedback, deletion.
- [ ] Identify any special-category or children's data.
- [ ] Record transfers (controller↔processor, processor sub-processors, third countries).
- [ ] List the processing parties and their roles.

## 4. Necessity & proportionality (Art. 35(7)(b))

- [ ] Why is personal data (rather than anonymous/synthetic data) needed?
- [ ] Is the processing the least-intrusive way to achieve the purpose?
- [ ] Are data minimised, purpose-limited, and retained only as needed?

## 5. Risk assessment (Art. 35(7)(c))

For each of: **discrimination**, **accuracy/erroneous output**, **opacity &
explainability**, **loss of confidentiality**, **loss of autonomy /
manipulation**, **security**, assess:

| Risk | Likelihood | Severity | Existing controls |
|------|-----------|----------|-------------------|
| | | | |

## 6. Mitigations (Art. 35(7)(d))

- [ ] Measures to address each residual risk above
- [ ] Owner and due date per measure
- [ ] Controls that will make remaining risk acceptable

## 7. Consultation & sign-off

- [ ] DPO consulted (mandatory, Art. 35(2))
- [ ] Data subjects / representatives consulted where relevant
- [ ] Residual risk accepted by (controller) — name, date
- [ ] Re-assessment trigger (material change, 3-yearly review)

---

**Note:** Where the same system is also high-risk under the EU AI Act (Art. 6),
run this DPIA alongside the FRIA (`fria-template.md`) and the conformity /
technical-documentation record (`model-card-template.md`); one assessment is no
substitute for the other.