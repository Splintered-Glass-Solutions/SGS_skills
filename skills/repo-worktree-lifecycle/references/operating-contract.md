# Repository Worktree and Release Contract

Apply this contract to any Git repository. Repository instructions and the shared deploy registry remain authoritative for branch names, protection, providers, and release commands. This contract coordinates working copies; it does not expand user authorization.

## 1. Assign a checkout and owner

- For a continuing task, reuse its recorded worktree after checking its owner, branch, base SHA, HEAD, dirty state, and active commands.
- For independent parallel tasks, use a distinct task-owned worktree and branch per task and repository. A forked conversation that shares a directory is not an isolated writer lane. Never dispatch two writers into the same worktree; give each writable checkout one owner at a time.
- Within one build batch, reuse the batch worktree across items and workers sequentially. Do not create a new worktree for every worker or phase.
- Identify and record the canonical local development branch that future feature work should branch from, including its path/ref/SHA and its relationship to the mapped remote development release ref. Start new local feature branches from its verified current HEAD.
- Use a primary checkout only when it is clean, the task has exclusive write ownership, and repository guidance allows it. Never switch, reset, clean, or repurpose a dirty primary checkout to start a task.
- Never check out the same local branch in two worktrees. Use a unique task branch such as `codex/<scope>-<date>-<short-id>`; inspect existing refs before creating it.
- Before the first write, record in the task ledger or manifest: task/owner, repository path and remote, worktree path, branch, exact base ref/SHA, scoped files or overlap areas, current dirty/untracked state, and intended release lane. Keep the record updated when ownership or state changes.

## 2. Work in parallel safely

- Different worktrees isolate files, but they share Git objects and branch refs. Branch movement, deletion, cherry-picks, shared generated paths, symlinked dependencies, and external services can still connect lanes.
- Parallelize only when the work has distinct writers and no unresolved overlap in files, APIs, migrations, generated outputs, fixtures, or runtime services. If scopes overlap, serialize writes to that area or divide ownership at a clear interface.
- Keep reviewers on a stable SHA. Stop the writer and its commands before review; do not review a moving checkout or let a reviewer edit it.
- Record dependencies between parallel lanes by task/commit and integrate only the dependency needed. Do not copy or merge every nearby branch just because it exists.
- A dirty file in another worktree is not permission to overwrite it and is not by itself proof of a conflict. Compare the actual scoped changes and behavior before integrating.

## 3. Integrate through one clean lane

- Treat the repository's mapped remote release ref as the source of truth for releases. The canonical local development branch is the required base for future local feature work, not a second deploy authority.
- Integrate accepted, reviewed task commits one at a time into a clean integration worktree based on the freshly verified intended base. Record the integration SHA and test the integrated state, including affected merge boundaries.
- Assign one integrator to each integration worktree and shared release ref at a time. Parallel feature branches enter that queue one at a time; after each merge, recheck the target head and validate the resulting candidate before continuing.
- Do not merge into a stale, divergent, or dirty primary checkout. Preserve its staged, unstaged, untracked, and ignored content. Before declaring the feature or release closeout complete, reconcile accepted task commits and the current intended remote development baseline into the canonical local development branch, then validate that exact branch head. A separate integration worktree is useful proof but does not replace this final synchronization gate.
- If the canonical checkout is dirty, stale, divergent, or contains unclassified local commits, keep it unchanged and report canonical local synchronization as `pending` or `blocked` with the owner and exact next action. Do not declare full closeout or start the next feature from a stale base until it is safely reconciled. For a Dev deployment whose candidate is this branch, do not publish a substitute worktree or proceed to deployment while canonical synchronization is pending. Other independent authorized checks may continue.
- Never resolve conflicts by blindly choosing one side. Preserve compatible intent, validate the combined behavior, and stop only for a concrete unresolved ownership or product decision.
- Serialize operations that publish or move a shared release ref. Use the repository's required PR and checks; re-read the release ref before and after rollout to detect concurrent advancement.

## 4. Release from verified source

- Resolve the logical environment, mapped remote branch, exact provider identity, and repository release procedure before writes. A branch name or local build does not identify the environment.
- For a Dev release, use the validated canonical local development branch as the release candidate. After local integration checks pass, publish that candidate through the repository's normal protected path; then fetch and deploy the resulting mapped remote release SHA. Do not publish a parallel feature/integration branch as a substitute for canonical local Dev.
- Immediately before publishing, refresh the mapped remote Dev ref. If it advanced since the canonical candidate was tested, integrate that movement into canonical local Dev and rerun affected aggregate checks before publication. If this cannot be done safely, keep the release pending.
- Verify the accepted change is present in the mapped remote release ref. Publish via the normal protected path. Deploy only an artifact built from that verified remote revision, unless the repository has a documented exception.
- Keep the canonical local development SHA, task integration SHA, remote merge/release SHA, provider deployment revision, and feature-acceptance evidence as separate fields. Deployment must use the mapped remote release ref. A successful deploy does not imply canonical local synchronization or feature acceptance.
- If the remote release ref advances during rollout, prove the deployed artifact contains the new head or rebuild/redeploy from it before reporting alignment.

## 5. Close every lane

At each handoff and task close, classify every task-owned checkout as one of:

- `active`: a named owner and exact next action remain;
- `handed_off`: the next owner, task, path/SHA, and resume step are recorded;
- `integrated`: the accepted commits are reachable from the recorded integration/release ref and required proof is linked;
- `preserved`: unique unfinished work remains recoverable with its owner and resume plan;
- `removed`: safely archived or removed after verifying preservation and no other owner.

No task-owned checkout may be left unclassified. Before removal, verify the exact path and repository, all owners, Git operations/locks, dirty and untracked files, branch reachability, stashes, ignored files, and any active process. Preserve unique work before removing anything. Use the app's recoverable archive for app-managed worktrees or ordinary non-force Git removal for manual ones. Never force-remove, reset, blanket-clean, or delete another task's branch. Prune missing worktree registrations only for the scoped repository after reviewing a dry run.

When a task stops before integration, either leave the checkout `active`/`handed_off` with a concrete owner and next action, or preserve it as recoverable work with a resume plan. Do not mark it complete merely because a commit or remote branch exists.

## 6. Control disk growth

- Reuse task worktrees and dependencies when ownership and base remain valid. Do not keep duplicate checkouts after verified integration just for convenience.
- Before cleanup, distinguish Git's shared object storage from per-worktree costs such as dependencies, build output, caches, local databases, and logs. Measure allocated and reclaimable space when disk reduction is part of the request; APFS shared blocks mean folder size is not equal to net disk reclaimed.
- Remove only task-owned generated caches when they are safe to recreate. Do not share or symlink dependencies across projects/worktrees unless the repository's toolchain explicitly supports it.
- Report worktrees kept, archived, removed, pruned registrations, and measured space effects separately.

## 7. Handoff and closeout report

For each affected repository, report the primary checkout state; task worktree/branch/base/HEAD and owner; accepted commits and task integration SHA; canonical local development branch/path/SHA and synchronization result; mapped remote release ref and merged SHA; provider deployment revision and environment; validation and remaining gates; and each worktree's lifecycle state. State canonical local synchronization as `completed`, `pending`, `blocked`, or `not applicable` only when the repository has no established canonical local development branch, with path/ref/SHA and divergence when relevant. State explicitly whether the primary checkout was updated. Local synchronization is a required closeout gate when that branch is the expected base for future features; it is separate from the remote release and deployment gates. Never imply that “merged,” “deployed,” “tested,” or “cleaned up” proves the other states.
