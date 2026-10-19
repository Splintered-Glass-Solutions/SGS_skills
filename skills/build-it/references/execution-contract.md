# Build-it execution contract

Applies only inside a user-authorized build-it execution. The parent owns phase
transitions; child completion reports are checkpoints, not final turn endings.
The parent's environment rule supplies the deployment target. This contract
does not override higher-priority instructions or tool confirmation requirements.
Child skills should link to this contract instead of copying this shared
introduction; keep their `build-it` sections limited to phase-specific rules.

## One inherited ledger

Use the existing Batch Manifest and one canonical cross-repo execution ledger.
Per-repo manifests link to that ledger; do not duplicate the same report in each
phase. Preserve repo-required QA records and evidence files as linked artifacts.
Record accepted scope/exclusions, acceptance IDs, current phase, exact repos and
refs/SHAs, local integration targets, resolved deployment identities, authority
and its user source, dependencies, scheduled gates, commands/results, decisions,
fixture cleanup, remaining blockers, and next action. Resume from the first
incomplete gate after rechecking mutable state. Reuse unaffected proof.

## Worktree ownership and release lifecycle

Follow the shared [repository worktree lifecycle contract](../../repo-worktree-lifecycle/references/operating-contract.md)
for every repository. Build-it keeps one task-owned batch worktree per affected
repository and reuses it across items sequentially. Independent tasks may use
separate worktrees and branches in parallel; integration and publication to a
shared release ref are serialized. Collapse into a clean, current-base local
integration worktree when the primary checkout is dirty or divergent. This is an
intermediate integration lane. Before the build is complete, synchronize the
canonical local development branch used for future feature bases, then validate
and record that exact branch head. It remains separate from the mapped remote
release ref used for deployment.

Keep each worktree classified as active, handed off, integrated, preserved, or
removed in the canonical ledger. Before build-it completes, reconcile accepted
work to the canonical local development branch and mapped remote release ref,
report their separate SHAs, the exact deployed revision, and all gates, then
remove only task-owned worktrees whose changes are preserved and whose cleanup
is safe. If the canonical branch is dirty, divergent, or contains unclassified
commits, preserve it and leave synchronization pending; keep the execution goal
open with an exact owner and resume action. Do not call the feature closed or
start the next feature from that stale base.

## Plan the release before building

Resolve the actual release path and live topology before topology-dependent
implementation: database sharing, all affected deployed consumers and revisions,
provider identities, exact case-sensitive remote refs, and component order.
During planning, read the shared
[project deploy-path skill](project-release-adapter.md) and its route
directory for every repository/component; recheck the route and current
registries before deployment. Follow the named project skill and repository
runbook. Record each route's source, release ref, deploy trigger, provider
identity source, and proof requirements in the canonical ledger.
Registry and branch contents are clues, not proof of the deployed revision.
Discover approved authentication, fixtures, provider access, and existing test
spending limits early. Do not print secrets or create credentials. Unknown
topology blocks dependent writes, not independent local implementation.

For each acceptance criterion, assign isolated-worktree, integrated-local,
deployed-runtime, and provider/UI proof as applicable. Identify which checks
truly must pass before integration and which depend on the planned deployment.

## Decisions owned by the agent

Choose the smallest maintainable, reversible approach consistent with accepted
behavior and existing project patterns. Ordinary supporting work includes
compatibility adapters, environment-scoped activation, repo-native dependency
setup, bounded fixture/harness repairs, and required release wiring. It must be
necessary to the feature, tested, and confined to authorized systems and data.
Prefer existing mechanisms; do not introduce a new platform or duplicate shared
infrastructure merely to avoid asking a question. Record consequential choices
and evidence, then proceed; routine choices do not need approval round trips.

Build-it is not approval for new purchases, subscriptions, credit economics,
permission expansion, persistent access, customer messages, destructive data
work, or an additional deployment environment. For paid provider tests, use a
verified existing user-approved test allowance and enforce its cost/call cap.
If no allowance covers a required paid action, prepare a minimal bounded canary
and ask only for that allowance. Credentials alone do not authorize spending.

