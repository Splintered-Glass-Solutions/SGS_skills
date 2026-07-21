---
name: pm-thread-sweep
description: >-
  PM thread sweep: review every open Codex thread for a named project, verify
  its work and required dev deployment, close only fully finished threads,
  continue incomplete work through autonomous-feature-build, and consolidate
  Preston decisions into numbered a/b/c questions. Use for Bonfire or any
  project when open threads need lifecycle review, finish-line coordination,
  decision triage, PM ledger updates, and safe closeout.
---

# PM Thread Sweep

## Purpose

Run a proof-based lifecycle sweep across all open Codex threads for one project.
The sweep reviews actual work, separates finished work from merely stopped work,
continues safe incomplete work, stages decisions for Preston, and closes only
threads with no remaining project or PM obligation.

This is a PM/orchestrator workflow. It does not turn the portfolio thread or a
persistent Project Agent into an implementation worker.

## Invocation

Accept a project name, repo family, saved project, batch, or explicit thread set.

Examples:

- `/pm-thread-sweep Bonfire`
- `/pm-thread-sweep StrIQ`
- `/pm-thread-sweep BF-W29 only`
- `Use PM Thread Sweep on all open Bonfire threads; finish safe work and close complete tasks.`

If scope is omitted, infer it only when one project is unambiguous. Otherwise ask
for the project before inspecting or mutating threads.

## Required Skills And State

Read and apply:

1. `/Users/preston/.codex/skills/orchestrator-mode/SKILL.md`
2. `/Users/preston/.codex/skills/project-portfolio-manager/SKILL.md`
3. `/Users/preston/.codex/skills/pm-project-agent/SKILL.md`
4. `/Users/preston/.codex/skills/pm-ingest-closeout/SKILL.md`
5. `/Users/preston/.codex/skills/close-thread/SKILL.md`
6. `/Users/preston/.codex/skills/autonomous-feature-build/SKILL.md`
7. `/Users/preston/.codex/skills/feature-finish-line/SKILL.md`
8. `/Users/preston/.codex/portfolio/project-registry.md`
9. `/Users/preston/.codex/portfolio/thread-registry.md`
10. `/Users/preston/.codex/portfolio/approval-ledger.md`
11. `/Users/preston/.codex/portfolio/work-ledger.jsonl`
12. `/Users/preston/.codex/portfolio/standards-registry.md`

Read the current project plan, release manifest, worktree registry, and latest
project-specific scorecard when they exist.

## Default Bonfire Scope

For `Bonfire`, discover threads by title, cwd, repo, ledger references, parent
thread, and project binding across:

- `/Users/preston/Code/bonfire`
- `/Users/preston/Code/Bonfire_AI`
- `/Users/preston/Code/Bonfire_ETL`
- `/Users/preston/Code/bonfire_shared_docs`
- `/Users/preston/Code/bonfire-super-admin`
- Bonfire worktrees and BF-W29 artifacts

Do not rely on a title-only search. Include a thread when its cwd, source packet,
work ledger, parent task, or project binding establishes project ownership.

## Phase 1: Discover And Normalize

1. List recent/open threads broadly, then query the project and each repo name.
2. Exclude the current PM thread from closure review.
3. Preserve already closed titles beginning with `－`; report them only when
   duplicate or reopened work matters.
4. Record for every candidate:
   - thread ID and exact title;
   - saved project, cwd, repo, worktree, branch, and HEAD when applicable;
   - persistent Project Agent, bounded worker, automation/monitor, research,
     release/integration, or ordinary task classification;
   - latest turn status and last substantive message;
   - work ID, batch, parent/project context thread, and dedupe key;
   - artifact, PR, deployment, approval, and ledger references.
5. Deduplicate aliases, repeated delegations, and child threads representing the
   same work. Preserve one canonical lifecycle record with all related IDs.

Use stable sweep dedupe keys:

`pm:thread-sweep:<project-slug>:<thread-id>:<latest-turn-id-or-head-sha>`

## Phase 2: Review The Work

Treat worker messages as evidence, not verdict. Review findings first.

For each implementation or QA thread:

1. Inspect the final diff, candidate SHA, branch/worktree state, and overlap with
   newer project work.
2. Verify relevant lint, type, unit, integration, build, browser, security, and
   feature-finish-line evidence for the risk level.
