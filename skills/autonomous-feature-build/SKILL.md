---
name: autonomous-feature-build
description: >-
  Use when the user wants a full feature built end to end with Codex acting as
  the orchestrator: consume a prep-work run contract when available, create or
  track a goal, inspect the repo, plan
  implementation, delegate bounded research, coding, testing, and log-reduction
  slices to cheaper capable subagents, use codex-safe-run and low-token
  guardrails, always invoke and enforce token-saver, implement the changes,
  preserve a resumable execution ledger,
  verify each truth surface, and report proof plus remaining risks.
---

# Autonomous Feature Build

## Mandatory Token-Saver Contract

Always invoke and follow `$token-saver` before inspecting, planning,
delegating, or executing. This is a required operating dependency of
`$autonomous-feature-build`, even when the user does not mention it.

- Build from the latest accepted run contract, checkpoint, or artifact after a
  cheap drift check. Do not replay stable discovery or prior reasoning.
- Search before opening and read only the smallest source slices needed for the
  next architecture, implementation, or validation decision.
- Redirect noisy builds, tests, browser runs, deploy logs, and monitors to
  file-backed artifacts. Bring only exit status, counts, exact failures,
  bounded excerpts, and paths into chat.
- Require compact subagent returns: changed files, commands, evidence,
  failures, residual risk, and decisions needed. Do not request or accept broad
  narrative or full log reproduction.
- Update one compact accepted-state ledger at major boundaries; resume from it
  instead of reconstructing the run from conversation history.
- Report only meaningful milestones and changed state. Do not narrate routine
  commands, repeat prior updates, or emit unchanged polling results.
- Stop blind retries and speculative work. After a failure, change a concrete
  hypothesis or input before retrying.
- Keep the final handoff short and link the durable ledger or evidence rather
  than pasting it.

Token conservation must never weaken product correctness, safety review,
validation, or proof. Reduce duplicate context and output, not required work.
If a path becomes noisy, stop or redirect it and continue from a compact
summary.

Use Codex as the orchestrator to build the requested feature end to end. Keep
product interpretation, architecture, decomposition, integration, validation
strategy, synthesis, and final review in the main thread. Delegate bounded
research, coding, testing, and log-reduction slices to cheaper capable subagents
or parallel tool waves when the work is independent and the expected evidence is
clear.

Invoking this skill is standing task-scoped approval to make the feature work
end to end after inspection and safety review. Do not pause for routine delivery
approval. That includes local code edits, tests, docs, branches, commits, pull
requests, ordinary PR merges, compatible migrations and schema updates,
non-destructive database upserts/seeds/backfills, queue/job setup, environment
variable additions, provider configuration, and deployment through Dev and
Production when the target is unambiguous and the change is compatible with
existing data and deployed code. Complete the delivery, verify it, and report
the result rather than asking whether to create a PR, merge it, run a normal
migration, or deploy it.

This standing authority does not waive stricter system, developer, project, or
user boundaries. Pause only for a genuinely dangerous, irreversible, or
materially expanded action: permissions, grants, roles, ownership, RLS/policy
changes; destructive or non-recoverable data operations; billing changes;
creating persistent OAuth clients, API keys, service accounts, or provider
account access; external customer/partner messages; or a protected-branch/tool
confirmation that the available authority cannot satisfy. When a deploy or
database action is ordinary and reversible or forward-fixable, make the best
safe decision and proceed. If an earlier bounded delegation packet or
planning-only instruction conflicts with end-to-end execution, treat the newest
explicit user instruction as the desired scope, run the safety review, and
continue without an approval checkpoint unless a stricter boundary applies.

Approval is not one boolean. Track these separately:

1. **Standing workflow authority** from this skill for ordinary implementation,
   delivery, migrations, and deployments in the identified target environments.
2. **Elevated resource/action approval** only for permissions, RLS, ownership,
   destructive or non-recoverable data work, billing, persistent OAuth/API
   access creation, or another named high-impact operation.
3. **Action-time confirmation** required by a tool or UI policy immediately
   before creating persistent access, sending communication, or another
   confirmation-gated action.

Persistent access creation requires elevated resource/action approval and may
also require a separate action-time confirmation. Earlier broad approval does
not replace either gate. Prepare the operation fully and ask only when the next
action is that gated final step.

Represent an elevated approval as:
`action + repo + branch/SHA when relevant + environment + provider/account +
exact operation or payload + approval evidence + status`. Preserve it across
`$continue` until revoked or invalidated by a changed target, materially changed
payload/diff, new permission or destructive impact, or expired external state.

Pair this with `$orchestrator-mode` for broad decomposition and with
`$codex-safe-run` for long, noisy, browser-heavy, or multi-agent work. Invoke
and enforce `$token-saver` first. Keep the
main thread lean: targeted searches, compact reads, bounded output, file-backed
logs for verbose commands, and no repeated streaming watchers in chat.

## Start

1. Load the latest `$prep-work` run contract or existing durable checkpoint when
   available. Reverify cheap drift-prone facts; do not repeat stable discovery.
2. Invoke `$token-saver`; define the narrow context packet, file-backed log
   locations, compact worker-return schema, retry bounds, and accepted-state
   checkpoint.
3. Create or resume a concrete goal when the host supports goal tracking. A
   stale `blocked` status must not override a newer user instruction to resume.
4. Classify the task and state the success bar.
5. Inspect the repo and confirm the worktree descends from the intended current
   base before editing. If it does not, use a clean current-base worktree or
   explicitly isolate the stale branch.
6. Identify the smallest set of independent workstreams.
7. Identify required live, local, or shared-state changes such as migrations,
   seeds, backfills, source-sync setup, queue/job setup, env additions, or
   provider configuration.
