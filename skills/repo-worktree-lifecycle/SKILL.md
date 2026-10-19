---
name: repo-worktree-lifecycle
description: Coordinate isolated Git worktrees across parallel coding, integration, release, handoff, and cleanup. Use when creating or reusing worktrees, merging parallel changes, deploying from a worktree, or preventing stranded local work.
---

# Repository Worktree Lifecycle

Use this shared workflow across repositories. Read the [operating contract](references/operating-contract.md) whenever work will create or change a branch/worktree, integrate parallel work, publish a release, or remove a checkout. Repository-specific instructions still define the true remotes, release refs, test commands, provider targets, and permissions.

This skill keeps parallel writers isolated, integration serialized, deployed revisions traceable to remote release refs, and every worktree owned or safely recoverable. It does not grant permission to publish, deploy, discard work, or remove checkouts beyond the current task's authorization.
