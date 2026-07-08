# Fathom Notes Api Agent Playbook

This is a platform-neutral version of the `fathom-notes-api` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when accessing the user's Fathom meeting notes, summaries, action items, transcripts, or Fathom-recorded meeting archives; especially when the ChatGPT/Fathom connector is connected in the UI but no callable Fathom tool is exposed. Covers Fathom API key loading, meeting listing, transcript fetching, Eric-isms capture, Fathom Actions recovery, and safe handling of Fathom secrets.

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

# Fathom Notes API

Use the Fathom REST API directly when Fathom connector tools are absent or unreliable. Do not stop at "Fathom tool unavailable" until checking the API key path.

## Credential Rules

- Prefer `FATHOM_API_KEY` from the shell environment.
- If missing, source `<agent-config>/secrets/fathom.env` if it exists.
- Never print, echo, log, or paste the API key.
- Do not use `FATHOM_WEBHOOK_SECRET` for reads. It is only for webhook verification.
- If a webhook secret or API key is pasted into chat or output, tell the user to rotate it if the thread is not private.

## API Basics

Fathom API base URL:

```text
https://api.fathom.ai/external/v1
```

All read calls use:

```text
X-Api-Key: $FATHOM_API_KEY
```

Core endpoints:

- `GET /meetings`
- `GET /recordings/{recording_id}/transcript`
- `GET /recordings/{recording_id}/summary`
- `GET /team_members`
- `GET /teams`

When listing meetings, include at least one content flag. For meeting-note recovery, default to:

```text
include_summary=true
include_action_items=true
```

Use `include_transcript=true` only for small, targeted pulls. For broader scans, list meetings first, then fetch transcripts by recording ID in batches.

## Standard Workflow

1. Use the live local shell clock as date authority when the task has a time window.
2. Convert local America/Chicago window boundaries to UTC for Fathom filters:
   - `created_after=...Z`
   - `created_before=...Z`
3. Probe identity if needed:
   - Try `GET /team_members` and `GET /teams`.
   - These may return empty for the user's key. If so, infer the user from successful `recorded_by[]=the user@splinteredglass.solutions` results.
4. List the user-recorded meetings:
   - `GET /meetings?include_summary=true&include_action_items=true&created_after=...&created_before=...&recorded_by[]=the user@splinteredglass.solutions`
5. Also list accessible meetings in the same window without `recorded_by[]`.
6. De-duplicate by `recording_id`.
7. Identify relevant meetings using multiple signals:
   - invitee names/emails
   - `recorded_by`
   - action-item assignees
   - summaries
   - transcript speaker turns
8. Fetch transcripts only for likely relevant meetings, no more than 3 concurrent transcript requests at a time.
9. Store raw API outputs in `/tmp/<task-slug>/` by default. Do not write raw transcripts into the repo unless explicitly needed.
10. For archive work, preserve source metadata:
   - meeting title
   - meeting date
   - `recording_id`
   - source URL with `?timestamp=<seconds>`
   - transcript speaker
   - context
   - confidence

## Eric-Isms Specific Notes

- Do not rely only on a Fathom person search or connector speaker index; previous runs missed Eric that way.
- Treat `Eric Kidwell` and known Eric emails as Kidwell signals, but verify transcript speaker turns before capturing quotes.
- Distinguish non-Kidwell Eric meetings, such as `Eric Manheimer`, by fetching transcript when necessary and documenting the exclusion.
- Capture only memorable Eric phrases. Skip generic action items, status updates, and other speakers' lines unless Eric explicitly attributes the saying.

## Helper Script

Use `scripts/fathom_api.mjs` for repeatable listing/fetching:

```sh
node <agent-config>/skills/fathom-notes-api/scripts/fathom_api.mjs meetings \
  --start 2026-06-02T05:00:00Z \
  --end 2026-06-08T20:31:52Z \
  --recorded-by the user@splinteredglass.solutions \
  --out /tmp/fathom/meetings.json
```

```sh
node <agent-config>/skills/fathom-notes-api/scripts/fathom_api.mjs transcripts \
  --ids 152238927,152444689,153196836 \
  --out-dir /tmp/fathom
```

The script loads `<agent-config>/secrets/fathom.env` automatically if `FATHOM_API_KEY` is not already set.

