---
name: close-thread
description: >-
  Close the current Codex thread by renaming it with a leading fullwidth dash
  marker only. Use when the user asks to close out, mark closed, or run the
  close-thread slash command for the current thread.
---

# Close Thread

## Overview

Use this skill to mark the current Codex thread as closed without archiving,
pinning, moving, sending follow-ups, creating tasks, or changing repo state.
The only thread mutation is renaming the current thread so its existing title
is prefixed with the fullwidth dash marker `－`.

## Required Behavior

1. Resolve the current Codex thread and its current title.
   - Use the Codex thread tools exposed in the current session.
   - If thread tools are not available yet, use `tool_search` for
     `list_threads`, `read_thread`, and `set_thread_title`.
   - Prefer an explicit current-thread identifier if the runtime exposes one.
   - If there is no explicit current-thread identifier, use `list_threads` and
     `read_thread` to identify the currently active thread from the latest
     turns and recency.
   - If the current thread cannot be identified with high confidence, stop and
     say the closeout is blocked because renaming the wrong thread would be
     unsafe.
2. Compute the closed title.
   - Preserve the existing title exactly.
   - If the title already starts with `－`, leave it unchanged.
   - Otherwise set the new title to `－` followed immediately by the current
     title, with no added space.
3. Rename the thread with `set_thread_title`.
   - Do not call `set_thread_archived`.
   - Do not archive, pin, unpin, hand off, fork, create a new thread, delete,
     move, deploy, push, commit, send external messages, or perform any other
     side effect.
   - Do not alter files, repo state, automations, reminders, or external
     systems as part of closing a thread.
4. After the rename succeeds, send one concise final response.
   - State that the thread is closed out now.
   - Include a brief high-level synopsis of what was done in this thread.
   - Include any outstanding items or caveats only if they are visible in the
     current conversation or thread summary.
   - Keep the closeout human-readable and short. Avoid tables unless the thread
     had many distinct workstreams.

## Summary Guidance

The closeout summary should capture outcomes, not every command. Include:

- the main work completed;
- delivery or validation status when relevant;
- unpushed local work, blockers, or follow-ups if any remain;
- a final sentence that the thread has been marked closed.

Do not invent missing history. If earlier context is unavailable, say the
summary is based on the visible thread context.

## Safety Rules

- This command is a title marker only. It is not an archive command.
- The fullwidth dash marker must be exactly `－`, not a hyphen-minus `-`, en
  dash, or em dash.
- Never double-prefix a title that already begins with `－`.
- If `set_thread_title` fails, do not claim the thread is closed.
- The final response is the last step after the rename attempt.
