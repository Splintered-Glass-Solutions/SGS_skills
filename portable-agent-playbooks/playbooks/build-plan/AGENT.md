# Build Plan Agent Playbook

This is a platform-neutral version of the `build-plan` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Plan one build item with a bounded subagent; route simple designs to Luna high and complex designs to Sol 6.1 low.

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

# Build Plan

Dispatch one read-only item planner under the [worker contract](../build-it/references/worker-contract.md).
This skill plans; it does not create a task, worktree, implementation or release.

Use `gpt-6-luna` with `high` reasoning for a localized change with established
patterns and clear acceptance. Use `gpt-6.1-sol` with `low` reasoning when design
must resolve shared schemas, auth/permissions, billing, cross-service contracts,
rollout compatibility or materially competing product requirements. File count
alone is not complexity. Record a one-sentence routing reason.

Call `collaboration.spawn_agent` with `fork_turns="none"`, the chosen explicit
model/reasoning and the compact packet. The user-configured build-it workflow
authorizes these model overrides. The planner inspects only relevant source and
returns a proposed plan, acceptance assertions, likely files, dependencies,
rollout concerns and unresolved decisions. It makes no writes and spawns no workers.
The parent records the plan in the canonical ledger, resolves cross-item conflicts
and verifies it stays within accepted scope. A returned plan is not code proof.

Retain a Luna/high planner for the implementation follow-up only when it is idle
and its same-item context passes the worker contract's lean-reuse check. Do not
reuse it to plan later items. A Sol 6.1 planner must not become the implementer;
pass its concise plan to a new Luna/high worker through build-implement.
For a standalone invocation, return the plan and stop unless implementation was
also requested. If subagents or the specified model are unavailable, report that
limitation; do not claim a model switch or create a visible task as a fallback.
