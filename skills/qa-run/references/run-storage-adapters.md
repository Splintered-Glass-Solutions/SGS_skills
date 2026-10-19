# QA Run Storage Adapters

Read this file completely before selecting where to save a QA run.

## Contents

- Required logical model
- Adapter A: normalized dashboard
- Adapter B: single table or document store
- Adapter C: local only
- Reviewer mapping
- Persistence proof

## Required logical model

Preserve these concepts even when field names differ:

- run/session identity, project, environment, target, scope, catalog/checklist revision, build revisions, status, timestamps;
- reviewer display name `Codey`, tester/executor identity, and optional separate sign-off identity;
- selected check identity and immutable specification snapshot/reference;
- append-only attempts with outcome, actual result, reason, notes, runtime context, and cleanup state;
- evidence metadata/path and defect/retest links;
- selected, terminal, passed, failed, blocked, skipped, N/A, not-run, and in-progress counts.

Use the project’s vocabulary and schema when it preserves equivalent semantics.

## Adapter A: normalized dashboard

Use an existing authenticated server API or approved QA writer with separate run, selected-check, attempt/result, evidence, defect-link, and event records.

Sequence:

1. verify deployed schema/API and access;
2. create the parent run with reviewer Codey;
3. snapshot selected checks;
4. append attempts/evidence/events during execution;
5. close or pause through the supported transaction;
6. read the run and rollups back through the dashboard/API.

Do not use direct browser writes to private schemas when a server boundary exists.

## Adapter B: single table or document store

Use the project’s existing QA run table/collection. Store scalar run metadata in first-class fields and atomic results in the supported child relation or structured JSON/document field.

At minimum persist:

```json
{
  "run_id": "project-stable-run-id",
  "project": "project-name",
  "environment": "local|dev|stage|prod|project-value",
  "reviewer": "Codey",
  "tester": "resolved actor or automation identity",
  "status": "in_progress|paused|completed|aborted|project-value",
  "scope": {},
  "revision": {},
  "started_at": "ISO-8601",
  "completed_at": null,
  "results": []
}
```

Use append/update semantics that preserve prior attempts. Do not replace the entire document without checking concurrent edits or revision/version fields.

## Adapter C: local only

Use when the project has no QA database/dashboard, its writer is unavailable, or Codey cannot satisfy a required FK.

Default location:

`output/qa/<environment>-<scope>-YYYY-MM-DD-HHMM/`

Required files:

- `run.json`: structured model above plus counts, result objects, persistence status, and evidence paths;
- `manual-run.md`: readable progress, commands, observations, defects, and handoff;
- `screenshots/` and `artifacts/` when evidence exists.

Use atomic local edits and re-read JSON after every material checkpoint. Local-only persistence is a valid project mode when no dashboard is intended. If the project expects dashboard storage but it is unavailable, label the local run `dashboard_sync_status: blocked`.

## Reviewer mapping

- Text field/document/local: store `Codey` exactly.
- Reviewer FK: resolve Codey through existing project identity data.
- Generic assignee-only schema: use Codey’s real ID only when the dashboard defines assignment as reviewer ownership and renders `Codey`.
- Keep tester/executor and reviewer separate.
- Never mark Codey as signatory without a real sign-off action.
- Never create or modify reviewer access as part of a run.

## Persistence proof

Dashboard/database proof requires:

1. mutation/transaction evidence;
2. read-back of the run and results;
3. rollups/counts matching local artifacts.

Local-only proof requires:

1. valid, re-readable `run.json`;
2. matching `manual-run.md` and result counts;
3. evidence paths that exist and contain no secrets.

Queued requests, HTTP acceptance without read-back, or a Markdown log without its promised structured record are not sufficient.
