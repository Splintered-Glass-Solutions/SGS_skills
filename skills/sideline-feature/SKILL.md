---
name: sideline-feature
description: Capture and preserve scoped feature ideas, feature plans, product explorations, technical designs, or deferred implementation context into a dedicated sidelined-features folder, mark the current task with a 🗄️ sidelined prefix, and close the thread. Use when the user says to sideline, park, shelve, defer, backlog, save for later, preserve context, or organize a feature plan without implementing it.
---
# Sideline Feature

Use this skill when a feature has been explored or scoped but should not be implemented now. The goal is to preserve useful context in the right repository location without making it look like active implementation truth.

## Workflow

1. Confirm the work is documentation-only unless the user explicitly requests code changes.
2. Identify the target repository:
   - For the current repository, use a repo-local `sideline_features/` folder at the repository root unless an existing equivalent folder is clearly established.
3. Inspect existing folders and references before renaming anything.
   - Do not rename existing folders if doing so would break manifests, governance docs, links, imports, automations, or unrelated in-progress work.
   - If an older folder exists with a different name and is referenced elsewhere, create or use `sideline_features/` instead of churning existing structure.
4. Create or update `sideline_features/README.md` with a concise index if it does not exist.
5. Save the feature packet as a dated Markdown file:
   - `YYYY-MM-DD_<short-feature-slug>.md`
   - Use lowercase words separated by hyphens or underscores consistently with the repo.
6. Include front matter when the repo uses front matter. A reusable schema may include:
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
8. Mark and close the current task after the artifact and index work succeeds:
   - Replace all existing leading status markers with one `🗄️` marker to
     indicate that the work is sidelined. Preserve the useful non-status title
     text and rebuild the title as `🗄️ <title>`.
   - Invoke the `close-thread` skill as the final workflow action. It must keep
     `🗄️` as the sole leading marker and unpin the current thread when needed;
     it must not add `－` beside it. Do not archive the thread.
9. If close-thread fails after the artifact is saved, report the saved artifact and the closeout failure separately; do not claim the thread was closed.

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

## Shared-documentation projects

Use a configured shared-docs repository for cross-system plans when the project
has one. Source repositories remain implementation truth; sidelined documents
are draft planning context. Record affected repositories without assuming a
particular repository family or making customer-facing commitments.

## Safety Rules

- Do not implement the feature while sidelining it.
- Do not apply migrations, deploy, push, merge, or mutate live systems.
- Do not create customer-facing compliance/legal claims.
- Do not present draft plans as current state.
- Do not overwrite or reorganize existing docs unless the user explicitly requested that exact cleanup.
- Do not dump secrets, private customer data, or sensitive transcripts into the packet. Link or summarize safely.

## Final Answer Shape

Keep the closeout response short. After the artifact is saved, the `close-thread` closeout is the final response and should include:

- artifact path as a clickable link
- whether an index was created/updated
- any folder naming decision, especially if an expected folder was not renamed
- confirmation that no implementation changes were made
- confirmation that the current task was marked with `🗄️` and closed, unless close-thread failed
