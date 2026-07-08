# SGS Skills

Private repo for reusable Codex project-management skills, slash-command
wrappers, and PM orchestration templates used by Splintered Glass Solutions.

## What Is Included

- `skills/pm-project-portfolio-manager`: portfolio scan, decisions, blockers,
  delegation candidates, scorecard/ledger updates.
- `skills/pm-delegate`: route selected work to the right verified project
  thread or bounded worker.
- `skills/pm-plate-spin`: find idle projects and propose small safe next moves.
- `skills/pm-clean-unreads`: classify unread Codex threads as ready to mark read
  or keep unread with next steps.
- `skills/pm-comms-check`: consolidate outstanding communications from the PM
  comms ledger.
- `skills/pm-comms-sync`: manually refresh the PM communications monitor.
- `commands/pm-*.md`: slash-command wrappers for the same workflows.
- `portfolio/templates`: worker packet, worker closeout, and daily PM brief
  templates.

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

See [docs/pm-system-overview.md](docs/pm-system-overview.md).

## Install Locally

From this repo:

```bash
./scripts/install-local.sh
```

This copies skills, command wrappers, and portfolio templates into
`/Users/preston/.codex`. Review the script before running on another machine.

