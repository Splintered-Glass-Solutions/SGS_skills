---
description: Start the current project locally for testing.
argument-hint: [optional app or repo context]
---

# Spin Up Local

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `$CODEX_HOME/skills/spin-up-local/SKILL.md`.
2. Treat `$ARGUMENTS` as the requested app, repo, feature, or service context.
3. If `$ARGUMENTS` is empty, infer the target from the current workspace and conversation.
4. Start the local app from the worktree containing the active changes, verify it is reachable, and return the local URL plus runtime targets.
