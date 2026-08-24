# Shadow AI — Detection & Remediation Checklist

Shadow AI = AI tools used by staff without company approval or knowledge.

## Risks (what you're protecting against)

- **DSGVO breach** — personal data leaves your control to an external provider without legal basis / DPA (AVV)
- **Loss of trade secrets / confidential data**
- **Copyright** infringement via output
- **Liability** without documentation or oversight

## Detect

- [ ] Survey teams: "which AI tools do you actually use?" (anonymous, blameless)
- [ ] Network/SSO logs for visits to known AI tool domains
- [ ] Expense/receipt scan for AI subscriptions
- [ ] Data-loss-prevention (DLP) alerts for large uploads to external services
- [ ] Interview works council / champions for hint of unofficial "ChatGPT clubs"

## Triage each tool

- [ ] What is it used for? · With what data? · By how many people?
- [ ] Is it a personal-data processing (→ GDPR) or trade-secret exposure (→ confidentiality)?
- [ ] Which risk tier if it were official? (→ risk-classification checklist)

## Remediate (in order)

1. [ ] **Stop the bleeding** — block the highest-risk tools (personal data / secrets) immediately
2. [ ] **Remediate** — offer an official, vetted equivalent (e.g. enterprise ChatGPT with DPA) so denial doesn't resurrect shadow use
3. [ ] **Publish** the approved-tools list (whitelist) in the KI-Richtlinie
4. [ ] **Train** — why it's harmful + what the safe path is
5. [ ] **Monitor** — recurring detection cadence (quarterly)

## Prevention (make shadow AI unnecessary)

- [ ] Clear, short "what's allowed / what's not" page
- [ ] Fast approval process (days, not months)
- [ ] Self-service vetted tools where safe
- [ ] Open reporting channel (no blame) + whistleblower protection (Art. 87 / HinSchG)

> **Principle:** people reach for shadow AI because the official path is slow or missing. Fix the path, not just the symptom.