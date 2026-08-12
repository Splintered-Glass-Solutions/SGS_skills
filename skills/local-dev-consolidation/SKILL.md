---
name: local-dev-consolidation
description: "Consolidate work across local repos, branches, or worktrees into a clean local branch based on the confirmed dev baseline, resolve conflicts, validate locally, and prepare a local-testing handoff. This skill is local-only by default: it does not push or deploy unless the user separately and explicitly requests deployment to dev. Trigger on consolidate local work, clean up working trees, merge everything into a local dev branch, wrap this into a dev-ready branch, or get my local environment clean."
---

# Local Dev Consolidation

Use this skill when local work is spread across one repo, multiple branches, or multiple worktrees and the goal is to safely consolidate functional work into a local dev-ready branch, validate it, and hand it off for local testing.

## Operating Contract

Default to `local_only` mode. Assume local inspection, consolidation, conflict resolution, commits on the isolated consolidation branch, and local validation are allowed.

A bare invocation of this skill never authorizes a push or deployment. Interpret phrases such as “merge everything to dev,” “wrap this into dev,” or “consolidate into dev” as: create or update an isolated local integration branch from the confirmed dev baseline. Do not interpret them as permission to update the remote `dev` branch or deploy a hosted dev environment.

If the user asks to plan, audit, assess, outline, or prepare consolidation rather
than execute it, enter `planning_only` mode. In that mode do not fetch, create a
branch/worktree, merge, cherry-pick, apply/drop a stash, prune, clean, deploy, or
otherwise mutate Git. Return the registry, baseline recommendation, risks,
validation plan, and exact approval needed to execute.

A request to use this skill is approval to inspect local git state, consolidate work locally, resolve conflicts, and run local validation. Pushing a branch or deploying to dev requires a separate, explicit request from the user. Prefer receiving that approval after reporting the local branch and local test results.

Do not push to production, merge to `main`, delete branches, delete worktrees, drop stashes, discard changes, mutate shared databases, or deploy to production unless the user explicitly asks for that action in the current conversation.

If a change is incomplete, broken, unsafe, or product-ambiguous, do not force it into dev. Isolate it, document it, and explain what remains.

## Goal

Move functional local work into a single clean local dev-ready path while preserving unfinished or unsafe work.

The end state should be:

- functional changes consolidated into one isolated local branch based on the confirmed dev baseline, or one clearly identified local branch per repo;
- merge conflicts resolved;
- local validation run;
- local testing instructions and exact worktree/branch/SHA provided;
- hosted dev remains unchanged unless the user separately requests deployment;
- when deployment is requested, it occurs only after the local result is available for testing and through the established dev process;
- dirty, unmerged, or incomplete work clearly accounted for;
- local cleanup completed only where safe;
- final report lists what shipped, what did not, and why.

## Workflow

1. Preflight scope.
   - Identify the active repo and likely related repos.
   - Run `pwd`, `git status --short --branch`, `git remote -v`, `git branch --show-current`, and `git worktree list`.
   - Inspect stashes and local branches when relevant.
   - Record repo path, current branch, upstream branch, dirty files, untracked files, active worktrees, stashes, branches ahead/behind, and likely deployment target.
   - Record `run_mode` as `planning_only` or `execute_consolidation` and an
     `observed_at` timestamp. If remote refs were not freshly fetched, label
     every remote-derived SHA provisional.

2. Identify the dev target.
   - Determine the repo's dev integration path from existing conventions: `dev`, `develop`, `staging`, deployment docs, package scripts, CI/CD config, infra scripts, README, or runbooks.
   - If the dev deploy target is ambiguous or could affect production, ask one concise question.
   - Do not assume `main` is the dev target.
   - Treat the confirmed dev ref as the local branch baseline, not as deployment authorization.
   - Choose the baseline by evidence, not checkout proximity: prefer the
     repository's confirmed remote dev integration ref, then a freshly verified
     local dev ref, and never default to a dirty current HEAD. Record the exact
     baseline ref and SHA.

3. Inventory local work.
   - For each relevant branch, worktree, or repo, inspect `git status --short`, `git diff --stat`, `git diff --name-only`, and recent branch history.
   - Classify changes as functional, tests/docs/supporting, generated artifacts, unrelated local output, incomplete feature work, risky schema/data/permission changes, secrets, production-only changes, or unclear ownership.
   - Do not revert or delete anything during inventory.
   - Create a machine-readable registry when more than five branches/worktrees
     are in scope. Required fields: batch ID/marker, work ID, task/thread ID,
     repo, worktree path, branch, HEAD SHA, last commit, upstream and state,
     baseline divergence, detached flag, dirty/untracked/conflict counts, stash
     linkage, owner, intent, target lane, risk class, overlap zone, validation
     artifact, closeout artifact, inclusion decision, and last observed time.
   - Treat detached worktrees, gone/missing upstreams, duplicate HEADs,
     production-only branches, and unknown historical temp paths as quarantine
     candidates, not deletion candidates.
   - Distinguish source/tests/docs from migrations, screenshots, reports,
     generated output, caches, env files, secrets, and local runtime artifacts.

4. Establish batch identity when work came from a coordinated project sprawl.
   - Preserve the plan's ASCII batch ID and human-facing numerical emoji.
   - Emoji may appear in reports and task titles, never Git refs or paths.
   - Require every candidate unit to map to a stable work ID and worker closeout.
   - Only units marked `ready_to_integrate` may move into the integration branch.

