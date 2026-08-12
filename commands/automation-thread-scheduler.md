---
description: Create or repair Codex automations as same-thread emoji-labeled heartbeats.
argument-hint: [automation-name-or-request]
---

# Automation Thread Scheduler

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `$CODEX_HOME/skills/automation-thread-scheduler/SKILL.md`.
2. Treat `$ARGUMENTS` as the automation name, automation id, or scheduling
   request.
3. Use the Codex `automation_update` tool for automation changes and
   `set_thread_title` for thread title changes.

## Defaults

- Prefer same-thread `heartbeat` automations.
- Add an emoji to the beginning of the target automation thread title.
- Do not create standalone cron automations unless the user explicitly asks for
  a separate standalone job, worktree, or project-scoped run.
- Search for duplicate schedules before creating or converting.
- Preserve automation memory and checkpoint files.

## Closeout

Report the changed automation id, heartbeat/thread status, emoji title,
duplicate cleanup result, memory update, and any remaining blocker.
