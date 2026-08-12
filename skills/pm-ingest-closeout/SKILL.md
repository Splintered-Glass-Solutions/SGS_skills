---
name: pm-ingest-closeout
description: >-
  PM ingest closeout: use when the user highlights or references a worker,
  bounded agent, or project-thread closeout and wants the PM thread to ingest
  its WORK_LEDGER_UPDATE, append it to the portfolio work ledger, validate the
  ledger, refresh current-state, and update active/blocked/waiting queues.
---

# PM Ingest Closeout

## Overview

Use this skill from the project-management thread to close the loop on worker
or project-thread closeouts. The goal is to stop leaving worker lifecycle
updates in chat: extract the closeout's `WORK_LEDGER_UPDATE`, append it to the
durable work ledger, validate it, regenerate current-state, and return the
updated queue status.

This is a local PM control-plane workflow. It does not deploy, send external
messages, mutate production, create threads, or approve gated actions.

## Inputs

Use the highlighted text, slash-command `$ARGUMENTS`, pasted closeout, closeout
artifact path, or current thread context.

Accepted input shapes:

- a full worker closeout containing `WORK_LEDGER_UPDATE:`
- a file path containing the closeout text
- a project-thread closeout pasted into the PM thread

If the closeout is only referenced by thread ID or vague summary and no
thread-reading tool is available, ask the user for the closeout text or artifact
path instead of guessing.

## Required Preflight

1. Read `$CODEX_HOME/portfolio/work-ledger.md`.
2. Read `$CODEX_HOME/portfolio/templates/worker-closeout-contract.md`.
3. Read `$CODEX_HOME/portfolio/pm-ledger-clickup-model.md`.
4. Read `$CODEX_HOME/skills/pm-project-agent/SKILL.md` when ingesting
   a closeout from a persistent Project Agent thread.
5. Read `$CODEX_HOME/portfolio/current-state.md` when it exists, so
   the before/after queue change is clear.
6. Confirm the closeout contains a parseable `WORK_LEDGER_UPDATE` JSON object
   or JSON array. If not, do not append anything; report the exact missing
   closeout field.

## Ingestion Command

Prefer the deterministic script:

```bash
node $CODEX_HOME/portfolio/scripts/ingest-closeout.mjs --closeout-file /path/to/closeout.txt
```

For selected or pasted closeout text, pipe the selected text on stdin:

```bash
node $CODEX_HOME/portfolio/scripts/ingest-closeout.mjs --stdin
```

The script:

- extracts `WORK_LEDGER_UPDATE`
- accepts one JSON object or an array of JSON objects
- validates required work-ledger fields and enum values
- appends only events whose `event_id` is not already present
- treats identical duplicate `event_id` values as already ingested
- fails on conflicting duplicate `event_id` values
- runs `validate-work-ledger.mjs`
- regenerates `current-state.json` and `current-state.md`
- runs `validate-current-state.mjs`

Use `--dry-run` when the user asks to preview an ingestion without appending.

## Rules

- Append only exact `WORK_LEDGER_UPDATE` JSON from the closeout. Do not invent
  or rewrite worker state unless the user explicitly asks for a manual repair.
- If the closeout reports `STATUS: blocked` or `STATUS: needs_approval`, ingest
  the work-ledger event when valid, then report the blocked/waiting queue and
  any `ACTION_PROPOSAL` or `APPROVAL_LEDGER_UPDATE` separately.
- Do not modify the approval ledger automatically unless the user explicitly
  asks to ingest an approval update too.
- Do not mark a work item complete unless the closeout's own ledger event says
  `status_after: completed`.
- If a persistent Project Agent closeout shows the Project Agent directly
  executed substantive implementation, QA, research, screenshots, repo hygiene,
  or validation instead of supervising a worker, ingest any valid lifecycle event
  but also report drift as `project_agent_executed_worker_work`. The next safe
  action should be to route remaining execution to a bounded worker and keep the
  Project Agent in a monitor/review role.
- The local work-ledger/current-state update is the required source of truth.
  Create ClickUp only for actionable follow-ups surfaced by the closeout
  (the user decision, worker/project follow-up, failed validation retest/fix, or
  blocked escalation), only when authorized, and only after checking dedupe key
  `pm:work:<project>:<work_id>:<slug>`. Report `ClickUp not created` when
  creation is not authorized or fails.
- After ingestion, read the regenerated
  `$CODEX_HOME/portfolio/current-state.json` or `.md` and report:
  - event IDs appended or already present
  - work IDs affected
  - active/delegated/waiting/blocked/completed queue impact
  - validation results
  - ClickUp task created or `ClickUp not created` for actionable follow-ups
  - any missing clean-unreads or approval-ledger follow-up

## Output Shape

Use icon-prefixed PM section headers so closeout ingestion results are easy to
scan. Keep the canonical label text after the icon.

```text
✅ CLOSEOUT INGESTED:
🧾 EVENTS APPENDED:
🟢 ALREADY PRESENT:
🆔 WORK IDS:
📊 QUEUE IMPACT:
✅ VALIDATION:
📌 CLICKUP:
🧭 FOLLOW-UP:
```

For blocked ingestion:

```text
🔴 CLOSEOUT NOT INGESTED:
⚠️ REASON:
🧩 NEXT NEEDED CLOSEOUT FIELD:
🧭 SAFE NEXT STEP:
```
