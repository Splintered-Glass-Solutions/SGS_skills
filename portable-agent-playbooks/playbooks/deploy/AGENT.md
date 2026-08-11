# Deploy Agent Playbook

This is a platform-neutral version of the `deploy` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Deploy the feature, functionality, branch, commit, or PR worked on in the current the agent task to an explicit environment or the sole registered environment for a single-target project, including dependency-aware deployment across multiple repositories such as frontend, backend, API, workers, infrastructure, and database components. Recover or create missing deployable artifacts when the current task contains a decision-ready feature scope. Use when the user invokes $deploy or /deploy, including a bare "deploy" in a registered single-environment project, and expects the agent to persist until every in-scope component is deployed or a genuine external blocker is proven.

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

# Deploy

Deploy the current task's implementation to the requested environment using
each project's own release path. Orchestrate every repository and runtime that
must move for the feature to work, while keeping feature testing outside this
skill.

## Environment Resolution

Read `references/environment-registry.json` before deciding the target. Resolve
the current repository and optional user-supplied environment with:

```bash
python3 <agent-config>/skills/deploy/scripts/resolve_environment.py resolve \
  --repo <absolute-repository-path> [--environment <name>] --json
```

The registry resolves only the logical environment and expected release lane.
It is not deploy authorization and does not replace project/provider preflight.
Always run the returned `identity_gate` and the project's documented provider
checks before a write.

Rules:

1. If the requester names an environment, normalize obvious aliases such as
   `prod` to `production` and require an exact registered match.
2. If the requester omits the environment, auto-select it only when the matched
   project has `allow_implicit_environment=true` and exactly one environment.
   State the resolved environment and provider target before publishing.
3. If the project has multiple environments, require the requester to name one.
   Never choose `dev` or `production` from branch name, URL, recent deploy, or
   prior conversation alone.
4. If the project is absent or ambiguous, ask for the environment and gather
   authoritative mapping evidence. Do not infer a deployment target.
5. Worktrees may resolve through their canonical Git remote, but provider
   safety checks must still approve that exact worktree or deployment path.

Maintain environment topology in this skill's registry. Keep immutable Vercel
team/project identity in
`<agent-config>/skills/vercel-deployment-safety/references/project-registry.json`;
do not duplicate or weaken that safety source.

## Invocation Contract

Treat the first argument as the target environment when supplied:

```text
/deploy dev
/deploy staging avatar uploader
/deploy prod PR 412 and API PR 98
/deploy
```

When no environment argument is supplied, use the registry resolver above.
Proceed only for a uniquely registered single-environment project. Otherwise
require an explicit target before making deployment changes. Normalize an
obvious typo only when it maps unambiguously to a registered environment, and
state the normalization. Treat remaining arguments as explicit feature, repo,
branch, commit, PR, or component scope.

An explicit `/deploy <environment>` invocation authorizes the normal in-scope
delivery mechanics required by documented project workflows: preparing
task-owned commits, pushing branches, creating or updating PRs, merging through
required checks, triggering provider rollouts, applying approved non-destructive
deployment steps, and waiting for rollout completion. It does not authorize
unrelated changes, branch-protection bypasses, destructive data operations,
permission changes, customer communication, or promotion beyond the named
environment.

## Outcome and Authority Contract

Treat `/deploy <environment>` as an outcome request, not merely a request to
look for an already-prepared PR. The requested feature is not deployed until
the required implementation exists, every component has moved through its real
release path, and the target environment contains the resulting artifact.

The latest explicit `/deploy` invocation supersedes an earlier user-provided
`planning-only`, `no build yet`, `local-only`, or `do not deploy` boundary for
the named feature to the minimum extent necessary to deploy it to the named
environment. It authorizes completing a decision-ready, task-owned
implementation when no deployable artifact exists. It does not override a
boundary repeated in the same invocation, higher-priority instructions, or the
safety limits in this skill.

Do not interpret an empty initial deployment graph as successful completion or
as permission to stop. First recover or create the missing task-owned artifact
using the artifact recovery procedure below. Stop only when the feature scope
is genuinely too ambiguous to implement safely, the user explicitly requested
deployment-only handling of existing artifacts, or a real approval, access,
safety, or external-state blocker remains.

## Goal and Persistence

Use the goal tools when available.

1. Inspect the current goal.
2. If no unfinished goal exists, create one with an objective like:
   `Fully deploy <feature scope> across <repositories/components> to
   <environment> and verify deployment evidence for every component.`
3. Do not set a token budget unless the user explicitly supplied one.
4. If an existing goal already covers this deployment, continue it. Do not
   replace an unrelated unfinished goal; report the conflict and request
   direction.
