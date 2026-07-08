---
description: Resolve found issues, deploy the fixes, and verify the live result.
argument-hint: [issue-source-or-deploy-target]
---

# Hot Fix

Resolve issues that have already been found, deploy the fixes through the
repo's established path, and verify the deployed behavior.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/hot-fix/SKILL.md`.
2. Treat `$ARGUMENTS` as the issue source, target repo, deploy environment, or release instruction.
3. If `$ARGUMENTS` is empty, infer the issue source and deploy target from the current conversation when obvious; otherwise ask for the missing context.

## Required Behavior

- Confirm or reproduce the found issue before editing when feasible.
- For debugging, state a concrete hypothesis after first inspection.
- Make the smallest durable fix that matches existing repo patterns.
- Run relevant tests, builds, browser checks, logs, or API probes before deploying.
- Deploy with the repo's normal release path after confirming the target.
- Verify the live deployed result against the original issue.

## Output

Report:

- issues fixed
- files changed
- verification run before deploy
- deployment target and command/path used
- live verification evidence
- remaining risk or follow-up
