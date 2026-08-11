# Feature Finish Line Agent Playbook

This is a platform-neutral version of the `feature-finish-line` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use after a planned feature build or implementation completes and the user wants the finishing pass: add missing deterministic and computer-use/browser tests, run focused feature validation, apply and verify required safe database migrations and non-destructive data setup including Bonfire's canonical unified production database, write or update atomic QA/QC catalog records, finish remaining polish, update docs, prepare stage-appropriate release artifacts, and reconcile local/merged/hosted/provider/production truth. Full-app/full-suite testing is separate and only runs when explicitly requested.

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

# Feature Finish Line

Use this skill after implementation work appears mostly complete and the user wants the feature hardened, verified, documented, and locally finished.

## Operating Contract

Assume local finishing work is allowed. Invoking this skill is also explicit
standing approval to complete required safe non-deployment work after the safety
review below is clean. Inherit the current task's prep/build approval register;
do not invent a new provider account, billing target, or unrelated data target.

Treat required database completion as part of the feature, not as release
preparation. This invocation explicitly authorizes applying additive,
backward-compatible migrations and required bounded non-destructive
upserts/seeds/backfills to the project's canonical database even when that
database is production or shared with production. For Bonfire, assume the
canonical unified Supabase database is the required target when repo/shared docs,
environment configuration, and the remote migration ledger agree. An application
label such as local or Dev does not create a separate Bonfire database.

This authority covers only operations required for the accepted feature or its
QA/QC runtime and only after exact target resolution, migration review, and
compatibility checks. It does not authorize grants, roles, ownership, RLS/policy
changes, object-owner changes, destructive data changes, unbounded rewrites,
billing changes, persistent access creation, application deployment, or unrelated
production-data cleanup.

Do not call a feature finished, fully functional, release-ready, or merely
"pending migration" while a required safe migration or bounded data setup remains
unapplied. Apply it, verify the remote ledger and live schema/data post-condition,
and rerun the affected feature checks. If a stricter gate blocks it, mark the
finish line incomplete and name the exact blocked operation.

Finish-line must leave behind real automated coverage for the feature. A feature is not finished if the only validation is manual clicking, source-text assertions, screenshots, a build, lint, or a public-page smoke check. Every invocation must either add or identify already-existing executable tests that directly exercise the new user-visible behavior, API contract, state transition, data persistence, or regression risk. If no meaningful automated test can be added because of missing credentials, missing harness support, external service limitations, or product ambiguity, record that as a blocker and propose the smallest harness/test-account change required. Do not report the feature as fully finished while that test gap remains.

Run focused tests that directly exercise the feature and its specific regression risks. Do not automatically run the repository-wide/full-app suite, broad cross-browser matrix, or unrelated regression inventory as part of finish-line. `full-suite-tests` or another explicit full-app testing request executes those broader gates. If focused validation cannot run, report the authored coverage as unverified rather than passed.

Finish-line must build an explicit issue-to-test coverage ledger. For every bug, feedback item, acceptance criterion, regression, user report, or behavior changed during the feature, list the issue, the failure mode/root cause, the executable test(s) that would fail if it regressed, and the suite command that runs those tests. Do not collapse several unrelated bugs into one vague "covered by e2e" claim. If one test covers multiple issues, name each issue and the exact assertion that covers it. If an issue is intentionally not covered, mark it as a blocker or residual risk and explain the smallest practical test/harness change needed.

Finish-line must also make the coverage ledger consumable by any later `full-suite-tests` run. The final report must include a "Finish-line coverage ledger" section with exact test file paths, test names or grep patterns, and required commands. When `full-suite-tests` is run afterward, those tests are mandatory in-scope checks and must pass or be explicitly marked blocked; they cannot be skipped merely because the broader suite has other smoke coverage.

Finish-line must also create or update the durable QA/QC catalog specification for every independently testable feature, bug fix, or regression completed by the work. Use `$qaqc-record-upsert` when available; otherwise read [references/qaqc-catalog-adapters.md](references/qaqc-catalog-adapters.md) completely. Use the project’s own schema, identity convention, fixtures, writer, and validation workflow. For Bonfire, also read [references/qaqc-catalog-write.md](references/qaqc-catalog-write.md) completely for its exact paths, fields, fixture aliases, and Supabase boundary. Update an existing stable behavior instead of duplicating it, create separate records for unrelated behaviors, and always leave a durable local or import-ready record. A catalog record tells QA what to test and what success means; it is not evidence that any environment passed.

