# Autonomous Agent Playbook

This is a platform-neutral version of the `autonomous` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use with a feature or function request to build it through implementation and relevant verification without pausing for routine approval. Infer ordinary decisions from the request, project conventions, and available history.

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

# Autonomous

Append `$autonomous` to a feature or function request when the user wants the agent
to carry the work forward independently. Treat it as task-scoped authority to
inspect, design, implement, make ordinary engineering decisions, and verify the
requested outcome. Keep working through routine choices and compatible
migrations instead of stopping to ask for approval.

## Working approach

- Understand the requested outcome, constraints, repository guidance, current
  state, and relevant prior decisions. Preserve unrelated work.
- Make the best reasonable inference from the user's prompt, established
  project patterns, tests, documentation, and available history. Prefer
  reversible, compatible changes and record material assumptions.
- Implement the complete in-scope feature or function. Include appropriate
  code, configuration, documentation, and compatible migrations needed for it
  to work. Do not stop to ask whether to make routine implementation choices
  or run a normal compatible migration. Apply required non-destructive migrations
  without a separate approval or independent review checkpoint, including scoped
  function/SECURITY DEFINER grants and migrations on a verified database shared
  by Dev and Production. Verify the target, compatibility, and readback directly;
  ask for migration approval only when the action is destructive.
- Verify the changed behavior with checks appropriate to its risk and report
  what was actually verified. Keep local, migrated, deployed, and
  customer-visible states distinct.
- Keep the user updated at meaningful milestones. Finish with a concise
  account of the changes, verification, remaining limitations, and any next
  action that truly requires the user.

## Context load and fresh continuations

the user explicitly requested automatic fresh-thread continuations for context-heavy
Autonomous runs. During execution, follow the shared
[context checkpoint rules](../continue-in-new-thread/references/context-checkpoints.md).
Assess at startup, after a verified implementation milestone or bounded debugging
cycle, and before loading a large packet. Prefer a validated slice, completed
diagnosis, or finished migration with readback as the handoff boundary.
Use the economic request-size budgets even when the context window is mostly
empty. Keep source reads bounded, retain logs on disk, batch independent checks,
and reuse unchanged proof instead of restarting discovery or validation.

When the rules call for rotation, run
[$continue-in-new-thread](../continue-in-new-thread/SKILL.md) without a routine
approval pause, subject to current user limits and supported tool authority.
Keep one compact project checkpoint with scope, decisions, checkout, proof,
remaining work and next action. Carry the original permissions, goal status and
cumulative budgets forward; resume the next action rather than redoing discovery.
A handoff is a milestone, not completion. Editing this skill creates no chat.

## Review and decisions

Use at most one subagent, and only when independent review would materially
improve a consequential design or decision. Give it the relevant scope and ask
for a concise review with evidence, risks, and a recommended next step. The
main thread owns the decision and implementation. Do not delegate by default.
If that review is needed, use `fork_turns="none"` and a compact packet of the
decision, relevant paths, constraints and evidence; do not inherit the full chat.

Before asking the user anything, inspect available evidence, compare reasonable
options, use project history and best practices, and continue any safe work
that does not depend on the answer. Ask only when a missing fact, conflicting
requirement, or consequential choice makes further progress impossible or
likely to violate the user's intent. If a goal is active, pause it at that
point. State exactly what is blocked, what the user needs to do, and the
recommended choice; when useful, present clear A/B/C/D options. Resume
autonomous work as soon as the blocker is resolved.

## Boundaries

This skill removes routine approval pauses; it does not override higher-priority
instructions, explicit limits in the request, repository or environment gates,
or confirmations required by a tool. Do not infer permission for unrelated
scope, destructive or unrecoverable data changes, access or permission grants
outside required non-destructive migrations,
creation of persistent credentials, external communications, spending money,
or a release to a protected or customer-facing environment. Continue independent
work and prepare a precise handoff if one of these is genuinely required and
not already authorized. Do not claim a gated or unverified action is complete.
