# PM Clean Unreads Agent Playbook

This is a platform-neutral version of the `pm-clean-unreads` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

PM clean unreads: use for PM-style cleanup of unread agent threads when the user wants to find threads whose work is actually done and safe to mark read. Identifies unread project/work threads where the feature finish-line has run, required local and dev/hosted testing is complete when applicable, deployment or dev-environment validation is proven, no approvals/blockers/follow-ups remain, and the thread can be marked read or returned as a ready-to-mark-read queue.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

# PM Clean Unreads

## Overview

Run a conservative unread cleanup pass for the agent project-management hygiene.
The goal is to remove unread noise only when the thread is truly complete and
no longer needs the user's attention.

Do not treat "agent said done" as enough. A thread is cleanable only when the
current evidence proves completion, finish-line validation, and the correct
environment proof for that project.

## Mandatory Incomplete-Thread Rule

If a thread is not complete, has incomplete work, has remaining action items,
is missing finish-line/dev proof, or contains any next step for the user or a
worker, it must stay unread. If explicit mark-unread tooling is available and
the run is authorized to clean unread state, mark or leave that thread unread
instead of clearing it.

For every thread kept unread, report the next needed step. The report should
make clear whether the blocker is worker continuation, the user approval,
failed validation, missing evidence, or unclear status.

Persistent Project Agent threads are PM/orchestrator lanes, not execution
workers. If a Project Agent thread directly implemented, tested, researched, or
QA'd substantive work that should have gone to a bounded worker, keep the
thread unread and classify the follow-up as
`project_agent_executed_worker_work`. The next needed step is to restore the PM
pattern: route remaining execution to a bounded worker, ingest any valid
closeout, and have the Project Agent review/report upward.

## Required Preflight

Read these before broad cleanup:

- `<agent-config>/skills/project-portfolio-manager/SKILL.md` (`pm-project-portfolio-manager`)
- `<agent-config>/portfolio/project-registry.md`
- `<agent-config>/portfolio/thread-registry.md`
- `<agent-config>/portfolio/approval-ledger.md`
- `<agent-config>/portfolio/work-ledger.md`
- `<agent-config>/portfolio/work-ledger.jsonl`
- `<agent-config>/portfolio/pm-ledger-clickup-model.md`
- `<agent-config>/portfolio/templates/clean-unreads-report.md`
- `<agent-config>/portfolio/standards-registry.md`

## Current PM Thread Exclusion

Always exclude the current PM/project-management thread that is running the
clean-unreads pass from unread classification and cleanup actions. Do not mark
the current thread read, do not mark it unread, and do not report it as an
active/incomplete thread. If the current thread appears in unread thread
tooling, classify it internally as `excluded_current_pm_thread` and omit it
from the output counts except for an optional one-line note under
`PROOF GATHERED`.

Use agent thread tooling when available:

- `list_threads` to find unread threads.
- `read_thread` to inspect the latest status and closeout.
- A future explicit mark-read tool may be used only after eligibility is proven
  and the run has authority to mark read.
- A future explicit mark-unread tool may be used only to preserve attention on
  threads classified `keep_unread_*` when incomplete work or action items
  remain.

Do not archive threads as a substitute for marking them read unless the user
explicitly asks to archive.

## Thread Context Fields

For every reported thread, include enough context for the user to recognize it
without opening the sidebar:

- `thread_title`: the exact agent thread title from `list_threads` or
  `read_thread`.
- `thread_id`: the exact thread id.
- `thread_link`: a clickable deep link only when thread tooling returns a
  stable URL or deep-link target. If no stable link is available, write
  `unavailable` and keep the `thread_id` visible.
- `last_message_sample`: the final paragraph of the latest meaningful
  user/assistant message or closeout, trimmed to 1-3 sentences. Prefer the
  last paragraph because it usually contains the latest state, next step, or
  blocker. Do not paste long logs, secrets, stack traces, or large artifacts.

If the latest message is a structured closeout, use the last useful paragraph
or field, such as `NEXT_RECOMMENDED_ACTION`, `HANDOFF_RECEIPT.next_safe_prompt`,
`Remaining`, or the final blocker/next-step paragraph. If the latest message is
only an acknowledgement with no useful context, say `acknowledgement only`.

## Eligibility Test

A thread is `ready_to_mark_read` only when all applicable checks pass:

1. The latest thread status is `completed`, not `active`, `inProgress`,
   `blocked`, errored, or waiting for user input.
2. The final answer or closeout says the scoped work is complete.
3. Feature finish-line has run when the work involved product/code/UI behavior,
   and the closeout includes exact checks or artifact paths.
4. Local validation is present for code changes: tests, lint/type/build, browser
   screenshots, smoke checks, or an explicit reason validation is not
   applicable.
5. Dev/hosted validation is present when applicable:
   - For deployable app work, dev deployment or hosted/dev smoke is proven when
     the project normally requires it.
   - If no dev environment exists, the thread must explicitly separate local
     proof from hosted/prod proof and name the missing environment.
   - Production-only hotfixes are not cleanable until the approved production
     deploy/hotfix and post-deploy verification are complete.
