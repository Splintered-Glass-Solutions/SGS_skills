---
name: explain-clearly
description: Explain or re-explain a topic in plain, accessible language. Use when the user asks to simplify an explanation, says “explain like I'm five,” or invokes this skill.
---

# Explain Clearly

Explain the subject to an intelligent adult who may not know its technical background. Use the current conversation as context when the user has not named a topic; ask what to explain only if the subject is unclear.

- Lead with the main point and why it matters in the user's situation. Provide enough background to connect the pieces, then explain how they work or what happens next as relevant.
- Prefer everyday words and short, direct sentences. Replace unnecessary jargon; when a technical term is useful or unavoidable, briefly define it in context.
- Use a concrete example or a familiar metaphor when it makes the idea easier to grasp. Explain where a metaphor stops fitting if that distinction matters.
- Preserve accuracy, important caveats, and uncertainty. Simplify the language, not the facts; don't invent details to fill gaps.
- Match the length and detail to the question. Avoid talking down to the user, childish language, forced metaphors, and announcing that the explanation is “for a five-year-old.”

## Use it

Example: `Use $explain-clearly to explain how this project's background jobs work
and why retries matter.` Supply the topic, audience and any source material. If
no topic is supplied, use the conversation only when it clearly identifies one.

Return a clear explanation and a concrete example where useful, with important
limits and uncertainty preserved. No external tools are required for a conceptual
explanation; factual verification still requires appropriate sources or project
evidence. This workflow does not authorize unrelated edits or external actions.
