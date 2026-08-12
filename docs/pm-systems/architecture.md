# PM System Architecture

The PM system is a local-first operating layer around Codex. It is designed to
keep many projects moving without relying on chat history as memory. Agents can
scan, classify, delegate, and validate, but the durable state lives in files.

## Architecture At A Glance

```mermaid
flowchart TD
  subgraph Control["Control surface"]
    PMThread["PM thread / Portfolio HQ"]
    Slash["Slash commands"]
    Skills["PM skills"]
    Dashboard["Read-only PM dashboard"]
  end

  subgraph Durable["Durable local state"]
    Projects["project-registry.md"]
    Threads["thread-registry.md"]
    Approvals["approval-ledger.md"]
    Work["work-ledger.jsonl"]
    Standards["standards-registry.md"]
    Comms["comms ledger + source registry"]
    Clean["clean-unreads reports"]
    Scorecards["dispatcher-scorecard.jsonl"]
    Current["current-state.json + current-state.md"]
  end

  subgraph Execution["Execution layer"]
    ProjectThreads["Verified persistent project threads"]
    Workers["Bounded workers / subagents"]
    SharedDocs["Shared-docs repos for umbrella context"]
  end

  subgraph External["External sources and action surfaces"]
    Slack["Slack"]
    Mail["Email / Superhuman / Gmail / Outlook"]
    ClickUp["ClickUp"]
    Teams["Teams"]
    Texts["Text threads"]
    Skool["Skool communities"]
  end

  PMThread --> Slash
  PMThread --> Skills
  Skills --> Durable
  Durable --> Current
  Current --> Dashboard
  Scorecards --> Dashboard
  Clean --> Dashboard
  Comms --> Dashboard

  External --> Comms
  External --> PMThread
  PMThread --> ProjectThreads
  PMThread --> Workers
  ProjectThreads --> Workers
  SharedDocs --> ProjectThreads
  Workers --> Work
  ProjectThreads --> Work
  Work --> Current
  Approvals --> Current
  Standards --> PMThread
```

## State Is Layered

```mermaid
flowchart LR
  Inputs["Raw inputs"] --> Ledgers["Append-only ledgers and reports"]
  Ledgers --> Derived["Generated current-state"]
  Derived --> Views["PM reports and dashboard"]
  Views --> Decisions["Human decisions and routing"]
  Decisions --> Inputs

  Inputs -.->|"Slack, email, ClickUp, Teams, texts, Skool, Codex threads"| Ledgers
  Ledgers -.->|"approval ledger, work ledger, comms ledger, clean-unreads, scorecards"| Derived
  Derived -.->|"active, blocked, waiting, decisions, unreads, comms, outcomes"| Views
```

Raw inputs can be messy and spread across tools. Ledgers normalize the observed
facts. `current-state` is regenerated from those sources so PM scans can start
from a compact machine-readable snapshot instead of replaying every thread.

## Command And Skill Routing

```mermaid
flowchart TD
  Ask["User request or scheduled run"] --> Scope{"What kind of PM work?"}

  Scope -->|"Broad portfolio state"| Portfolio["PM Project Portfolio Manager"]
  Scope -->|"Highlighted work to route"| Delegate["PM Delegate"]
  Scope -->|"Idle project motion"| Plate["PM Plate Spin"]
  Scope -->|"Unread thread cleanup"| CleanUnreads["PM Clean Unreads"]
  Scope -->|"Worker/project closeout"| Ingest["PM Ingest Closeout"]
  Scope -->|"Communication follow-ups"| CommsCheck["PM Comms Check"]
  Scope -->|"Refresh comms sources"| CommsSync["PM Comms Sync"]
  Scope -->|"Visual cockpit"| Dash["PM Dashboard"]

  Portfolio --> Current["Refresh current-state"]
  Delegate --> Registry["Check thread registry"]
  Plate --> Registry
  CleanUnreads --> Report["Write clean-unreads report"]
  Ingest --> Work["Append work-ledger event"]
  CommsCheck --> Comms["Read comms ledger"]
  CommsSync --> Comms
  Dash --> Current

  Registry --> Route{"Verified project thread?"}
  Route -->|"Yes and allowed"| ProjectThread["Message/continue verified project thread"]
  Route -->|"No or worker better"| WorkerPacket["Create bounded worker packet"]
  Route -->|"Gated or ambiguous"| Approval["Approval ledger + ACTION_PROPOSAL"]
```

