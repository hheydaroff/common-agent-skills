---
type: template
template: agent-deployment-checklist
---

# AI Agent Deployment Checklist

Autonomous agents can act across systems — send messages, call APIs, read data,
run code. Work through this gate before any agentic system reaches production.
Items must be **evidenced**, not just acknowledged.

## 1. Scope & autonomy boundaries

- [ ] Explicit task scope: what the agent may and may not do
- [ ] Bounded tool set (allow-list of APIs/tools), least privilege per action
- [ ] Actions requiring human approval listed (money, external sends, writes to prod)

## 2. Human oversight (Art. 14)

- [ ] Human-in-the-loop for consequential actions; a named operator who can override
- [ ] Agent cannot mark its own outputs as approved
- [ ] Confidence/uncertainty surfaced before consequential steps

## 3. Data & access

- [ ] Data classification applied: which data the agent may read/write (see `references/data-governance-and-bias.md`)
- [ ] Secret handling: no keys in prompts; scoped credentials; rotation
- [ ] Personal data minimised; DPIA if the agent processes personal data

## 4. Security (OWASP LLM Top 10)

- [ ] Prompt-injection defences: untrusted content cannot steer the agent
- [ ] Output validation / sandboxing before the agent acts (no unsanitised code execution)
- [ ] Data-leakage control: no exfiltration of confidential data to external models

## 5. Logging & audit (Art. 12)

- [ ] Every action logged: who/what/when, inputs and outputs, tool calls
- [ ] Log retention + audit trail; replayable for incident review

## 6. Testing & rollback

- [ ] Canary / shadow runs; edge-case and adversarial tests
- [ ] Kill switch / rollback plan and a defined owner

## 7. Go-live & monitoring

- [ ] Post-deploy monitoring for drift, failures, unexpected actions
- [ ] Incident response mapping (see `templates/incident-report-template.md`)

**Owner / evidence link per line, then a go-live sign-off name + date.**