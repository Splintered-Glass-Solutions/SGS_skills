# Bonfire Etl Validation Agent Playbook

This is a platform-neutral version of the `bonfire-etl-validation` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Validate Bonfire_ETL changes with the repo's ETL-specific test, smoke, readiness, and cost-gated provider checks. Use for ETL regression testing, readiness reports, local or live storage smoke tests, paid provider smoke tests, YouTube transcript checks, embedding/process/extract validation, or release confidence for Bonfire_ETL.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

# Bonfire ETL Validation

## Scope

Use this skill in `<workspace>/Bonfire_ETL` when the user asks to validate ETL behavior, prepare release confidence, run smoke tests, or assess production readiness for ETL workers.

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

