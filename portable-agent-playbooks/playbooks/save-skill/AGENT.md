# Save Skill Agent Playbook

This is a platform-neutral version of the `save-skill` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Save one or more local agent skills into the private SGS_skills GitHub repo, including skill files, agents metadata, slash-command wrappers, portable playbooks, docs/index updates, validation, commit, and push. Use when the user asks to save, archive, publish, commit, or push a custom skill to SGS_skills, or invokes the save-skill slash command for selected skill content.

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

# Save Skill

## Overview

Use this skill to persist the user's custom agent skills into
`<workspace>/SGS_skills` and push the result to GitHub. The output is a
repo commit containing the requested skill archive, command wrapper when
available, index/docs updates, and regenerated portable playbooks.

This is a repo-push workflow. It may mutate only local skill files when the user
provides new skill content, and the `SGS_skills` repo. It must not deploy,
message people, mutate production systems, change databases, alter protected
branches, or touch unrelated work.

## Inputs

Accept any of these forms:

- `$save-skill recap`
- `$save-skill <agent-config>/skills/recap/SKILL.md`
- `$save-skill <agent-config>/skills/recap`
- selected/pasted `<skill>...</skill>` content with a `name` and `path`
- "save this skill to SGS git"

If the user says `/save skill`, normalize that to the `save-skill` skill and
slash command. If multiple skills are named, process them in one commit.

## Required Paths

- Local skills root: `<agent-config>/skills`
- Local commands root: `<agent-config>/commands`
- Archive repo: `<workspace>/SGS_skills`
- Repo skills archive: `<workspace>/SGS_skills/skills`
- Repo command archive: `<workspace>/SGS_skills/commands`
- Repo skill index: `<workspace>/SGS_skills/docs/custom-skill-index.md`
- Portable generator:
  `<workspace>/SGS_skills/scripts/generate-portable-playbooks.rb`

## Workflow

1. Resolve the requested skill.
   - Prefer an explicit path or skill name from `$ARGUMENTS` or selected text.
   - For `<skill>...</skill>` blocks, read the `name` and `path`.
   - If content is provided and differs from disk, update the local skill first.
   - Do not guess among multiple plausible skills. Ask only when the target is
     ambiguous.
2. Inspect repo state.
   - Run `git status --short --branch` in `<workspace>/SGS_skills`.
   - If unrelated dirty work exists, do not stage it. If it overlaps the skill
     being saved, read it and work with it rather than reverting.
3. Validate local skill structure.
   - Confirm `SKILL.md` exists and has YAML frontmatter with matching `name`.
   - Confirm `agents/openai.yaml` exists. If missing, create it before archiving.
   - If a command wrapper exists at
     `<agent-config>/commands/<skill-name>.md`, include it.
4. Archive the skill into the repo.
   - Copy the full local skill folder to `skills/<skill-name>/`.
   - Copy the local command wrapper to `commands/<skill-name>.md` when present.
   - Do not copy system, plugin-cache, memory, portfolio state, secrets, env
     files, node_modules, build artifacts, or unrelated local files.
5. Update docs and portable playbooks.
   - Add the skill name to `docs/custom-skill-index.md` if absent.
   - Add or update a short usage section when the request asks for docs or when
     the skill is operationally important.
   - Run the portable generator so generalized playbooks stay in sync:

```bash
ruby <workspace>/SGS_skills/scripts/generate-portable-playbooks.rb
```

6. Validate changed files.
   - Run the skill validator when available:

```bash
python3 <agent-config>/skills/.system/skill-creator/scripts/quick_validate.py <agent-config>/skills/<skill-name>
```

   - If Python YAML dependencies are unavailable, use Ruby YAML parsing for
     `SKILL.md`, `agents/openai.yaml`, and the command wrapper frontmatter.
   - Run a targeted markdown sanity check over the changed docs/playbooks:
     unmatched fenced code blocks, missing files, and trailing whitespace.
7. Commit and push.
   - Stage only files related to the saved skill(s), docs/index updates, and
     generated portable playbooks.
   - Use a clear commit message such as:
     `chore: archive <skill-name> skill`
   - Push to `origin/main`.
   - Verify `git status --short --branch` is clean against `origin/main`.

## Documentation Expectations

When adding documentation, keep it short and practical. Include:

- what the skill saves;
- how to invoke it;
- what files it updates;
- validation performed;
- safety boundaries;
- what happens when a command wrapper or agents metadata is missing.

Prefer updating an existing repo doc over creating scattered new docs. For this
skill, the canonical repo doc is `docs/save-skill.md`.

## Safety Rules

- Never include secrets, `.env` files, token-bearing logs, private portfolio
  ledgers, or production data in `SGS_skills`.
- Never stage unrelated dirty work.
- Never run deploys, external messages, production mutations, DB permission
  changes, or protected-branch operations as part of this skill.
- If push fails, leave the local commit intact and report the exact failure.
- If validation fails, do not push unless the user explicitly approves pushing a
  known-bad archive.

## Final Response

Return a compact closeout:

- saved skill name(s);
- local and repo paths touched;
- commit hash and push result;
- validation summary;
- any skipped pieces, such as missing command wrappers.

