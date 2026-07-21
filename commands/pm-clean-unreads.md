---
description: PM clean unread Codex threads that are truly complete and keep incomplete work unread.
argument-hint: [optional-scope-or-thread-query]
---

# PM Clean Unreads

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/clean-unreads/SKILL.md` (`pm-clean-unreads`).
2. Treat `$ARGUMENTS` as an optional scope, query, project, or thread hint.
3. Default to a conservative dry-run classification unless the current prompt explicitly authorizes cleanup.
4. Read the portfolio registries, approval ledger, work ledger, and standards registry before broad cleanup.
5. Read `/Users/preston/.codex/portfolio/pm-ledger-clickup-model.md`.
6. Read `/Users/preston/.codex/skills/pm-project-agent/SKILL.md` when classifying Project Agent threads.

## Guardrails

- Mark only `ready_to_mark_read` threads read when mark-read tooling is available and the run is authorized.
- Exclude the current PM/project-management thread running this command from classification and cleanup; do not mark it read/unread or report it as incomplete.
- For every reported thread, include `thread_title`, `thread_id`, `thread_link` when available, and a compact `last_message_sample` from the final paragraph of the latest meaningful message.
- If a thread is incomplete, active, blocked, failed, missing proof, or has remaining action items, leave or mark it unread and report the next needed step.
- If a Project Agent thread directly executed worker-scoped work, keep it unread and classify the next step as `project_agent_executed_worker_work`.
- Do not archive as a substitute for read/unread cleanup.
- Append and validate work-ledger events only when cleanup materially changes PM state.
- Save every run to `/Users/preston/.codex/portfolio/reports/clean-unreads/YYYY-MM-DD-HHMM.md` with ready-to-mark-read, keep-unread, next step per thread, excluded current PM thread, and threads actually cleared.
- Use the local report as the durable ledger first. Create ClickUp tasks only for actionable kept-unread follow-ups, with dedupe keys. Report `ClickUp not created` when creation is not authorized or fails.