5. Keep working through safe, in-scope steps while the next action remains under
   the agent control. Do not stop merely because the rollout is slow, cross-repo,
   conflicted, or requires several provider polls.
6. Mark the goal complete only after every deployment graph node has terminal
   environment evidence and no required deployment work remains. Mark it
   blocked only under the goal tool's blocker contract.

The persistence goal does not broaden authority. Stop at approval, access,
destructive-migration, billing, unsafe-infrastructure, or external-service
boundaries that cannot be resolved safely in scope.

## Separate Deployment from Testing

Focus on release mechanics and deployment truth. Do not invoke `$test`,
`full-suite-tests`, browser QA, feature regression suites, or manual product
walkthroughs as part of this skill.

Allow only validation inherent to deploying safely:

- provider-required builds and required PR/CI gates;
- manifest, configuration, migration, and artifact validation required by the
  deployment runbook;
- health, readiness, version, revision, and deployment-status checks needed to
  prove that the requested artifact is live.

Do not bypass or disable required CI because testing is handled elsewhere. If a
required gate fails because of the task-owned implementation, diagnose it,
state a concrete hypothesis, repair the minimum in-scope issue, rerun the
required gate, and resume deployment. Hand work to `/test` only for broader QA
or a product-quality investigation that is not necessary to make the required
release gate pass. Repair deployment scripts, manifests, provider
configuration, release wiring, merge/deploy mechanics, and task-owned required
gate failures when they block the in-scope rollout.

## 1. Resolve the Deployment Scope

Use this precedence:

1. Explicit repos, PRs, commits, features, components, or environments in
   `/deploy` arguments.
2. A uniquely resolved single environment from the deployment registry.
3. The latest coherent implementation work in the current task.
4. PRs, branches, commits, and deployment artifacts created or referenced in
   the current task.
5. Related repositories required to make that implementation operational.

Inspect the conversation before the filesystem. Then use targeted reads of task
artifacts, git state, PR metadata, and nearby deployment docs. Do not treat every
dirty repo or recent commit as part of the release.

If no deployable artifact is immediately visible, perform an artifact recovery
sweep before classifying the request as not deployable:

1. Recover the latest coherent feature decision, selected option, acceptance
   criteria, and repository ownership from the current task and its artifacts.
2. Search task-linked worktrees, branches, commits, PRs, handoffs, and remote
   refs for an implementation. Prefer continuing the most complete task-owned
   artifact over rebuilding it.
3. Inspect required sibling repositories when the feature crosses app, API,
   worker, schema, infrastructure, or shared-package boundaries.
4. If the feature is decision-ready but still unimplemented, create a clean
   task-owned branch or worktree, implement the smallest complete agreed scope,
   run only the focused checks and required release gates needed to publish it,
   and then continue the deployment graph.
5. If material product decisions are missing, keep the deployment goal active
   while exhausting safe evidence. Then return `BLOCKED — IMPLEMENTATION SCOPE
   UNRESOLVED` with the exact missing decision instead of claiming there are
   zero deployable nodes.

Use `NOT DEPLOYABLE — NO IMPLEMENTED ARTIFACT` only when the user explicitly
limited the run to deploying pre-existing artifacts or when the named scope
cannot be connected to either an implementation or a decision-ready feature.
Do not deploy unrelated work.

For each candidate repository, record:

- absolute repo/worktree path;
- feature responsibility;
- task-owned branch, commit, and PR;
- target environment and provider/project/service;
- upstream and downstream dependencies;
- migration or infrastructure coupling;
- documented release skill/runbook;
- deploy trigger, success evidence, and rollback/roll-forward path;
- unrelated dirty files to preserve.

Record environment resolution as `explicit` or
`implicit-single-environment`. A project name containing `dev`, `stage`, or
`prod` does not override the registry's logical environment mapping. For
example, Tiburon's only Vercel project is named `tiburon-dev`, but its sole
deployable Vercel slot is registered as logical `production`.

Do not stage, commit, or deploy unrelated dirty work. If task-owned changes
overlap inseparably with unrelated work, stop for a scope decision rather than
publishing a mixed artifact.

## 2. Discover the Project's Real Deployment Path

For every repository or deployable component, inspect in this order:

1. Explicit deployment instructions supplied in the task.
2. Available project-specific deployment or release skills. Read and follow the
   applicable skill completely.
3. `AGENTS.md`, repository instructions, deployment runbooks, release docs, and
   environment matrices.
4. CI workflows, protected-branch rules, package scripts, infrastructure config,
   provider config, and recent successful deployment evidence.

Search narrowly with `rg` for terms such as `deploy`, `release`, `promotion`,
`environment`, `preview`, `staging`, `production`, the provider name, and the
target service. Do not invent a deploy command from framework conventions when
the project defines its own path.

