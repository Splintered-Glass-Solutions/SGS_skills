# Prep Collapse Bulk Edits Agent Playbook

This is a platform-neutral version of the `prep-collapse-bulk-edits` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Prepare the current agent thread for safe collapse of bulk edits by auditing every requested change, finding unfinished work and broken fixes, repairing authorized feature defects, rerunning focused validation, completing the finish-line evidence, and producing a collapse-ready handoff. Use before $bulk-edits-thread or $collapse-bulk-edits-thread when a thread contains several edits, tests, migrations, branches, or worktrees that must be brought to one verified state.

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

# Prep Collapse Bulk Edits

Use this as the final preparation gate before collapsing a bulk-edits thread.
It combines feature finish-line validation, bounded hot-fix repair,
autonomous-build closeout, and bulk-edit reconciliation planning. The goal is
to get every task-owned item over its real finish line so the later collapse is
a mechanical reconciliation, not a discovery or repair session.

This skill prepares and proves collapse readiness. It does not collapse a
branch, merge into `dev`, delete a worktree, push, deploy, send messages, or
apply unrelated database changes. Run `$collapse-bulk-edits-thread` only after
this skill returns a ready status.

## Operating contract

- Treat the entire current thread as the scope ledger: initial request,
  corrections, annotations, delegated work, implementation, tests, migration
  notes, and prior blockers all count.
- Preserve unrelated dirty files, staged changes, untracked files, branches,
  worktrees, stashes, and user intent. Never reset, blanket-stash, checkout,
  or clean broadly to make the report look green.
- Prefer the latest accepted behavior and explicit user correction over stale
  plans or earlier assumptions.
- Separate local, committed, merged, hosted, database, provider, and
  customer-visible proof. A passing local test is not a deployed or provider
  acceptance claim.
- Default the acceptance boundary to the current local working tree and its
  local stack. Hosted Dev, deployed environments, hosted authenticated browser
  checks, and live provider calls are opt-in gates only when the current thread
  explicitly requests them or the acceptance criteria require them. Their
  absence or failure must not block local collapse preparation; record them as
  deferred external proof with an owner and next action.
- Do not hide a failing required test behind a broad unrelated failure, and do
  not treat an unrelated failure as a feature defect without evidence.
- Keep focused validation narrow. Reserve full-app/full-suite execution for an
  explicit `$full-suite-tests` request.

## Pairing and preparation

Read and apply the relevant skills before acting:

- `$feature-finish-line` for coverage ledgers, migrations, QA/QC records,
  documentation, and truth-surface reconciliation.
- `$hot-fix` for concrete hypothesis-first diagnosis and bounded repair loops.
- `$autonomous-feature-build` for accepted-state checkpoints, token-saving,
  scoped implementation authority, and end-to-end verification.
- `$bulk-edits-thread` and `$collapse-bulk-edits-thread` for batch manifests,
  overlap checks, dirty-`dev` preservation, and the later merge contract.
- `$test` for feature-scoped deterministic, integration, local-stack, and
  browser evidence.
- `$agent-safe-run` for one-shot/file-backed logs and process discipline.
- `$session-budget` for a compact checkpoint when the thread crosses repos,
  environments, auth, billing, migrations, or repeated failures.

When `$autonomous-feature-build` is used, invoke `$token-saver` first. Do not
delegate merely to restate the same evidence; use bounded parallel work only
when it reduces independent validation cost without overlapping edits.

## Phase 0 — Establish the closeout boundary

Classify the run as QA/review with authorized feature repair. Before mutation,
write a compact authority ledger containing:

- current repo, worktree, branch, baseline SHA, and target collapse branch;
- task-owned files, commits, generated artifacts, and predecessor batches;
- local code-edit authority and exact feature scope;
- remote database/project, permitted read or write operations, and migration
  authority;
- RLS, permissions, ownership, provider/OAuth, billing, messaging, and deploy
  authority;
- explicit exclusions: unrelated dirty work, destructive operations, broad
  rewrites, production/customer actions, push, deployment, and merge.

