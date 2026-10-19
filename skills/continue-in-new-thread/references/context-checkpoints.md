# Context checkpoints for sustained execution

Build It and Autonomous share these rules. Read once when either execution run
starts; do not reload at each checkpoint. Keep the assessment in the existing
project ledger/checkpoint, not another growing report.
Each successor measures its own current context and restarts these chat-local
milestone counters; inherited load readings describe the source chat only.

## Assess cheaply at milestones

Record the signal, load band, rotate/stay/defer decision and next safe boundary.
Use current context tokens or remaining-window percentage only when the runtime
actually reports them. The latest per-response `input_tokens`, including cached
input, is a useful request-size signal; cumulative `total_token_usage` is not.
Lifetime token totals, account usage percentages and cached-input totals are not
current context occupancy. Mark missing metrics
`unavailable`; do not scan full transcripts just to estimate them.

### Economic context budget

Use these defaults even when the model has ample window remaining. Cached history
still contributes to usage; a cache hit does not waive a handoff. Assess only at
milestones or before a large load, using metrics already available or a bounded
latest-usage read. Do not add per-call transcript scans or polling to measure cost.

| Latest reported request input | Action while substantial work remains |
| --- | --- |
| Below 75k tokens | Continue with narrow packets and reads. |
| 75–99k | Update the compact checkpoint and select a stable handoff milestone. |
| 100–124k | Rotate at the next safe milestone before another substantial item or phase. |
| 125k or more | Finish or safely stop the current bounded unit, then rotate before new broad work. |

These are soft operating budgets, not hard caps or measured savings. Required
evidence and safe mutation completion take precedence. If unavoidable startup or
required task context already exceeds the budget, record that baseline and narrow
new loads; do not repeatedly create equally large chats. Skip a handoff with no
meaningful context reduction. Keep enough safety information to execute correctly.

### Window safety reserve

Also use these window bands; act on whichever economic or safety signal triggers
earlier. Do not wait for window exhaustion to control cost.

| Reported current window used | Action while substantial work remains |
| --- | --- |
| Below 60% | Apply the economic budget; this band alone does not justify staying. |
| 60–74% | Update the checkpoint and select the next stable handoff milestone. |
| 75–84% | Rotate at the next safe boundary before starting another large phase. |
| 85% or more | Reserve room for the handoff; reach the nearest safe checkpoint without starting new broad work. |

If metrics are unavailable, count substantial implementation/review/repair cycles
and large phase transitions since this chat began. Plan rotation after two such
cycles or two large phases that accumulated substantial source/tool material.
A compaction notice, difficulty recovering decisions, or repeated recovery of old
history is an earlier rotation signal. Record the observed reason, not an invented
token count. Small steps and short lookups do not count. Check before large loads
too; rotate earlier if the next phase would likely exhaust the available room.

Skip rotation when only a short final verification/report remains. A new chat has
its own startup cost; do not rotate on every phase or claim a summary shrinks
context already carried in this chat. Aim for a handoff prompt around 1–2k tokens
with links to the authoritative checkpoint; exceed this only for essential
constraints or exact recovery information. Load only current-phase references, use
bounded source reads, and store raw logs/evidence on disk with concise pointers.

## Make a stable handoff

When rotation is due, follow [Thread Handoff](../SKILL.md). The parent skills record
the user's explicit request for automatic continuations; carry that instruction and
the original invocation into the packet. Respect a later no-new-chat instruction,
user pause, or tool restriction. Do not create chats merely while editing skills.

Before creation, finish or safely stop all task writers and their subprocesses.
Record active services/operations and their ownership; never transfer halfway
through a migration, merge or provider mutation. An unresolved test may transfer
after a bounded repair cycle, with its failure and attempt count intact. If an
approval/answer is pending and continuation depends on it, stay in the source.

Use the existing ledger/checkpoint as authority. Give the successor a short prompt
with its exact path, objective, constraints/permissions, current gate, checkout
and HEAD/dirty state, critical decisions, blockers and next action. Link accepted
plans and proof instead of copying raw history, logs or all loaded skills. Carry
goal identity/status and total spend/retry allowances across all continuation
chats; a new chat does not reset them. Goals and agent IDs are provenance, not
proof that live goal/worker handles transferred. The successor checks its own
available goal state and reestablishes required workers without concurrent writers.
Preserve valid candidate-bound review evidence; never treat missing evidence as a pass.

Verify successor receipt, workspace access and priority before source closeout.
Mark needed worktrees `handed_off` with the successor owner; exclude them and
needed branches/services from source cleanup. If supported ownership transfer
is unavailable, keep the source open and record the limitation. Use the handoff
skill's `preparing` → `ready` checkpoint marker so the successor can prioritize
and inspect read-only without starting product work before transfer. Once ready,
only the successor coordinates writes; source work must not resume.

On resumption, read the checkpoint and current skill, recheck mutable Git/runtime/
provider state relevant to the next gate, and load only that gate's references.
Do not replay finished phases or the full source conversation. If creation or
verification fails, preserve the source/checkpoint and continue safe work there
when possible; record the failure rather than repeatedly creating successors.

## Calibrate these defaults

Use project-owned usage measurements when revising budgets. Measure worker, handoff, cache-warmup and retry usage together; no savings are guaranteed.
