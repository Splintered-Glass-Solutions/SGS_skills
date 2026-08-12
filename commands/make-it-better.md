---
description: Autonomously audit and improve a project across UX, design, copy, code quality, tests, polish, and delight.
argument-hint: [optional-project-context-or-permission-boundary]
---

# Make It Better

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `$CODEX_HOME/skills/make-it-better/SKILL.md`.
2. Treat `$ARGUMENTS` as project context, repo scope, product direction,
   permission boundary, or implementation approval details.
3. If `$ARGUMENTS` is empty, infer the project context from the current
   conversation and working directory.
4. Use `$orchestrator-mode`, `$codex-safe-run`, and, when implementation is
   allowed, `$autonomous-feature-build`.

## Required Behavior

- Go as far as possible without blocking on normal questions.
- Queue questions and checkpoints for the final deliverable.
- Move on to other areas when one area is blocked.
- Keep the work read-only unless implementation is clearly approved.
- If implementation is approved, start with high-confidence, low-risk,
  reversible improvements and verify them.
- Do not make production changes, deploy, rotate secrets, change database
  permissions, alter billing, or touch risky account-level configuration without
  explicit approval.

## Output

Report the loops completed, evidence gathered, changes made if any,
prioritized recommendations, validation performed, queued checkpoints, deferred
areas, and a concise next-pass prompt.
