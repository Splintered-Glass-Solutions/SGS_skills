---
name: bonfire-qaqc
description: Run, resume, reconcile, or report Bonfire QA/QC across frontend pages, interfaces, Web and AI APIs, MCP tools, ETL functions/schedules, and Super Admin. Use for full-suite QA, scoped or delta retests, production readiness, environment validation, blocked-check cleanup, dashboard sessions, manual walkthroughs, release regression checks, and weekly QA reporting. Persist Bonfire runs through the live Supabase QA infrastructure with reviewer Codey and use the Super Admin QA/QC dashboard as the staff interface.
---

# Bonfire QA/QC

Run Bonfire QA as an evidence-backed catalog and session workflow, not only as
a test command or Markdown checklist. Pair this skill with `$qa-run` when
executing and persisting a session. Use `$qaqc-record-upsert` when a feature,
bug fix, route, tool, or job needs a new or revised test specification.

## Operational source of truth

Use these sources for distinct purposes:

- Local authoring catalog: `shared/quality/qa_quality_checks.jsonl` in
  `bonfire_shared_docs`, plus its fixture registry and retirement ledger.
- Live operational catalog and run history: the shared Bonfire Supabase QA
  tables in `app_private` and their server-only `public.super_admin_qa_*` RPCs.
- Staff interface: the QA/QC section of the Dev Super Admin portal.
- Execution instructions: Bonfire repo `docs/qa/full-suite-runbook.md`,
  `docs/qa/environment-matrix.md`, `docs/qa/manual-run-template.md`, and
  `docs/qa/README.md`.
- Browser failure contract:
  `shared/quality/qa_browser_failure_evidence.md` in `bonfire_shared_docs`.
- Local run artifacts: resumable evidence and reconciliation copies, not a
  substitute for database persistence when the live QA writer is available.

For Bonfire, the configured shared Supabase project is
`ntosybsxqkuafqeaimpe`. Dev and production currently share this database.
Preston has approved QA catalog/session/result writes there, but this does not
authorize grants, roles, ownership, RLS, policies, permission changes, or
unrelated customer-data mutation.

Use reviewer display name `Codey`. The configured Bonfire reviewer identity is
`7d3fe45a-2305-492c-89ed-83d578dca9ff`. Treat reviewer assignment, test
execution, and release sign-off as separate concepts; never claim Codey signed
off merely because Codey owns the run.

## Run workflow

1. Resolve `local`, `dev`, or `prod` and the exact requested scope.
2. Read the environment matrix, relevant runbook sections, current catalog,
   fixture registry, retirement ledger, and latest live dashboard state.
3. Verify target health, deployed revision when available, authentication,
   Test Org membership, provider/AWS/MCP readiness, and current git state.
4. Create a dated local folder before execution:
   `output/qa/<environment>-<scope>-YYYY-MM-DD/`.
5. Create `run.json`, `manual-run.md`, `screenshots/`, and `artifacts/`.
6. Create the database session before testing through the existing server-only
   QA RPC. Read it back and verify reviewer, environment, selected checks,
   catalog version/checksum, and planned count.
7. Execute deterministic tests first, then route/service/job checks, then
   authenticated browser/manual checks.
8. Persist every terminal attempt as it completes and update the local run
   artifacts. Read back the stored result rather than trusting the request.
9. Reconcile selected count, attempts, evidence, outcomes, cleanup, reviewer,
   and current dashboard rollups before closing.
10. Complete a session only when every selected session check is terminal and
    stored parity is exact. A completed session is a QA record, not automatic
    release approval.

The session creation RPC intentionally fails closed when a requested check is
inactive, retired, unknown, unavailable in the environment, or not `ready`.
Split runnable `ready` checks from catalog-blocked checks. Do not bypass the
guard with direct inserts or silently remove blocked checks from reporting.

## Scope and delta rules

For a full run, select the active environment-eligible catalog, including
frontend, interfaces, Web API, Bonfire AI API, MCP, ETL, Super Admin, and
release-regression records.

For a delta or resumed run, do not rerun unaffected prior passes. Select only:

- checks never executed;
- checks whose exact blocker is now resolved;
- failures or locally `resolved` outcomes that require environment retest;
- checks whose specification or product behavior materially changed.

Exclude inactive and retired checks. Preserve the retirement ledger and report
how many prior selected checks were removed. Snapshot check revisions into the
session so later catalog edits cannot rewrite history.

