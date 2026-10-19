# Cleanup Worktrees Agent Playbook

This is a platform-neutral version of the `cleanup-worktrees` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Audit agent worktrees by actual chat inactivity, preserve unfinished work with sideline-feature, close inactive chats, and remove verified recoverable worktrees. Use for stale worktree or disk cleanup; skill creation and audit requests do not authorize deletion.

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

> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.


# Cleanup Worktrees

Use the shared [repository worktree lifecycle contract](../repo-worktree-lifecycle/references/operating-contract.md)
for checkout ownership and terminal states. This skill retains the detailed
preservation and deletion gates; the shared contract does not authorize broader
cleanup.

Default inactivity cutoff is 30 days. Use actual chat messages as the main
signal. Builds, dependency installs, metadata sweeps and title changes are
supporting evidence, not proof of active feature work.

## Audit candidates

1. Establish requested roots and cutoff. Inventory folders, nested Git
   checkouts, allocated sizes and free disk space. Reuse recent inventories
   instead of repeating expensive recursive scans.
2. Run `scripts/audit_threads.py` to map worktrees to chats and read actual
   user/assistant message dates. It is read-only. Confirm selected chats with
   app thread tools, including current title, identity and running state.
3. Accept ownership from exact chat CWD, an app worktree attachment, or a
   UUID-named folder matching the chat ID with the exact folder path recorded
   in that chat history. A casual path mention, similar title, branch name or
   dated folder name alone does not prove ownership. Resolve uncertain maps
   from scoped creation records; otherwise preserve them.
4. Every chat sharing a worktree must be inactive past the cutoff. Include
   child chats. A running task, open file, active automation, recent substantive
   source change or another recent owner blocks deletion. Pinning is a
   visibility preference: an inactive pinned chat may be unpinned under the
   user's cleanup authorization.
5. Inspect HEAD, branch, dirty/untracked/ignored files, Git operations, locks,
   stashes and Dev integration. Resolve the real Dev name including case.
   Record fetched upstream SHAs when refresh is necessary. Never move a
   checked-out Dev branch.

Produce a compact report: exact chat, last message date, folder, size,
dirty/unique work and planned preservation. Audit-only and skill-writing
requests stop at that report. Existing explicit cleanup authorization applies;
do not ask for it again.

## Preserve → sideline → close → remove

Proceed only for candidates covered by the user's cleanup authorization.

1. **Preserve code.** Documentation does not preserve implementation. Run
   `scripts/preserve_worktree.py` for each checkout: record HEAD/branch, create
   a Git bundle, save staged/unstaged binary patches and untracked files, and
   verify restored content in a temporary checkout. Keep original branch refs
   and stashes. Save reviewed root run notes and QA evidence too. Put recovery
   outside the removed folder in a private local directory; link it from the
   packet. Unknown ignored files require review. Never copy secrets into
   packets or recovery archives. Unique credential bindings without a retained
   source block that checkout.
2. **Sideline the exact owning chat.** Read its turns and use `$sideline-feature`
   to save completed work, dated proof, unfinished scope, decisions, paths/SHAs,
   recovery links and a resume plan in canonical `sideline_features/`. example-project-12
   uses `example-project-1`. Update the index and keep packets outside removed
   worktrees. Completed tasks need a short closeout packet that sidelines only
   their unresolved follow-up scope.
3. **Close the target with `$close-thread`.** Keep 🗄️ as the sole leading marker,
   unpin if necessary, and verify title/pin state. Do not archive. Keep the
   originating cleanup chat open. When the human explicitly authorizes
   messaging the owning chat, send a preservation-only prompt and wait for its
   final result; verify packet/closeout. Otherwise perform those workflows for
   the named target using app tools. A current-chat default must never rename
   the cleanup chat accidentally.
4. **Recheck before removal.** Require the same HEAD/status as the recovery
   manifest, no new substantive human message except the authorized preservation
   turn, recovery proof, no running owner/open files, and packet/closeout proof.
   A preservation turn does not restart the inactivity clock for that already
   authorized candidate; unrelated new work does. Skip changed candidates.
5. **Remove the named checkout.** Prefer `archive_worktree` for app-managed
   worktrees and verify its recoverable snapshot. For manual worktrees use
   `git worktree remove` without force. If verified preserved untracked files
   prevent removal, remove only exact manifest-listed originals with matching
   retained hashes, then retry once without force. Preserve secret-bearing and
   unknown files. Never force-remove, reset, blanket clean, delete primary
   checkouts or delete remote branches. Remove parent containers only after all
   checkouts are gone and remaining reviewed files are preserved. Multi-repo
   features require compatible recovery packets for every affected repo.

## Finish and resume

Save a ledger with per-chat/check-out result, timestamps, original HEAD/status,
manifest/packet links, closure/removal proof, failure reason and next action.
Recheck Git registrations, primary checkouts, branch refs and stashes. Report
both allocated bytes removed and actual net free-space change; APFS sharing
and concurrent activity make them different quantities.

Separate discovery from deletion so resumed runs reuse valid packets and
recovery artifacts. Read [recovery-and-improvements](references/recovery-and-improvements.md)
for restoration and optional refinements.
