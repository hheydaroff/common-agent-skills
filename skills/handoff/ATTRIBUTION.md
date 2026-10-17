# Attribution

Adapted from **Matt Pocock's skills** — https://github.com/mattpocock/skills
(`skills/productivity/handoff/SKILL.md`)
MIT License, Copyright (c) 2026 Matt Pocock. Vendored 2026-10, adapted to this
repo's conventions (frontmatter, pi tooling, deploy targets).

## Kept from upstream (every rule)
- Compact the current conversation into a handoff document for another agent.
- Save to the OS temp dir (`$TMPDIR`, else `/tmp`), **not** the workspace.
- Include a "suggested skills" section naming what the next agent should load.
- Do not duplicate content already in other artifacts (specs, plans, ADRs,
  issues, commits, diffs) — reference by path or URL.
- Redact secrets and PII.
- Treat passed arguments as the next session's focus and tailor the doc to it.

## Local modifications
- Frontmatter rewritten to repo convention ("Use when…" + trigger phrases,
  quoted description).
- **Deliberately opposite:** upstream is slash-only
  (`disable-model-invocation: true`, `agents/openai.yaml` with
  `allow_implicit_invocation: false`) and carries a Claude-Code-only
  `argument-hint` field. Ours stays model-invocable with tight trigger phrases;
  it still works as `/skill:handoff` in pi and `/handoff` in Claude Code.
  `agents/openai.yaml` was not vendored (pi/Claude/Codex all read `SKILL.md`).
- Added the resume-vs-fresh-agent mode split, and pi's actual resume commands
  (`pi --session/--fork/--continue`, `/import`).
- Added ground-truth step: `$PI_SESSION_FILE` / `$PI_SESSION_ID` recorded in the
  doc so the next agent can `session_query` / `session_search` for exact
  evidence, including detail already lost to compaction.
- Added the durable-vs-ephemeral split into `vault_memory`.
- Added a concrete doc template mirroring pi's own compaction summary format
  (Goal / Constraints / Progress / Key Decisions / Next Steps / Critical
  Context + `<read-files>` / `<modified-files>`).
- Added the temp-dir exception (other worktree / container / machine cannot read
  `$TMPDIR`) and the "verify suggested skill names exist" check.
- Added a "Not this skill" table against `/compact`, `/export`, `retro`,
  `parallel-agent-lanes`, `documentation-and-adrs`.