Resolve environment names per component. The word `dev` may map to different
branches, provider environments, projects, accounts, URLs, databases, or cloud
regions across repositories. Record the mapping explicitly and verify the
account/project/service before mutating it.

Use `orchestrator-mode` and `agent-safe-run` for multi-repo, multi-provider,
log-heavy, or long deployments. Keep verbose logs in `/tmp` or the repo's
documented deployment evidence folder and report compact milestones.

### Bonfire shared-ETL topology

For `bonfire-app`, `bonfire-api`, or `bonfire-etl`, do not infer the logical
environment from a Lambda name, an ECR tag, or an `infra/envs/dev` Terraform
path. Before any AWS write, read the current Bonfire environment matrix and
prove the complete live route: Railway environment/service → configured ETL
Function URL → Lambda function → active image/version.

- Treat explicitly named `bonfire_dev_*` functions as isolated Dev resources.
- Treat shared `bonfire_*` functions as potentially production-facing. They
  are the current production runtime when Railway Production points its ETL
  URLs at them, even if their legacy Terraform owner or AWS tags say `dev`.
- In the known shared-database source-sync topology, Railway Development and
  Railway Production intentionally use the same `ETL_SOURCE_SYNC_URL` and
  `bonfire_content_source_sync` router. Treat that as a declared release
  boundary, not an automatic environment mismatch or blocker.
- An explicit `/deploy dev` for that shared router authorizes its compatible
  code-only router rollout once the complete mapping is verified. State that
  both attached Railway environments receive the router image. This exception
  does not authorize unrelated shared resources, shared-data mutations, or a
  general production promotion. Honor an explicit `isolated Dev only` limit.
- Do not create or apply a duplicate `infra/envs/prod` stack merely because a
  logical production registry entry exists. First compare its Terraform module
  names and AWS identities with the shared runtime; stop if it would collide
  with or leave untouched the functions that production actually invokes.
- For a production ETL release, publish the exact `main` image artifacts and
  update only the verified production-facing functions. Read their `Active`
  state and exact image URIs back afterward. Record this as the production
  deployment proof, separately from Terraform ownership labels.

If the mapping cannot be proved from current provider configuration, stop
before deployment and report `BLOCKED — BONFIRE RUNTIME TARGET UNRESOLVED`.

### Bonfire ETL single-router code-only path

For one existing Lambda function whose only intended change is its container
image, use this low-variance path:

1. Build and publish an image tagged with the task-owned merged commit.
2. Change only that function's configured image tag. Inspect the configuration
   diff before planning; do not edit another function's tag by name similarity.
3. Create a targeted Terraform plan and save it. Require the plan to contain
   exactly one Lambda image update for the intended function and no other
   resource changes. Treat any extra change, missing update, or wrong function
   as a blocker and correct the configuration before applying.
4. Apply the saved plan, not a newly recomputed plan.
5. Re-read the Lambda's active state, image URI and digest, event-source mapping
   state, and the mapped application health endpoint. Keep the prior image tag
   or digest as the roll-forward/rollback reference.

Record only secret names and presence; never print Terraform variable values or
provider credentials.

## 3. Build the Deployment Graph

Create a manifest before publishing anything. Use one node per deployable
artifact or state transition:

| Node | Repo/component | Artifact | Target | Depends on | Deploy path | Success evidence | Rollback |
|---|---|---|---|---|---|---|---|

Include frontend, backend/API, workers, scheduled jobs, shared packages,
infrastructure, schemas/migrations, feature flags, and environment configuration
only when the feature actually depends on them.

Choose order from compatibility and dependencies, not a fixed repo list.
Typically prefer:

1. additive infrastructure or backward-compatible schema state;
2. backend/API compatibility;
3. workers or asynchronous consumers;
4. frontend or client consumers;
5. flags, aliases, routing, or traffic cutover.

For breaking contracts, create a staged expand/migrate/contract or dual-version
rollout so old and new components remain compatible during deployment. Do not
ship a frontend that requires an API or schema version that is not live.

Deploy independent nodes in parallel only when their rollouts and logs cannot
interfere. Serialize shared database, shared provider, migration, traffic, and
dependency-sensitive nodes.

Before executing, classify each node as `ready`, `blocked`, `already deployed`,
or `not applicable`. A node is already deployed only when the target
environment's live revision contains the exact required artifact.

If the graph initially has zero nodes but the invocation names or clearly
inherits a feature, return to artifact recovery. Do not skip goal creation, do
not mark the deployment complete, and do not stop solely because a PR or commit
does not exist yet.

## 4. Preflight Each Node

Perform read-only checks first:

