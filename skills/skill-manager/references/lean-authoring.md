# Lean authoring

Adapted from **nicobailon/skill-diet** (https://github.com/nicobailon/skill-diet, MIT,
Copyright (c) Nico Bailon): the level ladder, the edit ladder, the commit budget, the
four cuts and the drift rule. The upstream eval harness is **not** vendored — step 5 of
the full pass below is the cheap substitute.

## The levels

Put each fact on the lowest level that still reaches the agent before it needs it.

| Level | Holds | Read |
|---|---|---|
| `description` | one trigger per case | every session, for every skill |
| `SKILL.md` | what every run of this skill needs | when the skill is used |
| `references/` | what only some tasks need, behind a link that says when | when that case comes up |
| the tool's own help | flags, allowed values, exact field names | when the agent picks that command |
| the tool's replies, errors, checkers | the right name, the fix, the next step | when the agent calls the tool, or a guess is wrong |

Two consequences that matter in this repo:

- **A reference most tasks read belongs in `SKILL.md`.** The split is decided by read
  frequency, not by line count — ">150 lines" is the symptom, not the test.
- **A skill that teaches a tool copies no reference into the skill.**
  `jira-via-docker-gateway`, `n8n-builder`, `gog-cli`, `mcp-tools` and
  `create-pi-extension` all document a moving target. Keep the judgment calls — which
  tool for which job, what to do when it fails — and point at the live help for names,
  fields and allowed values. A copied API surface does not error when it goes stale; it
  silently teaches a command that no longer exists.

## The edit ladder

Before changing a skill, stop at the first step that handles the change.

1. **Fix it below the skill.** A mechanical mistake wants a check, a test, or a clearer
   error in the tool — `validate-skills.sh` exists because "quote your description" as
   prose was not enough. Prose is for judgment calls only.
2. **Check the model needs it.** If a fresh session does the right thing without the
   line, add nothing. A skill is read on every use; a line that changes no behaviour is
   a tax on every task.
3. **Edit, don't append.** Change the line that already covers the idea. A new section
   restating an old rule leaves two sources of truth, and the model will follow the
   wrong one.
4. **Pick its level** — the table above.
5. **Write the rule, not the story.** One positive rule under a short name, e.g.
   `## Keep descriptions double-quoted`. The bug, the incident and the measurement go in
   the commit message, where they cost no context.

## Budget

- Put `SKILL.md`'s line count before → after in the commit body.
- Offset growth with a cut in the same change. If there is nothing to cut, the file is
  overdue for a split, not for another section.
- Two copies of one idea, or more than ~10% growth since the last trim, means a full pass
  over the file rather than another patch.

## Full pass (when a skill is big or has drifted)

1. **Baseline** — copy the skill aside; record the `description`, `SKILL.md` and each
   reference size, and what a typical task actually loads.
2. **Consumers** — grep the skill name across this repo and the deploy targets
   (`~/.agents/skills`, `~/.claude/skills`, `~/.codex/skills`). Check nothing else links
   a file you are about to remove.
3. **Place** — sort every piece onto a level; anything most tasks need moves up. Scripts
   and templates are run or copied, never read.
4. **Cut and write** — apply the four cuts, name the rules, and end `SKILL.md` with one
   line per case saying where to look.
5. **Verify** — see below. Keep the new version only if it does at least as well.

### The four cuts

- what the model already knows — definitions, standard notation, common practice;
- what only a human needs — motivation, history, measurements (→ commit message);
- examples of an obvious idea — keep examples only where they encode a judgment call;
- every word a sentence can lose without changing what the agent does.

## Verify

1. Rerun the case that prompted the change **in a fresh session** with only the new
   version installed. The question is not "does it trigger" but "does it still do the
   thing".
2. Have a reviewer map each rule in the old version to a home in the new one, or confirm
   it was cut under the four cuts.
3. For anything the new version no longer says, write a one-line case and run it. If the
   agent gets it right without the line, the cut was correct.

## Drift

When a code change renames or changes behaviour a skill describes, update the skill in the
same change — a skill shipped against the old name is worse than no skill. Index a new
public operation by name only, unless agents will call it constantly.

## Skills only the user starts

If you only ever start a skill yourself, set `disable-model-invocation: true` in its
frontmatter: pi keeps it out of the system prompt, so it costs no context, and it stays
reachable as `/skill:<name>`. No skill in this repo does this today — every one here is
meant to be model-invoked.