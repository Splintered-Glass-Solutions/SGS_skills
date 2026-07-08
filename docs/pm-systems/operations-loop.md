# PM Operations Loop

The PM loop is designed to keep projects moving without creating noise. It
starts with durable state, routes only safe work, and closes the loop by
ingesting proof back into ledgers.

## End-To-End Loop

```mermaid
flowchart TD
  Start["Scheduled run or user request"] --> Load["Load registries, ledgers, standards, scorecards"]
  Load --> Generate["Generate and validate current-state"]
  Generate --> Scan["Scan the requested scope"]
  Scan --> Classify{"Classify each signal"}

  Classify --> Ignore["Ignore / duplicate / no action"]
  Classify --> Monitor["Monitor / passive status"]
  Classify --> Decision["Ask Preston / approval ledger"]
  Classify --> Delegate["Safe delegation"]
  Classify --> Escalate["Blocked escalation"]
  Classify --> Comms["Communication follow-up"]

  Ignore --> Local["Record locally if useful"]
  Monitor --> Local
  Decision --> Approval["Update approval ledger + ACTION_PROPOSAL if gated"]
  Delegate --> Route["Route via thread registry"]
  Escalate --> Approval
  Comms --> CommsLedger["Comms ledger, optional ClickUp if actionable"]

  Route --> ProjectThread["Verified project thread"]
  Route --> WorkerPacket["Bounded worker packet"]
  ProjectThread --> Closeout["Proof closeout"]
  WorkerPacket --> Closeout
  Closeout --> Ingest["PM ingest closeout"]
  Ingest --> WorkLedger["Append work-ledger event"]

  WorkLedger --> Scorecard["Append dispatcher scorecard"]
  Approval --> Scorecard
  CommsLedger --> Scorecard
  Local --> Scorecard
  Scorecard --> Refresh["Regenerate current-state"]
  Refresh --> Dashboard["Review PM dashboard"]
```

## Scan Classification

```mermaid
flowchart LR
  Signal["Signal"] --> Useful{"Useful?"}
  Useful -->|"No"| Ignore["Ignore"]
  Useful -->|"Yes"| Risk{"Needs action?"}
  Risk -->|"No"| Status["Record status/monitor"]
  Risk -->|"Yes"| Gate{"Gated?"}
  Gate -->|"Yes"| Proposal["Approval ledger + ACTION_PROPOSAL"]
  Gate -->|"No"| Route{"Best route?"}
  Route --> Thread["Verified project thread"]
  Route --> Worker["Bounded worker"]
  Route --> LocalTask["Local/ClickUp task candidate"]
  Route --> Clean["Clean-unreads candidate"]
```

Signals should be deduped against the approval ledger, work ledger, comms
ledger, clean-unreads reports, and latest dispatcher artifact before creating
new work.

## Delegation And Closeout

```mermaid
sequenceDiagram
  participant PM as PM thread
  participant Registry as Thread registry
  participant Project as Project thread
  participant Worker as Worker
  participant Ledger as Work ledger
  participant State as Current-state

  PM->>Registry: Check project route and authority
  alt verified thread and allowed
    PM->>Project: Send bounded prompt or continue thread
  else worker is better or thread is unavailable
    PM->>Worker: Create bounded worker packet
  else gated or ambiguous
    PM->>Ledger: Record waiting/blocked state
  end
  Project->>PM: Closeout with proof
  Worker->>PM: Closeout with WORK_LEDGER_UPDATE
  PM->>Ledger: Ingest validated event
  PM->>State: Regenerate current-state
```

Closeouts should include:

- status: `done`, `blocked`, `needs_approval`, or `no_new_signal`
- what changed or was found
- proof gathered
- validation commands and results
- files read or touched
- next recommended action
- approval proposal when needed
- `WORK_LEDGER_UPDATE` when lifecycle state changed

## Clean-Unreads Loop

```mermaid
flowchart TD
  Unread["Unread thread"] --> Complete{"Work complete?"}
  Complete -->|"No"| Keep["Keep unread"]
  Complete -->|"Yes"| FinishLine{"Finish-line or validation proof exists?"}
  FinishLine -->|"No"| Keep
  FinishLine -->|"Yes"| Remaining{"Remaining actions, blockers, approvals?"}
  Remaining -->|"Yes"| Keep
  Remaining -->|"No"| Safe["Safe to mark read"]

  Keep --> Report["Save clean-unreads report with next step"]
  Safe --> Cleared["Mark/read only safe items"]
  Cleared --> Report
  Report --> Current["Regenerate current-state"]
```

If a thread is not complete, it stays unread and the report must state the next
needed step.

## Comms Loop

```mermaid
flowchart TD
  Sources["Slack, email, texts, Teams, ClickUp, Skool, client comms"] --> Sync["PM comms sync"]
  Sync --> Candidates["Candidate communication items"]
  Candidates --> Ledger["Local comms ledger"]
  Ledger --> Check["PM comms check"]
  Check --> Actionable{"Needs response/action?"}
  Actionable -->|"No"| Archive["Local audit only"]
  Actionable -->|"Yes"| TaskPolicy["Local-first ClickUp policy"]
  TaskPolicy --> Dedupe["Dedupe by source/project/requester"]
  Dedupe --> Task["Create task only if authorized"]
  Dedupe --> LocalOnly["Otherwise report ClickUp not created"]
```

The PM comms system should flag possible obligations without sending replies or
creating external tasks unless that action is authorized.

## Outcome Measurement

```mermaid
flowchart LR
  Run["PM run"] --> Scorecard["Dispatcher scorecard"]
  Scorecard --> Activity["Activity counts"]
  Scorecard --> Outcomes["Outcome counts"]
  Scorecard --> Quality["Quality counts"]

  Activity --> A1["projects checked"]
  Activity --> A2["delegations prepared"]
  Activity --> A3["approvals requested"]

  Outcomes --> O1["blockers removed"]
  Outcomes --> O2["Preston decisions reduced"]
  Outcomes --> O3["delegated tasks completed"]
  Outcomes --> O4["stale projects revived"]
  Outcomes --> O5["unreads cleared safely"]
  Outcomes --> O6["comms converted to tasks"]

  Quality --> Q1["false positives"]
  Quality --> Q2["false-positive delegations"]
```

The scorecard should reward movement, not busyness. Outcome fields stay zero
unless the run artifact, work ledger, approval ledger, clean-unreads report, or
comms ledger proves actual movement.

## Daily Use

1. Start from `/pm-dashboard` or `PM Project Portfolio Manager`.
2. Refresh current-state before broad decisions.
3. Work the exact decision/blocker queue.
4. Delegate only bounded, proof-oriented work.
5. Ingest closeouts before cleaning unreads.
6. Use scorecards to ask: did the run move work or only create activity?
