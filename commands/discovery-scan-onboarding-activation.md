---
description: "Run Discovery: scan onboarding activation against the project where this command is invoked."
argument-hint: [project-path-or-scope]
---

# Discovery: scan onboarding activation

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at $CODEX_HOME/skills/discovery-scan-onboarding-activation/SKILL.md.
2. Treat the command's current working directory as the project context. Use an explicit project path from $ARGUMENTS only when one is provided; never fall back to another repository.
3. Treat any remaining $ARGUMENTS as the bounded scope or question for the workflow.
