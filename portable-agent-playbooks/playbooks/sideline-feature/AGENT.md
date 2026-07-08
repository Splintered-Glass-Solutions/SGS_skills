# Sideline Feature Agent Playbook

This is a platform-neutral version of the `sideline-feature` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Capture and preserve scoped feature ideas, feature plans, product explorations, technical designs, or deferred implementation context into a dedicated sidelined-features folder so future work can resume without losing decisions, source context, tradeoffs, and next steps. Use when the user says to sideline, park, shelve, defer, backlog, save for later, preserve context, or organize a feature plan without implementing it.

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

# Sideline Feature

Use this skill when a feature has been explored or scoped but should not be implemented now. The goal is to preserve useful context in the right repository location without making it look like active implementation truth.

## Workflow

1. Confirm the work is documentation-only unless the user explicitly requests code changes.
2. Identify the target repository:
   - For Bonfire ecosystem work, prefer `<workspace>/bonfire_shared_docs/sideline_features/`.
   - For other repositories, use a repo-local `sideline_features/` folder at the repository root unless an existing equivalent folder is clearly established.
3. Inspect existing folders and references before renaming anything.
   - Do not rename existing folders if doing so would break manifests, governance docs, links, imports, automations, or unrelated in-progress work.
   - If an older folder exists with a different name and is referenced elsewhere, create or use `sideline_features/` instead of churning existing structure.
4. Create or update `sideline_features/README.md` with a concise index if it does not exist.
5. Save the feature packet as a dated Markdown file:
   - `YYYY-MM-DD_<short-feature-slug>.md`
   - Use lowercase words separated by hyphens or underscores consistently with the repo.
6. Include front matter when the repo uses front matter. For Bonfire shared docs, include:
   - `id`
   - `title`
   - `doc_type: feature_plan`
   - `system`
   - `canonical_for`
   - `not_canonical_for`
   - `owner`
   - `status: draft`
   - `source_repos`
   - `source_paths`
   - `last_verified`
   - `review_cycle_days`
   - `audience`
   - `tags`
7. Make the document decision-ready but explicitly non-canonical.
8. Final response should link the saved artifact and state that no implementation changes were made.

## What To Capture

Every sidelined feature packet should include enough context for a future agent or engineer to resume:

- problem statement and product thesis
- current recommendation
- user-facing implications
- non-goals
- open decisions
- repo/service boundaries
- relevant source docs, paths, tickets, calls, or evidence
- proposed phases or work packages
- validation plan
- risks and mitigations
- gated actions or approvals
- recommended next step

Use `references/feature-packet-template.md` as the default structure when the repo has no better template.

## Bonfire-Specific Rules

For Bonfire, use `bonfire_shared_docs/sideline_features/` for cross-system sidelined features. This is intentionally different from canonical system docs and from implementation repos.

Preserve these boundaries:

- `bonfire/`, `Bonfire_AI/`, and `Bonfire_ETL/` source repos remain implementation truth.
- `bonfire_shared_docs` can preserve cross-system feature context.
- Sidelined feature docs are draft planning context, not customer-facing commitments or current production behavior.

If the sidelined feature is system-specific but still strategic, keep it in shared docs and mark the relevant `source_repos`. If it is purely local to a non-Bonfire repo, use that repo's local `sideline_features/`.

## Safety Rules

- Do not implement the feature while sidelining it.
- Do not apply migrations, deploy, push, merge, or mutate live systems.
- Do not create customer-facing compliance/legal claims.
- Do not present draft plans as current state.
- Do not overwrite or reorganize existing docs unless the user explicitly requested that exact cleanup.
- Do not dump secrets, private customer data, or sensitive transcripts into the packet. Link or summarize safely.

## Final Answer Shape

Keep the final answer short:

- artifact path as a clickable link
- whether an index was created/updated
- any folder naming decision, especially if an expected folder was not renamed
- confirmation that no implementation changes were made


