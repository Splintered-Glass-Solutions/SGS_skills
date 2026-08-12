---
description: Interview toward the real project goal and produce a small, verified spec before implementation.
argument-hint: [project-idea-or-context]
---

# Interview Spec

Interview the user to clarify the real project goal, reduce the request into small compartmentalized specs, and verify key decisions explicitly.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `$CODEX_HOME/skills/interview-spec/SKILL.md`.
2. Treat `$ARGUMENTS` as the seed project idea, feature request, automation, product direction, or unclear implementation ask.
3. If `$ARGUMENTS` is empty, infer the seed from the current conversation when obvious; otherwise ask for the project idea or workstream.
4. Stay in interview/spec mode until the user explicitly asks to implement after verifying the decisions.

## Required Behavior

- Find the real goal behind the request.
- Bias toward the smallest coherent scope slice.
- Split broad work into compartmentalized specs.
- Keep confirmed decisions, assumptions, and open questions separate.
- Ask the user to verify the key decisions explicitly before finalizing the spec or moving into execution.

## Output

When enough information is available, produce a concise spec with:

- real goal
- target user or operator
- confirmed decisions
- assumptions
- non-goals
- smallest useful scope
- acceptance criteria
- verification plan
- risks or unknowns
- recommended next action
