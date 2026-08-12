# Worker Task Packet

```text
PROJECT:
REPO_OR_SOURCE:
OBJECTIVE:
CURRENT_KNOWN_STATE:
IN_SCOPE:
OUT_OF_SCOPE:
AUTHORITY_LIMITS:
APPROVAL_LEDGER_REFERENCE:
WORK_LEDGER_REFERENCE:
WORK_ID:
WORK_LEDGER_EVENT_EXPECTED:
STANDARDS_REGISTRY_REFERENCE:
STANDARDS_TO_APPLY:
APPROVAL_REQUIRED_FOR:
ACTION_PROPOSAL_REQUIRED_FOR:
ACTION_PROPOSAL:
  target:
  action:
  risk:
  proof_ready:
  approval_needed:
  rollback_or_undo:
REQUIRED_PROOF:
VALIDATION_EXPECTED:
STOP_CONDITIONS:
RETURN_FORMAT:
```

Default authority limits:

- Do not deploy to production, merge to `main`, send external messages, change
  DB grants/ownership/RLS/roles, purchase anything, or mutate customer-facing
  production data without explicit approval.
- Do not revert unrelated user or worker changes.
- If live code, data, or source state contradicts the packet, stop and report
  the discrepancy before continuing.
- Treat `$CODEX_HOME/portfolio/work-ledger.jsonl` as the durable
  operational state log. If this packet changes lifecycle state, return the
  exact work-ledger event that should be appended.
- Apply `$CODEX_HOME/portfolio/standards-registry.md`, especially the
  proof standards, approval gates, delegation standards, and any project-specific
  preferences relevant to this task.
- If the worker discovers a the user-gated decision, return
  `STATUS: needs_approval` and include the exact approval ledger item that
  should be created or updated.
- For any proposed send, deploy, DB change, thread creation/messaging, purchase,
  broad compute run, production mutation, protected-branch operation, or other
  gated action, include an `ACTION_PROPOSAL` with target, action, risk,
  proof_ready, approval_needed, and rollback_or_undo. Do not perform the action.

Default return format: use
`$CODEX_HOME/portfolio/templates/worker-closeout-contract.md`.
