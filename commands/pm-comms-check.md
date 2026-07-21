---
description: PM comms check for outstanding communication follow-ups from the comms ledger and monitor memory.
argument-hint: [optional-source-project-or-time-window]
---

# PM Comms Check

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `/Users/preston/.codex/skills/pm-comms-check/SKILL.md`.
2. Treat `$ARGUMENTS` as an optional source, project, client, or time-window filter.
3. Default to read-only consolidation.
4. Do not scan every external source unless the user asks to sync; use `$pm-comms-sync` for that.
5. Read `/Users/preston/.codex/portfolio/pm-ledger-clickup-model.md`.

## Guardrails

- Use the local comms ledger as source memory.
- Do not create ClickUp tasks from a check run.
- Report missing local records or `ClickUp not created` statuses with dedupe keys when relevant.
