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
5. Read `/Users/preston/.codex/skills/pm-project-agent/SKILL.md` before sending
   work to a persistent Project Agent.
6. Delegate only to a verified persistent project thread or bounded worker when
   the registry and current authority allow it.
7. Read `/Users/preston/.codex/portfolio/pm-ledger-clickup-model.md`.

## Guardrails

- Do not deploy, send external messages, mutate production data, run production
  jobs, change DB grants/ownership/RLS/roles, purchase anything, or touch
  protected branches without a fresh `ACTION_PROPOSAL`.
- Invoking `/pm-delegate` on clear selected work is approval to create one fresh
  bounded worker thread in the relevant existing Codex project. Creating a new
  persistent Project Agent or a new Codex project still requires a separate
  action proposal/approval.
- Title every fresh worker `🧩 <Project>: <task>`. When selected work carries a
  shared numerical batch marker, preserve it first: `<number emoji> 🧩
  <Project>: <task>`. Apply the title with the thread-title tool after creation.
- Keep emoji out of branch/worktree names and durable work/dedupe IDs.
- Persistent Project Agent threads are PM/orchestrator lanes, not workers.
- Prefer bounded workers for repo QA, implementation, cleanup, screenshots,
  validation, source research, and proof collection.
- When routing executable work through a Project Agent, tell it to create or
  request a dedicated worker thread, monitor that worker, review the closeout,
  and report back upward. Do not ask the Project Agent to execute directly.
- Append and validate work-ledger events when delegation changes work state.
- Write the local ledger record before any ClickUp task. Create ClickUp only for actionable follow-up with a dedupe key; report `ClickUp not created` when task creation is not authorized or fails.