8. Perform a safety review for any stateful mutation: target environment,
   exact command/payload, rollback or forward-fix path, compatibility with
   existing data/deployed code, tenant isolation, auth/security impact, and
   whether the action crosses a stricter approval boundary.
9. Decide what must stay in the main thread and what can be delegated.
10. Launch at most one bounded delegation wave before integrating results.

## Resumable Execution Ledger

For multi-system work likely to pause, keep one durable checkpoint in the
workflow's existing artifact path. If none exists, create a task-scoped run-state
artifact under the repo's normal `output/`, `docs/qa/`, or equivalent ignored
artifact convention.

Keep it compact and update it after every major boundary:

- objective and accepted scope
- repo, worktree, branch, base SHA, and relevant PR/deploy IDs
- elevated approvals by class, target, account, and environment
- non-secret provider provenance: masked app/account, scopes, redirect URIs,
  secret names with present/missing status, and last verified time
- live truth matrix: local, merged branch, hosted environment, shared
  data/provider state, production/customer-visible
- migrations/env/provider operations completed or pending
- reusable PTY, browser, server, or auth sessions and their IDs/state
- proof gathered
- current blocker
- exact next safe action and exact next gated action

Never record secret values.

### Compact repair ledger

For a one-function repair or similarly narrow integration fix, use one
task-scoped ledger as the durable source of truth. Do not create separate docs,
finish-line, or QA worktrees or PRs merely to restate the same evidence unless
the repository release contract or the user explicitly requires them.

Include only: objective and root cause; task-owned commit; focused tests;
deployment image tag and digest when applicable; non-secret live request,
source, content, or job IDs; proof by layer; and any remaining rendered-UI
evidence or blocker. Reuse the repository's existing output or QA-artifact path
when one exists.

## External Integration And Environment Rules

- Treat a shared database used by production as production-connected even when
  the application target is Dev. Compatible, forward-fixable migrations are
  covered by standing workflow authority; RLS, grants, roles, ownership, and
  destructive production-data changes remain elevated actions.
- Before changing environment variables, determine whether the platform will
  auto-deploy or restart. Use a no-deploy option when available until the
  change is ready, then trigger at most one intentional deployment under this
  skill's standing authority.
- Prefer provider CLI/API setup when supported. Use browser/Computer Use only
  for provider steps that cannot be completed safely another way.
- Reuse existing PTY, browser, login, and dev-server sessions after inspecting
  their state. Do not start duplicates simply because the task resumed.
- If user authentication or biometrics block one lane, continue independent
  code, tests, docs, migration review, suite wiring, and release preparation.
  Stop the whole task only when no useful safe lane remains.
- Distinguish “provider configured,” “credentials installed,” “deployment using
  credentials,” “account connected,” and “provider-backed feature verified.”
  None implies the next.

## Main-Thread Responsibilities

- Own the product interpretation and technical design.
- Decide architecture, tradeoffs, validation strategy, and integration order.
- Decide and verify any required migrations, seeds, backfills, DB writes,
  queue/job setup, provider setup, or env changes covered by the skill's
  standing approval.
- Prevent parallel agents from editing the same files at the same time.
- Reopen important files and review delegated diffs before accepting them.
- Run or spot-check the verification that matters before claiming completion.
- Keep the goal status current until the feature is complete or genuinely
  blocked.
- Keep the durable execution ledger current enough that `$continue` can resume
  without reconstructing the whole run from chat history.

## Delegation Rules

Use cheaper capable subagents for bounded work such as:

- repo inventory and source tracing
- narrow implementation slices with clear file ownership
- focused tests, browser checks, screenshots, or log reduction
- alternate debugging hypotheses
- docs, migration, or integration impact scans

Each delegated prompt must include:

- repo path
- exact objective
- in-scope files or search targets
- out-of-scope areas
- expected return format
- verification commands
- stop conditions

Require compact returns with changed files, commands run, evidence gathered,
failures, residual risk, and any decision that still needs orchestrator
judgment.

## Safe Low-Token Mode

- Treat every `$token-saver` operating rule as binding for the entire run.
- Prefer `rg` and precise path filters over broad reads.
- Use parallel tool calls for independent inspections.
- Read only the files needed for the next decision.
- Use small output caps and summarize large outputs from file-backed logs.
- Avoid asking subagents for broad narrative; ask for evidence and decisions.
- Stop delegating when coordination cost exceeds likely savings.
- Switch to `$codex-safe-run` triage if Codex Desktop becomes slow, hot,
  swap-heavy, or helper processes accumulate.

## Completion Standard

Before the final response:

1. Inspect the final diff or final artifact.
2. Confirm every required local/dev/staging state change was either executed
   and verified, or explicitly marked blocked by a stricter approval boundary.
3. Run relevant tests, checks, screenshots, or browser verification for the
   feature's risk level.
4. Reconcile delegated evidence centrally.
5. Update the goal as complete only when no required work remains.
6. Report what changed, proof gathered, stateful operations performed or
   skipped, remaining risks, and recommended next
   action.
7. Report the live truth matrix explicitly; do not collapse local, merged,
   hosted, shared-provider/data, and production/customer-visible proof into one
   “done” claim.

## Default Framing

"I will use `$autonomous-feature-build` to build this feature end to end. I will
create a concrete goal, use `$orchestrator-mode` to keep this Codex thread as
the architect and reviewer, enforce `$token-saver`, pair long or noisy work with
`$codex-safe-run`, and
delegate bounded research, coding, testing, and log-reduction slices to cheaper
capable subagents while keeping integration, validation strategy, and final
review in the main thread."
