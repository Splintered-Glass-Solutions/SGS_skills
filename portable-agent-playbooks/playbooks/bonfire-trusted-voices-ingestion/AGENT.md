# Bonfire Trusted Voices Ingestion Agent Playbook

This is a platform-neutral version of the `bonfire-trusted-voices-ingestion` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Work on Bonfire trusted voices ingestion. Use for trusted_voices_nightly, trusted voices corpus build scripts, author/chapter/sermon chunk generation, storage ingestion, content_process handoff, or trusted voices docs and tests.

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

# Bonfire Trusted Voices Ingestion

## Scope

Use this skill in `<workspace>/Bonfire_ETL` for Trusted Voices corpus and nightly ingestion work.

Primary areas:

- `functions/trusted_voices_nightly/`
- `docs/trusted_voices/`
- `scripts/build_trusted_voices_*.py`
- `scripts/run_enterprise_content_queue.py`
- `scripts/summarize_enterprise_content_queue.py`
- shared storage/process helpers

## Workflow

1. Read `docs/trusted_voices/README.md` if the task concerns corpus scope or ingestion expectations.
2. Inspect the specific author/source build script before editing or running it.
3. Preserve stable source IDs, titles, author names, section/chapter metadata, and chunk ordering.
4. Keep generated content deterministic. Avoid rewriting corpus text unless the user explicitly asks.
5. Ensure generated items can be stored and handed off to `content_process` with tenant-safe storage paths.
6. Add or update tests in `functions/trusted_voices_nightly/tests` or shared tests when behavior changes.

## Known Scripts

The repo contains many source-specific builders, including:

- `scripts/build_trusted_voices_augustine*.py`
- `scripts/build_trusted_voices_bunyan*.py`
- `scripts/build_trusted_voices_calvin_sections.py`
- `scripts/build_trusted_voices_chrysostom*.py`
- `scripts/build_trusted_voices_edwards*.py`
- `scripts/build_trusted_voices_henry_*.py`
- `scripts/build_trusted_voices_luther_chunks.py`
- `scripts/build_trusted_voices_owen*.py`
- `scripts/build_trusted_voices_ryle_chunks.py`
- `scripts/build_trusted_voices_wesley*.py`
- `scripts/build_trusted_voices_whitefield*.py`

Use the nearest existing builder as the pattern for a new author or source type.

## Validation

Useful commands:

```bash
pytest functions/trusted_voices_nightly/tests -q
pytest shared/tests/test_storage.py shared/tests/test_validate.py -q
```

For bulk or live queue work, confirm limits first:

- `TRUSTED_VOICES_MAX_ITEMS_PER_RUN`
- target org/KB/source IDs
- whether storage writes and content processing enqueueing are intended

Do not run broad corpus backfills or live queue runners without explicit user direction.

