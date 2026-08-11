---
name: hot-fix
description: >-
  Resolve issues that have already been found, verify the fixes, deploy them
  through the repository's established release path, and confirm the deployed
  behavior. Use when Preston asks to hot fix, fix issues from QA/review/CI/logs,
  or resolve found problems and deploy the fixes.
---

# Hot Fix

## Overview

Use this skill to turn already-identified issues into a verified, deployed fix.
Keep the loop tight: reproduce or confirm the issue, make the smallest durable
change, run relevant proof, deploy by the repo's normal path, and verify the
live result.

## Workflow

1. Classify the work as build work or debugging under the session budget
   protocol. If the issue list is broad, cross-repo, risky, or likely to loop,
   use `session-budget` before editing.
2. Identify the issue source: QA notes, review findings, CI output, logs,
   browser evidence, user screenshots, or a prior agent report. Do not invent
   extra scope beyond the issues found.
3. Inspect the owning repo and current git state. Read relevant local
   instructions, package scripts, deploy docs, CI config, and matching code
   before editing. Preserve unrelated user changes.
4. For debugging issues, write a concrete hypothesis after first inspection and
   before changing code. For review findings, prioritize correctness,
   regressions, security, and missing proof.
5. Implement the smallest fix that addresses the verified issue. Prefer existing
   helpers, patterns, tests, and deployment scripts over new abstractions.
6. Run relevant verification before deployment: focused tests, type checks,
   lint/build, browser checks, screenshots, logs, or API probes as appropriate.
   Do not keep iterating without new proof.
7. Deploy through the repo's established path. Confirm the target environment,
   branch, service, and credentials first. If the deploy target or permission is
   ambiguous, ask before changing production state.
   When multiple environments are requested, resolve and preflight each target
   independently. Deploy a confirmed, explicitly authorized target even if
   another target is absent, unmapped, or uncertain. Do not infer or substitute
   the uncertain target; report it separately. Stop every target only when a
   shared artifact, safety prerequisite, or dependency makes a partial rollout
   unsafe.
8. Verify the deployed result against the original issue with live evidence:
   hosted route checks, API responses, logs, health checks, smoke tests, or
   screenshots. Keep "local build passed" separate from "deployment verified."
9. Report what changed, proof gathered, deploy target/version, live verification,
   and any residual risk or follow-up.

## Guardrails

- Do not run destructive git or infrastructure commands unless Preston asked
  for that exact operation in the current conversation.
- Do not merge, push, promote, or change production data when repo-specific
  memory or local instructions require an explicit current approval.
- Do not change database permissions, grants, roles, ownership, or RLS unless
  the user explicitly approved that exact class of change.
- Avoid drive-by refactors. Fix the found issues and leave unrelated cleanup for
  a separate task.
- If protected hosted QA is required, use the approved auth path instead of
  treating public-only checks as sufficient.

## Slash Command Arguments

When invoked from `/hot-fix`, treat `$ARGUMENTS` as the source of the found
issues, target repo, deploy environment, or release instruction. If arguments
are empty, infer from the current conversation only when the issue source and
deploy target are obvious; otherwise ask for the missing issue source or target.
