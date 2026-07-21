---
description: PM plate-spin pass to revive idle projects with safe next prompts and bounded delegation candidates.
argument-hint: [optional-project-or-lane]
---

# PM Plate Spin

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/plate-spin/SKILL.md` (`pm-plate-spin`).
2. Also apply `/Users/preston/.codex/skills/project-portfolio-manager/SKILL.md` (`pm-project-portfolio-manager`), `/Users/preston/.codex/skills/orchestrator-mode/SKILL.md`, and `/Users/preston/.codex/skills/pm-project-agent/SKILL.md`.
3. Treat `$ARGUMENTS` as an optional project, lane, or idle-work hint.
4. Read portfolio registries, approval ledger, work ledger, standards registry, and relevant dispatcher scorecards before scanning.
5. Read `/Users/preston/.codex/portfolio/pm-ledger-clickup-model.md`.

## Guardrails

- Prefer safe, small, reversible project movement over busywork.
- Use Bonfire and StrIQ shared-docs repos as umbrella context for broad project-order questions.
- Treat Project Agents as PM/orchestrator lanes. Safe spins that involve execution should become bounded worker prompts routed through the Project Agent, not work for the Project Agent to perform directly.
- Do not message project threads, create threads, deploy, send external messages, mutate production, or perform gated actions without the required approval path.
- Return next safe prompts for project threads or bounded workers, and append/validate work-ledger events only when lifecycle state changes.
- Write local durable records for every observed item first. Create ClickUp tasks only for actionable follow-ups with dedupe keys; report `ClickUp not created` when task creation is not authorized or fails.
