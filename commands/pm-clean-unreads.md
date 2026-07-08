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

## Guardrails

- Mark only `ready_to_mark_read` threads read when mark-read tooling is available and the run is authorized.
- Exclude the current PM/project-management thread running this command from classification and cleanup; do not mark it read/unread or report it as incomplete.
- For every reported thread, include `thread_title`, `thread_id`, `thread_link` when available, and a compact `last_message_sample` from the final paragraph of the latest meaningful message.
- If a thread is incomplete, active, blocked, failed, missing proof, or has remaining action items, leave or mark it unread and report the next needed step.
- Do not archive as a substitute for read/unread cleanup.
- Append and validate work-ledger events only when cleanup materially changes PM state.
