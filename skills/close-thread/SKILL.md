---
name: close-thread
description: >-
  Close the current Codex thread by unpinning it when needed and renaming it
  with a leading fullwidth dash marker. Preserve the reserved `🗄️` marker
  when closing a sidelined feature task. Use when the user asks to close out,
  mark closed, or run the close-thread slash command for the current thread.
---

# Close Thread

## Overview

Use this skill to mark the current Codex thread as closed without archiving,
moving, sending follow-ups, creating tasks, or changing repo state. If the
thread is pinned, unpin it, then rename the current thread with exactly one
leading fullwidth dash marker `－`. When the title begins with the reserved
`🗄️` sidelined marker, preserve that marker immediately before the dash. Remove
the priority star and all other emoji characters from the closed title.

## Required Behavior

1. Resolve the current Codex thread and its current title.
   - Use the Codex thread tools exposed in the current session.
   - If thread tools are not available yet, use `tool_search` for
     `list_threads`, `read_thread`, `set_thread_title`, and
     `set_thread_pinned`.
   - Prefer an explicit current-thread identifier if the runtime exposes one.
   - If there is no explicit current-thread identifier, use `list_threads` and
     `read_thread` to identify the currently active thread from the latest
     turns and recency.
   - If the current thread cannot be identified with high confidence, stop and
     say the closeout is blocked because renaming the wrong thread would be
     unsafe.
   - Determine whether the resolved thread is pinned from the thread listing or
     other thread metadata. Do not inspect or mutate any other thread.
2. Compute the closed title.
   - Start from the existing title. Detect and temporarily remove a leading
     `🗄️` marker plus surrounding separator whitespace, and remove any existing
     leading `－` marker before rebuilding the closed title.
   - Remove the priority markers `★`, `⭐`, and `*`, plus every other emoji
     character from the title. Use Unicode-aware emoji filtering, including
     variation selectors, emoji modifiers, zero-width joiners, and related
     presentation characters, so compound emoji are removed cleanly.
   - Preserve all remaining non-emoji title text. Trim whitespace left by the
     removed markers and collapse only the resulting leading/trailing or
     duplicate separator whitespace.
   - Set the closed title to `🗄️－` followed immediately by the normalized
     remaining title when the sidelined marker was present; otherwise use
     `－` followed immediately by the title. Do not add a space after the dash.
   - Examples: `★ 📊 Morning Brief` becomes `－Morning Brief`; `－⭐ Task` becomes
     `－Task`; `🗄️ Sidelined Feature` becomes `🗄️－Sidelined Feature`.
3. Close the thread state.
   - If the resolved thread is pinned, call `set_thread_pinned` with
     `pinned=false` for that thread only.
   - Rename the thread with `set_thread_title`.
   - If unpinning fails, do not claim the thread is fully closed; report that
     the title closeout may have succeeded but the thread remains pinned.
   - Do not call `set_thread_archived`.
   - Do not archive, pin, hand off, fork, create a new thread, delete, move,
     deploy, push, commit, send external messages, or perform any other side
     effect. Unpinning the resolved current thread is the one intended
     additional mutation.
   - Do not alter files, repo state, automations, reminders, or external
     systems as part of closing a thread.
4. After the required title and pin-state updates succeed, send one concise
   final response.
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

- This command normalizes the title to one fullwidth dash plus non-emoji text,
  preserving only the reserved leading `🗄️` sidelined marker when present, and
  clears the current thread's pin state when needed. It is not an archive
  command.
- The fullwidth dash marker must be exactly `－`, not a hyphen-minus `-`, en
  dash, or em dash.
- Never leave a priority star or another emoji in the closed title; `🗄️` is the
  sole reserved exception when it was intentionally added by sideline-feature.
- Never double-prefix the fullwidth dash; strip any existing leading `－` before
  rebuilding the title.
- If `set_thread_title` fails, do not claim the thread is closed.
- If the thread was pinned, verify that `set_thread_pinned(pinned=false)`
  succeeded before claiming it is fully closed.
- The final response is the last step after the rename attempt.
