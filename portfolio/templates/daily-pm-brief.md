# Daily PM Brief Template

Use this for a manual or scheduled portfolio sweep.

```text
PORTFOLIO STATUS:

DECISIONS NEEDED:

PENDING APPROVALS:

ACTION PROPOSALS:

BLOCKERS:

ACTIVE DELEGATIONS:

WORK LEDGER UPDATES:

STANDARDS APPLIED:

NEW SIGNAL SINCE LAST CHECK:

NO-NEW-SIGNAL AREAS:

PROOF:

RECOMMENDED NEXT ACTION:

APPROVAL LEDGER UPDATES:

CHECKPOINTS UPDATED:
```

Briefing rules:

- Keep it compact and decision-oriented.
- Prefer links/artifact paths over pasted logs.
- Separate safe next actions from gated next actions.
- Pull persistent approval/decision items from
  `$CODEX_HOME/portfolio/approval-ledger.md`.
- Pull operational work lifecycle from
  `$CODEX_HOME/portfolio/work-ledger.jsonl` and append compact events
  for picked-up, delegated, blocked, waiting, completed, resumed, superseded,
  cancelled, or no-new-signal work.
- Apply `$CODEX_HOME/portfolio/standards-registry.md` for quality
  bars, proof standards, approval gates, delegation standards, automation
  standards, and project-specific preferences.
- Report access blockers plainly.
