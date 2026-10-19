---
name: loose-ends
description: >-
  Reconcile and finish unfinished project work across code, data, review, release,
  and closeout. Use when asked to complete loose ends, finish work started in a
  prior thread, or bring an in-progress project through its authorized delivery path.
---

# Loose Ends

## Goal

Turn the work already started in a project into a verified, integrated outcome. Find the actual unfinished items from repository and release evidence, complete the authorized scope, and leave a clear account of any genuine external blocker. Do not interpret “everything” as permission to expand into unrelated product work.

## Reconcile Before Editing

1. Identify the repository, current branch, `HEAD`, its merge base with the intended integration target, upstream tracking state, open PR/release state, and working-tree status. Record a checkpoint: starting commit, changed tracked files, untracked files, and any running work. Treat user files and generated artifacts as owned data; inspect before touching them.
2. Establish the task's own starting point from the thread context, issue/PR, work log, commit history, QA artifacts, migrations, deployment records, and relevant code. Separate completed-and-proven, incomplete, stale, and unrelated work. Avoid treating old plans or summaries as current proof.
3. Fetch or otherwise inspect the latest target branch before deciding how to integrate. Compare it with the recorded checkpoint and current branch, and inspect commits and file-level changes added since this task began. Repeat this check immediately before integration; do not rely on the branch state observed at task start.
4. If the target advanced, preserve both lines of work. Choose the least disruptive integration strategy based on repository policy and branch ownership. Usually bring the latest target into the task branch, resolve conflicts by understanding both versions, then integrate the completed task back into that updated target. If work is already on the target branch, do not assume its local history is disposable or pushable; determine which commits are task-owned, which are newer independent work, and what remote review policy requires.
5. Never use force push, hard reset, destructive checkout, blanket cleanup, or broad file replacement to make reconciliation easy. Never overwrite a file or migration introduced or changed since the task checkpoint without inspecting and intentionally combining its behavior. Preserve unknown changes. If a conflict cannot be resolved confidently, isolate it and report the exact paths and competing behavior rather than discarding either side.
6. Before integration, review the diff against both the task checkpoint and the latest target. Verify that newer target commits and task changes are all represented, with no unrelated user changes accidentally included. Re-run affected checks after conflict resolution.

## Finish the Work

1. Use the repository's current contribution, migration, deployment, and environment instructions. Confirm the actual branch model (`dev`, release branch, or direct production); do not invent a `dev` path if the project does not use one.
2. Complete every discovered item that is in scope and already authorized. Prefer small, coherent changes. For database work, identify unapplied migrations and their order, inspect destructive effects, apply them only to the intended environment, and run the repository's validators. Apply required non-destructive migrations without a separate approval or independent review checkpoint, including scoped function grants on a verified shared Dev/Production database. Verify target, compatibility, and readback directly. Ask for migration approval only for destructive actions; keep unrelated permission, ownership, and RLS changes outside scope.
3. Run the focused checks required by the changed behavior, then the appropriate broader suite and runtime smoke checks. A successful build does not prove database migration, hosted behavior, or deployment. Record evidence for each relevant gate.
4. Inspect git status and the complete diff before staging. Stage only task-owned files. Commit with a useful message when requested or required by the delivery workflow. Push and create/update a PR only when authorized and consistent with project policy; attach the PR in the current task when the app supports it.
5. Deploy only to the project's real target after required review, migration, and release gates pass. Verify the deployed target itself, including routes/data or runtime behavior affected by the change. Do not claim production completion from local checks or a feature-branch deployment.
6. Clean up only task-owned temporary files and processes after verifying ownership. Do not remove pre-existing or unexplained untracked artifacts. Close a thread only after code, integration, release, and proof are complete; follow the close-thread skill's state changes separately.

## When Blocked

Continue all independent, reversible work first. If an unresolved decision, credential, unavailable service, denied review, or policy gate prevents full completion, use `interview-spec` continuation mode: provide a short evidence-based checkpoint and A/B/C options with a recommended path, consequences, and the exact next input needed. Do not label work complete or close the thread while a material gate remains open.

## Closeout

Summarize the work completed, the commit/PR and target environment, migration status, verification evidence, and any remaining blocker. Distinguish local completion, integration, and deployment. Keep the project state usable for the next person and leave no owned process or task artifact unexplained.
