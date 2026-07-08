---
name: interview-spec
description: Interview the user to discover the real goal behind a project, product idea, feature request, implementation ask, automation, or ambiguous workstream; bias toward small compartmentalized specs; and make the user verify key decisions explicitly before implementation or handoff. Use when the user asks to scope, spec, plan, define, break down, interview, clarify, or turn an idea into a decision-ready project spec.
---

# Interview Spec

## Overview

Use this skill to turn an unclear project idea into a small, verified spec. The agent's job is to interview for the real goal, separate decisions from assumptions, and stop with a decision-ready artifact unless the user explicitly asks to proceed into implementation.

## Operating Rules

- Start by naming the likely task class and the apparent goal in one or two sentences.
- Ask only the next highest-leverage 1-3 questions. Prefer questions that change scope, ownership, acceptance criteria, risk, or user value.
- Bias toward the smallest coherent spec that can be validated independently.
- Split broad requests into compartmentalized specs with clear boundaries instead of producing one large blended plan.
- Track confirmed decisions, assumptions, and open questions separately.
- Do not drift into implementation, migrations, deploys, PRs, or production changes while interviewing.
- Before presenting a final spec or moving into execution, ask the user to verify the key decisions explicitly.

## Interview Flow

1. Restate the seed request:
   - what the user appears to want
   - why it may matter
   - what is still ambiguous
2. Find the real goal:
   - desired outcome
   - target user or audience
   - current pain or trigger
   - what success would make possible
3. Narrow the scope:
   - smallest useful version
   - out-of-scope items
   - boundaries by repo, system, audience, channel, or workflow
   - dependencies and non-negotiable constraints
4. Verify key decisions:
   - ask the user to confirm the goal, scope slice, exclusions, and acceptance criteria
   - do not treat silence or weak agreement as final verification
5. Produce the spec:
   - keep it concise and implementation-ready
   - include enough detail for a future agent or engineer to execute without re-interviewing

## Spec Shape

Use this structure when the user is ready for the spec:

- Real goal
- Target user or operator
- Current problem
- Confirmed decisions
- Assumptions
- Non-goals
- Smallest useful scope
- Acceptance criteria
- Verification plan
- Risks or unknowns
- Recommended next action

For larger projects, produce multiple compartmentalized specs instead of one broad spec. Each spec should have one owner, one primary workflow, and a clear verification path.

## Question Style

- Prefer concrete tradeoff questions over generic discovery questions.
- When choices are visible, offer 2-3 options and name the consequence of each.
- If the user gives a fuzzy answer, tighten it into a proposed decision and ask for confirmation.
- If the user asks for "everything," push for the first compartment that creates proof or value.
- If the request is already clear, do not over-interview; produce the compact spec and ask for final verification.

## Verification Gate

Before implementation or handoff, explicitly ask the user to confirm a short decision ledger:

- goal
- first scope slice
- non-goals
- acceptance criteria
- validation method

If any item is not verified, label it as an assumption or open question.
