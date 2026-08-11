# Handoff Agent Playbook

This is a platform-neutral version of the `handoff` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Create a concise handoff document and a copyable message that compact the current conversation and working state so another agent or future session can continue. Use when the user asks for a handoff, session summary, continuation note, compacted context, transfer document, next-agent brief, or a saved recap of current progress across any project.

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

# Handoff

## Overview

Write a handoff document summarizing the current session so a fresh agent can continue the work. Save it in the temporary directory of the user's operating system, not in the current workspace.

If the user provides extra arguments or a stated focus, treat that as the intended purpose of the next session and tailor the handoff around it.

## Handoff Modes

Classify the request before acting:

1. **Document-only handoff** — the user asks for a handoff, recap for later,
   continuation note, or copyable prompt but does not explicitly ask to create
   or start a new thread.
   - Create the Markdown handoff and return its path plus the copyable message.
   - Do **not** create a agent thread.
2. **New-thread handoff** — the user explicitly asks to create, start, open, or
   hand off to a new thread/task.
   - Create the Markdown handoff first.
   - Then create the new thread in the **same the agent project** as the current
     thread.
   - Use the **same model and reasoning/thinking settings** as the current
     thread.
   - Never substitute a projectless thread, a different saved project, or the
     user's default model settings merely because they are convenient.

If the current project ID or current model/reasoning settings cannot be
resolved from the the agent app context or thread metadata, do not guess. Still
create the Markdown handoff, explain exactly which setting could not be
resolved, and ask for the missing direction before creating the new thread.

## Workflow

1. Determine the OS temp directory:
   - macOS/Linux: use `${TMPDIR:-/tmp}`.
   - Windows: use `%TEMP%` or `%TMP%`.
2. Create a Markdown file in that temp directory, using a clear name such as `handoff-YYYYMMDD-HHMMSS.md`.
3. Summarize only the information needed to continue the work. Do not duplicate content already captured in durable artifacts such as PRDs, plans, ADRs, issues, commits, diffs, logs, or generated reports; reference those by path, command, URL, branch, commit, or issue ID instead.
4. Redact sensitive information, including API keys, tokens, passwords, secrets, personal identifying details, private customer data, and credential-like environment variables. Preserve enough context to explain what kind of secret was present, for example `[REDACTED_API_KEY]`.
5. Include a `Suggested Skills` section naming skills that the next agent should invoke, with a one-line reason for each. If no specific skill is relevant, write `None identified`.
6. After writing the file, respond with the absolute path, a short note about what it is tailored for, and a full copyable handoff message the user can send to the new thread.
7. The copyable message must include all context the new thread needs to begin: the purpose, current state, key constraints, artifact path, completed work, remaining work, verification status, risks, and suggested skills. It should point to the saved Markdown handoff rather than duplicating every detail from it.
8. For a new-thread handoff:
   - Resolve the current thread's `projectId`, model, and reasoning/thinking
     effort before calling thread-creation tools.
   - Call `list_projects` and verify the resolved project still exists.
   - Use `create_thread` with `target.type = "project"` and that exact
     `projectId`.
   - Pass the current model and reasoning/thinking effort explicitly when the
     tool supports them.
   - Follow the project's normal environment rule: use a worktree for a Git
     project unless the user explicitly requests the saved project directly;
     use local for a non-Git project.
   - Do not create a second thread if creation returns an in-progress client
     thread ID. Wait for or inspect that task instead.
   - Confirm the created task is ready or active before reporting success.
   - Include the appropriate created-thread directive in the final response.

## Document Shape

Use this structure unless the user asks for a different format:

```markdown
# Handoff

## Purpose
What the next session is meant to accomplish.

## Current State
What is known, what changed, and where the work stands.

## Important Context
Key constraints, decisions, assumptions, user preferences, and project-specific guardrails.

## Artifacts and References
Paths, URLs, branches, commits, issues, commands, logs, or generated outputs the next agent should inspect instead of repeating here.

## Work Completed
Concrete actions already taken in this session.

## Remaining Work
Specific next steps, ordered by priority when possible.

## Verification
Tests, checks, evidence gathered, and known gaps.

## Risks and Watchouts
Known failure modes, unresolved questions, blocked items, or actions to avoid.

## Suggested Skills
Skills the next agent should use and why.
```

## Quality Bar

- Make the document useful to an agent without the conversation history.
- Keep it compact: prefer bullets, concrete file paths, exact commands, and unresolved questions over narrative.
- Distinguish completed work from planned or suggested work.
- Distinguish verified facts from assumptions or stale context.
- Do not claim deploys, merges, sends, tests, or production effects happened unless they actually did.
- Avoid including raw secrets, long pasted logs, private messages, or irrelevant conversation.

## Final Response Shape

For a document-only handoff, return the saved path first, then include a fenced
code block labeled as the copyable message for the next thread. Do not create a
thread or emit a created-thread directive.

The copyable message should be self-contained enough that the receiving thread can act without reading this conversation, but should still reference the saved handoff path for the complete details.

Use this shape:

````markdown
Saved handoff: /absolute/path/to/handoff-YYYYMMDD-HHMMSS.md

Copyable message for the new thread:

```text
Please continue from this handoff:
/absolute/path/to/handoff-YYYYMMDD-HHMMSS.md

Purpose:
[one or two sentences]

Current state:
[concise bullets]

Important constraints:
[concise bullets]

Remaining work:
[ordered next steps]

Verification and risks:
[checks run, gaps, watchouts]

Suggested skills:
[skill names and reasons, or None identified]
```
````

For a new-thread handoff, use the same response shape and additionally report
that the task was created in the same project with the same model/reasoning
settings. Emit the created-thread directive only after creation succeeds.
