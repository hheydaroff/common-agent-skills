
# Stakeholder Update

Generate concise, actionable stakeholder updates tailored to the audience. The most common mistake in status updates is burying the lead — always start with the most important thing.

## Workflow

### 1. Determine Update Type and Audience

Ask two questions:

**Type** — what kind of update:
- **Weekly**: Progress, blockers, next steps
- **Monthly**: Trends, milestones, strategic alignment
- **Launch**: Feature/product announcement with impact
- **Ad-hoc**: Escalation, pivot, major decision, incident

**Audience** — who reads it:
- **Executives / Board**: Outcome-focused, brief, strategic framing
- **Engineering**: Technical detail, blockers, decisions needed
- **Cross-functional partners**: Dependencies, shared goals, asks
- **Customers / External**: Benefits-focused, no internal jargon

If the user wants multiple audiences, generate separate versions from the same source material.

### 2. Gather Context

Ask the user for:
- What was accomplished since last update
- Current blockers or risks
- Key decisions made or pending
- What's coming next

If working inside a repo, scan recent commits, PRs, and issues to pre-fill context. Offer your summary and let the user correct/extend.

### 3. Generate the Update

Apply the appropriate template below. Then ask:
- Does the tone/emphasis need adjusting?
- Anything to add or remove?
- Want versions for other audiences?


## Templates by Audience

### Executive / Leadership

Executives want: strategic context, progress against goals, risks that need their help, and specific asks. **Keep under 200 words.**

```markdown
**Status:** [🟢 On Track / 🟡 At Risk / 🔴 Off Track]

**TL;DR:** [One sentence — the single most important thing to know]

**Progress:**
- [Outcome achieved, tied to goal/OKR]
- [Milestone reached, with impact]
- [Key metric movement]

**Risks:**
- [Risk]: [Mitigation plan]. [Ask if needed].

**Decisions needed:**
- [Decision]: [Options with your recommendation]. Need by [date].

**Next milestones:**
- [Milestone] — [Date]
```

**Rules for exec updates:**
- Lead with the conclusion, not the journey
- Status color reflects YOUR honest assessment — Yellow is good risk management, not failure
- Only include risks you need help with
- Asks must be specific: "Decision on X by Friday" not "support needed"
- Frame everything as outcomes, not activities

### Engineering Team

Engineers want: clear priorities, technical context, blockers resolved, and decisions that affect their work.

```markdown
**Shipped:**
- [Feature/fix] — [Link]. [Impact if notable].

**In progress:**
- [Item] — [Owner]. [Expected completion]. [Blockers if any].

**Decisions:**
- [Decision made]: [Rationale]. [Link to ADR if exists].
- [Decision needed]: [Context]. [Options]. [Recommendation].

**Priority changes:**
- [What changed and why]

**Coming up:**
- [Next items] — [Why these are next]
```

**Rules for engineering updates:**
- Link to specific tickets, PRs, and documents
- When priorities change, explain why — engineers buy in when they understand the reason
- Be explicit about what's blocking them and what you're doing to unblock
- Don't waste their time with info that doesn't affect their work

### Cross-Functional Partners

Partners (design, marketing, sales, support) want: what's coming that affects them, what you need from them, and how to give input.

```markdown
**What's coming:**
- [Feature/launch] — [Date]. [What this means for your team].

**What we need from you:**
- [Specific ask] — [Context]. By [date].

**Decisions made:**
- [Decision] — [How it affects your team].

**Open for input:**
- [Topic] — [How to provide feedback].
```

### Customer / External

Customers want: what's new, what's coming, and how it benefits them.

```markdown
**What's new:**
- [Feature] — [Benefit in their terms]. [How to use it / link].

**Coming soon:**
- [Feature] — [Expected timing]. [Why it matters to them].

**Known issues:**
- [Issue] — [Status]. [Workaround if available].

**Feedback:**
- [How to share feedback or request features]
```

**Rules for customer updates:**
- Zero internal jargon, ticket numbers, or technical implementation details
- Frame everything as what they can now DO, not what you built
- Be honest about timelines — "later this quarter" beats a date you might miss
- Only mention known issues if customer-impacting with a resolution plan

### Board

Board members want: metrics, strategic position, and material risks. **Under 150 words.**

```markdown
**Key Metrics:**
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| [North Star] | [Value] | [Target] | [↑/↓/→] |
| [Revenue/Growth] | [Value] | [Target] | [↑/↓/→] |

**Strategic Highlights:**
- [1-2 sentences on most significant progress]

**Material Risks:**
- [Risk with mitigation or ask]

**Decision/Approval Needed:**
- [If any — otherwise omit this section]
```


## Status Framework

### Green / Yellow / Red

| Status | Meaning | When to use |
|--------|---------|-------------|
| 🟢 Green | On track, no significant risks | Things are genuinely going well — not as a default |
| 🟡 Yellow | At risk, mitigation underway | At FIRST sign of risk — the earlier you flag, the more options exist |
| 🔴 Red | Off track, needs intervention | You've exhausted your own options and need escalation |

**Changing status:**
- Move to Yellow early — proactive, not reactive
- Move to Red when you genuinely need help, not when it's too late
- Move back to Green only when risk is resolved, not paused
- Always document what changed when status changes


## Risk Communication (ROAM)

When reporting risks, classify each one:

| Category | Meaning | What to communicate |
|----------|---------|---------------------|
| **Resolved** | No longer a concern | How it was resolved |
| **Owned** | Someone is actively managing it | Owner + mitigation plan |
| **Accepted** | Known, proceeding without mitigation | Rationale for acceptance |
| **Mitigated** | Actions reduced risk to acceptable level | What was done |

### Communicating a Risk

1. **State clearly**: "There is a risk that [thing] happens because [reason]"
2. **Quantify impact**: "If this happens, the consequence is [impact]"
3. **State likelihood**: "[Likely/possible/unlikely] because [evidence]"
4. **Present mitigation**: "We are managing this by [actions]"
5. **Make the ask**: "We need [specific help] to reduce this risk"

**Anti-patterns:**
- Burying risks in good news
- Being vague: "There might be some delays" — specify what, how long, and why
- Presenting risks without mitigations
- Waiting too long — a risk communicated early is a planning input; communicated late is a fire drill


## Multi-Audience Mode

When the user needs to communicate the same progress to multiple audiences:

1. Gather the raw context once
2. Generate each audience version sequentially
3. Ensure consistency — facts don't contradict across versions
4. Adjust altitude: exec gets outcomes, eng gets details, customers get benefits

Example: A feature launch might produce:
- **Exec**: "Shipped SSO. Enterprise win rate should improve 15%."
- **Engineering**: "SSO merged (PR #847). SAML + OIDC supported. Monitoring dashboard live."
- **Customer**: "You can now log in with your company credentials. No more separate passwords."


## Tips

- **Lead with the most important thing.** If there's bad news, put it first — don't hide it after good news.
- **Match length to attention.** Executives get a few bullets. Engineers get the details they need. Customers get clarity.
- **Asks must be actionable.** "We need help" is not an ask. "We need a decision on X by Friday" is.
- **Don't report activities — report outcomes.** "Had 14 standups" is not progress. "Shipped X which moved Y metric" is.
- **Status optimism kills trust.** One honest Yellow builds more credibility than three false Greens followed by a sudden Red.
- **Frequency beats length.** A short weekly update is better than a long monthly novel.
- **If nothing changed, say so.** "No update — tracking to plan" is a valid status. Don't pad.
