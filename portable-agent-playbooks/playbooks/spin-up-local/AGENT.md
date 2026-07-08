# Spin Up Local Agent Playbook

This is a platform-neutral version of the `spin-up-local` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Start a project locally so the user can test the exact work currently in progress. Use when the user says spin up local, local, run locally, let me test, start the app, give me the local link, or asks to verify that local frontend, backend, API, worker, or multi-repo changes are being used by the test server.

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

# Spin Up Local

## Overview

Use this skill to turn the current local workspace into a testable app URL. The job is not just to run a dev command; it is to prove which local code, branch, port, backend/API target, and related repos the browser will actually exercise.

## Workflow

1. Classify the request as build work unless it is only a lookup.
2. Identify the active repo and current local work:
   - Run `pwd`, `git status --short --branch`, `git branch --show-current`, `git remote -v`, and `git worktree list`.
   - Note dirty files, untracked files, branch name, upstream branch, and any sibling worktrees that may hold related work.
   - Do not discard, stash, reset, or merge user work just to start a server.
3. Discover the local app command from repo-native sources:
   - Prefer `package.json`, `README`, `Makefile`, `docker-compose*`, framework config, or repo docs.
   - Use existing dependencies if installed. Install only when required and safe for the repo.
   - Pick an open port instead of killing an unrelated listener.
4. Map runtime targets before giving the user the link:
   - Inspect relevant local env files for API/base URL names without exposing secrets.
   - Report whether the app is using local services, a dev/stage backend, production backend, mocks, or unknown targets.
   - For proxy-based apps, trace the server route or proxy config far enough to name the effective upstream.
5. Include related repos when the project requires them:
   - Look for sibling repos from env targets, docs, workspace files, git remotes, docker compose, package workspace config, or known project conventions.
   - If the frontend depends on local backend/API changes, start those local services too or explicitly report that the frontend is pointed at a remote backend.
   - If a required related repo has uncommitted local changes, run from that worktree rather than a clean clone, unless that would risk data mutation or production access.
6. Start the app from the worktree that contains the changes the user needs to test:
   - Use a long-running shell session for dev servers.
   - Keep the server running unless the user asks to stop it.
   - Capture the local URL, port, process/session, and command.
7. Verify reachability:
   - Check the URL with `curl` or the browser.
   - For UI work, use a browser or screenshot check when feasible.
   - If login or seeded data is needed, state the exact blocker or next credential/data step.
8. Report the result in a compact handoff:
   - Local URL.
   - Repo path, branch, dirty state summary.
   - Commands and ports started.
   - Effective API/backend targets.
   - What was verified.
   - What is not covered by local testing.

## Multi-Repo Rules

- Start narrow, then widen only when the app needs it.
- Keep local, dev, and production claims separate.
- Never mutate shared databases, run migrations, seed production, deploy, push, or merge unless the user explicitly asks.
- If local frontend changes require backend changes that are not present locally, say so before presenting the URL as feature-complete.
- If multiple local repos must be active, list every repo path, branch, command, port, and health check.

## Common Checks

- JavaScript/Next/Vite: inspect `package.json` scripts, `next.config.*`, `vite.config.*`, `.env*`, and app proxy routes.
- Node APIs: inspect `package.json`, `.env*`, `src/server*`, route files, Docker compose, and health endpoints.
- Python APIs/workers: inspect `pyproject.toml`, `requirements*.txt`, `Makefile`, `.env*`, app entrypoints, and job scripts.
- Dockerized stacks: inspect `docker-compose*.yml`, named volumes, port mappings, and service health checks before starting containers.

## Closing Shape

```markdown
Local app is running at: http://localhost:<port>

Running from:
- Repo:
- Branch:
- Dirty changes included:

Started:
- <command> on <port>

Runtime targets:
- API/backend:
- Other services:

Verified:
- ...

Not covered:
- ...
```

