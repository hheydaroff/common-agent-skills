# Audit workflow (full audit mode)

Adapted from cloudflare/security-audit-skill (MIT) — lean variant, see ../ATTRIBUTION.md.
The upstream coverage ledger, JSON schema, validators and fd-level artifact promotion are
deliberately not imported. Roles map to pi like this:

- **Parent** = you. You alone write the shared files.
- **Hunter / verifier / scout** = a `herdr-subagent` worker (load that skill first; needs
  `HERDR_ENV=1`). Use `--tools read,grep,find,ls` so source inspection is read-only.
  Without Herdr, run the phases yourself sequentially and say that independence was reduced.
- Workers share no context: put everything they need in the prompt.
- Hunters and verifiers return **one JSON object, no prose**; discard and re-run (fresh
  worker) any malformed reply instead of repairing it.

## 0. Setup

Resolve: target (absolute repo root), repo name, source ref (`git rev-parse HEAD`, dirty or
not), and an output dir **outside the target**: `~/security-audit-skill/<repo>/run-<N>`
(next unused N). Pick a profile and state it in the report:

| Profile | Hunters | Verification |
|---|---|---|
| `quick` | one wave, one hunter per top 2-3 boundaries | one verifier per candidate (also does the record check) |
| `standard` (default) | one hunter per subsystem x boundary, 3-6 total, then one gap-check wave | candidate verifier, then record verifier for every confirmed/needs_validation |
| `deep` | split per subsystem and lifecycle mode, repeat gap checks until clean | as standard, plus a second independent pass on any promoted/replaced record |

Profiles change breadth, never the evidence bar. A `quick` or scoped run (named paths, one
subsystem, one domain, a diff between refs) is reported as **partial coverage**; scope
exclusions are `out_of_scope`, never "covered". If a prior run exists in
`~/security-audit-skill/<repo>/`, read its `findings.json`: exclude still-unchanged
confirmed root causes from hunter prompts (list fingerprint + title + root cause only),
re-hunt changed source, and treat prior `needs_validation` as priority work. A prior
rejected claim only suppresses that exact claim. Never imply one run exhausts the target.

Write `run-metadata.json` (run id, repo, target, source ref, profile, scope paths, selected
domain files, prior-run paths, `execution_policy`: `source-only` or `sandboxed`).

## 1. Reconnaissance

Read the target yourself, or spawn up to three read-only scouts in parallel (product/stack,
principals/authority/controls, entry surfaces/copies/sinks). Facts only, with
repository-relative `file:line`. Do not use the network.

Scout prompts (adapted):

```text
Read the target at <target>. Do not use network access. Return source facts with
repository-relative file:line references.
A) Product type, users, operators, ordinary trust-sensitive actions; languages,
   frameworks, build system, locally visible deployment models; entry points and
   subsystem boundaries; comparable software visible from local docs/deps (or say none).
B) Every lower-trust principal and its by-design actions; authentication/peer identity
   at each entry surface; per-resource authorization and tenant/owner scope; privilege
   changes, confirmation, revocation, recovery, fallback paths; which controls are
   source-visible and which depend on an unobserved deployment fact.
C) Every place external or lower-trust input enters (HTTP/browser, RPC/message, files/
   archives, CLI/env/config, plugins/deps/CI, cloud events/IAM selectors, model context/
   tool args, deep links/webviews, local IPC); the major transformations, stored or
   derived copies, and security-relevant sinks; parallel paths to the same effect.
Do not execute or send inputs.
```

Synthesize `<output-dir>/architecture.md`, **hard cap about 1,000 words**: product,
principals, normal authority and protected resources; tech stack and deployment paths;
entry surfaces and key source-to-sink paths; trust boundaries with the strongest
source-visible control on each; starting paths; prior-run gaps and exclusions; and the
selected domain files with the boundary that justifies each. Select a domain file only
because recon found the trust-sensitive boundary in its "When to use this file" section,
not because a language or dependency name appears.

Then list **coverage units** in `architecture.md`: surface x boundary x attack class, each
with starting paths and its assigned domain/attack blocks. This is the lean replacement for
the upstream ledger: one line per unit, status `planned|covered|candidate|blocked|deferred|out_of_scope`.
Order by: (1) unauthenticated before authenticated surfaces, (2) boundaries guarding
credentials/cross-tenant data/code execution/release authority, (3) prior gaps and
changed source, (4) classes that historically yield confirmed findings for this target type.
Ties break alphabetically. A unit you cannot reach is `deferred` with a reason, never silent.

