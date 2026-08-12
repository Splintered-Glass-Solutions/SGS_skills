# 1. The AI Operating Model

## The central idea

AI is most reliable when treated as a sequence of bounded work modes rather
than as one giant instruction.

```text
Intent → Scope → Evidence → Action → Proof → State transition
```

Each step answers a different question:

| Step | Question | Typical failure when skipped |
|---|---|---|
| Intent | What outcome do we actually want? | AI solves the wrong problem |
| Scope | What is included, excluded, and authorized? | Scope creep or unsafe action |
| Evidence | What is true right now? | AI builds on stale assumptions |
| Action | What is the smallest useful next move? | Overbuilding or broad mutation |
| Proof | How do we know it worked? | Green-looking but unverified work |
| State transition | What is now local, merged, deployed, or handed off? | False completion claims |

## Five modes of AI work

### 1. Capture mode

The objective is preservation, not action.

Use capture mode for ideas, requests, bugs, and future work that should not
immediately consume engineering time. Capture one clear item and stop.

### 2. Planning mode

The objective is a decision-ready contract.

Planning should identify the goal, boundaries, dependencies, acceptance
criteria, risks, and first safe action. Planning should not quietly become
implementation.

### 3. Execution mode

The objective is a bounded change or investigation.

Execution needs a defined target, ownership, working context, validation plan,
and stop condition. Larger work should have an isolated branch, worktree, or
task lane.

### 4. Verification mode

The objective is to test the actual result against the intended behavior.

Verification is not the same as reading the diff, getting HTTP 200, seeing a
successful build, or receiving a plausible AI response.

### 5. Handoff mode

The objective is continuity.

A good handoff contains the current state, exact evidence, remaining work,
constraints, and the next action. It does not require replaying the original
conversation.

## Authority is layered

AI tasks often mix different kinds of permission. Separate them explicitly:

- inspect files or data;
- edit local files;
- create a branch or worktree;
- commit changes;
- merge to a local integration branch;
- deploy to development or production;
- mutate shared data;
- change permissions, billing, or credentials;
- send an external message.

Approval for one layer does not automatically authorize the next layer.

## Proof layers

Use precise language about where a result exists:

1. **Local:** the current files or local runtime show the behavior.
2. **Committed:** the work is recorded in a commit.
3. **Merged:** the commit is reachable from the intended integration branch.
4. **Hosted:** the target environment is running the change.
5. **Provider-backed:** the external provider or data path works.
6. **Authenticated:** the relevant identity and permissions work.
7. **Customer-visible:** the intended user can complete the real journey.

Never collapse these into one word such as “done.”

## Context is a budget

AI efficiency is not just shorter output. The whole job includes:

- planning calls;
- source selection;
- model input;
- tool definitions and tool output;
- retries;
- validation;
- handoffs;
- human repair.

The best economy pattern is:

1. search before opening large sources;
2. read the smallest useful slice;
3. use deterministic tools for exact work;
4. preserve an accepted-state checkpoint;
5. revise from the accepted result plus the requested delta;
6. change the hypothesis before retrying.

## The human remains the system owner

AI can investigate, propose, implement, test, and summarize. The human still
owns product intent, risk tolerance, permission, external commitments, and
the meaning of success.

The best collaboration is not “AI does everything.” It is “AI carries the
repeatable work while human judgment stays at the decisions that matter.”

## Common anti-patterns

### The giant prompt

One request asks AI to inspect every repo, fix every issue, deploy everything,
and notify everyone. This creates an unclear success bar and makes failure
localization difficult.

### The plausible-answer trap

The response sounds correct, so it is treated as verified. Require source
locations, commands, tests, screenshots, request IDs, or explicit uncertainty.

### The stale-context trap

AI continues from an old branch, old deployment, old screenshot, or old
decision. Recheck mutable facts cheaply before acting.

### The silent-scope trap

The task grows because adjacent work appears easy. Record additions as
separate scope, a batch amendment, or deferred follow-up.

### The context-replay trap

Every continuation reloads the full conversation. Carry forward the accepted
artifact, proof, decisions, and open questions instead.
