---
name: bonfire-etl-security-review
description: Review Bonfire_ETL security-sensitive code. Use when touching URL ingestion, crawler behavior, redirects, storage paths, Supabase/Postgres tenant validation, provider credentials, webhook auth, Sentry/logging, secret handling, or cross-tenant data boundaries.
---

# Bonfire ETL Security Review

## Scope

Use this skill in `/Users/preston/Code/Bonfire_ETL` when reviewing or changing security-sensitive ETL behavior.

Focus on concrete bugs and regression tests. Avoid broad security essays unless the user asks for a report.

## Source Of Truth

Read when relevant:

- `docs/etl_readiness_report.md`
- `security_best_practices_report.md`
- `shared/python/bonfire_etl_shared/validate.py`
- `shared/python/bonfire_etl_shared/storage.py`
- `shared/python/bonfire_etl_shared/sentry_instrumentation.py`
- `functions/content_source_sync_link/`
- Provider clients under `functions/content_source_sync_*/src/*client.py`

## Review Checklist

Prioritize:

- SSRF: block localhost, private IPs, link-local metadata hosts, unsafe DNS resolution, and unsafe redirects.
- Storage: sanitize filenames and enforce `org_id/kb_id/content_id/` path scope on reads and writes.
- Tenancy: verify `org_id`, `kb_id`, `source_id`, and `content_id` relationships before reading or mutating rows.
- Credentials: keep provider tokens/API keys out of row JSON, logs, Sentry, responses, tests, and docs.
- Webhooks: require the configured shared secret/header path unless the function has an explicit authenticated alternative.
- Provider payloads: do not log full bodies, transcript text, raw content, signed URLs, or OAuth credentials.
- Retries: mark transient provider/network failures retryable without retrying permanent auth or validation errors forever.
- Limits: preserve caps for bytes, pages, rows, chunks, media duration, API calls, and provider spending.

## Tests To Look For

Security-sensitive changes should usually add or update tests for:

- malicious URLs and redirects
- path traversal-like filenames
- cross-tenant storage pointers
- mismatched source/content/KB IDs
- missing or wrong webhook secrets
- redaction of sensitive fields
- provider auth failures

Useful commands:

```bash
pytest shared/tests/test_storage.py shared/tests/test_validate.py shared/tests/test_sentry_instrumentation.py -q
pytest functions/content_source_sync_link/tests -q
pytest functions/<function_name>/tests -q
```

## Review Output

When the user asks for a review, lead with findings ordered by severity and cite exact files/lines. If there are no findings, say so and note remaining test gaps or live paths not exercised.
