---
name: security-review
description: "Source-first security review of a codebase, API, service, CLI, library, daemon, agent/MCP server or IaC repo: find vulnerabilities that cross a real trust boundary, with evidence, severity, and the smallest fix. Use for 'security review', 'security audit', 'find vulnerabilities', 'is this safe', 'review this PR/diff for security', 'threat model this', 'check auth/injection/tenant isolation/prompt injection', or a full multi-agent audit with findings.json and REPORT.md. Guidance mode by default; full audit only when explicitly asked. Covers web/auth, client-side, AI/LLM/agents, cloud/IaC, supply chain, protocols/RPC, data isolation, desktop/mobile IPC, memory safety, resource exhaustion. NOT for compliance (eu-ai-act), general code quality (ponytail-review), or live pen-testing."
---

# Security Review

Find vulnerabilities that violate a real trust boundary, then give the owner source evidence,
priority and the smallest effective fix. Defensive and source-first. A candidate with no concrete
affected principal, resource or security outcome is not a finding.

Adapted from cloudflare/security-audit-skill (MIT); see `ATTRIBUTION.md`.

## Pick the mode first

| Mode | When | What you do |
|---|---|---|
| **Guidance** (default) | Security question, focused review, PR/diff review, triage of one suspected issue, "is this safe" | Use only the relevant principles + domain file below. No output dir, no artifacts, no phases. |
| **Full audit** | User explicitly says audit / pen-test a codebase, full / comprehensive / end-to-end review, or wants a report | Read `references/audit-workflow.md` and run it end to end. |

If it could be either, ask one question before creating files.

## Execution safety (both modes)

Source inspection is read-only. **Do not run target-controlled code** (builds, tests, scripts,
fixtures) unless an OS-enforced sandbox is in place: no external network, empty allowlisted
environment, read-only target, scratch-only writes, low CPU/memory/time limits. No sandbox means
no execution: report the decisive runtime fact as `needs_validation` with the smallest safe local
check. Never probe deployed endpoints, use real credentials or production data, publish
anything, stress availability, or go past the minimum effect that proves the defect.
Do not install dependencies.

## Core principles

**Require a boundary and a result.** For every candidate name: the lower-trust principal, the
accepted input or action, the intended control, the crossed boundary, the affected principal or
resource, and a concrete observable result. A missing best practice, guessed deployment
behaviour, generic parser crash or self-impact is not a finding (it is at most a hardening note).

**Respect source visibility.** Proxy, WAF, IdP policy, broker ACLs, provider settings, headers,
topology are real controls. If one is decisive and not in the repo, assume neither presence nor
absence: `needs_validation` with the exact missing fact.

**Three verdicts, distinct.**
- `confirmed` - complete source trace plus bounded observed result; the only verdict that gets severity.
- `needs_validation` - a specific source-grounded hypothesis blocked by one named fact; no severity. Not a low-confidence confirmed.
- `rejected` - disproved candidate.

**Severity anchors** (demonstrated conditions and result only; overall never exceeds impact):
- critical - unauthenticated code execution, full data-store access, or takeover of arbitrary accounts.
- high - fully defeats an explicit security control with real consequences: auth bypass, cross-tenant read/write, stored script execution against other users, authenticated code execution, unauthenticated remote stop of a shared service.
- medium - real boundary violation with limited blast radius, uncommon preconditions, or narrow resource set.
- low - disclosure of non-secret internals, or sustained effort for minimal gain.
- informational - confirmed but minimal; mainly a prerequisite inside a larger finding.

High vs medium: does the demonstrated result *fully defeat* an explicit control for an action with
real consequences, or only weaken it? If you cannot state the concrete damage, it is lower than it feels.

**Smallest effective fix.** Name the invariant the code must enforce and the narrowest change
at the last trusted decision point, with a regression test. Describe fixes; do not edit the
target during a review.

**Trace at depth.** Follow the input through parsing, identity, authorization, normalization,
state, derived copies and the final sink. Read sibling, legacy, batch, retry, cancellation,
migration and error paths that produce the same effect. Compare sibling controls for equivalence,
not just presence.

## Routing

| Reference | Load when |
|---|---|
| `references/attack-classes.md` | Always for a real hunt: ordinary classes (injection, access control, resource/file handling, crypto/secrets, business logic, feature abuse, chained vulns, wildcard, obvious things) plus a selector for the domain files |
| `references/audit-workflow.md` | Full audit mode only: setup, profiles, recon, hunting waves, verifier prompts, record shapes, report format |
| `references/domain-web-auth.md` | HTTP apps/APIs, proxies, sessions, CSRF, JWT, OAuth/OIDC, SAML, MFA, passkeys, account recovery, API keys, mTLS |
| `references/domain-client-side.md` | SPAs, browser extensions, webviews, service workers, storage, postMessage, CORS, WebSockets, DOM rendering |
| `references/domain-ai-llm.md` | Chatbots, RAG, agent memory, tool-calling loops, MCP servers/clients, prompt assembly, model-controlled actions |
| `references/domain-cloud-deployment.md` | IAM, IaC, containers/Kubernetes, service mesh, serverless/edge, ingress, provider events |
| `references/domain-supply-chain.md` | Dependency resolution, generated inputs, CI, release/signing/promotion, updates, plugins |
| `references/domain-protocols-rpc.md` | gRPC, GraphQL transports, Protobuf/Thrift, custom protocols, queues, brokers, webhooks, streaming |
| `references/domain-data-isolation.md` | Multi-tenant stores, caches/search, object links, analytics, export/backup, migration, deletion, restore |
| `references/domain-desktop-mobile-ipc.md` | Native apps, deep links, webview bridges, exported components, privileged helpers, Unix sockets/XPC/Binder/D-Bus |
| `references/domain-memory-safety-binary.md` | C/C++/unsafe Rust, kernel modules, parsers/decoders, FFI, binary loaders, JITs, firmware |
| `references/domain-resource-exhaustion.md` | Untrusted work can consume shared CPU, memory, disk, connections, workers, queues, quotas, spend |

Select a domain file only because you found the trust-sensitive boundary in its "When to use this file"
section, not because a language or dependency name appears. Use it alongside `attack-classes.md`.
In guidance mode, read the one or two domain files that match; do not read all of them.

Wording note: the references say "parent", "Task tool", `research`/`general` agents and
`subagent_type`. In pi, parent = you; delegation = `herdr-subagent` (see audit-workflow.md).

## Anti-patterns

1. Checklist deviations presented as vulnerabilities.
2. Defense-in-depth advice with no reachable boundary violation.
3. Live or shared-environment testing where bounded local evidence is insufficient.
4. Guessing provider, proxy, browser, identity or deployment behaviour not present in source.
5. Treating intended same-principal authority or self-impact as a cross-boundary result.
6. Reporting a parser or runtime effect stronger than the observed effect (crash is not code execution).
7. Prose-only hunter results that cannot be deduplicated or verified.
8. Re-reporting carried prior confirmed records, or using them as exemplars that anchor the hunt.
9. Assigning severity to `needs_validation`.
10. Writing the report before independent verification, or letting prose and JSON disagree.
11. Treating a prompt-injection demo as a finding: require a code-level boundary failure (see `domain-ai-llm.md`).
