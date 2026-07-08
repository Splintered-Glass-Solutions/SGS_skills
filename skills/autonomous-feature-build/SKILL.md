---
name: autonomous-feature-build
description: >-
  Use when the user wants a full feature built end to end with Codex acting as
  the orchestrator: create or track a goal, inspect the repo, plan
  implementation, delegate bounded research, coding, testing, and log-reduction
  slices to cheaper capable subagents, use codex-safe-run and low-token
  guardrails, implement the changes, verify the result, and report proof plus
  remaining risks.
---

# Autonomous Feature Build

Use Codex as the orchestrator to build the requested feature end to end. Keep
product interpretation, architecture, decomposition, integration, validation
strategy, synthesis, and final review in the main thread. Delegate bounded
research, coding, testing, and log-reduction slices to cheaper capable subagents
or parallel tool waves when the work is independent and the expected evidence is
clear.

Pair this with `$orchestrator-mode` for broad decomposition and with
`$codex-safe-run` for long, noisy, browser-heavy, or multi-agent work. Keep the
main thread lean: targeted searches, compact reads, bounded output, file-backed
logs for verbose commands, and no repeated streaming watchers in chat.

## Start

1. Create a concrete goal for the feature when the host supports goal tracking.
2. Classify the task and state the success bar.
3. Inspect the repo before planning implementation details.
4. Identify the smallest set of independent workstreams.
5. Decide what must stay in the main thread and what can be delegated.
6. Launch at most one bounded delegation wave before integrating results.

## Main-Thread Responsibilities

- Own the product interpretation and technical design.
- Decide architecture, tradeoffs, validation strategy, and integration order.
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
- Switch to `$codex-safe-run` triage if Codex Desktop becomes slow, hot,
  swap-heavy, or helper processes accumulate.

## Completion Standard

Before the final response:

1. Inspect the final diff or final artifact.
2. Run relevant tests, checks, screenshots, or browser verification for the
   feature's risk level.
3. Reconcile delegated evidence centrally.
4. Update the goal as complete only when no required work remains.
5. Report what changed, proof gathered, remaining risks, and recommended next
   action.

## Default Framing

"I will use `$autonomous-feature-build` to build this feature end to end. I will
create a concrete goal, use `$orchestrator-mode` to keep this Codex thread as
the architect and reviewer, pair long or noisy work with `$codex-safe-run`, and
delegate bounded research, coding, testing, and log-reduction slices to cheaper
capable subagents while keeping integration, validation strategy, and final
review in the main thread."