If the target branch, affected repository, feature scope, or authority is
materially ambiguous, stop with one decision item. Do not infer permission,
customer-data, billing, deployment, or destructive authority from credentials.

## Phase 1 — Inventory the whole thread

Build a closeout inventory from the conversation and repository evidence:

1. List every requested item, correction, acceptance criterion, bug,
   regression, and follow-up. Mark each `complete`, `incomplete`, `blocked`,
   `deferred`, or `out of scope` with evidence.
2. Inspect each affected repository's `git status --short --branch`, recent
   task commits, worktrees, branches, stashes, manifests, and conflict markers.
3. Identify the confirmed integration baseline and every active writable batch
   whose overlap zone intersects the work: shared routes, components, API
   contracts, migrations, generated clients, fixtures, or environment files.
4. Read existing finish-line reports, QA/QC records, test-run logs, batch
   manifests, run-state ledgers, and prior failure output. Search before opening
   large artifacts; keep only evidence needed for the next decision.
5. Inventory migrations, seeds, backfills, environment changes, provider
   setup, queues, billing, permissions, and generated files. A migration file
   or environment key is not proof it is applied or loaded.

Re-evaluate every prior blocker against the current acceptance boundary. A
stale hosted-Dev observation is not a local feature blocker unless hosted proof
was explicitly included in this thread's required acceptance criteria.

Stop before repair if the audit finds an unresolved semantic conflict between
two active batches, a destructive or unclear operation, an unapproved target,
or missing authority. Dirty work alone is expected and is not a blocker.

## Phase 2 — Build the issue-to-proof ledger

For every task-owned item, record:

| Item | Failure mode | Direct proof | Command/artifact | Status |
| --- | --- | --- | --- | --- |

Use exact test file paths, test names or grep patterns, migration IDs,
worktree/branch SHAs, browser URLs, database postconditions, and provider
fixture aliases. Each distinct symptom gets its own row; do not collapse
unrelated failures into “covered by e2e.” Include negative cases and relevant
tool calls, streaming, retries, auth, tenant isolation, credit/billing, and
responsive states.

Classify failures before editing:

- **Feature defect:** expected behavior is wrong or a task-owned assertion
  fails. Write one concrete root-cause hypothesis before changing code.
- **Test/harness defect:** the assertion or fixture cannot exercise the intended
  behavior. Repair the smallest harness boundary or mark the exact gap.
- **Generated/stale artifact:** local cache or generated output is invalid.
  Prefer a recoverable move/rebuild of the exact generated path; never edit
  generated output as source.
- **Environment/provider/auth blocker:** required external proof is unavailable
  or unsafe. Continue independent local work and report the boundary.
- **Unrelated regression:** outside task scope. Record it separately; do not
  repair it unless it blocks a required task-owned path.

## Phase 3 — Repair only what is authorized

For each required feature defect:

1. State the failure, evidence, and root-cause hypothesis.
2. Make the smallest task-owned fix; preserve accepted behavior and unrelated
   work.
3. Run the failing focused test and its direct integration boundary.
4. Re-run the relevant issue-to-proof rows and record the new result.

Use at most three bounded repair loops per failure family. After a repeated
failure, change the hypothesis or validation strategy; never blind-retry. Stop
for a user decision when a fix would change product direction, permissions,
RLS/ownership, billing, destructive data, deployment target, external
recipient, or accepted API behavior.

## Phase 4 — Execute the finish-line gates

Run the smallest practical sequence for every affected repository:

1. **Implementation completeness:** all requested items exist in the intended
   worktree and no task-owned fix is left half-applied.
2. **Focused behavioral QA:** unit/component/service/API/integration tests,
   tool-call and streaming contracts, type/lint/schema checks, and relevant
   local browser or integration flows.
3. **Local-stack proof:** when frontend/API behavior is involved, start exact
   worktrees on unique ports, verify health, process working directories,
   branch/SHA, frontend-to-API routing, and stop the processes afterward.
