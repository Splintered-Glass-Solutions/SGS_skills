---
description: Track the current thread's work in the correct local project ledger.
argument-hint: "[duration]"
---

# Time Track

The user invoked this command with: $ARGUMENTS

1. Read and follow `<agent-config>/skills/timetrack/SKILL.md`.
2. Treat `$ARGUMENTS` as the requested duration, such as `2hr`, `90m`, or
   `1h30m`.
3. Infer the project and evidenced work items from the current thread.
4. For 120 minutes or more, split the time into gradual, truthful records as
   described by the skill.
5. Append only to the local ignored project ledger. Do not create or update
   ClickUp time entries.
6. Return the exact records written and their total.