## Delegation Lifecycle

```mermaid
stateDiagram-v2
  [*] --> Observed
  Observed --> Recorded: local durable record
  Recorded --> Routed: safe delegate
  Recorded --> WaitingApproval: the user-gated
  Recorded --> NoAction: duplicate/passive/no next step
  Routed --> InProgress: project thread or worker starts
  InProgress --> Blocked: blocker found
  InProgress --> Completed: proof closeout
  Blocked --> WaitingApproval: needs decision/escalation
  Completed --> Ingested: PM ingest closeout
  Ingested --> CleanUnread: if unread and complete
  CleanUnread --> [*]
  NoAction --> [*]
```

Every lifecycle change should be reflected in `work-ledger.jsonl`, and every
the user-gated decision should be reflected in `approval-ledger.md`.

## Local Ledger / ClickUp Hybrid

```mermaid
flowchart TD
  Item["Observed item"] --> Local["Write/update local durable record"]
  Local --> Actionable{"Actionable follow-up?"}

  Actionable -->|"No"| Audit["Keep as audit/status only"]
  Actionable -->|"Yes"| Kind{"Why actionable?"}

  Kind --> Decision["the user decision needed"]
  Kind --> Followup["Worker/project follow-up"]
  Kind --> Validation["Failed validation or retest"]
  Kind --> Blocker["Blocked escalation"]
  Kind --> CommsAction["Communication response/action"]

  Decision --> Dedupe["Dedupe key + source refs"]
  Followup --> Dedupe
  Validation --> Dedupe
  Blocker --> Dedupe
  CommsAction --> Dedupe

  Dedupe --> ClickUp{"ClickUp authorized and unique?"}
  ClickUp -->|"Yes"| Task["Create concise ClickUp task"]
  ClickUp -->|"No"| LocalOnly["Local source of truth; report ClickUp not created"]
```

The local ledger is the audit and memory layer. ClickUp is only the actionable
task surface. Ready-to-mark-read items, passive waiting statuses, duplicates,
completed/no-op states, and observations with no next action stay local only.

## Dispatcher Scorecards

```mermaid
flowchart LR
  Run["Dispatcher run"] --> Activity["Activity metrics"]
  Run --> Outcomes["Outcome metrics"]
  Run --> Quality["Quality metrics"]

  Activity --> Prepared["delegations prepared"]
  Activity --> Approvals["approvals requested"]
  Activity --> Checks["projects checked"]

  Outcomes --> Removed["blockers removed"]
  Outcomes --> Decisions["the user decisions reduced"]
  Outcomes --> Done["delegated tasks completed"]
  Outcomes --> Revived["stale projects revived"]
  Outcomes --> Unreads["unread threads cleared safely"]
  Outcomes --> CommsTasks["comms items converted to tasks"]

  Quality --> FalsePositives["false positives"]
  Quality --> FalseDelegations["false-positive delegations"]
  Quality --> Evidence["evidence paths"]
```

Scorecards intentionally separate activity from movement. Preparing packets,
surfacing approvals, and checking projects are useful activity. They are not
outcomes until a blocker clears, a decision is reduced, a delegated task
finishes, a stale project revives, an unread is safely cleared, or a comms item
becomes an actionable task.

## Safety Boundary

```mermaid
flowchart TD
  Action["Potential action"] --> Gate{"Gated action?"}

  Gate -->|"Read-only scan, local docs, local validation"| Allowed["Allowed"]
  Gate -->|"Deploy, prod mutation, external send, DB grants/RLS/ownership, purchase, protected branch, thread create/message"| Proposal["ACTION_PROPOSAL required"]
  Gate -->|"External task creation"| TaskGate["Local-first ClickUp policy"]

  Proposal --> Approval["Explicit the user approval"]
  Approval --> Execute["Execute exact approved action"]
  TaskGate --> LocalRecord["Local durable record first"]
  LocalRecord --> Dedupe["Dedupe and authorization"]
  Dedupe --> Task["Create task only if authorized"]
  Allowed --> Proof["Collect proof and update ledgers"]
```

## Core Principle

The PM thread can reason, coordinate, and explain, but it should not be the only
place where project state exists. Durable records and generated current-state
are what make the system survivable, auditable, and automatable.
