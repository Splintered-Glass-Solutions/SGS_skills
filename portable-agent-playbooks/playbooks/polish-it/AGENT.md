# Polish It Agent Playbook

This is a platform-neutral version of the `polish-it` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Polish an existing app or website by removing developer-facing clutter, excessive warnings and redundant copy while preserving essential user guidance, trust and accessible feedback. Use when asked to polish, declutter or make a user experience feel production-ready.

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

# Polish It

Make the requested experience feel clear, intentional and professional to its real audience. Remove the signs of a development process that have leaked into the product. Follow the user's scope and existing design language; do not turn a polish pass into a redesign, feature expansion or release authorization.

## Inspect the experience

Identify the audience, their primary task, the target surface and what is actually in scope. Inspect the rendered experience where available, including a representative mobile viewport and relevant normal, empty, loading, success, error and restricted states. Compare with the current source and existing design system; distinguish a real product message from a development artifact. If runtime access is unavailable, make a source-based assessment and report that visual behavior remains unverified.

Look for permanent test-mode or fixture labels, internal environment and implementation details, diagnostic instructions, speculative warnings, repeated disclaimers, excessive helper text, redundant headings, placeholder copy, unnecessary status badges, and explanations of how a feature was built. Consider visual weight, spacing and hierarchy as well as words. Search related states and shared components so the same clutter is not left elsewhere within scope.

## Decide what earns its place

For each candidate ask: what decision, action, expectation, meaningful status or recovery does this help the intended user with, and at what moment? Remove content that has no concrete user purpose. Consolidate repeated messages, use direct labels and concise natural language, and place useful information near the relevant action. Prefer a focused contextual message over a persistent banner when appropriate. Use progressive disclosure only for genuinely optional detail, not to hide information needed to proceed.

Keep clear, timely information about actual transaction outcomes, errors and recovery, data limitations that could change a decision, costs and charges, privacy or permission consequences, destructive actions, and applicable required disclosures. Preserve accessible labels, screen-reader announcements, keyboard use, and necessary instructions. Tailor salience to severity; do not suppress real failures or misrepresent an unavailable, synthetic or incomplete result as real. Verify whether an environment indicator helps prevent a consequential mistake before removing it: for example, a sandbox indicator may matter when a payment or message can be mistaken for real. When the need or applicable requirement is uncertain, preserve it and report the uncertainty rather than guessing.

Move developer-only diagnostic detail to an existing appropriate developer surface, logs, documentation or test tooling when it is needed there and the user has authorized the change. Avoid adding a new debug panel or configuration system simply to move copy. Do not change underlying behavior, remove protections or disable tests to make an interface look clean.

## Make and verify the pass

When the user asks to make changes, apply the smallest coherent in-scope edits across the relevant states, then verify the actual changed experience and its primary task. Check desktop and mobile as appropriate, including keyboard and accessible error/status semantics when affected; exercise changed success and failure states when safely possible. Reuse existing fixtures and valid proof. Run focused checks appropriate to the change; do not create a database or perform external mutations merely for verification. Stop when the requested polish and relevant checks pass.

If the user asks only for an audit or plan, provide prioritized findings and proposed changes without editing the product. Report what changed or is proposed, the evidence and checks, and any material unverified states. Do not claim a deployed or live result from local proof. Research foundations and examples are in [references/research.md](references/research.md); consult them when the rationale or a difficult tradeoff is needed.
