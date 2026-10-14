# Replication blueprint

Turns the anatomy into a plan to rebuild the **behaviour**. Not the code, not the brand, not the content. Two sections stay strictly separate in the output:

- **Observed behaviour** (what the target does; ledger IDs, tags [O]/[S]/[I]).
- **Our design choices** (what we would build; every one justified, none disguised as observation).

If a design choice rests on a [P] claim, stop and promote it first.

## 1. What are we replicating?

Pick one; the answer sets the bar:

| Goal | Bar |
|---|---|
| Learn from it | none; skip this file |
| Match one flow (feature spike) | behavioural parity on the canonical transaction |
| Internal tool replacing a SaaS seat | parity on the 20% of features actually used |
| Competing product | parity on the core loop, plus a reason to switch (Layer 9 weaknesses) |

## 2. Parity ladder

Climb one rung at a time; ship at the lowest rung that meets the goal.

| Rung | Meaning | Done when |
|---|---|---|
| P0 | **Behavioural parity on the canonical transaction** | same input class gives output of comparable quality, shape and latency class |
| P1 | Core loop complete | create, edit, share/export, pay, as in the trace |
| P2 | Ecosystem | integrations, API/SDK, import/export, templates |
| P3 | Scale and ops | multi-tenant isolation, SLOs, compliance, support |

## 3. Subsystem decisions

For each box from Layer 3, one row. **Never clone what you can rent**, unless that subsystem is the moat or the hard 20%.

| Subsystem | Target does (tag) | Options for us | Decision | Why |
|---|---|---|---|---|
| Auth | ... | managed (Clerk/Auth0), library (Auth.js), self | | |
| Payments | ... | Stripe/Adyen/Paddle (merchant of record?) | | |
| Models | ... | hosted API, routed gateway, self-host | | |
| Jobs / workflow | ... | queue lib, Temporal, cloud workflow | | |
| Data | ... | Postgres(+pgvector), managed search, blob store | | |
| Realtime | ... | SSE, websockets, CRDT lib | | |
| Rendering / export | ... | existing OSS engine vs custom | | |

Substitute where their constraint isn't ours. They run at ten-million users; we start at zero, so defer sharding, multi-region and heavy autoscaling. Keep what the **user-visible behaviour** depends on.

## 4. Spike the riskiest mechanism first

1. List the load-bearing unknowns and the hard 20% from the anatomy.
2. Pick the one whose failure kills the project.
3. Write an **acceptance test derived from an observation**, not from taste:
   *"From a 2-page brief, produce a 10-slide deck in under 60 s with no text overflow on 9 of 10 prompts"* where the 60 s and the layout quality are taken from the target's observed output.
4. Build a throwaway spike (`prototype` skill) that tries to pass it. Report pass/fail, measured numbers, cost per run.

A failed spike is a valid outcome; it moves the "feasible?" answer from guess to measurement.

## 5. Verification table

Port of REA's idea: a reconstruction is verified against a **finite list of declared, comparable claims**, never against "equivalent overall".

| # | Observation (ID) | Input | Target result | Our result | Match? | Notes |
|---|---|---|---|---|---|---|

A pass covers only the rows listed. Rows we cannot test yet stay in the table as `untested`. Rerun the table after each rung.

## 6. Cost and effort

Give ranges, state assumptions, label confidence:

```
Build effort    P0: X-Y person-weeks    P1: ...      (confidence: L/M/H, why)
Run cost        per unit: tokens/compute/storage/fees  -> monthly at 100 / 10k / 1M units
Biggest cost lever   what would make this 10x cheaper
Break-even      price x volume vs fixed cost
```

Compare with the target's economics (Layer 7). If our unit cost is above their price, say so.

## 7. What not to copy

- Branding, copy, templates, illustrations, trademarks.
- Their training data, user data, proprietary datasets.
- Features nobody used in the trace (check changelog: shipped once, rarely mentioned).
- Their accidental complexity (legacy compat, scale workarounds).
- Anything behind a ToS clause or patent claim flagged in the ledger. Flag it; get legal review before building.

## 8. Risks and unknowns

| Risk / unknown | Likelihood | Impact | Evidence that would close it | Cost to get |
|---|---|---|---|---|

Include: ToS or IP exposure, vendor dependency (single model provider), quality gap, support burden, regulatory class (GDPR, payments licensing, EU AI Act risk class via `eu-ai-act`).

## 9. Sequenced plan

```
Week 0   spike (Section 4) -> go / no-go with numbers
Rung P0  canonical transaction, verification table rows 1..n pass
Rung P1  core loop
...
```

Hand off: `grill-me` to stress-test the plan, `prd-creator` → `prd-to-spec` → `spec-to-tasks` for the build, `product-launch` for positioning against the target, `design-an-interface` for the API surface we expose.
