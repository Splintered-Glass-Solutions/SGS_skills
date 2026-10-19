# Build Implement Agent Playbook

This is a platform-neutral version of the `build-implement` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Implement and test one accepted build item with a Luna high subagent in the existing batch worktree.

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

# Build Implement

Dispatch one implementation worker under the [worker contract](../build-it/references/worker-contract.md).
Use `gpt-6-luna` with `high` reasoning. Use `fork_turns="none"` for a new worker.
Reuse an idle Luna/high planner via followup_task only if its recorded model and
worktree match and its same-item context passes the worker contract's lean-reuse
check. Start a fresh implementer for a new item. Existing agents cannot be assumed
to switch models through a
follow-up message; create a correctly configured worker when necessary.

Acquire the sole-writer slot for the existing batch worktree before dispatch.
Follow the shared [repository worktree lifecycle contract](../repo-worktree-lifecycle/references/operating-contract.md): this worker writes only to its assigned checkout and does not create or switch branches/worktrees.
Pass the accepted item plan and relevant acceptance IDs, paths, state and authority.
Do not create another worktree, branch or visible task per item. The worker must
not invoke build-it, build-plan, build-implement or broad autonomous orchestration,
spawn agents, integrate branches, push or deploy. It implements the item using
repo patterns, adds meaningful coverage, performs one bounded quality review,
updates required docs/QA records and runs focused local checks. The shared steps 2–6 of bulk-auto-build remain required: issue-to-test coverage,
required data prerequisites, QA records, docs, one quality review and focused
local validation. Reconcile existing proof first. Read finish-line before any
missing coverage/catalog or data-completion operation; read bounded make-it-better
for the quality review and test for missing/invalidated runtime assertions.
Return every gate as passed, parent-scheduled under the execution contract, or
blocked; conditional loading never makes required finishing work optional.
Required shared-data operations remain parent-coordinated under inherited authority;
keep them scheduled or blocked correctly rather than attempting live writes.

Return the exact ending SHA and scoped dirty state, changed files, checks/results,
evidence paths, docs/QA record paths, unresolved issues and next action. Prefer a
scoped checkpoint commit when repository rules permit; never include unrelated work.
The parent verifies state, updates the canonical ledger and releases the writer
slot only after the worker has completed or stopped and no owned command can write.
A failed or interrupted worker retains ownership until reconciled.

Reuse this worker for precise independent review findings only while its context
remains lean; otherwise return its checkpoint and refresh under the worker contract.
Repair only the accepted
item, rerun affected checks and return a new revision. Standalone invocation
requires an accepted scope and explicit target worktree; it grants no deployment.
