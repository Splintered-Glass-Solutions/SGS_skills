# Use the library in your own environment

These workflows contain no publisher accounts or inherited permission. Choose a
skill for your task, read its instructions and supply your own project bindings.
You do not need the publisher’s private workspace, automation or portfolio records.

## Choose your runtime

- Codex: install or copy the selected `skills/<name>/` folder into your skills
  directory. Optional wrappers live in `commands/`. For the full library use
  `bash scripts/install-local.sh`; inspect existing local files first because
  matching archived files are updated. You can install individual skills instead.
- Other runtimes: use `portable-agent-playbooks/playbooks/<name>/AGENT.md` and its
  supporting files. Read the adapter for your runtime. Tool/API names specific to
  Codex require a real equivalent; the playbooks do not create those capabilities.

`<workspace>`, `<project-root>`, `<agent-config>`, `<skills-repo>` and similar
markers are placeholders, not runnable shell paths. Replace them before use.
Use supported runtime tools and current installed CLI help to resolve commands.

## Configure only what the selected workflow needs

| Workflow | Supply | If it is missing |
| --- | --- | --- |
| Planning or local code work | Repository, accepted scope, checks, limits | Inspect local docs; ask only for unresolved scope |
| Authenticated UI or QA | Target URL/environment, approved identity, secure login path, fixtures, permitted writes | Keep authenticated checks blocked; never substitute a maintainer account |
| QA storage | Existing catalog/writer and reviewer policy | Use local run artifacts; leave review unassigned when allowed |
| PM and communication | Your source/thread/project registry, local ledger/checkpoint paths, approved accounts | Start from the bundled portfolio templates and select sources; do not discover unrelated accounts |
| Build orchestration | Available worker models/tools, repository lifecycle and authorized release route | Resolve an equivalent documented configuration or report the missing capability |
| Demo production | Audience, source material, brand assets, authorized capture surface, selected voice and budget | Rehearse locally; do not assume paid access or an approved voice |
| Time tracking | Client ledger root, actual duration/start evidence and timezone | Ask for missing time; do not manufacture hours from chat length |
| Skill publication | Your archive checkout, verified remote/branch and publishing authority | Prepare reviewable local changes only |

Keep these bindings and all account state in private project configuration.
When a skill refers to a portfolio/registry path, use your configured equivalent;
it does not imply that the publisher’s file exists. The bundled templates describe
record shapes, not live data. Do not invent prior approvals, thread IDs or staff.

## Establish authority for each run

A skill describes a procedure; downloading it grants no access or permission.
The current user request and project policies determine allowed writes, release
targets, sending, spending and account changes. Preserve unrelated work, use
approved test fixtures, record exact blockers and distinguish local, hosted,
authenticated, persisted, deployed and externally delivered evidence.

## Before redistributing a skill

Apply the [publication boundary](publication-boundary.md). Generalize the workflow
by role and behavior, remove private account/project assumptions, validate links
and scripts, regenerate portable playbooks, and run the public-library validator.
A text replacement or passing scanner is not a semantic/privacy review. Licensing
and redistribution remain governed by the repository’s existing license terms.
