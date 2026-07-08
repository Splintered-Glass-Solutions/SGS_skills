# Full Suite Tests Agent Playbook

This is a platform-neutral version of the `full-suite-tests` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Run or plan a repository's full test and QA suite for a named environment. Use when the user says "full-suite-tests in local", "full-suite-tests in dev", "full-suite-tests in prod", "run full suite in local/dev/prod", "full QA in dev", "test everything in prod", or similar environment-scoped full validation requests across any project.

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

# Full Suite Tests

Use this skill when the user asks for a full test or QA pass scoped to an environment such as `local`, `dev`, `staging`, `preview`, or `prod`.

## Contract

Treat "full suite" as the repo's broadest reasonable validation pass, not a single default test command, unless the repo clearly defines it that way. By default, "full suite" means both deterministic checks and computer-use/e2e/browser validation when the project has those tests or user-facing flows.

The suite breadth must not shrink because the target is `dev`, `staging`, `preview`, `prod`, or an app URL. The environment changes the base URL, credentials/session, deploy metadata, and safety posture; it does not change the obligation to run all automated suites and all relevant browser/API/manual coverage across the repo. If a suite cannot run safely against an environment, mark that exact suite blocked with the reason and continue with the remaining non-blocked suites. Do not silently replace authenticated app tests with public smoke tests.

For monorepos or repos with multiple apps/packages, "full suite" means the entire repository scope: all package/workspace test commands, all configured lint/type/build checks, all e2e/computer-use/browser suites, all API/integration suites, and all documented manual or smoke checklists that apply to the target environment. Do not limit execution to the currently edited app unless the user explicitly narrows the scope.

If a previous or current `feature-finish-line` run produced a finish-line coverage ledger, those tests are mandatory full-suite inputs. Before running broad validation, locate the ledger in the current thread, PR notes, QA doc, commit/PR description, or finish-line final report. Add every listed test file, test name/grep pattern, direct command, and broader suite command to the suite inventory. A full-suite run is not complete until every finish-line ledger test has passed in the requested environment's applicable suite, or is explicitly marked blocked/not applicable with a concrete reason. Do not assume a route smoke, lint, build, or unrelated e2e pass covers a ledger item unless the exact assertion/test from the ledger ran.

Mandatory orchestration and safe-run posture:

- Always use the `orchestrator-mode` and `agent-safe-run` skills before starting broad checks or running full-suite tests. Treat both as part of this skill, even when the user does not mention them separately.
- Keep the active thread as the orchestrator for decomposition, validation strategy, delegated evidence review, and final synthesis.
- Make an explicit delegation decision before broad execution. For broad, high-cost, multi-suite, browser-heavy, or log-heavy runs, normally launch bounded the agent subagents for independent discovery, coverage slices, or log reduction when the slices can stand alone. Skip subagents only for a concrete reason and state it.
- Minimize the agent token usage during test execution. Do not stream full test, build, browser, deploy, or CI logs into the chat.
- Redirect verbose command output to dated files under `/tmp` or the repo's documented QA output folder, then read only compact summaries, targeted failures, and short log tails.
- Prefer compact milestone updates over repeated progress narration. Report status changes and actionable failures, not unchanged polling output.
- Avoid watches, live monitors, broad process dumps, full artifact dumps, full Playwright traces, full screenshots lists, and repeated unchanged CI/status polling.
- Run one heavy suite/check at a time unless the commands are clearly lightweight and independent. Do not parallelize browser suites, builds, or broad test runs inside the agent runtime.
- Use bounded command output caps and avoid commands that print secrets, large env files, generated assets, coverage dumps, `.next`, `dist`, `node_modules`, or full `test-results` contents.
- Run the full discovered suite inventory for the requested environment. Stop only when a prerequisite blocker makes later checks invalid or unsafe, then record exactly which suites are blocked and continue with any independent suites that remain safe to run.
- Preserve durable evidence by writing or updating the repo's QA run log when the run is substantial, blocked, or browser/manual coverage was attempted.
- Treat failures as a bounded batch repair loop, not a one-shot report. Run the full discovered suite first, collect the complete failure set, fix failures together when they share a likely cause or can be handled in one local batch, verify the batch locally, deploy to the requested non-production target when hosted retesting requires it, then rerun the affected hosted suite inventory. Do not run a separate loop for each feature or each individual failure unless isolation is necessary for safety or diagnosis. Default cap: up to 5 full run/repair/local-verify/deploy/retest loops, or a lower cap if the user explicitly gives one. Stop earlier when all in-scope suites pass or the remaining failures are blocked by a reasonably insurmountable hurdle that needs human review, external access, third-party service recovery, credentials, billing/account intervention, production approval, or another outside step. Maintain a compact loop log.