4. **Authenticated proof:** for local-only work, use a local-compatible
   harness or authenticated local browser session and keep hosted proof out of
   the required gate. Use Arc first for hosted authenticated UI only when the
   thread explicitly requests hosted/deployed acceptance; otherwise classify
   hosted checks as deferred external proof.
5. **Database gate:** inventory and inspect every required migration. Resolve
   the exact target, review compatibility and tenant safety, apply only
   authorized additive/forward-only feature operations, verify the remote
   ledger and live postcondition, and rerun affected checks. Never mutate an
   unclear target.
6. **QA/QC catalog:** create or update one atomic durable record per
   independently testable feature, bug, or regression using the repository's
   writer and fixture conventions. A catalog record is a specification, not
   pass evidence.
7. **Docs and handoff:** update the finish-line report, batch manifest, run
   ledger, changelog/release notes, and deferred-work list as applicable.
8. **Truth matrix:** mark local, committed, merged, hosted, shared database,
   provider-backed, authenticated UI, public, and customer-visible surfaces as
   `proved`, `blocked`, `not requested`, or `stale`. Hosted, deployed, and live
   provider rows are `not requested` or `deferred` by default when the current
   scope is local-only; they are not automatic blockers.

Do not run the full repository suite unless separately requested. If a broader
command was already run, preserve exact unrelated failures and do not relabel
them as feature proof.

## Phase 5 — Prepare the collapse packet

Create or update the existing batch manifest or QA/output artifact; do not
create duplicate ledgers when a canonical one exists. The collapse packet must
contain:

- batch ID, repositories, worktree paths, branches, baseline and current SHAs;
- requested items and explicit exclusions;
- task-owned commits and predecessor work intentionally included;
- overlap/conflict audit and protected unrelated dirty-file summary;
- issue-to-test coverage ledger with exact commands and results;
- repairs, hypotheses, retests, generated-artifact moves, and migration
  postconditions;
- QA/QC record IDs and import/deployment status;
- local/remote/hosted/provider/customer truth matrix;
- deferred work and why it is not required for collapse;
- exact next action: `$collapse-bulk-edits-thread` or a concrete blocker.

Before declaring ready, recheck `git status`, conflict markers, staged versus
unstaged boundaries, worktree ownership, and secret scans. Confirm every
requested task-owned item is either proved complete or explicitly blocked with
an owner/action. Only unresolved issues inside the declared acceptance
boundary make collapse unsafe; deferred hosted/deployed/provider proof does
not.

## Completion statuses

Return exactly one headline:

- `READY TO COLLAPSE` — all required task-owned work is complete, focused
  validation passes, migrations/data setup are verified or explicitly not
  applicable, and the packet is ready for the collapse skill.
- `READY TO COLLAPSE WITH NOTES` — collapse is safe, but clearly separated
  external proof (including hosted Dev or live provider checks) or unrelated
  regressions remain deferred and do not affect the task-owned reconciliation.
  Name every note.
- `BLOCKED — COLLAPSE NOT SAFE` — required work, validation, migration,
  conflict resolution, target authority, or semantic reconciliation remains
  unresolved. Give the exact blocker and smallest next safe action.

The skill must never claim a thread is ready merely because tests were not run,
the branch exists, the migration file exists, or the app returns HTTP 200.

## Final report

Report compactly but include:

1. Headline status.
2. Closeout inventory and inferred/explicit scope.
3. Authority ledger and protected unrelated work.
4. Worktree/branch/SHA and overlap audit for each repository.
5. Issue-to-test ledger and focused commands/results.
6. Defects, hypotheses, repairs, retests, and changed files.
7. Migration/database, QA/QC, provider, auth, and browser evidence.
8. Truth matrix separating local, committed, merged, hosted, provider, public,
   and customer-visible proof.
9. Collapse packet path and exact next action.

Never perform the collapse in this skill. Leave the current thread and
worktrees intact for `$collapse-bulk-edits-thread`.