Use latest-result semantics when reporting current status. Historical blocked
or failed attempts remain in history but do not override a newer terminal
result. Never edit old attempts to make a later retest look clean.

## Outcomes and evidence

Use the live vocabulary:

- `passed`: exact success criteria were observed at the claimed proof tier.
- `failed`: expected behavior was tested and contradicted by actual behavior.
- `blocked`: the check remains applicable but a prerequisite prevented proof.
- `skipped`: intentionally not executed because of scope or safety.
- `not_applicable`: the behavior does not apply to the selected environment.
- `resolved`: a defect was repaired locally but still requires applicable
  environment acceptance; do not count it as a hosted pass.

Require actual observations for every result. Require evidence before storing a
failure and a precise reason for blocked, skipped, or N/A outcomes. Route health,
HTTP acceptance, a rendered shell, enqueueing, or local tests alone do not prove
downstream or hosted behavior.

For Playwright, Cypress, Computer Use, and other automated browser attempts,
apply `shared/quality/qa_browser_failure_evidence.md` before persistence. Store
every mapped test and its independent outcome in
`runtime_context.browser_test_results`. A failed test requires its exact
file/line/title identity, failure class, actionable error message, bounded stack
excerpt (or why no stack exists), and artifact paths. Reject `Playwright failed`,
`Playwright terminal outcome: failed`, `passed | failed`, and other runner-exit
summaries as failure evidence. When the runner or reporter fails before an
attributable product assertion, record `blocked` with the infrastructure cause
and recovery action, not `failed`.

Validate every new Bonfire attempt packet before import or persistence:

```bash
python3 scripts/validate_qaqc_failure_evidence.py path/to/attempts.jsonl \
  --artifact-root path/to/run-folder
```

Do not complete or synchronize a session when this validation fails.

Store screenshots in the configured private evidence flow when available.
Otherwise save evidence under the run folder and persist a verified file
reference with filename, path metadata, size/hash where available, caption, and
capture time. Never store secrets, raw credentials, unrelated customer data, or
base64 binaries in result JSON.

## Blocker reconciliation

Treat blockers as execution state, not defects. Group current blockers by exact
reason, layer, system, interface, and latest session. Before rerunning, verify
whether the original reason is stale because access, fixture mapping, authority,
deployment, or credentials changed.

Create a new scoped retest session for newly unblocked checks. Preserve the old
blocked attempt and append the new outcome. Common Bonfire blocker lanes are:

- authenticated browser is not in Test Org;
- hosted Super Admin session is missing;
- catalog fixture aliases are unresolved;
- an API route lacks method-isolated or authenticated evidence;
- MCP limited-scope, revoked, or expired credential fixtures are missing;
- AWS scheduler/job access or disposable ETL fixtures are missing;
- provider, payment, external-recipient, or production authority is absent;
- browser automation failed before DOM, screenshot, console, and network proof.

Do not convert a browser/tool timeout into a product failure. Do not leave stale
blockers current after their prerequisite is demonstrably resolved; rerun them.

## Bonfire fixtures and authority

Use the active shared-database organization `Test Org`
(`21ccdc7d-53c0-4de0-bcef-48ebca590cc5`) for ordinary local and Dev app, API,
interface, and ETL checks unless a check explicitly requires Super Admin,
Preston Personal, a second-tenant denial fixture, or a provider sandbox.

Map `QA_PRIMARY_ORG` and `QA_DISPOSABLE_ORG` to Test Org. A disposable fixture
is a QA-only record inside Test Org, not the organization itself. Use a marker
such as `QA-CODEY-<run-id>` and record identifiers, before-state, mutation,
terminal state, cross-org safety evidence, and cleanup.

Preston has approved contained create, update, and destructive QA actions only
inside Test Org. This standing approval does not cover paid subscriptions, real
external recipients, public posting, provider-account deletion,
cross-organization writes, production application promotion, or permission
changes.

Use Preston Personal only for checks that explicitly require its MCP binding.
Use the configured Dev MCP endpoint
`https://dev-api.heybonfire.com/api/v1/mcp/{org_id}/{ai_id}`. Never print MCP,
Supabase, AWS, provider, or application credentials.

