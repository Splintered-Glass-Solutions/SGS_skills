---
name: rti-time-tracking
description: Use when Preston asks to log, track, add, or report ClickUp time for RTI work, especially Fabric, analytics, reporting, data modeling, or general RTI support that should go to the RTI list.
---

# RTI Time Tracking

Use this skill to add ClickUp time entries for RTI work without rediscovering the RTI ClickUp destination every time.

## Default Destination

When Preston says "track time to RTI", "RTI list", "RTI time", or similar and does not name a more specific RTI task, use:

- Task: `RTI - General`
- Task ID: `1p2b12g`
- URL: `https://app.clickup.com/t/1p2b12g`
- Hierarchy observed: `RTI > RTI`

Use this by default for Fabric sandbox work, Fabric AI enablement, data audits, workspace capability testing, general reporting analysis, and other broad RTI support.

Known RTI alternatives, only when the user's wording clearly maps to them:

- `RTI - Communications`: task ID `1mu6j2j`
- `RTI - Infastructure`: task ID `2454kju`
- `RTI - Project Managment`: task ID `2d4nfx8`
- `RTI - Modeling`: task ID `2454kjh`

Do not use RTI-related tasks found under unrelated lists such as `SGS > EmailTriage` unless Preston explicitly asks for that exact task.

## Workflow

1. If the user names an exact task or area, resolve it with ClickUp search first.
2. If the user says only RTI or RTI list, use `RTI - General` (`1p2b12g`).
3. Add a manual time entry with `_clickup_add_time_entry`; do not start a running timer unless Preston explicitly asks to start tracking now.
4. Use America/Chicago local time for `start` and `end_time` values.
5. If the current thread provides enough context, estimate the duration pragmatically and report the assumption. If the duration is genuinely unclear, ask one concise question before logging time.
6. Keep the description short and useful, for example: `Fabric sandbox workspace data and capability audit via Codex`.
7. Do not include `tags` unless there is a tested reason. The ClickUp connector has rejected simple string tags with `Name value is required`.
8. Omit `billable` unless Preston explicitly says billable or non-billable. Report the billable value returned by ClickUp.

## Time Entry Pattern

Use:

```json
{
  "task_id": "1p2b12g",
  "start": "YYYY-MM-DD HH:MM",
  "duration": "Xh Ym",
  "description": "Short RTI work description"
}
```

For work just completed in the current thread, choose a start time and duration that matches the observed work window. Prefer a reasonable rounded duration over excessive precision.

## Final Response

After adding time, report:

- Task name and URL
- Duration
- Start/end time in Central time
- Description
- Billable status

Mention any retry only if it affected the final entry, such as removing tags after the connector rejected them.
