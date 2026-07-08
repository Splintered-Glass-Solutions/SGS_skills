---
name: local-dev-consolidation
description: "Use when Preston wants local work across one or more repos, branches, or worktrees consolidated into a dev-ready state: inspect dirty working trees, identify merge conflicts and incomplete work, safely merge functional changes, run validation, deploy to the confirmed dev environment when explicitly requested, clean up local state, and report what shipped versus what remains. Trigger on phrases like consolidate local work, clean up working trees, merge everything to dev, deploy local work to dev, wrap this into dev, or get my local environment clean."
---

# Local Dev Consolidation

Use this skill when local work is spread across one repo, multiple branches, or multiple worktrees and the goal is to safely consolidate functional work into a dev-ready branch, validate it, optionally deploy it to dev, and leave the local environment clean enough to keep working.

## Operating Contract

Assume local inspection, consolidation, conflict resolution, and validation are allowed.

A request to use this skill is approval to inspect local git state, consolidate work locally, resolve conflicts, and run local validation. Pushing a branch or deploying to dev requires Preston to explicitly ask for dev deployment in the current conversation.

Do not push to production, merge to `main`, delete branches, delete worktrees, drop stashes, discard changes, mutate shared databases, or deploy to production unless Preston explicitly asks for that action in the current conversation.

If a change is incomplete, broken, unsafe, or product-ambiguous, do not force it into dev. Isolate it, document it, and explain what remains.

## Goal

Move functional local work into a single clean dev-ready path while preserving unfinished or unsafe work.

The end state should be:

- functional changes consolidated into one local branch or clearly identified repo branch;
- merge conflicts resolved;
- local validation run;
- dev deployment attempted only when explicitly requested and through the established dev process;
- dirty, unmerged, or incomplete work clearly accounted for;
- local cleanup completed only where safe;
- final report lists what shipped, what did not, and why.

## Workflow

1. Preflight scope.
   - Identify the active repo and likely related repos.
   - Run `pwd`, `git status --short --branch`, `git remote -v`, `git branch --show-current`, and `git worktree list`.
   - Inspect stashes and local branches when relevant.
   - Record repo path, current branch, upstream branch, dirty files, untracked files, active worktrees, stashes, branches ahead/behind, and likely deployment target.

2. Identify the dev target.
   - Determine the repo's dev integration path from existing conventions: `dev`, `develop`, `staging`, deployment docs, package scripts, CI/CD config, infra scripts, README, or runbooks.
   - If the dev deploy target is ambiguous or could affect production, ask one concise question.
   - Do not assume `main` is the dev target.

3. Inventory local work.
   - For each relevant branch, worktree, or repo, inspect `git status --short`, `git diff --stat`, `git diff --name-only`, and recent branch history.
   - Classify changes as functional, tests/docs/supporting, generated artifacts, unrelated local output, incomplete feature work, risky schema/data/permission changes, secrets, production-only changes, or unclear ownership.
   - Do not revert or delete anything during inventory.

4. Create a consolidation branch.
   - Create a consolidation branch from the correct dev base, such as `codex/dev-consolidation-YYYYMMDD`.
   - Fetch first when safe, then branch from the dev target.
   - If the current working tree is dirty, avoid commands that would overwrite it. Use a temporary preservation branch or worktree instead of stashing blindly.

5. Bring work together.
   - Merge or cherry-pick local branches/worktrees into the consolidation branch one unit at a time.
   - Prefer non-destructive operations such as `git merge --no-ff <branch>` or `git cherry-pick <commit>`.
   - Use file-level apply only when branch history is unusable.
   - After each unit, inspect conflicts, resolve deliberately, run the smallest relevant validation, and commit the resolved unit when the repo expects commits before deployment.

6. Exclude unsafe work.
   - Do not include broken generated output, local-only artifacts, secrets, logs, caches, temp files, unfinished experiments, code that fails focused validation, or migrations/data changes that require unapproved shared database mutation.
   - Preserve excluded work on its original branch/worktree and report it.

7. Resolve conflicts safely.
   - Read both sides of each conflict.
   - Preserve user intent where clear.
   - Prefer established repo patterns.
   - Avoid broad rewrites and blind ours/theirs resolutions.
   - Run focused tests for conflicted areas.
   - If a conflict reveals incompatible product direction or a risky schema/API contract change, pause and report it as a decision item unless the safe resolution is obvious.

8. Validate locally.
   - Run focused tests for touched modules first.
   - Run typecheck, build, lint, integration, or wider repo tests as supported.
   - Run browser/computer-use/e2e checks when UI, routing, or an end-user workflow changed.
   - Run migration/schema validation when schema changed, without applying to shared databases unless explicitly approved.
   - Use existing repo scripts first.
   - If a command fails because of unrelated pre-existing dirty work, prove the changed source subset passes if possible and report the unrelated blocker clearly.

9. Deploy to dev, only if explicitly requested.
   - Deploy only to the confirmed dev environment using the established repo process.
   - Before deployment, confirm branch, commit, environment name, and that no production target is involved.
   - Confirm required migrations/config are approved or safely dev-only.
   - After deployment, capture URL, deployment id, commit SHA, or build id.
   - Run health checks and smoke tests against dev.
   - If deployment fails, do not proceed to cleanup that would obscure the failure. Fix safe local issues and retry once when appropriate, otherwise report the blocker.

10. Clean up local state.
   - Only after validation, and dev deployment when requested, clean up safe artifacts.
   - Safe cleanup may include generated temp files created during this run, stopping local dev servers started by the run, and removing temporary consolidation worktrees created by the run.
   - Do not delete user-created branches, worktrees with unmerged work, stashes, untracked files not created by this run, unknown generated directories, or anything needed to recover excluded work.

11. Report the final state.
   - Separate completed work, validation, dev deployment, cleanup, excluded work, remaining dirty state, and production-readiness blockers.
   - Be explicit about anything not run and why.

## Safety Rules

- Never treat local-green as production-ready.
- Never deploy to production from this skill.
- Never merge to `main` unless Preston explicitly says to merge to `main`.
- Never drop work to make the tree look clean.
- Never apply database migrations to shared or cloud environments without explicit approval and confirmed target.
- Never include secrets, local env files, logs, caches, or large generated artifacts unless the repo explicitly tracks them.
- Never hide partial failure. If part of the consolidation worked and part did not, say exactly that.

## Standard Closing Shape

Use this structure:

```markdown
**Consolidation Result**
- Dev target:
- Branch:
- Deployment:
- Commit/SHA:

**Included**
- ...

**Excluded Or Deferred**
- ...

**Conflicts Resolved**
- ...

**Validation**
- ...

**Cleanup**
- ...

**Remaining State**
- ...

**Production Readiness**
- Local/dev status only. Production still requires ...
```
