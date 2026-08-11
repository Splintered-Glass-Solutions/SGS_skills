# Plan Handoff Agent Playbook

This is a platform-neutral version of the `plan-handoff` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Package completed research, exploration, discovery, ideation, architecture, or planning into one execution-ready Markdown handoff for a clean task. Use when the user says Plan Handoff, asks to package or compact a plan, wants to transfer a finished plan to another agent or fresh thread, or needs one canonical context document containing the concept, purpose, target audience, user story, requirements, decisions, implementation details, full execution plan, validation, risks, and references without the exploratory history or token-heavy reasoning.

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

# Plan Handoff

Create one durable source-of-truth document that lets a fresh execution task begin without the current conversation. Preserve the plan’s substance and rationale while removing the exploration that produced it.

This is a plan transfer, not a chronological recap, transcript, implementation, or generic summary.

## Core Contract

- Capture the final concept, the problem it solves, why it matters, and what success looks like.
- Preserve every actionable detail from an agreed execution plan.
- Include the context an implementer needs to make correct decisions without reopening the exploration.
- Separate verified facts, approved decisions, assumptions, proposals, and unresolved questions.
- Exclude raw chain-of-thought, step-by-step model reasoning, repeated discussion, rejected drafts, dead ends, and verbose tool history.
- Reference durable sources instead of pasting large artifacts or logs.
- Optimize for relevance density, not minimum length. Completeness outranks brevity when execution details are at risk.
- Do not implement the plan unless the user separately asks for implementation.

## Workflow

### 1. Establish the handoff boundary

Identify:

- the exact initiative or feature being handed off;
- the intended outcome of the next task;
- the latest agreed plan and accepted artifacts;
- what is complete, planned, proposed, or still undecided;
- the execution environment, repository, branch, service, document, or system of record when known.

Treat the latest explicit user direction and latest accepted plan as authoritative. Do not preserve superseded requirements merely because they appeared earlier.

If the exploration did not reach a complete plan, still create a useful handoff, mark it `Provisional`, and list the decisions required before execution. Do not invent missing product, architecture, security, data, deployment, or ownership decisions.

### 2. Build from final signal

Review the current conversation and relevant durable artifacts. Search for existing plans, specs, research reports, diagrams, issues, decisions, branches, commits, and verification evidence before writing.

Include:

- final conclusions and accepted ideas;
- concise decision rationale and important origin context;
- user and business purpose;
- target audience or affected actors;
- the success experience or core user story;
- required behavior and implementation functionality;
- exact constraints, guardrails, interfaces, and dependencies;
- the complete execution sequence;
- validation, rollout, and proof requirements;
- risks, edge cases, assumptions, and open decisions;
- exact artifact paths, URLs, IDs, branches, commits, commands, or source citations needed later.

Exclude:

- conversational chronology;
- raw internal reasoning or hidden thoughts;
- repeated explanations;
- discarded options unless their rejection creates an important constraint;
- obsolete drafts and stale instructions;
- full logs or source dumps when a path, link, excerpt, or concise finding is enough;
- unrelated work discovered during exploration.

Summarize rationale as evidence-backed decision context. Never expose private chain-of-thought.

### 3. Preserve plan fidelity

When a full execution plan exists, audit the handoff against it before saving. Carry forward every material item, including when applicable:

- phases, order, prerequisites, dependencies, and ownership;
- repositories, paths, components, services, functions, routes, schemas, and interfaces;
- product behavior, UI states, workflows, permissions, and edge cases;
- data contracts, migrations, backfills, compatibility, and rollback needs;
- integrations, credentials boundaries, providers, and environment assumptions;
- tests, acceptance criteria, observability, QA, rollout, deployment, and approval gates;
- exact proof boundaries such as local, CI, merged, hosted, production, or customer-visible;
- explicit non-goals and actions that require separate approval.

Do not compress an implementation step into a vague phrase such as “build the backend” when the exploration established specific files, APIs, data flows, or verification steps.

### 4. Label certainty

Use these meanings consistently:

- `Verified`: directly checked in the current work or supported by cited evidence.
- `Decided`: explicitly selected or approved, whether or not implemented.
- `Planned`: part of the agreed execution sequence but not yet completed.
- `Assumed`: needed to make the plan coherent but not confirmed.
- `Open`: unresolved and capable of changing implementation.

