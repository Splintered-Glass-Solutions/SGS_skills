---
name: save-skills
description: >-
  Analyze the current Codex conversation or selected text for repeated,
  reusable workflows that should become skills, dedupe candidates against the
  installed skill catalog, and create or improve high-confidence user-level
  Codex skills with picker metadata and slash-command wrappers. Use when
  Preston asks to save patterns from a thread as skills, mine a conversation
  for reusable commands, create skills from repeated instructions, or invokes
  the save-skills slash command.
---

# Save Skills

## Purpose

Turn durable workflow knowledge from the current conversation into concise,
reusable Codex skills and slash commands. This is a pattern-mining and local
skill-creation workflow.

Do not confuse it with `$save-skill`:

- `$save-skills` discovers and creates reusable skills from conversation
  patterns.
- `$save-skill` archives already-created skills to the private `SGS_skills`
  repository, commits, and pushes them.

Do not push to Git from this skill unless Preston explicitly also requests
`$save-skill` or asks to publish the generated skills.

## Inputs

Use, in priority order:

1. Explicitly selected or pasted text.
2. `$ARGUMENTS` from the slash-command wrapper.
3. The current conversation, including user corrections and repeated asks.

Supported modes:

- no arguments: analyze the current conversation and create high-confidence
  candidates;
- `dry-run`: return the candidate assessment without creating files;
- a topic or selected passage: analyze that scope plus the minimum conversation
  context needed to understand it;
- `include-project-specific`: allow stable project-specific candidates that
  would otherwise be generalized or skipped.

If the current conversation has been compacted, use the available thread recap,
durable artifacts, or thread-reading tools when available. Do not invent missing
history.

## Required Preflight

1. Read and follow:
   - `/Users/preston/.codex/skills/.system/skill-creator/SKILL.md`
   - `/Users/preston/.codex/skills/codex-slash-command-skill/SKILL.md`
2. Inventory existing user-level skills and slash wrappers:

```bash
rg --files /Users/preston/.codex/skills -g 'SKILL.md'
rg --files /Users/preston/.codex/skills -g 'agents/openai.yaml'
rg --files /Users/preston/.codex/commands -g '*.md'
```

3. Search names, descriptions, and workflow bodies for semantic overlap before
   proposing a new skill.
4. Read the closest matching skills in full. Prefer a focused update over a
   duplicate skill.

## Candidate Detection

Look for patterns such as:

- the same workflow requested or corrected two or more times;
- a stable sequence of preflight, execution, validation, and closeout steps;
- a repeated routing or judgment rule that general models routinely miss;
- a recurring cross-tool or cross-repository procedure;
- repeated output formatting, evidence, safety, or approval requirements;
- a workflow Preston explicitly says should become reusable.

Do not turn these into skills by default:

- one-off tasks or isolated fixes;
- facts better stored in project docs, registries, or memory;
- broad preferences already covered by global instructions or standards;
- vague intentions without a stable trigger and completion standard;
- temporary workarounds likely to expire quickly;
- aliases that add no meaningful discoverability;
- private message content, credentials, secrets, tokens, or customer-specific
  details that are unnecessary to run the generalized workflow.

## Candidate Scoring

Score each candidate from 0 to 3 on:

- `recurrence`: repeated evidence in the conversation;
- `repeatability`: stable steps and predictable inputs;
- `value`: meaningful time, quality, or risk reduction;
- `trigger_clarity`: a user phrase can reliably invoke it;
- `existing_coverage`: 0 means already covered; 3 means no adequate skill;
- `stability`: unlikely to become obsolete immediately.

Create a candidate only when:

- total score is at least 13 of 18;
- recurrence is at least 2, unless Preston explicitly requested the skill;
- trigger clarity and stability are each at least 2;
- it is not adequately covered by an existing skill.

Create no more than three new skills in one run. Report additional candidates
as deferred so Preston can review them without expanding the picker too quickly.

## Classification

Classify every candidate as one of:

- `create_new`: a distinct reusable workflow with no adequate skill;
- `improve_existing`: materially strengthens an existing skill;
- `covered`: an existing skill already handles it;
- `project_doc`: durable project knowledge, not a workflow skill;
- `preference_or_standard`: better expressed as an operating rule;
- `one_off`: insufficient recurrence or stability;
- `defer`: useful but below the creation threshold or beyond the three-skill cap.

For `improve_existing`, preserve the skill's established behavior, aliases, and
safety boundaries. Do not replace a broad existing workflow with a narrower
conversation-specific version.

## Skill Design Contract

For each `create_new` or `improve_existing` candidate:

1. Choose a short, verb-led, lowercase kebab-case name.
2. Create or update `/Users/preston/.codex/skills/<name>/SKILL.md`.
3. Create or update `/Users/preston/.codex/skills/<name>/agents/openai.yaml`.
4. Create `/Users/preston/.codex/commands/<name>.md` because this workflow is
   explicitly producing reusable slash commands.
5. Keep `SKILL.md` concise and focused on instructions the model would not
   reliably infer itself.
6. Include:
   - clear trigger description;
   - accepted inputs and context precedence;
   - required preflight;
   - decision or routing logic;
   - execution steps;
   - safety and authority limits;
   - validation requirements;
   - compact output contract;
   - stop or escalation conditions.
7. Add scripts or references only when they remove repeated code or keep a
   large body of conditional detail out of `SKILL.md`.
8. Generalize names, paths, client details, and examples unless the candidate is
   intentionally project-specific.

## Safety Rules

- Creating local skill and command files is authorized by invoking this skill.
- Do not deploy, send external messages, mutate production, alter database
  permissions, purchase anything, or change protected branches.
- A generated skill must preserve approval gates for those actions.
- Do not copy secrets, env values, private message bodies, or unnecessary
  customer data into generated skills.
- Do not update memory, standards registries, or project registries unless
  Preston separately asks for those changes.
- Do not commit or push generated skills without an explicit `$save-skill` or
  publish request.
- Never overwrite unrelated user edits. Read existing files and patch narrowly.

## Validation

For every created or changed skill:

```bash
python3 /Users/preston/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/preston/.codex/skills/<name>
```

If the Python validator cannot load YAML, use Ruby YAML parsing for `SKILL.md`,
`agents/openai.yaml`, and the command wrapper.

Also verify:

- folder name and frontmatter `name` match;
- `agents/openai.yaml` contains `display_name`, `short_description`, and a
  `default_prompt` containing the literal `$<name>`;
- command frontmatter parses and references the correct local skill path;
- no template TODOs remain;
- no secret-like values were introduced;
- the generated skill does not duplicate an existing trigger surface.

## Output

Use a compact report:

```text
🔎 PATTERNS REVIEWED:
✅ CREATED:
🛠️ IMPROVED:
♻️ ALREADY COVERED:
📝 DOC/STANDARD CANDIDATES:
⏸️ DEFERRED OR REJECTED:
🧪 VALIDATION:
📦 GIT STATUS: Not published; use $save-skill to archive and push.
```

For each created or improved skill, include its name, one-line purpose, and
clickable local paths. Do not paste full generated skill bodies into the final
response.
