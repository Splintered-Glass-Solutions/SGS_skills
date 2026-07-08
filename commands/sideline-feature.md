---
description: Preserve a scoped feature idea or plan in a sidelined-features folder so it can be resumed later without implementing it now.
argument-hint: [feature-name-or-context]
---

# Sideline Feature

Capture a deferred feature plan, product exploration, or technical design into the appropriate sidelined-features folder.

The user invoked this command with: $ARGUMENTS

## Preflight

1. Read and follow the local skill at `/Users/preston/.codex/skills/sideline-feature/SKILL.md`.
2. Treat `$ARGUMENTS` as the feature name, feature description, or context to sideline.
3. If `$ARGUMENTS` is empty, infer the feature from the current conversation when obvious; otherwise ask for the feature name or scope.
4. Stay documentation-only unless the user explicitly asks for implementation.
5. Do not make the feature look like active roadmap, current production behavior, or a customer-facing commitment.

## Destination Rules

- For Bonfire ecosystem work, use `/Users/preston/Code/bonfire_shared_docs/sideline_features/`.
- For other repositories, use `<repo-root>/sideline_features/` unless a clear local equivalent already exists.
- Inspect existing folders and references before renaming anything.
- Do not rename existing folders if it would break manifests, links, governance docs, automations, or unrelated work.

## Packet Requirements

Create or update a Markdown feature packet that includes:

- summary / product thesis
- current recommendation
- user-facing implications
- non-goals
- proposed scope
- repo or service boundaries
- work packages or phases
- validation plan
- risks and mitigations
- open questions
- recommended next step

Use `/Users/preston/.codex/skills/sideline-feature/references/feature-packet-template.md` when the target repo has no better template.

## Safety

Do not:

- implement the feature
- apply migrations
- deploy
- push, merge, or create a PR
- mutate live systems
- write secrets, private customer data, or sensitive transcripts into the packet
- overwrite unrelated docs

## Final Response

Return:

- the saved artifact path as a clickable link
- whether an index was created or updated
- any folder naming decision
- confirmation that no implementation changes were made

