# Orchestratror Mode Agent Playbook

This is a platform-neutral version of the `orchestratror-mode` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when the current model running the active agent thread should act as the orchestrator for broad or high-cost work: keep decomposition, tradeoffs, validation strategy, synthesis, and final review on the main model while delegating independent research, coding, and testing slices to cheaper subagents or parallel tool waves with bounded scope and explicit evidence requirements.

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

# Orchestratror Mode

Use the current model running the active agent thread as the orchestrator. Keep
the judgment-heavy work on this main model. Push repeatable, bounded, or
parallelizable work to cheaper the agent subagents or parallel tool waves only when
the slices are independent and the expected evidence is clear.

The efficiency target is not always fewer total tokens. The target is lower
premium-model usage, lower main-thread context load, and faster wall-clock
progress by moving bounded execution to cheaper capable agents.

For long, broad, or multi-agent work, pair this skill with `$agent-safe-run`.
Keep the agent runtime stable and minimize token usage: compact status updates,
short output caps, file-backed logs for verbose commands, targeted reads instead
of full dumps, and no watchers or repeated streaming output inside the chat.

## Workflow

1. State the objective, task class, and immediate success bar before widening
   the work.
2. Separate orchestrator decisions from delegable execution.
3. Keep architecture, prioritization, ambiguity resolution, tradeoffs,
   validation strategy, and final review with the current main-thread model.
4. Delegate only independent slices: repo scans, file inventory, docs
   extraction, focused testing, log reduction, narrow edits, or alternative
   debugging theories.
5. Require compact returns: findings, changed files, commands run, concrete
   evidence, residual risk, and what still requires orchestrator judgment.
6. Reopen important files, inspect risky diffs, and rerun or spot-check the
   verification that matters before claiming completion.
7. Use `$agent-safe-run` when the task may create many tool calls, long logs,
   browser/computer-use sessions, multiple subagents, or background processes.

## Token And Desktop Safety

- Keep the main thread lean: summarize exploration, avoid pasting full logs, and
  load only the next relevant file sections.
- Prefer `rg`, targeted `sed`, structured summaries, and bounded command output
  over broad `cat`, full process dumps, and long unfiltered test output.
- Redirect noisy builds, broad tests, CI logs, and monitors to files, then read
  compact tails or parsed summaries.
- Avoid live watchers in the agent runtime. Use one-shot polling or file-backed
  monitoring when progress must be checked.
- Stop adding agents when coordination cost or context overhead exceeds the
  expected savings.
- If the agent runtime gets slow, hot, swap-heavy, or helper processes accumulate,
  switch to `$agent-safe-run` triage before continuing orchestration.

## the agent-Native Delegation

- Use parallel tool calls for independent reads and inspections.
- When spawning subagents, prefer a cheaper capable model for bounded worker or
  explorer tasks unless the user asks for a specific model or the task requires
  the main model's judgment.
- Keep each delegated prompt short and self-contained. Do not include full
  conversation history unless it is necessary for the slice.
- Use subagents only when the task is broad enough to justify the coordination
  cost and the delegated slice can stand on its own.
- Do not send multiple agents to edit the same files at the same time.
- Do not delegate the immediate blocker if the next decision depends on direct
  inspection.
- Prefer one bounded wave at a time, then integrate before launching another.

## Handoff Packet

Write delegated prompts as self-contained packets. Assume the receiving agent
has not seen the conversation.

Include:

- repo path
- exact objective
- in-scope files or search targets
- out-of-scope areas
- expected return format
- verification commands
- stop conditions

Useful stop conditions:

- The live code does not match the assumption in the handoff.
- The work requires files outside the assigned scope.
- A verification command fails twice after a reasonable retry.
- The evidence is too weak to support a confident claim.

## Evidence Standard

Treat delegated output as evidence, not as a verdict to forward untouched.

- Reopen cited files when the claim affects behavior, security, migrations, or
  user-facing output.
- Prefer raw artifacts over summaries: diffs, commands, logs, screenshots, and
  exact failures.
- Resolve disagreement centrally if delegated slices conflict.

## When To Use It

Use this for:

- broad repo exploration
- multi-file implementation with separable workstreams
- test or browser validation that can run in parallel
- research or review passes where signal gathering is expensive
- debugging with multiple plausible theories

Skip it for:

- tiny fixes
- tightly coupled edits in the same fragile files
- debugging where one immediate blocker must be inspected directly first

## Default Framing

"I will use the current model in this agent thread as the orchestrator and
reviewer, use `$agent-safe-run` guardrails for long or noisy work, and use
cheaper capable subagents or bounded parallel tool work for independent
research, coding, or testing slices so the main context stays focused on
judgment, synthesis, and final quality while minimizing token waste."
