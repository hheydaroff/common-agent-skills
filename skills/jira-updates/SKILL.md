---
name: jira-updates
description: Get latest Jira ticket updates with changelogs and comments. Accepts project keys, JQL filters, or specific ticket keys as parameters. Use when user asks for "jira updates", "ticket status", "what's new in [PROJECT]", "sprint updates", or wants to review project activity.
---

# Jira Updates

Fetch and summarize recent Jira activity with changelogs.

## Parameters

Parse from user request:
- **projects**: Project keys (e.g., "DATA", "AUTO", "WEB")
- **tickets**: Specific ticket keys (e.g., "DATA-4207")
- **assignee**: Filter by assignee name
- **status**: Filter by status (e.g., "In-Progress", "Open")
- **days**: How far back to look (default: 7)

If no parameters provided, ask user which projects or tickets to check.

## Default Fields

Always use these fields in `searchJiraIssuesUsingJql`:

| Field ID | Name | Purpose |
|----------|------|---------|
| key | Key | Ticket identifier (AUTO-1234) |
| summary | Summary | Title |
| status | Status | Current state |
| updated | Updated | Last modification date |
| priority | Priority | Importance level |
| reporter | Reporter | Who created it |
| assignee | Assignee | Who owns it |
| description | Description | Full details |
| customfield_10070 | Acceptance Criteria | AC for stories |

**Fields array for API calls:**
```json
["key", "summary", "status", "updated", "priority", "reporter", "assignee", "description", "customfield_10070"]
```

## Workflow

1. Get Atlassian cloud ID via `getAccessibleAtlassianResources`
2. Build JQL from parameters:
   ```sql
   project in ([projects]) ORDER BY updated DESC
   ```
   Or for specific tickets:
   ```sql
   key in ([tickets]) ORDER BY updated DESC
   ```
3. Search with `searchJiraIssuesUsingJql`:
   - `maxResults`: 50-100
   - `fields`: `["key", "summary", "status", "updated", "priority", "reporter", "assignee", "description", "customfield_10070"]`
4. Categorize results by status
5. For active tickets (In-Progress, Waiting, Ready for Dev), fetch details with `getJiraIssue` + `expand=changelog`
6. Extract from changelog:
   - Status transitions
   - Assignee changes
   - Sprint moves
   - Recent comments (last 3)
7. Present as actionable summary

## URL Construction

**IMPORTANT:** All ticket keys MUST be rendered as clickable Markdown hyperlinks.

The Jira ticket URL format is:
```
https://<site-url>/browse/<KEY>
```

**Getting the site URL:**
1. The `getAccessibleAtlassianResources` response includes a `url` field for each site
2. Extract this URL (e.g., `https://smarteurope.atlassian.net`)
3. Construct ticket URL: `{site_url}/browse/{ticket_key}`

**Example:**
- Site URL: `https://smarteurope.atlassian.net`
- Ticket Key: `AUTO-1483`
- Markdown: `[AUTO-1483](https://smarteurope.atlassian.net/browse/AUTO-1483)`

## JQL Building

| Parameter | JQL Fragment |
|-----------|--------------|
| projects | `project in (DATA, AUTO)` |
| tickets | `key in (DATA-4207, AUTO-1493)` |
| assignee | `assignee = "Name"` |
| status | `status in ("In-Progress", "Open")` |
| days | `updated >= -7d` |

Combine with AND: `project in (DATA) AND status = "In-Progress" AND updated >= -7d`

## Output Format

### Summary Table
```
| Status | Count |
|--------|-------|
| In-Progress | X |
| Ready for UAT | X |
| Pending Confirmation | X |
| Open | X |
```

### Per-Ticket Update
```
## [KEY](https://<site-url>/browse/KEY): [Summary]
**Status:** X | **Priority:** X | **Updated:** YYYY-MM-DD
**Reporter:** X | **Assignee:** X

**Acceptance Criteria:**
[content or "Not specified"]

**Description:** (first 200 chars if long)

**Latest Updates:**
- [date] | [author]: [field] changed from '[old]' to '[new]'
- [date] | [author]: status changed from 'Open' to 'In-Progress'
- [date] | [author] commented: "[first 100 chars]..."
```

**Note:** Replace `<site-url>` with the actual Atlassian site URL from Step 1 of the Workflow.

### Grouping

Group tickets by status category for readability:
1. **In-Progress** - Active work
2. **Blocked/Waiting** - Needs attention
3. **Ready for Development** - Upcoming
4. **Pending Confirmation** - Awaiting validation
5. **Ready for UAT** - Testing phase

## Handling Large Results

When results exceed token limits (auto-saved to file), parse with `uv run python3`:

```bash
cat <filepath> | uv run python3 -c "
import json, sys

data = json.load(sys.stdin)
inner = json.loads(data[0]['text'])
issues = inner['issues']  # Response wraps issues in a dict with 'issues' key

for issue in issues:
    key = issue['key']
    fields = issue['fields']
    summary = fields.get('summary', '')
    status = fields.get('status', {}).get('name', 'N/A') if fields.get('status') else 'N/A'
    updated = fields.get('updated', '')[:10]
    priority = fields.get('priority', {}).get('name', 'N/A') if fields.get('priority') else 'N/A'
    reporter = fields.get('reporter', {})
    reporter_name = reporter.get('displayName', 'Unknown') if reporter else 'Unknown'
    assignee = fields.get('assignee', {})
    assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
    description = fields.get('description', '')  # May be ADF format
    ac = fields.get('customfield_10070', 'Not specified')

    print(f'{key} | {status} | {priority} | {updated} | {assignee_name} | {summary[:80]}')

    changelog = issue.get('changelog', {}).get('histories', [])
    for change in changelog[:5]:
        author = change.get('author', {}).get('displayName', 'Unknown')
        created = change.get('created', '')[:16]
        for item in change.get('items', []):
            field = item.get('field')
            from_val = item.get('fromString', '')
            to_val = item.get('toString', '')
            print(f'  {created} | {author}: {field} [{from_val}] -> [{to_val}]')
"
```

## Changelog Fields to Surface

| Field | Why It Matters |
|-------|----------------|
| status | Work progression |
| assignee | Ownership changes |
| Sprint | Planning shifts |
| priority | Urgency changes |
| description | Scope changes |

**Skip noise:** Rank, RemoteWorkItemLink, customfield_*

## Orchestration

This skill can be run in two modes:

### Standalone Mode (user invokes directly)
When the user runs `/jira-updates` directly:
- Follow all steps as documented
- Present full Jira update summary
- Wait for user direction on next steps

### Orchestrated Mode (invoked by another skill)
When this skill is invoked by another skill (e.g., called from `/daily-brief`):
1. Complete all steps in this skill
2. Return the formatted Jira updates output
3. **Immediately return control to the calling skill** - do NOT wait for user input
4. Do NOT offer follow-up options - the orchestrator handles next steps

**How to detect:** If you were just executing another skill (like daily-brief) and invoked this skill as a sub-step, you are in orchestrated mode.
