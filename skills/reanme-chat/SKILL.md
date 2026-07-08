---
name: reanme-chat
description: Rename the current Codex chat or thread to a concise, relevant title based on how the conversation has evolved. Use when the user asks to rename, retitle, title, summarize the thread name, or change the chat/thread name from its initial auto-generated title to something more accurate.
---

# Reanme Chat

## Overview

Use this skill to rename the active chat thread after the conversation has drifted from its initial title or accumulated a clearer outcome.

## Workflow

1. Identify the dominant evolved topic from the conversation, weighting the latest substantive user goal and completed work more heavily than the first prompt.
2. Draft one title that is specific enough to distinguish this thread later.
3. Keep the title concise:
   - 3-8 words when possible.
   - Under 60 characters.
   - Title Case.
   - No trailing punctuation.
   - Avoid generic words like "Chat", "Help", "Misc", "Follow-up", or "Discussion" unless they are part of a product name.
4. Include the project, product, repo, client, or workflow name when it is the best retrieval handle.
5. If the thread has multiple unrelated phases, prefer the current or final actionable outcome. If the user explicitly asks for a title covering the whole thread, choose a broader title.
6. If the user asks for options, provide 3-5 candidates and do not rename until they choose. Otherwise, pick the best title and rename directly when the title tool is available.

## Renaming

To rename a Codex thread:

1. Use `tool_search` to find the `set_thread_title` tool when it is not already available.
2. Call the thread-title tool for the current thread with the selected title.
3. If the title tool is not available, tell the user the suggested title and that you could not apply it from this environment.

Do not create a new thread. Do not archive, pin, fork, or hand off the thread unless the user separately asks for that action.

## Title Examples

- `StrIQ AI Market Context Plan`
- `Bonfire Dev QA Repair`
- `B2B API Pilot Packaging`
- `Weekly Fathom Action Items`
- `Revenue Comps Trust Roadmap`
