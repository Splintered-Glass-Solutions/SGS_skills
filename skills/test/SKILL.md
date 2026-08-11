---
name: test
description: >-
  Run feature-scoped validation for only the feature or related features worked
  on recently in the current Codex task. Use when Preston invokes $test or
  /test, asks to test the current feature, wants focused QA after recent
  implementation work, or wants the rigor of full-suite-tests without running
  unrelated repository suites.
---

# Test

Run a decision-complete test pass for the latest implemented feature scope in
the current task. Preserve the evidence standards of `full-suite-tests`, but do
not widen into unrelated repository validation.

## Contract

Treat this as **feature-scoped validation**, never a full-repository suite.
Identify the exact recent feature scope before running commands, test every
relevant layer of that scope, and explicitly exclude unrelated suites.

Use this scope precedence:

1. Feature names, files, issue IDs, or environment supplied with `/test`.
2. The latest coherent implementation work in the current task.
3. A current or recent `feature-finish-line` coverage ledger.
4. Files and commits changed for that work, plus their direct integration
   boundaries.
5. The narrowest coherent feature scope supported by the evidence.

Do not infer scope from dirty worktree files alone. Unrelated user changes,
older task work, generated artifacts, and nearby features are out of scope
unless the current task connects them to the feature under test.

If the current task contains multiple recently implemented features that form
one user workflow or shared change, test them together. If they are unrelated,
test only the latest one unless the user explicitly includes the others.

## Planning-Only Guard

Before running tests, determine whether the recent work actually implemented a
testable feature.

If the task only produced a plan, concept document, research, design options,
or other planning artifact:

- Do not run broad existing suites as a substitute for absent implementation.
- Do not claim the planned feature passed.
- Return `NOT TESTABLE YET — PLANNING ONLY`.
- Provide a concise future coverage inventory derived from the plan: expected
  deterministic checks, integration boundaries, browser workflows, responsive
  states, auth needs, and acceptance criteria.
- Stop unless the user explicitly asks to validate the planning artifact itself.

Apply the same guard when implementation cannot be located or the current task
contains only review/diagnosis with no change to validate.

## Environment

Use an explicitly supplied environment: `local`, `dev`, `staging`, `preview`,
`test`, `prod`, or `production`.

If none is supplied, use the most recent environment clearly established in
the current task. Otherwise default to `local`. Ask only when the environment
choice materially changes safety or local validation cannot exercise the
feature.

- `local`: test the current checkout/worktree and documented local services.
- Hosted non-production: verify the target URL and deployed revision before
  treating hosted results as proof. Do not deploy unless the request or active
  workflow authorizes it.
- Production: use read-only, production-safe actions by default. Never deploy,
  mutate customer data, change billing, or broaden permissions without exact
  approval.

Keep local, hosted non-production, and production proof as separate claims.

### Hosted proof tiers

For hosted integrations or user-facing data flows, report these independent
tiers rather than collapsing them into one pass/fail claim:

1. **Runtime:** deployed image/version, queue or worker state, and endpoint
   health.
2. **Workflow/data:** accepted request, terminal source/job status, and the
   expected persisted records.
3. **Rendered UI:** authenticated browser proof of the relevant source card,
   content library, or other user-facing surface.

Mark each applicable tier `passed`, `failed`, `blocked`, or `not applicable`.
If browser access or an approved test identity is unavailable, return
`INCOMPLETE — FEATURE-SCOPED` for rendered proof while stating any passed
runtime and workflow/data tiers. Do not treat an API response, database record,
or health endpoint as rendered-UI proof.

## Workflow

### 1. Establish the feature scope

Classify the task as QA/review. Inspect the current conversation first, then
read only the repo evidence needed to verify scope:

- the implementation summary, acceptance criteria, named issues, and user
  corrections in the current task;
- a finish-line coverage ledger, if one exists;
- the relevant diff, recent task-owned commits, and changed tests;
- nearby QA docs, package scripts, and local instructions for the changed area.

Use `rg` and targeted reads. Avoid broad generated directories and unrelated
worktree changes.

Write a compact feature scope manifest before execution:

- feature(s) and user-visible outcome;
- task-owned files or commits;
- direct dependencies and integration boundaries;
- environment and proof layer;
- acceptance criteria or issue IDs;
- explicit exclusions and assumptions.

