# Bulk Auto Build Agent Playbook

This is a platform-neutral version of the `bulk-auto-build` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Autonomously implement every feature in a prepared bulk-edits thread, one feature at a time, including safe required migrations, finish-line hardening, three focused make-it-better polish passes, documentation, feature-scoped testing, local hot-fix loops, and a clean handoff ready for local collapse back into the integration branch. Use when a bulk-edits manifest or to-do list contains multiple accepted features and the user wants them built end to end without routine decision checkpoints.

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

# Bulk auto build

Run the accepted features in the current bulk-edits thread as a durable,
autonomous execution queue. Treat each stable feature ID in the batch manifest
as one unit of work and finish that unit before starting the next. Keep the
current bulk worktree and branch isolated until the batch is locally ready to
collapse; do not silently switch to another checkout.

## Operating contract

- Read the current bulk manifest, to-do list, acceptance criteria, exclusions,
  and predecessor notes before editing.
- Invoke `$token-saver` first, then use `$autonomous-feature-build` as the
  per-feature implementation orchestrator. Pair long or noisy work with
  `$orchestrator-mode` and `$agent-safe-run`.
- Create or resume one concrete goal and one compact execution ledger. Record
  the batch ID, feature ID, repo, worktree, branch, base SHA, current commit,
  migrations, tests, docs, blockers, and exact next action. Never record
  secrets.
- Work sequentially by feature ID unless two features have proven-disjoint
  files, tests, migrations, and runtime surfaces. When in doubt, serialize.
  Never let workers edit the same file concurrently.
- Make routine product and implementation decisions autonomously. Queue only
  decisions that would materially change accepted behavior, permissions/RLS,
  ownership, destructive data, billing, persistent access, external messages,
  or an ambiguous deployment target.
- Preserve unrelated dirty work. Never reset, clean, stash, overwrite, or
  delete user changes to make the batch easier to run.
- Do not push, merge, deploy, promote traffic, or collapse the worktree. The
  success state is locally verified and ready for a later collapse workflow.

## Feature execution loop

For each unfinished feature in the batch, execute this sequence and update the
ledger after every boundary:

### 1. Build the feature

Invoke `$autonomous-feature-build` for this feature only. Pass it the feature
ID, user-visible outcome, acceptance criteria, exact in-scope files, direct
integration boundaries, explicit exclusions, current worktree/branch, and the
compact return format:

- changed files and commits;
- decisions made and assumptions;
- migrations/env/provider operations inspected or performed;
- tests and browser checks run;
- evidence paths;
- failures and residual risk;
- exact next action.

Keep architecture, product interpretation, integration, and final review in
the main thread. Delegate only bounded research, coding, testing, browser,
docs, or log-reduction slices with non-overlapping ownership. Review every
delegated diff before accepting it.

### 2. Finish the feature and complete required data work

Invoke `$feature-finish-line` immediately after the implementation appears
complete. Use its full finish-line contract for:

- executable issue-to-test coverage;
- focused deterministic and browser coverage;
- QA/QC catalog records;
- documentation and release-artifact reconciliation;
- the mandatory database completion gate;
- local/merged/hosted/shared-data/provider truth separation.

For every migration, seed, backfill, environment update, or provider operation:

1. Inventory the exact operation and resolve the exact target.
2. Inspect the diff or payload for compatibility, locks, tenant isolation,
   auth/RLS/grants, deployed-code compatibility, and forward-fix/rollback path.
3. Apply only additive, bounded, non-destructive, feature-required operations
   covered by the active finish-line authority.
4. Verify the migration ledger and live post-condition, then rerun the
   affected feature checks.

Stop only the affected lane and report the exact operation when the target is
ambiguous or the change is destructive, ownership-changing, permission-
expanding, billing-related, or otherwise outside ordinary feature authority.
Continue independent features when safe.

### 3. Apply three focused polish passes

Invoke `$make-it-better` three times for the same feature, with a narrow brief
each time. Do not broaden the product or redesign unrelated surfaces.

1. **Layout, style, and animation:** improve hierarchy, density, spacing,
   visual consistency, responsive composition, transitions, motion restraint,
   and perceived polish.
2. **Usability and mobile:** improve discoverability, interaction states,
   touch targets, keyboard/focus behavior, error recovery, responsive/mobile
   layout, and accessibility.
3. **Copy, labels, and spacing:** improve terminology, labels, helper text,
   CTAs, feedback, truncation, capitalization, tone, and final spacing rhythm.

