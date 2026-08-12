# 5. Facilitator Guide and Exercises

## Teaching objective

Move learners from “ask AI to do a thing” to “design a bounded, verifiable
workflow in which AI can do useful work safely.”

## Session 1: The operating model

### Teach

- the six-state loop: intent, scope, evidence, action, proof, state transition;
- capture versus planning versus execution;
- proof layers and authority layers;
- why context management is a whole-job problem.

### Exercise

Give learners this request:

> “Can you clean up our backlog, fix the bugs, and get everything ready to ship?”

Ask them to rewrite it into:

1. a capture note;
2. a planning request;
3. an execution contract;
4. a proof requirement.

### Debrief

The request is not bad because it is ambitious. It is bad because it does not
identify scope, ownership, target, authority, or completion evidence.

## Session 2: Multi-project and multi-repo work

### Teach

- portfolio versus project versus task scope;
- dependency mapping;
- one owner and evidence contract per workstream;
- overlap zones and one active writable batch;
- compact worker-return formats.

### Exercise

Give learners three fictional workstreams:

- an API contract change in repository A;
- a UI change in repository B;
- a deployment/configuration change in repository C.

Ask them to identify:

- dependency order;
- shared contracts;
- what can be delegated in parallel;
- what must remain in the main thread;
- what proof is required before integration.

### Debrief

Parallel work is valuable only when the integration contract is explicit.

## Session 3: Debugging and hotfixes

### Teach

- observed versus expected behavior;
- reproduction before speculation;
- one hypothesis before editing;
- focused regression checks;
- separating local proof from deployed proof.

### Exercise

Provide a bug report with an ambiguous screenshot and a failing test. Learners
must produce a debugging worksheet before proposing a fix.

Then ask them to convert the fix into a hotfix checklist with explicit stop
conditions.

### Debrief

The best debugging prompt is usually shorter than the best implementation
prompt because it is anchored in a precise reproduction and evidence packet.

## Session 4: Planning, handoff, and token discipline

### Teach

- narrow context packets;
- accepted-state checkpoints;
- deterministic tools for exact work;
- handoffs that preserve decisions and proof;
- when not to reload the full conversation.

### Exercise

Give learners a long, noisy task history. Ask them to reduce it to an accepted
state containing only:

- the objective;
- decisions;
- proof;
- remaining uncertainty;
- next action.

### Debrief

Compression is successful only if the next agent can act correctly without
reconstructing the discarded history.

## Assessment rubric

Score each dimension from 0 to 2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Scope | vague | mostly bounded | explicit inclusions/exclusions |
| Evidence | assumptions | some source material | exact evidence and limits |
| Authority | implied | partially stated | action-by-action boundary |
| Execution | monolithic | some decomposition | correct lanes and ownership |
| Validation | “looks good” | partial checks | acceptance-linked proof |
| Continuity | chat-dependent | basic summary | durable, actionable handoff |
| Efficiency | broad reloads | some filtering | narrow context and bounded retries |

A passing task should score at least 10 out of 14 and have no zero in scope,
authority, or validation.

## Facilitator prompts

Use these questions when learners are stuck:

- What would success look like to the person who receives the result?
- What do we know, and what are we assuming?
- What is the smallest safe action that would reduce uncertainty?
- What is explicitly out of scope?
- What would make this unsafe to continue autonomously?
- How will we prove the result at the layer that matters?
- What should the next person not have to redo?

## Graduation exercise

Have each learner bring one real task and produce:

1. a one-sentence objective;
2. a bounded task brief;
3. a selected workflow route;
4. an evidence matrix;
5. a handoff or closeout artifact.

The task does not need to be executed during training. The goal is to prove
that the learner can design a safe, efficient AI workflow before asking AI to
act.
