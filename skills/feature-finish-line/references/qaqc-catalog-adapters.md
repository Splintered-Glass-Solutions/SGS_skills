# QA/QC Catalog Adapters

Read this file completely when `$qaqc-record-upsert` is unavailable.

## Contents

- Required outcome
- Catalog discovery
- Logical record model
- Existing catalog adapter
- Local-only adapter
- Validation and database boundary

## Required outcome

Every finish-line invocation must leave one durable QA specification per independently testable feature, bug fix, acceptance criterion, or regression changed by the work.

- Create a record when no equivalent behavior exists.
- Update the existing record when the same behavior changed.
- Keep the record unchanged when it already describes the finished behavior accurately.
- Split unrelated behaviors into separate records.
- Do not store environment pass/fail results in a reusable specification record.

## Catalog discovery

Locate project-owned QA contracts, JSONL/JSON/YAML/CSV sources, spreadsheets, seed files, generators, migrations, dashboard APIs, or database tables. Search by stable behavior identity, exact surface, issue wording, source path, and existing test name.

Prefer the project’s schema, controlled vocabulary, writer, and validation commands. Do not impose another project’s fields or fixture model.

## Logical record model

Preserve these concepts even when field names differ:

- stable record/check identity;
- project/system/component ownership;
- exact page, interface, route/method, tool, job, schedule, or workload;
- one feature/function or regression behavior;
- prerequisites and portable fixture roles;
- deterministic prompt/input when applicable;
- executable steps including the original regression condition;
- observable success criteria and neighboring state that must remain unchanged;
- environment scope and safety/risk classification;
- implementation/test/source evidence;
- readiness, fixture-mapping, or product-intent status.

Use `NONE`, null, or field omission according to the project contract when a fixture type is not applicable. Never invent Bonfire-style account, organization, agent, or KB fields in projects that do not use them.

## Existing catalog adapter

1. Match the existing behavior by its stable key/identity.
2. Preserve its record ID when updating.
3. Use the project’s ID convention for a new record and prove uniqueness.
4. Make the smallest atomic local source edit.
5. Preserve historical scope and avoid rewriting/reordering unrelated dirty records.
6. Report `created`, `updated`, `unchanged`, or `pending import`.

If an identity collision describes a materially different behavior, repair the collision rather than overwriting it.

## Local-only adapter

When no central catalog exists, create:

`output/qa/<feature-slug>-qaqc-record.json`

Use a stable, self-describing JSON object containing the logical record model above. Add it to the finish-line handoff and state whether a future central-catalog import is needed. Local-only persistence is valid when the project intentionally has no dashboard/database catalog; it is a blocker only when the project expects central storage.

## Validation and database boundary

At minimum validate serialization, required project fields, unique/stable identity, controlled values, source references, executable steps, observable success criteria, and absence of secrets.

A local catalog write is required. Database/dashboard synchronization is separate:

- verify the exact target, schema, current record, version/checksum, writer, and read-back path;
- use an already-valid exact approval only for the same target and operation;
- never change permissions, grants, roles, ownership, RLS, policies, or reviewer/staff access as part of a record upsert;
- when authorized, perform an idempotent upsert and verify the stored record;
- otherwise preserve a validated pending-import artifact.

Database storage does not prove the behavior passed. Environment runs belong in the project’s QA run/session result workflow.
