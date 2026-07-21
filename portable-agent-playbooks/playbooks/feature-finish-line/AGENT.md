# Feature Finish Line Agent Playbook

This is a platform-neutral version of the `feature-finish-line` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use after a planned feature build or implementation completes and the user wants the finishing pass: add missing deterministic and computer-use/browser tests, run focused feature validation, finish remaining polish, identify blockers, complete safe local execution, review needed migrations/deploy steps, update repo/shared docs, prepare release notes, and generate or reuse Bonfire marketing assets. Full-app/full-suite testing is separate and only runs when explicitly requested.

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

Assume local finishing work is allowed. A request to use this finish-line skill is also standing approval to complete the non-deployment work that is required to make the feature actually work, after the safety review below is clean. Do not stop for a second manual approval merely because the remaining work includes database migrations, schema updates, non-destructive data upserts/seeds/backfills, environment-variable additions, queue/job setup, webhook/provider configuration, billing product/price/link configuration, or other external integration setup needed by the feature.

Finish-line must leave behind real automated coverage for the feature. A feature is not finished if the only validation is manual clicking, source-text assertions, screenshots, a build, lint, or a public-page smoke check. Every invocation must either add or identify already-existing executable tests that directly exercise the new user-visible behavior, API contract, state transition, data persistence, or regression risk. If no meaningful automated test can be added because of missing credentials, missing harness support, external service limitations, or product ambiguity, record that as a blocker and propose the smallest harness/test-account change required. Do not report the feature as fully finished while that test gap remains.

Run focused tests that directly exercise the feature and its specific regression risks. Do not automatically run the repository-wide/full-app suite, broad cross-browser matrix, or unrelated regression inventory as part of finish-line. `full-suite-tests` or another explicit full-app testing request executes those broader gates. If focused validation cannot run, report the authored coverage as unverified rather than passed.

Finish-line must build an explicit issue-to-test coverage ledger. For every bug, feedback item, acceptance criterion, regression, user report, or behavior changed during the feature, list the issue, the failure mode/root cause, the executable test(s) that would fail if it regressed, and the suite command that runs those tests. Do not collapse several unrelated bugs into one vague "covered by e2e" claim. If one test covers multiple issues, name each issue and the exact assertion that covers it. If an issue is intentionally not covered, mark it as a blocker or residual risk and explain the smallest practical test/harness change needed.

Finish-line must also make the coverage ledger consumable by any later `full-suite-tests` run. The final report must include a "Finish-line coverage ledger" section with exact test file paths, test names or grep patterns, and required commands. When `full-suite-tests` is run afterward, those tests are mandatory in-scope checks and must pass or be explicitly marked blocked; they cannot be skipped merely because the broader suite has other smoke coverage.

Do not push, merge, deploy to dev, deploy to production, change branch protections, or promote traffic unless the user explicitly asks for that deployment/promotion action in the current conversation. Finish-line approval covers preparation and required non-deployment mutations, but not dev/prod application deployment.

Before running any migration, cloud database mutation, live data operation, environment update, provider setup, billing change, webhook change, queue/job change, or other external mutation, inspect the exact diff/operation and report whether it can break existing data, API contracts, auth/permissions/RLS, env requirements, background jobs, billing, external integrations, or production user flows. If the review finds no plausible breaking-change risk, execute the smallest necessary non-deployment step and verify it. If the review finds plausible breakage, destructive data loss, customer-impacting ambiguity, or an unclear target environment/account, stop and ask for a rollout decision.

This standing approval does not waive exact approval requirements for database permissions, grants, roles, ownership, RLS policies, object owners, destructive production data changes, or sending real external messages to customers unless those actions are specifically named in the current request. If those appear necessary, stop and ask for exact approval.

If a safe local or live non-deployment fix is needed and it is unlikely to cause breaking changes, make the fix and rerun only the affected focused validation. If the fix would change product direction, data contracts, permissions/RLS/ownership, or customer-facing external behavior beyond the accepted feature scope, stop and report it as a remaining decision item.

## Finish-Line Sequence

Use this sequence as the high-level completion order. The detailed workflow below explains how to execute each step safely.

1. Verify feature is complete.
2. Run focused feature QA/regression checks; leave full-app testing to a separate request.
3. Confirm acceptance criteria are met.
4. Update documentation/changelog.
5. Generate release notes.
6. Generate suggested social copy.
7. Generate marketing assets.
8. Bundle all generated assets for review.
9. Mark feature ready for release.

