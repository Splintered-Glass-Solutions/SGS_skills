---
name: pm-plate-spin
description: >-
  PM plate spin: use for portfolio "spin the plates" passes that identify idle projects,
  open/unread Codex threads, stale delegated work, and small safe next moves to
  keep Preston's active projects moving. Use when asked to revive stalled
  project lanes, propose next prompts for project threads or workers, continue
  prior features, or ask Bonfire/StrIQ shared-docs umbrella contexts what the
  next order of business should be. Always pair with pm-project-portfolio-manager
  and orchestrator-mode.
---

# PM Plate Spin

## Overview

Run a bounded portfolio activation pass. The goal is to create useful movement
without inventing busywork, duplicating active work, or crossing approval gates.

Use `$pm-project-portfolio-manager` for the durable portfolio operating contract
and `$orchestrator-mode` for routing, delegation decisions, and fan-in/fan-out
discipline. Keep the manager thread responsible for prioritization, synthesis,
approval gating, and final review.

## Required Preflight

Read the current governing files before scanning:

- `/Users/preston/.codex/skills/project-portfolio-manager/SKILL.md` (`pm-project-portfolio-manager`)
- `/Users/preston/.codex/skills/orchestrator-mode/SKILL.md`
- `/Users/preston/.codex/portfolio/project-registry.md`
- `/Users/preston/.codex/portfolio/thread-registry.md`
- `/Users/preston/.codex/portfolio/approval-ledger.md`
- `/Users/preston/.codex/portfolio/work-ledger.md`
- `/Users/preston/.codex/portfolio/work-ledger.jsonl`
- `/Users/preston/.codex/portfolio/standards-registry.md`
- `/Users/preston/.codex/portfolio/scorecards/README.md`
- `/Users/preston/.codex/portfolio/scorecards/dispatcher-scorecard.jsonl`

If creating a worker packet, also read:

- `/Users/preston/.codex/portfolio/templates/worker-task-packet.md`
- `/Users/preston/.codex/portfolio/templates/worker-closeout-contract.md`

## Scan Targets

Look for current movement signals, not stale assumptions:

- Persistent project-thread bindings and `last_checked` values in the thread
  registry.
- Work-ledger items with `active`, `delegated`, `waiting`, `blocked`,
  `no_new_signal`, or old `completed` states that imply a next follow-up.
- Pending approval-ledger decisions that prevent safe movement.
- Latest dispatcher scorecards and run artifacts.
- Open, unread, or recently active Codex threads when thread tooling is
  available.
- Existing repo/docs artifacts only as needed to confirm a safe next move.

For Bonfire and StrIQ, treat the shared-docs repos as umbrella project context
for broad project-order questions:

- Bonfire umbrella context: `/Users/preston/Code/bonfire_shared_docs`
- StrIQ umbrella context: `/Users/preston/Code/striq-shared-docs`

Use implementation repos only for scoped execution, validation, QA, or code
changes.

## Idle Classification

Classify each lane with one status:

- `active`: current worker, project thread, automation, or repo work is already
  moving.
- `waiting_on_preston`: movement depends on a Preston decision or approval.
- `blocked_escalate`: blocked item is stale, risky, or needs explicit
  escalation.
- `continue_thread`: an open/unread or persistent thread has useful continuation
  context.
- `ask_shared_docs`: Bonfire or StrIQ needs umbrella planning context before
  choosing work.
- `safe_spin_ready`: a small bounded task can move the lane without approval.
- `no_action`: no meaningful next move, duplicate, or too risky without more
  signal.

## Safe Spin Menu

Prefer small tasks that collect proof or improve readiness:

- design audit or visual QA pass
- security or dependency review
- copy/content polish on a known surface
- focused test run or screenshot/browser proof
- docs/readiness cleanup
- repo hygiene classification
- blocker queue refresh
- "what should be next" prompt to a verified persistent project thread
- bounded worker packet for one repo or artifact family

Do not select work merely because a project is quiet. A safe spin needs a
specific target, a small scope, and a proof artifact.

## Routing Rules

- Use a verified persistent project thread only when the thread registry has a
  non-`TBD` `thread_id`, the binding is verified, the prompt fits
  `when_to_message_this_thread`, and the current run explicitly authorizes
  thread messaging.
- Use a bounded worker for repo execution, QA, screenshots, security review,
  source research, cleanup, or validation.
- Use `ask_shared_docs` for broad Bonfire/StrIQ prioritization before choosing
  scoped implementation work.
- Use `ACTION_PROPOSAL` before any thread creation or messaging, deploy,
  external send, production mutation, DB permission change, protected-branch
  operation, purchase, broad compute run, or irreversible action.
- Do not message approximate destinations. If the target cannot be verified,
  return the exact prompt as ready-to-send instead.
- Do not duplicate active work. If work-ledger says a lane is active or
  delegated, report the follow-up point instead of starting another worker.

## Work-Ledger Rules

Append compact work-ledger events only when lifecycle state changes in the run:

- `active`, `delegated`, `waiting`, `blocked`, `completed`, `no_new_signal`, or
  equivalent statuses allowed by the runbook.
- Include stable `work_id`, `event_type`, `status_after`, source, artifact,
  next action, and relevant `thread_id`, `approval_id`, or worker id.
- Do not write secrets or long logs.
- Validate the work ledger after appending.

For read-only assessment with no lifecycle change, report `none`.

## Output Shape

```text
PLATE SPIN STATUS:
IDLE LANES:
OPEN/UNREAD THREADS:
WAITING ON PRESTON:
BLOCKED / ESCALATE:
SAFE SPINS:
READY PROMPTS:
ACTION PROPOSALS:
WORK LEDGER UPDATES:
DISPATCHER SCORECARD:
PROOF GATHERED:
NEXT CHECK:
```

Keep final updates compact. Recommend at most five safe spins unless Preston
asks for a broader activation wave.
