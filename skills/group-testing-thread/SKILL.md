---
name: group-testing-thread
description: Monitor a shared testing or QA discussion thread with a temporary recurring automation, usually every hour for about one day, extract new bug reports, mark each accepted report with 👀, advance locally resolved reports to 🔵, advance dev-deployed and hosted-verified reports to ✅, use orchestrator-mode to dispatch parallel triage and fix slices, batch fixes across one or more repos, run full-suite-tests locally and in the requested hosted environment, deploy through PRs to dev or another non-production target, and post release notes back to the relevant thread. Use when the user asks Codex to watch a group text, Slack, Teams, email, or other testing thread during a coordinated test sweep and fix reported bugs until the temporary testing window ends.
---

# Group Testing Thread

Use this skill to run a temporary QA-response loop during a coordinated testing window. Treat the discussion thread as the intake source, create a disposable monitor, keep a durable checkpoint so reports are not duplicated, fix actionable bugs in batches, validate locally and in the hosted target, and update the same thread with release notes after dev deployment.

Pair this skill with `$orchestrator-mode` to coordinate multiple parallel agents, `$autonomous-feature-build` for each bug fix, and `$full-suite-tests` for local and hosted validation. For broad, noisy, or multi-repo work, use `$session-budget` and `$codex-safe-run` as appropriate.

## Inputs

Identify or ask for the minimum missing inputs:

- Source thread: text thread, Slack channel, Teams chat, email thread, Fathom notes, issue tracker, or pasted transcript.
- Cadence: default to every hour when the user does not specify one.
- Temporary lifetime: default to 24 hours when the user does not specify one.
- Testing window: start time, stop time, or "until user stops it".
- Project scope: repo or repos that may need changes.
- Target environment: usually `dev`, `staging`, or another non-production environment.
- Deployment path: one PR, one PR per repo, existing deploy workflow, or documented non-production promotion path.
- Release-notes destination: default to the same source thread that reported the bugs.
- Approval boundaries: production, billing, permissions, destructive data, real customer messaging, and protected branch changes require explicit approval.
- Persist any explicit non-production deployment permission in the monitor checkpoint and prompt. Treat it as scoped to this monitor and target environment only; it never implies permission for `main` or production.

## Bonfire Messages Preset

When the user says `Bonfire thread`, `Bonfire text thread`, or `Bonfire chat` without naming another service, use the established Apple Messages/iMessage group rather than Slack:

- Messages identifier: `iMessage;+;chat91142418163091161`.
- Known local Messages chat rowid: `2328`; re-resolve the identifier in `~/Library/Messages/chat.db` before relying on the rowid because local rowids can drift.
- Default cadence: hourly.
- Default target: `dev`, with `https://dev.heybonfire.com` as the hosted validation URL.
- Default repo family: begin in `/Users/preston/Code/bonfire`; include `/Users/preston/Code/Bonfire_AI` or `/Users/preston/Code/Bonfire_ETL` only when source tracing proves the bug crosses into those repos.
- Checkpoint by exact incoming message GUID. Use the GUID boundary for delta reads and store rowid/timestamp only as supporting evidence.
- Read the source delta directly from the local Messages database when available. Do not broaden to unrelated chats or reprocess older thread history after a checkpoint is established.
- Treat release-note replies and workflow Tapbacks as authorized only when the current request invokes this skill for that Messages thread. Keep them concise and verify the exact outgoing message or Tapback after writing.

## Temporary Automation

When the user asks for monitoring, create or update a temporary recurring automation rather than relying on the current chat to stay open.

- Search for the `automation_update` tool first, then use the available automation tool for creation, update, inspection, and deletion.
- Set the cadence from the request, defaulting to every hour.
- Set an explicit expiry or kill condition, defaulting to 24 hours after creation.
- Name the automation with the project and testing thread, for example `Bonfire dev group testing thread monitor`.
- Include the source thread, target environment, repos, checkpoint path or memory key, and release-notes destination in the automation prompt.
- Require the automation to delete, archive, or disable itself after the expiry time, or to stop after a user-specified end condition.
- Preserve a checkpoint after every run so overlapping runs do not duplicate bug intake or repeated release notes.
- If a run is still active when the next cadence fires, the new run must detect the active run and skip or report overlap rather than starting a competing fix loop.

## Source-Message Status Reactions

Use reactions on each actionable source message as the lightweight tester-facing status surface. Preserve the source message ID and current reaction state in the checkpoint so later runs do not duplicate or regress reactions.

