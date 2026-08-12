# AI Best Practices Training Package

Status: Draft curriculum package
Audience: Operators, product managers, engineers, and team leads using AI for real work
Format: Self-study, team workshop, or facilitator-led training

## Purpose

This package teaches people how to use AI as a reliable work partner across
planning, research, coding, debugging, QA, communication, and multi-project
operations. It treats AI work as a managed workflow with explicit scope,
evidence, authority, and handoffs.

The goal is not to make people write longer prompts. The goal is to help them
consistently produce useful outcomes without losing context, damaging existing
work, or confusing a plausible answer with verified reality.

## Learning outcomes

By the end, a learner should be able to:

- choose the right AI mode for a task instead of starting with an oversized
  autonomous request;
- separate capture, planning, implementation, validation, deployment, and
  communication authority;
- run a bounded multi-project or multi-repo effort without mixing unrelated
  work;
- debug from evidence and a concrete hypothesis rather than guess-and-retry;
- execute a hotfix with a narrow blast radius and a clear rollback or forward-fix
  path;
- use AI efficiently by controlling context, outputs, retries, and durable state;
- hand work to another person or AI task without requiring the original
  conversation;
- state exactly what is local, merged, deployed, authenticated, provider-backed,
  or customer-visible.

## Curriculum map

1. [The AI operating model](01-operating-model.md)
2. [Task playbooks](02-task-playbooks.md)
3. [Codex workflow and skill routing](03-codex-workflow.md)
4. [Templates and checklists](04-templates-and-checklists.md)
5. [Facilitator guide and exercises](05-facilitator-guide.md)

## Recommended learning paths

### Individual operator, 60 minutes

Read the operating model, then complete the planning, debugging, and handoff
templates against one real low-risk task.

### Engineering team, 2 hours

Teach the operating model, run the multi-repo and hotfix exercises, and review
the evidence matrix as a group.

### Leadership or PM team, 90 minutes

Focus on task classification, portfolio orchestration, delegation packets,
communication gates, and proof boundaries.

### New Codex user, one week

Use one small task each day: capture, plan, execute, verify, and close. Do not
start with a large autonomous build.

## The core loop

```text
Capture
  ↓
Clarify the outcome and authority
  ↓
Plan a bounded slice
  ↓
Choose the right execution lane
  ↓
Implement or investigate
  ↓
Validate the actual result
  ↓
Reconcile, communicate, or hand off
  ↓
Preserve only the state needed next
```

## Definition of good AI work

Good AI work is:

- useful: it moves the real objective forward;
- bounded: the scope and stop conditions are explicit;
- reversible: risky actions have a safe path back or forward;
- evidence-backed: claims match the checks actually performed;
- economical: context and retries are controlled across the whole job;
- resumable: another person or task can continue from a compact artifact;
- honest: uncertainty, blockers, and proof gaps are visible.

## Facilitator note

Use the examples as patterns, not as rigid scripts. The right workflow for a
one-file typo is intentionally lighter than the right workflow for a
multi-repo feature touching production data.
