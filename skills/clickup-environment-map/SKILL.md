---
name: clickup-environment-map
description: Use when working with Preston's ClickUp environments, finding ClickUp workspaces/spaces/folders/lists/shared hierarchy, or reading/writing ClickUp tasks, comments, channels, messages, and replies across SGS Consulting, And Studio, SGS_x_S.IS, or Matt's Workspace.
---

# ClickUp Environment Map

Use this skill before ClickUp work where the destination or source could live in Preston's SGS workspace, Eric/And Studio, SGS_x_S.IS, Matt's Workspace, a private shared folder/list, or ClickUp Chat. Pair it with the general `clickup` skill for task creation/update conventions.

## Critical Lookup Rule

Do not rely only on `GET /api/v2/team/{workspace_id}/space`.

For And Studio and similar shared/private ClickUp surfaces, also call:

```text
GET /api/v2/team/{workspace_id}/shared
```

That shared hierarchy endpoint is how shared private folders/lists such as `PD - Bonfire` appear. This is the likely reason prior runs struggled to find some ClickUp spaces.

## Token

Use the existing personal token from one of these files; do not print it:

- `/Users/preston/Code/sgs_admin/src/sync/load/.env`
- `/Users/preston/Code/sgs_admin/src/sync/timeentry/.env`

Variable: `CLICKUP_PK_TOKEN`. Both files were verified to contain the same token on 2026-06-05.

## Verified Workspaces

Read `references/clickup-map.md` for the current verified hierarchy and channel map. Refresh live data before high-stakes writes or if the user asks for "current", "all", "latest", or a missing destination:

```bash
python3 /Users/preston/.codex/skills/clickup-environment-map/scripts/refresh_clickup_map.py
```

As of 2026-06-05, the token authenticated as Preston Pope and reached:

- `SGS Consulting` (`10508245`)
- `And Studio` (`10643222`)
- `Matt's Workspace` (`9014349693`)
- `SGS_x_S.IS` (`90132433396`)

## API Patterns

Use `Authorization: $CLICKUP_PK_TOKEN` and `Content-Type: application/json`.

Hierarchy:

```text
GET /api/v2/team
GET /api/v2/team/{workspace_id}/space?archived=false
GET /api/v2/space/{space_id}/folder?archived=false
GET /api/v2/space/{space_id}/list?archived=false
GET /api/v2/folder/{folder_id}/list?archived=false
GET /api/v2/team/{workspace_id}/shared
```

Tasks:

```text
GET  /api/v2/list/{list_id}/task
POST /api/v2/list/{list_id}/task
GET  /api/v2/task/{task_id}
PUT  /api/v2/task/{task_id}
```

Task and list comments:

```text
GET  /api/v2/task/{task_id}/comment
POST /api/v2/task/{task_id}/comment
GET  /api/v2/list/{list_id}/comment
POST /api/v2/list/{list_id}/comment
GET  /api/v2/comment/{comment_id}/reply
POST /api/v2/comment/{comment_id}/reply
```

ClickUp Chat channels, messages, and message replies:

```text
GET  /api/v3/workspaces/{workspace_id}/chat/channels?limit=100
POST /api/v3/workspaces/{workspace_id}/chat/channels
POST /api/v3/workspaces/{workspace_id}/chat/channels/location
GET  /api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages
POST /api/v3/workspaces/{workspace_id}/chat/channels/{channel_id}/messages
GET  /api/v3/workspaces/{workspace_id}/chat/messages/{message_id}/replies
POST /api/v3/workspaces/{workspace_id}/chat/messages/{message_id}/replies
```

ClickUp documents say Chat API endpoints are experimental and may change. Verify docs or run the refresh script if chat calls fail.

## Communication Surfaces

Distinguish these surfaces:

- Task comments: attached to a task; support threaded replies through `/comment/{comment_id}/reply`.
- List comments: attached to a list; also support threaded replies.
- Chat channels: workspace, space, folder, list, ad hoc, DM, or group-DM chat rooms; top-level messages and message replies use v3 endpoints.
- Chat views/comments: legacy/conversation-style view comments use v2 view comment endpoints if encountered.

For private DMs/group DMs, prefer listing counts and IDs only unless the user explicitly asks to read or write those conversations.

## Write Discipline

Before creating or posting:

1. Resolve the exact workspace and destination list/channel ID.
2. If And Studio is involved, check both normal spaces and `shared`.
3. Confirm whether the user wants a task, task comment, list comment, channel message, or reply.
4. For task creation, follow the general `clickup` skill: preserve title, status, priority, due date, assignees, tags, evidence, and links.
5. Return the created/updated URL or ID plus the workspace/list/channel used.
