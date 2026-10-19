# PM Plate Spin Agent Playbook

This is a platform-neutral version of the `pm-plate-spin` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

PM plate spin: run a project-local "spin the plates" pass for the project where the skill was invoked. Identify idle work, stale delegated work, and small safe next moves only within that project. Never scan or route other projects unless the user explicitly invokes a separate portfolio-wide workflow. Always pair with pm-project-portfolio-manager and orchestrator-mode.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.


# PM Plate Spin

## Overview

Run a bounded activation pass for exactly one project: the project where this
skill was invoked. The goal is to create useful movement without inventing
busywork, duplicating active work, or crossing approval gates.

## Scope Boundary (Non-Negotiable)

- Resolve the invocation project from an explicit project path when provided;
  otherwise use the nearest Git root containing the current working directory.
- Scan only that project's repository, worktree, project-local artifacts, and
  exact thread/project bindings. Filter shared ledgers to records belonging to
  that project.
- Do not enumerate, summarize, compare, classify, or route work for any other
  project, even when global registries, portfolio ledgers, or open agent threads
  make other work visible.
- Interpret "each" or "spin the plates" as each relevant item within the
  invocation project, never as each project in the portfolio.
- If a requested next step belongs to another project, stop with
  `SCOPE_BLOCKED` and explain that it needs a separate, explicitly requested
  portfolio workflow. Do not perform a cross-project fallback.
- If the current directory is not inside a recognizable project, do not guess
  from a sibling repository or a global default; report the missing project
  context and stop.

Use `$pm-project-portfolio-manager` for the durable portfolio operating contract
and `$orchestrator-mode` for routing, delegation decisions, and fan-in/fan-out
discipline. Keep the manager thread responsible for prioritization, synthesis,
approval gating, and final review.

## Required Preflight

Read the current governing files before scanning. Use global registries only to
resolve and filter the single invocation project; do not enumerate other
projects from them:

- `<agent-config>/skills/project-portfolio-manager/SKILL.md` (`pm-project-portfolio-manager`)
- `<agent-config>/skills/orchestrator-mode/SKILL.md`
- `<agent-config>/skills/pm-project-agent/SKILL.md`
- The current project's entry in `<agent-config>/portfolio/project-registry.md`,
  if one exists, only to confirm the exact project root and configured owner/agent.
- The current project's exact entry in `<agent-config>/portfolio/thread-registry.md`,
  if one exists; never use it to discover approximate destinations.
- Project-filtered records from `<agent-config>/portfolio/approval-ledger.md`,
  `<agent-config>/portfolio/work-ledger.md`, and
  `<agent-config>/portfolio/work-ledger.jsonl`.
- `<agent-config>/portfolio/pm-ledger-clickup-model.md` and
  `<agent-config>/portfolio/standards-registry.md`, applied only to the
  current project.
- The current project's scorecard records, if any. Do not load or summarize
  portfolio-wide scorecards during a project-local run.

If creating a worker packet, also read:

- `<agent-config>/portfolio/templates/worker-task-packet.md`
- `<agent-config>/portfolio/templates/worker-closeout-contract.md`

## Scan Targets

Look for current movement signals, not stale assumptions, only within the
resolved invocation project:

- The exact project's persistent thread binding and `last_checked` value in the
  thread registry. Confirm that the recorded path matches the resolved project.
- Work-ledger items with `active`, `delegated`, `waiting`, `blocked`,
  `no_new_signal`, or old `completed` states that imply a next follow-up.
- Pending approval-ledger decisions for this project that prevent safe movement.
- The latest scorecard for this project, if present; do not run a portfolio
  dispatcher or compare project scorecards.
- Open, unread, or recently active agent threads whose recorded project and path
  exactly match the current project.
- Existing repo/docs artifacts in the current project only, as needed to confirm
  a safe next move.

If the invocation project itself is a example-project-12 or example-project-13 shared-docs project, treat
its shared docs as umbrella context for that project:

- example-project-12 umbrella context: `<workspace>/example-project-1`
- example-project-13 umbrella context: `<workspace>/example-project-3`

Use implementation repos only when they are inside the resolved project scope
and the task is scoped execution, validation, QA, or code changes. When the
invocation project is not one of those shared-docs projects, do not reach into
their docs or implementation repositories.

## Idle Classification

Classify each lane with one status:

- `active`: current worker, project thread, automation, or repo work is already
  moving.
