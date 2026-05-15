# Example Session: 7-Day Retention (Discovery Mode / OST)

A complete discovery-mode walkthrough. Shows the Opportunity Solution Tree flow from outcome through experiments.

## Input

> "Our 7-day retention is at 22%. We need to get it to 35% this quarter. I have interview notes and some analytics but I'm not sure what to focus on."

## Step 0 — Route

> **Agent:** This sounds like a discovery question — you have an outcome to improve but aren't sure which problem to solve. I'll run an Opportunity Solution Tree to map the space. Confirm?
>
> **User:** Yes, discovery mode.

## D1 — Define the desired outcome

> **Agent:** Let me confirm the outcome: "Increase 7-day retention from 22% to 35% by end of Q2." Is that right? And is this within your team's direct influence?
>
> **User:** Yes, we own the onboarding and core product experience. 35% by June 30.

Outcome locked: **Increase 7-day retention from 22% → 35% by June 30.**

## D2 — Map opportunities

> **Agent:** What do you know about why users drop off? Share your research — interview quotes, analytics funnels, support themes.
>
> **User:** From 8 interviews last month:
> - 5/8 said they "didn't know what to do after signing up"
> - 3/8 said they "couldn't get their team on board" — individual value wasn't enough
> - 4/8 said the daily email notifications felt spammy and they unsubscribed/churned
> - Analytics shows 60% of users never complete the setup wizard (drop at step 3 of 5)
> - Support tickets: "how do I invite my team?" is top question

> **Agent:** Here are the opportunities I'm extracting — all framed from the customer's perspective:
>
> 1. **"I don't know what to do after signing up"** — 5/8 interviews, 60% wizard abandonment at step 3
> 2. **"I can't get value alone — I need my team here"** — 3/8 interviews, top support ticket is team invites
> 3. **"The notifications feel spammy and push me away"** — 4/8 interviews, notification → unsubscribe → churn pattern
> 4. **"The setup process asks too much before I see value"** — 60% drop at step 3 (inferred from wizard data)
> 5. **"I forget about the product after day 1"** — hypothesis from low return-visit rate (day 2–7 analytics)
>
> Note: Opportunities 1 and 4 overlap (both about first-session friction). Want me to merge them or keep separate?
>
> **User:** Keep them separate — "not knowing what to do" is a guidance problem, "too much before value" is a flow problem.

## D3 — Prioritize opportunities

> **Agent:** Let me score these. Based on your interview frequency and analytics severity:
>
> | # | Opportunity | Importance | Satisfaction | Score | Tier |
> |---|---|---|---|---|---|
> | 1 | "I don't know what to do after signing up" | 0.9 | 0.2 | 0.72 | 🔴 |
> | 4 | "Setup asks too much before I see value" | 0.8 | 0.2 | 0.64 | 🔴 |
> | 2 | "I can't get value alone — need my team" | 0.7 | 0.3 | 0.49 | 🟡 |
> | 3 | "Notifications feel spammy" | 0.6 | 0.3 | 0.42 | 🟡 |
> | 5 | "I forget about the product after day 1" | 0.5 | 0.4 | 0.30 | 🟢 |
>
> Top 2 are clearly Opportunities 1 and 4. Want to include Opportunity 2 as a third, or focus on just the top 2?
>
> **User:** Top 2 plus Opportunity 2. Team activation feels important strategically.

Pursuing: **Opportunities 1, 4, and 2.**

## D4 — Generate solutions

> **Agent:**
>
> **Opportunity 1: "I don't know what to do after signing up"**
>
> | # | Solution | Perspective | Rationale |
> |---|---|---|---|
> | S1 | Interactive checklist with contextual tooltips | Designer | Progressive guidance without leaving the product |
> | S2 | Personalized "first 5 minutes" flow based on role/goal selection | PM | Different users need different first actions |
> | S3 | AI onboarding assistant that answers "what should I do?" in real-time | Engineer | Replaces static flows with dynamic guidance |
> | S4 | "Quick win" template — pre-populated workspace so value is immediate | PM | Skip the blank-canvas problem entirely |
>
> **Opportunity 4: "Setup asks too much before I see value"**
>
> | # | Solution | Perspective | Rationale |
> |---|---|---|---|
> | S5 | Defer setup steps 3–5 until after first value moment | Designer | "Time to value" before "time to configure" |
> | S6 | Progressive profiling — collect setup data across first week, not upfront | PM | Spread the burden across natural touchpoints |
> | S7 | "Instant sandbox" — show a working demo environment, migrate to real when ready | Engineer | Value in 10 seconds, personalization later |
>
> **Opportunity 2: "I can't get value alone — need my team"**
>
> | # | Solution | Perspective | Rationale |
> |---|---|---|---|
> | S8 | One-click team invite with pre-filled context ("X invited you to work on Y") | PM | Reduce friction of the invite flow itself |
> | S9 | "Solo value path" — features that work for individuals, teasing team capabilities | Designer | Make solo use valuable; team is upgrade, not prerequisite |
> | S10 | Auto-detect organization (email domain) and suggest connections | Engineer | Remove the invite step entirely for same-domain users |

