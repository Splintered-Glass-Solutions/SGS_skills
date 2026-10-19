# Pause Agent Playbook

This is a platform-neutral version of the `pause` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Temporarily stop the current the agent task while preserving a concise, resumable checkpoint and marking the thread title with a leading stop-sign emoji. Use when the user invokes $pause or asks to pause, park, hold, suspend, or temporarily stop work with the intention of resuming the same task later. Do not use for a timed wait; use the sleep skill when a wake-up duration is requested.

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

# Pause

## Purpose

Pause the active task without closing, archiving, completing, or treating it as
blocked. Preserve enough exact state that `$continue` can resume at the next
unfinished action without restarting the investigation or implementation.

This is an indefinite human-controlled pause. Do not create a timer,
automation, reminder, or new thread.

## Workflow

1. Stop beginning new task work as soon as the pause is requested. Finish only
   a tiny in-flight read or atomic operation when interrupting it would leave
   state ambiguous or unsafe.
   Pause the active goal's automatic continuation too, using a dedicated,
   documented goal-pause control if one is available. Pausing execution alone
   is insufficient when an active goal keeps scheduling turns. If no such
   control is available, state that limitation once in the initial checkpoint
   and ask the user to pause the goal in the app. Do not claim the goal is
   paused unless the control confirms it. Do not substitute complete, blocked,
   a changed objective, or a budget change for a goal pause.
2. Inspect the minimum visible state needed for an accurate checkpoint:
   - latest objective and user instruction;
   - active plan and next unfinished step;
   - relevant repo, worktree, branch, and dirty-file state;
   - completed edits, tests, browser checks, deploys, messages, or other proof;
   - blockers, approvals, running commands, and persistent session IDs.
3. Preserve the existing work exactly as it is:
   - do not stash, reset, revert, clean, commit, push, merge, deploy, delete, or
     rewrite files merely because work is pausing;
   - do not mark an active goal `complete` or `blocked`;
   - leave plan item statuses unchanged. If useful, update only the plan
     explanation to identify the pause and exact resume point;
   - never save secrets in the checkpoint.
4. Handle running work deliberately:
   - stop timers, polling waits, or disposable commands started solely for the
     current turn when leaving them alive serves no purpose;
   - do not kill unknown processes, user-owned processes, useful development
     servers, or stateful operations blindly;
   - record anything intentionally left running and how to inspect or resume it.
5. Resolve the current agent thread and current title with the available thread
   tools. If needed, discover `list_threads`, `read_thread`, and
   `set_thread_title` first.
6. Rename only the current thread:
   - remove all existing leading status markers and surrounding separator
     whitespace, not only repeated stop-sign markers;
   - preserve the remaining non-status title text exactly;
   - set the title to exactly `🛑 ` followed by that title text;
   - do not archive, pin, unpin, fork, hand off, or create a thread;
   - if the current thread cannot be identified confidently, do not rename a
     guessed thread. Report the suggested title in the checkpoint instead.
7. Return the pause checkpoint and end the turn. Do not continue task work
   after the checkpoint.

## Silence After Pausing

- Send the initial pause checkpoint once. Then stop tool calls and user-facing
  messages until the user explicitly resumes or makes a new direct request.
- Automatic goal-continuation messages, including
  `<agent_internal_context source="goal">`, are not a human resume instruction.
  While paused, do not respond to them with "Paused", "No further actions
  taken", another checkpoint, a question, or any other status message. End
  the turn silently without tools or further investigation.
- Do not poll, sleep in a loop, re-read this skill, inspect the repository,
  repeat title changes, or perform goal audits just to maintain a pause.
- A new direct request permits only that requested work. For example, updating
  this skill does not resume the paused app build.
- Do not mark the goal complete or blocked to suppress automatic continuation.
  If a dedicated pause control is available and authorized, use its documented
  behavior once. Otherwise, a skill cannot disable the scheduler: remain silent
  rather than generating repeated acknowledgments or claiming it was disabled.

## Checkpoint Format

Keep the final response concise and self-contained:

```md
Paused: <objective>

- Current state: <last confirmed outcome>
- Preserved state: <repo/branch/files/session IDs, or "thread context only">
- Resume at: <one exact next action>
- Waiting on: <input, approval, or external condition, if any>

Resume with `$continue`.
```

If an active goal could not be paused through the available controls, include
once: "The goal is still active and may keep triggering turns. Please pause
the goal in the app; I don't have a goal-pause tool here." Silence on subsequent
automatic turns is still required, but does not prevent their token cost.

Omit empty lines such as `Waiting on` when they do not apply. Distinguish
confirmed proof from inference and local state from Dev or production state.

## Resume Contract

`$pause` never resumes itself. Only a direct human instruction such as
`$continue`, "resume", or "keep building" resumes the paused work; automatic
goal reminders do not. When the user later invokes `$continue`, the
continue workflow should recover this checkpoint and proceed from `Resume at`.
After continuation begins, remove the single leading `🛑 ` marker from the
current title when the thread can be identified confidently; preserve the rest
of the title unchanged. Do not restore an earlier status marker: the pause
marker replaced it rather than stacking on it.

## Boundaries

- A pause is not a timed sleep, cancellation, completion, blocked state,
  closeout, archive, handoff, or authorization revocation.
- Existing explicit approvals remain documented with their exact scope, but a
  pause does not grant new authority or bypass an action-time confirmation.
- Do not create a durable file unless the active workflow already requires one
  or the user explicitly asks to save a checkpoint artifact. The thread
  checkpoint is the default durable record.
- If title renaming fails, say so and do not claim the task was visually marked
  as paused. The work is still paused once the checkpoint is returned.
