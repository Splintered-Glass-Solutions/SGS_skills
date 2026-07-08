# Bonfire Qaqc Agent Playbook

This is a platform-neutral version of the `bonfire-qaqc` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Run Bonfire QA/QC and release validation using the repo's canonical QA docs. Use when the user asks to run or prepare QA, QC, "full suite", "full QAQC", "test every page", "manual QA walkthrough", "production readiness", environment validation, app.heybonfire.com checks, dev/local/prod smoke tests, release sync validation, or weekly QA reporting for Bonfire.

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

# Bonfire QA/QC

## Overview

Use this skill to execute or prepare Bonfire QA in a standardized way. The source of truth is the repo documentation, not this skill:

- `docs/qa/full-suite-runbook.md`
- `docs/qa/environment-matrix.md`
- `docs/qa/manual-run-template.md`
- `docs/release-sync.md`
- `docs/qa/README.md`

If these docs are missing, report that as a blocker and offer to recreate them.

## Workflow

1. Infer the environment from the prompt: `local`, `dev`, or `prod`. If missing, ask before executing.
2. Read `docs/qa/environment-matrix.md` and the relevant sections of `docs/qa/full-suite-runbook.md`.
3. If executing a run, create a dated run folder before browser work:
   `output/qa/{environment}-full-YYYY-MM-DD/`
4. Create or update `manual-run.md` in that folder from `docs/qa/manual-run-template.md`.
5. Run automated checks that match the requested scope.
6. Run route/health/deploy checks for the target environment.
7. Use Browser Use/Computer Use for page-by-page walkthroughs when requested or when the request is a full suite/full QAQC.
8. Record pass/fail notes, URLs, account/org used, screenshots, console/network errors, defects, fixes, retests, and follow-ups in `manual-run.md`.
9. Summarize results clearly with pass/fail status and blockers.

## Full Suite Contract

When the user says “full suite”, “full QAQC”, “test every page”, or equivalent, treat it as one long-running end-to-end QA job by default. Do not ask the user to queue each page separately. Own the full queue until completion unless blocked.

For full-suite runs:

- Start with preflight: git state, target URL, deploy/CI status, auth/session readiness, runbook availability.
- Create `output/qa/{environment}-full-YYYY-MM-DD/manual-run.md` before browser work and keep the next queue item visible in the log.
- Run deterministic tests first when feasible, then route/health checks, then Computer Use/manual coverage.
- Cover every default page group below unless the user narrows scope.
- Mark each area `Pass`, `Partial`, `Fail`, or `Blocked`.
- Post short progress updates after each major area.
- If context compacts or the run resumes, continue from `manual-run.md` rather than restarting.
- Fix defects discovered during QA when the user asked for resolution, when prior context grants that expectation, or when the defect is in the QA harness and blocks the run.
- Retest the affected area after every fix.
- For `dev`, do not declare clean until fixes are merged/deployed and the final suite passes on `https://dev.heybonfire.com`.

Default full-suite queue:

1. Preflight: git state, target URL, deploy/CI status, auth/session readiness.
2. Auth/onboarding: login, signup, redirects, onboarding resume.
3. Home/dashboard: cards, usage, navigation, empty/error states, mobile.
4. Inbox: all sessions, session detail, notes/flags, sources/chunks, live chat, forms, mobile.
5. AI Agents: overview, create/edit, identity, style, knowledge, actions, behavior, advanced, installation, preview, error states, mobile editor.
6. Knowledge Base: create/settings, content library, source add/sync, Drive/YouTube/web/file flows, tags/authors, third-party catalog, mobile, errors.
7. Studio: resources, creation wizard, editor, revision chat, attachments, generated output, actions/templates, publish/download/delete.
8. Widget/embedded: floating, inline, hosted page, source selector, chat modes, history/resources drawers, support ticket, generated resources, mobile.
9. Campfire: trusted source selection, chat, source chips, history/resources/automation panels, mobile drawer behavior.
10. Settings/developers: organization, branding, team, billing/usage, API keys, playground.

