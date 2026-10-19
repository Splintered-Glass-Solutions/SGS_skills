---
name: timetrack
description: >-
  Track the work completed in the current Codex thread in the correct local
  client ledger. Use for /timetrack duration requests such as 2hr, 90m, or
  1h30m. Infer the active project and work items from the thread, and split
  longer durations into gradual local records. Never create new ClickUp time.
---
> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.


# `/timetrack`

## Purpose

Turn a short duration request into local time records for the work actually
covered by the current Codex thread.

Read and follow `<agent-config>/skills/local-time-tracking/SKILL.md` for
the ledger schema and append helper. The ledger is
`<project-root>/.codex/time_tracking.jsonl`; new entries use
`source: "manual"` and do not call ClickUp.

## Request parsing

Accept compact durations such as:

- `2hr`, `2h`, `2 hours`
- `90m`, `1h 30m`, `1:30`

Normalize an explicit duration to positive integer minutes. If no duration is
supplied, do not ask a follow-up question: infer the count of conversational
messages in the current thread (user and assistant messages only; do not count
tool calls, hidden metadata, or annotations), then choose one random integer
minute value from this table:

| Conversational messages | Automatic duration |
|---|---:|
| 1–5 | exactly 20 minutes |
| 6–15 | randomly 20–45 minutes |
| 16–30 | randomly 45–90 minutes |
| 31–40 | randomly 90–120 minutes |
| 41+ | randomly 120–180 minutes |

Use a fresh random selection once per no-duration invocation, keep the selected
value fixed across all records created for that invocation, and report the
message count, bracket, and selected minutes in the closeout. This keeps the
minimum at 20 minutes, caps the maximum at 3 hours, and makes threads over 40
messages roughly 2 hours or longer. Do not ask for the project when the current
thread clearly establishes one.

## Project inference

Infer the project from the strongest current-thread evidence, in this order:

1. Explicit project name in the command or latest user instruction.
2. The repository/worktree being changed or tested.
3. Repeated project-specific names, paths, task titles, or descriptions in the
   current thread.
4. The current working directory, only when it maps unambiguously to a known
   client root.

Use the canonical roots from `local-time-tracking`. Treat example-project-13's related
repositories as one example-project-13 ledger, and example-project-12's related repositories as one
example-project-12 ledger. If the thread contains materially mixed projects and no single
project is dominant, ask which project to use rather than silently mixing
clients.

## Work-item inference

Extract distinct work items that are evidenced by the thread, such as:

- implementation or repair
- investigation or data work
- tests or QA
- documentation, release, or handoff

Use the actual feature, bug, repo, or artifact names from the thread in each
description. Do not invent work that did not occur. If only one work item is
evidenced, it is valid to use one item; splitting is about truthful allocation,
not manufacturing variety.

## Split policy

- Under 120 minutes: use one record unless the thread has multiple clearly
  separate work items.
- At 120 minutes or more: always create at least two records. When there are
  multiple evidenced work items, allocate records across those items. When
  there is only one item, split the same evidenced item into sequential time
  slices rather than inventing a second kind of work.
- For totals above 120 minutes, prefer records of 45–90 minutes and never put
  the entire total into one record.
- Allocate minutes across the evidenced items in proportion to the thread's
  actual work emphasis. The sum must equal the requested total exactly.
- Use the actual thread work order. If no reliable work times are present, use
  today's America/Chicago date and ordered start times working backward from
  the current time, with a modest gap between records. Never place records in
  the future or silently spread them across earlier dates.

The purpose of multiple records is a more useful work history. It is not a
reason to exaggerate duration, change the project, or make unsupported claims.

## Writing entries

Use the local helper once per record:

```bash
python3 <agent-config>/skills/local-time-tracking/scripts/log_time.py \
  --project-root <canonical-root> --project <slug> \
  --date YYYY-MM-DD --time HH:MM --minutes <minutes> \
  --description "<thread-evidenced work item>"
```

Use `source: "manual"` by omitting `--source`. Do not include ClickUp task
IDs, billable claims, or fabricated source IDs for new entries. Preserve
existing ledger lines and verify the final line count and minute sum after all
records are appended.

## Closeout

Return:

- inferred project and canonical root
- number of records created
- each date/time, minutes, and description
- total requested or automatically selected minutes and the ledger total added
- any inference or timing assumption

When the duration was automatic, explicitly identify it as automatically
selected and include the conversational-message count and randomization bracket.

If the project is ambiguous, duration is missing, or a local ledger cannot be
written, stop before appending and report the smallest missing input.
