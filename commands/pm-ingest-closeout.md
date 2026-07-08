---
description: PM ingest a worker or project-thread closeout into the portfolio work ledger.
argument-hint: [selected-closeout-or-closeout-path]
---

# PM Ingest Closeout

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at
   `/Users/preston/.codex/skills/pm-ingest-closeout/SKILL.md`.
2. Treat `$ARGUMENTS` as the selected closeout text, pasted closeout, closeout
   artifact path, or context needed to find the closeout.
3. If `$ARGUMENTS` is empty, infer the selected closeout from the current
   conversation or selection context when obvious; otherwise ask for the missing
   closeout text or artifact path.
4. Read `/Users/preston/.codex/portfolio/pm-ledger-clickup-model.md`.

## Guardrails

- Append only valid `WORK_LEDGER_UPDATE` JSON from the closeout.
- Validate the work ledger after append.
- Regenerate and validate `current-state`.
- Treat local ledger/current-state as the source of truth. Create ClickUp only for actionable follow-ups with dedupe keys, and report `ClickUp not created` when not authorized or failed.
- Do not deploy, send external messages, mutate production, create Codex
  threads, or modify approval ledgers unless explicitly requested.
