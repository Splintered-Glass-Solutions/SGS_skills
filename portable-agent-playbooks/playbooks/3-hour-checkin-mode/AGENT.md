# 3 Hour Checkin Mode Agent Playbook

This is a platform-neutral version of the `3-hour-checkin-mode` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Run sustained work in focused three-hour blocks with autonomous progress, same-chat phone-readable snapshots, and decision-ready blocker paths. Use when the user requests this check-in mode.

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

# 3-hour check-in mode

Carry the user's existing objective forward through focused three-hour blocks. Use `$autonomous` within the user's actual constraints and approval history. The user's same-chat requirement takes precedence over that skill's automatic fresh-chat handoff; checkpoint in this chat instead. At startup, record the objective, granted and withheld authority, block start and next check-in in local time with timezone, checkpoint/report paths, and the next meaningful milestone. Reconcile any existing in-flight work before starting another writer. Keep the existing report card current when one exists; preserve its scope and history.

Work in coherent, bounded slices through implementation, appropriate checks, independent review where required, and the authorized release path. Coordinate any authorized parallel work and shared writers. Avoid repeatedly retrying one blocker or polishing a marginal detail while important independent work can proceed. Keep user-visible progress brief and checkpoint actual work, evidence, uncertainty, in-flight operations, and the first incomplete action. Separate local, hosted Dev, Production, provider and customer-visible proof.

When stumped, looping, or a blocker is holding up progress, pause attempts in that lane and use a fresh `gpt-6.1-sol` / `medium` subagent (`fork_turns="none"`) for a read-only `$fresh-perspective` review. Give it the original goal, decisions, constraints, exact evidence, attempts, and a bounded question; ask it to distinguish real gates from assumptions, recommend a discriminating next step and identify work that can proceed independently. This mode's specified model overrides the default model in `$fresh-perspective`. Apply the guidance critically, record the outcome, then proceed or move to an independent item. Do not spawn repeated reviews of the same unchanged blocker. If the required model or delegation is unavailable, record that the review did not occur and continue independent authorized work; do not silently substitute a model or bypass a genuine gate.

Near each three-hour mark, reach a safe boundary without interrupting writes or deployments and post a self-contained snapshot in this chat; if an operation cannot safely pause, report its actual state when possible and finish or reconcile it before any retry. Include a compact in-conversation visualization using `$visualize:visualize` when supported, plus accessible, phone-readable text for every current blocker: impact, evidence, actionable paths, recommendation, and any genuinely needed decision or approval. Group related blockers but retain their identifiers so none disappears. Identify choices already made; do not ask again. Highlight progress since the last snapshot, the next block's priority, test/deployment truth, and material uncertainty. Distinguish partial evidence from acceptance and overlapping entries from unique issues. A visualization is a snapshot, not a live report; if unavailable, provide the same essential status in text. Update the durable report and checkpoint before posting.

For a requested recurring schedule, use the available automation tool and `$automation-thread-scheduler`, preferring a same-thread heartbeat. Explicitly retain the user's requested check-in notifications and cadence, the task's constraints, checkpoint path, and same-chat destination in the automation prompt. Reuse an existing matching automation; verify its active status and target. Record the last snapshot and next due time in the checkpoint. If a scheduled wake coincides with a snapshot already delivered for that interval, reconcile in-flight work and avoid posting a duplicate; preserve the next regular check-in. A heartbeat provides scheduled wakeups, not uninterrupted execution: disclose that sleep, host shutdown, tool failures or session limits can prevent work or delivery, and never claim a watchdog or guaranteed continuous operation. Continue active work between check-ins while the runtime permits; do not sleep through available work just to wait for the next report. Stop or pause the schedule when the user requests it or the task is complete, according to the scheduler's capabilities.

The visualization contract places its reference in the final response, which ends the active turn. Before finalizing, check whether a supported, authorized immediate continuation in the same chat actually exists and arrange it only if supported. Do not treat the next three-hour heartbeat as immediate continuation or promise background work. If no immediate continuation is available, preserve the next action and plainly disclose that work will resume at the next successful scheduled wake or user message; still deliver the requested snapshot. Do not bypass the visualization contract by placing its reference in commentary, or create extra chats or unsupported schedules as a workaround.

Use only authority the user actually granted for this task; this mode grants no additional permission by itself. Honor explicit non-production merge authorization without repeating routine approval requests, while applying higher-priority constraints and the user's other explicit limits. Such authorization alone does not grant Production changes, database writes, migrations, destructive work, external messages, paid actions, or other unrelated authority. Respect tool-enforced confirmations. If the user reserves a final Production merge, prepare a concrete reviewable result and ask at that boundary. Other genuinely required permissions or missing facts remain gates; explain their source, prepare the decision where possible, and continue independent work.

If a block must end before completion, leave a checkpoint with exact current state and resume path; do not represent an ended chat or scheduled heartbeat as an agent that continues running in the background. Honor explicit handoff and thread-continuity instructions, and never create a new user-owned chat unless authorized or required by an explicitly invoked handoff workflow.
