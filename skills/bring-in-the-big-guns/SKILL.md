---
name: bring-in-the-big-guns
description: >-
  Escalate a stuck, looping, or repeatedly patched Codex task to the latest
  available frontier model at high reasoning, then repair the original problem
  and clean up damage from earlier attempts. Use when the user invokes this skill,
  says bring in the big guns, reports that Terra, Luna, or another smaller model
  is cycling, applying Band-Aids, producing half-built fixes, reopening failures,
  or making the workspace progressively messier.
---

# Bring In The Big Guns

## Purpose

Stop an unproductive repair cycle and transfer ownership to the strongest
available reasoning path. Finish both jobs: solve the original request and
reconcile the smaller model's attempted fixes into a clean, verified state.

This invocation explicitly authorizes one model-escalation handoff or recovery
agent when the active task cannot switch models in place. It does not authorize
deployment, destructive cleanup, production changes, or broader scope.

## Escalate the Model First

Before making another task edit:

1. Inspect the runtime's available model controls and effective model metadata.
2. Select the newest available frontier model with `high` reasoning.
3. If the active task already uses that model and reasoning level, continue in
   the active task.
4. If in-place switching is supported, switch and verify the effective model.
5. If in-place switching is not supported, hand the entire recovery to exactly
   one agent using the newest available frontier model and `high` reasoning.
   Give it the conversation context and the recovery checkpoint below. Do not
   keep editing in parallel while it works.
6. If neither switching nor a frontier-model handoff is available, say so
   plainly and ask the user to select the frontier/high setting. Do not claim an
   escalation occurred.

Resolve “latest frontier” from the models exposed by the current runtime; do
not permanently hardcode a model name that can become stale. Prefer the model
described as latest/frontier over balanced, fast, mini, Terra, or Luna variants.

## Freeze and Checkpoint

Preserve evidence before cleanup:

- restate the original objective and latest user instruction
- capture the repo, worktree, branch, base, `git status --short`, and relevant
  running processes or browser state
- summarize attempted fixes, commits, uncommitted diffs, observed errors, and
  which validations actually passed
- distinguish user-owned or pre-existing changes from Codex-created changes
- stop or interrupt smaller-model workers that are still changing the same
  scope, after retaining any useful output

Do not erase, reset, stash away, or overwrite dirty work merely to obtain a
clean baseline.

## Recovery Workflow

1. Reproduce or inspect the current failure before editing.
2. State one concrete root-cause hypothesis backed by current evidence.
3. Audit every earlier task-related change as one of:
   - correct and reusable
   - incomplete but salvageable
   - wrong or harmful
   - unrelated and therefore untouchable
4. Remove or repair only changes proven wrong and owned by this task. Use
   surgical patches; never use destructive broad resets or checkouts.
5. Implement the smallest coherent root fix. Do not stack another fallback,
   retry, special case, or state mutation unless it is part of the demonstrated
   root solution.
6. Clean up temporary debugging code, duplicate logic, stale processes,
   contradictory configuration, misleading errors, and obsolete attempted
   fixes introduced during the cycle.
7. Re-read the final diff against the original request and acceptance criteria.

If the earlier attempts crossed repositories or worktrees, reconcile ancestry
and ownership explicitly before moving code. Preserve isolated work until the
correct integration target is proven.

## Verification Contract

Verification must cover:

- the exact original reproduction
- a direct regression test for the root cause
- relevant focused tests for every cleaned-up area
- runtime, browser, screenshot, API, or log proof when the failure was visible
  only in an integrated environment
- `git diff --check` and a final dirty-work audit

After any user-visible success, wait long enough to detect loops, repeated
requests, retries, remounts, or delayed failures. A single green response is not
proof when the reported problem involved cycling or state restoration.

Keep proof boundaries explicit: local, authenticated local, merged, deployed,
shared-data, and customer-visible are different states.

## Guardrails

- Preserve all unrelated user changes.
- Do not deploy, push, merge, mutate shared data, or send communications unless
  already authorized for the exact target and action.
- Do not clean up by deleting material work without resolving ownership and
  recoverability.
- Do not broaden the feature while repairing it.
- Do not call a workaround a fix when the root failure remains.
- Do not declare success while a known request loop, failing direct regression,
  stale runtime error, or unverified cleanup remains.

## Reporting

Lead with the outcome, then report:

- effective frontier model and reasoning level, or the truthful escalation
  limitation
- root cause
- original problem fixed
- earlier-attempt mess removed, retained, or still uncertain
- tests and integrated proof
- files and commits changed
- remaining integration, deployment, or data caveats

Keep this report compact but evidence-backed.