For each pass, inspect the feature diff and runtime, implement only
high-confidence in-scope improvements, reject generic or speculative ideas,
add direct tests for changed behavior, and rerun the smallest affected checks.
Record the selected improvements and rejected ideas in the ledger.

### 4. Reconcile documentation

Update the app documentation after polish, not only during finish-line. Cover
the user-visible behavior, setup/configuration changes, API or data-contract
changes, test commands, migration/runbook instructions, and known limitations.
Update shared documentation when the repository convention requires it. Do
not claim hosted or customer-visible behavior unless that proof exists.

### 5. Test the feature in the current worktree

Invoke `$test` with the exact current worktree, branch, feature ID, local URL,
and feature scope. Require the test skill's feature-scoped result and ledger.
Run direct deterministic checks before browser checks, and include responsive
and authenticated coverage when applicable. Do not substitute hosted evidence
for an explicit local-worktree request.

The minimum evidence for a user-facing feature is:

- direct behavioral tests for every acceptance criterion or reported issue;
- affected API/state/component integration tests;
- a local browser or equivalent user-workflow check;
- mobile/responsive checks when layout or interaction changed;
- type/lint/build checks when they catch a changed boundary.

Keep verbose logs file-backed. Report exact commands, counts, artifacts, and
failures rather than generic pass/fail statements.

### 6. Repair with a local hot-fix loop

If `$test`, finish-line review, polish review, or browser QA finds an issue,
invoke `$hot-fix` with the exact issue evidence and **local-only, no-deploy**
scope. Before each repair, state a concrete hypothesis; make the smallest
task-owned fix; add or update the regression test; and rerun the failed check
plus its affected integration boundary.

Repeat until the feature passes or the same blocker persists after three
meaningfully different repair attempts. Do not use this loop to deploy,
change accepted product direction, weaken a test, bypass auth, or modify
permissions/RLS/destructive data. Queue those decisions with evidence.

After a successful repair loop, rerun `$feature-finish-line`'s required
coverage reconciliation only where the fix changed the acceptance surface.

## Batch progression and completion

After each feature:

- mark its status `complete`, `blocked`, or `incomplete` in the ledger;
- record its commits, migrations and post-conditions, QA/QC records, docs,
  tests, browser artifacts, and remaining risks;
- confirm the worktree is still the named worktree and no unrelated files were
  altered;
- move to the next feature only when the current feature has a defensible
  local finish state.

At batch end, run one bounded aggregate check containing every feature test in
the ledger, inspect the complete diff, and verify:

- every accepted feature has a disposition;
- every required migration is applied and verified or explicitly blocked by a
  stricter gate;
- every feature has executable coverage and a durable QA/QC record;
- docs and test wiring are updated;
- no push, merge, deploy, provider mutation, or customer-visible claim was
  made without separate authorization and proof;
- the worktree is clean except for intentional batch changes and generated
  evidence artifacts;
- a later local collapse can identify the exact branch, commits, base SHA,
  changed files, and unresolved risks.

## Durable ledger

Prefer the batch manifest's existing state section. If it is not suitable,
create one task-scoped ledger under the repository's established ignored
`output/` or QA artifact path. Keep it compact and update it after:

1. feature selection;
2. implementation;
3. finish-line and migration verification;
4. each polish pass;
5. test execution;
6. each hot-fix loop;
7. batch closeout readiness.

Use this per-feature record:

```text
Feature ID / title:
Status:
Acceptance criteria:
Files and commits:
Decisions and assumptions:
Migration/env/provider operations:
Finish-line coverage and QA/QC record:
Polish pass 1 — layout/style/animation:
Polish pass 2 — usability/mobile:
Polish pass 3 — copy/labels/spacing:
Documentation:
Test commands and evidence:
Hot-fix loops:
Remaining risk or blocker:
Exact next action:
```

## Final handoff

Report compactly:

- batch ID, feature order, repo/worktree, branch, base SHA, and final SHA;
- each feature's completed/incomplete/blocked status;
- files and commits changed;
- migrations/data/env/provider operations inspected, applied, skipped, and
  verified;
- finish-line coverage and QA/QC catalog records;
- polish changes from all three passes;
- documentation and shared-docs status;
- `$test` commands, browser artifacts, counts, and remaining uncertainty;
- hot-fix loops and final proof;
- local truth, merged truth, hosted truth, shared-data/provider truth, and
  production/customer-visible truth as separate statuses;
- exact follow-up needed to collapse locally into the integration branch.

Do not call the batch deployed, merged, release-ready, or customer-visible
unless that separate proof actually exists.