Default meaning:

1. Discover the project's own definition of full validation.
2. Build a complete suite inventory for the repo before running: deterministic, build/type/lint, integration/API, browser/e2e/computer-use, environment canaries, and documented manual smoke checklists.
3. Run deterministic automated checks first.
4. Verify environment/deploy health for the requested target.
5. Establish an authenticated test session when the app has authenticated user-facing surfaces.
6. Run computer-use/e2e/browser/manual/API smoke or regression coverage when the app has user-facing surfaces.
7. Record every suite/check as passed, failed, blocked, skipped by explicit user scope, or not applicable.
8. Repair and retest failures in batches until the suite is green, the loop cap is reached, or only explicit external blockers remain.

If the environment is missing, ask for it before executing. If the environment is present, proceed using the rules below.

## Environment Mapping

Use the user's environment word as the target:

- `local`: current checkout/worktree, local services, local dev server, local or test database as documented.
- `dev`, `staging`, `preview`, `test`: hosted non-production deployment for the current project.
- `prod`, `production`: live production deployment.

Do not guess destructive permissions from the environment name. Read repo docs and config first.

## Discovery

Before executing, inspect only enough to find the canonical suite:

- QA docs: `docs/qa/`, `docs/testing*`, `TESTING.md`, `README.md`, release runbooks.
- Package/task files: `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `Makefile`, `justfile`, `pyproject.toml`, `pytest.ini`, `tox.ini`, `Cargo.toml`, `go.mod`, `.github/workflows/`.
- Existing scripts containing `test`, `check`, `lint`, `type`, `build`, `e2e`, `playwright`, `cypress`, `puppeteer`, `browser`, `computer`, `computer-use`, `smoke`, `qa`, `release`.
- Project-specific skills or local instructions if present. Prefer those over this generic workflow.

Use `rg` and targeted file reads. Avoid broad scans of generated folders such as `node_modules`, `.next`, `dist`, `build`, `coverage`, and `test-results`.

## Execution Order

1. Preflight
   - Invoke `$orchestrator-mode` and `$agent-safe-run` as mandatory setup for broad test execution.
   - State the objective, task class, success bar, and delegation decision before widening the run.
   - Record repo path, branch, commit, dirty git state, requested environment, target URL, and known deploy/build identifier when applicable.
   - Locate any finish-line coverage ledger from this thread, repo QA docs, PR notes, branch docs, or recent finish-line report. If a ledger exists, import it into the suite inventory before execution. If the user specifically asks to validate recent finish-line work and no ledger can be found, report that as a coverage accounting blocker and reconstruct the issue-to-test mapping from diffs/tests before running broad checks.
   - Confirm required env vars/services are present without printing secrets.
   - Check whether the requested environment has safety constraints or approval requirements.
   - Produce a suite inventory before execution. Include every discovered script/check/config file and every finish-line ledger test, and classify each as in-scope, blocked, not applicable, or explicitly excluded by the user. Do not omit configured suites because they are slow, browser-heavy, or previously passing.

2. Automated checks
   - Run the repo's canonical full deterministic suite.
   - If no canonical suite exists, infer from project files:
     - JavaScript/TypeScript: package-manager test command, type-check, lint/check, build, then e2e/computer-use/browser tests if configured.
     - Python: `pytest`, type/lint commands if configured, build/package checks if present.
     - Go: `go test ./...`, vet/lint if configured.
     - Rust: `cargo test`, `cargo clippy` if configured, build/check if configured.
   - Include focused gates relevant to the changed area when repo docs or scripts identify them.
   - Run every direct finish-line ledger command or prove the repo's canonical command includes it. If a canonical full-suite command does not include a ledger test, run the ledger test separately and record the suite wiring gap as a follow-up or blocker.
   - In JavaScript/TypeScript workspaces, run all relevant package-manager scripts matching deterministic tests, browser/e2e/computer-use tests, prod/dev/preview canaries, lint, typecheck, build, and check. If a canonical `test:all`, `test:predeploy`, or equivalent omits configured browser/canary suites, run the omitted suites separately.
   - For monorepos, run root-level suite commands plus each workspace/package suite unless the root command is documented to transitively run them all.

3. Environment checks
   - `local`: start or reuse the documented local server and verify health/routes.
   - Hosted non-prod: verify target URL, deployed commit/version when possible, auth/session readiness, and smoke endpoints/routes.
   - Production: verify target URL and health using production-safe actions only.

4. Authenticated test-user setup
   - For any real app with login, dashboard, account, admin, settings, data, billing, or other authenticated surfaces, a full suite is incomplete unless browser/e2e/manual coverage logs in with an approved test or QA user.
   - First look for project docs that name approved QA users, seeded auth sessions, or test credentials. Then inspect safe local env names only, such as `PLAYWRIGHT_AUTH_SESSION_FILE`, `PLAYWRIGHT_AUTH_SESSION_JSON`, `PLAYWRIGHT_AUTH_EMAIL`, `PLAYWRIGHT_AUTH_PASSWORD`, `QA_EMAIL`, `TEST_USER_EMAIL`, or project-specific equivalents. Do not print secret values.
   - If no auth session exists, create or recover one only through approved, production-safe flows for the target environment: test-user signup in local/dev, passwordless or forgot-password flows for approved QA aliases, or an app-supported auth fixture. Use email access when available to complete the login/recovery flow.
   - Prefer `the user@splinteredglass.solutions` as the user's general cross-app QA identity when a project does not document a better one and the account is approved for the target environment.
   - For production, do not treat missing credentials as an acceptable pass. Report it as a blocker and continue only with clearly labeled unauthenticated/public checks until an authenticated session is obtained.
   - Do not use real customer accounts, invite real users, reset passwords for non-approved accounts, or create/modify paid production subscriptions unless the user explicitly approves that exact action.

5. Computer-use, browser, API, and manual coverage
   - If the project has a web app, UI, API workflow, or CLI workflow with a real user path, full suite includes the repo's computer-use/e2e/browser tests plus any manual walkthrough checklist.
   - Do not skip computer-use/e2e/browser tests merely because deterministic checks pass. Skip them only when the repo has no such tests/surface, the requested environment makes them impossible, or safety/credentials block them; report the skip as a blocker or explicit not-run item.
   - For authenticated apps, run the browser/e2e/manual checklist after login and cover authenticated routes with the approved user. Public-only checks are supplemental, not a replacement for authenticated app QA.
   - If the repo has deployed-environment canaries for `dev`, `preview`, or `prod`, run them for the requested environment with the same feature coverage expectations. A prod canary may be read-only, but it must still cover authenticated user workflows when the app has them.
   - If the same Playwright/Cypress/computer-use suite can point at local/dev/prod through base URL and auth variables, use that suite for all environments rather than maintaining weaker environment-specific smoke suites.
   - For any finish-line ledger item that names a browser/e2e/computer-use test, run that exact test or the suite that includes it against the requested environment when safe. If the environment cannot support the exact test because of auth, paid actions, external-service risk, or fixture limitations, mark that ledger item blocked and run the closest safe canary only as supplemental evidence.
   - Cover primary user workflows, auth/onboarding, navigation, settings/admin surfaces, data creation/edit paths, and mobile/responsive behavior when applicable.
   - Capture console/network errors and screenshots/artifacts for failures.

6. Repair and retest loop
   - Use a batch-first loop. One loop is: run the broad suite inventory for the target environment, identify all failures from that pass, group related failures, write concrete hypotheses for each group, fix all actionable groups locally, run focused local checks for each fix, run the relevant broader local suites, deploy the verified batch when the target is hosted non-production, then rerun the affected hosted full-suite inventory.
   - Do not spend a loop per feature, per screenshot, or per individual test when the failures can be diagnosed and fixed together. Use focused reruns inside a loop to prove a fix, but count the loop at the batch level.
   - Default to a maximum of 5 loops. If the user explicitly gives a lower cap, honor the lower cap. If the user asks for more than 5 loops, pause at loop 5 with a compact status report and ask before continuing.
   - For `local`, validate fixes against the local suite and local app. For hosted `dev`, `staging`, or `preview`, validate locally first, then deploy through the repo's documented non-production path before rerunning hosted checks. If deployment is blocked or not authorized for that target, record the hosted retest as blocked and report the exact next action needed.
   - For `prod` or `production`, do not deploy or mutate production as part of the loop unless the user explicitly approves that exact production action. Production loops are read-only by default and should stop at a local or non-prod fix plus a clear production validation blocker when deployment would be required.
   - Continue looping while the next step is under the agent control and reasonably safe: code fixes, test fixes, config corrections, fixture cleanup, local service restarts, retrying flaky third-party reads, recovering approved auth sessions, adding missing documented setup, and documented non-production redeploys for hosted retest.
   - Stop looping only when the suite is green, the loop cap is reached, or the remaining issue is blocked by something outside the current agent run: missing/expired credentials that cannot be recovered through approved paths, access or billing limits, unavailable third-party services, required human product/scope decision, production-safety approval, destructive data migration approval, account owner action, or another dependency that cannot be resolved from the repo/session.
   - Do not label ordinary test failures, unclear code paths, slow suites, or broad logs as blockers until a focused diagnosis has shown that the next useful step requires outside input or would exceed approved safety boundaries.
   - Keep a compact loop log with loop number, failure groups, hypotheses, local changes/actions, focused local retests, broader local retests, deployment identifier when applicable, hosted retest command/result, and whether the loop expanded or narrowed the remaining failure set.
   - When a fix touches application behavior, rerun both the focused failing check and the relevant broader local suite before deploying or calling the run green. For hosted targets, do not call the hosted run green until the deployed environment has also passed the affected hosted suite inventory.
   - If a fix could change product scope, user-visible behavior, permissions, data mutation, billing, auth, or environment safety posture, flag it for human review even when tests pass.

7. Report
   - Summarize pass/fail status by check type.
   - Include environment, URL, branch/commit/deploy, authenticated test user used, commands run, manual coverage, failures, blockers, and retests.
   - Include the suite inventory with status for each discovered suite/check. If anything did not run, state whether it was blocked, not applicable, explicitly excluded by the user, or unsafe for the target environment.
   - Include a "Finish-line ledger verification" section when a ledger exists: list every ledger issue/test, direct command result, broader suite result, environment applicability, and whether the exact assertion ran. If any ledger item did not run, the full suite is incomplete unless it is explicitly blocked or not applicable for the target environment.
   - State whether authenticated coverage ran. If it did not, the full suite is incomplete unless the app has no authenticated surface.
   - End with a high-level loop summary: total loops run out of the cap, failure groups found in each pass, what changed, what passed locally before deployment, deployment identifiers for hosted loops, hosted retest results, how the failures were solved or why they remain blocked, and any implications that should be reviewed to ensure the fixes did not unintentionally change app scope or functionality.
   - If a run-log convention exists, update it. Otherwise create a dated log only when the run is substantial or browser/manual coverage is performed.

## Safety Rules

- Production full suite is non-destructive by default.
- Do not delete production data, invite real users, mutate paid subscriptions, post public release notes, send real customer notifications, or run large/costly jobs unless the user explicitly approves that exact action.
- For databases, do not change permissions, grants, roles, ownership, RLS, or object owners without exact approval.
- A green `dev` or staging suite does not imply permission to promote to `main` or release to production. Do those only when the user explicitly asks. Non-production deploys are allowed inside the repair loop only when the requested target is hosted non-production and the loop needs a deployed retest; use the repo's documented non-production deployment path and report the deploy identifier.
- If secrets are needed, verify presence and names only; do not print secret values.

## Bonfire Known Mapping

When the current repo is Bonfire, use the repo's canonical QA docs:

- `docs/qa/full-suite-runbook.md`
- `docs/qa/computer-use-full-app-checklist.md`
- `docs/qa/computer-use-release-checklist.md` when the changed area touches Studio, actions, generated resources, widget actions, Campfire resource actions, Session API artifact generation, or resource persistence
- `docs/qa/environment-matrix.md`
- `docs/qa/manual-run-template.md`
- `docs/qa/README.md`

Environment URLs:

- `local`: `http://localhost:5001`
- `dev`: `https://dev.heybonfire.com`
- `prod`: production URL from the environment matrix or user prompt

