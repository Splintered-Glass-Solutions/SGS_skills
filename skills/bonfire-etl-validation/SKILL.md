---
name: bonfire-etl-validation
description: Validate Bonfire_ETL changes with the repo's ETL-specific test, smoke, readiness, and cost-gated provider checks. Use for ETL regression testing, readiness reports, local or live storage smoke tests, paid provider smoke tests, YouTube transcript checks, embedding/process/extract validation, or release confidence for Bonfire_ETL.
---

# Bonfire ETL Validation

## Scope

Use this skill in `/Users/preston/Code/Bonfire_ETL` when the user asks to validate ETL behavior, prepare release confidence, run smoke tests, or assess production readiness for ETL workers.

This is narrower than `bonfire-qaqc`; it focuses on the Bonfire_ETL repo, Lambda workers, storage, provider ingestion, processing, extraction, embedding, and shared ETL helpers.

## Source Of Truth

Read when relevant:

- `docs/etl_readiness_report.md`
- `security_best_practices_report.md`
- Function READMEs under `functions/<name>/README.md`
- Tests under `functions/<name>/tests` and `shared/tests`

## Default Validation Strategy

Start with local deterministic tests:

```bash
pytest functions/<function_name>/tests -q
pytest shared/tests -q
```

For source ingestion changes, include:

```bash
pytest functions/content_source_sync/tests -q
pytest shared/tests/test_storage.py shared/tests/test_validate.py -q
```

For processing/extraction/embedding changes, include the directly affected function suites and any shared helpers touched.

## Live Checks

Live checks require explicit user intent or task necessity.

- Supabase Storage smoke is acceptable when credentials are configured and the test is bounded.
- Live Postgres checks should be scoped to read-only or test-owned data unless the user approves writes.
- Paid transcription, embedding, extraction, and AI enrichment calls must be opt-in with clear caps.
- Do not run broad YouTube playlist/channel ingestion as routine validation.

## Report Format

Summarize:

- Commands run
- Pass/fail/skip counts
- Live services used
- Estimated paid-provider exposure, if any
- Security/tenancy checks covered
- Residual risks or untested live paths

Avoid pasting full logs unless a failure needs the relevant lines.

## Known Risk Areas

Prioritize validation around:

- SSRF and redirect protection for URL ingestion
- Storage path sanitization and tenant prefix enforcement
- `org_id`, `kb_id`, `source_id`, and `content_id` consistency
- Idempotency and duplicate prevention
- Provider rate limit and partial failure behavior
- Secret filtering in logs/Sentry
