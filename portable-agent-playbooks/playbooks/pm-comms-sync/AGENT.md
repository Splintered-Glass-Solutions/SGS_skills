# PM Comms Sync Agent Playbook

This is a platform-neutral version of the `pm-comms-sync` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

PM comms sync: manually run the communication safety-net scan across registered Slack, text, email, ClickUp, Teams, Skool, and client-contact surfaces. Use when the user wants to refresh comms monitoring outside the scheduled four-hour automation or validate the PM comms monitor.

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

# PM Comms Sync

## Overview

Run the same workflow as the scheduled PM comms monitor on demand. The goal is
to find new communication-derived action items, persist checkpoints, and avoid
duplicate capture.

Default mode is `ledger_first`: write candidates, duplicates, blockers, and
source checkpoints to the local comms ledger. Create ClickUp tasks only when the
current prompt or automation memory explicitly enables `clickup_create_enabled`.

## Safety

Do not send Slack messages, emails, texts, Teams messages, Skool replies, or
client messages. Do not mark source messages read. Do not mutate production
systems, deploy, change accounts, issue refunds, alter permissions, or expose
secrets.

Creating ClickUp tasks is allowed only when `clickup_create_enabled` is true
for the run and duplicate checks pass.

## Required Preflight

Read these first:

- `<agent-config>/portfolio/comms/source-registry.md`
- `<agent-config>/portfolio/comms/comms-ledger.jsonl`
- `<agent-config>/automations/pm-comms-monitor-every-4-hours-2/memory.md`

Use source-specific memory before rescanning:

- `<agent-config>/automations/nightly-email-task-triage/memory.md`
- `<agent-config>/automations/striq-feedback-issue-monitor/memory.md`

## Source Scan Order

1. Recover checkpoints from the comms monitor memory and source registry.
2. Scan only deltas where stable source ids or timestamps exist.
3. For sources without verified access or ids, perform a bounded discovery pass
   and record `blocked_source` or `needs_source_mapping` rather than guessing.
4. Classify candidates as actionable, review, duplicate, noise, or blocked.
5. Search local ledger and ClickUp duplicate anchors before creating any task.
6. Append compact JSONL events for candidates, created tasks, duplicates,
   blockers, and source checkpoint updates.
7. Refresh the monitor memory with per-source status and next-run checkpoint.

## Source Coverage

Registered surfaces include:

- SGS Slack
- StrIQ Slack
- StrIQ text threads
- Bonfire text threads
- SGS ClickUp
- Studio ClickUp
- SGS, HeyBonfire, personal, Caesura Ventures, Sparrowbend, Stewardship,
  R-T-I Outlook, and StrIQ email accounts
- Teams
- StrIQ Skool communities
- named direct-client email relationships such as Vanessa/Selah, John
  Nix/Songs4ACause, and Caleb/Stewardship

## Actionability Rules

Capture an item when the user likely needs to act, decide, delegate, unblock,
reply, review, approve, schedule, pay, sign, provide information, or follow up.

Ignore newsletters, receipts, automated notices, FYI-only status, duplicate
alerts, already-captured tasks, and chatter without a concrete ask unless the
source is a direct client or active project blocker.

If an item is ambiguous but plausibly important, record it as `needs_review`.
If ClickUp creation is enabled, create a low or normal priority `Review:` task.

## ClickUp Task Shape

When task creation is enabled, each task must include:

- action-oriented title
- source, requester, timestamp, project/client, and source link or stable id
- short evidence summary, not long quoted content
- recommended next action
- explicit due date with estimated-vs-explicit note
- duplicate anchors searched
- tags where supported: source, project/client, and `pm-comms`

Default destination for uncategorized communication tasks is ClickUp workspace
`10508245`, list `901414592170`, assignee `12890094`, unless the source
registry names a more specific project destination.

## Output Shape

```text
PM COMMS SYNC:
MODE:
SOURCE COVERAGE:
NEW ACTIONABLE:
REVIEW ITEMS:
TASKS CREATED:
DUPLICATES SKIPPED:
BLOCKED SOURCES:
CHECKPOINTS UPDATED:
NEXT RUN MEMORY:
```

End every run with explicit accounting. A no-new run is successful only when
the source coverage and checkpoint status are clear.