Do not push, merge, deploy to dev, deploy to production, change branch
protections, or promote traffic without exact task-scoped approval naming the
repo, target environment, and branch/SHA when relevant. Preserve that approval
across `$continue` only while the target and deployable change remain materially
the same. Finish-line approval covers preparation and inherited authorized
non-deployment work, but not application deployment.

Before running any migration, cloud database mutation, live data operation, environment update, provider setup, billing change, webhook change, queue/job change, or other external mutation, inspect the exact diff/operation and report whether it can break existing data, API contracts, auth/permissions/RLS, env requirements, background jobs, billing, external integrations, or production user flows. If the review finds no plausible breaking-change risk, execute the smallest necessary non-deployment step and verify it. If the review finds plausible breakage, destructive data loss, customer-impacting ambiguity, or an unclear target environment/account, stop and ask for a rollout decision.

This standing approval does not waive exact approval requirements for database
permissions, grants, roles, ownership, RLS policies, object owners, destructive
production data changes, or sending real external messages to customers. A
still-valid exact approval inherited in the task approval register is
sufficient; do not require it to be restated merely because finish-line was
invoked. If no valid exact approval exists, stop and ask for one.

Safe required migrations and bounded feature-specific non-destructive data setup
on the canonical production/shared-production database are already approved by
this invocation. Other production-data mutations, billing or paid-service
changes, provider-account access changes, persistent OAuth/API credential
creation, and deployment still require exact approval. Tool-required action-time
confirmation still applies even when the broader workflow was approved earlier.
Prepare the exact operation first and ask only when the gated final action is
next.

## Mandatory Database Completion Gate

Run this gate for every feature, including features that appear UI-only:

1. Inventory every migration, schema change, seed, catalog definition, and
   backfill introduced or required by all repos in feature scope.
2. Resolve the canonical database target from repo config, shared docs, platform
   project/reference, and the remote migration ledger. For Bonfire, prefer the
   established unified Supabase project; never create or assume a separate local,
   Dev, or production database without evidence.
3. Compare the ordered local migration set with the remote ledger and inspect the
   live catalog for drift. A file existing in Git is not proof it ran.
4. Review each pending operation for destructive SQL, table rewrites, locks,
   enum/check narrowing, nullability changes, backfill bounds, tenant isolation,
   RLS/grants/ownership, old-code/new-schema compatibility, new-code/old-schema
   compatibility, and a rollback or forward-fix path.
5. If the operation is additive/backward-compatible, bounded, non-destructive,
   feature-required, and contains no separately gated permission/RLS/ownership
   change, apply it to the canonical database using the repo's standard migration
   workflow. Do not stop to ask again merely because the target is production or
   shared with production.
6. Verify the remote migration ledger, expected tables/columns/indexes/rows or
   definitions, tenant-scoped readback, and absence of partial application. Do
   not treat CLI exit zero, HTTP 200, or a queued operation as terminal proof.
7. Rerun the smallest affected API/integration/browser test against the migrated
   database or authenticated app path. Record migration filenames/IDs, target
   project/reference, tool/command, timestamp, post-condition evidence, and any
   cleanup or forward-fix state without exposing secrets.
8. If a migration is destructive, ambiguous, permission/RLS/ownership-changing,
   unbounded, incompatible with deployed code, or aimed at an unresolved target,
   stop only that lane, present the exact operation and risk, and request the
   missing decision. Continue other finish-line work, but keep release readiness
   incomplete.

If a safe local or live non-deployment fix is needed and it is unlikely to cause breaking changes, make the fix and rerun only the affected focused validation. If the fix would change product direction, data contracts, permissions/RLS/ownership, or customer-facing external behavior beyond the accepted feature scope, stop and report it as a remaining decision item.

## Finish-Line Sequence

Use this sequence as the high-level completion order. The detailed workflow below explains how to execute each step safely.

