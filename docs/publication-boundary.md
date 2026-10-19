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

## Generalize the procedure, not only the words

Remove private topology, personal defaults and historical permissions. Renaming a
customer to a numbered example still leaves an unusable workflow if it requires
that customer’s repository layout, fixture IDs, staff, voice, monitor or automation.
Use roles and explicit inputs; keep live bindings in private project configuration.
Retain public publisher attribution, upstream licenses and official tool/API names.

Before publishing, verify that a new user can identify prerequisites, choose their
own accounts and timezone, supply their own paths and reviewer, and understand the
result and limitations. Provide a local fallback or an exact missing-capability
blocker where possible. Preserve executable tool names, environment variables and
APIs when generating portable copies. A download never grants live authority.

## Required publication checks

```sh
python3 scripts/test-public-validation.py
ruby scripts/validate-skill-metadata.rb
ruby scripts/generate-portable-playbooks.rb
python3 scripts/validate-public-library.py
git diff --check
```

The validator checks the entire working library, including generated copies and
new files. It rejects personal home paths, non-example emails/resource IDs,
credential patterns, private automation bindings, unreviewed URL hosts, forbidden
artifacts, broken relative links, invalid Python and unmatched Markdown fences.
`public-hosts.json` records reviewed public provider/documentation hosts; do not
add a private host merely to silence a failure. Diagnostics report locations and
rule names without echoing matched secrets.

The checks do not prove arbitrary prose or binaries are anonymous or universally
usable. Review the full publication diff, examples, metadata, templates and scripts
for personal names, customer details and implicit private setup. Review binary
assets visually. Keep this semantic review mandatory even when all checks pass.
CI also checks that portable outputs match a fresh regeneration.
