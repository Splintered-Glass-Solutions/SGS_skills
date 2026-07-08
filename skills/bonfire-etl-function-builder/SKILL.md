---
name: bonfire-etl-function-builder
description: Build, modify, or review Bonfire ETL Lambda function folders. Use when working on Bonfire_ETL functions, function.yaml files, Lambda handlers, SQS/webhook contracts, Dockerfiles, per-function tests, or shared bonfire_etl_shared helpers.
---

# Bonfire ETL Function Builder

## Scope

Use this skill in `/Users/preston/Code/Bonfire_ETL` when creating or changing a deployable ETL function under `functions/`.

The repo pattern is a containerized AWS Lambda with:

- `function.yaml` for deploy metadata and env placeholders
- `Dockerfile`
- `src/handler.py` for event normalization and Lambda/webhook responses
- `src/logic.py` for business behavior
- `src/models.py` for local message/config types
- `src/helpers.py` or provider clients only when the logic needs them
- `tests/` with focused fixtures for SQS and webhook paths

Prefer existing nearby functions as templates before inventing structure.

## First Reads

Read only what matches the task:

- Router pattern: `functions/content_source_sync/src/logic.py`
- Simple worker pattern: `functions/content_source_sync_youtube_video/`
- Provider worker pattern: `functions/content_source_sync_drive/`, `functions/content_source_sync_notion/`
- Provisioner pattern: `functions/content_source_provision_drive/`
- Nightly batch pattern: `functions/content_source_sync_nightly/`, `functions/trusted_voices_nightly/`
- Shared helpers: `shared/python/bonfire_etl_shared/`
- Function config validator: `scripts/validate_function_yaml.py`

## Implementation Rules

- Keep handlers thin. Normalize input, call logic, return structured responses.
- Put side effects and provider calls behind injectable clients or helper functions so tests can mock them.
- Use `bonfire_etl_shared.event_normalize`, `response`, `errors`, `sqs_client`, `storage`, `validate`, and `sentry_instrumentation` where the existing codebase already uses them.
- Preserve idempotency. Provider syncs should skip unchanged remote objects unless `force_reprocess` is set.
- Use Postgres/Supabase access patterns already present in the repo; do not introduce a new DB client style casually.
- Keep env names explicit in `function.yaml`; secrets should remain placeholders or secret refs.
- Update Terraform/env wiring only when the new function must be deployed by the shared stack.

## Test Expectations

Add or update focused tests under the function's `tests/` directory:

- Direct logic tests for success, skip/idempotent behavior, and failure reporting.
- Handler tests for webhook and SQS normalization if handler behavior changes.
- Fixture JSON for representative SQS/webhook payloads when the function accepts external events.
- Shared helper tests when behavior belongs in `shared/python/bonfire_etl_shared`.

Run the narrowest useful pytest command first. For cross-cutting shared changes, also run affected shared tests.

## Validation

Useful commands from repo root:

```bash
python3 scripts/validate_function_yaml.py functions/<function_name>/function.yaml
pytest functions/<function_name>/tests -q
pytest shared/tests -q
```

Only run live provider, storage, transcription, or embedding checks when the user requested them or the task explicitly requires them.
