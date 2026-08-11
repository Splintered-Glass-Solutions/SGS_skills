---
name: collapse-bulk-edits-thread
description: >-
  Close out a completed bulk-edits task by auditing the full thread and its
  worktree for unfinished work, migrations, conflicts, and validation gaps;
  merging the completed branch into the local dev branch; verifying the result;
  and removing only the temporary worktree after successful reconciliation.
  Use when Preston says to collapse, close, wrap up, or merge back a bulk-edit
  thread or worktree, including coordinated work across multiple repositories.
---

# Collapse Bulk Edits Thread

## Operating contract

This is a local closeout workflow. The target is the repository's local `dev`
branch (or the explicitly confirmed local dev-equivalent), not a remote branch,
hosted deployment, `main`, or production. The temporary bulk-edit worktree and
branch are disposable only after all required work has been reconciled and
verified.

Treat several repositories as one coordinated closeout when the thread changed
more than one repo. Maintain a per-repository result and do not claim the batch
is closed while any affected repository remains unresolved.

## Phase 1: Audit before mutation

1. Read the full current Codex task, including the initial bulk-edit scope,
   subsequent edit requests, replies, test results, and closeout comments.
   Read each affected repository's committed Batch Manifest and treat its
   planned items, exclusions, commits, validation evidence, and blank
   closeout-integration-SHA field as the closeout checklist.
2. Build a closeout inventory for every affected repository:
   - bulk-edit worktree path and branch;
   - local `dev` worktree and branch;
   - commits, dirty files, untracked files, stashes, and conflict markers;
   - features requested versus features completed;
   - tests/checks run and their actual results;
   - migrations, schema changes, data changes, permission changes, generated
     artifacts, deployment/configuration work, and known follow-ups.
3. Compare the bulk-edit branch with the current local `dev` baseline and
   identify work that is already present, unique and complete, incomplete,
   risky, unrelated, or unclear.
4. Stop before merging or deleting anything if the audit finds unfinished
   requested work, unresolved conflicts, unapplied or ambiguous migrations,
   failing required validation, unclear cross-repo ordering, risky database or
   permission changes, or a dirty/untracked file with unclear ownership.
5. Report a concise **Closeout Audit** with the exact outstanding items,
   evidence, affected repo/worktree, and the decision needed. A clean audit is
   required before continuing.

## Phase 2: Reconcile into local dev

Only continue when the audit is clear or Preston explicitly resolves every
reported decision item.

1. Recheck mutable Git state immediately before merging. Fetch remotes only to
   refresh references; do not push or deploy.
2. Confirm the exact local `dev` target and record its pre-merge SHA. Never
   assume the current checkout is the target.
3. Preserve unrelated dirty work and user-created untracked files. Do not use
   destructive reset, blanket stash, `ours`, or `theirs` resolution.
4. For each affected repository, merge the bulk-edit branch into local `dev`
   one logical unit at a time, preserving both existing dev behavior and the
   completed bulk-edit behavior. Resolve conflicts by reading both sides and
   run focused validation after each conflict or logical unit.
5. For cross-repo features, follow the dependency order established by the
   thread and verify that contracts, migrations, generated clients, shared
   types, API routes, and UI consumers remain compatible. If the order or
   contract is unclear, stop and report it instead of guessing.
6. Run the strongest practical local checks for every touched repo: diff
   checks, focused tests, typecheck/lint/build, and relevant integration or
   browser checks. Validate migrations/schema syntax without applying changes
   to shared databases unless Preston separately authorizes that exact action.
7. Re-read the final local `dev` tree and verify that each requested completed
   item is present, no pre-existing dev feature was removed unintentionally,
   and no unresolved conflict markers or accidental generated/secrets files
   remain.
8. Update the committed Batch Manifest with the pre-recording local `dev`
   integration SHA, closeout validation, and any deferred work. Commit that
   closeout record on local `dev` before considering temporary-worktree
   cleanup, and report the resulting final local `dev` SHA separately.

## Phase 3: Remove the temporary worktree

Remove the temporary bulk-edit worktree and its branch only after all of the
following are proven for that repository:

- the completed work is reachable from local `dev`;
- the final local `dev` SHA and status are recorded;
- focused and required broad validation passed or every skipped check is named;
- no unresolved merge, migration, conflict, or follow-up item remains;
- excluded work is preserved on its original branch/worktree;
- the worktree being removed is not the active checkout and contains no
  unaccounted user changes;
- the branch is fully merged into local `dev` and is safe to delete normally.

Use recoverable, explicit Git cleanup. Remove only the named temporary
worktree created for this bulk-edit task and delete only its fully merged local
branch with a non-force delete. Do not delete stashes, safety branches,
untracked user files, other active worktrees, or branches belonging to another
bulk-edit thread. If cleanup is not safe, leave it in place and report it.

## Boundaries

- Local only by default: no push, PR, hosted deployment, remote branch update,
  `main` merge, production action, or shared-database mutation.
- Never hide incomplete work to produce a clean report.
- Never claim the task is closed based only on branch ancestry; prove final
  content, validation, and readback from local `dev`.
- If one repository succeeds and another is blocked, report the split result;
  do not remove the blocked repository's worktree or call the coordinated
  closeout complete.
- Do not create a new Codex task or alter unrelated threads.

## Completion report

Lead with `CLOSED LOCALLY`, `CLOSED LOCALLY WITH NOTES`, or `BLOCKED`.

For each repository, report:

- repo path;
- bulk-edit worktree/branch and pre-merge SHA;
- local `dev` target and final SHA;
- included work and proof it is present;
- deferred/excluded work and where it remains;
- conflicts or migrations reviewed;
- validation commands and results;
- cleanup performed or explicitly retained, with reason;
- deployment status: not performed.

For a multi-repo batch, finish with the batch verdict and a clear list of any
remaining follow-ups. State explicitly whether all temporary worktrees were
closed and whether local `dev` is the verified continuation point.
