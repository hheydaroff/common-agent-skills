---
name: reverse-engineer-product
description: "Reverse-engineer an external product, service, feature or business you do not have source for: research it, observe the live thing, decompose it to first principles, and produce an anatomy plus a replication blueprint. Use for 'reverse engineer Gamma AI / Airbnb / Stripe payments', 'tear down X', 'how does X actually work under the hood', 'what is X's architecture', 'how would we build or clone X', or a competitor/feature deep-dive. Evidence-first: every claim is tagged observed / sourced / inferred / prior-knowledge, with an unknowns ledger. NOT for a source repo you already have (understand-codebase, how, why), NOT for your own product's behaviour spec (product-description), and no binary disassembly tooling."
---

# Reverse-engineer a product

Take a product you can only see from the outside and work out how it is built, why it works, and what it would take to rebuild it. The output is an **anatomy** (how it works, from first principles) and a **replication blueprint** (how we would build the same behaviour).

Method adapted from [morluto/rea](https://github.com/morluto/rea) (MIT): evidence ledger, observation vs inference vs unknown, cheapest-channel-first, claims reconciled against the running thing. REA's binary/decompiler tooling is deliberately **not** part of this skill. See [ATTRIBUTION.md](ATTRIBUTION.md).

## Not this skill

| Situation | Use instead |
|---|---|
| You have the source repo | `understand-codebase`, `how`, `why` |
| Describe behaviour of **our own** product | `product-description` |
| GTM / positioning vs a competitor | `product-launch` |
| Disassemble a native binary or APK | out of scope; say so, do not improvise |

## The one rule: provenance on every claim

The model "knows" Airbnb and Stripe from training data. That recall is the main failure mode: fluent, plausible, stale or wrong. Tag every claim:

| Tag | Meaning | May appear in the blueprint? |
|---|---|---|
| **[O]** observed | You looked at the live product or a fetched artifact in this session. Cite the observation ID. | yes |
| **[S]** sourced | A document says so. Cite URL, date, author. Vendor marketing is not engineering fact. | yes, with the source |
| **[I]** inferred | Reasoned from O/S. State the reasoning and what would falsify it. | yes, flagged as inference |
| **[P]** prior | Model memory. Untested. | **no**: promote it to O/S or park it in the unknowns register |

Never write a sentence about how the target works before you have collected evidence. First dump what you think you know into a table tagged [P], then try to promote or kill each row.

Bounded negatives stay bounded: "no public pricing page found on 2026-10-14" is not "it is free". Never claim you inspected something you only recalled.

## Modes

- **A. Full teardown** (default): anatomy + replication blueprint.
- **B. Mechanism trace**: "how does Stripe's payment intent flow work?" One mechanism, followed end to end (trigger, request, state change, result). Skip the moat and economics layers.
- **C. Replicate only**: the user already understands the target. Go to Step 5 using the user's description, but tag everything [P] until verified.
- **D. Compare**: two competitors, or one product across versions. Run Steps 1-3 on both, then diff the ledgers. Static differences are candidates, not causes.

## Process

### Step 0: Scope (one short message, default rather than stall)
1. **Target identity.** If the user said only "that app" or an ambiguous name, ask which. Never pick a target on their behalf.
2. **Question checklist.** Turn the request into 5-10 numbered questions, each with the evidence that would answer it (see [anatomy-first-principles.md](references/anatomy-first-principles.md) for the layer questions). This is the spine; Step 6 closes it.
3. **Goal and depth.** Understand only, evaluate a competitor, or clone? Clone raises the bar for Step 5.
4. **Guardrails.** Public information and your own accounts only. See Guardrails below.

### Step 1: Public sweep (claims layer, cheap)
Walk the channel ladder in [evidence-channels.md](references/evidence-channels.md), cheapest first: docs, API reference, changelog, status page, privacy policy and subprocessor list, job posts, engineering talks, SDKs and OSS, filings, patents, third-party teardowns. Run searches in **this** session; subagents have no web tools and silently answer from training data.

### Step 2: Hands-on observation (runtime layer)
Use the product. Free tier, your own account. Trace **one canonical transaction** end to end (a prompt becomes a deck, a search becomes a booking, a card payment becomes a payout). Capture network calls, error messages, headers, bundle strings, timings. Recipes in [runtime-observation.md](references/runtime-observation.md).

### Step 3: Reconcile
Compare Step 1 claims with Step 2 behaviour. A mismatch is a finding, not noise: report both sides and which you trust. Update the ledger ([teardown-report-template.md](references/teardown-report-template.md)).

### Step 4: Anatomy from first principles
Strip the UI and name the irreducible job, then rebuild the system from that job: flow, layers, data model, the hard 20%, moat, unit economics, weak spots. Delegate the decomposition technique to `first-principles-thinking`. Full model in [anatomy-first-principles.md](references/anatomy-first-principles.md).

### Step 5: Replication blueprint
Parity ladder, subsystem build/buy/OSS decisions, a spike on the riskiest mechanism, and a verification table (observation vs our behaviour). Details in [replication-blueprint.md](references/replication-blueprint.md). Keep **observed behaviour** and **our design choices** in separate sections.

### Step 6: Close
Revisit the Step 0 checklist and mark each question answered / partial / unresolved with its evidence. Do not call the teardown complete while a required question is open. Write `docs/TEARDOWN_<target>-<yyyy-mm>.md` (repo `docs/` convention; `~/` only with no repo). Summarise in plain language, tied to ledger IDs.

## Reference files

| File | When to load |
|---|---|
| [evidence-channels.md](references/evidence-channels.md) | Step 1, and any time you need to know where a fact could come from, what a channel can and cannot prove, or which search tool works here |
| [runtime-observation.md](references/runtime-observation.md) | Step 2: driving the live product, network capture, bundle mining, stack fingerprinting, mobile/desktop |
| [anatomy-first-principles.md](references/anatomy-first-principles.md) | Step 4: layer-by-layer anatomy and the question set |
| [replication-blueprint.md](references/replication-blueprint.md) | Step 5 and Mode C |
| [teardown-report-template.md](references/teardown-report-template.md) | Step 3 ledger format and the Step 6 output skeleton |

## Hand-offs

`first-principles-thinking` (decomposition) · `exa` / `tavily` / `summarize` (research, PDFs, YouTube) · `browser-tools` (live web) · `computer-use-peekaboo` (native/desktop UI) · `architecture-diagram` / `visual-explainer` (anatomy diagrams) · `prototype` (spike the risky mechanism) · `grill-me` (stress-test the plan) · `prd-creator` → `prd-to-spec` → `spec-to-tasks` (turn the blueprint into a build).

## Guardrails

- Public information and your own accounts. No auth bypass, credential stuffing, other users' data, or paywall circumvention.
- Probing is a handful of requests, never load. Rate-limit checks stop at the first 429.
- If the ToS forbids automated access or reverse engineering, say so in the report and stop the automated part. Desk research and manual use remain fine.
- Redact tokens, emails and user IDs from captures before they reach the report.
- Understanding is not freedom to operate. The blueprint flags patent and trade-secret risk; copying brand, copy, assets or training data is out of scope.
