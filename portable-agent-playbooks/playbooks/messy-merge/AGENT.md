# Messy Merge Agent Playbook

This is a platform-neutral version of the `messy-merge` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Safely merge feature work into Bonfire dev when multiple parallel features or messy overlapping branches are in flight. Use when the user says messy_merge, messy merge, merge this into dev, get this safely merged to dev, preserve other dev work, resolve overlaps with dev, or prepare a combined dev promotion set without losing concurrent changes.

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

# Messy Merge

Use this skill when the user wants feature work merged into `dev` while other Bonfire work is landing in parallel. The goal is a safe dev integration, not production promotion.

## Contract

Do not push, deploy, merge to production, mutate cloud databases, or delete/revert other work unless the user explicitly asks in the current thread.

Preserve existing `dev` work by default. If another change has already landed in `dev`, treat it as intentional unless there is strong evidence otherwise. Resolve conflicts by integrating this feature around that work. Stop and ask before removing, replacing, or substantially redesigning overlapping dev changes.

Keep the merge scoped to the requested feature. Do not use the merge as an excuse to clean up unrelated dirty files, reformat broad areas, or settle unrelated branch drift.

## Workflow

1. Preflight local state.
   - Run `git status --short --branch`.
   - Identify the current branch, target branch, dirty files, staged files, untracked files, and whether work appears unrelated.
   - Do not reset, checkout, stash, or clean user changes unless the user explicitly approves the exact operation.

2. Inspect current `dev` before changing anything.
   - Fetch or inspect the local remote-tracking state using non-destructive commands such as `git fetch --prune` only when network and repo policy allow it.
   - Compare against `origin/dev` or the configured dev remote branch with `git log --oneline --decorate --graph --max-count`, `git diff --stat`, and targeted file diffs.
   - Identify work that already landed in dev and any files likely to overlap with this feature.

3. Define the merge shape.
   - Determine whether the safest path is a normal merge, rebase onto dev, cherry-pick, manual patch application, or leaving a conflict report.
   - Prefer the repo's existing branch strategy and current thread instructions.
   - For Bonfire, do not promote to `main` or production unless the user explicitly requests that exact promotion in the current conversation.

4. Apply the integration safely.
   - Bring in dev or feature changes using the least destructive approach.
   - Resolve conflicts by preserving dev changes unless the user explicitly approved replacing them.
   - When both sides are valid, combine behavior and add tests around the combined outcome.
   - If a conflict touches permissions, grants, RLS, roles, ownership, billing, migrations, production data, or external integrations, stop for explicit approval before changing the contract.

5. Validate the combined state.
   - Run focused tests for the merged feature and the overlapping dev areas.
   - Run relevant wider checks: lint, typecheck, build, route/API tests, browser/Playwright checks, product KB validation, or repo-specific scripts.
   - For UI changes, run a local browser check against the dev server and report the URL and scenario tested.
   - If full-suite validation is blocked by unrelated dirty work or environment gaps, run scoped validation and clearly name the blocker.

6. Document only what changed.
   - Update repo-local docs if behavior, setup, API contract, test workflow, or operator guidance changed.
   - Update shared docs only when the change affects cross-repo contracts, data flows, operational runbooks, or customer-facing KB that is canonical there.
   - Do not invent shared-doc updates for purely local UI cleanup.

7. Report the merge handoff.
   - State the branch and target dev reference inspected.
   - List files changed by this feature and any conflicts resolved.
   - Summarize how existing dev work was preserved.
   - List tests/checks run and browser evidence.
   - Separate remaining blockers, optional follow-ups, and items requiring the user approval before production promotion.

## Conflict Rules

- Dev wins by default for unrelated behavior.
- Feature wins only for the feature's intended behavior.
- Combine when both sides are user-visible and compatible.
- Ask before deleting a dev-side feature, changing database/security contracts, or rewriting a broad shared abstraction.
- Never use `git reset --hard`, `git checkout -- .`, `git clean`, or force-push unless the user explicitly asks for that exact operation.

## Closing Shape

End with:

- Dev state inspected.
- Merge/integration action taken.
- Conflicts or overlaps and how they were resolved.
- Validation run.
- Docs updated or why not applicable.
- Remaining blockers before production promotion.