For hosted Campfire checks, use the resolved real Dev fixture from
`shared/quality/qa_fixture_registry.json`: prefer `QA_GENERAL_AGENT`, then
`QA_WIDGET_AGENT`, or use a named staff QA agent such as Bulverde Chapel for a
read-only check. Never skip hosted Campfire merely because a local spec uses a
synthetic agent UUID. Exercise the real flow: load Campfire, select an enabled
trusted voice when required, submit one bounded QA prompt, and verify bootstrap,
session creation, the assistant response, and sources when the check requires
them. Keep synthetic intercepted tests as local deterministic proof only.

For ETL, verify AWS CLI identity and exact scheduler/function target before any
execution. Prefer read-only inventory and disposable Test Org fixtures. Do not
run broad provider syncs, paid extraction waves, or YouTube playlists as routine
QA.

## Environment targets

- Local Web: `http://localhost:5001`
- Dev Web: `https://dev.heybonfire.com`
- Dev Session API: `https://dev-api.heybonfire.com`
- Dev Super Admin: `https://bonfire-super-admin-dev.up.railway.app`
- Production Web: `https://app.heybonfire.com`

For Super Admin, require `/api/health` HTTP 200 with `dataMode: live` before
treating the portal as available. Health does not prove authenticated portal
features. `QA_SUPER_ADMIN` is `preston@heybonfire.com`; use that approved
identity for hosted Super Admin checks. Before reporting authenticated proof as
unavailable, try the existing approved browser session for that identity and
verify the rendered account/role. If the session is expired, report the precise
sign-in blocker and ask Preston to refresh that session; do not substitute a
fixture-mode or non-admin identity.

For hosted Dev Web, use a real contained Dev QA session. Deterministic local
auth fixtures may redirect to login and cannot prove hosted acceptance. Use Arc
for authenticated hosted QA unless Preston explicitly requests Chrome.

Production QA is read-only unless Preston explicitly approves an exact action.
Never delete production data or modify a real paid subscription.

## Full-suite coverage

Cover these lanes unless the user narrows scope:

1. preflight, revisions, health, authentication, fixtures, and safety;
2. auth, onboarding, Home/Today, Inbox, Agents, Knowledge, Studio, Widget,
   Campfire, Settings, Developers, mobile, empty/error, and accessibility states;
3. every active Web and Bonfire AI API method/route, including authorization,
   tenant isolation, negative cases, retries, and idempotency;
4. MCP initialization, lists, calls, tools, resources, prompts, auth binding,
   scope enforcement, malformed requests, and session lifecycle;
5. ETL functions, schedules, manual workloads, eligibility, progression,
   retry/DLQ behavior, provider boundaries, and cleanup;
6. Super Admin pages, APIs, authorization, QA/QC dashboard, billing/provider
   safety, and audit behavior;
7. release regressions and cross-system flows.

Run targeted repo tests, type-check, lint, and build in proportion to scope.
Record compact command summaries and file-backed logs rather than streaming
large output through Codex.

## Historical import and recovery

When prior QA ran outside the live infrastructure, import it as a distinct
historical session. Preserve original outcomes, timestamps, notes, evidence
references, catalog snapshot, reviewer mapping, and source manifest. Exclude
retired checks and verify row/count/checksum parity. Never relabel historical
results as newly hosted proof.

After import, calculate the exact delta under the rules above and rerun only
that delta. If evidence binaries remain local, persist verified references and
state that the files are local rather than implying they were uploaded.

## Fixes during QA

Testing/reporting-only requests do not authorize fixes. If fixes are requested,
preserve the failed attempt, implement the repair through the appropriate
feature workflow, write or update its QA specification, and append a retest.
Use `resolved` for local repair and `passed` only after the required environment
acceptance succeeds.

For Dev, do not declare release-clean until required fixes are deployed to Dev
and the final hosted suite passes. Never promote or merge to `main` without an
explicit current production instruction.

## Required handoff

Report:

- environment, target, deployed revisions or missing revision evidence;
- database session ID/key, reviewer Codey, selected count, and catalog version;
- pass, fail, blocked, skipped, N/A, resolved, and not-run counts;
- quality and completion denominators separately;
- exact failures, current blockers, fixtures, cleanup, and evidence paths;
- database read-back parity and local run folder;
- fixes, deploys, provider calls, messages, or permissions not performed;
- whether the result is testing evidence or actual release sign-off.

Use `docs/release-sync.md` separately when validating release-note synchronization.
Do not post or mutate production release history without an explicit request.
