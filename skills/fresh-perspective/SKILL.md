---
name: fresh-perspective
description: Bring in an independent Astra agent to assess whether the current chat is making progress toward the user's goal, diagnose loops or misplaced effort, and course-correct the next action. Use when the user asks for a fresh perspective, asks whether we are going down the right path, or questions an apparent rabbit hole or repeated unproductive attempts.
---

# Fresh Perspective

Recover direction by judging the work against the user's actual intended outcome.
This is a strategy and progress review, broader than a code review. A sound path
may need continuation rather than a correction; do not manufacture problems.

## Capture the situation

Pause new attempts in the disputed lane while collecting a compact checkpoint.
Preserve useful output and dirty work; stop only task-owned workers that would
keep changing the reviewed state. Do not interrupt unrelated work.

Build an evidence packet from accessible conversation history and relevant artifacts:

- Original user request in the user's words, subsequent corrections, authorized
  scope, and the concrete outcome that would count as done.
- Current working goal and plan, actual state, and task-relevant changes.
- A short chronology of attempted approaches, observed outcomes, repeated errors,
  and what each attempt actually taught us. Separate claims from proven results.
- Remaining blockers, pending decisions, applicable constraints, and the evidence
  behind any supposedly mandatory gate. Include exact rules when they seem to
  cause redundant work.
- Links or paths to the few artifacts needed to verify the situation, plus known
  history gaps or uncertainty. Retrieve missing context narrowly if available;
  do not present a parent's paraphrase as the original user instruction.

## Dispatch one independent Astra reviewer

Use `collaboration.spawn_agent` with `model="gpt-6-astra"`,
`reasoning_effort="high"`, and `fork_turns="none"`. Give it the evidence packet
and access to relevant artifacts. Invocation authorizes this review subagent;
it does not authorize messaging another user-owned chat or creating one.
If Astra is unavailable, report the limitation; do not silently substitute a
model or claim Astra reviewed the work.

The reviewer is read-only and must not delegate, edit, commit, deploy, send
messages externally, or mutate goals or shared data. Ask it to independently:

1. Reconstruct the intended outcome and assess how the current work serves it.
2. Identify meaningful progress, drift, repeated attempts without new evidence,
   unsupported assumptions, premature complexity, and unnecessary scope.
3. Distinguish real blockers from optional polish or low-impact distractions.
   Check whether a gate comes from an actual instruction, a necessary acceptance
   condition, or an agent's interpretation. Never recommend ignoring explicit
   user requirements or required safety/authorization boundaries.
4. For real hurdles, identify the best supported explanation and the smallest
   discriminating check or alternate approach that could resolve them. Label
   hypotheses and missing evidence rather than inventing a root cause.
5. Return a clear direction: continue, course-correct, or blocked pending a
   specific dependency. Recommend what to keep, stop, defer, or change; rank the
   next actions and give an observable success/stop condition for the first one.
   Name any question that truly requires the user's decision.

Require a compact evidence-backed answer: intended outcome; verdict; decisive
findings with references; recommended next action and why; what can be deferred;
and material uncertainties. Do not demand a broad audit, clean workspace, full
test rerun, or extra feature work unless relevant evidence justifies it.

## Apply the course correction

Read the review critically against user instructions and current evidence.
Explain any material disagreement instead of blindly accepting recommendations.
Do not restart the same review repeatedly: one targeted follow-up is enough if
a decisive fact is missing or contradicted; otherwise take the recommended step.

Update the thread's working checkpoint with the intended outcome, retained proof,
revised plan, deferred distractions, remaining uncertainty, and next action.
Correct stale task plans or owned task notes when available. Reconcile an active
goal only through supported goal controls: do not create a goal unless explicitly
requested, mark an unfinished goal complete to replace it, pause without a user
request, or declare it blocked contrary to the tool's criteria. If its objective
cannot be edited, record the corrected objective in the checkpoint and explain
that the existing goal record remains unchanged.

Give the user the verdict and the concrete next step, then execute that step if
it is within existing authorization. A planning-only task stays at a revised,
decision-ready plan; a review-only request ends with findings. Ask only for a
decision that actually prevents progress, continuing independent useful work
where possible. No new deployment, outreach, destructive cleanup, spending, or
shared-data authority follows from a course correction.

Stop when the next action's success condition is met, or a specific unresolved
dependency prevents it. Report what changed in direction and the resulting proof;
do not claim the original task is complete merely because the review is complete.
