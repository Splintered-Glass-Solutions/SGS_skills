---
name: striq-clickup
description: Use when doing StrIQ work or creating ClickUp tasks for StrIQ-related repos, including striq-backend, striq-api, ios-striq, frontend, and striq-shared-docs. Provides StrIQ's ClickUp workspace, list, status semantics, priority, Preston/Austin assignee routing, and task intake workflow.
---

# StrIQ ClickUp

## Defaults

Use these defaults when the user asks to create or track work for the StrIQ project in any related repo:

- ClickUp workspace ID: `10508245`
- Space: `STRIQ`
- Space ID: `90140247191`
- List: `StrIQ`
- List ID: `901403371774`
- Default status: `On Deck`
- Default priority: `normal`
- Default time-tracking task: `86b79404b` (`STRIQ`)
- Preston ClickUp user ID: `12890094`
- Main assignee for most StrIQ work: `Austin Teague`
- Austin ClickUp user ID: `82259978`
- Austin email: `adteague89@gmail.com`

## Status Semantics

- `On Deck`: ready to start ASAP, clear enough to implement or investigate now.
- `Backlog`: feature request, roadmap idea, discovery item, or work that depends on a later product/platform decision.

Use the user's requested status when supplied. When classifying from meeting notes, use `On Deck` only for concrete follow-ups or ready implementation work; use `Backlog` for speculative improvements.

## Assignee Routing

- Assign Austin (`82259978`) for general dev/product/UI work unless the user says otherwise.
- Assign Preston (`12890094`) for AI, data methodology, data quality, analytics, cost analysis, customer-facing data investigations, or any task the user says should be tagged to "me" or "Preston".
- Assign both only when the user explicitly asks or the task clearly needs both ownership tracks.
- Resolve assignees through ClickUp tools if a new name/email appears.

## Task Intake

When creating StrIQ tasks:

1. Use list ID `901403371774` unless the user explicitly asks for another ClickUp list.
2. Apply the assignee routing above before falling back to Austin.
3. Use status `On Deck` and priority `normal` unless the user specifies otherwise or the status semantics above imply `Backlog`.
4. Preserve any user-provided estimate, due date, title, screenshots, acceptance criteria, and implementation notes in the task description.
5. When tasks come from Fathom calls or other source material, include short direct quotes and source links/timestamps in the task description.
6. If the task creation tool cannot set the time estimate on create, create the task first and then update `time_estimate` in minutes.

## Time Tracking

When tracking time for StrIQ work, use the single ClickUp task `86b79404b` (`STRIQ`) by default, regardless of the specific implementation or investigation task being discussed.

- Add a short description of what was worked on for each time entry.
- Do not search for a more specific task for StrIQ time tracking unless the user explicitly asks for a different task.
- Use workspace ID `10508245`.

## Related Repos

Treat these as StrIQ-related unless the user says otherwise:

- `/Users/preston/Code/striq-backend`
- `/Users/preston/Code/striq-api`
- `/Users/preston/Code/ios-striq`
- `/Users/preston/Code/frontend`
- `/Users/preston/Code/striq-shared-docs`
