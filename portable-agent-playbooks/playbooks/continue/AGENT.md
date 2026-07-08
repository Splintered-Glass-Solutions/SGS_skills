# Continue Agent Playbook

This is a platform-neutral version of the `continue` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Resume interrupted agent work after a limit, pause, network cutout, app reload, context compaction, or stalled thread. Use when the user invokes /continue, says continue, resume, pick back up, keep going, do not restart, or asks the agent to continue the exact work already underway without losing context.

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

# Continue

## Purpose

Use this skill to resume the same work that was already in progress. The goal is
continuity: rebuild the last known objective, identify what changed or was
already proven, and carry the work forward without starting over or asking
the user to restate context when it can be recovered locally.

This skill is not a license for open-ended autonomous work. Resume the active
objective, not a new adjacent idea.

## Recovery Contract

Start with a compact recovery pass before taking action:

1. Identify the latest user instruction and treat it as authoritative.
2. Reconstruct the active objective from the conversation, any active plan,
   tool output, terminal output, current working directory, changed files, and
   durable artifacts.
3. Separate confirmed facts from inferred state.
4. Detect the task type: quick lookup/message, debugging, build work, planning,
   research/transcript, QA/review, automation, or communication.
5. Resume at the next unfinished step using the matching task rule.

Do not restart the whole task unless the previous state is unavailable or
clearly invalid. Do not claim prior work was verified unless there is visible
evidence in the thread, filesystem, terminal, git state, logs, test output, or a
durable artifact.

## Preflight

Inspect only what is needed to recover momentum:

- current conversation and latest user message
- active plan/checklist status, if present
- current `cwd`, repo root, branch, and `git status --short --branch` when in a
  repo
- relevant changed files and recent diffs
- current terminal output if a command or dev server may still be running
- local instructions such as `AGENTS.md`
- durable artifacts named by the thread: notes, plans, checkpoints, logs,
  screenshots, generated files, test reports, queue/checkpoint files, or memory
  files

If a command/session may still be running, inspect it before starting duplicate
work. If a server is already running and useful, reuse it.

## Resume Decision

After preflight, state the recovered state in one or two sentences:

```md
Continuing: <objective>. Last confirmed state: <evidence>. Next step: <action>.
```

Then continue according to the task type:

- `quick lookup/message`: finish the requested answer or message in one short
  pass.
- `debugging`: state the current hypothesis before editing, then validate the
  fix or report why validation is blocked.
- `build work`: make one coherent implementation pass, then run the relevant
  tests, screenshot checks, browser checks, typecheck, build, or syntax check.
- `planning`: stop when the spec or decision brief is complete; do not drift
  into implementation unless the user asked for it.
- `research/transcript`: preserve durable notes, citations, source IDs, or
  extracted evidence before closing.
- `QA/review`: lead with findings and evidence references.
- `automation`: include create/no-create accounting, checkpoint handling, and
  next-run memory when the workflow supports it.
- `communication`: produce concise recipient-fit text or send only if the user
  clearly asked to send.

## Safety Gates

Continue autonomously only when the next step is recoverable, bounded, and
within the current thread's approvals.

Stop and ask for the smallest missing input when continuation would require:

- production deploys, promotions, rollbacks, broad live jobs, or paid provider
  runs without explicit current-thread approval
- database grants, ownership, roles, RLS, destructive data changes, or
  permission changes without exact approval
- sending customer/client/team messages unless the user explicitly asked to send
- overwriting unrelated dirty work, force-pushing, rebasing shared work, or
  merging protected branches without approval
- product, billing, auth, privacy, compliance, or data-retention choices that
  cannot be inferred safely
- secrets exposure or copying secrets into logs/messages

If the user already gave approval in the current thread, preserve the exact
scope: target repo, branch, environment, account, recipient, and action.

## When State Is Ambiguous

If the prior work cannot be recovered confidently:

1. Do a lightweight local evidence pass.
2. State what is known, what is inferred, and what is missing.
3. Choose the safest useful next step if one exists.
4. Ask one concise question only when no safe continuation is possible.

Use this no-op shape when blocked:

```md
I cannot safely continue yet.

Known: <evidence>.
Missing: <specific context or approval>.
Smallest input needed: <question or approval>.
```

## Checkpointing

For long, cross-repo, high-cost, or uncertain resumptions, checkpoint before a
second major pass:

1. Objective
2. What changed or was found
3. Proof gathered
4. Remaining uncertainty
5. Recommended next action

If the work should survive another pause, save or update the durable artifact
that the workflow already uses, such as a plan file, QA report, run log,
checkpoint file, memory note, or generated handoff. Do not create new memory
entries unless the user explicitly asks for memory updates.

## Final Shape

Keep the final answer short and continuity-focused:

- what was resumed
- what changed or was completed
- what was verified
- files/artifacts changed
- remaining blocker or next action, if any

If relying on recovered or inferred state, say so plainly.