## 2. Hunting waves

Spawn one hunter per group of closely related units (never combine unrelated boundaries).
Every hunter prompt contains, in order:

1. Two-sentence role: find source-grounded security invariant failures in the assigned
   units, and return exactly one JSON object matching the result contract below.
2. `architecture.md` verbatim.
3. Assigned units, starting paths, boundary.
4. The **exact blocks** you selected, copied verbatim (never block names alone): each
   chosen ordinary attack-class block from `attack-classes.md`, and from each selected
   `domain-*.md` its `Core discipline`, chosen attack-class subsections, `Universal moves`
   and `Validation rules`.
5. Excluded blocks with a reason for each.
6. The core hunting method and candidate gate below.
7. Prior confirmed exclusions and peer-owned units not to duplicate.
8. The result contract.

An unexpected different boundary goes in `uncovered`, not into the hunter's own scope.

### Core hunting method — include in every hunter prompt

```text
## Defensive vulnerability-finding method

Your goal is to find source-grounded security invariant failures and the smallest fix,
not to expand harm beyond the boundary result. Stay within source review and bounded local execution.
Do not contact deployed endpoints, provider APIs, registries, identity systems,
message brokers, shared services, or other users. Use local dummy data only.

READ THE CODE AT DEPTH. Follow each assigned input through parsing, identity,
authorization, normalization, state, derived copies, and the final sink. Read sibling,
legacy, batch, retry, cancellation, migration, and error paths that produce the same
effect. Compare sibling controls for equivalence, not only presence, and compare what
one component guarantees with what the next component assumes.

WORK FROM A CONCRETE INVARIANT:
1. Name the lower-trust principal and starting capability.
2. Name the accepted value, action, state transition, or resource selector.
3. Locate the control that should reject, bind, isolate, limit, or revoke it.
4. Trace the exact source path after that decision.
5. Stop at the smallest affected dummy record, wrong return value, process-integrity
   effect, or locally observable shared-resource effect.
6. State a source-level change and regression case that enforce the invariant.

DEPTH BOUND: trace only paths that can reach your assigned boundary or whose
guarantees that boundary relies on. Stop a line of investigation as soon as the
invariant is settled either way, and record the result in your structured output —
a covered, candidate, or blocked disposition, or an `uncovered` entry — instead of
continuing to search.

TEST SAD PATHS AND DISAGREEMENTS. Check absent, empty, zero, negative, maximum,
over-limit, duplicate, mixed encoding, stale, revoked, reordered, concurrent,
partially migrated, failed dependency, and rollback state only where the interface
accepts them. Compare canonicalization and units at every parser or policy handoff.
For multi-step issues, treat each output as a prerequisite and do not assume a later
boundary. If any prerequisite is not established, record a blocker.

When a proposed high or critical candidate reveals a reusable root cause, search paths
owned by the assigned coverage IDs for lexical, structural, and logical variants.
Consolidate the same root cause, but establish each variant's conditions and impact
independently. Do not investigate peer-owned units. Return a variant with no current
coverage unit as `uncovered`.

DEFAULT IS SOURCE-ONLY. Do not run target-controlled code (builds, tests, scripts,
fixtures, fuzzers) unless the parent states that an OS-enforced sandbox exists (no
external network, empty allowlisted environment, read-only target, scratch-only writes,
low CPU/memory/time limits). If execution would settle the claim and no sandbox is
granted, return needs_validation naming that exact blocker plus the smallest local check
an owner could run. Never contact deployed endpoints, provider APIs, registries, or
identity systems; never use real credentials or production data; never stress
availability or continue past the minimum observed effect.

A deployment, browser, provider, broker, OS, proxy, package, secret, or identity fact
outside source is not proof either way. If one such fact is decisive, return a
needs_validation record with the exact missing observation and safe owner-observed check.
```

### Candidate gate — include in every hunter prompt

