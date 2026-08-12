---
description: PM ingest a worker or project-thread closeout into the portfolio work ledger.
argument-hint: [selected-closeout-or-closeout-path]
---

# PM Ingest Closeout

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at
   `$CODEX_HOME/skills/pm-ingest-closeout/SKILL.md`.
2. Treat `$ARGUMENTS` as the selected closeout text, pasted closeout, closeout
   artifact path, or context needed to find the closeout.
3. If `$ARGUMENTS` is empty, infer the selected closeout from the current
   conversation or selection context when obvious; otherwise ask for the missing
   closeout text or artifact path.
4. Read `$CODEX_HOME/portfolio/pm-ledger-clickup-model.md`.
5. Read `$CODEX_HOME/skills/pm-project-agent/SKILL.md` when the closeout came from a persistent Project Agent thread.

## Guardrails

- Append only valid `WORK_LEDGER_UPDATE` JSON from the closeout.
- Validate the work ledger after append.
- Regenerate and validate `current-state`.
- Treat local ledger/current-state as the source of truth. Create ClickUp only for actionable follow-ups with dedupe keys, and report `ClickUp not created` when not authorized or failed.
- If a Project Agent directly executed worker-scoped work, ingest valid ledger state but flag `project_agent_executed_worker_work` and route remaining execution to a bounded worker.
- Do not deploy, send external messages, mutate production, create Codex
  threads, or modify approval ledgers unless explicitly requested.
