# Plugin Agent Playbook

This is a platform-neutral version of the `plugin` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Help the user plug back into an ongoing thread with a concise plain-language recap, relevant UI screenshots, and one batch of validated A/B/C decisions that unlock the next autonomous work. Use when he returns to review progress, clear blockers, give direction, or provide permissions. Not for installing software plugins.

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

# Plugin

Help the user quickly reconnect with work after time away. Combine the orientation of Recap, the useful choices of Interview Spec, and lightweight runtime screenshots inspired by Showme. Deliver one compact review packet so he can answer, correct direction, and send the work forward with clear boundaries.

## Recover before asking

Inspect the latest objective, prior decisions and permissions, current checkpoint, relevant files, and existing proof. Recheck cheap facts that may have changed, including Git state, running sessions, and blockers. Keep this pass scoped to the current thread; do not restart the project or repeat completed checks.

Identify what is finished, what remains, and what actually requires the user's input. Separate verified facts from guesses and stale evidence. Explain local checks, deployed behavior, and customer acceptance separately. Do not make him restate recoverable context or choose routine implementation details.

This invocation prepares a review and decisions; it does not itself authorize product edits, deployment, shared-data changes, or external messages. Safe inspection and local screenshot artifacts are included. Preserve existing approvals and unrelated work.

## Show the work when visuals matter

If UI is being built or changed, show one or two readable screenshots of the relevant surfaces or interaction states. Prefer existing current runtime captures whose source and environment can be verified. If missing or stale, capture the exact current UI using available browser tools; use the authenticated-browser-testing skill for authenticated live views. Use Showme guidance when runtime provenance or evidence packaging needs more detail, without turning this into a full QA or presentation project.

Inspect each image before showing it. Render it inline using an absolute Markdown image path and label it **Visual 1** or **Visual 2**. Add a short caption with the surface, environment, and what needs feedback. Preserve raw pixels and avoid sensitive information. Label old captures as old; mockups cannot prove implemented behavior. If access or runtime is unavailable, state the limitation and include the precise missing input in the decision batch. Do not make product changes merely to obtain a screenshot.

Tie any visual-direction question to a numbered image and a specific visible element. Invite optional comments such as `Visual 1: make the dates easier to scan`.

## Batch the decisions

Prepare all currently knowable questions needed for the next bounded batch in one packet, including direction, blockers, acceptance, and missing permissions. Usually three to five questions are enough; use fewer when possible, and more only for distinct decisions that genuinely unlock this batch. Do not serially reveal questions you could have identified upfront.

For each numbered question:

- Give one short sentence of context: why the decision matters to the goal.
- Offer **A / B / C** with concrete effects. Mark the best supported choice **recommended**, even when it is B or C. Keep options distinct, plain, and brief; accept a custom answer.
- Validate proposed options against current code, available tools, existing decisions, and permissions. Do not invent capabilities or present unavailable paths as ready. If feasibility is uncertain, make the option a bounded investigation and say what it would establish.
- Explain material scope, time, cost, data, or release consequences only where they affect the choice. Do not fabricate estimates.
- For a permission question, specify the exact action, target, environment/account, and payload or revision when relevant. An opinion on design or an acknowledgment of the recap is not permission for a different operation.

Use the async question tool when available and suitable, placing the context and options in each self-contained question. Present the batch together; avoid duplicating the full questions in prose. Otherwise use the compact format below. Do not interpret silence or a preselected option as an answer.

## Keep the packet short

Aim for a two-minute read: roughly 250–450 words excluding images, fewer for simple threads. Use short sections and bullets, not a long narrative. Explain like someone has forgotten the conversation: plain and concrete, never babyish. Include only context needed to judge the next work.

```markdown
**Goal:** What we are trying to achieve and why, in one or two sentences.

**Where we are**
- What changed and how we got here.
- What is checked, with one useful proof link.
- What remains or is blocked, and why.

**Review**
[One or two inline screenshots and short captions, only when relevant.]

**Decisions for the next batch**
1. [One sentence of context and the question.]
   A — [Choice and effect; recommended if appropriate.]
   B — [Choice and effect.]
   C — [Choice and effect.]

**After your answers:** [The bounded next batch, its completion check, and any operation still gated.]

**Reply:** `1A 2C`, plus any image comments or corrections to the goal.
```

Omit empty sections. If no input is needed, say so and give the already authorized next step instead of manufacturing choices. Do not force every question into three options when only two honest alternatives exist; use a real defer/investigate option where useful.

## Turn answers into continuation

When the user responds, map every answer and visual comment to its decision. Briefly confirm the selected direction, scope, success checks, and exact permissions; record them in the existing task checkpoint when one is used. Do not create a new artifact just to repeat the packet or update memory without a request.

Continue the selected next batch autonomously within those boundaries when the response authorizes it. Ask a follow-up only for a consequential ambiguity or a genuinely new fact. Reuse existing approvals; request an action-time confirmation only when a tool or applicable instruction requires it. Do not promise that one review can preapprove unknown future operations.
