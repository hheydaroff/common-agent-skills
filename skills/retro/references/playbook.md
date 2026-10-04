# Retro playbook

## Signal → likely cause → proposal

| Signal (digest field) | Likely cause | Typical fix (home) |
|---|---|---|
| `nav_before_first_edit` high (median >10) across sessions, same `files_read_in_multiple_sessions` | Agent rediscovers the same layout each time | Add a short "where things live" map to AGENTS.md (≤30 lines), or split a huge doc. (repo) |
| `paths_that_did_not_exist`, `repo.stale_pointers` | Docs point at moved/deleted files; agent guesses | Fix/remove the pointer; add a check script to CI. (repo) |
| `empty_searches` high | Naming inconsistent, no glossary | CONTEXT.md glossary / rename. (repo) |
| `rereads` high, `hot_reads` on one file | File too long or cut by offset; info not in context after compaction | Split the file, add a summary header. (repo) |
| `corrections` ≥1 with the same theme in ≥2 sessions | Convention never written down | AGENTS.md rule (project) or vault_memory / personal rule. (rule) |
| `repeated_prompts` | Input lost, agent stalled or looped | Check the excerpt; usually a tool/extension bug, not a doc issue. (tooling) |
| `security_blocks` same reason repeatedly | Agent keeps trying a blocked path | AGENTS.md "don't do X, do Y instead" or a skill using the allowed path. (rule/skill) |
| `tool_errors` same message repeatedly | Broken tool/env, stale skill instructions | Fix the tool or the skill text that teaches the wrong call. (skill) |
| `edit_churn` (≥4 edits on one file) | Spec unclear, trial and error | Spec-first for that area; add a test that pins the behaviour. (process) |
| `code_edited_no_verify`, `unverified_code_rate` >0.3 | No fast check exists or none known to the agent | Add a one-command check (`make check` / validate script) and name it in AGENTS.md; CI if absent. (process/automation) |
| `sessions_5plus_files_edited_without_early_spec_read`, no PRD/SPEC in `repo.prd_spec` | Big change started without a written target | Use prd-creator → prd-to-spec before multi-file work. (process) |
| `outcome`: reverts, `fix:` commits, follow-up sessions on same files | Result did not hold | Look at the excerpt for what was skipped (test? spec?). (process) |
| `repeated_commands_automation_candidates` | Manual sequence repeated across sessions | Script/Makefile target/hook; cron only if user wants. (automation) |
| Skill named in `skills_seen` yet errors/corrections follow | Skill content wrong or weak | Edit the skill. (skill) |
| Task recurs (same kind of prompt ≥3×) and no skill covers it | Missing skill | New skill. (skill) |
| `compactions` ≥1 per session | Context polluted by big outputs | Pipe output through spool/filters, split the task, smaller sessions. (habit/tooling) |
| `cache_hit` low (<0.6) | Prompt prefix changing, long gaps | Habit: keep sessions warm, avoid mid-session system changes. (habit) |
| `cost` dominated by one model/session in `top_cost_sessions` | Expensive model on routine work | Cheaper model for that task class. (growth) |

## The seven homes (choose exactly one per proposal)

1. **repo-navigability**: AGENTS.md map, README/doc pointers, glossary, file splits.
2. **process**: PRD/SPEC first, tests before fixes, verification command, CI, review gates.
3. **automation**: scripts, Makefile/just targets, hooks, cron (only if asked).
4. **skill-update / new-skill**: edit the source in common-agent-skills.
5. **rule/memory**: project AGENTS.md rule or vault_memory. Ask: who should own this truth? A fact about an external tool belongs upstream/in a skill, not a personal rule.
6. **tooling**: pi extension or environment bugs (security rules too strict, broken MCP, etc.).
7. **growth**: user habits with evidence: prompt clarity, spec-first discipline, session size, model choice, review of outputs.

## Verify before claiming

Pre-pass flags are leads. Check with `excerpt`:
- `corrections`: real only if the user disagreed with what the agent did, not "don't" in a fresh instruction.
- `tool_errors`: an `exit 1` from `grep` with no match or a deliberate failing test is not friction.
- `nav_before_first_edit`: high is fine for research/writing sessions (`first_edit_at_call` null or docs-only edits). Compare like with like.
- Automated/scheduled prompts (e.g. "[Signal message …]") are not user behaviour; exclude them from growth findings.

## Trends

If `previous_retro.compare` exists, add a table in the report (metric: prev → now). Judge direction: lower is better for everything except `cache_hit_avg`. A metric that did not move after its proposal was applied means the proposal was wrong or too weak: say so and propose a stronger or different fix, or retire the rule it added.

## Pruning

Also propose **deletions**: rules in AGENTS.md / skills that no session touched or that were followed by no change in behaviour, docs never read in N sessions, over-long AGENTS.md (`repo.agent_docs_lines` >200).