If ambiguity would materially change which feature is tested, ask one concise
question. Otherwise choose the narrowest defensible scope and state the
assumption.

### 2. Build the focused test inventory

Map every acceptance criterion, issue, or changed behavior to the smallest
real test set that proves it. Include applicable checks from these layers:

- direct unit, component, service, or route tests;
- focused integration or API tests at changed boundaries;
- type, lint, schema, or build checks limited to packages affected by the
  feature when those checks can catch relevant failures;
- exact finish-line ledger tests and grep patterns;
- browser/e2e/computer-use workflows for user-facing behavior;
- responsive/mobile states when the feature affects layout or interaction;
- authenticated coverage when the feature is behind login;
- environment canaries for hosted proof.

Tests must assert real behavior or outcomes. Type-checks, builds, snapshots,
route health, grep matches, and public smoke tests are supporting evidence, not
substitutes for an applicable behavioral assertion.

Run the smallest broader suite that proves the feature's integration or
regression boundary. Do not run unrelated workspace packages, entire browser
catalogs, or repository-wide lint/build/test commands merely for breadth. A
broader command is allowed when it is the canonical and practical way to run
the required focused tests; explain why it is included.

Record each inventory item as `in scope`, `blocked`, `not applicable`, or
`excluded`, with the reason. Reconstruct an issue-to-test ledger from the task
and diff when no finish-line ledger exists.

### 3. Execute in risk order

Run:

1. direct deterministic tests;
2. focused integration and affected-package checks;
3. local app or environment health needed for the workflow;
4. authenticated browser/e2e/computer-use checks;
5. hosted canaries when the requested proof layer is hosted.

For a user-facing feature, browser coverage is required unless no browser
surface exists or an explicit blocker prevents it. For an authenticated
feature, public-only coverage cannot produce a passing result.

Use project-specific test and QA skills when applicable. Use
`orchestrator-mode` and `codex-safe-run` for multi-surface, browser-heavy,
log-heavy, or otherwise costly runs. For a small deterministic pass, skip that
overhead and state that the run is intentionally bounded.

Keep verbose logs in `/tmp` or the repo's QA output folder and report compact
summaries, focused failures, and artifact paths. Never print secrets.

### 4. Repair and retest within scope

If the invocation authorizes fixing the current feature, batch related failures,
state a concrete hypothesis before editing, repair only task-owned feature code
or tests, and rerun the focused failure plus its relevant integration boundary.
Use at most three batch repair loops unless the user sets a lower cap.

Do not use a test failure to redesign the feature, edit unrelated code, deploy
without authorization, or widen product scope. Stop for a user decision when a
fix would change accepted behavior, permissions, data mutation, billing, auth,
or environment safety.

If the user asked only to test or review, do not edit application code. Report
findings first with file/line or artifact evidence.

## Result Rules

Use one headline status:

- `PASS — FEATURE-SCOPED`: every in-scope behavioral check passed at the
  claimed proof layer.
- `FAIL — FEATURE-SCOPED`: an in-scope assertion failed.
- `INCOMPLETE — FEATURE-SCOPED`: required coverage could not run, including
  missing authenticated or browser proof.
- `NOT TESTABLE YET — PLANNING ONLY`: no implemented feature exists to test.

Never translate these into “full suite passed,” “repo is green,” “release
ready,” or production proof beyond the environment actually tested.

Report:

- feature scope manifest and exclusions;
- environment, repo/worktree, branch, commit, target URL, and deploy ID when
  applicable;
- issue/acceptance-criterion-to-test ledger;
- commands run and status by layer;
- hosted proof tier status when applicable;
- auth identity category used, without secrets;
- browser/manual coverage and artifact paths;
- failures, blockers, repairs, and retests;
- remaining uncertainty and the next safe action.

Create or update a durable QA run log only when the run is substantial, hosted,
browser/manual, or the repo requires it. Otherwise keep the result in the task.

## Safety

- Preserve unrelated dirty work and never reset user changes.
- Do not create fixtures in production or use real customer accounts without
  exact approval.
- Do not change database permissions, grants, roles, ownership, or RLS without
  exact approval.
- Do not promote to production, send external messages, or create project work
  unless the user explicitly asks.
- A focused pass proves only the named feature scope and proof layer.
