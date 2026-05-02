# Example Session: Transactional Email

A complete `solution-ideator` walkthrough, abbreviated for readability. Real sessions will be longer — this shows the shape and the artifacts produced.

## Input

> "We need to send transactional email from our app — password resets, order confirmations, that kind of thing. Not sure how to approach it."

## Step 1 — Classify

> **Agent:** Are you asking me to (a) explore solutions to a problem, (b) evaluate a solution you've already picked, or (c) something else?
>
> **User:** (a). I don't have anything picked yet.

Classified: **`problem`**. Proceed to constraints.

## Step 2 — Gather constraints

> **Agent:** What does "solved" look like in 6 months? Be specific — metrics, user behaviours, or team outcomes.
>
> **User:** Emails arrive reliably (>99% delivery), password reset flow doesn't break, and we're not paying more than ~$100/month at our current volume of ~50k emails/month.
>
> **Agent:** What's non-negotiable? Stack, budget, timeline, compliance, team skills, infra.
>
> **User:** GDPR compliance is required — we're EU-based. We're on AWS. Small team (2 backend engineers), so minimal ops surface. Budget ceiling $150/month hard.
>
> **Agent:** Let me tag those:
> - `MUST`: GDPR-compliant email processing
> - `MUST`: budget ≤ $150/month at current volume
> - `SHOULD`: minimise ops surface (small team)
> - `SHOULD`: AWS-native (you're already there)
>
> Confirm the tags?
>
> **User:** Yes.
>
> **Agent:** Is there prior art — previous attempts, existing integrations, something that already failed?
>
> **User:** Nothing. Greenfield.
>
> **Agent:** Is this a one-way door or two-way? How painful is switching providers in 6 months?
>
> **User:** Two-way. We'd just swap SDKs if needed.

## Step 3 — Propose axes

> **Agent:** Candidate axes:
>
> 1. **Build vs. buy vs. integrate OSS** — determines where your small team's effort goes.
> 2. **Provider-specific vs. abstracted** — affects lock-in and cost of switching (your "two-way door" answer).
> 3. **Sync vs. async send** — affects request latency and failure modes.
> 4. **Templates in code vs. templates in provider** — affects who can edit email copy (devs only vs. PM/support).
> 5. **Single provider vs. multi-provider fallback** — affects reliability (your 99% target).
>
> Pick 2–3.
>
> **User:** 1, 2, 3.

## Step 4 — Expand the tree

With 3 binary axes, 8 combinations. Collapsed to 6 realistic branches (some combinations don't make sense — e.g., "build + provider-specific" is contradictory):

- **Branch A:** Build + abstracted + sync — in-process SMTP client with provider-agnostic interface.
- **Branch B:** Build + abstracted + async — internal queue + worker, abstracted interface.
- **Branch C:** Buy SaaS + provider-specific + sync — direct SES/Postmark SDK call from request handler.
- **Branch D:** Buy SaaS + provider-specific + async — SaaS provider's webhook-based queue.
- **Branch E:** Buy SaaS + abstracted + sync — SaaS behind a thin in-house wrapper.
- **Branch F:** Integrate OSS + abstracted + async — self-hosted Postal/Listmonk + queue.

## Step 5 — Prune

```
Branch                                Status        Reason
────────────────────────────────────  ───────────  ───────────────────────
A: Build + abstracted + sync          ❌ pruned    violates MUST: budget
                                                    (SMTP reputation +
                                                    compliance tooling
                                                    cost > $150/mo for a
                                                    small team to maintain)
B: Build + abstracted + async         ❌ pruned    same as A
C: Buy SaaS + prov-specific + sync    ✓ survives
D: Buy SaaS + prov-specific + async   ✓ survives
E: Buy SaaS + abstracted + sync       ✓ survives
F: Integrate OSS + abstracted + async ⚠ borderline violates SHOULD:
                                                    minimise ops surface
                                                    (self-hosting = more
                                                    ops) — penalty applied
```

3 survivors + 1 borderline. Under 50% pruned → proceed.

## Step 6 — Evaluate

|                              | C (SES direct sync) | D (SES async) | E (SES + wrapper) | F (self-host OSS) |
|------------------------------|---------------------|---------------|-------------------|-------------------|
| Hits success criteria        | ✓                   | ✓             | ✓                 | ~                 |
| SHOULD: minimise ops surface | ✓                   | ~             | ✓                 | ✗                 |
| SHOULD: AWS-native           | ✓                   | ✓             | ✓                 | ~                 |
| Reversibility                | ✗ hard              | ✗ hard        | ✓ easy            | ~                 |
| Implementation cost          | S                   | M             | S                 | L                 |

**Per-branch narrative:**

- **Branch C (SES direct, sync)** — Fastest to ship. But password-reset endpoints will block on SES's API latency (~100–400ms), and if SES has an incident the request fails. Provider-specific code means migrating to Postmark later means touching every caller. Cheap in cost, expensive in lock-in.
- **Branch D (SES async)** — Solves the latency and partial-failure problem, but adds SQS + a worker process for your 2-person team to monitor. For 50k/month (0.02/sec average), most sends don't need async — the latency hit in C is already fine for most flows.
- **Branch E (SES + thin wrapper)** — Same ship-speed as C, plus a ~50-line interface that makes provider swap trivial. Matches the two-way-door constraint. No queue, no operational overhead. Password-reset sync latency is still SES-bound but acceptable (<500ms worst case).
- **Branch F (self-host OSS)** — Eliminates the per-email provider cost entirely, but you inherit deliverability reputation, SPF/DKIM/DMARC tuning, bounce handling, and an additional service to run. For 2 engineers at 50k/month, the math doesn't work — provider cost (~$10–20/month at this volume on SES) is wildly cheaper than one engineer-day/month of ops.

## Step 7 — Recommend

> ## Recommendation: Branch E — SES behind a thin in-house wrapper
>
> **Why this one:** You're on AWS (SES is the cheapest option at your volume — ~$5/month for 50k emails), GDPR-compliant out of the box in eu-west-1, and two-way-door reversibility means the thin wrapper is the only divergence from "just use SES directly" — that wrapper buys you cheap migration later. Sync is fine at your volume; no queue to operate. Implementation: ~1 day.
>
> **What you're giving up:**
> - Password-reset endpoints will take 100–400ms longer than with pure async dispatch.
> - If SES has a regional incident, affected requests fail — no built-in fallback provider.
>
> **When you'd revisit this decision:**
> - If monthly volume exceeds 500k emails (async dispatch starts paying for itself operationally).
> - If the 99% delivery target slips because of SES incidents (multi-provider fallback becomes worth the complexity).
> - If team grows beyond 4 backend engineers (self-hosted OSS becomes reconsiderable).
>
> **Rejected alternatives (ADR-ready):**
> - **Branch C (SES direct):** chosen against because provider-specific code violates the two-way-door preference at near-zero cost to avoid (the wrapper is 50 lines).
> - **Branch D (SES async):** async adds operational surface your 2-person team can't justify at 50k/month volume.
> - **Branch F (self-host OSS):** ops cost dwarfs SES's ~$5/month at this volume; self-hosted email is a false economy below ~1M/month.
> - **Branches A & B (build from scratch, pruned):** violate `MUST: budget ≤ $150/month` once reputation and compliance tooling costs are included.

## Step 8 — Save artifact

Saved to `SOLUTION-TREE-transactional-email-2026-05-02.md` at repo root.

## Step 9 — Handoff

> **Agent:** Approach settled: **SES behind a thin in-house wrapper**. Recommend `design-an-interface` next — the wrapper's shape is the thing to design now. These are decided — don't re-ask:
>
> - Success criteria: 99% delivery, $100/mo at 50k emails/mo, password-reset reliable
> - MUST constraints: GDPR-compliant, budget ≤ $150/mo
> - Chosen approach: SES provider, sync dispatch, thin abstraction layer
> - Rejected: direct SES coupling, async queue, self-hosted OSS
>
> See `SOLUTION-TREE-transactional-email-2026-05-02.md`.
