# Agent Usage Steward Agent Playbook

This is a platform-neutral version of the `codex-usage-steward` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Review an agent workflow's usage allowance and context/coordination overhead using authorized metrics, retain honest coverage accounting and recommend bounded efficiency improvements.

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

# Codex Usage Steward

Optimize verified accepted work per unit of usage without weakening correctness,
review or delivery. This workflow grants no account access, monitoring schedule,
spending authority, permission to contact other chats or authority to stop work.

## Configure and invoke

Supply the runtime/account usage source, permitted task metrics, observation
window, private checkpoint location, warning thresholds and reset/timezone policy.
Use available authorized account tooling or a signed-in usage view; do not assume
an API, particular staff identity, personal account or local transcript/database.

Example: `Use $codex-usage-steward for one read-only efficiency check of this
project. Use the supplied usage export and recent task summary, distinguish
unknown metrics, and recommend changes without sending messages or changing jobs.`

For recurring monitoring, require an explicit user request, resolve their cadence
and timezone, verify one canonical schedule and retain checkpoints in its existing
chat. Check for duplicates. A configured schedule is not proof that it has run.
Do not create competing monitors or launch monitoring subagents by default.

## One bounded pass

1. Read the latest checkpoint and cheaply verify source freshness and scope.
2. Record allowance, reset time and credits separately when available. Missing
   values remain unavailable rather than zero. Do not read credentials/auth files.
3. Sample permitted current-task metrics: latest per-response fresh/cached input,
   output, calls, worker/startup/handoff costs, repeated reads or coordination,
   retries, repeated verification and accepted outcomes when actually measured.
4. Inspect only the bounded task evidence needed for actionable hypotheses.
   Do not ingest whole transcripts, unrelated projects or historical archives.
5. Compare observations to the user's configured thresholds and prior epoch.
   Treat resets/tier changes as separate accounting epochs. Do not invent caps.
6. Distinguish observed overhead from inference. A short wait count does not
   prove waste, a large context does not prove unnecessary work, and a reused
   test is valid only if candidate, fixtures and affected dependencies still match.
7. Recommend at most a few concrete changes: narrow reads, batch independent
   queries, retain a checkpoint, wait longer on unchanged status, or reuse exact
   still-valid evidence. Preserve explicit model choices and review gates.

## Coverage, actions and proof

For each category record direct, sampled, unavailable or not applicable, with
observation time and a concise evidence pointer. Cover allowance/reset/credits,
context, coordination, repeated reads/retries, evidence validity, model/effort fit
and whole-job accepted-outcome efficiency only to the extent the source supports.
No local source proves exhaustive cross-host or cloud-only activity.

Apply low-risk improvements to this check's own reads/output. Changes to another
workflow, cross-chat advisories, notifications, scheduling, spending, subscriptions,
security, product code or running jobs require current task authority. Do not
silently change global defaults, weaken tests or interrupt another writer.

Keep deduplication state and delivery receipts private. Record an alert delivered
only after a real authorized delivery is verified; an advisory is not a completed
optimization without outcome evidence. For a requested monitor, stay quiet on
unchanged/non-actionable checks and notify only according to its explicit policy.

Return a compact source/coverage summary, observed changes, suggested or completed
actions, evidence, limits and next checkpoint. Price equivalents, if requested,
are estimates distinct from actual billed charges or guaranteed savings.

This public edition intentionally omits a private transcript/database snapshot
helper and account mappings. Supply an authorized metrics adapter or export; if
none exists, report the missing coverage rather than creating a database or
claiming that usage monitoring is operational.
