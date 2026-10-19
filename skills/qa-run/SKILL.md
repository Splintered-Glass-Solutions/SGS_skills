---
name: qa-run
description: Execute a scoped QA/QC pass, retain per-check attempts and evidence, and persist the run through an existing project store or a local artifact fallback.
---

# QA Run

Resolve the project, environment, target revision, selected behavior scope,
approved fixtures, tester and reviewer from the request or project configuration.
Do not assume a publisher's staff identity, account, database or standing approval.
A reviewer assignment is not sign-off; keep executor, reviewer and signatory separate.

Read [run-storage-adapters.md](references/run-storage-adapters.md) before persistence.
For a dashboard-backed project, also use the [dashboard adapter checklist](references/dashboard-run-contract.md).

## Scope and authority

Use a bounded QA-only scope by default. Product repairs, deploys, schemas,
permissions, paid operations and real external sends need current task authority.
Writes require approved disposable fixtures and an exact cleanup plan. Credential
access alone is not permission to modify accounts or production data.

1. Discover the project-owned QA catalog or accepted checklist. Record its
   revision, retirements and immutable selected check IDs before execution.
2. Resolve reviewer identity through existing project mappings. If review is not
   assigned, record it as unassigned; do not invent a person or staff UUID.
3. Select the existing API/database writer when available, otherwise create a
   local run folder. Do not create schemas or broaden access just to save results.
4. Create the parent run with project, target, revisions, scope, executor,
   reviewer, fixture bindings, safety exclusions and timestamps in UTC.
5. Execute safe checks in dependency order, reusing still-valid exact evidence.
   Use approved browser sessions for authenticated UI. Treat missing access or
   prerequisites as blocked, not passed.
6. Append one attempt per executed check. Use project-native statuses mapped to
   passed, failed, blocked, skipped or not applicable, with a concrete reason.
   Preserve failures when retesting; never rewrite an earlier attempt as passed.
7. Attach concise evidence: exact command or observation, exit status, target
   revision, safe screenshot/log link, defect link and relevant assertion.
8. Verify persistence through readback. Reconcile selected checks against results,
   latest-attempt counts, unresolved defects and cleanup before closing the run.

## Failure evidence

For a browser failure retain the target URL/environment, steps, expected and
observed behavior, relevant console/network error, screenshot and check/revision.
Use the project's evidence schema when available. Redact secrets and real user
records. A link to a test file alone does not establish that the test ran.

## Closeout

Report scope and revision, selected/result counts, per-outcome rollup, exact
failed or blocked checks, evidence locations, persistence/readback state,
review/sign-off state and next action. A local artifact is valid local evidence;
it is not proof of a dashboard write, hosted behavior or independent sign-off.
For whole-project execution use `full-suite-tests` when installed; do not quietly
expand a scoped QA request to a full-suite run.
