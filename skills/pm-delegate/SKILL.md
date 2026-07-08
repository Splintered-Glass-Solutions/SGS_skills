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
prioritization, approval gates, and final synthesis; the relevant verified
project thread owns the execution lane whenever one exists. Bounded agents or
workers should normally be launched from, or handed through, that project
thread so the project context and continuity stay in the right place.

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
3. Identify the relevant project and its persistent project thread. If the
   thread registry has a verified `thread_id` for that project, use that thread
   as the delegation anchor for any successful delegation unless the route is
   `ask_preston`, `action_proposal`, or `no_action`.
4. Read `/Users/preston/.codex/portfolio/approval-ledger.md`.
5. Read `/Users/preston/.codex/portfolio/work-ledger.md` and
   `/Users/preston/.codex/portfolio/work-ledger.jsonl`.
6. Read `/Users/preston/.codex/portfolio/standards-registry.md`.
7. For broad or multi-project selections, read
   `/Users/preston/.codex/skills/orchestrator-mode/SKILL.md` and make an
   explicit delegation decision.
8. If creating a worker packet, read:
   - `/Users/preston/.codex/portfolio/templates/worker-task-packet.md`
   - `/Users/preston/.codex/portfolio/templates/worker-closeout-contract.md`

## Routing Decision

Classify the selected item into one route:

- `persistent_project_thread`: use when the thread registry has a verified
  `thread_id`, the action fits `when_to_message_this_thread`, and the work is
  coordination, continuity, synthesis, or project-lane follow-up.
- `bounded_worker`: use when the work fits `when_to_create_new_worker_instead`,
  such as repo QA, implementation, source research, cleanup, screenshots,
  status classification, validation, or proof collection.
- `ask_preston`: use when the target project is ambiguous, the selected text
  asks for prioritization, or a product/business decision is required.
- `action_proposal`: use when delegation would involve thread creation,
  deploys, sends, production mutation, DB grants/ownership/RLS/roles,
  protected-branch operations, purchases, or broad paid/compute work.
- `no_action`: use when the selected item is already resolved or has no current
  useful delegation.

Prefer a bounded worker over a persistent project thread for executable repo
work. Prefer the persistent project thread for project continuity, planning
context, or fan-in/fan-out coordination.

Project-thread anchoring rule:

- For every successful delegation, name the relevant project thread and
  `thread_id`.
- If the selected item is executable repo work and the route is
  `bounded_worker`, first hand the worker packet into the relevant verified
  project thread and ask that project thread to run or spawn the bounded worker.
- Do not silently spawn a bounded worker directly from the portfolio manager
  thread when a verified project thread exists. Direct PM-thread spawning is
  allowed only when there is no verified project thread, project-thread
  messaging tooling is unavailable, or Preston explicitly asks the manager
  thread to spawn directly. In those cases, record the reason in the final
  answer and work-ledger event.

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
2. Confirm the relevant project thread is verified when one exists.
3. Send the packet to the relevant project thread when thread messaging tooling
   is available and authority permits internal Codex thread messaging. The
   prompt should tell the project thread to run or spawn the bounded worker, keep
   the stop conditions, and return the closeout contract.
4. Spawn a bounded worker directly from the PM thread only when no verified
   project thread exists, project-thread messaging tooling is unavailable, or
   Preston explicitly asks for direct PM-thread spawning. Include the reason in
   the worker packet, final answer, and work-ledger event.
5. If neither project-thread messaging nor worker tooling is available, save or
   return the packet and state that it is ready to send.
6. Append a `delegated` work-ledger event with a stable `work_id`, the project
   `thread_id`, and the project-thread anchoring method used.
7. Validate the work ledger.

When the route is `persistent_project_thread`:

1. Confirm `thread_id` is not `TBD` and `binding_status` is `verified_existing`.
2. Confirm the selected work fits `when_to_message_this_thread`.
3. Send a bounded prompt only when current authority permits internal Codex
   thread messaging.
4. Include a stop condition and required closeout.
5. Append a `delegated` or `waiting` work-ledger event.
6. Validate the work ledger.

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
- Garden.io hygiene, finish-line QA, visual checks, and isolated website/app
  fixes should usually become bounded workers.
- Personal ops, client communications, and support/customer-facing work must not
  send external messages unless Preston explicitly asks to send.
- Production deploys, production jobs, protected branches, and DB permission
  changes always require an `ACTION_PROPOSAL`.

## Output Shape

For successful delegation, return:

```text
DELEGATED:
TARGET:
ROUTE:
PROJECT THREAD:
WORK_ID:
AUTHORITY:
VALIDATION:
NEXT CHECK:
```

For blocked delegation, return:

```text
NOT DELEGATED:
REASON:
NEXT SAFE STEP:
ACTION_PROPOSAL:
```

Keep the final answer compact. Link durable artifacts or ledger paths instead
of pasting long packets.
