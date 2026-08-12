---
description: PM project portfolio manager pass across projects, threads, approvals, work ledger, and scorecards.
argument-hint: [portfolio-scope-or-question]
---

# PM Project Portfolio Manager

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `$CODEX_HOME/skills/pm-project-portfolio-manager/SKILL.md`.
2. Treat `$ARGUMENTS` as the requested portfolio scope or question.
3. Read project registry, thread registry, approval schema, approval ledger, work ledger, standards registry, and relevant dispatcher scorecards.
4. Read `$CODEX_HOME/portfolio/approval-schema.md`.
5. Read `$CODEX_HOME/portfolio/delegation-watchlist.md` when delegation follow-through is in scope.
6. Read `$CODEX_HOME/portfolio/pm-ledger-clickup-model.md`.
7. Read `$CODEX_HOME/skills/pm-project-agent/SKILL.md` when the scope involves Project Agent threads.
8. Use `$orchestrator-mode` for all-project scans, dispatcher runs, stale-work sweeps, multi-repo current-state scans, or broad delegation passes.

## Guardrails

- Do not deploy, send messages, mutate production, create/message Codex threads, change DB permissions, or touch protected branches without a fresh `ACTION_PROPOSAL`.
- Keep local proof, hosted/browser proof, dev-live proof, and production-live proof separate.
- Append and validate work-ledger or scorecard updates when the run changes durable PM state.
- Dispatcher scorecards must separate activity from outcome movement: blockers removed, the user decisions reduced, delegated tasks completed, stale projects revived, false-positive delegations, unread threads cleared safely, and comms items converted to tasks.
- When approval entries change, run `$CODEX_HOME/portfolio/scripts/validate-approval-ledger.mjs`.
- Show exact the user decisions blocking motion from `current-state.approvals.blocking_decisions`.
- Show delegation follow-through flags from `current-state.delegation_watchlist.flagged`.
- Treat persistent Project Agent threads as PM/orchestrator lanes, not workers. Route executable work to bounded workers through them, and flag `project_agent_executed_worker_work` if a Project Agent directly executes worker-scoped work.
- Write or update a local durable record for every observed PM item before considering ClickUp.
- Create ClickUp only for actionable follow-ups with dedupe keys. Do not create ClickUp for ready-to-mark-read, passive status, duplicate, no-next-action, completed, or no-op observations.
- If ClickUp creation fails or is not authorized, keep the local ledger/report as source of truth and report `ClickUp not created`.
