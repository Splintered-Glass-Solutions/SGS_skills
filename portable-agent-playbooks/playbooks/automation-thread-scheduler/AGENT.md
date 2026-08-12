# Automation Thread Scheduler Agent Playbook

This is a platform-neutral version of the `automation-thread-scheduler` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Create or repair the agent automations and scheduled monitors with thread hygiene: prefer same-thread heartbeat automations, prevent recurring cron thread spam, add an emoji-prefixed automation thread title, remove or pause duplicate standalone schedules, and preserve automation memory/checkpoints. Use when the user asks to create, schedule, update, repair, convert, or clean up a the agent automation, monitor, reminder, recurring run, heartbeat, or scheduled skill.

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

# Automation Thread Scheduler

Use this skill whenever creating or maintaining a the agent automation or scheduled
monitor. The default is a visible, same-thread automation that does not create a
new agent thread every run.

## Core Policy

- Prefer `kind: heartbeat` with `destination: thread` for recurring follow-ups,
  monitors, reminders, and scheduled skill runs.
- Do not create a recurring standalone `cron` automation unless the user
  explicitly asks for a separate standalone job, worktree, or project-scoped
  background run.
- Every active same-thread automation must have a target thread title that
  starts with a distinguishing emoji.
- The automation prompt must explicitly say to continue the existing the agent
  thread and not create, fork, hand off, or open new threads.
- Preserve durable memory and checkpoints for every automation that has a
  memory path.
- Search for duplicate or legacy schedules before creating a new one. Pause or
  delete duplicate standalone cron automations when they would spam extra
  threads.

## Required Tooling

Before changing automations, search for and use the `automation_update` tool.
Do not edit `automation.toml` directly as the primary update path when the app
tool is available.

For thread titles, search for and use `set_thread_title`. If the automation
already has a `target_thread_id`, rename that exact thread. If a new heartbeat
is created and the tool returns or writes a target thread id, rename it after
creation.

## Preflight

1. Classify the work as `automation`.
2. Resolve the automation intent:
   - task name and objective;
   - cadence and timezone;
   - whether the user explicitly wants a separate standalone job;
   - target thread, current thread, or existing automation id;
   - memory path and any source-specific checkpoint files.
3. Inspect existing automation configs under
   `$CODEX_HOME/automations/*/automation.toml`.
4. If `$CODEX_HOME` is empty, use `$CODEX_HOME` directly.
5. Find candidate duplicates by:
   - matching `id`;
   - matching `name`;
   - matching prompt objective;
   - matching memory path;
   - matching cadence and cwd/project.
6. Read existing automation memory before changing behavior when a memory file
   exists.

## Creation Rules

When creating a scheduled automation and the user has not explicitly requested
standalone cron behavior:

- Use `automation_update` with:
  - `kind: heartbeat`;
  - `destination: thread`;
  - `status: ACTIVE` unless the user asks to stage or pause it;
  - a user-readable cadence in the `rrule`;
  - `targetThreadId` when continuing a known thread.
- Put the run instructions, memory path, safety boundaries, and checkpoint
  writeback requirements in the prompt.
- Include this thread rule in the prompt:

```text
Thread visibility:
- Continue this existing agent thread for every run.
- Do not create, fork, hand off, or open a new agent thread for this monitor.
- Use the final ::inbox-item{...} as the compact user-visible status surface.
```

- Rename the target thread with an emoji prefix immediately after creation or
  conversion.
- Pick an emoji that fits the automation domain:
  - `📡` communications, monitoring, inbox, Slack, email, Teams, Skool;
  - `🧪` QA/testing;
  - `🛠️` build/maintenance;
  - `📊` reports, analytics, dashboards;
  - `🗂️` portfolio/project management;
  - `⏱️` time tracking or periodic rollups.
- If the domain is unclear, use `🤖`.

## Conversion Rules

When an existing recurring automation is opening a new thread each run:

1. View the automation with `automation_update`.
2. Read its local `automation.toml` to confirm `kind`, `status`, `rrule`, and
   current target.
3. Convert the canonical automation to:
   - `kind: heartbeat`;
   - `destination: thread`;
   - same name, prompt intent, cadence, and active/paused status;
   - same memory path and safety rules.
4. Add or update the prompt's `Thread visibility` section.
5. Rename the target thread with a leading emoji.
6. Search for duplicate active cron automations with the same name or prompt.
7. Pause duplicates when the app can update them cleanly. Delete duplicates only
   when they are clearly redundant and would continue creating extra threads.
8. Record the conversion in the automation memory.

## Cron Exceptions

Use `kind: cron` only when one of these is true:

- the user explicitly asks for a new separate thread/job/worktree.
- The automation must run in a project/worktree environment that is not tied to
  an existing conversation.
- The run is expected to produce a standalone artifact without conversational
  continuity.
- The automation should be isolated for safety, credentials, or repo state.

When using cron, still prevent spam:

- make the standalone behavior explicit in the final answer;
- include an expiry, archive instruction, or compact inbox-only status when
  appropriate;
- record why cron was chosen in memory or the final response.

## Memory Updates

When the automation has a memory path, append a concise configuration note after
creation, conversion, duplicate cleanup, or title changes:

```markdown
## Automation Configuration Notes

- <UTC time> / <local time>: Created/converted automation `<id>` as a
  same-thread heartbeat targeting thread `<thread_id>`. Thread title set to
  `<emoji title>`. Duplicate standalone schedules checked: <result>. Cadence,
  prompt intent, active status, and memory/checkpoint behavior preserved.
```

Do not overwrite operational checkpoint sections unless the task requires it.

## Verification

Before final response, verify:

- exactly which automation id changed;
- the active canonical automation is `kind = "heartbeat"` unless cron was
  explicitly requested;
- the automation has a `target_thread_id` or the app confirmed a thread target;
- the target thread title starts with an emoji;
- duplicate standalone crons were handled or explicitly reported;
- memory was updated when supported.

Useful local check:

```bash
find $CODEX_HOME/automations -maxdepth 2 -name automation.toml \
  -print -exec rg -n "^(id|kind|name|status|rrule|target_thread_id|target) =" {} \;
```

## Final Response

Return compact accounting:

- automation id and name;
- same-thread heartbeat or cron exception;
- emoji thread title;
- duplicate cron cleanup result;
- memory path updated;
- anything still blocked or requiring user choice.

Always end scheduled-automation maintenance with an inbox item directive.