Hosted dev auth rule: deterministic local auth fixtures may not work against hosted `dev`. Prefer a real contained dev QA Supabase session for authenticated hosted Computer Use. If fake auth redirects to login, record it as an auth-readiness issue, create/reuse a contained QA account if credentials/admin access are available, and rerun.

Cost/destructive guardrails:

- `local` and `dev` may use small real API calls, short videos, small uploads, one or two chat messages, and bounded generated-resource tests.
- `prod` must be non-destructive unless the user explicitly approves a specific action.
- Never create or modify real paid production subscriptions without explicit approval.
- Never delete production data.
- Never invite real production users unless the recipient is approved.
- Do not run YouTube playlist ingestion as routine QA. Use single videos only unless a playlist bug is explicitly under test.

## Run Log Requirements

The full-suite run folder must include:

- `manual-run.md`
- `screenshots/`
- `artifacts/`
- references to `test-results/` when failures occur

`manual-run.md` must include:

- environment, URL, branch/commit/deploy
- QA account and org used
- automated checks and results
- page-by-page results
- defects found, fixes made, and retests
- console/network errors
- final release assessment

## Release Sync

Use `docs/release-sync.md` when the user asks about release notes, public release history, release sync dry runs, or validating `/api/internal/releases/sync`.

- Authoring source: `releases/current.md`.
- Public storage target: `app_releases`.
- Required token must match in GitHub Actions and hosted runtime as `RELEASE_SYNC_TOKEN`.
- Prefer the dry run command from `docs/release-sync.md` before posting to a running app.
- Never post production release notes or alter production release history without a clear user request.

## Environment Rules

- Local URL: `http://localhost:5001`.
- Dev URL: `https://dev.heybonfire.com`.
- Production URL: `https://app.heybonfire.com` or the production URL specified by the user.
- Apply the cost/destructive guardrails above for all environments.
- Do not merge, push, or promote anything into `main` unless the user explicitly asks for that specific `main`/production promotion in the current conversation. A hotfix, green dev PR, successful QA run, or "finish the fix" request is not enough by itself. When in doubt, stop after merging to `dev`, report the validation status, and ask before opening or merging a `dev` to `main` PR.

## Local App Setup

For local QA, run from the Bonfire repo root:

```bash
PATH=/Users/the user/.cache/agent-runtimes/agent-primary-runtime/dependencies/node/bin:$PATH corepack pnpm dev
```

The app should run on `http://localhost:5001`. If port `5001` is already in use, inspect the process first. Restart an existing Bonfire dev server when needed so it serves the current branch.

## Automated Checks

For focused auth/signup regression:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run src/app/auth/actions.test.ts src/app/@modal/'(.)signup'/page.test.tsx src/lib/auth/request-origin.test.ts src/lib/auth/login-redirect.test.ts
```

For a full local suite:

```bash
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= corepack pnpm exec vitest run
corepack pnpm type-check
corepack pnpm lint:check
```

For release confidence:

```bash
corepack pnpm build
```

Record command summaries, not full noisy logs, unless failures need details.

## Manual QA

Use `docs/qa/full-suite-runbook.md` as the checklist. Do not improvise a new checklist unless the runbook is missing or the user asks for a special-purpose test.

For each tested area, capture:

- Steps performed.
- Expected behavior.
- Actual behavior.
- Result: Pass, Partial, Fail, or Not Run.
- Evidence: screenshot, URL, console/network error, or request id when useful.
- Follow-up owner or recommended fix when known.

## ClickUp Reporting

When the user asks to report QA results to ClickUp:

1. Resolve the target ClickUp chat channel with ClickUp channel tools.
2. Prefer an exact channel name match.
3. If no exact target exists, do not post to an unrelated channel silently. Report the delivery blocker and closest channels found.
4. Post a concise markdown summary: environment, overall status, checks run, failures, production risks, and follow-ups.

## Output Style

End with:

- Overall status.
- Environment, URL, and branch/commit or deployed build tested.
- Automated check pass/fail counts.
- Manual/page coverage summary and result counts.
- Release sync dry-run/post result if applicable.
- Defects fixed and remaining blockers.
- Location of the dated QA log if one was created.

