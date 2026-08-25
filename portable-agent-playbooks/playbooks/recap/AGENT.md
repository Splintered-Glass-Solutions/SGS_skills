# Recap Agent Playbook

This is a platform-neutral version of the `recap` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Produce a concise thread recap with current state, decisions, evidence, blockers, and clear next action paths. Use when the user asks to recap a thread, summarize where things stand, prepare a handoff, or decide what can happen next across many active agent threads.

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

# Recap

## Purpose

Use this skill to turn the current thread into a decision-ready status recap.
The goal is to help the user quickly reload context across many simultaneous
threads without re-reading all messages, logs, diffs, or tool output.

This skill is read-only by default. Do not continue implementation, deploy,
send messages, change files, update memory, or create durable artifacts unless
the user explicitly asks for that as part of the command arguments.

## Inputs

The command may be invoked with optional context in `$ARGUMENTS`, such as:

- a project, repo, branch, or environment to focus on
- a specific decision or blocker to explain
- "save" or "handoff" if the user wants a durable artifact
- "brief" if the user wants the shortest useful version

If no arguments are provided, infer scope from the current thread and latest
user request.

## Recovery Pass

Inspect only enough context to produce an accurate recap:

1. Latest user request and the thread's active objective.
2. Any active plan/checklist and recent assistant commitments.
3. Current `cwd`, repo root, branch, and `git status --short --branch` when the
   work happened in a repo.
4. Changed files and recent diffs only when they are relevant to the recap.
5. Recent validation, QA, deploy, tool output, screenshots, URLs, issue IDs,
   PRs, tasks, or artifacts mentioned in the thread.
6. Durable artifacts created or consulted during the thread, such as reports,
   logs, notes, queues, checkpoints, or generated files.
7. Relevant Showme proof packages, screenshots, annotated images, branded
   presentation candidates, and their manifests. Prefer artifacts created for
   the current feature in the current thread; do not search broadly for
   unrelated project images.
8. If a command/session may still be running, inspect it before stating final
   status.

Do not do broad repo archaeology just to make a recap more complete. If a fact
is not visible from the thread or quick local evidence, label it as unknown.

## Recap Shape

Default to this structure:

```md
**Thread Recap**
Objective: <one sentence>
Current State: <done / partially done / blocked / unclear>

What Happened:
- <high-signal completed work or findings>

Evidence:
- <tests, deploys, logs, files, URLs, commands, timestamps, or exact artifacts>

Visual Proof:
- <one to three relevant Showme images rendered with absolute Markdown image paths>
- <short caption stating what each image proves and its proof boundary>

Decisions Made:
- <explicit decisions or assumptions that now guide the work>

Open Decisions:
- <decisions the user still needs to make, if any>

Next Action Paths:
A. <safest immediate next step>
B. <alternate path, usually implementation or deeper verification>
C. <higher-risk or gated path, such as deploy/promotion/customer send>
D. <stop/no-op path when waiting is reasonable>

Recommended Order:
1. <first action>
2. <second action, if needed>
```

Keep the recap concise. Expand only when the thread contains multiple repos,
deployments, production/live evidence, or unresolved decisions.

## Showme Visual Proof

When the thread contains relevant Showme images, display the clearest one to
three artifacts directly in the recap using absolute paths:

```md
![<feature and state>](<absolute-path-to-image.png>)
```

Select images in this order when available:

1. A selected or release-ready branded proof image when the recap is intended
   for product or release communication.
2. An annotated proof screenshot when the recap is intended for engineering or
   QA handoff.
3. The raw screenshot when it is the only readable or relevant evidence.

For each displayed image, add a brief caption identifying the feature surface
and boundary, such as local, preview, Dev, staging, production, or
customer-visible. Do not display generated artwork, stale candidates, or
unrelated screenshots as proof. A branded Showme image may be displayed as
presentation collateral, but it must not upgrade the underlying evidence
boundary. Preserve any manifest status such as candidate, selected template,
release-ready, or blocked.

If no relevant Showme image exists, omit the image block rather than inventing
one or linking to an unrelated artifact. If the thread contains Showme runtime
evidence but no image, summarize that evidence under `Evidence` instead.

## Next Action Paths

Use clear labels:

- `A` should be the lowest-risk useful next step.
- `B` should be the next implementation or investigation path.
- `C` should be any gated live/deploy/external path, clearly marked as needing
  approval when relevant.
- `D` should be the pause/stop/escalate option when the best move is not to keep
  spending time.

If the paths have a natural sequence, say "do all in order" and list the order.
If they are alternatives, say "choose one."

## Decision And Safety Rules

- Separate confirmed facts from inferences.
- Separate local, dev, hosted, and production status.
- Do not claim tests, deploys, sends, or database changes happened unless there
  is visible evidence.
- Do not recommend production deploys, promotions, migrations, broad jobs,
  permission/RLS/grant/ownership changes, destructive data changes, paid
  provider runs, or external sends without marking them gated.
- Do not expose secrets.
- Do not overwrite unrelated dirty work.
- If asked to produce a handoff for another thread or agent, include exact paths
  and command evidence, but keep secrets out.

## Durable Output

Only create a file when the user explicitly asks to save, hand off, or archive
the recap. If saving is requested and no path is specified, choose a small
plain-text markdown artifact under the relevant repo's `tmp/`, `output/`,
`docs/qa/`, or another existing local convention. Report the exact path.

Do not update the agent memory unless the user explicitly asks to update memory.

## Final Response

Return the recap itself. Do not append process notes unless there is a validation
or evidence limitation the user needs to know.
