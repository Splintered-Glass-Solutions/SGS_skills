# Local Time Tracking Agent Playbook

This is a platform-neutral version of the `local-time-tracking` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Log, append, report, or backfill work time in a local per-project JSONL ledger. Use when the user requests local time tracking or a time report. New entries are local-only; ClickUp is historical source data only.

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

# Local Time Tracking

## Storage

Keep one append-only ledger at the client project root:

`<project-root>/.codex/time_tracking.jsonl`

The ledger is intentionally not Git tracked. Add the exact path to that
checkout's `.git/info/exclude`; do not change the committed `.gitignore` just
to hide a personal work log. Never put credentials, tokens, or secrets in the
ledger.

Each line is one JSON object with this shape:

```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "minutes": 90,
  "description": "Short, work-specific description",
  "project": "sample-project",
  "timezone": "Etc/UTC",
  "source": "manual",
  "source_id": null,
  "source_duration_ms": null,
  "task": null,
  "task_id": null,
  "billable": null
}
```

`date`, `time`, `minutes`, and `description` are required. Use the append
helper at `scripts/log_time.py` when available. It creates the directory,
preserves JSONL formatting, adds the local Git exclude, and skips an entry
when its non-empty `source_id` is already present.

## Project roots

Use the user-approved canonical client root. Related repositories for one client share one ledger. Keep root mappings in private project configuration rather than this public skill. Resolve missing or ambiguous roots before writing.

## Workflow

1. Identify the project and its canonical root.
2. Determine the local date, start time, and duration in minutes. Use
   the user/project timezone; use UTC only as an explicit fallback. Pass the
   resolved timezone to the helper with `--timezone`.
3. Write a concise description that names the actual work.
4. Append one JSON object with `source: "manual"`, or use `source: "clickup"`
   and the ClickUp entry ID only for a historical backfill.
5. For reports, sum `minutes` from the selected ledger and return hours plus
   the exact date range. Do not infer billability when it is null.

Do not start, stop, or add new time to ClickUp. If historical ClickUp data is
needed, fetch it read-only, preserve its entry IDs, and import it once into the
matching local ledger.

## Quick append

```bash
python3 <agent-config>/skills/local-time-tracking/scripts/log_time.py \
  --project-root <project-root> \
  --date 2026-08-13 --time 14:30 --minutes 45 \
  --description "Release validation and QA evidence" \
  --project sample-project
```

The command is safe to repeat when `--source-id` is supplied for imported
ClickUp entries. For manual entries without a source ID, only append once.

## Final response

Report the project, ledger path, date/time, duration, description, and whether
the entry was appended or skipped as a duplicate. For reports, include the
count and total minutes/hours. Mention any unresolved project mapping.
