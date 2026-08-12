---
description: Mark the current Codex thread closed by prefixing its title.
argument-hint: [optional-closeout-context]
---

# Close Thread

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at
   `$CODEX_HOME/skills/close-thread/SKILL.md`.
2. Treat `$ARGUMENTS` as optional closeout context to consider in the final
   synopsis.
3. Rename only the current thread title by adding the leading `－` marker when
   it is not already present.
4. Do not archive, pin, move, hand off, fork, create tasks, change files, push,
   deploy, send external messages, or perform any side effect other than the
   title rename.
5. After the rename succeeds, respond with a short synopsis of what was done in
   the thread, any visible outstanding items, and that the thread is closed out.
