# Roles & Responsibilities — actors and the obligation catalogue

## The 6 actors (Art. 3)

| Role | Definition (core) | Core duties |
|------|-------------------|-------------|
| **Anbieter (provider)** — Nr. 3 | Develops OR has developed + places on market under own name/mark | Tech docs, conformity, CE, EU-DB registration, QM (Art. 16–17) |
| **Betreiber (deployer)** — Nr. 4 | Uses AI system **in own responsibility**, unless private/non-professional use | Human oversight, staff training, DSFA (Art. 26) |
| **Bevollmächtigter (representative)** — Nr. 5 | In EU, acts beside/for the provider toward authorities | Hold docs (10 yrs), cooperate with authorities (Art. 22) |
| **Einführer (importer)** — Nr. 6 | EU-established, first to place a third-country-branded system on EU market | Pre-placement verification (Art. 23) |
| **Händler (distributor)** — Nr. 7 | Supplies on EU market without being provider/importer (foreign mark) | Verification, storage conditions (Art. 24) |
| **Produkthersteller** — Art. 25 Abs. 3 | Product manufacturer whose product *is/contains* an AI system | May be treated as provider |

> **Betreiber test — 5 gates, all must hold:**
> 1. **Stelle** — a natural/legal person or other body acting independently.
> 2. **KI-System** — meets Art. 3 Nr. 1 (or a general-purpose AI *system*, Art. 3 Nr. 66).
> 3. **Verwendung** — deliberate, targeted use *with control over input & output data*. Merely consuming results without controlling the process = **not** a deployer.
> 4. **Geschäftstätigkeit** — commercial/business use. Purely private use = household exception (Art. 2 Abs. 10), excluded.
> 5. **Eigene Verantwortung** — own account + own risk. Includes SaaS (as long as you steer usage). Excludes the employee acting for the employer — **the employer is the deployer**, not the employee.

## Art. 25 — Quasi-provider (3 cases → treated as provider)

A distributor, importer, deployer or third party **becomes the provider** when they:
1. **(a)** put their **own name/mark** on an already-placed high-risk system;
2. **(b)** make a **substantial modification** to a high-risk system (it stays high-risk);
3. **(c)** change the **intended purpose** of a non-high-risk system so that it *becomes* high-risk.

> **Art. 25 Abs. 2 — "Ehemaliger Anbieter" (former provider):** once (a)/(b)/(c) occurs, the provider who *initially* placed the system **ceases to be its provider** and must cooperate with the new provider (share information + reasonably accessible technical access, minus trade secrets). Exception: the initial provider had explicitly declared the system must **not** be turned into high-risk.
> **Anbieter without self-development:** Art. 3 Nr. 2/3 covers "entwickelt **oder entwickeln lässt**" — you are the Anbieter even if you *commissioned* the build (placed under your own name). You don't have to code it yourself. (Mere *embedding* of a third-party system into your site, e.g. a chat widget, is unsettled — likely not enough on its own.)

> **Substantial modification (Art. 3 Nr. 23):** not foreseen in the original conformity assessment AND affects conformity. Examples: OS change, architecture rework (monolith→microservices), new training data, algorithm change, new domain, third-party plugins, hardware change.

**Decision tree for "foreign system":**
- own name/mark → **Anbieter** (Art. 25 a)
- substantially modified + own product → **Quasianbieter** (Art. 25 b)
- repurposed into high-risk → **Quasianbieter** (Art. 25 c)
- unchanged, no rebranding → **Händler**
- used internally, unchanged → **Betreiber**

## Provider obligations for high-risk (Art. 16–22)

| Art. | Obligation |
|------|-----------|
| 16 | Ensure compliance; name/address; QM; EU declaration; CE mark; registration; corrective actions; accessibility |
| 17 | Quality-management system |
| 18 | Keep documentation (**10 years**) |
| 19 | Keep automatically-generated logs (**≥ 6 months**) |
| 20 | Corrective action ("unverzüglich" = without culpable delay); inform authorities |
| 21 | Cooperate with authorities ("begründete Anfrage", intelligible language, official EU language) |
| 22 | Authorised representative (mandatory for non-EU providers) |

## Deployer obligations for high-risk (Art. 26 — key Absätze)

| Abs. | Obligation |
|------|-----------|
| 2 | Oversight only by **trained, competent persons** with adequate support |
| 4 | Use only **suitable, representative input data** |
| 5 | Monitor per instructions; inform provider/authority of risks |
| 6 | Keep logs (**≥ 6 months**) |
| 7 | **Inform worker representatives & affected employees BEFORE deployment** |
| 8 | Public bodies: register in EU database |
| 9 | Conduct **DSFA** where required |
| 10 | Remote biometrics: strict rules + judicial approval |
| 11 | **Inform affected persons that a high-risk AI system is used** |
| 12 | Cooperate with authorities |

## Fundamental-rights impact assessment (Art. 27)

Mandatory for deployers that are **public bodies or private bodies providing public services** (exception: critical digital infrastructure), plus deployers of:
- **credit-scoring** of natural persons
- **emergency-call triage / first-responder prioritisation**

Before first use; update on system changes; may reuse existing DPFIA/DSFA; report results to the market-surveillance authority.

## The AI Officer / KI-Beauftragter (context of Art. 4)

- **Not legally mandated** (unlike the DPO under Art. 37 GDPR) — but the practical answer to the Art. 4 AI-literacy duty.
- Core duties: ensure AI competence, monitor AI compliance (AI Act + GDPR + IP), run risk assessments & audits, draft policies (AUP / KI-Richtlinie), train staff, coordinate with DPO/CISO/compliance, liaise with authorities, keep shadow AI under control.

## The golden split (prevents the most common exam error)

> **Provider = build + document.** Technical documentation, CE marking, EU-DB registration, conformity assessment — *only* the provider (only the builder can document the internals).
> **Deployer = use + oversee.** Human oversight in practice, staff training, DSFA, worker information — *only* the deployer.