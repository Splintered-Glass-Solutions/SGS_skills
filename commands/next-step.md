---
description: Choose and run the next safe, bounded step from the current context.
argument-hint: [optional-context-or-goal]
---

# Next Step

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/next-step/SKILL.md`.
2. Treat `$ARGUMENTS` as optional context for selecting the next step.
3. If `$ARGUMENTS` is empty, infer the next step from the current conversation,
   active plan, repo state, and latest validation/deploy/QA evidence.
4. If the next step is safe, bounded, and useful, execute one focused pass.
5. If the next step is gated, ambiguous, unsafe, or low-value, do not make
   changes. State the blocker and the smallest input needed.

## Guardrails

- Do not run production jobs, migrations, broad provider/API work, paid jobs,
  customer messaging, protected-branch operations, destructive data changes, or
  deploy/promote actions without explicit current-thread approval for the exact
  target.
- Do not expose secrets.
- Do not overwrite unrelated dirty work.
- Stop after one coherent next step; do not chain into an open-ended loop.
