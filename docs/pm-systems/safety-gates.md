# PM Safety Gates

The PM system is designed to keep autonomous work useful without allowing
dangerous or irreversible actions to happen quietly.

```mermaid
flowchart TD
  Action["Possible PM action"] --> Risk{"Is it gated?"}

  Risk -->|"Read-only scan / local proof / planning"| Allowed["Allowed"]
  Risk -->|"Deploy / prod mutation / send message / DB grants / protected branch / create threads"| Proposal["Requires ACTION_PROPOSAL"]
  Risk -->|"External task creation"| Policy{"Approved destination?"}

  Policy -->|"Local ledger only"| Local["Write local PM state"]
  Policy -->|"ClickUp approved"| ClickUp["Create ClickUp task"]
  Policy -->|"Unclear"| Ask["Ask user"]

  Allowed --> Evidence["Collect proof"]
  Proposal --> User["User approval"]
  User --> Execute["Execute if approved"]
```

## Always Approval-Gated

- production deploys or hotfixes
- production data mutation
- external sends: email, SMS, Slack, Teams, customer/client messages
- DB permission, grant, role, ownership, or RLS changes
- billing, purchasing, or paid external jobs
- protected branch operations
- destructive Git cleanup
- creating or messaging new persistent threads unless explicitly authorized

## Proof Separation

Keep these claims separate:

- local validation
- hosted/browser validation
- dev/staging live validation
- production live validation

Do not imply one proves another.

