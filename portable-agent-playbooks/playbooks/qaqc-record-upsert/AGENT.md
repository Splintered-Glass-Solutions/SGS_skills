# Qaqc Record Upsert Agent Playbook

This is a platform-neutral version of the `qaqc-record-upsert` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Create or update durable QA/QC feature and functionality specification records. Use when the user asks to add, register, revise, sync, or backfill a QA/QC record for a feature, bug fix, regression, page, interface, API route, MCP tool, ETL job, or release; when a finish-line workflow needs to tell QA what to test and what success looks like; or when duplicate QA records need reconciliation.

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

# QA/QC Record Upsert

Create or update atomic, executable QA specifications without confusing the specification with an environment test result.

## Operating contract

- Always leave a durable local source-of-truth record or import-ready pending record.
- Create one record per independently testable behavior. Split unrelated fixes.
- Update the matching behavior instead of creating a duplicate.
- Never store secrets, raw credentials, customer-sensitive prompts, or environment-specific database IDs.
- Preserve unrelated dirty work and edit the smallest possible catalog surface.
- Do not claim that a feature passed merely because its specification was written.
- Treat a shared database sync as a separate external mutation. Use it only when exact existing approval names the target and operation.

For Bonfire work, read [references/bonfire-catalog.md](references/bonfire-catalog.md) completely before editing or syncing a record.

## Workflow

### 1. Inventory the behaviors

Read the feature request, bug report, implementation diff, tests, finish-line ledger, release artifact, and relevant source files.

List every independently executable behavior. For each one, capture:

- original failure or user need;
- exact product surface;
- expected behavior and neighboring state that must not change;
- required account, organization, agent, KB, prompt, provider sandbox, device, or seeded data;
- source evidence and executable regression tests.
- the best evidence-backed date the product behavior first became available, when the project catalog supports introduction dates.

Do not collapse several bugs into one generic record.

### 2. Locate the catalog and existing record

Find the project catalog contract, local JSONL/CSV/seed source, generator, migration, and database target. Search with `rg` by:

1. stable `coverage_key`;
2. exact interface, method/route, tool, job, or schedule;
3. feature/function and issue wording;
4. source and test paths.

Inspect any matching record before deciding to create or update.

### 3. Choose the disposition

- `created`: no equivalent behavior exists.
- `updated`: the same behavior exists but its steps, criteria, fixtures, scope, or source evidence changed.
- `unchanged`: the existing record already describes the behavior accurately and completely.
- `pending import`: the local record is ready but approved database synchronization is unavailable.

Match by stable product behavior, not PR, commit, release, date, or environment. Preserve the existing `check_id` on update. Use the project's ID convention for a new row and prove uniqueness.

Treat an introduction date as product history, not record metadata: prefer an explicit release date, then implementation-source introduction evidence. Do not replace it with today's date when updating an existing record unless better evidence corrects the estimate.

If a `coverage_key` collision describes a materially different behavior, stop and repair the identity conflict rather than overwriting it.

### 4. Write an executable specification

Make the record runnable by QA without implementation knowledge.

- Name the exact page, interface, route/method, MCP tool, ETL job, schedule, or workload.
- Use portable fixture aliases and `NONE` for non-applicable fixture categories.
- State flags, roles, seeded state, safe target, and cleanup requirements.
- Include a bounded happy path, persistence/idempotency check, and the nearest meaningful negative, disabled, unauthorized, empty, retry, mobile, or failure case.
- For bug fixes, recreate the original failure condition and assert the exact adjacent data or UI state that must remain unchanged.
- Define observable terminal success. HTTP acceptance, enqueueing, or a rendered shell alone is not success for downstream work.
- Mark unresolved fixture mapping or product intent explicitly instead of inventing it.

### 5. Upsert the local source

Use `apply_patch` for the atomic source edit. Do not rewrite or reorder an entire dirty catalog.

When no project catalog exists, create `output/qa/<feature-slug>-qaqc-record.json` and report the missing central-catalog mapping as a blocker.

If the change affects several atomic records, report the disposition of each.

### 6. Validate

Run the project's validation or generator when available. At minimum prove:

- valid serialization and all required fields;
- controlled vocabulary compliance;
- unique `check_id` and correct `coverage_key` identity;
- valid source references;
- portable fixtures and meaningful success criteria;
- no secrets or live credentials;
- deterministic output after a second run or re-read.

Do not hide pre-existing validator failures. Separate new-record validation from unrelated repository failures.

### 7. Synchronize only when authorized

Before any database write, inspect the exact project/schema/table, current matching row, catalog version/checksum, upsert payload, revision behavior, and access implications.

- Shared Dev/production data is production-connected.
- Skill invocation authorizes local catalog work, not a shared database write.
- Reuse a still-valid exact approval only when it names the same target and operation.
- Never alter grants, roles, ownership, RLS, policies, or object permissions without separate exact approval.
- When authorized, use an idempotent upsert and verify the stored row/checksum without printing secrets.
- Otherwise stop the external lane at `pending import` while completing local work.

Database storage still does not prove an environment passed. Store executions, notes, screenshots, defects, cleanup, and statuses in the QA session/result workflow.

## Required handoff

Report:

- feature or bug behavior;
- disposition;
- `check_id` and `coverage_key`;
- local catalog file;
- database target and sync status;
- fixtures, steps, and success criteria added or changed;
- validation commands and results;
- remaining fixture, product-intent, access, or import blockers.
