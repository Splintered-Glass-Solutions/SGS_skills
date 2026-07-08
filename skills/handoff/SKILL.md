---
name: handoff
description: Create a concise handoff document and a copyable message that compact the current conversation and working state so another agent or future session can continue. Use when the user asks for a handoff, session summary, continuation note, compacted context, transfer document, next-agent brief, or a saved recap of current progress across any project.
---

# Handoff

## Overview

Write a handoff document summarizing the current session so a fresh agent can continue the work. Save it in the temporary directory of the user's operating system, not in the current workspace.

If the user provides extra arguments or a stated focus, treat that as the intended purpose of the next session and tailor the handoff around it.

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

Return the saved path first, then include a fenced code block labeled as the copyable message for the next thread.

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
