---
description: PM comms sync to manually run the communications monitor and refresh local comms state.
argument-hint: [optional-source-project-or-clickup-mode]
---

# PM Comms Sync

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `/Users/preston/.codex/skills/pm-comms-sync/SKILL.md`.
2. Treat `$ARGUMENTS` as an optional source, project, client, or mode filter.
3. Default to `ledger_first` unless `$ARGUMENTS` explicitly enables ClickUp creation.
4. Do not send messages, replies, texts, posts, or emails.