## D5 — Design experiments

> **Agent:** Let me design experiments for the most promising solutions:
>
> **Experiment 1: Validate S4 (Quick-win template)**
>
> | Field | Content |
> |-------|---------|
> | **Assumption** | Value — users who see a populated workspace in first session will return |
> | **Hypothesis** | Users given a pre-populated template will have ≥50% higher day-2 return rate than control |
> | **Method** | A/B test — 50% of new signups get a pre-populated workspace vs. blank |
> | **Metric** | Day-2 return rate |
> | **Success threshold** | ≥50% relative lift (control ~15% → treatment ≥22%) |
> | **Timeline** | 2 weeks (need ~500 signups per arm) |
> | **Skin-in-the-game** | Yes — real user behavior, not stated preference |
>
> **Experiment 2: Validate S5 (Defer setup steps)**
>
> | Field | Content |
> |-------|---------|
> | **Assumption** | Usability — users can still get value if steps 3–5 are deferred |
> | **Method** | Fake-door — remove steps 3–5 from wizard for 50% of users, track if they reach the "aha moment" (first meaningful action) without them |
> | **Metric** | % reaching first meaningful action within session 1 |
> | **Success threshold** | ≥ same rate as full-wizard completers (currently ~40% of the 40% who finish → 16% overall; treatment should hit ≥16% of their cohort) |
> | **Timeline** | 2 weeks |
> | **Skin-in-the-game** | Yes — real product usage |
>
> **Experiment 3: Validate S9 (Solo value path)**
>
> | Field | Content |
> |-------|---------|
> | **Assumption** | Value — solo users can find enough value to retain without team |
> | **Method** | Concierge — manually onboard 20 solo users with a "solo-first" flow, track 7-day retention |
> | **Metric** | 7-day retention of concierge cohort |
> | **Success threshold** | ≥30% 7-day retention (vs. current 22% baseline) |
> | **Timeline** | 10 days |
> | **Skin-in-the-game** | Yes — real usage over time |

## D6 — Full tree visualization

```
🎯 Outcome: Increase 7-day retention from 22% → 35% by June 30
│
├── 🔴 Opportunity 1: "I don't know what to do after signing up" (Score: 0.72)
│   ├── S1: Interactive checklist with contextual tooltips
│   ├── S2: Personalized "first 5 minutes" flow by role
│   ├── S3: AI onboarding assistant
│   └── S4: Quick-win template ← Experiment 1 (A/B, day-2 return ≥22%)
│
├── 🔴 Opportunity 4: "Setup asks too much before I see value" (Score: 0.64)
│   ├── S5: Defer steps 3–5 until after first value ← Experiment 2 (fake-door, ≥16%)
│   ├── S6: Progressive profiling across first week
│   └── S7: Instant sandbox with demo environment
│
└── 🟡 Opportunity 2: "I can't get value alone — need my team" (Score: 0.49)
    ├── S8: One-click team invite with context
    ├── S9: Solo value path ← Experiment 3 (concierge, 7-day ret ≥30%)
    └── S10: Auto-detect org by email domain
```

## D7 — Save artifact

Saved to `OST-retention-7day-2026-05-14.md`.

## D8 — Recommend next step

> **Agent:** Discovery complete. Three experiments designed — all runnable in parallel over 2 weeks.
>
> **Top opportunities:** "I don't know what to do after signing up" + "Setup asks too much before value."
> **Most promising solutions:** S4 (quick-win template) and S5 (defer setup steps) — both attack time-to-value from different angles.
>
> **Next steps:**
> 1. Run Experiments 1–3 in parallel (2 weeks)
> 2. After results: if S4 or S5 validate, transition to **Decision mode** to pick the technical approach for implementation
>
> Want me to set up the Decision mode tree for any of these solutions now, or wait for experiment results?
