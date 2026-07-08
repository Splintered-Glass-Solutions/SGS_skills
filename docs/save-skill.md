# Save Skill Workflow

`/save-skill` archives a local Codex skill into this private SGS skills repo,
regenerates the portable playbook version, commits the result, and pushes it to
GitHub.

## When To Use It

Use this command when a custom skill has been created or updated under
`/Users/preston/.codex/skills` and should be preserved in
`Splintered-Glass-Solutions/SGS_skills`.

Examples:

```text
/save-skill recap
/save-skill /Users/preston/.codex/skills/recap/SKILL.md
/save-skill close-thread
```

If selected text contains a `<skill>` block with a `name` and `path`, the command
uses that as the source skill.

## What It Saves

- `skills/<skill-name>/SKILL.md`
- `skills/<skill-name>/agents/openai.yaml`
- any additional files inside the local skill folder
- `commands/<skill-name>.md` when a local slash-command wrapper exists
- generated portable playbooks under
  `portable-agent-playbooks/playbooks/<skill-name>/`
- index entries in `docs/custom-skill-index.md` and
  `portable-agent-playbooks/README.md`

## Normal Run

1. Resolve the skill name or path.
2. Check `/Users/preston/Code/SGS_skills` for unrelated dirty work.
3. Validate the local skill structure.
4. Archive the local skill and command wrapper into the repo.
5. Update `docs/custom-skill-index.md`.
6. Run:

```bash
ruby /Users/preston/Code/SGS_skills/scripts/generate-portable-playbooks.rb
```

7. Run targeted validation for YAML/frontmatter and markdown fences.
8. Commit and push to `origin/main`.

## Safety Boundaries

The command must not copy secrets, `.env` files, token-bearing logs, production
data, portfolio ledgers, or unrelated local artifacts. It must not deploy, send
messages, mutate production systems, change database permissions, or perform
protected-branch operations.

If validation or push fails, the command reports the exact failure and leaves the
local repo state visible for follow-up.
