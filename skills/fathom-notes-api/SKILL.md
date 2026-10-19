---
name: fathom-notes-api
description: Use when accessing the user's Fathom meeting notes, summaries, action items, transcripts, or Fathom-recorded meeting archives; especially when the ChatGPT/Fathom connector is connected in the UI but no callable Fathom tool is exposed. Covers Fathom API key loading, meeting listing, transcript fetching, speaker-attributed quote capture, Fathom Actions recovery, and safe handling of Fathom secrets.
metadata:
  short-description: Access Fathom notes via API
---

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

1. Use the user-provided date and timezone context, or verify the local clock when the task has a time window.
2. Convert window boundaries in the user-selected timezone to UTC for Fathom filters:
   - `created_after=...Z`
   - `created_before=...Z`
3. Probe identity if needed:
   - Try `GET /team_members` and `GET /teams`.
   - These may return empty for the user's key. If so, resolve the authorized recording owner from the request or configuration.
4. List the user-recorded meetings:
   - `GET /meetings?include_summary=true&include_action_items=true&created_after=...&created_before=...&recorded_by[]=owner@example.com`
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

## Speaker attribution

Verify the intended person using meeting participants and transcript speaker turns. Distinguish people with similar names before attributing a quote.

## Helper Script

Use `scripts/fathom_api.mjs` for repeatable listing/fetching:

```sh
node <agent-config>/skills/fathom-notes-api/scripts/fathom_api.mjs meetings \
  --start 2026-06-02T05:00:00Z \
  --end 2026-06-08T20:31:52Z \
  --recorded-by owner@example.com \
  --out /tmp/fathom/meetings.json
```

```sh
node <agent-config>/skills/fathom-notes-api/scripts/fathom_api.mjs transcripts \
  --ids <recording-id-1>,<recording-id-2> \
  --out-dir /tmp/fathom
```

The script loads `<agent-config>/secrets/fathom.env` automatically if `FATHOM_API_KEY` is not already set.
