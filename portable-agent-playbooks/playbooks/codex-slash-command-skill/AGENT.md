# Agent Slash Command Skill Agent Playbook

This is a platform-neutral version of the `codex-slash-command-skill` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Create or repair user-level agent skills that should appear in the slash picker or behave like slash commands. Use when the user asks to make a workflow into a slash command, create a slash-command skill, expose a skill in the picker, fix a skill that is not showing up, or mirror an existing user-level agent command/skill pattern under ~/.agent.

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

# the agent Slash Command Skill

## Overview

Use this skill to create a agent workflow that appears correctly in the slash picker the first time.

On this machine, a picker-visible user-level skill requires the real skill folder under `<agent-config>/skills/<skill-name>/` with both `SKILL.md` and `agents/openai.yaml`. A Markdown wrapper under `<agent-config>/commands/<skill-name>.md` is useful when the user asks for a classic command wrapper, but it is not a substitute for skill UI metadata.

## Default Contract

When the user asks for a `/command`, a slash command, or a skill that should show in the slash picker:

1. Create or update the real user-level skill at `<agent-config>/skills/<skill-name>/`.
2. Always include:
   - `SKILL.md`
   - `agents/openai.yaml`
3. Also create `<agent-config>/commands/<skill-name>.md` when the user says "slash command", "make it a / command", "command wrapper", or wants `$ARGUMENTS` behavior.
4. Do not stop after creating only `SKILL.md`.
5. Do not stop after creating only `~/.agent/commands/<skill-name>.md`.
6. Validate all YAML/frontmatter before reporting success.

## Naming

- Use lowercase letters, digits, and hyphens only.
- Keep the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` `default_prompt`, and optional command filename aligned.
- Prefer the shortest clear name, such as `sideline-feature`, `interview-spec`, or `striq-feature-release-update`.
- Preserve existing misspelled or older folders as aliases unless the user explicitly asks to rename or remove them.

## Required File Shapes

### `SKILL.md`

Use only `name` and `description` in frontmatter.

Quote or fold descriptions that contain punctuation likely to confuse YAML, especially colons.

```markdown
---
name: example-skill
description: >-
  Create or run the example workflow. Use when the user asks for the example
  process, wants it exposed as a slash command, or says the picker entry is
  missing.
---

# Example Skill

## Overview

Use this skill to ...
```

### `agents/openai.yaml`

This is the picker-facing metadata. Do not omit it.

```yaml
interface:
  display_name: "Example Skill"
  short_description: "Run the example workflow"
  default_prompt: "Use $example-skill to run the example workflow."
policy:
  allow_implicit_invocation: true
```

`policy.allow_implicit_invocation` is optional, but include it for workflows that should trigger naturally from user phrasing, not only explicit `$skill-name` references.

Keep `default_prompt` short and include the literal `$skill-name`. Quote shell commands carefully so `$skill-name` is not expanded away while generating or patching metadata.

### Optional `~/.agent/commands/<skill-name>.md`

Create this wrapper when the user explicitly asks for a `/command` or when the workflow needs `$ARGUMENTS`.

```markdown
---
description: Run the example workflow from the slash command menu.
argument-hint: [example-context]
---

# Example Skill

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `<agent-config>/skills/example-skill/SKILL.md`.
2. Treat `$ARGUMENTS` as the context for the workflow.
3. If `$ARGUMENTS` is empty, infer the context from the current conversation when obvious; otherwise ask for the missing context.
```

## Workflow

1. Inspect comparable existing skills or commands before writing:
   - `find <agent-config>/skills -maxdepth 3 -path '*/agents/openai.yaml' -type f`
   - `find <agent-config>/commands -maxdepth 1 -type f -name '*.md'`
2. If creating a new skill, prefer the official initializer:
   - `python3 <agent-config>/skills/.system/skill-creator/scripts/init_skill.py <skill-name> --path <agent-config>/skills --interface display_name='...' --interface short_description='...' --interface default_prompt='Use $<skill-name> to ...'`
3. Replace template TODOs completely.
4. Add or patch `agents/openai.yaml` manually if helper scripts fail.
5. Add the optional command wrapper when requested.
6. Validate structure and metadata.
7. Report the exact files created and any visibility caveat.

## Validation

Run the official validator when available:

```bash
python3 <agent-config>/skills/.system/skill-creator/scripts/quick_validate.py <agent-config>/skills/<skill-name>
```

If it fails with `ModuleNotFoundError: No module named 'yaml'`, do not block. Use Ruby's YAML parser as the fallback:

```bash
ruby -ryaml -e "path='<agent-config>/skills/<skill-name>/SKILL.md'; text=File.read(path); data=YAML.safe_load(text.split('---',3)[1]); raise 'bad name' unless data['name']=='<skill-name>'; puts data.inspect"
ruby -ryaml -e "path='<agent-config>/skills/<skill-name>/agents/openai.yaml'; data=YAML.safe_load(File.read(path)); raise 'missing display_name' unless data.dig('interface','display_name'); raise 'missing default_prompt' unless data.dig('interface','default_prompt').to_s.include?('$<skill-name>'); puts data.inspect"
```

For command wrappers, validate the frontmatter too:

```bash
ruby -ryaml -e "path='<agent-config>/commands/<skill-name>.md'; text=File.read(path); data=YAML.safe_load(text.split('---',3)[1]); raise 'missing description' unless data['description']; puts data.inspect"
```

Confirm file placement:

```bash
find <agent-config>/skills/<skill-name> -maxdepth 3 -type f -print | sort
test -f <agent-config>/commands/<skill-name>.md && sed -n '1,40p' <agent-config>/commands/<skill-name>.md
```

## Visibility Troubleshooting

If the skill exists but is not visible:

- Confirm the skill is under `<agent-config>/skills`, not only a repo-local `skills/` folder.
- Confirm `agents/openai.yaml` exists and parses.
- Confirm `interface.display_name`, `interface.short_description`, and `interface.default_prompt` are present.
- Confirm `default_prompt` includes the literal `$skill-name`.
- Confirm the user is searching for terms in `display_name`, `short_description`, or the skill name.
- Do not treat restart as the first answer until these checks pass.

If the current thread's loaded skill list does not include a newly created skill, that can be a session-context snapshot. The on-disk picker metadata can still be correct; report the files and the validation evidence clearly.

## Final Response

Return:

- skill path
- `agents/openai.yaml` path
- command wrapper path, if created
- validation performed
- any remaining visibility caveat

