---
name: next-step
description: >-
  Decide and execute the most reasonable next safe step after a completed run,
  plan, QA pass, deploy, investigation, or phased feature discussion. Use when
  the user asks "next", "next step", "what now", "continue with the next phase",
  "work the next most reasonable step", or wants autonomous continuation with
  gated safety logic. Never deploy, promote, roll back, shift traffic, or publish
  a release through this skill. Safe, bounded database migrations may be applied
  when their dedicated migration gate passes.
---

# Next Step

## Purpose

Use this skill to turn a loose "what should we do next?" moment into bounded
execution. The agent should identify the most reasonable next step, verify that
it is safe to do autonomously, and then do it. If nothing safe or useful is
available, stop and say so.

This skill is intentionally action-oriented. Do not only propose a plan unless
the safe next step is planning, triage, or asking for a missing approval.

Deployment is always out of scope for this skill, even when it is the obvious
next step or was approved earlier in the thread. A database migration is not
treated as a deployment and may be executed only under the migration gate below.

## Operating Contract

Start by classifying the prior work and current state:

- `continue_plan`: a phased plan exists and the next phase is known.
- `finish_artifact`: a generated artifact needs saving, committing, indexing,
  polishing, or cleanup.
- `fix_blocker`: tests, lint, QA, migration, or runtime checks exposed a concrete
  blocker.
- `verify_or_close`: work appears done but needs proof, documentation, or final
  cleanup.
- `unclear`: the next step cannot be inferred safely.

Then choose one next step using this priority order:

1. Fix a concrete blocker that is local, bounded, and already evidenced.
2. Complete a required artifact or cleanup that was left unfinished.
3. Run missing validation that is safe, relevant, and not overly broad.
4. Apply a required safe database migration when the migration gate passes.
5. Implement the next phase of an explicit accepted plan.
6. Produce a small decision-ready plan if implementation is not yet safe.
7. Stop with "no safe autonomous next step" if all likely actions are gated or
   low-value.

## Safety Gate

Proceed autonomously only when all are true:

- The next step is inferable from the current conversation, repo state, or a
  durable plan/artifact.
- Scope is small enough for one focused pass.
- The action is reversible or low-risk.
- Required credentials and environment context are already available.
- Validation can be run without unsafe live side effects.
- The action does not require a user/product decision that would materially
  affect behavior, data, cost, or rollout.

Stop and ask, or report blocked, when the next step involves:

- any application or infrastructure deployment, promotion, rollback, traffic
  shift, release publication, or deployment command; never perform these through
  this skill, regardless of prior approval
- grants, ownership, RLS or policy changes, destructive migrations or writes,
  unbounded backfills, or broad data mutation
- paid/broad provider jobs, scraping waves, AI extraction waves, or sync jobs
  without an approved bounded run mode
- sending messages, customer notifications, release notes, emails, or public
  updates
- using or exposing secrets
- merging to protected branches, rebasing shared work, force pushing, or
  overwriting unrelated dirty work
- ambiguous product choices, pricing, billing, auth, permissions, or compliance
  behavior

If the user explicitly approved another gated action in the current thread, the
approval applies only to that named action and target environment. Prior approval
does not override this skill's deployment exclusion; report deployment as the
next gated action and leave it for a separate explicit deployment workflow.

### Database Migration Gate

A database migration may be the selected next step only when all are true:

- the exact database and environment are resolved from current evidence
- the migration is required by the accepted work already in scope
- the migration is additive or otherwise backward-compatible and has no
  destructive DDL, grants, ownership, RLS, or policy changes
- lock, rewrite, compatibility, and rollback risks have been reviewed and are
  acceptably bounded
- local and remote migration history is reconciled, with no unresolved ordering
  or drift
- the canonical migration workflow is known, credentials already exist, and the
  result can be verified immediately

If any condition fails, do not apply the migration. Prepare or validate it
locally when useful, then report the exact blocker or approval needed.

## Workflow

1. Inspect current state lightly:
   - latest user request
   - any active plan or checklist
   - repo status, current branch, and changed/untracked files when in a repo
   - most recent validation/deploy/QA evidence
   - local instructions such as `AGENTS.md` when present

2. State the candidate next step in one sentence.

3. Apply the safety gate:
   - if safe, say "I’m going to do X" and execute
   - if gated, say exactly what is gated and what approval/input is needed
   - if the candidate is a database migration, apply the database migration gate
   - if the candidate is a deployment, do not execute it; report it as excluded
   - if nothing useful is safe, say that and do no file/system changes

4. Execute one bounded pass:
   - make the smallest coherent implementation or cleanup
   - run focused validation when relevant
   - update durable artifacts if the work produced evidence or decisions
   - do not drift into a second unrelated next step

5. Close with:
   - what was done
   - what was verified
   - what remains blocked or next
   - any files changed

## Common Patterns

### After QA Or Full-Suite Runs

Prefer fixing the highest-signal blocker if it is local and bounded. Examples:

- add missing `.gitignore` entries for generated artifacts
- commit or move a QA artifact
- add a lint config only if the intended lint scope is obvious
- write a safe dry-run/smoke path for a job when production execution is blocked

Do not execute production jobs merely because QA found them blocked.

### After Planning

If the plan is explicit and accepted, implement phase 1 or the next unfinished
phase. If the plan has unresolved product choices, write the decision brief or
ask only the missing question.

### After Deploy

Run read-only, production-safe or environment-appropriate verification. Never
deploy, promote, roll back, shift traffic, or publish a release through this
skill, even with approval in the current thread.

### Before A Database Migration

Resolve the canonical target and compare migration ledgers before applying it.
Inspect the SQL for destructive operations, permissions changes, unbounded data
work, table rewrites, and lock risk. Apply only when the database migration gate
passes, then verify both migration history and the intended post-condition.

### Dirty Worktree

Work with existing changes. Do not clean, revert, or stage unrelated files
unless that is the selected next step and it is clearly safe.

### Nothing Safe

Return a concise no-op verdict:

```md
No safe autonomous next step.

The likely next actions are gated because <reason>. The smallest useful input
needed is <approval/decision/credential>.
```

## Output Shape

For non-trivial runs, use:

```md
Next step: <chosen action>
Safety: <safe | gated | no-op>, because <reason>
Result: <what changed or was found>
Verification: <checks run or why none>
Remaining: <next blocker or next likely action>
```

Keep the response short unless the next step produced findings that need detail.
