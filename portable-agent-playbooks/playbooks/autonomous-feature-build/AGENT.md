# Autonomous Feature Build Agent Playbook

This is a platform-neutral version of the `autonomous-feature-build` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when the user wants a full feature built end to end with the agent acting as the orchestrator: create or track a goal, inspect the repo, plan implementation, delegate bounded research, coding, testing, and log-reduction slices to cheaper capable subagents, use agent-safe-run and low-token guardrails, implement the changes, verify the result, and report proof plus remaining risks.

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

# Autonomous Feature Build

Use the agent as the orchestrator to build the requested feature end to end. Keep
product interpretation, architecture, decomposition, integration, validation
strategy, synthesis, and final review in the main thread. Delegate bounded
research, coding, testing, and log-reduction slices to cheaper capable subagents
or parallel tool waves when the work is independent and the expected evidence is
clear.

Invoking this skill is standing approval to perform the non-destructive work
needed to make the feature actually function end to end after inspection and
safety review. That includes local code edits, tests, docs, migrations, schema
updates, non-destructive database upserts/seeds/backfills, queue/job setup,
provider configuration, environment-variable additions, and other required
local or dev/staging setup steps when the target environment is clear and the
operation is compatible with existing data and deployed code.

This standing approval does not waive stricter approval boundaries from system,
developer, project, or user instructions. Stop and ask for exact approval before
permissions, grants, roles, ownership, RLS/policy changes, destructive data
operations, production DB mutations, billing changes, external customer/partner
messages, protected-branch operations, or dev/production deploys unless those
actions are specifically requested in the current conversation. If an earlier
bounded delegation packet or planning-only instruction conflicts with
end-to-end execution, treat the newest explicit user instruction as the desired
scope, but still surface the scope change and run the safety review before live
mutation.

Pair this with `$orchestrator-mode` for broad decomposition and with
`$agent-safe-run` for long, noisy, browser-heavy, or multi-agent work. Keep the
main thread lean: targeted searches, compact reads, bounded output, file-backed
logs for verbose commands, and no repeated streaming watchers in chat.

## Start

1. Create a concrete goal for the feature when the host supports goal tracking.
2. Classify the task and state the success bar.
3. Inspect the repo before planning implementation details.
4. Identify the smallest set of independent workstreams.
5. Identify required live, local, or shared-state changes such as migrations,
   seeds, backfills, source-sync setup, queue/job setup, env additions, or
   provider configuration.
6. Perform a safety review for any stateful mutation: target environment,
   exact command/payload, rollback or forward-fix path, compatibility with
   existing data/deployed code, tenant isolation, auth/security impact, and
   whether the action crosses a stricter approval boundary.
7. Decide what must stay in the main thread and what can be delegated.
8. Launch at most one bounded delegation wave before integrating results.

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

- Prefer `rg` and precise path filters over broad reads.
- Use parallel tool calls for independent inspections.
- Read only the files needed for the next decision.
- Use small output caps and summarize large outputs from file-backed logs.
- Avoid asking subagents for broad narrative; ask for evidence and decisions.
- Stop delegating when coordination cost exceeds likely savings.
- Switch to `$agent-safe-run` triage if the agent runtime becomes slow, hot,
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

## Default Framing

"I will use `$autonomous-feature-build` to build this feature end to end. I will
create a concrete goal, use `$orchestrator-mode` to keep this agent thread as
the architect and reviewer, pair long or noisy work with `$agent-safe-run`, and
delegate bounded research, coding, testing, and log-reduction slices to cheaper
capable subagents while keeping integration, validation strategy, and final
review in the main thread."

