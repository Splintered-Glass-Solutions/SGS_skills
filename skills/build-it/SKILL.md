---
name: build-it
description: Carry a bounded feature batch through model-routed planning, sequential implementation, review, local integration, authorized deployment and proof.
---
> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.


# Build It

Carry the supplied feature or bounded batch through the sequence below in the
current task, with fresh continuation chats when context warrants. Read each
linked skill when its phase begins and follow its
mechanics. Phase calls stay within one workflow; context continuations below
replace its coordinator chat. A request to create, edit, or explain this skill does
not start a product build.

## Invocation and autonomous handoffs

Example: `$build-it add Astra to example-project-12 with the agreed credit pricing`.

An invocation requesting execution authorizes the named scope through all
phases, including local integration and the deployment target rule below.
Make routine implementation decisions, produce a concrete brief, and proceed
without asking the user to invoke the next skill or approve the same scope again.
Explicit narrower user limits (such as planning only, local only, no deploy,
or a usage cap) still govern the run.

At the start of each execution run, resume a matching active goal if one exists;
otherwise create one with this objective: complete the supplied scope through
all build-it phases, including build, tests, merge, deployment, and final proof.
If a different unfinished goal prevents creating it, do not replace or complete
that goal; keep this build's ledger current and report the limitation. Keep
working through the ordered steps unless the user narrows or stops the work. Do
not mark the goal complete at a child-skill milestone or after local tests.

Use the user's supplied scope and latest corrections. Do not silently include
other captured ideas or unrelated work from this task. If a material decision
cannot be resolved from evidence, complete independent in-scope work and ask
only for that decision. Access failures, incompatible product intent,
destructive operations, and unresolved provider targets remain real boundaries.
No customer messages, permission expansion, purchases, or destructive data work
are authorized merely by invoking the workflow.

## Required subagent execution

These are mandatory execution gates, not optional delegation suggestions. Keep
this task as coordinator; do not perform item design, implementation or review
in the coordinator as a shortcut, even when its model matches the required worker.
Use [the worker contract](references/worker-contract.md) and these phase skills:

| Phase | Skill | Explicit worker settings |
| --- | --- | --- |
| Routine item plan | [build-plan](../build-plan/SKILL.md) | `model="gpt-6-luna"`, `reasoning_effort="high"` |
| Complex item plan | [build-plan](../build-plan/SKILL.md) | `model="gpt-6.1-sol"`, `reasoning_effort="low"` |
| Implementation, tests and repairs | [build-implement](../build-implement/SKILL.md) | `model="gpt-6-luna"`, `reasoning_effort="high"` |
| Independent item review | [sol-review](../sol-review/SKILL.md) | `model="gpt-6.1-sol"`, `reasoning_effort="medium"` |

New workers must use `collaboration.spawn_agent` with `fork_turns="none"` and
explicit model/effort arguments. Pass compact scoped packets, not the conversation.
Classify each plan with a recorded reason: established localized work is routine;
material architecture, shared-data, auth, billing or rollout decisions are complex.
Reuse an idle Luna/high planner only for that same item's implementation while its
context remains lean under the worker contract. Start fresh workers for later items.
A Sol 6.1 planner
cannot become Luna through a follow-up instruction. Initial review must use a fresh
Sol 6.1/medium worker distinct from both planner and implementer; it is read-only.
Use its findings to direct the next changes: send each actionable defect to Luna,
then have the reviewer inspect the repaired current state before the item passes.

Use one batch worktree per affected repository, shared sequentially across items.
Only one implementation worker may write at a time, including owned subprocesses;
no reviewer runs against a moving candidate. The Batch Brief establishes scope and
order; detailed item planning uses the state left by preceding items. Read worker
skills only as their phases begin. Do not create sidebar worker tasks or change
the coordinator's model. A verified context continuation replaces the coordinator
chat; it is not a worker fallback. Parent integration, release and hosted-proof
gates remain.

For each item, record planner/implementer/reviewer agent IDs, actual requested
model/effort, routing reason, accepted plan, candidate SHA plus scoped dirty state,
local proof and review verdict tied to that candidate. Do not mark the item complete
or advance dependent work without required local gates and a current-state Sol 6.1
pass. A missing or stale review is incomplete, not implicitly approved. Independent
items may proceed only after a blocked item's writer has stopped and state is safe.

If required tooling/model is unavailable, mark that gate blocked and report the
specific limitation. Do not silently substitute models, self-review, do the worker's
job in the coordinator, or create a visible task as fallback. A user may explicitly
change these rules; record that override instead of claiming the default flow ran.

## Ordered sequence

Before planning, read [the execution contract](references/execution-contract.md).
Pass its ledger path, scope, current phase, authorized environment, and gate
schedule into every child skill and bounded worker. This contract governs
orchestration only when the user has invoked build-it for execution; editing or
reviewing skills does not start or resume a product build. Standalone child
invocations retain their own boundaries. Higher-priority instructions, explicit
user limits, and tool-required confirmations always prevail.

