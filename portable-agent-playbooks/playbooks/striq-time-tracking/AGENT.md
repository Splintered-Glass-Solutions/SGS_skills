# Striq Time Tracking Agent Playbook

This is a platform-neutral version of the `striq-time-tracking` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Log or start ClickUp time tracking for StrIQ work across striq-backend, striq-api, ios-striq, frontend, and striq-shared-docs. Use when the user asks to track time, log time, add time, start a timer, preserve an active timer, or report StrIQ time for implementation, investigation, QA, planning, release, or shared-docs work.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

# StrIQ Time Tracking

## Overview

Use this skill to track StrIQ time consistently without rediscovering the
ClickUp destination. Default to a manual time entry on the standing StrIQ task
unless the user explicitly asks to start a running timer.

## Defaults

- ClickUp workspace ID: `10508245`
- Default task: `STRIQ`
- Default task ID: `86b79404b`
- Default task URL: `https://app.clickup.com/t/86b79404b`
- Default description style: concise, work-specific note
- Time zone: America/Chicago

Treat these repos as StrIQ-related unless the user says otherwise:

- `<workspace>/striq-backend`
- `<workspace>/striq-api`
- `<workspace>/ios-striq`
- `<workspace>/frontend`
- `<workspace>/striq-shared-docs`

## Workflow

1. Classify the request.
   - For "track time", "log time", "add time", or "track time on this", create a
     manual time entry.
   - For "start tracking now", "start a timer", or "run a timer", check the
     currently running timer first, then start a timer only if no conflicting
     timer is active.
   - For "track this work individually" or similar, preserve any active timer
     and create a separate manual entry.
2. Use ClickUp tools. If the ClickUp tools are not loaded, search for the
   ClickUp tool capability first.
3. Do not search for a narrower ClickUp task unless the user names a specific
   task, repo task, assignee, or destination. Use task `86b79404b` by default.
4. Use America/Chicago local time for start and end values.
5. If the current thread provides enough context, estimate the duration
   pragmatically and state the assumption. Prefer rounded useful durations over
   excessive precision.
6. If duration or timing is genuinely missing, ask one concise question before
   logging time.
7. Keep the description short and useful, such as
   `StrIQ shared-docs workflow and skill setup`.
8. Avoid optional fields that have been unreliable unless required by the tool:
   do not add tags by default; omit billable unless the user explicitly specifies
   it or the ClickUp tool requires a value.

## Manual Entry Pattern

Use the ClickUp add-time-entry tool with this shape when available:

```json
{
  "task_id": "86b79404b",
  "start": "YYYY-MM-DD HH:MM",
  "duration": "Xh Ym",
  "description": "Short StrIQ work description"
}
```

Use the workspace ID `10508245` if the tool requires a workspace.

## Active Timer Guardrail

Before starting any new StrIQ timer, inspect the current running timer. If a
timer is already running, do not overwrite or stop it unless the user explicitly
asks. For a separate manual entry, preserve the active timer and ask only for
the missing duration/details needed to add the separate entry.

If a StrIQ investigation is interrupted and the user says to track time on it,
log the interrupted-but-useful work with a short descriptive note. Do not claim
the investigation is complete just because the time was logged.

## Final Response

After logging or starting time, report:

- Task name and URL
- Duration
- Start and end time in Central time, or timer start time if a running timer was started
- Description
- Billable status if returned or specified
- Any active-timer preservation or blocker that affected the result

