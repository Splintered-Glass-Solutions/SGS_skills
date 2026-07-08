---
name: clickup
description: Use when creating, updating, finding, summarizing, or organizing ClickUp tasks, lists, priorities, statuses, due dates, assignees, comments, or task descriptions. Provides the general ClickUp workflow; use a more specific company/project ClickUp skill when one applies.
---

# ClickUp

Use this as the general ClickUp operating guide. If a more specific skill applies, such as `striq-clickup`, use that skill's defaults for workspace, list, assignees, statuses, and project conventions.

## Workflow

1. Resolve the destination list before creating tasks.
   - If the user explicitly names a list, use ClickUp list lookup/search tools to resolve it.
   - If a project-specific skill provides a default list, use that list.
   - If neither is true and the list is ambiguous, ask a concise question before creating.
2. Resolve assignees through ClickUp tools when the user gives names, emails, or "me".
3. Preserve user intent in the task:
   - Title
   - Status
   - Priority
   - Due date
   - Start date, when useful
   - Assignees
   - Tags
   - Source links
   - Direct quotes or acceptance criteria when provided
4. Prefer `markdown_description` for task descriptions so evidence, links, and checklists remain readable.
5. After creating or updating tasks, return the task URLs and the important fields that were set.

## Status and Priority

- Do not invent statuses if the user gave a project convention. Use the exact capitalization from the project skill or existing list.
- If a requested status fails, inspect or ask for valid statuses rather than silently changing meaning.
- Map plain-language priority carefully:
  - "ASAP", "urgent", "blocker" -> `urgent`
  - "high priority" -> `high`
  - "normal" or unspecified -> `normal`
  - "low priority" -> `low`

## Dates

- Always set a due date when creating a ClickUp task. If the source does not provide an explicit deadline, use the best practical estimate from the context and make that estimate visible in the task description or final response.
- Convert relative dates to exact dates using the user's locale/timezone from context.
- For "next week" without a specific day, choose Friday of the next calendar week for due dates unless the project-specific skill says otherwise.
- Mention the exact date used in the final response.

## Evidence-Rich Tasks

When the task comes from a meeting, call, email, Slack thread, doc, or issue:

- Include the source link in the description.
- Include short direct quotes when useful for future context.
- Include timestamped links for meeting transcripts when available.
- Separate evidence from acceptance criteria.

Keep quotes short and specific. Do not paste large transcript sections.

## Final Response

Summarize task creation/update results with:

- Task title
- URL
- Status
- Priority
- Due date, if set
- Assignees
