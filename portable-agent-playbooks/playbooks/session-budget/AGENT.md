# Session Budget Agent Playbook

This is a platform-neutral version of the `session-budget` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when agent work is long, ambiguous, cross-repo, high-cost, repeatedly looping, or needs task-type budget rules; includes checkpoints for debugging, build work, planning, research/transcripts, QA/review, automation, and communication so sessions produce artifacts instead of open-ended token burn.

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

# Session Budget

Use this skill to keep agent work bounded, useful, and reusable. The goal is not a hard token cap; it is a clear objective, right-sized context, early checkpoints, and evidence before continued iteration.

## First Classification

Classify the task before going deep:

- `quick_lookup_message`: answer, draft, send, or inspect one small thing.
- `debugging`: diagnose wrong behavior, errors, broken flows, regressions, or production issues.
- `build_work`: implement code, UI, app behavior, scripts, docs, tests, or dashboards.
- `planning`: produce a spec, implementation plan, architecture recommendation, or decision brief.
- `research_transcript`: fetch, summarize, inspect sources, recover transcripts, or synthesize external context.
- `qa_review`: review code, run QA, validate a feature, or produce findings.
- `automation`: create, update, inspect, or run recurring workflows.
- `communication`: text/email/status update intended for another person or channel.

If the task spans more than one type, name the primary type and the handoff point where the next type begins.

## Budget Rules

- Quick lookup/message: finish in one short pass. If context gathering is needed, say what was inspected and stop after the answer or send.
- Debugging: inspect first, then state a concrete hypothesis before editing. After edits, run a targeted validation or explain why validation is unavailable.
- Build work: after each meaningful implementation pass, run relevant tests, screenshots, browser checks, or syntax checks before continuing.
- Planning: stop at a decision-ready spec unless the user asked for implementation. Surface breaking changes, architecture shifts, pattern deviations, and cross-repo implications.
- Research/transcript: save durable notes, citations, extracted IDs, transcript paths, or summary artifacts when the work could be needed again.
- QA/review: findings first, evidence-backed, with file/line, URL, screenshot, command output, or artifact references where possible.
- Automation: verify schedule, cwd, active/paused status, expected artifacts, and end-of-run accounting. Preserve next-run memory when supported.
- Communication: keep the message recipient-fit and mobile-safe. Use attachments or files for long prompts/assets instead of dumping large text into chat.

## Checkpoints

For long, high-cost, or uncertain work, checkpoint before continuing. Use this shape:

1. Objective
2. What changed or was found
3. Proof gathered
4. Remaining uncertainty
5. Recommended next action

Trigger a checkpoint when any of these happen:

- The session has become exploratory instead of execution-focused.
- A repo or source was inspected for more than one pass without a concrete hypothesis.
- Build/debug work is continuing after a failed validation.
- The task crosses repos, environments, auth systems, billing, data permissions, deployment, or production behavior.
- The user is likely to benefit from deciding whether to continue, reuse, or stop.

## Stop Conditions

Stop or ask for direction when:

- Planning has a decision-ready spec and implementation was not requested.
- A quick task requires broad repo archaeology.
- Debugging has no new evidence after a hypothesis and one validation loop.
- Research cannot access the source and fallback paths have been tried.
- The next step would change permissions, grants, roles, ownership, RLS, production deployment, billing, or irreversible external state without explicit approval.

## Reuse Signals

Recommend making a skill, script, checklist, or automation when:

- The same project/task family appears multiple times.
- The task includes provider-specific setup, auth quirks, validation commands, or recovery steps.
- A workflow would save future source reprocessing or repo rediscovery.
- The work produced a useful durable artifact that future agents should load.

## Final Answer Requirements

For substantial sessions, include:

- What was done
- What was verified
- What artifact changed or was created
- What remains uncertain or blocked
- Whether this pattern should be kept, made reusable, or tightened/stopped
