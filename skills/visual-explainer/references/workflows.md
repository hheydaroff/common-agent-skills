# Visual Explainer Workflows

These are ready-made task recipes. When the user asks for one of these, follow the recipe. (Adapted from the upstream slash commands.)

---

## /generate-web-diagram

---
name: generate-web-diagram
description: Generate a standalone HTML diagram and open it in the browser
---

Load the visual-explainer skill and generate an HTML visual explainer for: $@

Use the skill’s reference routing and final checklist. Pick a representation that fits the topic: Mermaid for connected flows/topologies; CSS cards for text-heavy explanations; tables for matrices; timelines for linear history.

Write to `docs/diagrams/` (inside the current repo/project) with a descriptive filename and open the result in the browser.

---

## /generate-visual-plan

---
name: generate-visual-plan
description: Generate a visual implementation plan
---

Load the visual-explainer skill and generate a self-contained HTML implementation plan for: $@

## Research first

Read relevant repo files before planning. Identify entry points, existing patterns, affected modules, public APIs, tests, config/schema/data model, similar features, and constraints from README/CHANGELOG/docs.

## Required page sections

1. Goal and scope: what will change and what is intentionally out.
2. Current state: short diagram/table of existing architecture.
3. Proposed design: architecture/data/control flow, preferably Mermaid or hybrid cards.
4. Implementation sequence: ordered phases with dependencies.
5. File map: files to create/edit/delete and why.
6. Interface/contracts: types, APIs, schemas, CLI flags, config, events.
7. Risk and decision matrix: correctness, tests, migration, release, UX, security/privacy, performance.
8. Test plan: unit/integration/e2e/edge cases mapped to files.
9. Acceptance checklist: observable done criteria.

Use hierarchy: overview and architecture dominate; detailed file/test/reference sections stay compact or collapsible. Follow the skill’s Mermaid, table, overflow, and delivery rules.

Write to `docs/diagrams/` (inside the current repo/project) and open in browser.

---

## /generate-slides

---
name: generate-slides
description: Generate a slide deck as a self-contained HTML page
---

Load the visual-explainer skill and generate a slide deck for: $@

Before writing HTML, read `./templates/slide-deck.html`, `./references/slide-patterns.md`, and only the shared CSS/library sections needed for the source.

Plan the deck first: inventory the source, map every item to slides, choose a narrative arc, and assign a composition to each slide. Use the 10 slide types and nav chrome from `slide-patterns.md`/`slide-deck.html`, including carousel dots, prev/next, slide count, and keyboard controls. Keep each slide to `100dvh`; split dense content across slides rather than scrolling or dropping content.

Use visual-first slides: diagrams, charts, tables, SVG accents, and images from `surf` only when they clarify the story. Vary compositions; three centered slides in a row is a smell.

Write to `docs/diagrams/` (inside the current repo/project) and open in the browser.

---

## /diff-review

---
name: diff-review
description: Generate a visual diff review for code changes
---

Load the visual-explainer skill and generate a self-contained HTML diff review.

## Scope detection

Interpret `$@` as a branch, commit, range, PR, or `HEAD`. If no argument is given, compare the working tree against `main`/`master`.

## Data gathering before HTML

Run the relevant git commands for: diff stats, name-status, changed files, line counts, public API/type/function changes, added/removed files, docs/changelog changes, tests touched, dependencies/config changes. Read changed files in full plus surrounding code paths needed to validate behavior. If reviewing committed work, read commit messages. If this session created the work, use available progress/plan notes for rationale.

## Source verification

Before generating, know and cite:

- exact changed files and line-count scope;
- each function/type/module name referenced;
- before/after behavior for important changes;
- likely coupling and test impact.

Use file paths, command outputs, or file:line evidence. Do not invent rationale or code paths.

## Required page sections

1. Executive summary: intuition, problem solved, factual scope.
2. File map: full tree, color-coded new/modified/deleted; compact, `<details>` if long.
3. Architecture impact: Mermaid or hybrid diagram when relationships matter.
4. Before/after behavior: side-by-side visual comparison.
5. Risk review: correctness, tests, API compatibility, security/privacy, performance, maintainability.
6. Coupling map: dependencies, hidden coupling, migration/release concerns.
7. Review recommendation: merge/readiness, blockers, follow-ups.

