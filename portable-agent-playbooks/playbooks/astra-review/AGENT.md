# Astra Review Agent Playbook

This is a platform-neutral version of the `astra-review` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Independently review one implemented build item with a fresh Astra 6 low reviewer; return evidence-backed findings without editing.

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

# Astra Review

Dispatch a fresh `gpt-6-astra` / `low` reviewer with `fork_turns="none"` under the
[worker contract](../build-it/references/worker-contract.md). Review is read-only.
Do not reuse the design or implementation agent as the initial independent reviewer.

Pass the accepted behavior/constraints, item base and candidate code state, changed
files, applicable repo rules, exact test evidence and remaining gates. Omit the
implementation conversation and its assurances. The reviewer independently inspects
the diff and necessary surrounding code for correctness, regression risk, acceptance
coverage, compatibility and test quality. It may run safe non-mutating checks;
commands that alter files, fixtures, generated output or shared services go back
to the implementer. No product edits, commits, deployments, live writes or agents.

Return one verdict: `pass`, `changes requested` or `blocked`, with exact reviewed
SHA/scoped diff fingerprint, concrete findings (file/line, failure scenario, severity,
required assertion), evidence inspected and limitations. Style preferences outside
accepted criteria are optional follow-ups, not blockers. Do not invent changes to
justify the review. Missing required local proof means blocked, not pass.

The parent sends actionable findings to the Luna implementer, then asks a lean
same-item reviewer to inspect the new diff and affected evidence. If context has
grown, replace it with a fresh independent Astra/low reviewer under the worker
contract, carrying prior findings and proof instead of the conversation.
Re-review changes and their impacts;
do not restart the full audit without a reason. Use the parent repair limit (at most
three materially different attempts per failure family); known authority/access
failures are not retried. Only a pass on the current state closes local item review.
Astra 6 sign-off is code/local review, never deployed or provider acceptance.
Standalone review returns findings and stops; implementation needs separate authority.