- `waiting_on_user`: movement depends on a the user decision or approval.
- `blocked_escalate`: blocked item is stale, risky, or needs explicit
  escalation.
- `continue_thread`: an open/unread or persistent thread has useful continuation
  context.
- `ask_shared_docs`: example-project-12 or example-project-13 needs umbrella planning context before
  choosing work.
- `safe_spin_ready`: a small bounded task can move the lane without approval.
- `no_action`: no meaningful next move, duplicate, or too risky without more
  signal.

`ask_shared_docs` is valid only when the shared-docs project is the resolved
invocation project. It is not a cross-project routing mechanism.

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
  non-`TBD` `thread_id`, the binding is verified, its project/path match the
  resolved invocation project, the prompt fits `when_to_message_this_thread`,
  and the current run explicitly authorizes thread messaging.
- Persistent Project Agent threads are PM/orchestrator lanes, not workers. Use
  them to pick the next safe worker, monitor worker progress, review closeouts,
  and report status upward.
- Use a bounded worker for repo execution, QA, screenshots, security review,
  source research, cleanup, or validation. If a verified Project Agent exists,
  route the worker packet through that Project Agent with
  `PROJECT_AGENT_ROLE: PM_ORCHESTRATOR_NOT_WORKER`.
- Use `ask_shared_docs` only for broad prioritization inside the resolved
  shared-docs project.
- Use `ACTION_PROPOSAL` before any thread creation or messaging, deploy,
  external send, production mutation, DB permission change, protected-branch
  operation, purchase, broad compute run, or irreversible action.
- Do not message approximate destinations. If the target cannot be verified,
  return the exact prompt as ready-to-send instead.
- Never create a worker, prompt, or task in another repository. If the safest
  move would cross the project boundary, return `SCOPE_BLOCKED` instead.
- Do not duplicate active work. If work-ledger says a lane is active or
  delegated, report the follow-up point instead of starting another worker.
- Flag `project_agent_executed_worker_work` when an existing Project Agent
  thread directly implemented, tested, researched, or QA'd work that should have
  gone to a bounded worker. The next safe prompt should restore the PM pattern:
  delegate remaining execution to a worker and ingest any valid closeout.

## Work-Ledger Rules

Record every observed item for the resolved project locally before considering
ClickUp. Do not create records for other projects discovered in global sources.
Use:

- work-ledger events when lifecycle state changes
- clean-unreads reports for unread-thread status
- comms ledger for communication-derived observations
- approval ledger for the user decisions
- current-state regeneration for scan summaries

Append compact work-ledger events when lifecycle state changes in the run:

- `active`, `delegated`, `waiting`, `blocked`, `completed`, `no_new_signal`, or
  equivalent statuses allowed by the runbook.
- Include stable `work_id`, `event_type`, `status_after`, source, artifact,
  next action, and relevant `thread_id`, `approval_id`, or worker id.
- Do not write secrets or long logs.
- Validate the work ledger after appending.

For read-only assessment with no lifecycle change, report `none`.

ClickUp is only for actionable follow-ups surfaced by the plate-spin pass:
the user decision needed, worker/project follow-up needed, failed/not-green
validation needing retest/fix, blocked escalation, or communication follow-up.
Do not create ClickUp tasks for passive active/waiting status, duplicates,
ready-to-mark-read threads, no-next-action items, or completed/no-op state.
Use dedupe key format `pm:work:<project>:<work_id-or-thread_id>:<slug>` and
report `ClickUp not created` when creation is not authorized or fails.

## Output Shape

Use icon-prefixed PM section headers so plate-spin reports are easy to scan.
Keep the canonical label text after the icon.

```text
📍 PROJECT SCOPE:
🌀 PLATE SPIN STATUS:
😴 IDLE LANES:
🧵 OPEN/UNREAD THREADS:
⚠️ WAITING ON PRESTON:
🔴 BLOCKED / ESCALATE:
🟢 SAFE SPINS:
🧭 READY PROMPTS:
⚠️ ACTION PROPOSALS:
🧾 WORK LEDGER UPDATES:
🗂️ LOCAL RECORDS:
📌 CLICKUP TASKS:
📊 DISPATCHER SCORECARD:
🧾 PROOF GATHERED:
⏭️ NEXT CHECK:
```

Keep final updates compact. Recommend at most five safe spins for the resolved
project. Never summarize other projects. A broader activation wave requires a
separate, explicit portfolio-workflow request.
