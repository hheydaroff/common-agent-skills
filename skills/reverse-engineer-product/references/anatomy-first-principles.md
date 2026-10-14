# Anatomy from first principles

Goal: explain the product from the irreducible job outward, so the explanation survives removal of the UI, the brand and the incumbent's way of doing it. Decomposition technique: `first-principles-thinking` (Socratic questions, Five Whys, constraint mapping, inversion). This file is the product-specific structure to fill.

Every statement carries a tag ([O]/[S]/[I]/[P]) and a ledger ID. Layers with only [P] stay as open questions.

## Layer 1: the irreducible job

Strip name, UI and category. State what must be true for the product to exist.

```
JOB      "<person/org> needs <outcome> but <obstacle>."
NEED     the minimum capabilities that outcome requires (3-5 bullets)
WHY NOW  what changed that made it feasible or worth buying (model quality, regulation, cost curve, distribution)
ANALOGY  the shortcut label the market uses ("Uber for X") and the first place it fails
```

Examples: Airbnb = match a spare room to a stranger who needs it for a night, and make strangers trust each other with money and keys. Stripe = move money between a buyer and a seller across banks that don't talk, with failures that never double-charge. Gamma = turn a rough idea into a presentable slide deck faster than a person fits content to a layout.

## Layer 2: one unit of work, end to end

The canonical transaction from [runtime-observation.md](runtime-observation.md) §0, now annotated with the system underneath:

```
step | what the user sees | what the system must do | evidence | tag
```

Every later layer hangs off this table. A component that isn't on the path of some step is either secondary (admin, billing, analytics) or an undiscovered step.

## Layer 3: system anatomy

For each box state **what it is for, what evidences it, and what you assume**:

| Box | Question | Typical evidence |
|---|---|---|
| Client | web, native, extension, embedded widget? offline? | bundle, store listing |
| Edge / CDN / WAF | who fronts it, what is cached? | headers, DNS |
| API / gateway | REST, GraphQL, gRPC, versioned how? | API surface table, SDKs |
| Auth / identity | sessions, JWT, OAuth, SSO, org model? | cookies, OIDC doc, SDK |
| Core services | monolith or services? what is the domain split? | status page components, routes |
| Orchestration | queues, workflows, agents, schedulers? | latency shape, job posts, postmortems |
| Model / compute | which models, hosted where, routed how, cached? | bundle strings, subprocessors, latency, pricing |
| Data stores | relational, document, search, vector, blob, analytics? | subprocessors, job posts, SDK ids |
| Realtime | streaming, websockets, collaboration (CRDT/OT)? | network capture |
| Billing / metering | seats, credits, usage, invoicing, tax? | pricing, limits, 402/429 errors |
| Observability / ops | status page, incident history, regions | status page, postmortems |

Draw it only after most rows have evidence (`architecture-diagram` or `visual-explainer`). Mark unevidenced boxes dashed.

## Layer 4: data model

Entities, keys, relationships, lifecycles. Source: API surface table, ID formats, SDK types, error messages, URL structure.

```
Entity     key format        belongs to      lifecycle states     evidence
```

Look for: tenancy boundary (user, workspace, org), the central aggregate (deck, listing, charge), the append-only record (event, ledger entry, version), and what is soft-deleted. Money systems: look for idempotency keys and immutable ledger rows. Collaborative products: look for operation or version ids.

## Layer 5: the hard 20%

Which mechanisms carry the difficulty? Name them and say why they're hard. The answer decides whether a clone takes a weekend or three years.

| Product class | Usual hard part |
|---|---|
| Marketplace | cold-start supply, ranking/matching, trust and fraud |
| Payments | idempotency, reconciliation, compliance, bank connectivity, disputes |
| Generative content tool | quality control (layout/overflow/consistency), prompt-to-structure pipeline, cost per generation, evals |
| Collaboration | conflict resolution, permissions, sync |
| Search / feed | relevance, freshness, spam |
| Dev platform | reliability, backwards compatibility, docs/DX |

Heuristic: the hard part is wherever the vendor has patents, dedicated teams in job posts, or long postmortems.

## Layer 6: moat

Sort honestly into: data/network effect, supply side, distribution, brand/trust, switching cost, regulation/licences, cost/scale advantage, model or algorithm advantage, **or none** (first, fast and well-designed is clonable). For each claim state the evidence and whether a new entrant could neutralise it.

## Layer 7: unit economics

```
Revenue per unit    plan price / credits / take rate               [S] pricing page
Cost per unit       compute/tokens, payment fees, storage, support [I] from vendor price lists
Free-tier cost      what a non-paying user consumes before the cap [I] from limits
Gross margin        estimate with a range, show the arithmetic
Scaling driver      what makes cost grow: seats, tokens, GB, transactions
```

Back-compute from published prices (model token prices, cloud pricing, processor fees) and the observed per-transaction work (tokens in a streamed response, images generated, calls made). Always give ranges and the assumptions. A margin you cannot bound is an unknown.

## Layer 8: scale and org signals

Headcount and hiring mix, release cadence, region count, uptime history, customer logos, incident frequency. These tell you how much machine is behind the product and whether a small team can match the **current** version or only the early one.

## Layer 9: where it is weak

Review sites, store reviews, support forums, community threads, the changelog's bug fixes, status incidents. Cluster the complaints. Each cluster is an opening for a replica to be better, not just equal.

## Inversion and falsification (one pass, before closing)

- **Inversion:** "If I wanted this product to fail, what would I break?" The answers are the load-bearing parts. Compare with Layer 5.
- **Falsification:** for each [I] item, write the observation that would prove it wrong, and say if you can get it. Then either get it or downgrade confidence.
- **Analogy check:** where the report says "like X", replace with the mechanism. If you can't, you have an analogy, not understanding.

## Output of this step

A filled Layers 1-9 section of the report ([teardown-report-template.md](teardown-report-template.md)), a one-paragraph "how it really works" in plain language, and the list of load-bearing unknowns passed to the blueprint step.
