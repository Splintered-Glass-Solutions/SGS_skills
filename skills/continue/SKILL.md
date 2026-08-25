---
name: continue
description: >-
  Resume interrupted Codex work after a limit, pause, network cutout, app reload,
  context compaction, or stalled thread. Use when the user invokes /continue,
  says continue, resume, pick back up, keep going, do not restart, or asks Codex
  to continue the exact work already underway without losing context, existing
  sessions, scoped approvals, proof layers, or the next action-time gate.
---

# Continue

## Purpose

Use this skill to resume the same work that was already in progress. The goal is
continuity: rebuild the last known objective, identify what changed or was
already proven, and carry the work forward without starting over or asking
the user to restate context when it can be recovered locally.

This skill is not a license for open-ended autonomous work. Resume the active
objective, not a new adjacent idea.

## Recovery Contract

Start with a compact recovery pass before taking action:

1. Identify the latest user instruction and treat it as authoritative.
2. Reconstruct the active objective from the conversation, any active plan,
   tool output, terminal output, current working directory, changed files, and
   durable artifacts.
3. Separate confirmed facts from inferred state.
4. Detect the task type: quick lookup/message, debugging, build work, planning,
   research/transcript, QA/review, automation, or communication.
5. Resume at the next unfinished step using the matching task rule.

Do not restart the whole task unless the previous state is unavailable or
clearly invalid. Do not claim prior work was verified unless there is visible
evidence in the thread, filesystem, terminal, git state, logs, test output, or a
durable artifact.

A newer user instruction to continue resumes the work even if a host goal still
shows a stale `blocked` status. Do not recreate the goal or treat that stale
status as a fresh blocker. Update the plan, continue safe lanes, and follow the
host tool's explicit threshold before marking the resumed goal blocked again.

## Preflight

Inspect only what is needed to recover momentum:

- current conversation and latest user message
- active plan/checklist status, if present
- current `cwd`, repo root, branch, and `git status --short --branch` when in a
  repo
- relevant changed files and recent diffs
- current terminal output if a command or dev server may still be running
- local instructions such as `AGENTS.md`
- durable artifacts named by the thread: notes, plans, checkpoints, logs,
  screenshots, generated files, test reports, queue/checkpoint files, or memory
  files
- the task's prep/build execution ledger, approval register, and proof matrix
- any persistent PTY, browser, server, OAuth, or auth session IDs and current
  state

### Pause Recovery

If the visible thread contains a `$pause` checkpoint:

1. Treat its `Objective`, `Current state`, `Preserved state`, `Resume at`, and
   `Waiting on` fields as the primary recovery index, then verify any
   drift-prone state that is cheap to recheck.
2. Resume from `Resume at`; do not repeat completed work merely because the
   thread was paused.
3. After recovery succeeds, inspect the current thread title. If and only if it
   begins with `🛑 `, remove that single leading marker and preserve every other
   character in the title.
4. Do not remove a stop-sign emoji located elsewhere in the title, and do not
   alter the thread's pin, archive, or ownership state.
5. If title renaming fails, continue the recovered task and report that the
   visual pause marker remains.

If a command/session may still be running, inspect it before starting duplicate
work. If a server is already running and useful, reuse it.

For multi-system work, recover this minimum state before widening the run:

- exact repo/worktree/branch/base SHA
- current objective and acceptance/test ledger
- approvals by class, target, account, environment, and evidence
- local, merged, hosted, shared data/provider, and production/customer-visible
  proof status
- completed/pending migrations, env changes, provider configuration, and deploys
- exact next safe action and exact next gated action

## Resume Decision

After preflight, state the recovered state in one or two sentences:

```md
Continuing: <objective>. Last confirmed state: <evidence>. Next step: <action>.
```

Then continue according to the task type:

- `quick lookup/message`: finish the requested answer or message in one short
  pass.
- `debugging`: state the current hypothesis before editing, then validate the
  fix or report why validation is blocked.
- `build work`: make one coherent implementation pass, then run the relevant
  tests, screenshot checks, browser checks, typecheck, build, or syntax check.
- `planning`: stop when the spec or decision brief is complete; do not drift
  into implementation unless the user asked for it.
- `research/transcript`: preserve durable notes, citations, source IDs, or
  extracted evidence before closing.
- `QA/review`: lead with findings and evidence references.
- `automation`: include create/no-create accounting, checkpoint handling, and
  next-run memory when the workflow supports it.
- `communication`: produce concise recipient-fit text or send only if the user
  clearly asked to send.

## Safety Gates

Continue autonomously only when the next step is recoverable, bounded, and
within the current thread's approvals.

Stop and ask for the smallest missing input when continuation would require:

- production deploys, promotions, rollbacks, broad live jobs, or paid provider
  runs without explicit current-thread approval
- database grants, ownership, roles, RLS, destructive data changes, or
  permission changes without exact approval
- sending customer/client/team messages unless the user explicitly asked to send
- overwriting unrelated dirty work, force-pushing, rebasing shared work, or
  merging protected branches without approval
- product, billing, auth, privacy, compliance, or data-retention choices that
  cannot be inferred safely
- secrets exposure or copying secrets into logs/messages

If the user already gave approval in the current thread, preserve the exact
scope: target repo, branch, environment, account, recipient, and action.

Preserve valid exact approval across the interruption using the task tuple:
`action + repo + branch/SHA when relevant + environment + provider/account +
exact operation or payload + approval evidence + status`. Invalidate it only
when revoked or when the target, account, environment, branch/SHA, payload/diff,
permission/destructive impact, or relevant external state materially changed.
Do not treat that preserved approval as satisfying a tool-required action-time
confirmation. Prepare the final action, ask at action time, and continue other
safe work while waiting.

Treat a shared database used by production as production-connected even if the
application target is development. Never infer permission to reapply or widen
RLS/grants/roles/ownership from a general “continue.”

## When State Is Ambiguous

If the prior work cannot be recovered confidently:

1. Do a lightweight local evidence pass.
2. State what is known, what is inferred, and what is missing.
3. Choose the safest useful next step if one exists.
4. Ask one concise question only when no safe continuation is possible.

Use this no-op shape when blocked:

```md
I cannot safely continue yet.

Known: <evidence>.
Missing: <specific context or approval>.
Smallest input needed: <question or approval>.
```

## Checkpointing

For long, cross-repo, high-cost, or uncertain resumptions, checkpoint before a
second major pass:

1. Objective
2. What changed or was found
3. Proof gathered
4. Remaining uncertainty
5. Recommended next action

If the work should survive another pause, save or update the durable artifact
that the workflow already uses, such as a plan file, QA report, run log,
checkpoint file, memory note, or generated handoff. Do not create new memory
entries unless the user explicitly asks for memory updates.

Update the checkpoint before yielding at a biometric/login/action-time gate so
the next continuation can reuse the prepared operation and existing session.
Never store secret values.

## Final Shape

Keep the final answer short and continuity-focused:

- what was resumed
- what changed or was completed
- what was verified
- files/artifacts changed
- remaining blocker or next action, if any
- the proof layer reached and the exact next gated action

If relying on recovered or inferred state, say so plainly.
