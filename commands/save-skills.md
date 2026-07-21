---
description: Analyze the current conversation and create reusable skills from repeated workflows.
argument-hint: [current-thread|selected-text|dry-run|include-project-specific]
---

# Save Skills

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `/Users/preston/.codex/skills/save-skills/SKILL.md`.
2. Treat selected text as the highest-priority source, then `$ARGUMENTS`, then
   the current conversation.
3. If `$ARGUMENTS` is empty, analyze the current conversation and create only
   high-confidence candidates that pass the skill's scoring and dedupe rules.
4. If `$ARGUMENTS` contains `dry-run`, assess and report candidates without
   creating or changing files.

## Guardrails

- Prefer improving an existing skill over creating a duplicate.
- Create no more than three new skills per run.
- Generalize private or project-specific conversation details unless explicitly
  told to preserve project scope.
- Do not commit or push; use `$save-skill` separately for Git persistence.
- Do not deploy, send messages, mutate production, change database permissions,
  purchase anything, or alter protected branches.