- fetch current remote state and inspect exact branch/commit ancestry;
- verify PR status, base branch, required checks, mergeability, and environment
  protection rules;
- verify provider authentication and the exact account/project/service;
- verify environment variables or secrets by name/presence without printing
  values;
- verify migration direction, compatibility, target database/project, and
  destructive or permission-changing operations;
- record current live revision and rollback or roll-forward candidate;
- confirm downstream nodes remain compatible during rollout.

Reconcile long-lived branches with the current target base through the project's
normal workflow. Do not force-push shared branches, bypass protection, or reset
user work.

For production or shared data infrastructure, stop before destructive schema
changes, backfills, grants, roles, ownership, RLS, paid-resource expansion, or
irreversible operations unless the user explicitly approved that exact action.
An environment label is not proof that its attached database or provider
resources are safe; inspect the actual target.

## 5. Execute and Observe

Follow each node's documented path exactly. Reuse existing PRs and deployment
runs when they contain the required artifact. Create new branches or PRs only
when the release path needs them.

After each state-changing action:

- capture branch, commit, PR, workflow/run, provider deployment, service, URL,
  and timestamp identifiers;
- wait with bounded polling and compact updates until the node reaches a
  terminal provider state;
- diagnose deployment-mechanic failures, state a concrete hypothesis before
  editing, repair in scope, and resume from the failed node;
- re-read remote/provider state rather than assuming an accepted command
  completed the rollout.

If a node fails after earlier nodes are live, keep the system in the safest
compatible state. Prefer an approved roll-forward when earlier state is
backward-compatible. Use rollback only when the project's runbook supports it
and it will not worsen schema or data compatibility. Never improvise a database
rollback.

Do not declare a cross-repo feature deployed when only one repository or
provider completed. Keep the remaining graph active and continue.

## 6. Prove Deployment Completion

For every node, require evidence appropriate to the platform:

- the exact task-owned commit is merged or otherwise present in the release
  artifact;
- the provider reports a successful rollout for the correct service and
  environment;
- the live revision, image digest, build marker, release ID, or ancestry can be
  reconciled to the required commit;
- deployment health/readiness is green;
- required migration/infrastructure state is applied to the correct target;
- dependent nodes point at compatible live endpoints or versions.

Re-check live ancestry after rollout because another merge may have advanced
the environment. A newer live revision is acceptable only when it is a
descendant or artifact that demonstrably contains the required change.

Health proves deployment readiness, not feature behavior. State clearly that
feature testing was not run and should be performed separately with `/test`.

## Status and Closeout

Use one headline:

- `DEPLOYED — COMPLETE`: every graph node has verified target-environment
  evidence.
- `DEPLOYMENT IN PROGRESS`: provider work is still non-terminal and the agent is
  continuing to monitor it.
- `PARTIALLY DEPLOYED`: at least one node is live and another is not; never use
  this as success.
- `BLOCKED — NOT FULLY DEPLOYED`: a genuine external, approval, access, safety,
  or required-CI blocker prevents completion.
- `BLOCKED — IMPLEMENTATION SCOPE UNRESOLVED`: deployment intent is clear but a
  material product or technical decision is missing, so creating the artifact
  would require guessing.
- `NOT DEPLOYABLE — NO IMPLEMENTED ARTIFACT`: no task-owned deployable work was
  found, no decision-ready feature can be recovered, or the user explicitly
  limited the run to existing artifacts.

Report:

- requested environment and exact per-component mappings;
- deployment graph and final node status;
- repo/worktree, branch, commit, PR, provider run, service, URL, and live
  revision for each node;
- merge, provider rollout, health, migration/infrastructure, and dependency
  gates as separate claims;
- unrelated work excluded;
- deployment repairs and retries;
- blockers, rollback/roll-forward posture, and exact next action;
- explicit note that feature testing was not part of this run.

Do not call the deployment complete based only on a push, merged PR, green CI,
provider trigger, healthy URL, or one completed repository. Completion requires
the whole graph and the actual requested environment.

## Safety Boundaries

- Deploy only to the named environment. `/deploy dev` does not authorize main
  or production; `/deploy prod` does not authorize unrelated services.
- A bare `/deploy` authorizes only the sole environment returned by the
  fail-closed registry resolver. It never authorizes a target in a
  multi-environment or unregistered project.
- Follow protected-branch, approval, environment-protection, and provider gates.
- Never print secrets or dump environment files.
- Never change database permissions, grants, roles, ownership, or RLS without
  exact prior approval.
- Never deploy real customer data changes, destructive migrations, backfills,
  paid subscription changes, or public communications without exact approval.
- Preserve unrelated local changes and existing user-owned branches/PRs.
- Keep local, merged, provider-deployed, hosted-live, and customer-visible proof
  distinct.