1. Verify feature is complete.
2. Run focused feature QA/regression checks; leave full-app testing to a separate request.
3. Confirm acceptance criteria are met.
4. Apply and verify every required safe database migration and bounded data setup.
5. Create or update atomic QA/QC catalog records for every finished feature or bug.
6. Update documentation/changelog.
7. Generate release notes when appropriate, otherwise mark deferred or not applicable.
8. Generate suggested social copy when appropriate, otherwise mark deferred or not applicable.
9. Generate/reuse marketing assets when applicable, otherwise mark deferred or not applicable.
10. Bundle all generated assets for review.
11. Mark feature ready for release.

Marketing assets step: for a customer-facing release candidate, create
persona-specific promotional graphics, feature screenshots, headlines,
subtitles, and launch-ready assets using the project’s approved branding. Use Bonfire branding only for Bonfire work. For internal,
infrastructure, or technically blocked work, mark this step deferred/not
applicable unless the user explicitly requests collateral.

Do not generate duplicate marketing assets. When marketing is applicable, first
run `<agent-config>/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"`
from the relevant repo. Reuse the existing package when found. Only run
`marketing-asset-generation` when no package exists or the user explicitly asks
for fresh assets.

Every finish-line report must include completed/incomplete state for each sequence step. If the code is release-ready but marketing assets are blocked, say that explicitly instead of marking the whole sequence complete.

## Workflow

1. Preflight the repo state.
   - Run `git status --short --branch`.
   - Identify the active repo, branch, changed files, and any unrelated dirty work.
   - Fetch the intended target branch and prove the worktree descends from its
     current base before adding finish-line changes. If it does not, use a clean
     current-base worktree or explicitly isolate/port the stale-branch work.
   - Do not revert user changes. Work around unrelated dirt unless it blocks validation.

2. Understand the feature.
   - Read relevant diffs, commits, tests, docs, route files, components, or service modules.
   - Infer the expected behavior from the current thread and implementation.
   - Build an initial issue/behavior inventory from the user request, screenshots, videos, bug reports, acceptance criteria, code diffs, and prior failures. Treat each distinct reported symptom as its own coverage item until proven to share the same root cause.
   - If the intended behavior cannot be inferred safely, ask one concise question.

3. Identify the validation surface.
   - Deterministic checks: unit tests, integration tests, API tests, lint, typecheck, build, migrations/schema checks, or repo-specific scripts.
   - Computer-use/browser checks: real UI flows, local app behavior, screenshots, console/network errors, auth flows, mobile/responsive checks, or end-to-end happy paths.
   - For every browser failure, preserve the exact test identity, failure class,
     actionable assertion/error, bounded stack excerpt (or explicit unavailable
     reason), and artifact paths. Keep neighboring mapped test outcomes
     independent; never hand off only `Playwright failed` or `passed | failed`.
     Classify runner/auth/fixture/reporter failures before an attributable
     assertion as QA infrastructure blockers rather than product defects.
   - Prefer existing repo test patterns and runbooks over inventing new harnesses.
   - For web/app features, include at least one test that executes the actual workflow through a browser or equivalent integration boundary unless the feature is purely internal and has no user path.
   - For authenticated features, coverage must authenticate with an approved test user/session or explicitly mark authenticated coverage blocked; public-only checks do not satisfy finish-line coverage for authenticated features.
   - For every inventory item, name the smallest executable test level that can catch it quickly and the broader suite that will catch it before release. Examples: deterministic API payload test + browser workflow test; component state test + authenticated end-to-end flow; migration/schema test + hosted canary.
   - Verify the planned tests are included in normal suite commands. If a focused test is not reached by the repo's deterministic, browser, predeploy, or full-suite commands, either add it to the normal suite configuration or record a blocker that full-suite cannot currently enforce the regression.
   - Build a proof matrix with separate rows for local, committed/pushed/merged,
     hosted environment, shared database/provider configuration, authenticated
     provider-backed behavior, production deployment, and customer-visible
     release. Mark each `proved`, `blocked`, `not requested`, or `stale` with
     evidence.

