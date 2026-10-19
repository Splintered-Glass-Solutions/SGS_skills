# Dashboard QA Adapter Checklist

Use this checklist to adapt the generic run model to a project-owned dashboard.
No table names, endpoints, staff IDs, fixture accounts or standing write authority
are shipped with the public skill.

## Resolve before writing

- Documented QA API or writer, authentication mechanism and exact environment.
- Catalog revision, active/retired check semantics and selected-scope snapshot.
- Parent run, attempts, evidence, defects, events and finalization schema.
- Real tester/reviewer identities, allowed unassigned state and sign-off policy.
- Disposable fixture bindings, cleanup, allowed mutations and external effects.
- Idempotency/version guards, evidence limits, readback and rollup behavior.

Confirm deployed contracts instead of assuming that a design document is live.
Resolve identities through existing mappings; never create staff, grants, roles,
RLS changes or schema migrations to make a run writable. Use local persistence
and report an exact blocker when the project writer or required reviewer is absent.

## Verify persistence

Create a scoped run only after authority and configuration are established.
Read back the run and selected scope. Append each check attempt and attach safe
evidence. Reconcile selected versus attempted checks, retain failures and retests,
verify latest-attempt rollups and preserve unresolved defects before finalizing.

A successful HTTP status alone is not persistence proof. Verify the stored IDs,
statuses, evidence relationships and visible dashboard result when required.
Reviewer assignment and passing tests do not constitute a human sign-off.
