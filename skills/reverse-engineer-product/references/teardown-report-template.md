# Teardown report template

Output path: `docs/TEARDOWN_<target>-<yyyy-mm>.md` (repo `docs/`; `~/` only when there is no repo). Raw, redacted captures: `docs/teardown/`. Keep the report scannable; bulk payloads stay in the capture files and are cited by ID.

## Evidence ledger format

Maintain this from Step 1 onward, not at the end. One row per claim that matters.

```
ID   | Claim                                   | Tag | Grade | Source (URL / obs ID)        | Date       | Confidence | Boundary / what it doesn't show
F1   | API is REST, versioned /v1              | O   | A     | O3 network capture           | 2026-10-14 | high       | free tier, EU region only
F2   | Uses Postgres + pgvector                | S   | B     | job post (url)               | 2026-09-30 | medium     | posts lag reality
F3   | Sharded by workspace                    | I   | -     | F1 ids carry ws_ prefix (O3) | 2026-10-14 | low        | would be falsified by cross-ws id reuse
F4   | Runs Claude for generation              | P   | -     | model memory                 | -          | unverified | promote or park in U-list
```

Rules: no row without a tag; [P] never feeds the blueprint; bounded negatives carry their bound ("not found in docs, changelog, bundle on 2026-10-14").

## Unknowns register

```
ID | Question                         | Why it matters (which decision) | Evidence that would close it | Cost to get | Status
U1 | Which models serve generation?   | cost model, quality bar          | bundle strings, latency probe | low         | open
```

Statuses: `open`, `answered (F#)`, `unreachable` (needs authority we don't have, e.g. internal access).

## Question checklist (from Step 0)

```
Q1 <question>      -> answered / partial / unresolved    evidence: F2, F5, O3
```

Do not call the report complete while a required question is unresolved. Keep "partial" honest.

## Report skeleton

```markdown
# Teardown: <target>  (<yyyy-mm-dd>)

## 0. Scope
Target, version/tier/region observed, goal (understand / evaluate / clone), guardrails applied, limits of access.

## 1. Summary
10 lines max. How it really works in plain language; the 3 things that surprised us; the verdict on replicability.

## 2. Irreducible job and canonical transaction
Layer 1 and Layer 2 tables. Diagram of the flow.

## 3. Anatomy
Layers 3-9 from anatomy-first-principles.md, each statement with [tag] and ledger ID.
System diagram (dashed = unevidenced).

## 4. Data model and API surface
Entities, API surface table, ID formats.

## 5. Hard 20%, moat, unit economics, weak spots
Concise tables. Ranges and assumptions for every number.

## 6. Claims vs observation
Mismatches found in Step 3: what they say, what it does, which we trust and why.

## 7. Replication blueprint
Observed behaviour (read-only recap) | Our design choices. Parity ladder, subsystem decisions, spike + acceptance test, verification table, cost/effort, what not to copy, risks, sequenced plan.

## 8. Evidence ledger
Table (above).

## 9. Unknowns register
Table (above).

## 10. Checklist closure
Q1..Qn with status.

## Appendix
Observation log (O#, how produced), links to docs/teardown/ captures, queries run.
```

## Plain-language close

End the chat reply with 5-8 lines: what it is, how it works, the part that is hard, what a rebuild takes, the biggest unknown, and the path to the report. Tie claims to ledger IDs, not to confident prose.
