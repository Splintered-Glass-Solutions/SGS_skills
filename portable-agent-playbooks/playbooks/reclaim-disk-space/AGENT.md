# Reclaim Disk Space Agent Playbook

This is a platform-neutral version of the `reclaim-disk-space` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Audit and reclaim disk space on a Mac when storage is low, prioritizing measured, disposable caches and generated output while preserving active work and data.

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

# Reclaim disk space

Use this for low disk space, requests to find or clear storage, and follow-up cleanup. Start with the user's requested target, preservation rules, and existing authorization. A request to find candidates is an audit; a request to clean up authorizes the routine, clearly disposable scope it describes. Do not repeat a permission question already answered. Present uncertain, consequential, or disruptive candidates concretely before asking about them.

## Measure and prioritize

- Record `df -k /System/Volumes/Data` before and after each cleanup class and at the end. Distinguish bytes reported by a tool from actual host free-space change: APFS clones, sparse files and concurrent activity make directory sizes unreliable as reclaim estimates. State the unit and target, if any.
- Use bounded `du` and targeted process/open-file checks instead of scanning the whole disk repeatedly. Rank by likely benefit and confidence; inspect `~/Library/Caches`, package caches, Downloads, `/private/tmp`, generated build output, Docker and Git temporary packs as relevant. Sizes, ownership, activity, and permissions must be verified now; prior results are leads, not deletion authority.
- Avoid disrupting builds, browser sessions, running jobs or worktrees. Preserve source, personal and client files, backups, app data, Codex sessions and checkpoints, volumes, databases, and unfinished or ambiguous work. Do not empty Trash as a shortcut. Do not bypass a tool or automatic approval rejection by changing the deletion method or permissions.

## High-value candidates

- **Regenerable package caches:** Check current size and active users. Where within the authorized cleanup scope, use the package manager's own targeted cleanup, such as `uv cache clean` or `pnpm store prune`; preserve dependencies needed for current or offline work. Do not force through npm ownership errors or alter ownership. Dry-run Homebrew cleanup and inspect the exact targets before applying it.
- **Generated builds:** Inactive `.next` directories have previously recovered substantial space. Establish their owning checkout and purpose, Git ignored/untracked status, process and open-file activity, and identity/mtime; recheck immediately before deleting. Preserve outputs used by an active server, unfinished task, proof, or uncertain worktree. Apply current user authorization and preservation rules; do not remove a worktree or treat size or age alone as proof of disposability.
- **Docker:** Use time-bounded `docker ps`, `docker system df` and relevant builder inventory; map containers, images and mounts to projects. If healthy and authorized, evaluate builder-cache pruning and Docker's supported space-reclamation mechanism, with host `df` readback. A restart interrupts containers: perform one only when explicitly requested or authorized and when it is consistent with all current database and workload preservation rules. If container state cannot be established, do not assume a restart is safe. Never manually delete `Docker.raw`, volumes, databases, or ambiguous containers; do not use broad `docker system prune --volumes`. Inspect whether a reclamation operation pulls or starts an image and its side effects before using it.
- **Browser and app caches:** Browser disk caches can be large; prefer the application's cache-clearing controls and preserve profiles, sessions and cookies unless explicitly included. Playwright browser revisions may be needed by existing project installations: inspect `.links`, installed revisions and active processes before treating any as unused. Preserve active updater staging and any item whose removal was rejected by automatic review.
- **Git `tmp_pack_*`:** Potentially large but high risk. Preserve recent, open, changing or ambiguous files and follow any current age or project-specific restriction. Any authorized removal requires individual regular-file identity and age checks, no writer, lock or open handle, unchanged final stat, and successful `git fsck --connectivity-only --no-dangling` before and after. Never delete permanent packs, refs, or working data to meet a target.
- **Downloads and logs:** Installed-app installer images, old logs and clearly redundant downloads may be useful candidates. Verify installation, ownership and need. Archives, photos, exports and business records are user data, not disposable caches; identify them for review rather than infer duplicates from their names. Check actual copies and hashes before calling files duplicates.

Stop when the requested outcome is met or only ambiguous/disruptive candidates remain. Report actual before/after free space, what was removed, material effects or failures, and the best remaining candidates with their estimated sizes and decision needed. If a restart, cleanup or permission operation is rejected, do not work around it; explain the rejection when it prevents completion.