Use diff color language consistently: red removed/before, green added/after, amber modified/risk, blue neutral context. Use responsive section navigation for 4+ sections. Follow the skill’s Mermaid and overflow rules.

Write to `docs/diagrams/` (inside the current repo/project) and open in browser.

---

## /plan-review

---
name: plan-review
description: Compare an implementation plan against the current codebase
---

Load the visual-explainer skill and generate a self-contained HTML plan review.

## Inputs

Use `$@` as the plan path or plan text. If no path is given, ask for the plan.

## Data gathering before HTML

Read the plan in full. Extract goals, assumptions, proposed files/functions/types, migrations, tests, rollout/release notes, and explicit risks. Read every referenced file, plus importers/dependents that may be affected. Use ripgrep for existing patterns, similar implementations, public API boundaries, config/schema files, and tests.

## Source verification

For each proposed change, verify whether referenced files/functions/types exist, whether current behavior matches the plan, what ripple effects are missing, and whether the proposed test coverage fits the current test style. Cite plan sections and file:line evidence.

## Required page sections

1. Plan summary: problem, core idea, scope.
2. Accuracy verdict: correct, stale, risky, unsupported, missing.
3. Current architecture: diagram of affected subsystem only.
4. Proposed architecture: matching visual diff against current state.
5. Gap/risk matrix: correctness, tests, API, data model, UX, security/privacy, performance, maintainability, release.
6. File-by-file review: proposed edits, current reality, recommendation.
7. Better plan: concrete corrections or simplifications.
8. Decision: approve, revise, or reject with rationale.

Use current-vs-planned visual language. Include responsive nav. Follow the skill’s Mermaid, overflow, and evidence rules.

Write to `docs/diagrams/` (inside the current repo/project) and open in browser.

---

## /project-recap

---
name: project-recap
description: Generate a visual project recap for context switching
---

Load the visual-explainer skill and generate a self-contained HTML project recap.

## Data gathering before HTML

Read project identity files (`README`, changelog, package/build files), top-level tree, current git status, recent commits, unmerged/stale branches, TODO/FIXME in recent files, progress/todo memory if present, and key entry points/source files. Focus on what a returning developer needs to rebuild the mental model.

## Verify before generating

Cite command output or file:line evidence for project state, module/function/type names, recent activity, current blockers, and next-step claims. Do not fabricate momentum or rationale.

## Required page sections

1. Project identity: what this repo is, stack, entry points.
2. Architecture snapshot: Mermaid or hybrid diagram of current conceptual modules.
3. Recent activity: grouped narrative, not raw log.
4. Current state: uncommitted work, branches, TODOs, known blockers.
5. Mental model map: key modules, data flow, command/test/deploy paths.
6. Risks and cognitive debt: hotspots and gotchas.
7. Useful commands and files.
8. Likely next steps, based only on evidence.

Use responsive nav. Use compact reference tables for file maps and commands. Follow the skill’s Mermaid, overflow, and delivery rules.

Write to `docs/diagrams/` (inside the current repo/project) and open in browser.

---

## /fact-check

---
name: fact-check
description: Verify a generated document against actual code and git history
---

Load the visual-explainer skill and fact-check the document named by `$@`. If no argument is given, use the most recently modified HTML file in `docs/diagrams/` (inside the current repo/project).

## Claim extraction

Read the target document. Extract verifiable claims about file paths, function/type/module names, behavior, architecture, data flow, APIs, commands, dependencies, tests, performance/security assertions, and git history. Skip subjective design opinions.

## Verification

For each claim, inspect the actual source or git history. Re-read referenced files. For diff reviews, compare before/after with `git show` or the relevant range. For plan docs, verify referenced files/functions/types exist and behave as described.

Classify claims as verified, corrected, unsupported, or unverifiable. Preserve the document’s structure. Correct factual errors in place and add a verification summary that lists what was checked and changed. For HTML, match the existing page style and open it in the browser. For markdown, report the path in chat.