After identifying the affected repositories, read the shared
[project deploy-path skill](references/project-release-adapter.md) and its route
directory during planning. Recheck the selected route and current registries
before deployment; use the project-specific skill and runbook for each component.

At the start of execution, also read the shared
[repository worktree lifecycle contract](../repo-worktree-lifecycle/references/operating-contract.md).
It governs checkout ownership, parallel writers, clean integration lanes, release
source and worktree closeout across projects. Project skills still supply their
own branch topology and provider procedures.

Own routine engineering and safe rollout decisions within the accepted scope.
Do not ask the user to choose a compatibility adapter, reversible activation
mechanism, dependency setup, test-harness repair, or release wiring when evidence
supports a safe implementation. Resolve rollout feasibility during planning,
not after writing a globally enabled migration. Read-only verification of live
targets and deployed consumers precedes topology-dependent decisions.

Skill links resolve relative to this folder in `<agent-config>/skills`.

1. **Capture — [to-do-list](../to-do-list/SKILL.md).** Capture the supplied
   bounded scope with its note rules. Reuse an existing matching capture rather
   than duplicating it. This is an internal capture phase: immediately leave
   gathering mode for planning; do not end the workflow with `Noted.`.
2. **Plan — [to-do-list-planning](../to-do-list-planning/SKILL.md).** Produce
   the Batch Brief, item IDs, acceptance criteria, exclusions, repositories,
   overlap zones, dependencies, and validation. The parent invocation starts
   the next bulk-edit phase for the unambiguous in-scope brief; a standalone
   planning skill's end-of-phase handoff is not a new approval requirement.
3. **Prepare — [bulk-edits-thread](../bulk-edits-thread/SKILL.md).** Verify the
   integration baseline and topology, preserve competing work, create isolated
   worktrees and committed manifests, and establish the local runtime. Continue
   into build after preparation; do not wait for more edits to be supplied.
4. **Build — [bulk-auto-build](../bulk-auto-build/SKILL.md).** Enforce the
   required plan → Luna implementation → fresh Sol 6.1 review loop for every item.
   Complete items sequentially with its finish-line, migration, documentation, polish,
   and focused verification mechanics. Respect its local-only boundary during
   this phase. Keep the execution goal open through merge, deployment, and final
   deployed proof; use the batch ledger for detailed state and evidence.
5. **Polish — [make-it-better](../make-it-better/SKILL.md).** Review only cross-feature interactions and consistency not already covered
   by the single item-quality reviews. Reuse valid evidence. For one item or no
   new interaction, mark this phase not applicable with a reason. Additional
   polish requires a concrete defect; no artificial changes are required.
6. **Test the working tree — [test](../test/SKILL.md).** Validate the exact
   isolated feature worktrees and their local services. Reconcile prior item
   proof and run only missing, invalidated or cross-feature assertions. Repair found defects
   with local-only, no-deploy hot-fix loops and retest before advancing.
7. **Prepare collapse — [prep-collapse-bulk-edits](../prep-collapse-bulk-edits/SKILL.md).**
   Audit all accepted items and assemble the ready packet. The acceptance
   boundary here is the isolated working tree plus required authorized data
   prerequisites. The hosted tests in step 11 are explicitly scheduled after
   deployment, so their pending status does not create a circular pre-collapse
   requirement. Any provider acceptance explicitly required before integration
   still applies. Never advance with an unresolved required local gate.
8. **Collapse — [collapse-bulk-edits-thread](../collapse-bulk-edits-thread/SKILL.md).**
   Reconcile task-owned work into a clean, verified local dev-equivalent
   integration worktree, then update the canonical local development branch
   when it is safe. Preserve unrelated dirty and staged work in the primary
   checkout. A clean integration worktree alone does not pass the canonical
   branch closeout gate. Remove only safely reconciled temporary worktrees under
   the child skill's cleanup rules. Keep the task open.
9. **Test local dev — [test](../test/SKILL.md).** Start and validate the actual
   canonical local development branch and matching services after synchronization.
   Record its SHA and
   runtime routing. Exercise the actual integrated runtime and affected merge/routing boundaries;
   worktree proof alone does not satisfy this stage. Collapse checks on this
   same unchanged integrated runtime may be reused. Repair
   task-owned integration defects locally and retest before release.
10. **Deploy — [deploy](references/project-release-adapter.md).** Deploy to **Dev** for projects
    with multiple environments. For a project with exactly one registered
    environment, deploy to that sole environment, including production when
    that is the project's only environment. This is the user's chosen target
    rule, not an inference from a branch or provider name. Resolve the current
    [project deploy path](references/project-release-adapter.md) for every affected
    repository/component, then resolve the current environment and provider
    identity from its authoritative registry. Follow its named project skill
    and repository runbook. If the route is missing, conflicting, or not
    identity-verified, keep that deploy node pending/blocked; continue safe
    independent work, but do not guess or close Build It as deployed. If
    multiple environments exist but no Dev mapping exists, ask for the target.
    Use normal required commits,
    pushes, PRs, protected merges, migrations within authority, and provider
    rollouts, using the validated canonical local development branch as the
    candidate. Do not publish a separate integration worktree directly as a
    substitute if canonical sync is pending. Do not promote from Dev to production on multi-environment
    projects. Complete every required component and record live revisions.
