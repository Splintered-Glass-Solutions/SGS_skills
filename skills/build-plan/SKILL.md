---
name: build-plan
description: Plan one build item with a bounded subagent; route simple designs to Luna high and complex designs to Sol 6.1 low.
---

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
