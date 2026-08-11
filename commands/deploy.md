---
description: Deploy the current task's feature across all required repositories.
argument-hint: "[environment] [feature-pr-or-repo]"
---

# Deploy

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `/Users/preston/.codex/skills/deploy/SKILL.md` completely.
2. Treat the first argument as the required target environment and later
   arguments as optional feature, PR, commit, repository, or component scope.
3. If the environment is missing or ambiguous, ask for it before making
   deployment changes. Normalize only an unambiguous typo and state it.
4. Resolve every repository and runtime required by the current task's feature,
   build the deployment graph, and create or continue the persistence goal.
5. Continue until every graph node has verified deployment evidence or the
   skill's genuine blocker boundary is reached.
6. Do not run feature test suites; leave feature validation to `/test`.
