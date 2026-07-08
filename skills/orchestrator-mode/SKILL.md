---
name: orchestrator-mode
description: >-
  Use when the current Codex thread should act as the orchestrator for broad,
  high-cost, or multi-agent work: create or track a goal, keep decomposition,
  architecture, tradeoffs, validation strategy, synthesis, and final review on
  the main model, make an explicit delegation decision, and for broad or
  high-cost work normally launch bounded Codex subagents for independent
  research, coding, testing, log-reduction, or coverage slices. Pair with
  codex-safe-run guardrails to minimize token usage and Desktop runaway risk.
---

# Orchestrator Mode

Use the current model running the active Codex thread as the orchestrator. Keep
judgment-heavy work on the main model. Push repeatable, bounded, or
parallelizable work to cheaper Codex subagents whenever the slices are
independent and the expected evidence is clear. Parallel tool waves are useful
for quick file reads, but they are not a replacement for subagents on broad or
high-cost work.

When this skill is invoked for broad, high-cost, multi-file, multi-repo,
research-heavy, QA-heavy, or ambiguous work, the default is to launch at least
one bounded subagent wave before synthesizing the final answer. Skip subagents
only when there is a concrete reason, and state that reason explicitly.

The target is lower premium-model usage, lower main-thread context load, and
faster wall-clock progress. It is not always fewer total tokens.

For long, broad, or multi-agent work, pair this skill with `$codex-safe-run`.
Keep Codex Desktop stable and minimize token usage: compact status updates,
short output caps, file-backed logs for verbose commands, targeted reads instead
of full dumps, and no watchers or repeated streaming output inside chat.

## Start

1. State the objective, task class, and success bar before widening the work.
2. Create a concrete goal when the host supports goal tracking and the work is
   substantial enough to justify it.
3. Inspect the repo or source material before committing to an implementation
   plan.
4. Separate orchestrator decisions from delegable execution.
5. Make an explicit delegation decision:
   - "Subagents required" for broad/high-cost work with independent slices.
   - "Subagents skipped" only for a short, concrete exception such as missing
     subagent tooling, a tiny task, a privacy/safety boundary, or a single
     serial blocker that must be inspected directly.
6. If subagents are required, identify and launch one bounded wave before doing
   the whole task in the main thread.

## Orchestrator Responsibilities

- Keep architecture, prioritization, ambiguity resolution, tradeoffs,
  validation strategy, integration, synthesis, and final review in the main
  thread.
- Delegate independent slices such as repo scans, file inventory, docs
  extraction, focused testing, log reduction, narrow edits, coverage audits, or
  alternative debugging theories. For broad/high-cost work, this is mandatory
  when subagent tooling is available and at least one slice can stand alone.
- Prevent parallel agents from editing the same files at the same time.
- Treat delegated output as evidence, not as a verdict to forward untouched.
- Reopen important files, inspect risky diffs, and rerun or spot-check the
  verification that matters before claiming completion.
- Update the goal as complete only when no required work remains.

## Codex-Native Delegation

- Prefer subagents over main-thread-only exploration for broad work. Use
  parallel tool calls for small independent reads and inspections, not as the
  sole delegation mechanism when subagents can provide a real bounded pass.
- When spawning subagents, prefer a cheaper capable model for bounded worker or
  explorer tasks unless the user asks for a specific model or the task requires
  main-model judgment.
- Keep each delegated prompt short and self-contained. Do not include full
  conversation history unless it is necessary for the slice.
- Use subagents for broad or high-cost tasks whenever the delegated slice can
  stand on its own. Do not default to doing the whole task in the main thread
  merely because it is possible.
- Do not delegate the immediate blocker if the next decision depends on direct
  inspection.
- Prefer one bounded wave at a time, then integrate before launching another.
- In the final response for substantial work, say whether subagents were used.
  If they were skipped, name the exception.

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

Require compact returns with changed files, commands run, concrete evidence,
failures, residual risk, and anything that still requires orchestrator judgment.

## Token And Desktop Safety

- Keep the main thread lean: summarize exploration, avoid pasting full logs, and
  load only the next relevant file sections.
- Prefer `rg`, targeted `sed`, structured summaries, and bounded command output
  over broad `cat`, full process dumps, and long unfiltered test output.
- Redirect noisy builds, broad tests, CI logs, and monitors to files, then read
  compact tails or parsed summaries.
- Avoid live watchers in Codex Desktop. Use one-shot polling or file-backed
  monitoring when progress must be checked.
- Stop adding agents when coordination cost or context overhead exceeds the
  expected savings.
- If Codex Desktop gets slow, hot, swap-heavy, or helper processes accumulate,
  switch to `$codex-safe-run` triage before continuing orchestration.

## Completion Standard

Before the final response:

1. Inspect the final diff or final artifact.
2. Run relevant tests, checks, screenshots, or browser verification for the
   feature's risk level.
3. Reconcile delegated evidence centrally.
4. Report what changed, proof gathered, remaining risks, and recommended next
   action.

## Default Framing

"I will use `$orchestrator-mode` to keep this Codex thread as the orchestrator
and reviewer, pair it with `$codex-safe-run` guardrails for long or noisy work,
and launch bounded cheaper capable subagents for independent research, coding,
testing, coverage, or log-reduction slices when the task is broad enough. I
will skip subagents only for a concrete exception and state that exception."
