---
description: Save a local Codex skill into SGS_skills, regenerate playbooks, commit, and push.
argument-hint: [skill-name-or-path]
---

# Save Skill

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `/Users/preston/.codex/skills/save-skill/SKILL.md`.
2. Treat `$ARGUMENTS` as the skill name, skill folder, `SKILL.md` path, or
   selected skill content to archive.
3. If `$ARGUMENTS` is empty, infer the skill from selected text when it contains
   a clear `<skill>` block or path. Otherwise ask which skill to save.
4. Archive the skill into `/Users/preston/Code/SGS_skills`, update docs/indexes,
   regenerate portable playbooks, validate, commit, and push.

## Guardrails

- Stage only files related to the saved skill and generated docs/playbooks.
- Do not copy secrets, `.env` files, production data, portfolio ledgers, or
  unrelated local artifacts.
- Do not deploy, send messages, mutate production, change DB permissions, or
  perform protected-branch operations.
