# QA Run Storage Adapters

## Common record model

Keep these concepts using the project's field names:

- run ID, project, environment, target and catalog/checklist revision;
- immutable selected-check IDs and count;
- executor identity, optional configured reviewer and separate signatory;
- code/build revisions, timestamps, fixture bindings and mutation boundaries;
- append-only attempts with check ID, input, status, expected/observed result;
- command/observation evidence, safe artifacts and defect relationships;
- cleanup state, final rollups and persistence/readback status.

Never assume a named reviewer exists. Resolve required identity foreign keys
through existing project mappings. If unavailable, use local artifacts and report
central persistence blocked; do not create staff access or substitute an identity.

## Existing store

1. Discover the documented authenticated writer and schema.
2. Validate the exact target and write authority before creating the run.
3. Create the parent run and snapshot the selected scope.
4. Append each result/attempt with idempotency keys or version guards as supported.
5. Read back stored attempts and evidence; reconcile IDs, statuses and counts.
6. Retain retries, failures and defect history. Finalization cannot erase them.

Do not issue raw SQL or create missing tables just because API writes fail.
Preserve an import-ready local run when the configured store is unavailable.

## Local fallback

Use a new project-local `output/qa/<run-id>/` directory unless a project convention
already exists. Keep `run.json`, `selected-checks.json`, `attempts.jsonl`,
`manual-run.md` and safe evidence files. Add private artifacts to the local Git
exclude when they must not be committed. Never store credentials or raw sessions.

An example metadata document:

```json
{
  "run_id": "qa-example",
  "project": "sample-project",
  "environment": "local",
  "reviewer": null,
  "review_status": "unassigned",
  "selected_count": 1,
  "persistence": "local"
}
```

Treat this as a model, not a deployed schema. Use atomic local updates, preserve
existing runs and validate required fields and count reconciliation. If the
project requires dashboard persistence, a local fallback does not satisfy that
gate; mark synchronization blocked until verified through readback.
