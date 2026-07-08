---
name: bonfire-deployment-strategy
description: "Use when planning, changing, or executing Bonfire deployment, CI, PR merge, dev deploy, production promotion, release validation, fast lane, slow lane, or full-suite gating workflows. Captures the default Bonfire rule: dev deploys use the fast lane unless Preston asks otherwise; production promotion uses the slow full-suite lane."
---

# Bonfire Deployment Strategy

Use this skill for Bonfire release, deployment, CI, and promotion decisions.

## Core Policy

- Default dev deployment lane: `fast`.
- Default production promotion lane: `slow`.
- A green dev deploy is not permission to promote to `main` or production.
- Do not merge, push, or promote to `main` unless Preston explicitly asks for that exact production promotion in the current conversation.
- Do not bypass branch protection, required checks, or production gates unless Preston explicitly asks for that exact bypass and the risk is stated.

## Lane Definitions

Fast lane is for normal PRs and pushes targeting `dev`, especially when Preston is batching multiple features into dev before a later hosted full-suite pass.

Fast lane should include:

- dependency install
- lint check
- format check
- app type-check
- widget type-check
- production build

Slow lane is for production promotion, PRs/pushes targeting `main`, manual full-suite requests, and any explicit "full suite" or broad QA request.

Slow lane should include fast lane plus:

- broad Vitest suite
- Knowledge deterministic suite
- DB-pressure deterministic suite
- Playwright browser install
- Knowledge Computer Use suite
- DB-pressure Computer Use suite
- hosted/manual full-suite QA when the request is environment-scoped

## Workflow Expectations

1. Identify target environment: local, dev, main, prod, or production.
2. For dev PR/deploy work, use fast lane unless Preston explicitly asks for slow/full validation.
3. For production promotion, use slow lane and the Bonfire full-suite runbook.
4. If several features are being merged into dev, keep individual PR gates fast, then run full-suite validation against hosted dev before production promotion.
5. For production promotion, pair automated slow lane with manual/authenticated QA evidence when protected routes or customer-facing flows matter.

## Related Skills

- Use `full-suite-tests` when Preston asks for a full suite in local/dev/prod.
- Use `feature-finish-line` before publishing a feature PR if implementation validation is incomplete.
- Use GitHub publish workflows for commit, push, PR, and merge mechanics.

## Reporting

When reporting a deployment or PR:

- State which lane ran.
- State whether the target is dev or production.
- List required checks and any skipped slow-lane checks.
- If only fast lane ran, say that production readiness is not proven.
- If slow lane ran, include the full-suite evidence and any manual QA gaps.
