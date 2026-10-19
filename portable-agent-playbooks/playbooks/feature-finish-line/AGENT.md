# Feature Finish Line Agent Playbook

This is a platform-neutral version of the `feature-finish-line` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Finish accepted feature work with meaningful coverage, required data gates, QA records and docs. Marketing is opt-in; full-app testing is separate.

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


# Feature Finish Line

## When called by build-it

Inside a user-authorized build-it execution, read and apply the [shared build-it execution contract](../build-it/references/execution-contract.md) before acting. Its phase scheduling and handoffs qualify this skill's standalone rules; the parent owns phase transitions. Outside build-it, preserve this skill's standalone behavior. Higher-priority instructions, user limits, safety boundaries, and tool-required confirmations remain in force.

Under build-it, phase readiness is distinct from final release readiness. The
contract's tightly bounded scheduled-activation exception applies to the mandatory
database completion gate and pre-integration finish requirements below. Complete
all safe prerequisites needed now; never claim final completion until scheduled
activation and required hosted/provider proof are executed. Update the shared
ledger and link existing QA/docs artifacts instead of duplicating reports.
Use only authority established for the current task; this public template provides no standing project permissions.

Use this skill after implementation work appears mostly complete and the user wants the feature hardened, verified, documented, and locally finished.

## Operating Contract

Finish the accepted scope with meaningful regression coverage, a per-issue test ledger, durable QA specifications, documentation and focused validation. Read the generic catalog adapter in `references/qaqc-catalog-adapters.md` for persistence.

Inherit the current task authority and preserve exact target and operation boundaries. Local finishing does not authorize deployment, shared-data writes, provider or billing changes, permission expansion or external messages. Prepare required external operations, verify their compatibility and exact target, execute only when authorized, and retain readback evidence. A missing data or runtime gate remains blocked.

## Mandatory Database Completion Gate

1. Inventory required migrations, schemas, seeds, catalog definitions and backfills.
2. Verify the exact canonical target and compare its ledger and live catalog with local migrations.
3. Review destructive effects, locks, tenant isolation, permissions and old/new code compatibility.
4. Execute only operations authorized for the current task; use the smallest bounded change.
5. Verify applied revisions and postconditions through readback. Preserve pending operations and
   missing authority as explicit blockers rather than claiming feature completion.

## Finish-Line Sequence

Use this sequence as the high-level completion order. The detailed workflow below explains how to execute each step safely.

1. Verify feature is complete.
2. Run focused feature QA/regression checks; leave full-app testing to a separate request.
3. Confirm acceptance criteria are met.
4. Apply and verify every required safe database migration and bounded data setup.
5. Create or update atomic QA/QC catalog records for every finished feature or bug.
6. Update documentation/changelog.
7. Generate release notes when appropriate, otherwise mark deferred or not applicable.
8. Generate social copy only when requested, otherwise mark not applicable.
9. Generate/reuse marketing assets only when requested, otherwise mark not applicable.
10. Bundle all generated assets for review.
11. Mark feature ready for release.

Marketing assets and promotional/social copy are opt-in deliverables. A customer-facing
release candidate alone does not request collateral. Preserve required project
changelog/release documentation, QA records and runtime proof. When requested,
use the approved branding and the instructions below; do not publish or send
without the user's delivery authorization.

Do not generate duplicate marketing assets. When marketing is applicable, first
run `<agent-config>/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"`
from the relevant repo. Reuse the existing package when found. Only run
`marketing-asset-generation` when no package exists or the user explicitly asks
for fresh assets.

Every finish-line report must include completed/incomplete state for each sequence step. If the code is release-ready but marketing assets are blocked, say that explicitly instead of marking the whole sequence complete.

## Detailed procedures

For implementation/test-harness gaps, QA catalog writing, rollout operations or
an explicitly requested release package, read the relevant numbered section of
[detailed procedures](references/detailed-workflow.md). Its sections cover inventory,
coverage, catalog, rollout, local fixes, docs and requested collateral. For a clean
completion pass, reconcile the existing ledger under the contracts above; do not
load the full procedure or repeat valid checks. Normal required CI remains mandatory.

## Standard Closing Shape

End with a concise handoff:

- Files changed.
- Tests and checks run.
- Feature test coverage added or confirmed, including the exact behavior asserted.
- Finish-line coverage ledger: every issue/behavior mapped to exact automated tests, with the direct command and full-suite command that exercise each test.
- QA/QC catalog records: every issue/behavior mapped to a created, updated, unchanged, or pending-import specification with the project record ID, stable key/identity, local file, database/dashboard sync state, and validation evidence; include exact `check_id` and `coverage_key` for example-project-12.
- Local/browser verification performed.
- Docs updated, including shared docs status.
- Release notes/social copy prepared or explicitly marked not applicable.
- Marketing assets reused/generated, including package path and manifest path, or blocker.
- Finish-line sequence status: completed/incomplete state for verify, QA/regression, acceptance criteria, required database migrations/data setup, QA/QC catalog records, docs/changelog, release notes, social copy, marketing assets, bundled handoff, and release readiness.
- Migration/env/provider/billing/webhook/queue/job/seed/backfill/deploy readiness, breaking-change review, exact canonical database target, remote migration-ledger comparison, operations applied, and post-condition proof.
- Remaining blockers or follow-ups.

If everything is locally complete, say so directly. Do not imply production readiness unless production or deployment validation actually ran.
