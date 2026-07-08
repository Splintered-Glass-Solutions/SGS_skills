# PM Operations Loop

The main PM loop starts with a portfolio scan, classifies work, delegates only
safe bounded tasks, and then ingests proof back into durable state.

```mermaid
flowchart LR
  Scan["Scan portfolio state"] --> Classify["Classify work"]
  Classify --> Decisions["Decisions needed from user"]
  Classify --> Delegable["Safe delegation candidates"]
  Classify --> Blocked["Blocked / escalation items"]
  Classify --> Idle["Idle projects"]

  Delegable --> Delegate["PM Delegate"]
  Idle --> PlateSpin["PM Plate Spin"]
  Blocked --> Escalate["Escalate / ACTION_PROPOSAL"]
  Decisions --> User["Ask user"]

  Delegate --> ProjectThread["Relevant project thread"]
  ProjectThread --> Worker["Bounded worker or project-agent follow-up"]
  Worker --> Closeout["Proof-oriented closeout"]
  Closeout --> Ledger["Append work-ledger event"]
  Ledger --> NextScan["Next PM scan"]
```

## Steady State

```mermaid
flowchart LR
  PMScan["PM scan"] --> Prompt["Next safe prompt"]
  Prompt --> ProjectThread["Project thread"]
  ProjectThread --> Work["Worker executes"]
  Work --> Proof["Proof + closeout"]
  Proof --> Ledger["Ledger update"]
  Ledger --> Clean["Clean unread if truly done"]
  Clean --> PMScan
```

## Closeout Contract

Workers should return:

- status: `done`, `blocked`, `needs_approval`, or `no_new_signal`
- what changed or was found
- proof gathered
- validation commands and results
- files read/touched
- next recommended action
- handoff receipt
- approval proposal when needed
- work-ledger update recommendation

The PM thread reviews that closeout before updating durable state.