4. Add missing tests.
   - Add focused deterministic coverage for the new behavior and important regressions.
   - Add computer-use/browser coverage when the feature has UI, routing, local runtime behavior, or an end-user workflow.
   - The new test must assert the feature's real outcome, not just that a page renders. Examples: request payload/response contract, saved data visible after navigation, sort/filter changes a request or result order, modal action sends/tracks the intended event, form submission reaches the intended endpoint, or a regression condition no longer occurs.
   - Prefer exercising the actual component/page/API through the project's normal test harness. Mock external dependencies only at service boundaries; do not mock away the feature behavior being verified.
   - If a deployed/live behavior depends on real auth, maps, payments, email, search, or third-party APIs, add a local deterministic/browser regression where possible and also add or update an environment canary/smoke that runs against the deployed target with safe test credentials.
   - Keep tests realistic and maintainable. Avoid brittle sleeps, broad snapshots, and duplicated fixtures.
   - Do not count source-code grep tests, snapshot-only tests, type-only checks, or route-inventory checks as the feature's required real test unless the feature itself is a static code-generation/routing contract.
   - Do not stop after adding a single happy-path test when the feature fixed multiple issues. Each distinct issue must have at least one direct assertion for the specific failure mode, such as Enter-key behavior, stale persisted state, exact payload defaults, mobile layout state, auth/session preservation, pagination/windowing, provider data completeness, or deployed-environment recovery.
   - Use realistic fixture scale and failure timing. If the reported bug involved large result sets, async suggestions, mobile state, stale local storage, pagination, retries, missing backend rows, or external-service delay, include fixture data or harness behavior that reproduces that pressure instead of relying on a one-record happy-path mock.
   - Add negative/regression assertions where useful: prove stale data is not sent, heavy records are not eagerly rendered, forbidden requests do not erase auth, unavailable suggestions do not fake success, or a "no results" state does not appear while a valid search is being resolved.
   - After adding tests, update the issue-to-test coverage ledger before focused validation and the later full-suite handoff so failures can be traced back to the reported symptoms.

5. Run focused feature validation and prepare the full-suite handoff.
   - Run the smallest deterministic, integration, browser/e2e, lint, typecheck, or smoke commands that directly exercise the feature and changed files.
   - Do not run the repository-wide/full-app suite, broad route inventory, broad cross-browser matrix, or unrelated test groups unless the user explicitly requests full-app testing.
   - Confirm by inspection that every test named in the coverage ledger is included in at least one normal broader suite command. If a test is absent from the broad suite, fix the suite wiring or mark finish-line incomplete.
   - Record the exact focused commands run and the broader suite command reserved for a later `full-suite-tests` request.
   - When the user later asks for `full-suite-tests`, the full-suite run must include every finish-line ledger test and report each as passed, failed, blocked, or not applicable for the requested environment.
   - Clearly distinguish focused tests executed during finish-line from broader tests reserved for a separate full-suite run.

6. Create or update the QA/QC catalog records.
   - Use `$qaqc-record-upsert` when available. If it is unavailable, read [references/qaqc-catalog-adapters.md](references/qaqc-catalog-adapters.md) completely. For Bonfire, also read [references/qaqc-catalog-write.md](references/qaqc-catalog-write.md) completely.
   - Locate the project QA catalog and search for each issue/behavior by its stable identity/key, interface/route/job/tool, feature wording, issue title, source path, and test name.
   - Update the existing record when it represents the same behavior; otherwise create one new atomic record per independently executable behavior.
   - Populate the project’s required ownership, surface, behavior, prerequisites/fixtures, deterministic input or prompt when applicable, test steps, success criteria, environment scope, safety classification, source evidence, and readiness status. Never impose non-applicable fixture categories or store secrets/environment credentials.
   - Make the smallest local source-of-truth edit and run the project’s schema, identity/uniqueness, controlled-vocabulary, source-reference, checksum, and secret validations.
   - If the project has no central catalog, create `output/qa/<feature-slug>-qaqc-record.json`. Treat this as valid local persistence unless the project requires a central dashboard/database import.
   - For Bonfire's unified database, treat validated additive QA/QC catalog upserts required by the current finish line as authorized non-destructive data setup. Apply them after target and schema verification unless a separately gated risk exists. For other projects, follow the project's canonical database boundary and the mandatory database completion gate.
   - Record each disposition as `created`, `updated`, `unchanged`, or `pending import`, including the project’s record ID/stable key, local file, database/dashboard sync state, and blockers. Use `pending import` only when a separately gated risk, unresolved canonical target, or unavailable project writer prevents the authorized import; never use it to defer an otherwise safe required Bonfire upsert.
   - Do not mark finish-line complete if a changed behavior has no durable local QA record or explicit pending-import artifact.