- Add 👀 when investigation starts and the report is accepted into the active batch.
- Replace 👀 with 🔵 only after the issue is fixed locally and its focused validation passes.
- Replace 🔵 with ✅ only after the batched deployment is live and the exact issue is verified in the requested hosted environment.
- Do not use ✅ for a local-only fix, an open PR, a deployment still in progress, or an unverified hosted change.
- If the source supports only additive reactions, remove the prior status reaction before adding the next one. Keep exactly one workflow-status reaction per bug report.
- Batch related fixes and perform one deployment per repo when practical. Advance all locally resolved items to 🔵 while the batch waits, then advance each item to ✅ only after hosted verification.
- If reaction writes are unavailable, record that delivery blocker in the checkpoint and continue the engineering work. Do not substitute a reply for the requested reaction unless the user explicitly asks.
- For Messages/iMessage Tapbacks, target the exact incoming report bubble, not a nearby reply, screenshot, summary, or outgoing message. Persist the message GUID before reacting.
- After every reaction write, re-read the source message and verify that exactly one workflow reaction is visible. If verification fails, record the failure and do not advance the checkpoint state.
- Never cycle through 👀, 🔵, and ✅ merely to test reaction controls. A live test on an active report stops at the highest state supported by real evidence; normally that is 👀 when investigation begins.
- Store reaction history as an ordered transition with timestamps, for example `accepted_at`, `resolved_locally_at`, and `deployed_verified_at`, so later monitor runs can audit why a status advanced.

## Orchestrator Mode And Parallel Agents

Use `$orchestrator-mode` as the default execution posture for each monitor run. Keep the current thread as the orchestrator and dispatch multiple bounded agents at the same time when work can proceed independently.

- Start with a compact orchestration plan after intake: bug groups, likely repos, agent assignments, protected files or areas, validation commands, and stop conditions.
- Use parallel agents for independent bug triage, repo/source tracing, screenshot or repro analysis, focused implementation slices, local test runs, browser checks, and log reduction.
- Prefer one agent per independent repo, surface area, or bug group. Do not assign two agents to edit the same files or the same migration/config surface at the same time.
- Give every agent a narrow packet: repo path, exact bug IDs, in-scope files or search targets, out-of-scope areas, expected return format, validation commands, and stop conditions.
- Require compact returns: changed files, commands run, evidence, failures, residual risk, and decisions that need orchestrator judgment.
- Keep product interpretation, architecture, cross-repo contracts, deployment decisions, release notes, checkpoint updates, and final validation synthesis in the orchestrator thread.
- Use agents to reduce token usage, not increase narrative: avoid broad reads, full logs, repeated watchers, and verbose summaries. Put heavy logs in files and ask agents for short failure tails or structured summaries.
- After each agent wave, reopen important changed files and review diffs centrally before accepting or deploying the batch.
- Launch another parallel wave only when the remaining work is still independent and the coordination cost is lower than doing it in the main thread.

## Workflow

1. Establish the monitor checkpoint.
   - Record the source thread, start time, cadence, expiry time, repos, target environment, and last processed message ID or timestamp.
   - If there is prior run memory, load it before checking the thread.
   - Do not reprocess messages already covered by the checkpoint unless the user asks for a re-audit.

2. Check the thread.
   - Fetch only messages newer than the checkpoint.
   - Extract candidate bug reports, regressions, screenshots, repro steps, affected user or org, severity, environment, and reporter.
   - Classify each item as actionable bug, duplicate, needs clarification, already fixed, out of scope, not reproducible yet, or non-bug feedback.
   - Preserve links, message IDs, screenshots, and timestamps for citations and follow-up.
   - Add 👀 to each newly accepted actionable report and persist the reaction state.

3. Build the orchestration and batch plan.
   - Group related bugs by repo, surface area, likely root cause, and validation path.
   - Prefer one fix batch and one PR per repo unless isolation is necessary.
   - For cross-repo bugs, define the repo order and integration boundary before editing.
   - State the concrete hypothesis for each bug before implementation.
   - Assign independent work to parallel agents and keep overlapping files or stateful changes in the orchestrator thread.

4. Fix each actionable bug.
   - For each bug, create or track a concrete goal when goal tracking is available.
   - Use `$autonomous-feature-build` to inspect the relevant repo, implement the fix, and run focused local validation.
   - When there are multiple independent bugs or repos, run multiple autonomous-feature-build-style agent packets in parallel under the orchestrator plan.
   - Keep product interpretation, architecture, safety review, and final integration judgment in the main thread.
   - Avoid overlapping edits to the same files from parallel agents.
   - After the focused local repro passes, replace that report's 👀 with 🔵. Keep it blue while waiting for the shared deployment batch.

5. Validate locally before deployment.
   - After all actionable local fixes in the batch are complete, run `$full-suite-tests` for `local` in every affected repo.
   - Use parallel agents for independent focused retests and log reduction, but run broad/heavy full-suite commands according to `$full-suite-tests` safe-run rules.
   - Include focused repro tests for each bug plus the repo's broader deterministic, build, lint, type, browser, API, and manual coverage where applicable.
   - If the suite fails, repair failures in bounded batches and rerun affected local checks before deployment.

