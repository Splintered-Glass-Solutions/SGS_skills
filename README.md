# SGS AI Operating Resources

Reusable skills, playbooks, training, and operating patterns from [Splintered
Glass Solutions](https://splinteredglass.solutions/).

SGS helps teams turn AI ambition into practical, governed work: clearer
planning, better context, safer execution, stronger QA, and systems people can
actually adopt. This repository is the public library behind that approach.

**Start here:** [AI Best Practices](packages/ai-best-practices/README.md) ·
[Skill catalog](docs/custom-skill-index.md) · [Portable playbooks](portable-agent-playbooks/README.md)

**Need help applying this to your team?** [Start a conversation with SGS](https://splinteredglass.solutions/contact).

## What is in this repository?

| Area | Use it for | Start here |
| --- | --- | --- |
| `skills/` | Codex-native workflows for planning, coding, debugging, QA, handoffs, and context management | [Skill catalog](docs/custom-skill-index.md) |
| `packages/` | Curated training and implementation-ready bundles | [Package index](packages/README.md) |
| `portable-agent-playbooks/` | Platform-neutral versions for Claude, Claude Code, Cursor, OpenAI agents, or another agent runtime | [Portable playbooks](portable-agent-playbooks/README.md) |
| `commands/` | Thin slash-command entry points for supported Codex skills | [Command map](docs/pm-systems/command-map.md) |
| `portfolio/templates/` | Reusable task packets, closeout contracts, and operating briefs | [Template guide](portfolio/templates/README.md) |
| `docs/` | Operating model, safety gates, contribution guidance, and publication rules | [Documentation hub](docs/README.md) |

## Featured resources

### Learn the operating model

[AI Best Practices](packages/ai-best-practices/README.md) is a practical
curriculum for individuals, engineering teams, PMs, and leaders. It covers
task classification, to-do capture and planning, multi-project and multi-repo
coding, debugging, hotfixes, QA, communication, handoffs, and token-efficient
AI use.

### Build with bounded execution

The core workflow is simple:

```text
Clarify the outcome and authority
        ↓
Plan a bounded slice
        ↓
Choose the right execution lane
        ↓
Implement or investigate
        ↓
Validate the actual result
        ↓
Reconcile, communicate, or hand off
```

Useful starting points include:

- [Expansive planning](skills/expansive-planning/SKILL.md)
- [Bulk editing threads](skills/bulk-edits-thread/SKILL.md)
- [Debugging and hotfixes](skills/hot-fix/SKILL.md)
- [Testing and QA](skills/test/SKILL.md)
- [Token and context management](skills/token-saver/SKILL.md)
- [Handoffs](skills/handoff/SKILL.md)
- [Public-resource improvement](skills/make-it-better/SKILL.md)

### Adapt patterns across agent platforms

The [portable playbooks](portable-agent-playbooks/README.md) preserve the
workflow and safety gates while replacing machine-specific paths and tool
assumptions with placeholders.

## What SGS believes

- Business outcomes come before tools.
- AI should be grounded in approved context and clear ownership.
- Bounded workflows are easier to trust than vague autonomy.
- Human review belongs around judgment and irreversible actions.
- Validation should distinguish local, merged, deployed, provider-backed, and
  customer-visible proof.
- Documentation and training are part of implementation, not an afterthought.

## Public boundary

This repository intentionally contains generalized, reusable material. It does
not contain live project state, customer data, credentials, private meeting
notes, environment-specific migration work, or personal operating ledgers.
See [the publication boundary](docs/publication-boundary.md) before adding a
new skill or package.

## Contributing and support

- Read [Contributing](CONTRIBUTING.md) before proposing a skill or package.
- Use [Security](SECURITY.md) for a suspected secret or sensitive-data issue.
- Browse the [documentation hub](docs/README.md) for the operating model and
  maintainer guidance.
- For AI implementation help, [contact SGS](https://splinteredglass.solutions/contact).

## About SGS

[Splintered Glass Solutions](https://splinteredglass.solutions/) partners with
growing companies across positioning, systems, workflow, data, practical AI,
custom tools, and launch support. This library shares the working patterns
behind that practice.