7. Review rollout and migration safety.
   - Identify any migrations, schema/type changes, seed/backfill scripts, env changes, deploy steps, queues/jobs, or provider credentials needed for the feature to actually work after code merge.
   - For every migration, inspect the exact SQL or migration code for destructive operations, table rewrites, enum/check changes, locking risk, backfill behavior, tenant isolation, RLS/policy/grant/ownership changes, indexes, rollback/forward-fix path, and compatibility with currently deployed code.
   - For every required non-deployment external change such as env vars, cloud database migrations, seed/upsert/backfill scripts, billing products/prices/links, webhooks, queue/job setup, provider config, or one-off operational commands, inspect the exact command/payload first. Apply required safe canonical-database migrations and bounded feature data setup under this skill's standing authority. Run other operations only when they fall inside the inherited approval register and the safety review is clean.
   - For every deploy step, check compatibility between old code/new schema and new code/old schema, required env vars, feature flags, worker/job order, external provider scopes, and smoke-test plan.
   - Do not deploy to dev or production merely because deployment is needed.
     Deployment requires an exact task-scoped approval naming the repo, target,
     and branch/SHA when relevant; re-confirm if those materially change.
   - If applying an approved migration, env update, provider setup, billing setup, webhook setup, queue/job setup, seed, backfill, or other non-deployment operation, run the smallest scoped command, capture durable evidence, and verify the post-condition without printing secrets.
   - Before env updates, determine whether the platform auto-deploys or restarts.
     Use a no-deploy option when available until deployment is explicitly
     authorized.
   - For persistent OAuth clients, API keys, service accounts, permissions, or
     representational communication, obey any action-time confirmation policy
     immediately before the final create/save/send action.

8. Finish remaining polish and test wiring.
   - Fix local issues discovered during implementation review when the fix is within the feature scope and low risk.
   - Add regression coverage for each fix and rerun only the affected focused tests.
   - Keep edits scoped to the implementation, test harness, and relevant docs.

9. Execute remaining safe local tasks.
   - Run any local setup, generation, migrations, seed commands, or data backfills only when they are clearly local and reversible.
   - Apply required safe migrations and bounded feature-specific data setup to
     the verified canonical database under the mandatory database completion
     gate, including Bonfire's unified production-connected database. Run other
     non-deployment operations only inside the inherited authorized target and
     approval register. Paid-service or billing changes, provider-account
     permissions, persistent access creation, and customer messaging remain
     separately gated. Continue other safe work while those lanes wait.

10. Document the change.
   - Update repo-local docs when the behavior, setup, testing, API contract, runbook, or user workflow changed.
   - Update the project shared docs repo when applicable. Locate it from the prompt, sibling directories, git remotes, or established repo conventions such as `*_shared_docs`, `*-shared-docs`, or `shared-docs`.
   - If shared docs are not applicable or cannot be located, say that clearly.
   - Update changelog or release-note source artifacts when the repo has a maintained release-note path and the feature is ready for that surface.
   - Find and reconcile any existing finish-line report before creating a new
     one. Update a current mutable report; create a new dated report only when
     the old artifact is historical or a new proof stage materially changed.

