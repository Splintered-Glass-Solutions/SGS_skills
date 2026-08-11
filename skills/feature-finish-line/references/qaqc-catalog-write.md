# Bonfire QA/QC Catalog Adapter

Read this file completely for Bonfire finish-line work after reading the generic adapter or `$qaqc-record-upsert` contract.

## Contents

- Required outcome
- Discovery order
- Identity and upsert rules
- Required Bonfire fields
- Writing useful QA instructions
- Local write and validation
- Shared database boundary
- Finish-line reporting

## Required outcome

Every finish-line invocation must leave behind a durable QA specification for every independently testable feature, bug fix, acceptance criterion, or regression changed by the work.

- Create a record when no matching behavior exists.
- Update the existing record when the behavior already exists.
- Split unrelated behaviors into separate records.
- Do not create a duplicate merely because the feature has a new commit, PR, release, or environment.
- Do not store a pass/fail execution result in the specification record. Environment-specific runs and evidence belong in the QA session/result tables.

The finish-line is incomplete if no local catalog record or explicit pending-import record exists.

## Discovery order

1. Locate the project shared-docs repository and its QA catalog contract, JSONL/CSV/seed source, generator, or migration.
2. Search by stable coverage key, exact route/interface, feature/function wording, issue title, and source path.
3. Prefer the project's existing schema and writer/importer.
4. For Bonfire, use:
   - `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_check_catalog.md`
   - `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_quality_checks.jsonl`
   - `/Users/preston/Code/bonfire_shared_docs/shared/quality/qa_release_update_checks.jsonl` when the record belongs to the release-regression tranche
   - `app_private.qa_quality_check` only when the exact shared Supabase write is authorized
5. If no project catalog exists, create an import-ready record at `output/qa/<feature-slug>-qaqc-record.json` in the active repository and identify the missing central-catalog mapping as a blocker.

Preserve unrelated dirty work. Never regenerate, reorder, or rewrite the entire catalog when an atomic upsert is sufficient.

## Identity and upsert rules

Use a deterministic identity independent of database UUIDs and deployments.

- `coverage_key`: stable product surface plus behavior, such as `frontend:agent-editor:mobile-launcher-size` or `api:post-widget-session:bootstrap-token`.
- `check_id`: preserve the existing ID on update. For a new record, follow the catalog's prefix/number convention and prove it is unique before writing.
- Match an existing row by `coverage_key` first, then confirm `interface`, `feature_function`, and source evidence describe the same behavior.
- If a matching coverage key contains a materially different behavior, stop and repair the identity collision instead of overwriting it.
- One record may be updated with better steps, fixtures, prompts, criteria, or source references. Do not erase useful historical scope.

## Required Bonfire fields

Populate every field from the Bonfire catalog contract:

- `check_id`
- `layer`: `frontend`, `interface`, `api`, `mcp`, or `etl`
- `system`
- `interface`
- `feature_function`
- `date_added`: ISO `YYYY-MM-DD`; best evidence-backed estimate of when the behavior first became available, not the finish-line or QA-record date
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

Use fixture aliases from the catalog contract. Use `NONE` when a fixture category is not applicable. Never store passwords, bearer tokens, API keys, provider secrets, customer-sensitive prompts, or environment-specific database IDs.

For new Bonfire behavior, use the earliest defensible availability evidence: an explicit release date when one exists, otherwise the relevant implementation source introduction date. For an update to an existing behavior, preserve its current `date_added` unless stronger evidence corrects it. Add or update the matching entry in `shared/quality/qa_date_added_provenance.jsonl` so the estimate remains auditable.

## Writing useful QA instructions

Write the record so a QA staff member unfamiliar with the implementation can execute it without guessing.

- Name the exact page, interface, method/route, MCP tool, ETL job, schedule, or operational workload.
- State required flags, seeded state, account role, organization, agent, KB, provider sandbox, or device/viewport.
- Include a bounded happy path, persistence/idempotency check, and the nearest relevant negative, disabled, unauthorized, empty, retry, mobile, or failure condition.
- Define observable success. For asynchronous work, terminal content/job/provider state is required; HTTP acceptance or queueing alone is not success.
- For a bug fix, reproduce the original failure condition and assert the exact neighboring state that must remain unchanged.
- Set `specification_status` to `fixture_mapping_required` or `product_intent_required` rather than inventing missing IDs or product behavior.
- Set production scope to read-only unless a fresh approval explicitly permits the mutation.

## Local write and validation

1. Upsert the smallest possible local catalog source record.
2. Preserve JSONL validity and deterministic formatting used by the project.
3. Validate required fields, controlled vocabularies, unique `check_id`, stable/unique `coverage_key`, source-reference existence, and absence of secrets.
4. Run the repository's catalog generator/checksum/validation command when present.
5. Report `created`, `updated`, or `unchanged`, plus the exact record ID, coverage key, file, and validation command.

If the implementation changed several independent behaviors, create/update one record per behavior and report each disposition.

## Shared database boundary

A local catalog update is always required. A database write is separate.

- Inspect the exact project, schema/table, current row/checksum, import command or payload, permissions implications, and whether Dev shares production data.
- Do not infer shared-database permission from the finish-line invocation.
- Use already-valid exact approval when the current task approval register names the same database target and operation.
- Otherwise prepare a pending import artifact and report `database sync: blocked pending exact approval`.
- Never change grants, roles, ownership, RLS, policies, or object permissions as part of a catalog upsert without separate exact approval.
- When authorized, use an idempotent upsert, verify the stored row and checksum, and preserve revision history when the schema supports it.

Database persistence does not prove the feature passed. Record actual executions through the QA session/result workflow.

## Finish-line reporting

Include a `QA/QC catalog record` section with:

- behavior/issue
- disposition: `created`, `updated`, `unchanged`, or `pending import`
- `check_id`
- `coverage_key`
- local source file
- database target and sync status
- validation evidence
- remaining fixture, product-intent, access, or import blocker
