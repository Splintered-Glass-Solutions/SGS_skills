---
name: prep-work
description: Run before large, long-running, autonomous jobs to audit whether Codex has the repo context, target environments and accounts, credentials, database/API access, environment variables, approval classes, existing sessions, and validation path needed to finish without avoidable user interruption, then produce a reusable run contract for the executing skill.
---

# Prep Work

Use this skill before starting a substantial implementation, migration, deploy, integration, automation, data job, or full validation run where autonomy depends on prerequisites being present.

The purpose is readiness, not execution. Produce a clear go/no-go assessment and
a handoff contract the executing skill can consume without repeating discovery.

## Rules

- Stay read-only unless the user explicitly asks for setup or mutation.
- Do not print, persist, or echo secrets. Report only secret names and present/missing status.
- Prefer safe checks that prove access without changing state.
- If a check might mutate data, spend money, affect production, or trigger external workflows, stop and ask first.
- Separate confirmed facts from assumptions.
- Ask only for the smallest missing credential, permission, URL, account, approval, or decision needed to continue.
- Respect repo-specific safety rules such as cloud-only DB targets, no local Supabase/Postgres, production approval gates, and git hygiene.
- Treat a shared database used by production as a production-connected surface
  even when the application target is development.
- Distinguish three approval classes: standing workflow authority, exact
  resource/action approval, and action-time confirmation required by a tool or
  UI policy. Never imply that one class satisfies another.
- A caveat is not a stop signal. Identify the safe lane that can proceed while
  a credential, provider login, or action-time gate remains pending.

## Workflow

### 1. Define The Job

Restate the work in concrete terms:

- Objective
- Repo(s) and service(s) involved
- Expected deliverable
- Target environment, if any
- Truth surfaces that must be proven separately: local, merged branch, hosted
  environment, shared data/provider state, and production/customer-visible
- Whether deployment, migration, live API calls, or external side effects are in scope
- Validation needed to consider the job complete

### 2. Inventory Required Access

List every dependency the job may need:

- Repo paths and branches
- Runtime tools and package managers
- Database targets and migration permissions
- Env vars and secret names
- External APIs and account scopes
- Required provider identity and account, not only the provider project
- Browser/auth sessions and any already-running PTY, OAuth, or dev-server session
- Persistent access creation such as OAuth clients, API keys, or service
  accounts, including whether the final action needs action-time confirmation
- Deployment platforms
- Monitoring/logging/analytics access
- Test data, fixtures, or approved QA accounts
- User approvals for destructive, paid, production, or shared-resource operations
- Whether env changes auto-deploy or can be applied without triggering a deploy

### 3. Run Safe Readiness Checks

Use compact, read-only checks where possible:

- `pwd`, `git status --short`, `git branch --show-current`
- `rg --files`, `find`, or package/script inspection
- package/runtime versions
- presence of env var names without values
- schema/migration folders
- docs/runbooks/AGENTS instructions
- cloud DB host confirmation before any DB-related work
- whether a shared DB is production-connected, regardless of the app environment
- API docs or existing client wrappers
- test commands and local server commands
- reusable active sessions before starting duplicate login, browser, server, or
  terminal work

Never dump full env files, command histories, tokens, or large logs.

### 4. Classify Gaps

Use these groups:

- **Blockers**: missing items that prevent safe autonomous completion.
- **Caveats**: work can proceed, but some validation/deploy/live check will remain incomplete.
- **Risks**: likely failure modes and how to reduce them.
- **Action-time gates**: steps that can be prepared now but need confirmation at
  the final UI/tool action.
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

Record approvals precisely instead of writing “approved” without scope:

| Surface | Target | Allowed now | Action-time confirmation | Evidence |
| --- | --- | --- | --- | --- |
| Example | development OAuth client | prepare only | create client/key | user instruction |

For exact approvals, record the reusable non-secret tuple:
`action + repo + branch/SHA when relevant + environment + provider/account +
exact operation or payload + approval evidence + status`. Preserve it until it
is revoked or invalidated by a changed target, materially changed payload/diff,
new permission or destructive impact, or expired external state.

For provider credentials, record only non-secret provenance: environment,
provider, masked app/account identifier, required secret names and
present/missing status, scopes, redirect URIs, owner/source, and last safely
verified time. Never record secret values.

The executing skill should inherit this table, reverify only cheap drift-prone
facts, and preserve the same targets and limits.

Produce the run contract as one canonical block. If the task already has a
plan, QA packet, or run-state artifact, update that durable surface. Otherwise
return the block in the final response so the executing skill can save it in
its ledger before the first edit or external operation.

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

## Existing Sessions And Checkpoints

- <session/tool/id>: <running, reusable, stale, or absent>

## Proof Matrix

- Local:
- Merged branch:
- Hosted environment:
- Shared data/provider state:
- Production/customer-visible:

## Verdict

<Ready to run autonomously | Ready with caveats | Blocked until user provides X>
```

## Verdicts

- **Ready to run autonomously**: all required access and approvals are present for the requested scope.
- **Ready with caveats**: implementation can proceed in named safe lanes, but
  live validation, migration, deploy, or another step remains gated.
- **Blocked**: no useful safe lane can proceed without an essential prerequisite.
  Do not use this verdict merely because one later provider or credential step
  is unavailable.

Keep the final assessment concise and actionable.
