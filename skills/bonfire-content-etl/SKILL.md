---
name: bonfire-content-etl
description: Work on Bonfire content ingestion, knowledge bases, ETL, content sources, uploads, Google Drive, Notion, YouTube, Fathom AI, Fireflies AI, source sync status, content visibility, source downloads, or files under src/services/*content*, src/services/*source*, src/features/content-sources, src/app/api/content, src/app/api/knowledge_base, src/app/api/trigger_sync, or docs/source-etl-handoff.md.
---

# Bonfire Content Sources + ETL

Use this skill for Bonfire ingestion, knowledge base, and content source work in `/Users/preston/Code/bonfire`.

## Source Areas

- Content services: `src/services/content-service.ts`, `src/services/content-upload-service.ts`, `src/services/etl-service.ts`
- Source services: `src/services/content-source-service.ts`, `src/services/youtube-source-service.ts`, `src/lib/google-drive-source.ts`, `src/lib/notion-source.ts`, `src/lib/fathom-ai-source.ts`, `src/lib/fireflies-ai-source.ts`
- Knowledge base service: `src/services/knowledge-base-service.ts`
- Content source UI: `src/features/content-sources/**`
- Content API routes: `src/app/api/content/**`, `src/app/api/knowledge_base/**`, `src/app/api/trigger_sync/**`
- Source ETL docs: `docs/source-etl-handoff.md`

## Ingestion Rules

- Preserve source identity and sync status. Check `content_source_sync_status` behavior before changing triggers or source processing.
- Keep uploaded files, generated content records, and knowledge base versioning consistent.
- Respect content visibility and source download flags.
- Do not run broad external playlist/channel ingestion as routine validation. Use narrow fixtures or single-item syncs unless a playlist/channel bug is explicitly under test.
- For third-party providers, avoid logging raw credentials, tokens, private meeting content, or full document contents.
- For public/widget source display or downloads, verify org, AI, KB, and content visibility boundaries.

## Workflow

1. Classify the source path: upload, manual content, Google Drive, Notion, YouTube, Fathom AI, Fireflies AI, or generic ETL.
2. Read `docs/source-etl-handoff.md` when behavior is unclear.
3. Inspect the source service, content service, knowledge base service, and matching route tests.
4. If schema changes are needed, follow `bonfire-supabase-rls`.
5. If widget source rendering changes, also follow `bonfire-chat-widget`.
6. Add tests for status transitions, visibility/download permissions, duplicate handling, and provider error handling where affected.

## Focused Checks

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/services/content-service.test.ts src/services/content-upload-service.test.ts src/services/content-source-service.test.ts src/services/knowledge-base-service.test.ts src/app/api/content src/app/api/knowledge_base src/app/api/trigger_sync
corepack pnpm type-check
```

For provider-specific UI:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/features/content-sources
```

## Handoff Notes

State which source type was affected, whether schema/types changed, and whether any external provider call was exercised or only mocked.