Marketing assets step: create persona-specific promotional graphics, feature screenshots, headlines, subtitles, and launch-ready assets using Bonfire branding.

Do not generate duplicate marketing assets. Before creating a new package, run `<agent-config>/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"` from the relevant repo. Reuse the existing package when found. Only run `marketing-asset-generation` when no package exists or the user explicitly asks for fresh assets.

Every finish-line report must include completed/incomplete state for each sequence step. If the code is release-ready but marketing assets are blocked, say that explicitly instead of marking the whole sequence complete.

## Workflow

1. Preflight the repo state.
   - Run `git status --short --branch`.
   - Identify the active repo, branch, changed files, and any unrelated dirty work.
   - Do not revert user changes. Work around unrelated dirt unless it blocks validation.

2. Understand the feature.
   - Read relevant diffs, commits, tests, docs, route files, components, or service modules.
   - Infer the expected behavior from the current thread and implementation.
   - Build an initial issue/behavior inventory from the user request, screenshots, videos, bug reports, acceptance criteria, code diffs, and prior failures. Treat each distinct reported symptom as its own coverage item until proven to share the same root cause.
   - If the intended behavior cannot be inferred safely, ask one concise question.

3. Identify the validation surface.
   - Deterministic checks: unit tests, integration tests, API tests, lint, typecheck, build, migrations/schema checks, or repo-specific scripts.
   - Computer-use/browser checks: real UI flows, local app behavior, screenshots, console/network errors, auth flows, mobile/responsive checks, or end-to-end happy paths.
   - Prefer existing repo test patterns and runbooks over inventing new harnesses.
   - For web/app features, include at least one test that executes the actual workflow through a browser or equivalent integration boundary unless the feature is purely internal and has no user path.
   - For authenticated features, coverage must authenticate with an approved test user/session or explicitly mark authenticated coverage blocked; public-only checks do not satisfy finish-line coverage for authenticated features.
   - For every inventory item, name the smallest executable test level that can catch it quickly and the broader suite that will catch it before release. Examples: deterministic API payload test + browser workflow test; component state test + authenticated end-to-end flow; migration/schema test + hosted canary.
   - Verify the planned tests are included in normal suite commands. If a focused test is not reached by the repo's deterministic, browser, predeploy, or full-suite commands, either add it to the normal suite configuration or record a blocker that full-suite cannot currently enforce the regression.

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

6. Review rollout and migration safety.
   - Identify any migrations, schema/type changes, seed/backfill scripts, env changes, deploy steps, queues/jobs, or provider credentials needed for the feature to actually work after code merge.
   - For every migration, inspect the exact SQL or migration code for destructive operations, table rewrites, enum/check changes, locking risk, backfill behavior, tenant isolation, RLS/policy/grant/ownership changes, indexes, rollback/forward-fix path, and compatibility with currently deployed code.
   - For every required non-deployment external change such as env vars, cloud database migrations, seed/upsert/backfill scripts, billing products/prices/links, webhooks, queue/job setup, provider config, or one-off operational commands, inspect the exact command/payload first, then run it when the safety review is clean. The finish-line invocation is sufficient approval for these clean, required completion steps.
   - For every deploy step, check compatibility between old code/new schema and new code/old schema, required env vars, feature flags, worker/job order, external provider scopes, and smoke-test plan.
   - Do not deploy to dev or production merely because deployment is needed; deployment always requires explicit current-turn approval naming the deployment target.
   - If applying an approved migration, env update, provider setup, billing setup, webhook setup, queue/job setup, seed, backfill, or other non-deployment operation, run the smallest scoped command, capture durable evidence, and verify the post-condition without printing secrets.

7. Finish remaining polish and test wiring.
   - Fix local issues discovered during implementation review when the fix is within the feature scope and low risk.
   - Add regression coverage for each fix and rerun only the affected focused tests.
   - Keep edits scoped to the implementation, test harness, and relevant docs.

8. Execute remaining safe local tasks.
   - Run any local setup, generation, migrations, seed commands, or data backfills only when they are clearly local and reversible.
   - Run required non-deployment shared cloud, production, paid-service, billing, webhook, database, env, seed, or backfill operations after the safety review is clean; finish-line invocation supplies the required approval. Stop only for deployment, unclear target/account, plausible breaking change, destructive data risk, exact permissions/RLS/ownership changes, or real customer messaging that was not specifically named.