5. Create a consolidation branch.
   - Create a consolidation branch from the correct dev base, such as `codex/dev-consolidation-YYYYMMDD`.
   - Fetch first when safe, then branch from the dev target.
   - Keep the consolidation branch local. Do not fast-forward, reset, merge into, or push the repository's local or remote `dev` ref merely because the request says “merge to dev.”
   - If the current working tree is dirty, avoid commands that would overwrite it. Use a temporary preservation branch or worktree instead of stashing blindly.

6. Bring work together.
   - Merge or cherry-pick local branches/worktrees into the consolidation branch one unit at a time.
   - Prefer non-destructive operations such as `git merge --no-ff <branch>` or `git cherry-pick <commit>`.
   - Use file-level apply only when branch history is unusable.
   - After each unit, inspect conflicts, resolve deliberately, run the smallest relevant validation, and commit the resolved unit when the repo expects commits before deployment.
   - Before integrating, check both ancestry/PR evidence and direct file-content
     overlap so repeated consolidation branches are not applied twice.
   - Record focused validation and the resulting integration SHA per unit.

7. Exclude unsafe work.
   - Do not include broken generated output, local-only artifacts, secrets, logs, caches, temp files, unfinished experiments, code that fails focused validation, or migrations/data changes that require unapproved shared database mutation.
   - Preserve excluded work on its original branch/worktree and report it.

8. Resolve conflicts safely.
   - Read both sides of each conflict.
   - Preserve user intent where clear.
   - Prefer established repo patterns.
   - Avoid broad rewrites and blind ours/theirs resolutions.
   - Run focused tests for conflicted areas.
   - If a conflict reveals incompatible product direction or a risky schema/API contract change, pause and report it as a decision item unless the safe resolution is obvious.

9. Validate locally.
   - Run focused tests for touched modules first.
   - Run typecheck, build, lint, integration, or wider repo tests as supported.
   - Run browser/computer-use/e2e checks when UI, routing, or an end-user workflow changed.
   - Run migration/schema validation when schema changed, without applying to shared databases unless explicitly approved.
   - Use existing repo scripts first.
   - If a command fails because of unrelated pre-existing dirty work, prove the changed source subset passes if possible and report the unrelated blocker clearly.

10. Hand off for local testing.
   - Stop after local validation unless the user explicitly requested deployment.
   - Report the exact worktree path, local branch, baseline SHA, integration SHA, startup command, local URL when known, and the specific workflows the user should test.
   - State clearly: `Deployment: not performed; local testing is the next step.`
   - Preserve the consolidation worktree and branch so the user can test the exact validated result.
   - Recommend the sequence: test locally, report any findings, then explicitly request deployment to dev.

11. Deploy to dev, only after a separate explicit request.
   - Deploy only to the confirmed dev environment using the established repo process.
   - Do not infer deployment permission from skill invocation, a successful merge, a green test suite, or the phrase “merge into dev.”
   - Before deployment, confirm branch, commit, environment name, and that no production target is involved.
   - Confirm required migrations/config are approved or safely dev-only.
   - After deployment, capture URL, deployment id, commit SHA, or build id.
   - Run health checks and smoke tests against dev.
   - If deployment fails, do not proceed to cleanup that would obscure the failure. Fix safe local issues and retry once when appropriate, otherwise report the blocker.

12. Clean up local state.
   - Only after validation, and dev deployment when requested, clean up safe artifacts.
   - Safe cleanup may include generated temp files created during this run, stopping local dev servers started by the run, and removing temporary consolidation worktrees created by the run.
   - Do not delete user-created branches, worktrees with unmerged work, stashes, untracked files not created by this run, unknown generated directories, or anything needed to recover excluded work.
   - A coordinated batch worktree is not cleanup-eligible until its closeout,
     integration SHA, validation artifact, and include/defer decision are in the
     registry. Report cleanup candidates first; do not treat successful
     integration as permission to delete user work.

13. Report the final state.
   - Separate completed work, validation, dev deployment, cleanup, excluded work, remaining dirty state, and production-readiness blockers.
   - Be explicit about anything not run and why.

## Safety Rules

- Never treat local-green as production-ready.
- Never push or deploy during the default `local_only` workflow.
- Never treat “merge to dev” as approval to modify remote `dev` or a hosted dev environment.
- Never deploy to production from this skill.
- Never merge to `main` unless the user explicitly says to merge to `main`.
- Never drop work to make the tree look clean.
- Never apply database migrations to shared or cloud environments without explicit approval and confirmed target.
- Never include secrets, local env files, logs, caches, or large generated artifacts unless the repo explicitly tracks them.
- Never hide partial failure. If part of the consolidation worked and part did not, say exactly that.

## Standard Closing Shape

Use this structure:

```markdown
**Consolidation Result**
- Mode:
- Batch ID / marker:
- Observed at:
- Dev target:
- Baseline ref/SHA:
- Branch:
- Deployment: not performed unless separately and explicitly requested
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

**Next Steps**
- Test locally at ...
- If local testing passes, explicitly request deployment to dev.

**Registry**
- Path:
- Ready to integrate:
- Deferred/quarantined:
- Cleanup candidates (not deleted):

**Production Readiness**
- Local status only by default. Hosted dev requires a separate deployment request; production still requires ...
```
