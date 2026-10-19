# Project QA Catalog Write Adapter

Use the project’s existing schema and writer; no publisher database is assumed.

1. Resolve catalog sources, storage target, schema and permitted writer from
   project-owned documentation. Discover the stable identity for each behavior.
2. Search for existing records before adding one. Preserve IDs and history.
3. Capture surface, prerequisites, input, steps, observable success, safety scope,
   source/test evidence and readiness using the project’s vocabulary.
4. Validate serialization, required fields, unique identity and source references.
5. Write local specifications atomically without overwriting unrelated work.
6. Synchronize remotely only with exact current task authority, version guards
   and readback. Do not alter schemas, roles or permissions as a catalog upsert.
7. Otherwise retain a pending-import artifact and report the precise blocker.

Catalog records define tests; they do not establish an environment passed.
Keep pass/fail attempts in the project’s separate QA run store.
