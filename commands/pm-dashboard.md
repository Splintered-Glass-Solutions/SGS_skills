---
description: PM dashboard local read-only cockpit for portfolio work, blockers, decisions, unreads, comms, idle projects, and scorecards.
argument-hint: [optional-port]
---

# PM Dashboard

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow `$CODEX_HOME/skills/pm-dashboard/SKILL.md`.
2. If `$ARGUMENTS` contains a port number, run the dashboard with `PORT=<port>`.
3. Otherwise run:

```bash
node $CODEX_HOME/portfolio/portal/start-dashboard.mjs
```

## Guardrails

- This is a local read-only PM cockpit.
- Do not create ClickUp tasks, message threads, deploy, mutate production,
  change DB permissions, or perform protected-branch operations.
- Report the URL shown by the server, normally
  `http://127.0.0.1:8787/#dashboard`.
