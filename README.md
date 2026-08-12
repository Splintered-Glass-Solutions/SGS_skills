# SGS Skills

Private repo for reusable Codex skills, slash-command wrappers, and PM
orchestration templates used by Splintered Glass Solutions.

## What Is Included

- `skills/`: all archived user-level custom Codex skills from
  `/Users/preston/.codex/skills`, excluding only system/bundled/plugin skills.
  This includes PM skills plus custom workflows such as `handoff`,
  `orchestrator-mode`, `codex-safe-run`, `feature-finish-line`,
  `full-suite-tests`, `bonfire-feature-release-update`,
  `striq-feature-release-update`, `make-it-better`, `next-step`,
  `autonomous-feature-build`, and the Bonfire/StrIQ/SGS helper skills.
- `commands/`: user-level slash-command wrappers from `/Users/preston/.codex/commands`.
- `portfolio/templates`: worker packet, worker closeout, and daily PM brief
  templates.
- `docs/custom-skill-index.md`: current archived skill list.
- `portable-agent-playbooks/`: generalized versions of every archived skill for
  Claude, Claude Code, Cursor, OpenAI/Codex, or other agent platforms.
- `docs/ai-best-practices/`: reusable training materials for applying AI to
  planning, multi-project and multi-repo coding, debugging, hotfixes, QA,
  handoffs, communication, and context/token management.

## What Is Not Included

Live portfolio state is intentionally not copied here by default:

- project/thread registries
- approval ledgers
- work-ledger events
- dispatcher scorecards
- private source artifacts

Those files may include live project names, thread IDs, client context, or
operational details. Keep this repo focused on reusable PM system mechanics
unless a specific state snapshot is intentionally sanitized for sharing.

## Operating Model

The PM thread is the control room. Skills encode the workflows. The portfolio
folder is the durable source of truth. Persistent project threads keep project
context warm. Bounded workers execute scoped tasks and return proof-oriented
closeouts. Ledgers make work state survive chat compaction.

See:

- [docs/pm-systems](docs/pm-systems/README.md) for the dedicated PM systems
  diagrams, operating loop, safety gates, unread cleanup logic, and roadmap.
- [docs/pm-system-overview.md](docs/pm-system-overview.md) for the compact
  overview.
- [docs/save-skill.md](docs/save-skill.md) for the `/save-skill` workflow that
  archives local Codex skills into this repo, regenerates portable playbooks,
  commits, and pushes.

## Portable Versions

For non-Codex platforms, use
[portable-agent-playbooks/README.md](portable-agent-playbooks/README.md).
Each archived skill has a platform-neutral `AGENT.md` plus `manifest.yaml`.
The portable versions replace machine-specific paths with placeholders such as
`<agent-config>` and `<workspace>`, while preserving safety gates and workflow
structure.

## AI Best Practices Training

Start with [docs/ai-best-practices/README.md](docs/ai-best-practices/README.md).
The package includes the operating model, task playbooks, Codex skill routing,
reusable templates, checklists, facilitator exercises, and an assessment rubric.

## Install Locally

From this repo:

```bash
./scripts/install-local.sh
```

This copies archived skills, command wrappers, and portfolio templates into
`/Users/preston/.codex`. Review the script before running on another machine.
