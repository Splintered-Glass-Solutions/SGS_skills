> Public template: example project paths, schemas and fixtures are illustrative.
> Resolve real bindings and current authority from private project configuration;
> examples confer no account, data-write, permission or deployment authority.
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
   - Use `$qaqc-record-upsert` when available. If it is unavailable, read [references/qaqc-catalog-adapters.md](qaqc-catalog-adapters.md) completely. For example-project-12, also read [references/qaqc-catalog-write.md](qaqc-catalog-write.md) completely.
   - Locate the project QA catalog and search for each issue/behavior by its stable identity/key, interface/route/job/tool, feature wording, issue title, source path, and test name.
   - Update the existing record when it represents the same behavior; otherwise create one new atomic record per independently executable behavior.
   - Populate the project’s required ownership, surface, behavior, prerequisites/fixtures, deterministic input or prompt when applicable, test steps, success criteria, environment scope, safety classification, source evidence, and readiness status. Never impose non-applicable fixture categories or store secrets/environment credentials.
   - Make the smallest local source-of-truth edit and run the project’s schema, identity/uniqueness, controlled-vocabulary, source-reference, checksum, and secret validations.
   - If the project has no central catalog, create `output/qa/<feature-slug>-qaqc-record.json`. Treat this as valid local persistence unless the project requires a central dashboard/database import.
   - For example-project-12's unified database, treat validated additive QA/QC catalog upserts required by the current finish line as authorized non-destructive data setup. Apply them after target and schema verification unless a separately gated risk exists. For other projects, follow the project's canonical database boundary and the mandatory database completion gate.
   - Record each disposition as `created`, `updated`, `unchanged`, or `pending import`, including the project’s record ID/stable key, local file, database/dashboard sync state, and blockers. Use `pending import` only when a separately gated risk, unresolved canonical target, or unavailable project writer prevents the authorized import; never use it to defer an otherwise safe required example-project-12 upsert.
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
     gate, including example-project-12's unified production-connected database. Run other
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
     Marketing assets and social/promotional copy are required only when the user
     explicitly requests those deliverables. Otherwise mark them not applicable.
   - Generate release-note draft material after validation and live-status classification. Keep production/public release notes unpublished unless production-live proof exists and the user has requested publication through the release workflow.
   - Keep required release documentation focused on changed behavior, validation and limitations. Include promotional copy, social copy, support/sales collateral and generated assets only in an explicitly requested package.
   - Use the project’s feature-release/update workflow for team-facing release notes when the user asks for a package or delivery. For example-project-12, use `example-project-12-feature-release-update` for ClickUp, group text, or production update-log requests. Pass along any marketing asset package path or `asset-manifest.json` found or created in this finish-line run so release notes reuse those assets.
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
   - Include a "QA/QC catalog record" section with one row per issue/behavior: disposition, project record ID, stable key/identity, local catalog file, database/dashboard sync status, validation evidence, and remaining blocker. For example-project-12, report `check_id` and `coverage_key` explicitly.
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
