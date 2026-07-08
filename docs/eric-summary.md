# Draft Summary For Eric

Hey Eric, thought you might find this interesting.

I have been setting up a project-management layer inside Codex that acts like a
portfolio manager across all of my active projects. The basic idea is that
there is one PM/control thread that watches the state of all the projects,
tracks decisions/blockers, delegates bounded work into the right project
threads, and keeps things from getting lost across a bunch of separate Codex
conversations.

The system has a few parts working together:

- Project registry: durable list of active projects, repos, boundaries, and
  allowed work.
- Thread registry: maps each project to a persistent Codex project-agent thread.
- Approval ledger: tracks anything that needs explicit approval before
  proceeding, like deploys, production mutations, external sends, DB permission
  changes, etc.
- Work ledger: append-only JSONL event log for picked-up, delegated, blocked,
  waiting, and completed work.
- Standards registry: proof standards and operating rules, like separating
  local validation from hosted/dev/prod validation.
- PM skills/slash commands:
  - `/pm-project-portfolio-manager`
  - `/pm-delegate`
  - `/pm-plate-spin`
  - `/pm-clean-unreads`
  - `/pm-comms-check`
  - `/pm-comms-sync`

The interesting part is that it is becoming fairly orchestrated. The PM thread
can scan all registered projects, identify what is idle or blocked, decide what
can safely be delegated, send work into the right persistent project thread,
and then ingest the result back into the ledger. It also has guardrails so it
does not deploy, send messages, mutate production, create new threads, or touch
sensitive systems without an explicit action proposal.

We also set up clean-unread logic so Codex threads only get marked read if the
work is actually complete, validation has run, dev/hosted proof exists when
applicable, and no remaining action items or approvals are outstanding.
Otherwise they stay unread and the PM report tells me the next required step.

The end goal is basically a lightweight autonomous PM system: keep agents
working, keep projects from going stale, keep decisions surfaced, and make sure
important communications or project tasks do not slip through the cracks. Chat
is the control surface, but the actual state lives in durable ledgers and
registries so it survives thread compaction and can be audited later.

Still some gaps to fill, but it is already useful. Next I want to tighten
closeout ingestion, communications monitoring, and a simple PM dashboard/current
state view.

I can share the PM skills repo with you too if you want to look at how the
skills and command wrappers are structured.

