---
name: bulk-edits-thread
description: Prepare one scoped Codex editing task and isolated local worktree from the confirmed dev baseline, using an approved Batch Brief and a committed Batch Manifest. Use when Preston says "bulk edits thread", wants one focused task ready to receive many related edits, or asks to start an isolated local editing lane. Always enforce codex-safe-run throughout.
---

# Bulk Edits Thread

Prepare one current, validated, locally running workspace for a bounded feature
batch. The normal path is isolation-first: start from confirmed `dev` and do
not absorb work from other branches. `collapse-bulk-edits-thread` is the only
normal reconciliation point back into local `dev`.

Require a user-approved Batch Brief from `to-do-list-planning` before starting
a new focused batch. A separately explicit recovery/consolidation request may
use `local-dev-consolidation`; do not treat a normal bulk-edits invocation as
that request.

## Workflow

1. Classify the run as build work in an isolated execution lane. Record the
   Batch Brief's batch ID, scope, exclusions, affected repositories, overlap
   zones, acceptance criteria, and validation plan. If there is no approved
   Batch Brief, stop and request planning rather than inferring scope.
2. **Deployment-topology gate:** When the Batch Brief names Dev, staging,
   production, a deployment, or a hosted integration, map before implementation:
   exact app/runtime environment, database sharing, customer-mutation authority,
   involved repositories/components, and every deployable node. For Bonfire
   source sync, prove Railway environment → Function URL → Lambda → image.
   Record shared assets as a release boundary, not an automatic blocker. Do not
   make topology-dependent implementation or deployment assumptions until this
   mapping is known.
3. **Mandatory safe-run gate:** Read and follow `codex-safe-run` before any repository action, and keep its token-budget and compact-output rules active for the entire bulk-edits task. Take one `codex-safe-monitor.sh --once` snapshot at the start. Do not start persistent monitors, streaming CI checks, verbose process dumps, or unnecessary Browser/Computer Use/MCP sessions.
4. Read and follow the current `reanme-chat`, `local-dev-consolidation`, and
   `spin-up-local` skills before acting. Use `session-budget` when the
   repository has many active branches/worktrees or an overlap is ambiguous.
5. Rename the current Codex task first by prefixing its existing name with
   `✍️BULK - `, preserving the existing thread name exactly after the prefix.
   Do not create, fork, archive, or hand off a task.
6. Run an isolation preflight against every affected repository:
   - fetch the remote safely;
   - inspect the current branch, dirty tree, remotes, worktrees, stashes, and branches;
   - identify the repository's actual dev integration branch;
   - record the freshly fetched dev ref and exact baseline SHA;
   - identify every active writable batch whose overlap zone intersects the
     Batch Brief (route, component family, API contract, migration, or shared
     fixture);
   - stop with a decision item if an overlapping writable batch exists.
7. Create one uniquely named local branch and worktree from the fetched dev
   tip, such as `codex/bulk-<scope-slug>-YYYYMMDD`. Add a numeric suffix when
   needed; never reuse a date-only bulk branch. Preserve all existing user work
   before switching contexts.
8. Create and commit a non-secret Batch Manifest at
   `.codex/batches/<batch-id>.md` in each affected worktree. It must record:
   batch ID; scope and exclusions; repository/worktree/branch; baseline dev
   ref/SHA; planned item IDs and acceptance criteria; touched areas and overlap
   zones; commits; validation evidence; deferred work; and a blank
   closeout-integration-SHA
   field. Keep it updated as the batch proceeds.
9. Do not merge, cherry-pick, or copy work from another branch/worktree by
   default. Integrate predecessor work only when the approved Batch Brief names
   its batch ID/commit and the isolation preflight confirms it is necessary and
   non-overlapping. Preserve all other work where it is.
10. Implement only planned items. Make an atomic commit per planned item or
   tightly coupled acceptance unit, update the Batch Manifest with its commit
   and focused validation, and do not hide conflicts with blanket `ours` or
   `theirs` resolution. Require an explicit Batch Brief amendment before adding
   unrelated work.
11. Run focused validation for each touched area, then the appropriate broad
   repo-native checks. Do not apply migrations or mutate any shared database.
12. Follow `spin-up-local` from the isolated worktree. Start the repo-native
   local command on an open port, keep it running, map its effective
   backend/database targets without exposing secrets, and verify the local URL
   or health endpoint.
13. Recheck `git status`, branch, baseline and current commit, Batch Manifest,
   server process, and URL. Account for every local change as a planned item,
   an explicit predecessor, or deferred work.

## Boundaries

- Treat this as local preparation only. Do not push, open a PR, deploy to dev, merge to `main`, or touch production unless Preston separately authorizes it in the current conversation.
- A focused bulk-edit branch is not a recovery or catch-all consolidation lane.
  Do not pull apparently safe work from other branches unless it is explicitly
  named in the Batch Brief.
- Never discard, reset, delete, or silently stash user work to make the repository look clean.
- Never create or use a local Supabase/Postgres database for Bonfire repositories. Use only the configured approved cloud target when the app requires database access, and do not run migrations during this workflow.
- Keep `codex-safe-run` active throughout: use one-shot checks, capped/file-backed logs, and concise delta-only updates. Do not use watchers or start extra Desktop threads, agents, Browser/Computer Use, or MCP-heavy sessions unless the task requires them.
- Do not claim readiness until consolidation validation passes and the local app or service is reachable.
- If incompatible product directions or unsafe work prevent a single branch, stop with a concise decision item instead of guessing.

## Completion Message

Report the batch ID and scope, Batch Manifest path, baseline SHA, isolated
branch/worktree, explicit predecessor work, deferred work, validation, local
URL, runtime targets, and any remaining caveat. Include a compact safe-run
status: app-server roots, swap/memory state, cleanup performed, and whether
Desktop remains safe to continue. End successful runs with this exact standalone
sentence:

`Okay, we're ready to start making edits. Start firing away whenever you're ready.`
