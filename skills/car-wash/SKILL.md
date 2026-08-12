---
name: car-wash
description: "Clean up local git state after large builds, merges, PRs, or multi-worktree work. Use when the user asks for a car wash, repo cleanup, branch consolidation, local git reset/baseline cleanup, stale branch cleanup, or to make a project ready to continue building from the right local development branch."
---

# Car Wash

Use this skill when the user wants a repo's local git state consolidated, cleaned up, and ready for more work.

## Operating Contract

This is a local git hygiene workflow. Do not assume pushing, PR work, deployment, production promotion, or destructive cleanup is allowed.

Allowed by default:

- Inspect branches, remotes, commits, worktrees, stashes, tags, and dirty files.
- Fetch remotes when network/auth allows.
- Create safety branches or named stashes to preserve work.
- Merge local feature branches into the chosen local integration branch.
- Delete only local branches that are fully merged into the integration branch, not checked out in any worktree, and removable with `git branch -d`.

Require explicit current-thread approval before:

- Pushing to any remote branch.
- Opening, merging, or updating PRs.
- Promoting between shared branches such as `dev` -> `main`, `develop` -> `main`, `staging` -> `prod`, or any production/default-branch path.
- Running `git reset --hard`, `git clean -fd`, `git branch -D`, `git stash drop`, deleting worktree directories, or pruning local work.
- Rewriting history with rebase, amend, filter-branch, or force push.

Never revert unrelated user changes. If dirty files block branch movement, preserve them first and report the preservation mechanism.

## Choose The Integration Branch

Infer the local branch the user should keep building from:

1. If the prompt names a branch, use that branch.
2. Else prefer an existing local `dev` branch when the repo has one.
3. Else prefer an existing local `develop` branch.
4. Else use the remote default branch from `origin/HEAD` when it is clearly set.
5. Else use the current branch if it is clean and appears to be the active integration branch.
6. If still ambiguous, stop and ask which branch should be the consolidation target.

Do not silently reset the integration branch to its remote. Local commits may be real work.

## Workflow

1. Identify the repo and branch shape.
   - Run `git rev-parse --show-toplevel`.
   - Run `git status --short --branch`.
   - Run `git branch --show-current`.
   - Run `git worktree list --porcelain`.
   - Run `git branch -vv`.
   - Run `git remote -v`.
   - Run `git symbolic-ref --short refs/remotes/origin/HEAD` if `origin` exists.

2. Refresh remote truth if possible.
   - Run `git fetch --all --prune`.
   - If fetch fails because of network, DNS, auth, or lock issues, continue from local refs and say the audit is based on locally available refs.

3. Establish the integration baseline.
   - Confirm the target branch exists locally, or create it from the matching remote tracking branch if the local branch is missing.
   - Compare the target branch with its upstream when one exists:
     - `git rev-list --left-right --count TARGET...UPSTREAM`
     - `git merge-base --is-ancestor UPSTREAM TARGET`
     - `git merge-base --is-ancestor TARGET UPSTREAM`
   - If the target branch and upstream diverged, merge the upstream into the local target only when that is safe and expected for the repo. Otherwise report the divergence.

4. Preserve dirty work before moving branches.
   - If any worktree is dirty, inspect `git diff --stat`, `git diff --cached --stat`, and untracked paths.
   - If changes appear task-related and should move to the target branch, keep them in place or commit them only when the user asked for a commit.
   - If changes are unrelated or branch switching is needed, use a named stash such as `git stash push -u -m "car-wash YYYY-MM-DD preserve before branch consolidation"`.
   - Do not drop the stash during cleanup unless explicitly approved.

5. Classify every local branch.
   - For each local branch, determine:
     - Is it checked out in another worktree?
     - Is it already merged into the target branch?
     - Is the target branch an ancestor of it, meaning it has unique work?
     - Does it have an upstream, and is it ahead/behind that upstream?
   - Useful commands:
     - `git for-each-ref --format='%(refname:short) %(upstream:short)' refs/heads`
     - `git merge-base --is-ancestor BRANCH TARGET`
     - `git merge-base --is-ancestor TARGET BRANCH`
     - `git log --oneline --decorate --left-right TARGET...BRANCH`
     - `git cherry -v TARGET BRANCH`
   - Treat branches in other worktrees as active until proven otherwise.

6. Consolidate unique local work into the target branch.
   - Switch to the target branch only after dirty work is preserved.
   - If the upstream has commits missing locally, merge the upstream first unless that would cross a promotion boundary.
   - Merge one branch at a time into the target branch using normal merges, not rebases.
   - Prefer `git merge --no-ff BRANCH` for meaningful unique work, so branch provenance remains visible.
   - If a branch is purely ahead by one small local commit and linear history is clearly safe, a fast-forward is acceptable.
   - Resolve conflicts by reading the conflicted code path and preserving intended behavior from both sides. Do not choose ours/theirs blindly.
   - If a branch appears stale, superseded, too large, or conflicts with current target behavior, leave it unmerged and explain why.

7. Validate the consolidated target branch.
   - At minimum run `git diff --check`.
   - Run repo-appropriate validation for touched areas: typecheck, lint, unit tests, integration tests, build, schema checks, or existing project scripts.
   - Prefer the repo's own package manager and scripts over inventing commands.
   - If validation is too expensive or blocked, run the highest-signal smaller checks and report what remains.

8. Clean safe local branch noise.
   - Re-run `git branch -vv` and `git worktree list --porcelain`.
   - Delete local branches only when:
     - `git merge-base --is-ancestor BRANCH TARGET` succeeds.
     - The branch is not the target branch, the default branch, the current branch, or an obvious backup/safety branch.
     - The branch is not checked out in any worktree.
     - `git branch -d BRANCH` succeeds without force.
   - Do not remove worktrees, stashes, untracked files, ignored files, caches, or generated artifacts unless the user explicitly approves that exact cleanup.

9. Finish on the target branch.
   - Leave the active checkout on the target branch unless another branch is required for safety.
   - Final proof should include:
     - Current branch and `git status --short --branch`.
     - Target branch ahead/behind versus upstream.
     - Whether the target tree differs from upstream.
     - Branches merged into the target.
     - Branches deleted.
     - Branches left alone and why.
     - Stashes or safety branches created.
     - Tests/checks run and failures or blockers.

## Output Style

Lead with the verdict:

- `CLEAN`: the target branch contains the consolidated work, checkout is tidy, and validation passed or has only explicitly named skipped checks.
- `CONSOLIDATED WITH NOTES`: the target branch contains the safe work, but there are retained stashes, active worktrees, unpushed local commits, skipped checks, or nonblocking branch leftovers.
- `BLOCKED`: consolidation could not safely finish because of conflicts, missing target branch, ambiguous dirty work, failed validation, or permission/network limits.

Keep the summary concrete. Separate local-only state, remote divergence, and promotion/deployment status. Do not imply anything has shipped unless a push/deploy actually happened.
