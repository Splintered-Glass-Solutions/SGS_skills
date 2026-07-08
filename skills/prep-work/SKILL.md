---
name: prep-work
description: Run before large, long-running, autonomous jobs to audit whether Codex has the repo context, credentials, database/API access, environment variables, approvals, and validation path needed to finish without avoidable user interruption.
---

# Prep Work

Use this skill before starting a substantial implementation, migration, deploy, integration, automation, data job, or full validation run where autonomy depends on prerequisites being present.

The purpose is readiness, not execution. Produce a clear go/no-go assessment before the main work begins.

## Rules

- Stay read-only unless the user explicitly asks for setup or mutation.
- Do not print, persist, or echo secrets. Report only secret names and present/missing status.
- Prefer safe checks that prove access without changing state.
- If a check might mutate data, spend money, affect production, or trigger external workflows, stop and ask first.
- Separate confirmed facts from assumptions.
- Ask only for the smallest missing credential, permission, URL, account, approval, or decision needed to continue.
- Respect repo-specific safety rules such as cloud-only DB targets, no local Supabase/Postgres, production approval gates, and git hygiene.

## Workflow

### 1. Define The Job

Restate the work in concrete terms:

- Objective
- Repo(s) and service(s) involved
- Expected deliverable
- Target environment, if any
- Whether deployment, migration, live API calls, or external side effects are in scope
- Validation needed to consider the job complete

### 2. Inventory Required Access

List every dependency the job may need:

- Repo paths and branches
- Runtime tools and package managers
- Database targets and migration permissions
- Env vars and secret names
- External APIs and account scopes
- Browser/auth sessions
- Deployment platforms
- Monitoring/logging/analytics access
- Test data, fixtures, or approved QA accounts
- User approvals for destructive, paid, production, or shared-resource operations

### 3. Run Safe Readiness Checks

Use compact, read-only checks where possible:

- `pwd`, `git status --short`, `git branch --show-current`
- `rg --files`, `find`, or package/script inspection
- package/runtime versions
- presence of env var names without values
- schema/migration folders
- docs/runbooks/AGENTS instructions
- cloud DB host confirmation before any DB-related work
- API docs or existing client wrappers
- test commands and local server commands

Never dump full env files, command histories, tokens, or large logs.

### 4. Classify Gaps

Use these groups:

- **Blockers**: missing items that prevent safe autonomous completion.
- **Caveats**: work can proceed, but some validation/deploy/live check will remain incomplete.
- **Risks**: likely failure modes and how to reduce them.
- **Not Needed**: access or actions that may sound relevant but should not be used.

### 5. Ask For Minimal Inputs

Ask for only the precise missing items. Prefer this style:

> I need the dev cloud DB target confirmation and a GoHighLevel PIT with read-only contacts/businesses scopes. I do not need production deploy access.

### 6. State The Autonomous Run Contract

Explicitly define what Codex may do and what remains gated.

Common allowed actions:

- Local source edits
- Read-only repo and docs inspection
- Local tests, type-checks, lint, builds
- Mocked or fixture-backed validation
- Migration file creation
- Local dev server/browser verification when safe

Common gated actions:

- Applying DB migrations
- Mutating production/dev shared data
- Running paid or broad external jobs
- Deploying
- Pushing/merging/creating PRs
- Sending messages
- Rotating, exposing, or writing secrets

## Output Template

Use this structure:

```md
## Job

<one paragraph summary>

## Required Access

- <surface>: <why needed>

## Confirmed

- <thing>: <status/evidence>

## Missing Or Unconfirmed

- <thing>: <impact>

## Risks

- <risk>: <mitigation>

## Needed From You

- <specific input, credential name, permission, URL, account, or decision>

## Autonomous Run Contract

I will:
- <allowed action>

I will not:
- <gated action without approval>

## Verdict

<Ready to run autonomously | Ready with caveats | Blocked until user provides X>
```

## Verdicts

- **Ready to run autonomously**: all required access and approvals are present for the requested scope.
- **Ready with caveats**: implementation can proceed, but live validation, migration, deploy, or another step is blocked.
- **Blocked**: starting now is likely to stall, fail, or require rework because an essential prerequisite is missing.

Keep the final assessment concise and actionable.
