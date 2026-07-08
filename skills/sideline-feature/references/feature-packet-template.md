# Sidelined Feature Packet Template

Use this structure when the target repo has no stronger local template.

```md
---
id: <feature-id>
title: <Feature Name>
doc_type: feature_plan
system: <shared|repo-or-service-name>
canonical_for:
  - planning context for <feature>
not_canonical_for:
  - current production behavior
  - committed implementation details
  - customer-facing commitments
owner: <owner>
status: draft
source_repos:
  - <repo>
source_paths:
  - <path-or-source-doc>
last_verified: YYYY-MM-DD
review_cycle_days: 30
audience:
  - product
  - engineering
  - ai_agents
tags:
  - sidelined-feature
  - <topic>
---

# <Feature Name>

Date: YYYY-MM-DD

## Summary

<One-paragraph feature summary and why it is being sidelined.>

## Product Thesis

<What problem it solves and for whom.>

## Recommendation

<Current best path, including what to keep, defer, or avoid.>

## User-Facing Implications

<How the feature changes workflow, UI, permissions, support, pricing, setup, or risk.>

## Non-Goals

<What should not be included in the first pass.>

## Proposed Scope

<First release, later release, and explicit exclusions.>

## Work Packages

<Repo-by-repo or phase-by-phase execution plan.>

## Validation Plan

<Tests, QA, live proof, docs, customer review, or approvals needed.>

## Risks

<Risks and mitigations.>

## Open Questions

<Decisions to make before implementation resumes.>

## Recommended Next Step

<Smallest next action to restart the work.>
```

