# Sequential build workers

Applies to user-authorized build-it execution and explicit build-plan,
build-implement or sol-review requests. Build-it always routes item review to
sol-review; its execution path does not call astra-review. A standalone
astra-review request may use this contract for that independent review. Use
same-task subagents, not new the agent sidebar tasks. The parent retains scope,
ordering, authority, canonical ledger,
integration, release and final proof. Subagents do not recursively orchestrate.

## Compact packet

Pass objective/item ID; accepted decisions/exclusions; applicable constraints and
authority; exact repo/worktree/branch/base SHA plus scoped dirty state; relevant
source paths; acceptance assertions and proof phase; selected prior evidence;
assignment, writable paths and requested return. Link artifacts; do not attach
full conversation, raw logs, all skills or the entire batch when unnecessary.
Workers still receive platform/repository instructions: fork_turns=none removes
conversation inheritance, not all startup overhead.
Aim for a dispatch prompt around 1–2k tokens plus linked plans/evidence. Load only
the assigned item's relevant sources and current-phase skills; never omit essential
constraints to meet the packet target. Return concise findings and artifact pointers,
not source dumps or replayed logs.

## Worker context lifetime

The parent must assess worker context as well as its own. Use latest reported
per-response input when available; never treat cumulative agent usage as occupancy.
Checkpoint near 75k input, refresh at a safe boundary from 100k, and do not start
new broad work from 125k. These are soft defaults; finish unsafe-to-interrupt
operations and preserve required evidence. Record unavoidable startup context
instead of repeatedly spawning equally large replacements.

Start fresh planners and implementers for each new item. An idle Luna/high planner
may continue into implementation of the same item only if context is below 75k
when measurable, or clearly limited to one bounded planning pass when unavailable.
Reuse same-item implementers/reviewers for focused repairs while still lean. When
metrics are unavailable, refresh after two substantial repair/review cycles that
accumulated large packets. A compaction notice requests a checkpoint and refresh
at the next safe boundary when substantial work remains; do not retain one worker
through many compactions. Skip refresh for a short final result/check only.

Workers return a checkpoint to the parent before their budget is exceeded by the
next large load. They never create chats, replacement agents or worktrees. The
parent stops/waits for the old worker and its subprocesses, reconciles SHA/dirty
state and ownership, then dispatches a replacement with `fork_turns="none"`, the
same required model/effort, accepted plan, exact next action, evidence and cumulative
attempt counts. Keep the existing worktree/runtime and valid proof. A replacement
reviewer remains independent of planner/implementer and checks the repaired current
candidate and affected boundaries. Refreshing context does not reset a failed gate.
Record replacement agent IDs, required routing, retired owner and context signal
in the canonical ledger. A checkpoint return leaves unfinished acceptance gates
pending; it is neither a pass nor a new failure. Advance only after the required
current-state proof and independent review pass.

## Worktree ownership and sequence

Use one task-owned batch worktree per affected repository, shared sequentially
across all items. Do not create a worktree per worker/item. Only one implementation
worker may write in the batch at a time, including generated files and service
commands. The parent records owner agent ID, item, worktree and starting state;
while owned, the parent and reviewers do not modify that checkout or ledger files
inside it. Worker returns are reconciled into the ledger by the parent after release.
Never run a reviewer against a moving implementation. On interruption, stop/wait
for the writer and its owned commands, inspect state, then transfer ownership.

For each item:
1. Plan with build-plan against the current batch state and earlier item results.
2. Parent checks scope/dependencies; resolve only material missing decisions.
3. Implement with build-implement on Luna/high, with focused local validation.
4. Review the stable candidate with sol-review on a fresh Sol 6.1/medium worker.
5. Return concrete defects to Luna, validate and re-review until passed or blocked
   under the bounded repair rule. The parent checks verdict against current state.
6. Record local completion and evidence before advancing to the next item. Preserve
   blocked status; only independent authorized items may proceed after writer release.

Do not simulate changing an agent's model via text instructions. New workers use
explicit model, reasoning_effort and fork_turns=none. Reuse only a worker already
on the required model/effort. Parent waits with bounded calls and handles completed
returns; no polling of unchanged state and no workers left running after closeout.
Use bounded waits that leave room for user updates. Prefer one status snapshot per
meaningful event; do not repeatedly read full worker histories or launch a model
turn merely to narrate an unchanged wait. Keep long command output in files and
return only the exit status, concise error/proof and relevant artifact paths.
If model or delegation tooling is unavailable, report the exact limitation and
continue only independent supported work. Do not silently substitute a model or
create visible tasks. No savings percentage is guaranteed; measure whole-job usage.

## Proof and authority

Per-item Luna work owns implementation, required docs/QA records, one quality review
and focused local proof. Sol 6.1 owns independent review, not edits. Parent owns batch
interaction checks, integration, deployment and hosted proof under execution-contract.
Re-use unaffected evidence; never replace a required runtime gate with a review.
No child may expand scope, cloud permissions, paid test allowances, environment or
external communication authority. No review pass means the item remains incomplete.
