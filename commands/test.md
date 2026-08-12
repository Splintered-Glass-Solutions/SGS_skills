---
description: Test only the feature or features worked on recently in this task.
argument-hint: [feature-or-environment]
---

# Test

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `$CODEX_HOME/skills/test/SKILL.md` completely.
2. Treat `$ARGUMENTS` as explicit feature, file, issue, or environment scope.
3. If `$ARGUMENTS` is empty, infer the latest coherent implementation work from
   the current task using the skill's scope precedence.
4. Run feature-scoped validation only. Do not claim full-repository coverage.
5. If the recent work is planning-only, return the skill's planning-only result
   and future coverage inventory without running unrelated broad suites.