3. Confirm skipped tests are intentional and non-blocking.
4. Check PR status, target branch, required checks, review state, merge/deploy
   status, and exact deployed SHA when remote work is relevant.
5. Separate local green, PR green, dev-live green, and production-live claims.
6. Confirm generated artifacts, temporary browser state, one-off mutation tools,
   and dirty work are intentionally preserved or cleaned.
7. Confirm any `WORK_LEDGER_UPDATE` was ingested and validated. If worker JSON is
   malformed, do not silently rewrite it; save a PM observation and identify the
   normalization follow-up.

For research, planning, communication-prep, or status threads:

1. Verify the promised artifact exists and is decision-ready.
2. Check whether the artifact still leaves a send, assignment, acknowledgment,
   implementation, approval, or follow-up obligation.
3. Do not close merely because the research pass ended.

## Deployment Requirement

Classify deployment as `required`, `not_required`, or `gated`.

Deployment is normally required before closure when the thread owns user-facing
code, shared dev behavior, provider configuration, migration-dependent behavior,
or a release slice whose finish line names dev/staging proof.

Deployment is normally not required for read-only research, planning packets,
internal documentation, local tooling with a local-only finish line, or work
explicitly superseded before release.

When deployment is required, closure needs all of:

- exact candidate is integrated into the intended dev/staging target;
- deployed SHA or immutable artifact matches the reviewed candidate;
- stable dev/staging URL or environment identity is recorded;
- required migrations/configuration completed under valid authority;
- hosted health and critical browser/API checks are green;
- no rollback, alert, or unresolved hosted failure remains.

Do not deploy merely because the sweep found a missing deployment. Deploy only
when the current invocation explicitly approves the named environment and the
action does not cross a stricter boundary. Otherwise stage an `ACTION_PROPOSAL`.

## Lifecycle Classification

Assign exactly one primary state to each open thread:

### `READY_TO_CLOSE`

All work is reviewed and accepted, required validation is green, deployment is
not required or proven green, closeout is ingested, and no decision, action,
acknowledgment, follow-up, or child work remains.

### `KEEP_OPEN_ACTIVE`

The thread or its approved child worker is currently making useful progress.
Report its current step and next checkpoint; do not interrupt or duplicate it.

### `CONTINUE_WITH_AUTONOMOUS_BUILD`

Required work remains and is locally/dev safe to continue. The finish line is
clear enough for end-to-end execution without a Preston product decision.

### `DECISION_NEEDED`

Progress depends on a real Preston choice: product behavior, scope, priority,
human ownership, commercial position, external send, environment, migration,
protected branch, deployment, or security authority.

### `BLOCKED_EXTERNAL`

Progress depends on access, a provider, a client/teammate response, unavailable
credentials, rate limits, or another external state that Preston cannot resolve
by choosing among immediate implementation options.

### `EXCLUDED_PERSISTENT`

Persistent Project Agents and continuing recurring monitors remain open unless
Preston explicitly decommissions the lane. Review their health and unresolved
queue, but never close them just because the latest delegated batch finished.

### `ALREADY_CLOSED`

The title already starts with `－`. Do not double-prefix or reopen it during a
sweep.

## Absolute Closeability Gate

Every condition below must be true before closing:

- latest substantive request is satisfied;
- no unresolved review finding or test failure;
- no required uncommitted, unpushed, unmerged, undeployed, or unverified work;
- dev/staging proof is current when required;
- no pending Preston decision, external send, human acknowledgment, or action;
- no active child worker or expected closeout;
- closeout artifact and durable PM state are current;
- thread is not a persistent Project Agent or recurring monitor;
- closure will not hide a security, data, billing, migration, or release gate.

When uncertain, keep the thread open.

## Continue Incomplete Work

For `CONTINUE_WITH_AUTONOMOUS_BUILD`:

1. Review the thread's work and identify concrete deficiencies before messaging.
2. Use the same bounded worker thread when the context is coherent, the worktree
   remains valid, and no ownership conflict exists.
3. Send a concise continuation prompt that explicitly invokes
   `$autonomous-feature-build` and includes:
   - findings from the PM review;
   - exact remaining objective and finish line;
   - current candidate/base/worktree;
   - required local and dev proof;
   - deployment classification;
   - authority and exclusions;
   - closeout and valid ledger contract.
