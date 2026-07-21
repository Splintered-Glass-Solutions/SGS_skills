---
name: pm-delegate
description: >-
  PM delegate: delegate highlighted or selected portfolio work to the correct Codex project
  agent, bounded worker, or approval queue. Use from the project-management
  thread when Preston highlights a blocker, next action, task packet, or PM
  update line and asks to delegate it.
---

# PM Delegate

## Overview

Use this skill to turn selected PM text into a routed delegation without making
the manager thread do all the work. The manager thread keeps routing,
prioritization, approval gates, and final synthesis. In general, a delegation
should spin up a fresh bounded worker thread for the selected work instead of
shoehorning execution into an old persistent project thread. Persistent Project
Agent threads are PM/orchestrator lanes and context anchors, not default
implementation or research workers.

Use existing project threads for project continuity, fan-in, closeout review,
or explicit "continue this lane" work. Use a new bounded worker thread for the
actual delegated task whenever the work is implementation, QA, source research,
planning/research, cleanup, screenshots, status classification, validation, or
proof collection.

This skill is intentionally for the portfolio/project-management thread. For
normal single-repo continuation, use the repo's usual skill or `$next-step`
instead.

## Inputs

Use the highlighted text, slash-command `$ARGUMENTS`, or the latest user message
as the delegation candidate. If there is no clear candidate, ask Preston for the
missing selected text.

The selected text may be:

- a blocker
- a safe next action
- a project row from a portfolio update
- a worker packet
- a stale/no-movement item
- a QA/review follow-up
- a repo hygiene or finish-line task

## Required Preflight

1. Read `/Users/preston/.codex/portfolio/project-registry.md`.
2. Read `/Users/preston/.codex/portfolio/thread-registry.md`.
3. Identify the relevant project and any persistent project thread. Treat the
   persistent thread as context and coordination metadata, not as the default
   execution target. For normal delegated work, create a new bounded worker
   thread in the matching project/workspace when thread creation tooling is
   available.
4. Read `/Users/preston/.codex/portfolio/approval-ledger.md`.
5. Read `/Users/preston/.codex/portfolio/work-ledger.md` and
   `/Users/preston/.codex/portfolio/work-ledger.jsonl`.
6. Read `/Users/preston/.codex/portfolio/pm-ledger-clickup-model.md`.
7. Read `/Users/preston/.codex/portfolio/standards-registry.md`.
8. Read `/Users/preston/.codex/skills/pm-project-agent/SKILL.md` before
   messaging any persistent Project Agent thread.
9. For broad or multi-project selections, read
   `/Users/preston/.codex/skills/orchestrator-mode/SKILL.md` and make an
   explicit delegation decision.
10. If creating a worker packet, read:
   - `/Users/preston/.codex/portfolio/templates/worker-task-packet.md`
   - `/Users/preston/.codex/portfolio/templates/worker-closeout-contract.md`

## Routing Decision

Classify the selected item into one route:

- `persistent_project_thread`: use when the thread registry has a verified
  `thread_id`, the action fits `when_to_message_this_thread`, and the work is
  coordination, continuity, synthesis, closeout review, project-lane follow-up,
  or Preston explicitly asks to continue/use that existing thread.
- `bounded_worker`: use when the work fits `when_to_create_new_worker_instead`,
  such as repo QA, implementation, source research, cleanup, screenshots,
  planning/research, status classification, validation, or proof collection.
- `ask_preston`: use when the target project is ambiguous, the selected text
  asks for prioritization, or a product/business decision is required.
- `action_proposal`: use when delegation would involve creating/changing a
  persistent project thread, deploys, sends, production mutation, DB
  grants/ownership/RLS/roles, protected-branch operations, purchases, or broad
  paid/compute work. Do not treat creating a short-lived bounded worker thread
  for an explicitly requested delegation as an action-proposal event.
- `no_action`: use when the selected item is already resolved or has no current
  useful delegation.

Prefer a new bounded worker thread over a persistent project thread for nearly
all delegated work. Prefer the persistent project thread only for project
continuity, fan-in/fan-out coordination, closeout review, or when Preston
explicitly asks to use/continue the old thread.

Fresh-thread delegation rule:

- For every successful delegation, name the new bounded worker thread or queued
  worktree/thread id. Also name the relevant persistent project thread when one
  exists, but label it as `project_context_thread`, not the execution target.
- Every fresh bounded worker has the delegated-subtask marker `🧩` in its title.
  Use `🧩 <Project>: <bounded task>` by default.
- When the selected work belongs to an Elephant Dinner, release train, sprint,
  or other explicitly numbered batch, preserve its numerical emoji at the very
  start of the worker title: `<batch emoji> 🧩 <Project>: <bounded task>`. Do not
  substitute a different number within the same batch.
- Keep emoji out of branch names, worktree paths, work IDs, and dedupe keys.
  Store the human-facing title, `batch_id`, and `batch_marker` in the local
  ledger event when a batch exists.
- If the route is `bounded_worker` and thread creation tooling is available,
  create a fresh bounded worker thread directly from the PM thread with the
  right project/workspace, packet, authority limits, stop conditions, and
  closeout contract.