6. Deploy to the requested non-production environment.
   - Use the repo's documented deployment path.
   - Prefer a single PR for the batch per repo unless the project requires otherwise.
   - Do not merge, promote to production, or change protected branches unless the user explicitly requested that in the current conversation.
   - Record PR URL, branch, commit SHA, deployment URL, and deploy identifier.

7. Validate hosted environment.
   - Run `$full-suite-tests` for the target hosted environment, usually `dev`.
   - Confirm the deployed commit or version when possible.
   - Include authenticated app coverage when the app has authenticated surfaces.
   - Rerun exact repro paths from the thread against the hosted environment.
   - After each issue passes its hosted repro, replace its 🔵 with ✅.

8. Post release notes to the relevant text thread.
   - After PRs are pushed or deployed to dev, update the source thread with concise release notes.
   - Include fixed bug summaries, PR links, dev deployment status, validation status, and any items still blocked or needing retest.
   - Keep the post recipient-fit and compact; link to longer QA logs or PRs instead of pasting large artifacts.
   - Do not overstate readiness: separate locally fixed, PR pushed, dev deployed, dev validated, and still blocked.

9. Report and checkpoint.
   - Update the monitor checkpoint to the latest processed message ID or timestamp.
   - Record which release-note message was posted so future runs do not repost the same notes.
   - Report bugs found, bugs fixed, duplicates, blocked items, PRs, deploys, local test results, hosted test results, release notes posted, and remaining risks.
   - Save enough durable notes that the next cadence run can continue without reprocessing the thread.

10. Expire the temporary automation.
   - On or after the configured expiry time, delete, archive, or disable the automation.
   - Before shutting down, run one final checkpoint pass if safe and requested by the automation prompt.
   - Post or report final accounting: total bugs processed, fixed, deployed, validated, deferred, and blocked.

## Bug Intake Ledger

Use this compact ledger shape during each run:

```markdown
## Intake

- New messages checked: <count>
- New actionable bugs: <count>
- Duplicates or already known: <count>
- Needs clarification: <count>
- Last processed checkpoint: <message id or timestamp>
- Automation expires: <timestamp>

## Bugs

| ID | Source | Summary | Repo | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| BUG-001 | <thread link> | <short summary> | <repo> | actionable | <screenshot/repro/link> |
```

Add a `Reaction` column when the source supports reactions, using `👀`, `🔵`, or `✅` as the current state.

## Release Notes Template

Post a compact update to the relevant text thread after PRs are pushed or dev deployments complete:

```markdown
Dev testing update:

Fixed and pushed:
- <bug summary> - <PR or commit link> - <dev validation status>
- <bug summary> - <PR or commit link> - <dev validation status>

Validation:
- Local full suite: <passed/failed/blocked>
- Dev full suite: <passed/failed/blocked>

Still open:
- <blocked item or "none">

Next monitor pass: <time>, unless the temporary monitor expires first.
```

## Fix Loop Rules

- Do not run a separate full-suite cycle for every bug when a batch is safer and cheaper.
- Do run focused validation for each bug before calling it locally fixed.
- Do run the full local suite before deploying the batch.
- Do run the full hosted suite after deployment.
- If multiple repos are affected, run local and hosted validation per affected repo/environment.
- If a bug cannot be reproduced, capture the attempted repro, evidence, and exact clarification needed.
- If a fix requires production access, destructive data changes, permissions, roles, ownership, RLS, billing, or real customer communication, stop and ask for exact approval.

## Cross-Repo Handling

When a bug spans multiple repos:

1. Identify the source of truth for the behavior.
2. Confirm interface contracts between repos before editing.
3. Implement compatible changes in dependency order.
4. Run focused contract tests or integration checks.
5. Run full local validation for every changed repo.
6. Deploy through each repo's documented non-production path.
7. Run hosted validation for every affected deployed surface.
8. Post one thread update that clearly maps each repo PR to the user-visible fix.

## End-Of-Run Report

Include:

- Source thread and checkpoint covered.
- Cadence window checked and automation expiry time.
- Bugs found, fixed, deferred, duplicated, and blocked.
- Files/repos changed.
- Branches, commits, PRs, deploy IDs, and target URLs.
- Release notes posted back to the thread, with link or message ID when available.
- Local `$full-suite-tests` status by repo.
- Hosted `$full-suite-tests` status by repo/environment.
- Authenticated QA coverage status where applicable.
- Remaining uncertainty and next checkpoint time.

## Default Stopping Point

Stop after the requested non-production environment is deployed, validated, and release notes are posted to the thread. A green dev or staging run does not imply approval to merge to main or promote to production.
