# Continue In New Thread Agent Playbook

This is a platform-neutral version of the `continue-in-new-thread` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Continue a context-heavy Codex task in a new thread by transferring its essential decisions, evidence, constraints, and next actions. Use when the current thread is becoming too large to work reliably or the user asks for a fresh continuation thread.

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

# Thread Handoff

Create a verified continuation before closing the source thread. A title match
does not transfer conversation history, files, or working-tree state; explicitly
carry each needed item forward.

## Decide whether to hand off

Use this when remaining context is becoming too small for the work left, or
when the thread's size makes it hard to preserve important context reliably.
Treat this as a continuity operation, not permission to broaden the task. Keep
working in the current thread when an approval or user answer is pending and the
successor would need to act on it before it arrives.

## Build the handoff

Before creating the successor, assemble a compact, actionable handoff from the
available thread history. Include only information needed to continue:

- The user's objective, current phase, scope, and explicit constraints or
  permissions.
- Decisions already made and why; distinguish confirmed facts from assumptions
  and unresolved questions.
- Work completed, exact files/paths, IDs, URLs, branch or worktree details, and
  the evidence or validation level supporting each result.
- Remaining work in priority order, with the next concrete action.
- Risks, blockers, pending approvals, and any actions the successor must not
  take without new authorization.

Preserve exact identifiers and important numbers. Do not claim that a test,
deployment, database write, or external action succeeded unless the thread
contains evidence for it. If earlier history is unavailable, state that the
handoff covers only the visible context.

## Create and verify the successor

1. Resolve the current thread title, project, host, and workspace from active
   thread metadata. Keep the same title as requested. Use the same project and
   host when available; use a projectless thread only when the source is
   projectless.
2. Create the successor with the handoff as its initial prompt, so the context
   arrives with the new task. Ask the successor to run `$prioritize` on itself
   first, then continue from the stated next action. Do not prioritize the
   source thread.
   For an ongoing build, record `handoff=preparing` in the existing checkpoint
   before creation. Instruct the successor to prioritize itself and verify
   checkout access read-only, then wait for `handoff=ready` naming its thread as
   owner before any product write or new worker dispatch. It must reuse the
   ledger and retain scope, permissions, cumulative budgets and incomplete gates.
3. Preserve workspace state separately from conversational context. If
   continuing requires uncommitted changes or a particular worktree, identify
   the exact checkout and ensure the successor can access that state using a
   supported, authorized mechanism. Do not assume a same-name thread shares a
   checkout. Do not reset, stash, commit, publish, or remove work as part of
   transferring context unless separately authorized. If the needed workspace
   cannot be safely made available, leave the source open and explain what is
   missing.
4. Confirm creation succeeded and the successor has the handoff prompt. If
   creation is pending, wait for its terminal status. If creation fails or the
    result is ambiguous, do not close the source or claim the handoff is
    complete.
5. Verify the successor itself is prioritized: its title has one leading `★`
   and its native pin state is set. Do not treat the instruction in the initial
   prompt as proof that prioritization happened. If it cannot be verified, keep
   the source open and report the limitation.

6. For an ongoing build, after receipt, workspace access, priority and supported
   ownership transfer are verified, record `handoff=ready` with the successor's
   thread ID in the checkpoint. The source stops product work before this marker
   is written; only the successor may proceed. If verification fails, leave the
   marker unready and retain source ownership before resuming safe source work.

## Close the source thread

After the successor and its priority are verified, use `$close-thread` to close
out the source thread. This skill creates and prioritizes the successor;
`$close-thread` handles only source-thread preservation, cleanup, and closing.
For an ongoing continuation, first record needed worktrees as `handed_off` with
the verified successor owner. Retain those checkouts, branches, evidence and
needed services; exclude them from source cleanup. Closing the source chat does
not complete the original objective or authorize publishing/removing continuing
work. If checkout ownership/access cannot safely transfer, leave the source open.
Follow its requirements and target the source thread only. Do not begin its
cleanup before the successor is ready. If closeout cannot safely complete,
leave the source thread available and report the specific blocker. Do not claim
the source is closed unless its required title and pin-state updates succeeded.

## Report

Give a short result stating the successor title and that it received the
handoff, whether it was prioritized, and whether the source thread closed. If
any step failed or remains pending, state which one and what should happen next.
