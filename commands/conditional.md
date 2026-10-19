---
description: Gate any requested action or ordered action chain on the immediately preceding result.
argument-hint: [action-or-action-chain]
---

# Conditional Gate

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at
   `<agent-config>/skills/conditional/SKILL.md`.
2. Treat `$ARGUMENTS` as the success-branch action or ordered action chain.
3. Inspect the immediately preceding result and evidence in the current task.
4. Execute the requested action(s) only when the preceding result clearly
   succeeded; otherwise return the skill's compact conditional hold recap.
5. Preserve explicit targets and arguments. Do not infer unrelated actions or
   broaden the requested scope.
