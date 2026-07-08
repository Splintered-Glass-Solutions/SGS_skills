# Bonfire Content Source Integration Agent Playbook

This is a platform-neutral version of the `bonfire-content-source-integration` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Add or modify Bonfire content source integrations. Use for provider source work involving Notion, Fathom AI, Fireflies AI, Read AI, SharePoint, Google Drive, YouTube, links, provision functions, sync functions, provider credentials, content_source.config, normalized content storage, or content_process enqueueing.

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

# Bonfire Content Source Integration

## Scope

Use this skill in `<workspace>/Bonfire_ETL` for first-class content source providers.

Content source integrations normally include:

- Router support in `functions/content_source_sync/`
- Optional provider provisioning in `functions/content_source_provision_<provider>/`
- Provider sync worker in `functions/content_source_sync_<provider>/`
- Env and queue wiring in `function.yaml` and Terraform
- Tests for router, provisioner, sync logic, and provider client behavior

## Source Of Truth

Read the roadmap first:

- `docs/feature_plans/note_source_integrations_roadmap.md`

Then read the provider plan when relevant:

- `docs/feature_plans/notion_source_integration.md`
- `docs/feature_plans/fathom_ai_source_integration.md`
- `docs/feature_plans/fireflies_ai_source_integration.md`
- `docs/feature_plans/read_ai_source_integration.md`
- `docs/feature_plans/sharepoint_source_integration.md`

Use existing integrations as examples:

- Links: `functions/content_source_sync_link/`
- Drive: `functions/content_source_provision_drive/`, `functions/content_source_sync_drive/`
- YouTube: `functions/content_source_sync_youtube_video/`, `functions/content_source_sync_youtube_playlist/`, `functions/content_source_sync_youtube_channel/`
- Note/meeting providers: `functions/content_source_sync_notion/`, `functions/content_source_sync_fathom_ai/`, `functions/content_source_sync_fireflies_ai/`

## Common Contract

Every sync worker should create or update one Bonfire `content` row per stable provider object and store normalized content in Supabase Storage before enqueueing `content_process`.

Put provider-neutral metadata in `content.details` when available:

- `provider`
- `provider_object_id`
- `provider_object_type`
- `provider_updated_at`
- `provider_url`
- `content_hash`

Use provider timestamps, revision IDs, or normalized-content hashes to skip unchanged items unless `force_reprocess` is set.

## Credential Handling

- Store provider connection metadata in `content_source.config`.
- Keep raw tokens/API keys out of logs, tests, docs, and row JSON when a secret store is available.
- Prefer secret refs or the existing `CONTENT_SOURCE_CREDENTIAL_SECRET_PREFIX` pattern for note/meeting providers.
- Webhook responses and Sentry events must not include raw payload bodies, tokens, signed URLs, or transcript/content text.

## Failure Behavior

- Continue syncing independent items after a per-object failure when possible.
- Record partial failures in `content_source.sync_issue` or the existing provider-specific issue path.
- Mark retryable provider failures clearly so SQS retries can work.
- Do not enqueue `content_process` until storage write and content row update are complete.

## Validation

Run focused tests for the touched provider plus the router:

```bash
pytest functions/content_source_sync/tests -q
pytest functions/content_source_sync_<provider>/tests -q
pytest functions/content_source_provision_<provider>/tests -q
```

Use live provider calls only when explicitly requested and with tight caps.

