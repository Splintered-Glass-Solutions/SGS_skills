# Bonfire QA/QC Catalog Reference

## Canonical sources

- Contract: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_check_catalog.md`
- Main JSONL catalog: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_checks.jsonl`
- Retirement ledger: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_check_retirements.jsonl`
- Release-history regression delta: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_release_update_checks.jsonl`
- Release-history evidence: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_release_update_inventory.md`
- Dashboard/database design: `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_dashboard_product_spec.md`
- Database table: `app_private.qa_quality_check`

Read the current contract before editing because catalog version, counts, import tools, and schema can change.

For removals, retire rather than delete: add or update one idempotent retirement-ledger row, set the deployed catalog row inactive with a retirement timestamp and reason, and preserve its definition, revision, attempt, evidence, and defect history. Active selection is the union of catalog sources minus retirement-ledger IDs, and the database dashboard must likewise filter `is_active = true`.

Use the release-history delta only for a regression discovered from a historical feature-update or release artifact. Put ordinary new finish-line coverage in the current main/incremental source selected by the catalog contract; do not misclassify it merely because the feature may later be released.

## Required fields

Populate every field:

- `check_id`
- `layer`
- `system`
- `interface`
- `feature_function`
- `date_added`: ISO `YYYY-MM-DD`; best evidence-backed estimate of when the behavior first became available, not when the QA row was created or updated
- `test_account`
- `test_organization`
- `ai_agent`
- `knowledge_base`
- `test_prompt`
- `prerequisites`
- `test_steps`
- `success_criteria`
- `environment_scope`
- `safety_level`
- `source_reference`
- `coverage_key`
- `specification_status`

## Controlled values

- `layer`: `frontend`, `interface`, `api`, `mcp`, `etl`
- `environment_scope`: `local_dev_prod_readonly`, `local_dev`, `dev_prod_readonly`, `local_only`, `dev_only`
- `safety_level`: `read_only`, `contained_write`, `external_write`, `destructive`, `paid`
- `specification_status`: `ready`, `fixture_mapping_required`, `product_intent_required`

Use fixture aliases from the live catalog contract. Common values include `QA_AUTHENTICATED_USER`, `QA_ORG_ADMIN`, `QA_SUPER_ADMIN`, `QA_API_KEY`, `QA_ETL_OPERATOR`, `ANONYMOUS`, `QA_PRIMARY_ORG`, `QA_DISPOSABLE_ORG`, `QA_GENERAL_AGENT`, `QA_WIDGET_AGENT`, `QA_ADMIN_AI`, `QA_RICH_KB`, `QA_EMPTY_KB`, `QA_DISPOSABLE_KB`, and `NONE`.

## Identity examples

- `frontend:agent-editor:mobile-launcher-size`
- `interface:widget:anonymous-browser-privacy`
- `api:post-widget-session:bootstrap-token`
- `mcp:agent-tools:read-query-scope`
- `etl:content-source-sync:canonical-dedupe`

Keep `coverage_key` stable across releases and environments. Preserve an existing `check_id` when updating the same behavior.

For `date_added`, prefer an explicit dated release/feature artifact. Otherwise use the implementing source file's first tracked date; use the latest introduction among multiple required files, then a uniquely relocated source or narrow owning-directory date. Preserve the basis in `shared/quality/qa_date_added_provenance.jsonl`. Use the catalog baseline only as an explicitly labeled fallback when no stronger evidence exists.

## Test specification quality

Steps must tell QA exactly what to open or call, which fixture to use, what action to perform, what state to refresh/retry, what failure or permission case to exercise, what evidence to capture, and what cleanup is required.

Success criteria must be observable and specific. Include persistence, idempotency, authorization/tenant isolation, errors, and terminal downstream evidence where applicable.

Examples of insufficient success criteria:

- "works"
- "returns 200"
- "page loads"
- "job queued"

Examples of useful success criteria:

- The saved mobile launcher size persists after refresh and leaves desktop/open-chat geometry unchanged.
- A token-first widget starts without `api_client_key`, while the legacy compatibility fixture still starts.
- One scheduled ETL event produces the expected bounded work once, reaches terminal content state, and leaves retries/DLQs attributable.

## Database boundary

Bonfire Dev and production may share Supabase data. Treat `app_private.qa_quality_check` as shared-production-connected unless current evidence proves otherwise.

Before an authorized upsert, verify:

1. exact Supabase project and database;
2. actual migration ledger/table schema;
3. current row selected by `check_id` and `coverage_key`;
4. catalog version and record/catalog checksums;
5. revision-history behavior if configured;
6. that the operation changes no permissions, grants, roles, ownership, RLS, or policies.

Without exact database-write authority, complete and validate the local record and report `pending import`.
