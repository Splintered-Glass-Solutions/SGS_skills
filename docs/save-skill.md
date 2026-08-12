# Maintainer Archive Workflow

This is the maintainer workflow for preserving a generalized local skill in
the SGS resource library. It keeps the Codex-native source, optional command
wrapper, portable playbook, and catalog entry aligned.

## Before archiving

1. Confirm the workflow is useful beyond one project or customer.
2. Remove private names, customer context, credentials, live state, and
   environment-specific assumptions.
3. Replace machine-specific paths with `$CODEX_HOME`, `<workspace>`, or another
   explicit placeholder.
4. Decide whether the skill belongs in the public catalog or should remain in a
   private operating archive.

## What to save

- `skills/<skill-name>/SKILL.md`
- `skills/<skill-name>/agents/openai.yaml`
- additional reference files or scripts that are safe to share
- `commands/<skill-name>.md` only when the wrapper has a matching source skill
- generated portable playbooks under
  `portable-agent-playbooks/playbooks/<skill-name>/`
- a catalog entry in `docs/custom-skill-index.md`

## Normal run

1. Resolve the skill name or source path.
2. Check the repository for unrelated dirty work.
3. Validate the skill structure and publication boundary.
4. Archive the generalized skill and matching command wrapper.
5. Regenerate portable playbooks:

   ```bash
   ruby scripts/generate-portable-playbooks.rb
   ```

6. Validate YAML/frontmatter, Markdown fences, links, and sensitive-content
   scans.
7. Review the full diff before committing and pushing.

## Safety boundary

The archive workflow must not copy secrets, `.env` files, token-bearing logs,
production data, portfolio ledgers, or private client artifacts. It does not
deploy, send messages, mutate production systems, change permissions, or
perform protected-branch operations.