```text
## Candidate gate

1. A candidate needs a complete repository-relative source trace and evidence for the
   claimed root cause, including the strongest source-visible control.
2. A proposed confirmed record needs a bounded local observed result, meaningful impact
   across a stated boundary, complete conditions, and no visible preventing layer.
3. Do not strengthen a crash into code execution, ordinary work into shared availability,
   or a same-principal action into privilege gain.
4. If a required fact is not source-visible or locally observable, use
   needs_validation. Name exact blockers; do not give it severity or speculative completion.
5. A missing best practice with no affected principal/resource is excluded or hardening,
   not a finding. A candidate disproved by source is not needs_validation.
6. Use the same source-derived fingerprint for the same root cause in every state.
   It must match `^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$` and must not include a line,
   wave, agent, severity, or verdict.
7. Return an empty candidate array when nothing survives these gates.
```

### Hunter result contract

```json
{
  "units": [{"unit": "assigned id", "disposition": "covered|candidate|blocked",
              "reviewed_paths": ["repo/relative/path"],
              "checks": [{"invariant": "control checked", "method": "source|local", "result": "what was established"}],
              "candidate_fingerprints": [], "unresolved": []}],
  "candidates": [],
  "hardening": ["concrete non-finding note"],
  "uncovered": [{"surface": "...", "boundary": "...", "attack_class": "...", "starting_paths": [], "reason": "..."}]
}
```

