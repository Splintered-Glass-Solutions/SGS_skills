# 2. Task Playbooks

Each playbook gives a default route. Use the lightest route that preserves
correctness and safety.

## Playbook A: Quick lookup or communication

### Use when

The task has one clear question, one small answer, or one routine message.

### Route

1. Identify the recipient or answer contract.
2. Inspect only the necessary source.
3. Produce the answer or draft.
4. Verify any live link or mutable fact.
5. Stop.

### Do not

Start a planning or autonomous build workflow for a one-step task.

## Playbook B: Capture a future task

### Use when

You want to remember work without deciding how or when to execute it.

### Output

One concise item containing the desired outcome and enough context to recognize
it later.

### Stop condition

The item is saved. No repository inspection or implementation follows.

## Playbook C: Multi-project or multi-repo work

### Use when

The task crosses projects, repositories, services, worktrees, or ownership
boundaries.

### Route

1. Define the portfolio outcome, not just a list of tickets.
2. Inventory active work and dependencies.
3. Separate projects into independent workstreams.
4. Assign one owner and one evidence contract per workstream.
5. Identify shared contracts: APIs, schemas, fixtures, providers, or deploys.
6. Sequence overlapping work; do not edit the same surface concurrently.
7. Delegate bounded packets with exact paths, exclusions, and return format.
8. Ingest each result into a central status ledger.
9. Reconcile cross-project dependencies before declaring completion.

### Required status fields

- objective;
- current state;
- owner or worker;
- repository and branch/worktree;
- baseline and current commit;
- proof gathered;
- blocker or decision needed;
- next action;
- external or deployment status.

### Failure to avoid

Treating several repositories as one giant worktree with unclear ownership.

## Playbook D: Related coding batch

### Use when

Several edits share a product surface, repository boundary, test surface, and
acceptance boundary.

### Route

```text
Capture → Batch Brief → Approved isolated worktree → Atomic edits
→ Focused tests → Local runtime check → Audited local-dev merge
```

### Batch Brief must answer

- What is the objective?
- Which items are included?
- What is explicitly excluded?
- Which repositories and surfaces are affected?
- What overlap zones could conflict?
- What proves each item is complete?
- What is the fresh development baseline?
- Which questions block execution?

### Failure to avoid

Using a fixed item count as the definition of a batch. Split at ownership,
contract, migration, deployment, or acceptance boundaries instead.

## Playbook E: Debugging

### Use when

The system behaves incorrectly and the cause is not yet known.

### Route

1. Describe the observed behavior and expected behavior separately.
2. Capture the smallest reproducible input.
3. Inspect the actual execution path and relevant data contract.
4. State one concrete hypothesis before editing.
5. Add or run a focused regression check.
6. Make the smallest fix that tests the hypothesis.
7. Re-run the focused check.
8. Run adjacent validation for regression risk.
9. Record what remains uncertain.

### Debugging contract

```text
Observed:
Expected:
Reproduction:
Evidence:
Hypothesis:
Smallest test:
Change:
Result:
Remaining risk:
```

### Failure to avoid

Blindly retrying a failed command without changing the hypothesis, input,
scope, or tool.

## Playbook F: Hotfix

### Use when

A known issue needs a narrow, urgent repair.

### Route

1. Confirm the incident and affected surface.
2. Establish the current deployed or integration baseline.
3. Constrain the change to the smallest safe fix.
4. Add a regression test or executable reproduction.
5. Run focused validation and relevant smoke checks.
6. Review security, data, and compatibility risk.
7. Deploy only through the established release path and explicit target.
8. Verify the deployed behavior separately from local proof.
9. Communicate the result with exact evidence and remaining limitations.

### Stop conditions

Stop for unclear target, destructive data work, permissions, billing,
persistent credentials, or an expanded scope disguised as a hotfix.

## Playbook G: New feature end to end

### Use when

The user wants AI to carry a feature through implementation, tests, docs,
integration, and delivery.

### Route

1. Prepare the environment, repository, accounts, and acceptance bar.
2. Define a concrete goal and accepted scope.
3. Decompose into independent slices.
4. Keep architecture and final review in the main thread.
5. Delegate bounded research, coding, testing, or log reduction.
6. Maintain one compact execution ledger.
7. Validate each truth surface: local, merged, hosted, provider, authenticated,
   and customer-visible as applicable.
8. Stop at genuine approval or access gates.
9. Finish with proof, risks, deferred work, and the next action.

### Failure to avoid

Calling a feature complete because local tests pass while hosted, provider, or
customer-visible proof is still missing.

## Playbook H: QA and review

### Use when

The objective is to find defects, verify a feature, or create durable QA
evidence.

### Route

1. Define the scope and acceptance contract.
2. Run deterministic checks first.
3. Use browser or visual checks where user behavior matters.
4. Record each check as pass, fail, blocked, skipped, or unavailable.
5. Attach evidence and exact failure boundaries.
6. Fix only authorized, understood issues.
7. Retest the affected path.
8. Separate product failures from environment, account, provider, or data
   blockers.

### Failure to avoid

Flattening “blocked,” “not run,” and “passed” into one green summary.

## Playbook I: Research, transcript, or external-source synthesis

### Use when

The task requires source retrieval, document analysis, transcript recovery, or
evidence-backed synthesis.

### Route

1. Define the question and acceptable source types.
2. Search indexes, metadata, and durable notes before opening large sources.
3. Read the smallest relevant excerpts.
4. Record source locations, dates, IDs, and limitations.
5. Separate verified facts, inference, assumptions, and open questions.
6. Save a durable summary when the research may be reused.

### Failure to avoid

Presenting a fallback source, old transcript, or inferred answer as if it were
the original authoritative evidence.

## Playbook J: Handoff and continuation

### Use when

The task is pausing, changing threads, approaching compaction, or moving to
another worker.

### Handoff contents

- objective;
- current status;
- exact repositories, branches, worktrees, and commits;
- changed files or artifacts;
- proof gathered;
- decisions made;
- remaining work;
- blockers and approval gates;
- first next action;
- suggested skills.

### Failure to avoid

Creating a narrative recap that omits exact state or asks the next worker to
reconstruct the original investigation.

## Playbook K: Communication

### Use when

The work needs a text, email, status update, client message, or task record.

### Route

1. Identify audience, channel, purpose, and sensitivity.
2. Verify the facts and links being communicated.
3. Draft in the channel's natural cadence.
4. Keep one clear next action.
5. Send only when the user has authorized the send and the channel is correct.

### Failure to avoid

Sending a polished message that overstates deployment, customer impact, or
completion.