11. Prepare release notes, social copy, and marketing assets.
   - First classify the feature as customer-facing release candidate,
     customer-facing but technically blocked, internal-only, or infrastructure.
     Marketing assets are required only for a customer-facing release candidate
     or when the user explicitly requests them. Otherwise mark them deferred or
     not applicable instead of generating collateral by default.
   - Generate release-note draft material after validation and live-status classification. Keep production/public release notes unpublished unless production-live proof exists and the user has requested publication through the release workflow.
   - Include feature summary, what changed, why it matters, who benefits, screenshots, customer-facing announcement copy, suggested social copy, internal support/sales notes, QA status, known limitations, and links to generated assets.
   - Use the project’s feature-release/update workflow for team-facing release notes when the user asks for a package or delivery. For Bonfire, use `bonfire-feature-release-update` for ClickUp, group text, or production update-log requests. Pass along any marketing asset package path or `asset-manifest.json` found or created in this finish-line run so release notes reuse those assets.
   - When marketing is applicable, use `marketing-asset-generation` after validation and live-status classification to create or reuse persona-specific promotional images without overstating deployment status.
   - When marketing is applicable, first run `<agent-config>/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"` from the relevant repo. If it finds an `asset-manifest.json`, reuse that package and include its path in the handoff.
   - When marketing is applicable and no package exists, run the Marketing Asset Generation workflow to create the local package. If image generation is unavailable, include prompts and mark image rows as `planned`, `failed`, or `blocked` instead of pretending assets were generated.
   - Bundle release-note drafts, social copy, screenshots, marketing asset package paths, and generated/reused asset links/files in the final feature handoff.
   - Do not upload assets, post externally, publish release notes, or send customer-facing announcements unless the user explicitly asks for that delivery action.

12. Report what remains.
   - Separate completed work, tests run, local verification, remaining blockers, optional follow-ups, and items needing user/product/deploy/credential approval.
   - Include a rollout section that states whether migrations, env updates, provider setup, billing setup, webhooks, queues/jobs, seeds/backfills, or deploys were needed, whether breaking-change review passed, exactly what was or was not executed, and what live verification proved.
   - Include a "Feature test coverage" line naming the exact test(s) added or reused for the feature, what behavior they assert, and whether authenticated/deployed coverage is complete or blocked.
   - Include a "Finish-line coverage ledger" section with one row per issue/behavior: issue title, root cause or failure mode, test file, test name/grep pattern, command that runs it directly, broader suite command that includes it, and current status.
   - Include a "QA/QC catalog record" section with one row per issue/behavior: disposition, project record ID, stable key/identity, local catalog file, database/dashboard sync status, validation evidence, and remaining blocker. For Bonfire, report `check_id` and `coverage_key` explicitly.
   - Include a "Finish-line sequence status" section with one row for each of the 11 high-level steps: completed, incomplete, blocked, or not applicable, plus evidence or artifact path.
   - Include a "Marketing assets" section with reused/generated package path, asset manifest path, persona image statuses, screenshots, social copy status, and any blocked asset-generation reason.
   - Explicitly state whether the repo's full-suite definition now exercises every finish-line ledger test. If not, list exactly which tests are missing from full-suite and do not call the finish-line complete until that is fixed or blocked.
   - Include the proof matrix and the inherited approval register with secret
     names/status only. Do not collapse local, merged, hosted, provider-backed,
     production, and customer-visible truth into one readiness claim.
   - Record exact approvals as `action + repo + branch/SHA when relevant +
     environment + provider/account + exact operation or payload + approval
     evidence + status`, and note any invalidation or action-time gate.
   - Be explicit about anything not run and why.

## Standard Closing Shape

End with a concise handoff:

- Files changed.
- Tests and checks run.
- Feature test coverage added or confirmed, including the exact behavior asserted.
- Finish-line coverage ledger: every issue/behavior mapped to exact automated tests, with the direct command and full-suite command that exercise each test.
- QA/QC catalog records: every issue/behavior mapped to a created, updated, unchanged, or pending-import specification with the project record ID, stable key/identity, local file, database/dashboard sync state, and validation evidence; include exact `check_id` and `coverage_key` for Bonfire.
- Local/browser verification performed.
- Docs updated, including shared docs status.
- Release notes/social copy prepared or explicitly marked not applicable.
- Marketing assets reused/generated, including package path and manifest path, or blocker.
- Finish-line sequence status: completed/incomplete state for verify, QA/regression, acceptance criteria, required database migrations/data setup, QA/QC catalog records, docs/changelog, release notes, social copy, marketing assets, bundled handoff, and release readiness.
- Migration/env/provider/billing/webhook/queue/job/seed/backfill/deploy readiness, breaking-change review, exact canonical database target, remote migration-ledger comparison, operations applied, and post-condition proof.
- Remaining blockers or follow-ups.

If everything is locally complete, say so directly. Do not imply production readiness unless production or deployment validation actually ran.
