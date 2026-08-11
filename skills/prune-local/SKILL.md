---
name: prune-local
description: >-
  Audit and safely prune local Git worktrees and branches across one or more
  related repositories. Use when Preston says prune local, prune everything,
  clean up old worktrees, or asks which branches still need a bulk-edit
  collapse. Verify each branch against its repository's local dev target,
  report unresolved work, cross-repo gaps, and collapse recommendations, then
  remove only fully integrated and safely disposable local leftovers.
---

# Prune Local Work

## Operating contract

This is a local-only cleanup and reconciliation audit. Never push, delete a
remote branch, deploy, merge to `main`, touch production, or mutate a shared
database. The default scope is the current repository plus clearly related
repositories discovered from the current task, shared feature paths, or
explicit user scope; do not scan or delete arbitrary unrelated repositories.

Use the repository's confirmed local `dev` branch as the comparison target. If
the target is ambiguous, stop that repository and report the ambiguity. A
branch being old, named like a feature, or merged by ancestry alone is not
enough to delete it.

## Workflow

1. Establish scope and a timestamp. Record every repository in scope and the
   local dev target that will be used for that repo.
2. Refresh local Git references when safe, then inventory each repo with:
   - current branch and dirty state;
   - all worktrees and their paths;
   - local branches, upstreams, ahead/behind counts, and recent commits;
   - untracked files, stashes, conflict markers, and detached worktrees;
   - branches checked out elsewhere or belonging to another active task.
3. For every non-target branch/worktree, compare both history and content with
   local `dev`. Inspect unique commits and diffs; do not rely on branch names or
   merge-base status alone.
4. Classify each unit as:
   - **CLEANUP ELIGIBLE**: all intended work is present in local `dev`, no
     unique or unaccounted changes remain, the worktree is not active, and safe
     non-force cleanup is possible;
   - **COLLAPSE RECOMMENDED**: it appears to be a completed or nearly completed
     bulk-edit worktree/branch whose work is not yet reconciled; point to
     `$collapse-bulk-edits-thread` and list the evidence;
   - **OUTSTANDING**: unique commits, dirty files, untracked work, migrations,
     conflicts, failed checks, or incomplete requests remain;
   - **QUARANTINED**: ownership, repo target, detached history, upstream, or
     worktree purpose is unclear. Preserve it and ask for direction.
5. For cross-repo functionality, group related branches by feature and verify
   that each repo's local dev contains the compatible implementation. Check
   shared API contracts, types, migrations, generated clients, configuration,
   and consumer/provider version alignment. If one repo is integrated and
   another is not, do not prune either side; report the cross-repo gap and
   recommend collapse on the unresolved bulk-edit task.
6. Produce the audit report before cleanup. Include exact repo paths, branch
   names, worktree paths, SHAs, unique files/commits, and the reason for every
   classification. If any item is outstanding or ambiguous, report it clearly
   and continue cleaning only independently proven eligible items.
7. Recheck cleanup candidates immediately before mutation. Remove only named
   temporary worktrees that are not active, contain no unaccounted changes,
   and are fully represented in local `dev`. Delete only their fully merged
   local branches with `git branch -d`; never use force deletion.
8. Preserve all excluded branches, worktrees, stashes, untracked files, safety
   branches, and unknown artifacts. Do not silently stash, reset, clean, prune,
   or discard anything outside the explicitly verified cleanup candidates.
9. Re-run the inventory and verify that every cleanup action succeeded and that
   local `dev` still contains the work that justified the cleanup. Report any
   cleanup failure without retrying destructively.

## Safety gates

- Do not remove a worktree that is the current checkout or active in another
  task.
- Do not remove a branch with unique commits, dirty files, untracked files,
  unresolved conflicts, an active stash linkage, or unclear ownership.
- Do not treat an unapplied migration, schema/permission change, or data change
  as safely integrated merely because its source file exists in `dev`.
- Do not apply migrations to prove integration. Validate syntax and report the
  required target/action instead.
- If a branch likely needs implementation work, use the collapse recommendation
  rather than pruning it.
- If cleanup spans multiple repos, report a per-repo result and a batch result;
  one unresolved repo prevents a claim that the related feature is fully clean.

## Completion report

Lead with `PRUNED LOCALLY`, `PRUNED LOCALLY WITH OUTSTANDING WORK`, or
`BLOCKED`.

Use this shape:

```markdown
**Prune Result**
- Scope:
- Observed at:
- Local dev targets:

**Cleanup Eligible**
- Repo / branch / worktree / SHA / cleanup performed

**Collapse Recommended**
- Repo / branch / worktree / evidence / next skill

**Outstanding Or Quarantined**
- Repo / branch / worktree / exact unresolved work / preservation location

**Cross-Repo Checks**
- Feature / repos / compatibility result / remaining gap

**Verification**
- Final local dev branches and status:
- Cleanup actions confirmed:
- Remote/deployment status: not performed
```

Always state whether any branches or worktrees remain intentionally preserved
and why.
