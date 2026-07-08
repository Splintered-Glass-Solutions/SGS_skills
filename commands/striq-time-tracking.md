---
description: Log or start ClickUp time tracking for StrIQ work.
argument-hint: [time-context]
---

# StrIQ Time Tracking

Log or start ClickUp time tracking for StrIQ work.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/striq-time-tracking/SKILL.md`.
2. Treat `$ARGUMENTS` as the work description, duration, timing, repo context, or timer instruction.
3. If `$ARGUMENTS` is empty, infer the context from the current conversation when obvious; otherwise ask only for the missing duration or timing detail.
4. Use the default StrIQ ClickUp task unless the user names a different task or destination.
5. Preserve any already-running timer unless the user explicitly asks to stop or replace it.

## Output

Return:

- ClickUp task and URL
- Duration
- Central start and end time, or timer start time
- Description used
- Billable status if available
- Any active-timer caveat or blocker
