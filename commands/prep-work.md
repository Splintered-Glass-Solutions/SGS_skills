---
description: Audit whether a large autonomous job has the credentials, access, approvals, environment, and validation path needed before starting.
argument-hint: [job-description]
---

# Prep Work

Run a read-only readiness audit before starting a large autonomous job.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `$CODEX_HOME/skills/prep-work/SKILL.md`.
2. Treat `$ARGUMENTS` as the proposed job description.
3. If `$ARGUMENTS` is empty, ask the user for the job scope before checking anything.
4. Stay read-only unless the user explicitly asks for setup or mutation.
5. Never print secret values. Report only secret names and present/missing status.

## Plan

Produce a readiness report that answers:

- What job is being prepared for?
- Which repos, services, databases, APIs, env vars, accounts, and approvals are required?
- Which prerequisites are confirmed?
- Which items are missing or ambiguous?
- What can be done autonomously now?
- What remains blocked or gated?

## Commands

Use compact, read-only checks as relevant to the job:

- Repo: `pwd`, `git status --short`, `git branch --show-current`, `rg --files`
- Runtime: inspect package scripts, Python/Node/tool versions, test commands
- Env: check key names/presence only, never values
- DB: confirm target host/environment before any schema or migration work
- External APIs: verify docs, client wrappers, auth scope requirements, and safe validation options
- Deploy: inspect config and linkage without deploying

Do not run migrations, deploys, syncs, backfills, paid jobs, production mutations, broad external API jobs, or git publish actions unless the user explicitly approves that exact action.

## Verification

Before giving a verdict, verify:

- Required access is either confirmed, missing, or explicitly not needed.
- Secret handling did not expose values.
- Any DB target is classified as local/dev/prod/cloud before recommending DB actions.
- Any destructive or production-impacting step is listed as gated.
- Validation commands are identified or the lack of them is called out.

## Summary

Return the skill's output template:

- Job
- Required Access
- Confirmed
- Missing Or Unconfirmed
- Risks
- Needed From You
- Autonomous Run Contract
- Verdict

## Next Steps

If ready, state the exact autonomous run scope. If not ready, ask only for the minimum missing inputs needed to proceed.