Every assigned unit appears exactly once. A `covered` unit has paths, at least one check,
and nothing unresolved. Candidate shapes are in [Record shapes](#record-shapes) below, with
`proposed_verdict` in place of `verdict`.

### After each wave

- Map each result to its units and update their status in `architecture.md`. Reject
  duplicate/absent unit ids.
- Consolidate candidates by fingerprint then root cause: one root cause with several entry
  paths is one candidate with the strongest trace; independent missing controls get separate
  fingerprints.
- **Gap check:** spawn one fresh read-only critic with `architecture.md` and the unit list.
  It looks for unmapped entry points, unchecked parallel paths, missing lifecycle modes,
  selected domain classes without a unit, unjustified exclusions, units closed without
  paths/checks. It proposes coverage, not findings. Require:
  `{"missing_units": [{"surface","boundary","attack_class","starting_paths","reason"}], "reassign": ["unit ids that did not close"], "stop": false}`.
  `quick`: one critic pass, record accepted gaps as `deferred`. `standard`: one more wave
  for accepted gaps, then stop. `deep`: repeat until the critic returns no missing units.

## 3. Validate every candidate independently

Give each unique `confirmed`/`needs_validation` candidate to a **fresh** verifier that did
not hunt it and has not seen any other verifier's conclusion. Send only: the candidate,
the architecture facts needed to read its path, the relevant domain `Validation rules`, the
execution policy, and prior records with the same fingerprint.

```text
You did not write this candidate. Try to refute it from repository source (and bounded
local evidence only if the parent granted a sandbox). Do not contact deployed endpoints
or external/shared services.

1. Verify every trace and evidence file, positive line number, scope and description.
   Confirm the first entry is a real lower-trust entrypoint and the last is the claimed
   sink or boundary effect.
2. Reconstruct the strongest source-visible validation, identity, authorization,
   normalization, lifecycle, framework and containment controls on the path. Where the
   architecture summary names a comparable baseline, note whether it shares the pattern —
   as calibration, never as grounds to dismiss.
3. For a proposed confirmed candidate, independently reproduce the minimum observed
   result when possible. Verify inputs, interface shape, conditions and affected dummy
   principal/resource. Do not infer a stronger result or continue after it.
4. Verify that likelihood, impact, confidence and the proposed fix match only what the
   evidence establishes.
5. For a proposed needs_validation candidate, decide whether the blocker is genuinely
   outside source/local observation. If source refutes the trace, reject it. If the
   missing fact remains decisive, keep needs_validation and make the local and
   owner-observed plans exact and non-destructive.
6. Preserve the fingerprint for the same source-derived root cause across every state.

Return exactly one JSON object and no prose:
{"decision": "confirmed|needs_validation|rejected", "record": { ... }}
A corrected record replaces the hunter's wording.
```

A verifier may promote `needs_validation` to `confirmed` only after independently
establishing the complete path and result. Demote to `needs_validation` when a specific
deployment/runtime fact stays unknown. `rejected` when source, a visible control, missing
meaningful impact, or an impossible prerequisite refutes it. `needs_validation` is never a
parking place for a speculative idea. The fingerprint must match unless the verifier names
a genuinely different root cause (then it is a new candidate and goes through validation).

## 4. Write `findings.json`

All final records, one per fingerprint, as `{"run": {...metadata...}, "findings": [records]}`.
Parse it with `jq .` or `python3 -m json.tool`, and check by hand: unique fingerprints, every
`confirmed` has severity and a fix, no `needs_validation` has severity, every trace path
exists in the repo and line numbers are positive.

## 5. Independent record verification

One fresh verifier per final `confirmed` and `needs_validation` record (parallel). It checks
the structured record, not the hunter write-up.

- `confirmed`: every trace path/line/scope and operation; the real entry interface and input
  shape; every condition and preventing layer; affected principal/resource and demonstrated
  impact; severity separation (likelihood, demonstrated impact, overall no greater than
  impact); that the fix enforces the invariant rather than merely moving trust.
- `needs_validation`: the trace supports only the stated root cause; each blocker is decisive
  and not answerable locally; it names a boundary and a possible concrete result; at least one
  exact validation-plan step; fingerprint matches prior/current records.

Reply: `{"decision":"verified","fingerprint":"..."}` or
`{"decision":"replace","reason":"...","record":{...}}`. Do not apply a replacement that
promotes a verdict, or materially changes root cause, trace, input, result, impact or
severity, until a **third** worker that neither hunted, validated nor proposed it re-verifies
it. Do not verify only `confirmed` records: a misleading `needs_validation` wastes owner time.
In `quick`, phases 3 and 5 merge into one verifier pass; never skip independent review of a
`confirmed` record in any profile.

## 6. Report

Only after phase 5 passes for every retained record. Write `REPORT.md` (prose never changes a
verdict, severity or blocker):

1. Profile, scope, source ref, execution policy, prior-run use, `deferred`/`out_of_scope`
   units; a `quick`, scoped or incomplete run says plainly it is a partial pass.
2. One short security posture summary.
3. Confirmed-findings table: severity, title, boundary, one-line observed result.
4. Each confirmed finding: source location, lower-trust principal, bounded reproduction
   (a function call, fixture, CLI command, IPC/file action or locally rendered policy — HTTP
   is only one possible interface), conditions, actual result, impact, priority rationale,
   smallest source fix and regression case. Full trace for medium/high/critical.
5. Separate **NEEDS VALIDATION** section: title, trace, exact blocker, bounded local next
   step, safe owner-observed deployment check. No severity; never live-test guidance.
6. Hardening notes and positive source patterns, kept apart from findings.
7. Coverage summary (units covered/candidate/blocked/deferred, key exclusions, gap-check result).

Do not list rejected records as findings. A clean run may have zero confirmed records: say so
and state the coverage limits without inventing LOW findings.

Terminal states: report written and `findings.json` checked, **or** `run_status: "incomplete"`
in `run-metadata.json` with the reason, disclosed in the report. Never stop mid-phase.

## Record shapes

Upstream defines a strict JSON schema; these are the fields to keep.

```jsonc
// confirmed
{"verdict":"confirmed","fingerprint":"stable-root-cause-id (no line/wave/agent/severity)",
 "title":"","description":"",
 "boundary":{"principal":"lower-trust actor","input":"accepted value/action","control":"intended control","affected":"principal/resource"},
 "root_cause":"","intended_behavior":"",
 "trace":[{"path":"repo/relative.ext","line":12,"note":"entry|hop|sink"}],
 "evidence":[{"path":"","line":0,"note":""}],
 "conditions":[""],
 "execution":{"interface":"function|fixture|cli|ipc|policy","input":"","observed_result":""},
 "impact":"","likelihood":"low|medium|high",
 "severity":"critical|high|medium|low|informational","confidence":"low|medium|high",
 "remediation":{"invariant":"","change":"smallest source change","regression_test":""}}
// needs_validation (no severity)
{"verdict":"needs_validation","fingerprint":"","title":"","description":"","claimed_root_cause":"",
 "trace":[],"evidence":[],"blockers":["exact missing fact"],
 "validation_plan":{"local":"bounded fixture or null","deployment":"what an owner should observe or null"}}
// rejected
{"verdict":"rejected","fingerprint":"","title":"","reason":"what disproved it"}
```
