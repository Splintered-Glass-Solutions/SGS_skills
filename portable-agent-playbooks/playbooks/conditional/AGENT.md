# Conditional Agent Playbook

This is a platform-neutral version of the `conditional` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Evaluate the immediately preceding Codex result and conditionally execute any explicitly requested next action or ordered action chain only when that result clearly succeeded; otherwise return a compact blocker-and-decision recap. Use for gated commands, skills, reviews, deployments, communications, or closeout workflows.

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

# Conditional Gate

## Overview

Use this skill as a general gate between a completed step and any explicitly
requested next action. Inspect the latest concrete result in the current task,
classify it as success or not-success, then either execute the requested action
or ordered action chain or return a short decision-ready recap. It can gate
any next action, regardless of domain. Treat ambiguity as not-success.

## Contract

Parse the text after `$conditional` as the success branch. Resolve any named
skills and explicit actions using the current task context. The branch may be a
single action or an ordered chain, and may apply to any domain. Common examples:

- `$conditional inspect the logs` means: if the immediately preceding step
  passed, inspect the requested logs.
- `$conditional test dev` means: if the immediately preceding step passed,
  invoke `$test dev`.
- `$conditional draft release notes and close thread` means: if it passed,
  draft the release notes, then close the current thread. Keep `close-thread`
  last because its contract requires its rename and final reply to be the last
  action.
- Preserve explicit arguments such as `dev`, `production`, `draft`, or a named
  destination. Do not invent additional actions or broaden the environment.

## Decision Gate

1. Read the immediately preceding assistant result, tool evidence, and any
   stated headline. Do not infer success merely because a command ran.
2. Classify the prior step as success only when its required outcome is clear:
   `PASS`, `PASSED`, `SUCCESS`, `COMPLETE`, `DEPLOYED — COMPLETE`, or an
   equivalent evidence-backed result with no unresolved required blocker.
3. Classify `FAIL`, `FAILED`, `INCOMPLETE`, `BLOCKED`, `NOT TESTABLE YET`,
   ambiguous output, missing evidence, or a partial chain as not-success.
4. If the prior step is not-success, do not execute the requested actions.
   Return the fallback recap below.

## Success Branch

When the gate passes:

- Execute the requested action or each requested action sequentially, using the
  named skill when one exists. Route the action according to its domain and
  current task context; do not restrict routing to deployment, testing, QA, or
  release workflows.
- Apply each invoked skill's own safety and delivery rules. The conditional
  gate does not authorize unrelated deploys, production changes, data writes,
  external sends, or commits.
- If an action fails or becomes blocked, stop the remaining chain and report
  which action failed, what succeeded before it, and the next safe choice.
- If `close-thread` is requested with other actions, run it last.

## Fallback Branch

When the gate does not pass, return a compact recap rather than repeating the
full thread:

- **Status:** prior step and its exact result.
- **Blockers:** only the core unresolved blockers, with evidence.
- **Decisions:** the choices already made that still hold.
- **Next actions:** provide a small set of labeled options, normally:
  - **A:** lowest-risk step that resolves the blocker;
  - **B:** alternate investigation or local path;
  - **C:** gated live, deploy, provider, or external path;
  - **D:** pause/no-op.
- Recommend an order when the options are sequential.

Do not execute any success-branch action, close the thread, send external
communications, deploy, edit files, update memory, or create durable artifacts
in the fallback branch.

## Output Rules

- Lead with `CONDITIONAL PASS` or `CONDITIONAL HOLD`.
- State exactly which prior result controlled the branch.
- Keep the fallback concise and decision-sized.
- Separate local, hosted Dev, staging, and production proof.
- Never call an incomplete test successful just because deployment succeeded.
- Never claim a requested action ran unless it actually completed.

## Examples

```text
Initial prompt: deploy to dev
Next prompt:    $conditional test dev
```

If deployment is `DEPLOYED — COMPLETE`, run `$test dev`. If deployment is
blocked or ambiguous, return the fallback recap and do not test the hosted
environment.

```text
Next prompt: $conditional draft release notes and close thread
```

If the immediately preceding test is `PASS — FEATURE-SCOPED`, run the release
update workflow and then `$close-thread`. If it is `INCOMPLETE — FEATURE-SCOPED`,
return the blocker recap and leave the thread open.