4. If the thread is a persistent Project Agent, tell it to supervise and create
   a fresh bounded worker; never ask the Project Agent to execute the build.
5. If the old worktree is stale, conflicted, deleted, or owned by another lane,
   create a fresh bounded worker from the correct source instead of reviving it.
6. Do not launch duplicate work. Check title, work ID, branch, source packet, and
   ledger dedupe keys first.
7. Keep no more than four technical continuation lanes active at once. Order
   dependencies and release/integration work before downstream feature lanes.

Autonomous build standing authority does not authorize external messages,
production mutation, protected-branch operations, deployments not explicitly
approved in the invocation, billing changes, destructive data actions, or DB
permission/RLS/grant/role/ownership changes.

## Stage Preston Decisions

Consolidate decisions across threads; do not ask the same underlying question
multiple times.

Use this exact format:

```text
1. [DECISION-ID] Short decision question
   a. Recommended: concrete choice and what it unlocks
   b. Alternative: concrete tradeoff
   c. Defer/decline: safe fallback and consequence
   Evidence: thread IDs, artifact/PR/deployment, current blocker
```

Rules:

- Number questions by urgency and dependency order.
- Use lowercase `a`, `b`, and `c` choices.
- Put the recommended choice first and label it `Recommended`.
- Make options mutually exclusive and executable.
- State exact environment, scope, migration, recipient, or owner when relevant.
- Never bury a DB permission, production, billing, external-send, or protected-
  branch approval inside a broad option.
- Provide a compact reply hint such as `Reply: 1a, 2c, 3b`.
- Write pending decisions to the approval ledger before reporting them.

## Close Eligible Threads

For each `READY_TO_CLOSE` thread:

1. Re-read its latest turn immediately before mutation.
2. Apply the `$close-thread` protocol to that explicit target thread:
   - preserve the exact current title;
   - prefix it with exactly `－` when not already prefixed;
   - use `set_thread_title` only;
   - do not archive, pin, message, hand off, fork, or alter repo state.
3. Verify the returned title begins with `－`.
4. Append a durable PM closure event with the proof and thread ID.
5. Report the exact thread title and why closure was safe.

The target thread is explicit during a sweep, so do not infer the current PM
thread or send `/close-thread` into unrelated threads.

## Durable Report And PM Ledger

Before final reporting, save:

`/Users/preston/.codex/portfolio/reports/thread-sweeps/YYYY-MM-DD-HHMM-<project-slug>.md`

Include:

- discovery scope and exclusions;
- one row per canonical thread;
- review evidence and deployment classification;
- closed threads;
- continued autonomous-build threads;
- active/blocked/external threads;
- consolidated decision set;
- ledger events appended or rejected;
- ClickUp accounting;
- exact next sweep checkpoint.

Write local durable records first. Create ClickUp tasks only for actionable
follow-ups and only when authorized. Never create tasks for informational status,
ready-to-close threads, duplicates, completed/no-op work, or passive waiting.

## Safety And Stop Conditions

- No external/customer/team messages without explicit approval.
- No production deploy or mutation without explicit approval.
- No protected-branch merge/push without explicit approval.
- No DB permissions, grants, roles, ownership, RLS, policies, destructive data,
  billing, or secret changes without exact approval.
- Stop if a thread's project ownership is ambiguous.
- Stop closure if proof is stale, deployment identity is uncertain, or another
  thread still depends on the work.
- Stop after two failed attempts to inspect the same inaccessible thread and
  classify it `BLOCKED_EXTERNAL` or `DECISION_NEEDED` with the exact gap.

## Final Report Shape

Use icons for scanning, but keep labels stable:

```text
📊 SWEEP SUMMARY:
✅ CLOSED:
🟢 DEPLOYED / VERIFIED:
🛠️ CONTINUING WITH AUTONOMOUS BUILD:
⏳ KEEP OPEN / ACTIVE:
🔴 BLOCKED:
🧠 PRESTON DECISIONS:
🧾 LEDGER / CLICKUP:
🔁 NEXT CHECKPOINT:
```

Report exact thread names and IDs, the last substantive-message synopsis, proof,
and the next step. Do not claim a thread is closed until the rename succeeds.
