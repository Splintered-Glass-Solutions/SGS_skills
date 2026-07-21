# Bulk Edits Thread Agent Playbook

This is a platform-neutral version of the `bulk-edits-thread` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Prepare a the agent task and local repository for a rapid series of edits by renaming the current task with today's date, consolidating safe work from active branches and worktrees onto a current local dev-based branch, validating the merged state, and starting the app locally. Use when the user says "bulk edits thread", wants one task ready to receive many edits, or asks to gather work from other tasks before beginning an editing session.

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

# Bulk Edits Thread

Prepare one current, validated, locally running workspace before the user starts sending a sequence of edits. Orchestrate the existing rename, consolidation, and local startup skills instead of duplicating their full procedures.

## Workflow

1. Classify the run as build work with a consolidation phase.
2. Read and follow the current `reanme-chat`, `local-dev-consolidation`, and `spin-up-local` skills before acting. Use `session-budget` when the repository has many active branches/worktrees or the consolidation becomes ambiguous.
3. Rename the current the agent task first to `YYYY-MM-DD - Bulk Edits`, using today's local date. Do not create, fork, archive, or hand off a task.
4. Run the local consolidation preflight against the active repository:
   - fetch the remote safely;
   - inspect the current branch, dirty tree, remotes, worktrees, stashes, and branches;
   - identify the repository's actual dev integration branch;
   - compare active branch/worktree commits and working changes against the fetched dev tip;
   - distinguish already-merged, unique functional, incomplete, generated, risky, and unrelated work.
5. Create or select one local `agent/bulk-edits-YYYYMMDD` branch based on the fetched dev tip. Preserve all existing user work before switching contexts.
6. Consolidate only safe, functional work that is not already represented in dev. Merge or cherry-pick one logical unit at a time, resolve conflicts deliberately, and capture merge/conflict-resolution changes in commits. Never hide work by using blanket `ours` or `theirs` resolution.
7. Preserve excluded or uncertain work on its existing branch/worktree and report it. Do not force unfinished experiments, secrets, local output, production-only changes, or unapproved schema/data/permission mutations into the bulk-edit branch.
8. Run focused validation for merged areas, then the broad repo-native checks appropriate for the resulting branch. Do not apply migrations or mutate any shared database.
9. Follow `spin-up-local` from the consolidated worktree. Start the repo-native local command on an open port, keep it running, map its effective backend/database targets without exposing secrets, and verify the local URL or health endpoint.
10. Recheck `git status`, branch, commit, server process, and URL. Account for every active local change as included, already in dev, or explicitly deferred.

## Boundaries

- Treat this as local preparation only. Do not push, open a PR, deploy to dev, merge to `main`, or touch production unless the user separately authorizes it in the current conversation.
- Never discard, reset, delete, or silently stash user work to make the repository look clean.
- Never create or use a local Supabase/Postgres database for Bonfire repositories. Use only the configured approved cloud target when the app requires database access, and do not run migrations during this workflow.
- Do not claim readiness until consolidation validation passes and the local app or service is reachable.
- If incompatible product directions or unsafe work prevent a single branch, stop with a concise decision item instead of guessing.

## Completion Message

Report the consolidated branch, included and deferred work, validation, local URL, runtime targets, and any remaining caveat. End successful runs with this exact standalone sentence:

`Okay, we're ready to start making edits. Start firing away whenever you're ready.`

