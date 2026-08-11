# User Story Execution Contract

Instantiate this contract from the user's shorthand. Omit sections that are not
applicable, but never omit authority, evidence, repair, or proof boundaries.

## Objective

- Story name:
- Actor:
- Organization/account:
- Business outcome:
- Final observable result:

## Execution Boundary

- Current repo/worktree/branch:
- Must remain on current branch/thread:
- Local code changes:
- Remote database target and permitted operations:
- RLS/permission authority:
- Provider/OAuth authority:
- Approved recipients or address pattern:
- Deployment authority:
- Explicitly prohibited operations:
- Token/log policy:

## Prerequisites

- Authentication identity category:
- Required organization configuration:
- Required skills/connectors:
- Existing source content/templates:
- Test-only fixtures to create:
- Tenant-isolation control:

## Step Template

Repeat for every user action:

### Step N — Outcome

**User action**

State the exact UI action or prompt.

**Expected result**

- visible UI result
- authoritative persisted state
- resource/provider/downstream result
- ownership and permission result

**Audit**

- correctness and grounding
- usability and output quality
- source linkage
- tenant isolation/privacy
- failure, loading, retry, or revision behavior

**Evidence**

- URL/record/resource identifiers
- screenshot or browser artifact
- focused test/command
- database or provider proof

**Failure loop**

1. Record actual versus expected.
2. State a concrete root-cause hypothesis.
3. Implement the smallest authorized repair.
4. Run a focused deterministic check.
5. Rerun this step and its direct integration boundary.
6. Continue only after pass or a genuine blocker.

## Cross-Story Acceptance Criteria

- Every source is the intended source and every link works.
- AI output is grounded, specific, useful, and free of invented commitments.
- Created records persist under the correct tenant.
- Independent objects can be revised independently.
- Revisions preserve accessible history where supported.
- Provider actions reach only approved recipients and are proven at draft,
  sent, and received layers as applicable.
- Role-based access proves both permitted and denied cases when relevant.
- Public sharing proves incognito rendering, private-data isolation, and
  revocation when supported.
- Local, remote-database, hosted, provider, public, and customer-visible proof
  remain separate.

## Durable Ledger

Update after every major boundary:

- current step and status
- setup/state changes completed
- evidence captured
- defects and hypotheses
- changed files and stateful operations
- retests completed
- current blocker
- exact next safe action

Never record secrets.

## Final Result

- Headline status:
- Acceptance-criterion-to-proof ledger:
- Repairs and retests:
- Truth matrix:
- Remaining uncertainty:
- Exact next safe action:
