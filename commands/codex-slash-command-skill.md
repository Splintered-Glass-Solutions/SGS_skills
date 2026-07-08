---
description: Create or repair a user-level Codex skill so it appears in the slash picker.
argument-hint: [skill-or-workflow-context]
---

# Codex Slash Command Skill

Create or repair a user-level Codex skill with the full slash-picker-visible structure.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/codex-slash-command-skill/SKILL.md`.
2. Treat `$ARGUMENTS` as the requested skill name, workflow, missing picker entry, or command context.
3. If `$ARGUMENTS` is empty, infer the requested skill or command from the current conversation when obvious; otherwise ask for the workflow to turn into a skill.
4. Create `SKILL.md` and `agents/openai.yaml` for picker visibility.
5. Create a matching `~/.codex/commands/<skill-name>.md` wrapper when the user asks for a `/command` or `$ARGUMENTS` support.

## Output

Return:

- skill path
- picker metadata path
- command wrapper path, if created
- validation performed
- any visibility caveat
