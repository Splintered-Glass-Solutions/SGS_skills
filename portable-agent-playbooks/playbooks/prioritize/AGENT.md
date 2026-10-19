# Prioritize Agent Playbook

This is a platform-neutral version of the `prioritize` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Mark the current the agent task as a native priority by pinning it and setting its single leading title-status marker to a star. Use when the user invokes /prioritize, asks to prioritize, star, flag, pin, or elevate the current task.

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

# Prioritize Task

1. Resolve the current task's existing title from the active-thread context or a
   thread read/list tool. Do not invent a replacement title.
2. Trim surrounding whitespace and remove all existing leading status markers
   plus their separator whitespace. Preserve the remaining non-status title
   text exactly. A leading status stack such as `✍️ 📋` must be removed as a
   unit, not retained behind the star.
3. Rename only the current task to `★ <title>` using the thread-title tool.
   If the normalized title already has exactly one `★` marker, leave the title
   unchanged and report that it is already prioritized.
4. Pin the current task with the native thread-pinning tool. A pin places the
   task in the agent's pinned-task ordering rather than ordinary recency sorting.
   Do not claim it can set a specific pin rank: the available tool has no
   priority-rank or reorder field.
5. Do not create, archive, fork, or modify any other task.

If the current title cannot be resolved, ask for it rather than replacing it.