Approved Bonfire auth users:

- Production Bonfire real-app QA must use an authenticated approved user. Prefer `the user@heybonfire.com` for Bonfire production app checks.
- `the user@splinteredglass.solutions` is the approved fallback Bonfire QA identity for hosted dev/prod auth when `the user@heybonfire.com` is not already available or explicitly required. Do not report "no auth provided" for Bonfire hosted QA until this identity has been tried through the available secure credential path.
- Local reusable credential source: macOS Keychain generic password, service `bonfire-playwright-qa-dev`, account `the user@splinteredglass.solutions`. Never write the plaintext password into this skill, memory, repo files, logs, or command output.
- For hosted Bonfire Playwright runs, prefer a real Supabase session using the approved fallback account before falling back to public-only checks. Retrieve the password without printing it:

```bash
BONFIRE_QA_PASSWORD="$(security find-generic-password -a 'the user@splinteredglass.solutions' -s 'bonfire-playwright-qa-dev' -w 2>/dev/null || true)"
PLAYWRIGHT_BASE_URL=https://dev.heybonfire.com \
PLAYWRIGHT_SKIP_WEBSERVER=true \
PLAYWRIGHT_AUTH_SESSION_FILE= \
PLAYWRIGHT_AUTH_EMAIL=the user@splinteredglass.solutions \
PLAYWRIGHT_AUTH_PASSWORD="$BONFIRE_QA_PASSWORD" \
NEXT_PUBLIC_POSTHOG_PROJECT_TOKEN= \
corepack pnpm test:computer
```

- Before calling hosted auth blocked, verify the keychain item exists or the current thread supplied a credential, verify `PLAYWRIGHT_AUTH_EMAIL` and `PLAYWRIGHT_AUTH_PASSWORD` are present without printing values, and verify the harness is not using placeholder Supabase config such as `example.supabase.co`. If the sign-in attempt fails because Supabase config resolves to a placeholder host, report that as a harness/config blocker, not missing auth.
- If a stored Playwright auth session is missing or stale, use the approved fallback account, password auth, passwordless, or forgot-password flow and the user-controlled email access to establish the session before calling authenticated Bonfire QA complete.

Default Bonfire full suite includes both deterministic checks and Computer Use coverage:

- Deterministic checks: Vitest, type-check, lint check, build for release confidence, and focused gates relevant to the changed area.
- Computer Use/browser checks: `corepack pnpm test:computer` plus the full-app Computer Use checklist for full-suite QA. Also run the Studio/actions/resources Computer Use release checklist when the changed area matches that checklist.

For Bonfire, keep the standing release guardrail: validated `dev` is the stopping point unless the user explicitly asks for `main` or production promotion in the current conversation.

