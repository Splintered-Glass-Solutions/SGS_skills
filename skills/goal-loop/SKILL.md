---
name: goal-loop
description: "Turn current work into an explicit goal and keep going to completion, using independent Sol review to guide code changes toward release readiness."
---

# Goal Loop

Use this when Codex is already working on a user-requested task without an explicit goal and should keep going until the deliverable is complete. For code changes, completion means release-ready implementation. This does not authorize publishing, deployment, or other gated release actions.

## Start the goal

1. Identify the current user-requested outcome and inspect applicable repository instructions, existing changes, and acceptance criteria. Preserve unrelated work.
2. If there is no active goal, create one with `create_goal`. Make its objective specific to the current task and define completion as the requested deliverable being done; for code implementation, require release readiness. Do not create a generic goal or broaden the user's scope. If a relevant goal already exists, continue it; do not replace it. If an active goal is unrelated, clarify before changing its objective.
3. Derive completion criteria from the user's request and project conventions. For code implementation, the requested behavior must be implemented, relevant local checks must pass, and the current implementation must have a Sol Review `pass`. For other deliverables, use task-appropriate acceptance evidence. Treat release readiness as local implementation readiness; deployment or publication is a separate action unless explicitly requested and authorized.
4. For long, ambiguous, cross-repository, high-cost, or repeatedly failing work, use the `session-budget` skill and checkpoint objective, progress, evidence, uncertainty, and next action.

## Work and review loop

- Make the next change needed to meet the acceptance criteria. Run relevant checks after meaningful implementation changes; do not claim checks that were not run.
- When the task includes a coherent, reviewable code implementation slice, use `$sol-review` for an independent, read-only review. Give it the accepted behavior and constraints, base and candidate code state, changed files, applicable repo rules, exact check evidence, and remaining gates. Do not pass it implementation assurances in place of evidence.
- Treat Sol findings as the next-work list. Repair actionable findings in the implementation, rerun affected checks, then request review of the new diff and affected evidence. Repeat until Sol passes the current state and acceptance criteria are met. Follow Sol Review's review and repair limits; do not loop indefinitely on the same failure.
- If the task has no reviewable code implementation, do not manufacture a code change to force Sol Review. Complete the user's actual deliverable against task-appropriate evidence and state why Sol Review did not apply.
- If blocked by missing information, access, or a required external decision, finish independent work, state the precise blocker and recommended next action, and leave the goal active. Do not claim release readiness while a required gate is unresolved.

## Finish

When completion criteria are met, update the goal to `complete`. Report the implemented outcome, checks actually run, the latest Sol verdict and reviewed state, and any separate release action that remains. If criteria are not met, keep the goal active and clearly state what remains.