9. Document the change.
   - Update repo-local docs when the behavior, setup, testing, API contract, runbook, or user workflow changed.
   - Update the project shared docs repo when applicable. Locate it from the prompt, sibling directories, git remotes, or established repo conventions such as `*_shared_docs`, `*-shared-docs`, or `shared-docs`.
   - If shared docs are not applicable or cannot be located, say that clearly.
   - Update changelog or release-note source artifacts when the repo has a maintained release-note path and the feature is ready for that surface.

10. Prepare release notes, social copy, and marketing assets.
   - Generate release-note draft material after validation and live-status classification. Keep production/public release notes unpublished unless production-live proof exists and the user has requested publication through the release workflow.
   - Include feature summary, what changed, why it matters, who benefits, screenshots, customer-facing announcement copy, suggested social copy, internal support/sales notes, QA status, known limitations, and links to generated assets.
   - Use `bonfire-feature-release-update` for team-facing release notes when the user asks for a release/update package, delivery, ClickUp post, group text, or production update-log entry. Pass along any marketing asset package path or `asset-manifest.json` found or created in this finish-line run so release notes reuse those assets.
   - Use `marketing-asset-generation` after validation and live-status classification to create or reuse persona-specific promotional images without overstating deployment status.
   - First run `<agent-config>/skills/marketing-asset-generation/scripts/find_marketing_asset_package.py --feature-name "<Feature Name>"` from the relevant repo. If it finds an `asset-manifest.json`, reuse that package and include its path in the handoff.
   - If no package exists, run the Marketing Asset Generation workflow to create the local package. If image generation is unavailable, include prompts and mark image rows as `planned`, `failed`, or `blocked` instead of pretending assets were generated.
   - Bundle release-note drafts, social copy, screenshots, marketing asset package paths, and generated/reused asset links/files in the final feature handoff.
   - Do not upload assets, post externally, publish release notes, or send customer-facing announcements unless the user explicitly asks for that delivery action.

11. Report what remains.
   - Separate completed work, tests run, local verification, remaining blockers, optional follow-ups, and items needing user/product/deploy/credential approval.
   - Include a rollout section that states whether migrations, env updates, provider setup, billing setup, webhooks, queues/jobs, seeds/backfills, or deploys were needed, whether breaking-change review passed, exactly what was or was not executed, and what live verification proved.
   - Include a "Feature test coverage" line naming the exact test(s) added or reused for the feature, what behavior they assert, and whether authenticated/deployed coverage is complete or blocked.
   - Include a "Finish-line coverage ledger" section with one row per issue/behavior: issue title, root cause or failure mode, test file, test name/grep pattern, command that runs it directly, broader suite command that includes it, and current status.
   - Include a "Finish-line sequence status" section with one row for each of the 9 high-level steps: completed, incomplete, blocked, or not applicable, plus evidence or artifact path.
   - Include a "Marketing assets" section with reused/generated package path, asset manifest path, persona image statuses, screenshots, social copy status, and any blocked asset-generation reason.
   - Explicitly state whether the repo's full-suite definition now exercises every finish-line ledger test. If not, list exactly which tests are missing from full-suite and do not call the finish-line complete until that is fixed or blocked.
   - Be explicit about anything not run and why.

## Standard Closing Shape

End with a concise handoff:

- Files changed.
- Tests and checks run.
- Feature test coverage added or confirmed, including the exact behavior asserted.
- Finish-line coverage ledger: every issue/behavior mapped to exact automated tests, with the direct command and full-suite command that exercise each test.
- Local/browser verification performed.
- Docs updated, including shared docs status.
- Release notes/social copy prepared or explicitly marked not applicable.
- Marketing assets reused/generated, including package path and manifest path, or blocker.
- Finish-line sequence status: completed/incomplete state for verify, QA/regression, acceptance criteria, docs/changelog, release notes, social copy, marketing assets, bundled handoff, and release readiness.
- Migration/env/provider/billing/webhook/queue/job/seed/backfill/deploy readiness, breaking-change review, and any approved rollout actions performed.
- Remaining blockers or follow-ups.

If everything is locally complete, say so directly. Do not imply production readiness unless production or deployment validation actually ran.

