---
name: bonfire-page-autonomous-audit
description: Autonomously inventory, test, repair, and validate every feature and connected workflow of a named Bonfire page across Web, Bonfire_AI, Bonfire_ETL, database, infrastructure, and documentation. Use when Preston asks for a complete page audit, end-to-end functional QA, authenticated Bulverde Chapel testing, cross-repository repairs, or safe additive production database changes while keeping the existing thread working trees and branches unchanged.
---

# Bonfire Page Autonomous Audit

Audit a named Bonfire page as a complete product surface, not as a collection of isolated UI controls. Use `$autonomous-feature-build` for implementation discipline and finish only when every inventoried function has an evidence-backed status.

## Fixed operating context

- Use the existing working trees and branches assigned to the current thread.
- Do not create another branch or worktree.
- Do not switch, rename, rebase, reset, or delete a current branch.
- Inspect Git status before editing. Preserve and do not stage unrelated work or generated artifacts.
- Use existing corresponding working trees for Bonfire Web, Bonfire_AI, and Bonfire_ETL.
- Use the existing authenticated browser session for `preston@heybonfire.com` and the **Bulverde Chapel** organization when available.
- Never record or expose credentials, tokens, secret values, or private customer data.

If a required repository has no existing thread working tree, inspect its current normal checkout read-only and report the missing writable lane. Do not create a replacement working tree.

## Success bar

Produce and verify:

1. A complete feature and function inventory.
2. A cross-repository architecture and data-flow map.
3. Acceptance criteria and evidence for every inventory item.
4. Repairs for every reproducible defect within the authorized scope.
5. Regression coverage and affected-area validation.
6. Required database, ETL, API, infrastructure, and documentation changes.
7. A truth matrix separating local, CI, merged-dev, hosted-dev, production database, deployed production, and customer-visible proof.

Do not call the page fully operational while any inventoried function is untested, contradicted by evidence, or supported only by indirect proof.

## 1. Establish current state

1. Identify the page, route, organization, relevant records, and affected repositories.
2. Inspect the existing working trees, branches, HEAD SHAs, dirty files, active servers, and reusable browser session.
3. Confirm which database and hosted environments the local applications use.
4. Preserve a compact run ledger under the repository's normal ignored `output/` or `docs/qa/` convention.
5. Record authority boundaries and non-secret environment/provider presence only.

Do not start duplicate servers or browser sessions before inspecting existing ones.

## 2. Inventory the full page

Inventory every:

- control, form, field, button, menu, filter, tab, table, modal, and navigation path;
- loading, empty, disabled, validation, error, success, retry, and offline state;
- create, read, update, delete, persistence, refresh, concurrency, and lifecycle behavior;
- authentication, tenant isolation, capability, role, and permission boundary;
- API route, Session API call, ETL path, storage operation, queue, job, webhook, and provider interaction;
- desktop, tablet, mobile, keyboard, focus, overflow, and responsive behavior.

For each item, record:

- intended behavior;
- acceptance criteria;
- owning files and repositories;
- dependencies and state transitions;
- test method;
- status: operational, partially operational, broken, blocked, or unverified.

## 3. Trace end to end

Trace each behavior through all applicable layers:

```text
UI -> client state -> Web API/server action -> service/repository
   -> database/storage/queue -> Bonfire_AI or Bonfire_ETL
   -> provider/integration -> persisted result -> refreshed UI
```

Confirm identifiers, organization scoping, permissions, error propagation, retry behavior, and backward compatibility at each boundary. Do not assume a green frontend test proves API, provider, database, or hosted behavior.

## 4. Test systematically

Test the happy path plus meaningful:

- invalid and boundary inputs;
- loading, empty, partial, stale, and failure responses;
- unauthorized, wrong-organization, and insufficient-role behavior;
- refresh and durable persistence;
- retries, duplicate submission, concurrency, and terminal lifecycle;
- desktop, short viewport, tablet, and mobile geometry;
- cross-repository and provider failure modes.

Prefer deterministic unit/integration tests first, then mocked browser proof, then contained authenticated acceptance. Treat mocked browser checks as local proof only.

## 5. Diagnose and repair

Before editing a defect, state:

1. reproduction evidence;
2. concrete root-cause hypothesis;
3. proposed repair;
4. risks and affected surfaces;
5. test plan;
6. migration, configuration, provider, and deployment impact.

Make scoped changes in the existing working trees. Update every connected repository needed for the actual end state. Do not substitute a truthful placeholder, narrower behavior, or easier passing implementation for the page's stated functionality.

Add regression tests at the boundary where the defect escaped. Review all diffs centrally before accepting them.

## 6. Database and stateful changes

Safe, required work may include:

- additive backward-compatible production migrations;
- nullable columns, new tables, indexes, constraints, functions, or triggers;
- idempotent seeds and narrowly bounded backfills;
- corrective tenant-scoped Bulverde Chapel data updates;
- backward-compatible queue, storage, job, and integration setup;
- safe environment-variable additions that do not create persistent provider credentials.

Before any production database mutation:

1. Confirm the exact project, database, environment, organization, and migration target.
2. Run a read-only preflight and count affected rows without exposing sensitive values.
3. Verify compatibility with currently deployed Web, AI, and ETL versions.
4. Confirm tenant isolation, locking/runtime impact, idempotency, and rollback or forward-fix strategy.
5. Save the migration in the authoritative existing working tree.
6. Apply it exactly once.
7. Run post-migration validation and re-measure the affected state.
8. Record migration ID, target, row counts, proof, and recovery strategy in the run ledger.

Never run destructive database tests against a shared production-connected database. Do not delete or truncate production data, weaken tenant isolation, or change RLS, grants, roles, ownership, or billing under this skill. Do not create persistent OAuth clients, API keys, or service accounts.

## 7. Validation and finish line

Run the relevant subset of:

- focused regression tests;
- affected component, route, service, repository, AI, and ETL suites;
- type-check, lint, formatting, and diff checks;
- builds for affected bundles;
- browser checks and screenshots;
- migration validation, preflight, and postflight queries;
- Terraform or infrastructure validation;
- contained authenticated Bulverde Chapel acceptance.

Keep generated artifacts untracked unless the repository explicitly treats them as deliverables. Do not push, merge, deploy, or change the current branch unless the user separately requests it.

## Final report

Report:

- feature/function inventory;
- architecture and data-flow map;
- pass/fail/blocker matrix;
- issues and root causes;
- changes by existing working tree;
- tests, browser evidence, screenshots, API proof, and database validation;
- migrations, seeds, backfills, configuration, and infrastructure work;
- Git status separating intended and unrelated changes;
- remaining provider or deployment limitations;
- truth matrix for local, CI, merged-dev, hosted-dev, production database, deployed production, and customer-visible state.

Lead with what is operational, what was repaired, and what remains genuinely unproved.
