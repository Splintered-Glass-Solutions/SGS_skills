---
name: to-do-list-planning
description: Turn a bounded set of captured to-do notes into a concise proposed Batch Brief for isolated implementation. Use when the user asks to plan, scope, group, sequence, or prepare related captured items before starting $bulk-edits-thread; do not use for capture-only to-do gathering or implementation.
---

# To-Do List Planning

Turn one related capture set into a decision-ready execution contract. This is
planning only: inspect current state as needed, but do not create a worktree,
branch, product change, deployment, or shared-database mutation.

## Workflow

1. Classify the run as `planning` and stop gathering mode. Identify one batch
   by an explicit batch ID when available; otherwise use the narrowest stated
   product scope. Search only matching captured notes and the active task,
   rather than loading the whole note archive.
2. Check that the candidates share a page/feature surface, repository boundary,
   and test surface. Treat 6–12 items as a guideline, not a target. Split a
   batch at an ownership, API-contract, migration, deployment, or acceptance
   boundary.
3. Inspect the current product and repository state read-only only as far as
   needed to replace assumptions with evidence. Separate confirmed current
   behavior from requested changes and do not treat a captured note as proof
   of a capability or an implementation decision.
4. Identify overlap zones: routes, component families, API contracts,
   migrations, shared fixtures, and affected repositories. If another active
   writable batch overlaps, recommend sequencing rather than parallel editing.
5. Produce one concise proposed Batch Brief with:
   - batch ID and concise scope title;
   - objective, included items, exclusions, and assumptions;
   - acceptance criteria and item IDs;
   - affected repositories and overlap zones;
   - dependencies, risks, and only decision-critical questions;
   - expected validation by item and broad validation;
   - the required fresh-dev baseline check for execution.
6. End at the Batch Brief. It becomes approved only when the user explicitly
   starts the bulk-edit phase. Pass only the accepted brief and necessary
   evidence into `$bulk-edits-thread`; do not replay the capture discussion.

## Handoff Contract

The execution task must create a committed Batch Manifest from the accepted
Batch Brief at `.codex/batches/<batch-id>.md` in each affected worktree. The
manifest carries the baseline SHA, planned items, touched areas, commits,
validation, deferred work, and final closeout integration SHA through
`collapse-bulk-edits-thread`.

If planning reveals incomplete scope, incompatible product directions, or a
risky schema/permission decision, stop with the smallest decision needed. Do
not create a vague batch merely to begin editing.
