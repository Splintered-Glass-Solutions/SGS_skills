# PM Systems

This folder documents the SGS/Codex project-management operating system: how
the PM thread, project threads, workers, skills, ledgers, approvals,
communication monitors, dashboard, and dispatcher outcome scorecards work
together. The examples are tool-agnostic patterns; replace the named connectors
or task systems with the ones your organization actually uses.

## Files

- [architecture.md](architecture.md): high-level system map, durable state,
  routing, scorecards, and safety boundary.
- [operations-loop.md](operations-loop.md): day-to-day portfolio scan,
  delegation, closeout, clean-unreads, comms, and outcome flow.
- [command-map.md](command-map.md): PM skill and slash-command responsibilities.
- [safety-gates.md](safety-gates.md): approval boundaries and action rules.
- [unread-cleanup.md](unread-cleanup.md): how unread Codex/project threads are
  classified.
- [gaps-and-roadmap.md](gaps-and-roadmap.md): known gaps and recommended next
  improvements.

The diagrams are written in Mermaid so GitHub can render them directly.
