# PM System Overview

This is the compact map of the SGS/Codex project-management operating system.
The deeper docs live under [docs/pm-systems](pm-systems/README.md).

The core idea is simple: chat is the control surface, but durable files are the
source of truth. The PM thread coordinates scans and decisions, project threads
hold project context, workers do bounded work, and ledgers preserve state across
compaction, restarts, and future PM passes.

## Operating Picture

```mermaid
flowchart TD
  Operator["Preston / operator"] --> PM["PM thread / portfolio HQ"]

  PM --> Skills["PM skills and slash commands"]
  PM --> State["Local durable PM state"]
  PM --> ProjectThreads["Verified project threads"]
  PM --> Workers["Bounded workers / agents"]
  PM --> Cockpit["Read-only PM dashboard"]

  Sources["Slack, email, texts, Teams, ClickUp, Skool, client comms"] --> CommsSync["PM comms sync/check"]
  CommsSync --> LocalLedger["Local comms and work ledgers"]
  LocalLedger --> State

  Skills --> Scan["Portfolio scan"]
  Skills --> Delegate["Delegate selected work"]
  Skills --> PlateSpin["Revive idle projects"]
  Skills --> CleanUnreads["Clean unread threads"]
  Skills --> Ingest["Ingest worker closeouts"]

  State --> Registries["Project/thread registries"]
  State --> Approvals["Approval ledger"]
  State --> WorkLedger["Work ledger"]
  State --> Standards["Standards registry"]
  State --> Scorecards["Dispatcher scorecards"]
  State --> CurrentState["Generated current-state.json/md"]

  Scan --> CurrentState
  Delegate --> ProjectThreads
  ProjectThreads --> Workers
  Workers --> Ingest
  Ingest --> WorkLedger
  WorkLedger --> CurrentState
  CurrentState --> Cockpit
  Scorecards --> Cockpit
```

## Durable State Flow

```mermaid
flowchart LR
  Observation["Observed signal"] --> Record["Write local durable record first"]
  Record --> Classify{"Actionable?"}

  Classify -->|"No: passive, duplicate, complete"| LedgerOnly["Keep local audit trail only"]
  Classify -->|"Yes: decision, blocker, worker follow-up, failed validation, comms action"| ActionSurface["Action surface"]

  ActionSurface --> Approval{"Preston-gated?"}
  Approval -->|"Yes"| Proposal["ACTION_PROPOSAL + approval ledger"]
  Approval -->|"No"| Route["Route to project thread, worker, or ClickUp"]

  Route --> ClickUp{"ClickUp authorized and unique?"}
  ClickUp -->|"Yes"| Task["Create concise ClickUp task"]
  ClickUp -->|"No"| LocalOnly["Report ClickUp not created"]

  Proposal --> CurrentState["Regenerate current-state"]
  Task --> CurrentState
  LocalOnly --> CurrentState
  LedgerOnly --> CurrentState
```

## Outcome Loop

```mermaid
sequenceDiagram
  participant PM as PM thread
  participant State as Local state files
  participant Project as Project thread
  participant Worker as Worker/agent
  participant Dash as PM dashboard

  PM->>State: Read registries, ledgers, standards, scorecards
  PM->>State: Generate and validate current-state
  PM->>PM: Classify decisions, blockers, idle lanes, comms, unreads
  PM->>Project: Route bounded work when verified and allowed
  Project->>Worker: Execute narrow task
  Worker->>PM: Closeout with proof and WORK_LEDGER_UPDATE
  PM->>State: Ingest closeout, validate ledgers
  PM->>State: Append scorecard outcome metrics
  State->>Dash: Render active work, blockers, decisions, unreads, comms, outcomes
```

## Command Families

- `PM Project Portfolio Manager`: broad scan, durable state refresh, decisions,
  blockers, safe next moves, scorecard updates.
- `PM Delegate`: route highlighted work to the right verified project thread or
  bounded worker.
- `PM Plate Spin`: identify small safe next prompts for idle projects.
- `PM Clean Unreads`: mark only truly complete unread threads as read and keep
  incomplete work visible.
- `PM Ingest Closeout`: ingest worker/project closeouts into the work ledger and
  refresh current-state.
- `PM Comms Check` and `PM Comms Sync`: consolidate communication follow-ups
  from monitored channels.
- `PM Dashboard`: launch the local read-only cockpit.

## Safety Rules

No deploys, production mutations, external messages, database permission/RLS
changes, protected-branch operations, purchases, or Codex thread creation or
messaging happen without a fresh `ACTION_PROPOSAL` and explicit approval.

ClickUp is an action surface, not the source of truth. Every observed item lands
in the local ledger/report layer first; ClickUp tasks are created only for
actionable follow-ups with dedupe keys.

## Current Health

The system now has:

- durable registries, approval ledger, work ledger, standards registry, and
  dispatcher scorecards
- generated `current-state.json` and `current-state.md`
- closeout ingestion
- delegation watchlist
- durable clean-unreads reports
- local ledger/ClickUp hybrid policy
- read-only PM dashboard
- dispatcher outcome scorecards that separate activity from actual movement

The next useful evolution is trend reporting across scorecard outcomes and
cleaner automated comms coverage across every source.
