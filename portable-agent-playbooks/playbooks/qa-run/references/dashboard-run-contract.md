> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.
# example-project-12 QA Run Adapter

Read this file completely for example-project-12 runs after reading `run-storage-adapters.md`.

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

- QA catalog contract: `<workspace>/example-project-1/shared/quality/qa_quality_check_catalog.md`
- QA dashboard product/schema specification: `<workspace>/example-project-1/shared/quality/qa_dashboard_product_spec.md`
- Main check catalog: `<workspace>/example-project-1/shared/quality/qa_quality_checks.jsonl`
- Retirement ledger: `<workspace>/example-project-1/shared/quality/qa_quality_check_retirements.jsonl`
- Release regression delta: `<workspace>/example-project-1/shared/quality/qa_release_update_checks.jsonl`
- example-project-12 QA runbooks: `<workspace>/example-project-12/docs/qa/`
- Browser failure evidence contract:
  `<workspace>/example-project-1/shared/quality/qa_browser_failure_evidence.md`

These files describe intent and local sources. Verify the deployed API, migration ledger, actual table catalog, access, and current catalog checksum before writing.

Treat the retirement ledger as a denylist over every local catalog source, and treat `app_private.qa_quality_check.is_active = false` as the deployed equivalent. Never select a retired check for a new session or include it in pass-rate denominators unless the user explicitly reactivates it. Preserve existing revisions, attempts, evidence, and defect history.

## Project fixture bindings and authority

Use a project-owned non-secret fixture registry. Resolve environment, QA identity, organization, test fixtures and provider identities before a run. Verify the rendered identity and effective role. Retrieve credentials through the approved secure login path; never record them. Capture the exact current authorization for any mutations and limit writes and cleanup to the named disposable fixtures. This public template grants no standing write authority and includes no live account mappings.

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
- Run `scripts/validate_qaqc_failure_evidence.py` from `example-project-1`
  before writing new attempt packets. A reporter/harness failure without an
  attributable product assertion is `blocked`, not `failed`.

## Persistence proof

A successful run write requires all three:

1. mutation response or transaction evidence;
2. read-back of the created session and child records;
3. dashboard/API rollups matching the local run log.

A local `manual-run.md`, queued request, or successful HTTP acceptance without read-back is not dashboard persistence proof.
