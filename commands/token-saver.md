---
description: Complete a task with minimal useful context, output, tool use, and retries.
argument-hint: [task or token-saving focus]
---

# Token Saver

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `$CODEX_HOME/skills/token-saver/SKILL.md` completely.
2. Treat `$ARGUMENTS` as the task or token-saving focus.
3. If `$ARGUMENTS` is empty, infer the task from the current conversation when clear; otherwise ask only for the missing objective.
4. Preserve correctness, evidence, safety, and user constraints while reducing avoidable context, source reads, output, tool calls, and retries.
