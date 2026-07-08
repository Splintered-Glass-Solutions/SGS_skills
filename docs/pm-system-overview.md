# PM System Overview

This file is retained as a compact overview. The dedicated PM systems docs now
live under [docs/pm-systems](pm-systems/README.md).

## System Map

```mermaid
flowchart TD
  Preston["Preston"] --> PMThread["PM Thread / Portfolio HQ"]

  PMThread --> Skills["PM Skills + Slash Commands"]
  PMThread --> State["Portfolio State Files"]
  PMThread --> Threads["Project Threads / Workers"]
  PMThread --> Sources["External Work Sources"]

  Skills --> PMPortfolio["PM Project Portfolio Manager"]
  Skills --> PMDelegate["PM Delegate"]
  Skills --> PMPlate["PM Plate Spin"]
  Skills --> PMClean["PM Clean Unreads"]
  Skills --> PMCommsCheck["PM Comms Check"]
  Skills --> PMCommsSync["PM Comms Sync"]

  State --> ProjectRegistry["project-registry.md"]
  State --> ThreadRegistry["thread-registry.md"]
  State --> ApprovalLedger["approval-ledger.md"]
  State --> WorkLedger["work-ledger.jsonl"]
  State --> Standards["standards-registry.md"]
  State --> Scorecards["dispatcher scorecards"]

  Threads --> Persistent["Verified Persistent Project Threads"]
  Threads --> Workers["Bounded Worker Threads / Agents"]

  Sources --> Slack["Slack"]
  Sources --> Email["Email"]
  Sources --> ClickUp["ClickUp"]
  Sources --> Teams["Teams"]
  Sources --> Texts["Text Threads"]
  Sources --> Skool["Skool / Communities"]
```

## Main PM Loop

```mermaid
flowchart LR
  Scan["Scan portfolio state"] --> Classify["Classify work"]
  Classify --> Decisions["Decisions needed from Preston"]
  Classify --> Delegable["Safe delegation candidates"]
  Classify --> Blocked["Blocked / escalation items"]
  Classify --> Idle["Idle projects"]

  Delegable --> Delegate["PM Delegate"]
  Idle --> PlateSpin["PM Plate Spin"]
  Blocked --> Escalate["Escalate / ACTION_PROPOSAL"]
  Decisions --> Preston["Ask Preston"]

  Delegate --> ProjectThread["Relevant project thread"]
  ProjectThread --> Worker["Bounded worker or project-agent follow-up"]
  Worker --> Closeout["Proof-oriented closeout"]
  Closeout --> Ledger["Append work-ledger event"]
  Ledger --> NextScan["Next PM scan"]
```

## Command Responsibilities

```mermaid
flowchart TD
  Portfolio["/pm-project-portfolio-manager"] --> Queue["Decision queue + project status"]
  Delegate["/pm-delegate"] --> ProjectRoute["Route selected work"]
  Plate["/pm-plate-spin"] --> SafeMoves["Small safe next prompts"]
  Clean["/pm-clean-unreads"] --> ReadQueue["Unread cleanup queue"]
  CommsCheck["/pm-comms-check"] --> Followups["Communication follow-ups"]
  CommsSync["/pm-comms-sync"] --> CommsLedger["Refresh comms state"]
```

## Safety Gates

```mermaid
flowchart TD
  Action["Possible PM action"] --> Risk{"Is it gated?"}

  Risk -->|"Read-only scan / local proof / planning"| Allowed["Allowed"]
  Risk -->|"Deploy / prod mutation / send message / DB grants / protected branch / create threads"| Proposal["Requires ACTION_PROPOSAL"]
  Risk -->|"External task creation"| Policy{"Approved destination?"}

  Policy -->|"Local ledger only"| Local["Write local PM state"]
  Policy -->|"ClickUp approved"| ClickUp["Create ClickUp task"]
  Policy -->|"Unclear"| Ask["Ask Preston"]

  Allowed --> Evidence["Collect proof"]
  Proposal --> Preston["Preston approval"]
  Preston --> Execute["Execute if approved"]
```

## Current Gaps

- Closeout ingestion is still partly manual.
- Clean-unreads status should write durable run reports.
- Communication source coverage needs a normalized source registry and dedupe
  keys.
- A derived current-state view would make broad scans faster and less reliant
  on thread replay.
- A read-only PM dashboard would make active, blocked, waiting, and decision
  queues easier to inspect.
