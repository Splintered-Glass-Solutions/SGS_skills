---
description: PM project portfolio manager pass across projects, threads, approvals, work ledger, and scorecards.
argument-hint: [portfolio-scope-or-question]
---

# PM Project Portfolio Manager

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/project-portfolio-manager/SKILL.md` (`pm-project-portfolio-manager`).
2. Treat `$ARGUMENTS` as the requested portfolio scope or question.
3. Read project registry, thread registry, approval ledger, work ledger, standards registry, and relevant dispatcher scorecards.
4. Use `$orchestrator-mode` for all-project scans, dispatcher runs, stale-work sweeps, multi-repo current-state scans, or broad delegation passes.

## Guardrails

- Do not deploy, send messages, mutate production, create/message Codex threads, change DB permissions, or touch protected branches without a fresh `ACTION_PROPOSAL`.
- Keep local proof, hosted/browser proof, dev-live proof, and production-live proof separate.
- Append and validate work-ledger or scorecard updates when the run changes durable PM state.
