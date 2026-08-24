# AI Officer Playbook — what to actually do

You are the central person for AI governance, compliance and shadow-AI control. This is the operating model.

## Your standing responsibilities

1. **AI literacy (Art. 4):** ensure staff who build/use AI are trained, in proportion to role (developers vs users) and deployment context. Document the training evidence.
2. **Inventory:** maintain a live register of every AI system/tool in use (internal + SaaS/embedded), with risk tier, role, data processed.
3. **Classification:** assign each use case a risk tier (verboten / hochrisiko / begrenzt / minimal) — see `checklists/risk-classification-checklist.md`.
4. **Policies:** own the KI-Richtlinie (AI policy), AUP, vendor checklists, approval process.
5. **Oversight & audits:** ensure human oversight is real, run periodic compliance audits.
6. **Interfaces:** coordinate with DPO (DSFA), CISO (security), compliance, works council, procurement.
7. **Authorities & incidents:** prepare for market-surveillance contact; run the serious-incident process (Art. 73).
8. **Shadow AI:** continuously detect and remediate unauthorized use.

## The 7-phase governance roadmap

1. **Preparation & awareness** — management briefing, AI inventory, first risk estimate, governance structure
2. **Draft the KI-Richtlinie** — AI-Act + ISO 42001 aligned; roles, processes, risk assessment, principles; align with DPO/HR/procurement/works council
3. **Detailed risk assessment & classification** — tier every system; log in a central AI register
4. **Implement high-risk obligations** — risk-management system (ISO 31000/42001), data governance, tech documentation + logging, human oversight, cybersecurity, conformity + CE
5. **Registration, monitoring & evidence** — EU-DB registration, post-market monitoring, incident reporting, internal audits
6. **Training, communication & culture** — eLearnings, awareness campaigns, an AI ombudsstelle (help desk)
7. **Audit, adaptation, continuous improvement** — annual audits, lessons learned, keep the policy living

## KI-Richtlinie: whitelist vs blacklist

| | Whitelist (default-deny) | Blacklist (default-allow) |
|--|--------------------------|---------------------------|
| Risk | Controlled (only reviewed tools) | Higher — anything ships by default |
| Speed/innovation | Slower | Fast, bottom-up ideas flow |
| Governance effort | Lower per tool, but review bottleneck | Higher, scattered tools |
| Shadow AI | Lower (clear official path) | Low *by definition* but unvetted risk |
| Data protection | Strong | Weaker until an incident |

Choose per context: default **whitelist** for regulated/sensitive environments; blacklist only in low-regulation, high-literacy teams.

## Incident & escalation flow (Art. 73)

1. Detect a serious incident (or a staff report — protect the reporter, Art. 87 / HinSchG)
2. Triage: is it a "serious incident" (risk to health/safety/fundamental rights)?
3. Report to market-surveillance authority: 15 days (probable link) / 2 days (otherwise)
4. Coordinate with the provider (Art. 20 corrective action) and DPO (if personal-data breach → Art. 33 GDPR in parallel)
5. Document: timeline, causes, measures, notifications.

## Standing questions a good AI Officer asks about any new AI use case

- What is it? (AI system at all?) · Who are we? (role) · Which tier? (risk) · What obligations follow? · What data? (GDPR basis, special categories) · Who oversees it? (human oversight) · How do we document/register? · What happens on failure?