## Separate preparation from activation

For shared catalogs, schemas, flags, and services, inspect all affected consumers.
Prefer backward-compatible schema preparation, inactive data/configuration,
compatible code deployment, then activation limited to the authorized target.
A Dev rollout must not silently expose new behavior to production consumers.
Isolation must hold at backend selection/execution and persisted-state boundaries,
not just in UI visibility. A global enabled flag or a tenant shared with production
does not establish environment isolation. Prove isolation and old-code compatibility
with negative tests and live configuration checks before shared writes.

Autonomously implement this staging when safely achievable within scope. If it
requires production code promotion, a new infrastructure boundary, unapproved
access, or altered product behavior, escalate that specific decision instead.

An operation may be `scheduled` after deployment only when the ledger names its
exact target/operation, compatibility evidence, prerequisite revision, execution
phase, verification, and disable/forward-fix path. Before integration, prove the
unactivated feature is safe, old and new code tolerate the intermediate state,
and every current-phase assertion passes. Never schedule a schema prerequisite
past the first runtime that needs it. Schema preparation that is safe and required
now must still be applied under existing authority; scheduling is not deferral
for convenience. Standalone local finish-line authority remains unchanged.

Worktree tests, prep-collapse, and local collapse may pass their phase with these
explicit future activation/hosted gates. Retain task-owned worktrees or artifacts
needed for release and recovery; cleanup is not a prerequisite to deployment.
Execute all scheduled operations and required proof at their assigned phases.
The feature is not complete or release-ready while any required gate is pending.

## Repair before escalation

Before asking, identify the exact blocked operation and boundary; perform safe
read-only checks and evaluate practical in-scope alternatives. Repair routine
engineering/harness/release defects, rerun affected checks, and continue. Do not
ask merely because work is dirty, a dependency is missing, a migration is shared,
or a child skill reached its standalone completion sentence.

Keep dependency-blocked lanes blocked while completing independent authorized
work. A child blocker does not invoke pause or end the entire build automatically.
When no safe progress remains, stop with the exact evidence, preserved state,
recommended solution, and only the missing decision/access/authority. Do not
perform risky trial writes or three retries of a known authority failure.
For technical failures, use the parent's bounded hypothesis-driven repair limit;
do not weaken assertions or bypass auth, protected branches, or release gates.
User stop/pause and explicit limits take effect immediately.

## Evidence reuse and phase cost

Assign each acceptance assertion a phase and proof boundary. Each result records
acceptance ID, command/test, relevant code state (SHA plus scoped dirty diff),
environment, effective runtime/configuration, fixture context, outcome and evidence
path. Reuse it only when those relevant conditions are unchanged. A phase change
alone does not invalidate proof. A merge, configuration/fixture change or deployment
requires checking which assertions it invalidates; do not blindly rerun everything.
Required repository CI and explicit user-requested fresh checks still run.

Worktree proof never stands in for integrated-runtime or hosted proof. Integrated
checks establish merge/routing compatibility on the actual integrated checkout;
hosted checks establish the feature on the released revision. Reuse checks already
performed on the same unchanged boundary. Keep failures and missing proof visible.

Read the ledger and user corrections after its checkpoint before older history.
Recover targeted history when requirements are missing, disputed or stale. Load
only the current phase's dependencies and provider references; do not re-read an
unchanged contract retained in context. Child results update the ledger with phase,
changed acceptance IDs, evidence, blockers and next action, not full repeated reports.
Do not change task titles for routine build-it phase transitions; preserve the
user's chosen title and priority. Standalone metadata behavior remains unchanged.

Apply the parent's economic context budget to coordinator and worker lifetimes;
window availability and cache hits do not waive it. Batch independent read-only
operations, keep long output in files, and do not add unchanged status-poll turns.
Context refresh preserves the same scope, worktree, valid evidence, scheduled
gates and cumulative attempts. Record worker replacement IDs and the next pending
gate; do not reopen passed phases solely to rebuild a fresh chat's history.
