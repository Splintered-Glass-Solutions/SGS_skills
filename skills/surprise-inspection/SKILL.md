---
name: surprise-inspection
description: Independently audit whether an ongoing Codex task is advancing the user's actual objective, especially when work may be stuck, circling through testing, accumulating process, or consuming excessive effort. Use when the user requests a surprise inspection or an outside course-correction review.
---

# Surprise inspection

Assess the current task as a whole, then make the best authorized course correction. A long task is not automatically a failure: distinguish necessary complexity and verified outcomes from activity that does not advance acceptance.

## Gather a compact evidence packet

Identify the user's original goal, later corrections and approvals, success criteria, active work and current ownership. Include short verbatim excerpts of the user's relevant instructions where safe, separate from the parent's interpretation. Read the latest relevant checkpoint and only enough earlier history to establish the pattern; examine exact governing rules and live state when material. Note what was actually shipped or verified, what remains, repetitions and their outcomes, and any known resource or cost evidence. Label gaps and stale evidence; never invent token, time, cost or progress figures. Hold new attempts on the disputed path during review; preserve in-flight jobs and unrelated work. Do not interrupt other agents or mutate the environment just to perform the inspection. For each suspected repeat, identify what changed (revision, target, inputs, external state or required proof) and which decision its result would change.

Distinguish user/system/developer requirements, explicit skill rules, actual technical prerequisites or active wrapper requirements, and the agent's own inferred or optional process. Check later user authorizations and overrides before calling something blocked. A wrapper requirement may be real even when the underlying policy does not demand that particular mechanism. Preserve safety, source/target identity, production approval, and side-effect boundaries; do not manufacture evidence or waive real gates.

## Independent review

Use the `$sol-review` principle of a fresh, independent, read-only reviewer, but route this inspection to `gpt-6.1-sol` at **high** reasoning, when supported. Spawn one reviewer with `collaboration.spawn_agent(model="gpt-6.1-sol", reasoning_effort="high", fork_turns="none")`, a compact packet, exact paths, relevant recent checkpoints and a request to inspect evidence independently. Do not send secrets. Ask it not to modify state, spawn agents, or perform external writes. If the model or subagent facility is unavailable, state that independent review was unavailable and make a clearly labeled self-assessment; do not pretend the model ran or wait indefinitely for routing.

Ask the reviewer to return:

1. A verdict: on track, course-correct, blocked, or uncertain, with the real objective and specific evidence.
2. Material outcomes versus repeated attempts, including why duration is justified or where effort became a loop, detour, or excessive process. Do not infer waste from elapsed time alone.
3. Actual hard gates, active technical requirements, assumptions or self-imposed gates, and remaining uncertainties, with citations and their provenance.
4. The smallest actionable next step, proposed removals or simplifications, expected proof of progress, and precise stop or reconciliation conditions. Flag any decision that truly requires the user.

Ask for proportional, evidence-backed recommendations; do not require a fixed number of findings or another inspection. Bound the review to the task and preserve the user's existing authority. Use one review, with at most one targeted clarification for a decisive missing fact; another review needs a material change or unresolved finding that warrants its cost.

## Act and communicate

Check recommendations against the evidence and current instructions; do not blindly accept a reviewer suggestion that bypasses a real gate. State what to keep, stop and defer. Implement the smallest useful, already-authorized correction in the current chat, verify an observable result, then resume the original acceptance criteria with one concrete next action. If the user requested review or planning only, honor that boundary. An advisory blocked verdict does not itself set a native goal status. Avoid extra approval requests for actions already authorized. A reviewer is advisory and read-only; the parent owns decisions and execution. Do not start a new chat, modify schedules, send messages to others, or widen scope unless authorized.

Update an existing checkpoint if the work is sustained, recording the decision, evidence, uncertainty and next action without creating a competing ledger. Tell the user plainly what is progressing, what is wasting effort or actually blocked, what is changing, and what remains unverified. Explain any disagreement with the independent review and do not equate local or staged evidence with production acceptance.

## Research foundation

For later skill improvements, see [research notes](references/research.md). Do not reload them for every inspection.
