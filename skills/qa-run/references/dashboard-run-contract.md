# Bonfire QA Run Adapter

Read this file completely for Bonfire runs after reading `run-storage-adapters.md`.

## Contents

- Canonical sources
- Preferred transaction boundary
- Proposed table mapping
- Codey reviewer mapping
- Lifecycle and outcome rules
- Metrics
- Safety and evidence
- Persistence proof

## Canonical sources

- QA catalog contract: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_check_catalog.md`
- QA dashboard product/schema specification: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_dashboard_product_spec.md`
- Main check catalog: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_checks.jsonl`
- Retirement ledger: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_check_retirements.jsonl`
- Release regression delta: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_release_update_checks.jsonl`
- Bonfire QA runbooks: `/Users/preston/Code/bonfire/docs/qa/`
- Browser failure evidence contract:
  `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_browser_failure_evidence.md`

These files describe intent and local sources. Verify the deployed API, migration ledger, actual table catalog, access, and current catalog checksum before writing.

Treat the retirement ledger as a denylist over every local catalog source, and treat `app_private.qa_quality_check.is_active = false` as the deployed equivalent. Never select a retired check for a new session or include it in pass-rate denominators unless the user explicitly reactivates it. Preserve existing revisions, attempts, evidence, and defect history.

## Bonfire defaults

- Environment: use the named/current environment; otherwise default to `dev` and state the assumption.
- Test workflow: use `$bonfire-qaqc` and `/Users/preston/Code/bonfire/docs/qa/`.
- Local run folder: follow the Bonfire QA runbook, normally `output/qa/{environment}-full-YYYY-MM-DD/` for full runs.
- Reviewer: `Codey` exactly.
- Production and shared Supabase data: read-only unless separately authorized.

## Current Bonfire fixture bindings and authority

Use `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_fixture_registry.json` as the non-secret fixture binding source. Verify each referenced row still exists and is active before a run; do not copy tokens or passwords into QA records.

- `QA_PRIMARY_ORG` and `QA_DISPOSABLE_ORG`: `Test Org`, UUID `21ccdc7d-53c0-4de0-bcef-48ebca590cc5`.
- `QA_AUTHENTICATED_USER` and `QA_ORG_ADMIN`: `codex-dev-qaqc@haybonfire.com` for Test Org when its secure login path is available.
- `QA_SUPER_ADMIN`: `preston@heybonfire.com`.
- `QA_GENERAL_AGENT`: `Creative Scope QA Level 2`, UUID `ce6cd921-ca5a-4549-a93d-3e02d93fb2af`.
- `QA_WIDGET_AGENT`: `Creative Scope QA Level 3`, UUID `8745576f-c468-458c-bfe4-ddb40166e109`.
- `QA_RICH_KB` and `QA_PUBLIC_KB`: `Creative Scope QA KB`, UUID `bca5e6f4-ceca-4992-b537-905b35080313`.
- `QA_DISPOSABLE_KB`: `test drive`, UUID `0673bb3e-e096-4c5a-a92e-a6750fdebb06`; create and clean up per-run records instead of deleting the KB.
- `QA_API_KEY`: retrieve the Test Org Dev key from macOS Keychain service `codex-bonfire-test-org-api-dev`; never log or persist the raw value.
- `QA_SCOPED_API_KEY`: use the same Test Org Keychain entry for the current read/write MCP suite; create narrower read-only/write-only keys only when a scope-enforcement check requires them.
- `QA_ETL_OPERATOR`: AWS CLI identity `arn:aws:iam::088342066989:user/live-ai-preston-pope` in `us-east-1`.
- `SCHEDULER`: the exact AWS EventBridge Scheduler resource named by the check; resolve its live input and target before execution.
- `SERVICE_IDENTITY`: the deployed Lambda execution identity for the named job; resolve it from the live Lambda configuration rather than using a human credential.
- Preston Personal MCP: org UUID `d37b225b-7b49-49d7-a628-d383359e851b`, agent `Bonnie` UUID `e150080c-acbe-44f6-b85e-1ebc966d0f00`, Codex MCP name `bonfire-preston-personal`.

For protected hosted Super Admin checks, first use an existing approved browser
session authenticated as `preston@heybonfire.com` and verify the rendered
identity/role. Do not record “hosted authenticated proof unavailable” before
trying that session. If it has expired, preserve the exact sign-in blocker and
request a session refresh rather than replacing it with fixture-mode proof.

For hosted Campfire checks, use `QA_GENERAL_AGENT` or `QA_WIDGET_AGENT` from
this registry instead of a synthetic local-only UUID. Select an enabled trusted
voice when Campfire requires it, submit one bounded QA prompt, and verify the
real bootstrap/session/assistant-response path. A synthetic intercepted browser
test is local proof and cannot justify skipping the hosted check.

For local and hosted Dev, Preston has approved create, update, external-effect-free destructive, and cleanup actions whose durable application data is contained to Test Org. Create a QA-marked record when possible, capture its ID/before-state, mutate or delete only that record, verify the terminal state, and verify tenant isolation. This approval does not include paid Stripe subscriptions, real external recipients, public posts, destructive provider-account operations, cross-organization writes, permission/RLS/role changes, or production application promotion.

Hosted endpoints:

- Bonfire Dev: `https://dev.heybonfire.com`
- Super Admin Dev and QA/QC dashboard: `https://bonfire-super-admin-dev.up.railway.app`
- Session API and Agent Tools MCP Dev: `https://dev-api.heybonfire.com`

