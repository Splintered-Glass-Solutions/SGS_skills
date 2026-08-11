---
name: run-user-story
description: >-
  Expand a short, high-level product scenario into a complete user-story
  hardening contract, then execute it end to end by testing each step, auditing
  the actual result, diagnosing defects, implementing authorized fixes, and
  retesting until the story passes or reaches a genuine blocker. Use when the
  user asks Codex to create and run a user story, exercise a realistic workflow,
  test and harden a multi-step journey, turn an example into an autonomous QA
  run, or produce the same audit-repair-retest style of workflow used in prior
  Bonfire business or ministry testing.
---

# Run User Story

Turn shorthand into an executable contract and run it. Do not stop after writing
the story unless the user explicitly asks for `draft only`, `prompt only`, or
`planning only`.

## Pairing

Before execution, load and follow these skills when available:

- `$test` for feature-scoped coverage and evidence
- `$autonomous-feature-build` for authorized diagnosis, repair, and retesting
- `$codex-safe-run` for browser-heavy, multi-surface, or noisy work
- `$session-budget` for durable checkpoints on long runs

Minimize token and log overhead, but impose no arbitrary token cap and never stop
merely to conserve tokens.

## 1. Interpret The Shorthand

Extract or safely infer:

- actor and authenticated identity category
- organization, tenant, account, or workspace
- starting surface and exact user actions
- expected result after each action
- source data, connectors, skills, templates, and knowledge required
- resources, revisions, messages, tasks, shares, or records created
- target environment and proof surfaces
- permissions and state changes required
- prohibited actions and final outcome

Use the current conversation, repository instructions, and existing product
configuration to resolve ordinary ambiguity. Ask only when an unresolved choice
would materially alter permissions, customer data, billing, deployment,
destructive impact, or accepted product behavior.

## 2. Establish The Authority Ledger

Write a compact authority ledger before mutation:

- current repo, worktree, branch, and whether they must remain fixed
- local code-edit authority
- exact remote database and allowed operation classes
- RLS, permission, role, and policy authority
- provider/OAuth configuration authority
- approved message recipients or test-address pattern
- deploy authority
- destructive or breaking operations

Never infer high-impact authority from the existence of credentials. Preserve the
current thread, worktree, and branch by default. Do not deploy unless the user
explicitly authorizes the exact target. Treat deletion, reset, truncation,
breaking migrations, and data loss as prohibited unless explicitly authorized.

An explicit user instruction may authorize non-destructive production-connected
database, RLS, permission, configuration, seed, upsert, provider, or messaging
work. Record that exact scope and honor it literally. A tool-required
action-time confirmation still applies.

## 3. Expand The Story

Read [references/story-contract.md](references/story-contract.md) completely and
instantiate it for the supplied scenario.

Make every step observable and decision-complete. Include:

- the exact user action or prompt
- prerequisites and setup
- expected UI, data, provider, and permission outcomes
- quality audit criteria, including grounding and tenant isolation
- evidence to capture
- repair and retest boundary
- final acceptance criteria

Use realistic test data. Prefer existing sources and templates when the story
depends on retrieval. Label new fixtures as test-only. Do not mistake route
health, mocks, builds, or screenshots for real authenticated behavioral proof.

Save a durable run ledger for substantial, browser-based, hosted, provider, or
multi-system stories under the repository's existing QA/output convention.

## 4. Execute Immediately

Unless the user asked for draft-only output:

1. Inspect the current implementation and establish the narrow feature scope.
2. Verify prerequisites, identities, tenant, connectors, and source records.
3. Execute one story step through the real user surface.
4. Compare actual versus expected behavior and inspect downstream state.
5. If the step fails or quality is weak, record evidence and state a concrete
   root-cause hypothesis before editing.
6. Implement the smallest authorized fix.
7. Run focused deterministic checks, then rerun the failed user step and its
   direct integration boundary.
8. Continue only when the step passes or a genuine blocker is recorded.
9. Repeat through the complete journey, including external receipt, incognito,
   permission-denial, revision-history, or revocation proof when applicable.

Do not repeat an identical failed approach. After repeated failures, change the
hypothesis or validation strategy and checkpoint the evidence. Continue while
safe, authorized progress remains; stop only for a genuine blocker or missing
authority.

## 5. Audit Every Step

Audit applicable dimensions:

- correct source selection and working links
- factual grounding, attribution, and no invented claims
- organization ownership and tenant isolation
- persistence in the authoritative database/review surface
- correct revision behavior rather than silent overwrite
- provider draft, sent, received, and thread state
- recipient resolution from organization context
- role-based allow and deny behavior
- public/incognito rendering and private-data exposure
- share revocation
- loading, error, empty, retry, responsive, and accessibility behavior

For AI output, passing means both technically successful and meaningfully useful.

## 6. Completion

Finish with one story status:

- `PASS — FEATURE-SCOPED`
- `FAIL — FEATURE-SCOPED`
- `INCOMPLETE — FEATURE-SCOPED`
- `NOT TESTABLE YET — PLANNING ONLY`

Report:

- instantiated story and explicit exclusions
- authority ledger
- environment, repo/worktree/branch/SHA, identity category, and target URLs
- acceptance-criterion-to-proof ledger
- defects, hypotheses, fixes, changed files, and stateful operations
- focused tests and authenticated browser/provider evidence
- truth matrix separating local, remote database, hosted, provider, public, and
  customer-visible proof
- remaining uncertainty and exact next safe action

Do not collapse local success into deployed, hosted, production, provider, or
customer-visible success.

## Invocation Examples

- `Use $run-user-story in our sales test org: pull the latest discovery call,
  create a proposal from our template, revise it, and verify public sharing.`
- `Use $run-user-story for the ministry test org: submit three prayer requests
  through the widget, draft distinct follow-ups, route them to staff, and verify
  email receipt.`
- `Use $run-user-story draft only: an admin turns a meeting transcript into a
  training guide and shares it with volunteers.`
