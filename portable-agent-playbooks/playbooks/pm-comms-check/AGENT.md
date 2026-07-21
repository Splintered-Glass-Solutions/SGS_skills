# PM Comms Check Agent Playbook

This is a platform-neutral version of the `pm-comms-check` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

PM comms check: consolidate the user's communication follow-ups across the PM comms ledger, source checkpoints, blocked source reports, and created ClickUp tasks. Use when the user asks what communications, asks, follow-ups, approvals, or client/team items may be slipping through the cracks.

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

# PM Comms Check

## Overview

Run a read-only PM communications check. The goal is to show the user what needs
attention now without rescanning every source or creating new tasks.

Default posture: read-only. Do not send messages, reply, mark mail read, mark
threads read, create ClickUp tasks, update ClickUp, or mutate source systems.

## Required Inputs

Read these before reporting:

- `<agent-config>/portfolio/comms/source-registry.md`
- `<agent-config>/portfolio/comms/comms-ledger.jsonl`
- `<agent-config>/portfolio/pm-ledger-clickup-model.md`
- `<agent-config>/automations/pm-comms-monitor-every-4-hours-2/memory.md`

If available and relevant, also inspect:

- latest `pm-comms-monitor-every-4-hours-2` automation run output
- latest manual `pm-comms-sync` output in the current thread
- ClickUp task URLs or task ids already recorded in the comms ledger

## Classification

Classify open items into:

- `needs_the user_now`: direct ask, deadline, approval, blocker, or client issue.
- `delegatable`: clear task another project agent or worker can take.
- `waiting_on_other`: already responded to or waiting on someone else.
- `captured_in_clickup`: already persisted as a ClickUp task.
- `needs_review`: plausible but ambiguous follow-up.
- `blocked_source`: a source could not be checked and needs access recovery.
- `duplicate_or_noise`: already captured, FYI-only, automated, newsletter, receipt,
  or non-actionable chatter.

## Ledger / ClickUp Model

`pm-comms-check` is read-only by default. It reads the local comms ledger as the
audit/source memory and reports ClickUp status from existing ledger entries. It
must not create ClickUp tasks.

If the check discovers an observed follow-up that is missing from the local
ledger, report `local_record_missing` and the exact dedupe key to capture during
`pm-comms-sync`. Do not create ClickUp from the check.

ClickUp should exist only for actionable communication follow-ups:

- the user response/action needed
- direct client/team ask
- blocker or escalation
- approval/decision needed
- failed/not-green validation reported through comms

Do not create ClickUp for duplicate observations, FYI-only messages, already
captured tasks, completed/no-op state, or no-next-action items.

## Output Shape

Use icon-prefixed PM section headers so communications reports can be triaged
quickly. Keep the canonical label text after the icon.

```text
📬 PM COMMS CHECK:
🧭 STATUS:
⚠️ NEEDS PRESTON NOW:
🧵 DELEGATABLE:
📌 CAPTURED IN CLICKUP:
🟡 NEEDS REVIEW:
🔴 BLOCKED SOURCES:
🟢 DUPLICATES / NOISE:
📡 SOURCE COVERAGE:
🧭 NEXT SAFE ACTIONS:
```

For each actionable item include:

```text
- title:
  source:
  project:
  requester:
  received_at:
  evidence:
  clickup:
  dedupe_key:
  recommended_next_step:
```

Keep the answer compact. Prefer the newest unhandled items and anything with a
deadline, direct client impact, or blocked project work.