AWS ETL inspection uses account `088342066989`, region `us-east-1`, through the configured `live-ai-preston-pope` CLI identity. Re-run `aws sts get-caller-identity` before every live ETL pass. Live schedule or queue invocation remains bounded to Test Org and the named check; do not infer broad production fan-out authority from CLI access.

## Preferred transaction boundary

Use deployed server-only QA endpoints when available. The proposed endpoint families are:

- `POST /api/qa/sessions`
- `GET/PATCH /api/qa/sessions/{sessionId}`
- `POST /api/qa/sessions/{sessionId}/attempts`
- `PATCH /api/qa/attempts/{attemptId}` while in progress
- `POST /api/qa/attempts/{attemptId}/complete`
- `POST /api/qa/attempts/{attemptId}/evidence-upload`
- `POST /api/qa/defects`
- `POST /api/qa/defects/{defectId}/attempts`
- `POST /api/qa/sessions/{sessionId}/complete`

Do not assume these endpoints exist merely because the product specification lists them.

## Proposed table mapping

When the deployed implementation matches the current specification:

- `app_private.qa_test_session`: one run/session.
- `app_private.qa_test_session_check`: selected checks and stable snapshots.
- `app_private.qa_test_session_fixture`: non-secret fixture resolutions.
- `app_private.qa_test_attempt`: append-only execution/retest results.
- `app_private.qa_test_evidence`: screenshot, file, URL, request-ID, console, or network evidence metadata.
- `app_private.qa_defect` and `qa_defect_attempt`: defect and attempt history.
- `app_private.qa_test_event`: append-only audit stream.
- `qa_v_session_rollup`: coherent session metrics.
- `qa_v_check_recent_history`: last five terminal attempts.

Adapt to the actual deployed schema/API. If the dashboard implementation is absent or unavailable, use the generic local-only adapter and mark `dashboard_sync_status: blocked`. Do not create missing tables or permissions as part of a run.

## Codey reviewer mapping

The reviewer display name must be exactly `Codey`.

1. Query the existing dashboard/staff identity mapping for Codey.
2. If the deployed schema has `reviewer_id`, use Codey's real ID.
3. If it has a text `reviewer_name`, set `Codey` exactly.
4. If it follows the current proposal and has no reviewer column, use Codey's real staff/auth UUID in `qa_test_session.assigned_to` and verify the dashboard renders that identity as `Codey`.
5. Keep the authenticated actor in `started_by` and attempt `tested_by`.
6. Never use Codey's identity in `signoff_by` without an actual Codey sign-off action.
7. If no valid Codey mapping exists, stop dashboard creation rather than inventing a UUID or assigning a human substitute.

## Lifecycle and outcome rules

- Create the session and selected-check snapshots before testing.
- Keep terminal attempts immutable.
- Create a new monotonically numbered attempt for every retest.
- Require actual result plus evidence for failures.
- For browser failures, require `runtime_context.browser_test_results` with an
  independent outcome for every mapped test and attributable error/stack/artifact
  detail for each failed test. Reject runner-exit-only and mixed aggregate text.
- Require reasons for blocked, N/A, and skipped outcomes.
- Keep not-run as session-check state, not an attempt outcome.
- Verify cleanup for checks that mutate disposable state.
- Write audit events for creation, assignment, attempts, evidence, defect linkage, overrides, pause/resume, completion, and sign-off.

## Metrics

Use the dashboard's actual views/functions when deployed. Otherwise verify the formulas:

```text
applicable_selected = passed + failed + blocked + skipped + not_run + in_progress
evaluated_applicable = passed + failed + blocked
quality_pass_rate = passed / evaluated_applicable
execution_completion_rate = (passed + failed + blocked) / applicable_selected
spec_disposition_rate = (passed + failed + blocked + not_applicable) / all_selected
```

When `evaluated_applicable = 0`, quality is `Not enough data`.

## Safety and evidence

- Production defaults to read-only.
- Dev may share production data.
- Contained writes require approved disposable fixtures and cleanup.
- External writes require approved sandbox recipients/records.
- Destructive and paid checks require exact approval and bounded scope.
- Store evidence privately; never put binary/base64 data directly in the relational table.
- Redact secrets and unrelated customer/personal data before upload.
- Run `scripts/validate_qaqc_failure_evidence.py` from `bonfire_shared_docs`
  before writing new attempt packets. A reporter/harness failure without an
  attributable product assertion is `blocked`, not `failed`.

## Persistence proof

A successful run write requires all three:

1. mutation response or transaction evidence;
2. read-back of the created session and child records;
3. dashboard/API rollups matching the local run log.

A local `manual-run.md`, queued request, or successful HTTP acceptance without read-back is not dashboard persistence proof.