11. **Test the deployed environment — [test](../test/SKILL.md).** Test the
    feature on precisely the environment and revisions just deployed, including
    applicable authenticated UI, workflow/data, and provider proof. Keep real
    customer data protected and use approved fixtures. Health alone is not a
    passing feature test.
12. **Fix found issues — [hot-fix](../hot-fix/SKILL.md).** If step 11 found no
    issues, record this phase as not needed. Otherwise diagnose from evidence,
    repair the smallest in-scope defect, verify locally, deploy to the same
    authorized environment, and repeat its affected hosted tests. Reconcile
    repair commits with the integration/release lane. Change the hypothesis
    after failed attempts; stop for a concrete unresolved blocker after three
    meaningfully different attempts per failure family. Never claim success
    while a required assertion is failing or untested.
13. **Sync canonical local dev.** After deployment and any hot-fix, fetch and
    recheck the mapped remote development release ref. Safely bring that release
    head and all accepted task commits into the canonical local development
    branch, then run affected local checks against its final SHA. Preserve a dirty,
    stale, or divergent primary checkout; leave this gate pending and keep the
    execution goal open until it can be reconciled safely. The provider release
    can be reported separately as deployed while closeout remains pending.
14. **Show proof — [showme](../showme/SKILL.md).** Present real screenshots or
    runtime evidence from the final tested deployed revision. In this workflow,
    showme intentionally runs last, after collapse and deployment. Preserve raw
    evidence, annotations, provenance, and readable artifact links. Branded
    assets or external delivery follow their own requested scope.

## Phase boundaries and resumption

### Context load and fresh continuations

the user explicitly requested automatic fresh-thread continuations for context-heavy
Build It runs. During execution, follow the shared
[context checkpoint rules](../continue-in-new-thread/references/context-checkpoints.md).
Assess at startup, after each reviewed item and phase, and before loading a large
packet. Prefer handoffs after preparation, a reviewed item, working-tree tests,
or integrated-local tests; after deployment, finish revision readback before
handing off. Use both economic request-size budgets and window safety bands; do
not wait for compaction or a context-limit failure. These checks apply to reused
workers too: replace them through same-task subagents, not continuation sidebar chats.

When the rules call for rotation, run
[$continue-in-new-thread](../continue-in-new-thread/SKILL.md) without a routine
approval pause, subject to current user limits and supported tool authority.
Continue the same batch from its first incomplete gate. Carry the canonical
ledger, worker/review records, scheduled gates, deployment authority, goal status
and cumulative budgets forward; never restart capture/planning or mark the build
complete merely because the coordinator moved. Editing this skill creates no chat.

Child skills' local-only and no-deploy rules apply during their own phases;
the parent explicitly invokes collapse and deployment later. A successful
child's completion sentence is a milestone, not the end of this workflow.
An explicit user stop or pause takes effect immediately.

Maintain one compact ledger alongside the Batch Manifest with the current phase,
feature IDs, repo/worktree/branch/SHA, integration target, deploy environment,
commands and results, evidence paths, unresolved items, and exact next action.
Use session-budget and safe-run guidance for sustained work. On resumption,
recheck mutable Git/runtime/provider state and continue from the first
incomplete phase. Reuse still-valid evidence; rerun checks when changed code,
integration, deployment, or an unresolved concern invalidates it.

Record phase status as pending, running, passed, blocked, or not applicable with
a reason. Do not silently skip phases. Keep worktree, integrated local dev,
remote release, deployed revision, authenticated feature behavior, and provider
readback as distinct claims. A failure in a prerequisite blocks dependent
phases but need not stop independent authorized work.

Record future gates as `scheduled` with their prerequisite phase and exact
operation/assertion. Scheduled is neither passed nor waived. A phase may pass
with future gates outstanding only under the compatibility conditions in the
execution contract. Do not automatically invoke pause on a child blocker; first
repair in scope or continue independent work. Stop immediately on a user pause.

When maintaining this workflow, exercise the read-only scenarios in
[workflow scenarios](references/workflow-scenarios.md); syntax validation alone
does not prove that the instructions lead to safe autonomous decisions.

## Completion

Finish with a concise account of the delivered behavior, local integration
SHA, target environment and deployed revisions, all three test stages,
hot-fix outcome, and clickable showme evidence. Report any genuine gap and its
next action. The workflow is complete only when every required phase passed
or is explicitly not applicable, each implemented item has the required worker
records and current-state Sol 6.1/medium review pass, and final proof matches the
deployed result. Only then mark the execution goal complete. Report any explicit
user routing override separately.