Do not turn a plausible idea into a decided requirement. Do not describe planned implementation as completed work. Call out stale or time-sensitive facts.

### 5. Choose a durable destination

Use the user’s requested path or named system of record first.

Otherwise:

1. Save beside the existing canonical plan when one exists.
2. Else use an existing `docs/plans`, `docs/plan-handoffs`, or equivalent project planning directory.
3. Else create `docs/plan-handoffs/YYYY-MM-DD-<initiative-slug>.md` in the current workspace.

Use a descriptive initiative slug, not a generic filename. Do not overwrite an unrelated handoff. Update an existing handoff only when the user clearly asks to revise that artifact; otherwise create a new dated version.

Redact secrets, tokens, credentials, private customer data, and unnecessary personal information. Preserve the fact that a protected value or private dependency exists using a safe placeholder.

## Required Document Shape

Use this structure, adapting subsections to the initiative. Omit a section only when it truly does not apply; do not silently omit unknown information.

```markdown
# Plan Handoff: <Initiative>

Status: Ready for execution | Provisional | Blocked
Created: YYYY-MM-DD
Execution objective: <one sentence>

## Fresh-Task Directive
How the next task should use this document, where to begin, and what not to redo or change.

## Core Concept
The synthesized idea and intended solution in plain language.

## Purpose and Origin
The problem, opportunity, relevant background, why this work exists, and concise rationale for the selected direction.

## Target Audience and Actors
Primary users, secondary users, administrators, systems, or stakeholders affected.

## Success Story
One concrete user story or end-to-end scenario showing the desired successful experience.

## Outcomes and Success Criteria
Observable product, technical, operational, or business results that define success.

## Scope
### In Scope
### Out of Scope

## Functional and Product Requirements
Required behavior, workflows, states, interfaces, permissions, error handling, and edge cases.

## Current State and Key Context
Verified existing behavior, relevant architecture, work already completed, and facts an implementer must know.

## Decisions and Rationale
Final decisions with concise evidence-backed reasons. Include rejected alternatives only when their rejection is an ongoing constraint.

## Technical Design
Components, repositories, files, data flow, APIs, schemas, integrations, security boundaries, compatibility, and operational design.

## Full Execution Plan
Numbered phases and steps with prerequisites, dependencies, exact targets, expected outputs, validation, and approval gates. Preserve all details already agreed.

## Validation and Acceptance
Tests, QA scenarios, observability, rollout checks, acceptance criteria, and required proof layers.

## Risks, Edge Cases, and Guardrails
Failure modes, security or data risks, rollback needs, actions to avoid, and approval boundaries.

## Assumptions and Open Questions
Clearly label what must be confirmed and whether it blocks execution.

## Artifacts and References
Canonical plans, research, paths, URLs, issues, branches, commits, diagrams, commands, or evidence.

## Suggested Skills
Skills the execution task should invoke and why, or `None identified`.

## First Execution Action
The exact safe first step for the fresh task.
```

## Readiness Test

Before finalizing, verify that:

- a capable agent can understand the initiative without this conversation;
- the core concept, purpose, audience, and success story are clear;
- all material requirements and agreed execution steps survived compression;
- implementation targets and dependencies are specific where the source plan was specific;
- scope, non-goals, risks, and approval boundaries are explicit;
- verified facts are not mixed with plans or assumptions;
- the handoff points to canonical evidence and avoids large duplicated source material;
- no secret or unnecessary private data is present;
- the fresh task has an unambiguous first action;
- no exploratory fluff, raw reasoning, or conversational history remains.

Set the status:

- `Ready for execution` only when no unresolved decision blocks the first execution phase.
- `Provisional` when the document is useful but important decisions or evidence remain open.
- `Blocked` when execution would be unsafe or directionally ambiguous.

## Delivery

Return:

1. the absolute clickable path or canonical document link;
2. the readiness status;
3. one sentence naming any blocking uncertainty;
4. this compact fresh-task prompt:

```text
Use $<suggested-execution-skill-if-any> as applicable and execute from this canonical plan handoff:
<absolute path or document link>

Treat the handoff as the source of truth. Begin with “First Execution Action,” preserve its scope and approval boundaries, and do not repeat the completed exploration unless a documented assumption or open question requires verification.
```

Do not create a new task unless the user explicitly asks to create or start one. If asked, create it only after the handoff document is saved and follow the available thread-management rules.
