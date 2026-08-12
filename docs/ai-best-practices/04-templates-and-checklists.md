# 4. Templates and Checklists

These templates are intentionally short. Add detail only when the risk or
complexity requires it.

## Universal task brief

```text
Objective:
Why it matters:
Requested outcome:
In scope:
Out of scope:
Current evidence:
Target repository / system:
Authority granted:
Authority not granted:
Acceptance criteria:
Required proof:
Stop conditions:
First safe action:
```

## Batch Brief

```text
Batch ID:
Scope title:
Objective:
Included items:
Excluded items:
Affected repositories:
Affected surfaces:
Overlap zones:
Dependencies:
Acceptance criteria by item:
Focused validation:
Broad validation:
Risks:
Decision-critical questions:
Fresh baseline required:
```

## Delegation packet

```text
Role:
Repository / worktree:
Objective:
In-scope paths or search targets:
Out-of-scope areas:
Inputs and known evidence:
Expected return:
Validation commands:
Stop conditions:
Do not deploy / send / mutate:
```

## Debugging worksheet

```text
Observed behavior:
Expected behavior:
Smallest reproduction:
Relevant logs / request IDs / files:
Current data or API contract:
Hypothesis:
Focused regression test:
Smallest proposed change:
Validation result:
Residual risk:
```

## Hotfix checklist

- [ ] Incident and affected surface confirmed.
- [ ] Current target and baseline rechecked.
- [ ] Change is narrow and reversible or forward-fixable.
- [ ] Regression reproduction or test exists.
- [ ] Focused validation passed.
- [ ] Relevant smoke or browser check passed.
- [ ] Security, data, and compatibility impact reviewed.
- [ ] Deployment target is explicit.
- [ ] Deployed behavior verified separately from local behavior.
- [ ] Communication states exact proof and remaining gaps.

## Evidence matrix

| Surface | Status | Evidence | Remaining gap |
|---|---|---|---|
| Local files |  |  |  |
| Local tests |  |  |  |
| Committed |  |  |  |
| Merged branch |  |  |  |
| Hosted environment |  |  |  |
| Provider / data path |  |  |  |
| Authenticated workflow |  |  |  |
| Customer-visible journey |  |  |  |

## Accepted-state checkpoint

```text
Objective:
Accepted result:
Decisions:
Constraints:
Proof gathered:
Open questions:
Current blocker:
Exact next action:
Source fingerprints or commit IDs:
```

## Handoff template

```text
Continue from:

Purpose:
Current state:
Repositories / branches / worktrees:
Changed files or artifacts:
Decisions made:
Proof gathered:
Remaining work:
Blockers / approvals needed:
Do not redo:
First next action:
Suggested skills:
```

## Prompt quality checklist

Before sending a substantial AI request, confirm:

- [ ] The outcome is stated in one sentence.
- [ ] The audience and target system are clear.
- [ ] Scope and exclusions are explicit.
- [ ] Existing evidence is named.
- [ ] The requested authority is clear.
- [ ] Success and failure conditions are observable.
- [ ] The output format is appropriate.
- [ ] The task has a bounded first action.
- [ ] The AI knows when to stop and ask.

## Closeout checklist

- [ ] Every requested item is marked complete, deferred, blocked, or excluded.
- [ ] Tests and checks are named with results.
- [ ] Local, merged, hosted, provider, authenticated, and customer-visible
      status are separated.
- [ ] Unrelated changes remain preserved.
- [ ] No secrets or temporary artifacts were included.
- [ ] The next action is obvious.
- [ ] The durable state artifact is current.
