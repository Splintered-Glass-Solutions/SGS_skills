# Repo Worktree Lifecycle Agent Playbook

This is a platform-neutral version of the `repo-worktree-lifecycle` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Coordinate isolated Git worktrees across parallel coding, integration, release, handoff, and cleanup. Use when creating or reusing worktrees, merging parallel changes, deploying from a worktree, or preventing stranded local work.

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

# Repository Worktree Lifecycle

Use this shared workflow across repositories. Read the [operating contract](references/operating-contract.md) whenever work will create or change a branch/worktree, integrate parallel work, publish a release, or remove a checkout. Repository-specific instructions still define the true remotes, release refs, test commands, provider targets, and permissions.

This skill keeps parallel writers isolated, integration serialized, deployed revisions traceable to remote release refs, and every worktree owned or safely recoverable. It does not grant permission to publish, deploy, discard work, or remove checkouts beyond the current task's authorization.
