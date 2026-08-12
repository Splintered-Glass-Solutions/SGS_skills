# Contributing

SGS welcomes reusable improvements that help people apply AI with more clarity,
safety, and operational discipline.

## Good contributions

- Solve a repeatable problem across more than one project or organization.
- State when the skill should trigger and when it should stop.
- Separate read-only inspection from mutation, deployment, and external sends.
- Define the evidence needed to claim success.
- Use placeholders for paths, accounts, projects, customers, and tools.
- Include a compact example or validation checklist when it improves adoption.

## Before you submit

- Read [the publication boundary](docs/publication-boundary.md).
- Keep the change focused and update the relevant index or package README.
- Check for stale links, duplicate names, broken command wrappers, and private
  context.
- Run `ruby scripts/generate-portable-playbooks.rb` when a skill changes.
- Report validation results and any remaining uncertainty in the pull request.

## Scope and licensing

Unless a file states otherwise, contributions remain subject to the repository
owner's copyright and are not automatically licensed for unrestricted reuse.
Ask before copying a package into a commercial product or redistributing it as
a standalone offering.
