---
description: Recap the current thread with status, decisions, evidence, and next paths.
argument-hint: [optional-focus-or-save-request]
---

# Recap

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/recap/SKILL.md`.
2. Treat `$ARGUMENTS` as optional focus for the recap.
3. If `$ARGUMENTS` is empty, infer the scope from the current conversation,
   active objective, repo state, tool output, and latest validation/deploy/QA
   evidence.
4. Produce a concise recap with objective, current state, what happened,
   evidence, decisions made, open decisions, and next action paths A/B/C/D.
5. If the paths should be done sequentially, say "do all in order"; otherwise
   make clear that Preston should choose one.

## Guardrails

- Read-only by default: do not edit files, update memory, deploy, send
  messages, run broad jobs, or make external changes unless the command
  arguments explicitly request that action.
- Separate local, dev, hosted, and production status.
- Mark production deploys, migrations, data mutations, customer sends, paid
  provider runs, and permission/RLS/grant/ownership changes as gated.
- Do not expose secrets.
- If a fact cannot be verified from the thread or quick local evidence, label it
  as unknown instead of guessing.
