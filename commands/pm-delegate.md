---
description: PM delegate selected portfolio work to the correct project agent or bounded worker.
argument-hint: [selected-work-or-context]
---

# PM Delegate

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/delegate/SKILL.md` (`pm-delegate`).
2. Treat `$ARGUMENTS` as the selected/highlighted work to delegate.
3. If `$ARGUMENTS` is empty, infer the selected work from the current
   conversation or selection context when obvious; otherwise ask for the missing
   selected text.
4. Use `$pm-project-portfolio-manager` routing rules and the portfolio registries
   before delegating.
5. Delegate only to a verified persistent project thread or bounded worker when
   the registry and current authority allow it.

## Guardrails

- Do not deploy, send external messages, mutate production data, run production
  jobs, change DB grants/ownership/RLS/roles, purchase anything, or touch
  protected branches without a fresh `ACTION_PROPOSAL`.
- Do not create new Codex threads unless the selected work explicitly requires
  it and the current conversation approves it.
- Prefer bounded workers for repo QA, implementation, cleanup, screenshots,
  validation, and proof collection.
- Append and validate work-ledger events when delegation changes work state.
