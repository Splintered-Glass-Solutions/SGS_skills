# Publication Boundary

The repository is designed to be useful to customers, practitioners, and
other agent builders without exposing the private context behind SGS's work.

## Include

- Generalizable skills and platform-neutral playbooks.
- Reusable templates, checklists, training materials, and diagrams.
- Examples that use placeholders instead of real customer, project, account,
  environment, or credential data.
- Safety rules that make authority, validation, and uncertainty explicit.

## Exclude

- Customer names, private project names, client communications, or meeting
  notes.
- API keys, tokens, credentials, secret paths, private URLs, and raw logs.
- Live portfolio ledgers, thread registries, approval records, and account
  state.
- Environment-specific migration instructions that only make sense for one
  organization or project.
- Personal operating preferences that are not necessary to understand the
  reusable workflow.

## Before opening a pull request

1. Read the whole diff, not only the file you changed.
2. Search for customer names, project names, personal names, absolute local
   paths, email addresses, secrets, IDs, and private URLs.
3. Replace concrete values with role-based placeholders.
4. Confirm every README link and every command wrapper has a valid source.
5. Run the repository's validation commands and report what they prove.

Public visibility is not proof that content is safe. Treat every commit as a
publication decision.