6. The approval ledger has no pending item tied to the thread's work.
7. The work ledger has no current `active`, `delegated`, `waiting`, or `blocked`
   event for the same `work_id` after the alleged completion.
8. The final answer does not contain a pending next step that the user must
   review, approve, send, deploy, stage, commit, or choose.
9. No unhandled `ACTION_PROPOSAL`, `blocked_by`, `needs_approval`, failed test,
   failed hosted smoke, or "not green" status remains.

## Classifications

Classify each unread thread as exactly one:

- `ready_to_mark_read`: all eligibility checks pass.
- `keep_unread_active`: thread is still running, waiting, or mid-validation.
- `keep_unread_needs_the user`: the user decision, approval, review, send,
  deploy, commit, or prioritization is still needed.
- `keep_unread_failed_or_not_green`: finish-line, dev, hosted, or production
  validation failed or is incomplete.
- `keep_unread_unclear`: evidence is insufficient; provide the exact missing
  proof.
- `project_agent_executed_worker_work`: persistent Project Agent directly did
  worker-scoped execution instead of routing/supervising a bounded worker.
- `not_project_work`: unread thread is personal/admin/non-project noise; do not
  mark read unless the latest request is plainly done and no follow-up remains.

## Dev Environment Rule

"Deployed and tested in dev" means one of:

- A named dev/staging/preview environment was deployed or updated and tested.
- The repo/project has no dev environment, and the closeout explicitly says so
  while providing local plus hosted/prod boundary notes.
- The work was documentation/planning/read-only and did not require deployment.

Do not mark read when a deployable feature is only locally green and the thread
still says PR, commit, push, dev deploy, preview verification, or production
hotfix remains.

## Cleanup Actions

Default to read-only classification unless the user explicitly asks to clean.

## Durable Run Artifact

Every clean-unreads run must save a local report before returning:

```text
<agent-config>/portfolio/reports/clean-unreads/YYYY-MM-DD-HHMM.md
```

The report is the local ledger surface for unread observations. It must include:

- run timestamp and scope
- excluded current PM thread
- `READY_TO_MARK_READ_QUEUE`
- `KEEP_UNREAD_QUEUE`
- next step per kept-unread thread
- `THREADS_ACTUALLY_CLEARED`
- `THREADS_LEFT_OR_MARKED_UNREAD`
- ClickUp candidates and `ClickUp not created` entries
- dedupe keys for every reported thread:
  `pm:unread:<project-or-source>:<thread_id>:<classification-or-work-slug>`

Use `<agent-config>/portfolio/templates/clean-unreads-report.md` as the
required section template when writing the report.

Do not create ClickUp tasks for `ready_to_mark_read`, passive active/waiting
status, duplicate observations, completed/no-op threads, or items with no next
action. Only create or propose ClickUp tasks when the kept-unread item has an
actionable follow-up: the user decision, worker/project follow-up,
failed/not-green validation, blocked escalation, or communication response.
If ClickUp creation is not explicitly authorized or fails, keep the report as
source of truth and write `ClickUp not created`.

When mark-read tooling is available and the run is authorized:

1. Mark only threads classified `ready_to_mark_read`.
2. Do not mark active, blocked, failed, or ambiguous threads read.
3. If mark-unread tooling is available, mark or leave all `keep_unread_*`
   threads unread so unresolved work stays visible.
4. Record the count and thread IDs for both read and kept-unread actions in the
   run artifact and final response.
5. Append a compact work-ledger event if this was a portfolio cleanup run and
   the cleanup materially changed PM state.
6. Validate the work ledger after appending.

When mark-read tooling is not available, return a `READY_TO_MARK_READ_QUEUE`
with exact thread IDs and evidence, plus a `KEEP_UNREAD_QUEUE` with the next
needed step for each incomplete thread. Do not archive as a workaround.

## Output Shape

Use icon-prefixed PM section headers so unread cleanup reports are scannable at
a glance. Keep the canonical label text after the icon.

```text
🧹 CLEAN UNREADS STATUS:
✅ READY TO MARK READ:
🟡 KEEP UNREAD - ACTIVE:
⚠️ KEEP UNREAD - NEEDS PRESTON:
🔴 KEEP UNREAD - FAILED OR NOT GREEN:
❓ KEEP UNREAD - UNCLEAR:
📥 NOT PROJECT WORK:
🧭 NEXT NEEDED STEPS:
✅ ACTION TAKEN:
🧾 WORK LEDGER UPDATES:
📄 RUN ARTIFACT:
📌 CLICKUP TASKS:
🧾 PROOF GATHERED:
⏭️ NEXT CHECK:
```

For each ready item include:

```text
- thread_title:
  thread_id:
  thread_link:
  last_message_sample:
  project:
  proof:
  finish_line:
  dev_or_hosted_validation:
  reason_safe_to_mark_read:
  dedupe_key:
  clickup: not_actionable
```

For each kept-unread item include:

```text
- thread_title:
  thread_id:
  thread_link:
  last_message_sample:
  project:
  classification:
  why_not_complete:
  next_needed_step:
  dedupe_key:
  clickup: created | ClickUp not created | not_actionable
```

Keep the response compact. Prioritize false-negative safety over clearing more
unreads.