- After creation, use the thread-title tool to apply the required title because
  thread creation may infer a different title from the prompt. If worktree
  setup returns only a pending ID, record the desired title and apply it as soon
  as the real thread ID resolves.
- If direct worker thread creation tooling is unavailable, send the packet to
  the relevant verified Project Agent and explicitly instruct it to create a
  fresh bounded worker thread. This is a fallback, not the default.
- Do not send delegated execution into an old project thread merely because it
  exists. Only use the old thread directly when the selected work is truly
  project continuity/fan-in or Preston explicitly asks to use that thread.

## Execution Rules

When the route is `bounded_worker`:

1. Create a self-contained task packet with:
   - project and repo/source path
   - objective
   - current known state
   - in scope and out of scope
   - authority limits
   - standards to apply
   - required proof
   - validation expected
   - stop conditions
   - required closeout contract
2. Confirm the relevant project/workspace and persistent project context when
   one exists.
3. Create a fresh bounded worker thread directly when thread creation tooling is
   available. The worker prompt must include:
   - `WORKER_ROLE: BOUNDED_DELEGATED_WORKER`
   - `WORKER_TITLE: <batch emoji when applicable> 🧩 <Project>: <task>`
   - `BATCH_ID` and `BATCH_MARKER` when the source plan supplies them.
   - The worker owns only the scoped packet, not project-level direction.
   - The worker must keep the authority limits and stop conditions.
   - The worker must return the closeout contract.
4. If direct worker-thread creation is unavailable, use the verified Project
   Agent only as a dispatcher: send the packet and explicitly instruct it to
   create a fresh bounded worker thread, not execute the work in the old thread.
5. If neither worker-thread creation nor project-thread messaging is available,
   save or return the packet and state that it is ready to send.
6. Write or update the local durable record first: append a `delegated`
   work-ledger event with a stable `work_id`, dedupe key, the new worker
   thread id or pending worktree id, any project context thread id, and the
   routing method used.
7. Create ClickUp only when the delegation produces actionable follow-up that
   Preston or another worker must act on and task creation is authorized.
   Do not create ClickUp for informational delegation status, duplicates,
   completed/no-op state, or no-next-action items. Use dedupe key format
   `pm:work:<project>:<work_id>:<slug>` and report `ClickUp not created` if
   creation is not authorized or fails.
8. Validate the work ledger.

When the route is `persistent_project_thread`:

1. Confirm `thread_id` is not `TBD` and `binding_status` is `verified_existing`.
2. Confirm the selected work fits `when_to_message_this_thread`.
3. Send a bounded prompt only when current authority permits internal Codex
   thread messaging and the work is genuinely continuity/fan-in/closeout.
4. Include `PROJECT_AGENT_ROLE: PM_ORCHESTRATOR_NOT_WORKER`, a stop condition,
   and required closeout. If the prompt contains executable repo work, direct
   the Project Agent to create a fresh bounded worker thread and supervise
   rather than execute directly.
5. Append a `delegated` or `waiting` work-ledger event before any ClickUp
   consideration.
6. Apply the PM ledger / ClickUp hybrid model for actionable follow-up tasks.
7. Validate the work ledger.

When the route is `action_proposal`:

Do not perform the action. Return:

```text
ACTION_PROPOSAL:
  target:
  action:
  risk:
  proof_ready:
  approval_needed:
  rollback_or_undo:
```

Update the approval ledger only when the decision needs to persist beyond the
current turn.

## Portfolio-Specific Routing Notes

- Broad Bonfire project-agent/orchestrator context should prefer
  `/Users/preston/Code/bonfire_shared_docs`; scoped app QA and implementation
  should use `/Users/preston/Code/bonfire`.
- Broad StrIQ project-agent/orchestrator context should prefer
  `/Users/preston/Code/striq-shared-docs`; scoped frontend/backend/stage work
  should use the matching implementation repo.
- Persistent Project Agents are PM lanes. They should route implementation, QA,
  source research, screenshots, validation, cleanup, and other execution to
  fresh bounded worker threads, then monitor and report back. Do not reuse them
  as catch-all worker threads.
- Garden.io hygiene, finish-line QA, visual checks, and isolated website/app
  fixes should usually become bounded workers.
- Personal ops, client communications, and support/customer-facing work must not
  send external messages unless Preston explicitly asks to send.
- Production deploys, production jobs, protected branches, and DB permission
  changes always require an `ACTION_PROPOSAL`.

## Output Shape

Use icon-prefixed PM section headers so delegation outcomes are obvious at a
glance. Keep the canonical label text after the icon.

For successful delegation, return:

```text
🧵 DELEGATED:
🎯 TARGET:
🧭 ROUTE:
🆕 WORKER THREAD:
🏷️ WORKER TITLE:
🧵 PROJECT THREAD:
🔢 BATCH:
🆔 WORK_ID:
🔁 DEDUPE_KEY:
🛡️ AUTHORITY:
📌 CLICKUP:
✅ VALIDATION:
⏭️ NEXT CHECK:
```

For blocked delegation, return:

```text
🔴 NOT DELEGATED:
⚠️ REASON:
🧭 NEXT SAFE STEP:
⚠️ ACTION_PROPOSAL:
```

Keep the final answer compact. Link durable artifacts or ledger paths instead
of pasting long packets.
