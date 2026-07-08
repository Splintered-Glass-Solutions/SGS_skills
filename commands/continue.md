---
description: Resume interrupted Codex work from the current context.
argument-hint: [optional-recovery-context]
---

# Continue

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/continue/SKILL.md`.
2. Treat `$ARGUMENTS` as optional recovery context for the interrupted work.
3. If `$ARGUMENTS` is empty, infer the active objective from the current
   conversation, active plan, repo state, terminal output, and durable artifacts.
4. Resume the same objective at the next unfinished step; do not restart the
   task unless the previous state is unrecoverable.
5. Run the task-type validation or evidence step before reporting completion.

## Guardrails

- Latest user instruction wins over older context.
- Separate confirmed evidence from inferred state.
- Do not run production deploys, migrations, paid/broad jobs, destructive data
  changes, permission/RLS/grant/ownership changes, protected-branch operations,
  or real external sends without explicit current-thread approval for the exact
  target.
- Do not expose secrets or overwrite unrelated dirty work.
- If continuation is ambiguous, ask the smallest possible question instead of
  starting a new direction.
