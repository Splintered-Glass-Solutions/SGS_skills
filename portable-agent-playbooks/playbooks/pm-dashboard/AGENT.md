# PM Dashboard Agent Playbook

This is a platform-neutral version of the `pm-dashboard` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

PM dashboard: use when the user wants the local read-only PM cockpit/dashboard for active delegated work, blocked work, decisions needed, unread cleanup, comms follow-ups, idle projects, and recent dispatcher scorecards.

## Portability Notes

- Replace `<agent-config>` with the local configuration folder for the
  target agent platform.
- Replace `<workspace>` with the user's active project/workspace root.
- Treat slash commands and `$skill-name` references as invocation hints.
  If the target platform does not support slash commands, paste this
  playbook into the agent's custom instructions or project memory.
- Keep all original safety gates. Do not send messages, deploy, mutate
  production data, change permissions, or perform irreversible actions
  without explicit approval from the user.
- If a referenced connector or tool is not available in the target platform,
  stop and report the missing capability instead of simulating external
  actions.

## Instructions

# PM Dashboard

## Purpose

Open the local read-only PM cockpit quickly.

The dashboard summarizes:

- 🧵 active delegated work
- 🔴 blocked work
- ⚠️ decisions needed
- 🧭 delegation watchlist flags
- 🧹 unread cleanup queue
- 📬 comms follow-ups
- 😴 idle projects
- 📊 recent dispatcher scorecards and outcome movement
- 🔒 source/read-only state

## Quick Start

Run:

```bash
node <agent-config>/portfolio/portal/start-dashboard.mjs
```

Default URL:

```text
http://127.0.0.1:8787/#dashboard
```

The launcher refreshes and validates current-state first, then starts
`<agent-config>/portfolio/portal/server.mjs` with:

```text
PM_DASHBOARD_READ_ONLY=1
```

## Rules

- The dashboard is local-only and binds to `127.0.0.1`.
- Treat the cockpit as read-only. Do not use it to create tasks, message
  threads, deploy, or mutate production.
- If a port is busy, the server automatically tries the next ports.
- If current-state generation or validation fails, stop and report the failing
  command instead of opening a stale dashboard.
- Use the dashboard for fast review; use the specific PM skills for action:
  `$pm-delegate`, `$pm-ingest-closeout`, `$pm-clean-unreads`,
  `$pm-comms-check`, `$pm-comms-sync`, `$pm-plate-spin`, and
  `$pm-project-portfolio-manager`.

## Output Shape

```text
📊 PM DASHBOARD:
🔗 URL:
✅ PREFLIGHT:
🧾 SOURCE STATE:
⚠️ NOTES:
```

