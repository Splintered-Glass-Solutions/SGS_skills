# Qa Run Agent Playbook

This is a platform-neutral version of the `qa-run` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Execute a QA/QC pass for any software project and persist a new run with reviewer Codey. Use when the user says QA run, run QA/QC, start a dashboard session, test a feature or full project and record results, retest failures, or save QA evidence/history. Adapt to an existing dashboard API or relational/document database when available, and otherwise create durable local run artifacts. Use the Bonfire-specific adapter for exact Bonfire catalog, API, table, and storage paths.

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

# QA Run

Execute a project’s selected QA/QC scope, preserve one result per check/attempt, attach safe evidence, and persist a new run. Set the reviewer display name to exactly `Codey` in every storage mode.

Read [references/run-storage-adapters.md](references/run-storage-adapters.md) completely before starting. For Bonfire, also read [references/dashboard-run-contract.md](references/dashboard-run-contract.md) completely and use `$bonfire-qaqc` for its canonical test workflow.

## Authority and boundaries

Invoking this skill authorizes creation and update of one bounded QA run and its QA-only result, evidence, defect-link, and audit records in the project’s already-configured run store. It does not authorize:

- schema/table creation or migrations;
- grants, roles, ownership, RLS, policies, staff-access changes, or reviewer identity creation;
- unrelated application/customer-data changes;
- paid, destructive, external-write, provider, or production mutations without separate exact approval;
- deployment, merge, promotion, external messaging, or release sign-off.

If no safe configured database/dashboard writer exists, save locally. Never broaden permissions merely to persist a run.

## Defaults

- Reviewer: `Codey`.
- Environment: use the prompt/current task target; otherwise use the project adapter’s default, or `local` when no adapter exists.
- Scope: use named features/interfaces/checks; when no narrower scope exists, use the project’s full active QA catalog/checklist.
- Safety: run read-only checks by default. Include contained writes only with approved disposable fixtures. Exclude higher-risk checks until authorized.
- Outcomes: use the project’s vocabulary when defined; otherwise use `passed`, `failed`, `blocked`, `not_applicable`, and `skipped`.

Reviewer, tester/executor, and sign-off identity are distinct. Never assign a human substitute, invent Codey’s database UUID, or mark Codey as having signed off.

## Workflow

### 1. Discover the project QA contract

Inspect the active repository, branch, dirty state, project docs, test commands, QA catalogs/checklists, prior run artifacts, deployed target, and configured QA storage.

Prefer project-owned runbooks and skills. Do not impose Bonfire’s routes, schema, fixtures, or environment defaults on another project.

Choose one storage mode:

1. dashboard API or normalized QA database;
2. project-specific single table/document store;
3. local-only run artifacts.

Record the selected mode and evidence that it exists. A design document or migration file is not proof that a database schema is deployed.

### 2. Resolve reviewer Codey

- Text-capable stores: write `reviewer: "Codey"` exactly.
- Identity/FK stores: resolve Codey through the project’s existing reviewer/staff mapping and verify the rendered display name.
- Local-only mode: write `reviewer: "Codey"` in both `run.json` and `manual-run.md`.
- Never create a reviewer account/mapping or reuse the tester’s identity without explicit authorization.

If a database requires a reviewer FK and Codey is unresolved, use local-only persistence and report the database run as blocked. Do not discard completed QA work.

### 3. Create durable run state before testing

Create a dated run directory using project conventions. When none exist, use:

`output/qa/<environment>-<scope>-YYYY-MM-DD-HHMM/`

Create:

- `manual-run.md` for human-readable progress/resume state;
- `run.json` for structured run metadata and results;
- `screenshots/` and `artifacts/` as needed.

Record project, environment, target, scope, catalog/checklist revision, code/build revisions, tester/executor, reviewer `Codey`, storage mode, fixtures, safety exclusions, and cleanup plan.

For database/dashboard modes, create and read back the parent run before testing. Verify reviewer, target, scope, revision, and selected count. For local-only mode, write and re-read valid `run.json` before testing.

### 4. Materialize scope and resolve fixtures

Snapshot the selected checks so later catalog edits cannot rewrite history. Resolve only non-secret fixture aliases or safe metadata. Never store passwords, tokens, raw API keys, or provider secrets.

Retain unresolved applicable checks and record them as blocked when execution reaches them. Do not silently remove difficult checks from the denominator.

### 5. Execute the QA pass

Follow the project’s canonical QA workflow and check specifications. Run focused deterministic checks first when appropriate, then service/route/job checks, then authenticated browser/manual flows.

For every selected check:

1. start a new attempt;
2. execute prerequisites, happy path, meaningful negative case, and success criteria;
3. capture actual result, runtime context, cleanup state, and evidence;
4. save the terminal outcome once;
5. update the local run artifacts immediately;
6. when using a database/dashboard, read the saved result back before continuing.

Retests create a new attempt. Never overwrite failed history with a later pass.

For automated browser checks, preserve reporter output as structured per-test
results. Each mapped test needs an exact identity and independent outcome. Each
failed test also needs a failure class, the first actionable error/assertion,
a bounded stack excerpt (or explicit unavailable reason), and artifact paths.
Never persist `Playwright failed`, a bare process exit code, or mixed text such
as `passed | failed` as the actual result. If the runner, auth, fixture, or
reporter fails before an attributable product assertion, store `blocked` with
the precise infrastructure reason and rerun action.

### 6. Save results and evidence

Require actual observations for every terminal result. Require evidence for failures and reasons for blocked, N/A, and skipped outcomes.

Run any project-owned failure-evidence validator before persistence. For
Bonfire, the canonical contract and command are in
`<workspace>/bonfire_shared_docs/shared/quality/qa_browser_failure_evidence.md`.
Treat validator failure as a QA infrastructure blocker and do not synchronize
the incomplete attempt as a product failure.

Use private project evidence storage when configured; otherwise save locally in the run directory. Redact secrets, unrelated customer data, email addresses, and personal information. Store file paths/metadata in structured results rather than embedding binary/base64 data.

Create or link defects only in the project’s configured QA/defect system. Do not create external tickets or send messages unless separately requested.

### 7. Close, pause, or leave incomplete truthfully

Verify outcomes, evidence, defect/waiver requirements, blocker/N/A/skip reasons, cleanup, safety exceptions, and metric denominators.

- Complete only when the selected scope’s closeout rules are satisfied.
- Pause when work will resume.
- Leave incomplete when applicable checks remain skipped/not run or persistence is inconsistent.
- Do not sign off as Codey; reviewer assignment is not reviewer approval.

### 8. Verify persistence

Reconcile the stored run against `manual-run.md` and `run.json`:

- project, environment, scope/revision, reviewer `Codey`, status, and selected count;
- outcome counts, attempts, evidence, defects, and cleanup;
- quality/completion calculations and environment/build attribution.

For database/dashboard modes, require mutation evidence, read-back, and matching rollups. For local-only mode, require valid structured JSON, matching Markdown, existing evidence paths, and a stable re-read. State the proof tier explicitly.

## Required handoff

Report:

- project, environment/build, overall result, and scope;
- storage mode and exact run ID/path/dashboard URL;
- reviewer `Codey` and identity-resolution status;
- selected/executed/outcome counts and metric denominators;
- defects, regressions, recoveries, evidence, cleanup, and blockers;
- persistence/read-back proof;
- local versus database/dashboard truth;
- actions not authorized or not performed.
