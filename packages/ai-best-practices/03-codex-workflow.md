# 3. Codex Workflow and Skill Routing

The local Codex skill catalog is best understood as a routing system. Skills
are not all peers: some are modes, some are gates, some are executors, and
some are domain adapters.

## Skill roles

### Mode skills

These change how the current task behaves:

- `to-do-list`: capture-only mode;
- `to-do-list-planning`: planning-only mode;
- `recap`: read-only status mode;
- `sleep`: pause mode;
- `close-thread`: closeout naming mode;
- `orchestrator-mode`: main-thread coordination mode.

### Meta and safety skills

These govern the quality of the work rather than the product itself:

- `token-saver`: context, output, retry, and accepted-state discipline;
- `session-budget`: task classification, checkpoints, and stop conditions;
- `codex-safe-run`: desktop, process, browser, and resource safety;
- `security-best-practices`: security review;
- `prep-work`: readiness and access audit;
- `bring-in-the-big-guns`: escalation after repeated failure.

### Lifecycle skills

These move work through the system:

- intake: `note`, `sideline-feature`;
- clarification: `interview-spec`, `expansive-planning`;
- packaging: `plan-handoff`, `handoff`;
- execution: `bulk-edits-thread`, `autonomous-feature-build`, `hot-fix`;
- validation: `test`, `qa-run`, `full-suite-tests`, `feature-finish-line`;
- integration: `collapse-bulk-edits-thread`, `local-dev-consolidation`;
- continuation: `continue`, `next-step`, `recap`;
- cleanup: `car-wash`, `prune-local`.

### Portfolio skills

These operate above a single code task:

- `project-portfolio-manager` and `pm-project-portfolio-manager`;
- `pm-project-agent`, `pm-dashboard`, and `plate-spin`;
- `pm-delegate`, `delegate`, and `pm-ingest-closeout`;
- `pm-thread-sweep`, `pm-clean-unreads`, and `pm-comms-check`;
- `pm-comms-sync`, `pm-elephant-dinner`, and `prioritize`;
- `automation-thread-scheduler` and `group-testing-thread`.

### Product and domain adapters

These should be selected after the general task boundary is known. Examples
include adapters for:

- application routes, authentication, billing, content, ETL, deployment, QA,
  demos, organization audits, marketing, and database policy;
- project-management systems, data quality, release communication, and time
  tracking;
- client proposals, personal operations, meeting archives, dashboards, PDFs,
  design tools, and hosting providers.

They provide local operational knowledge. They do not replace the general
scope, authority, validation, or handoff rules.

## Recommended routing patterns

### A small coding task

```text
hot-fix or direct implementation → test → concise recap
```

### A related batch of coding tasks

```text
to-do-list → to-do-list-planning → bulk-edits-thread
→ test / spin-up-local → collapse-bulk-edits-thread
```

### A large feature

```text
prep-work → token-saver → orchestrator-mode
→ autonomous-feature-build → feature-finish-line
→ deploy or handoff
```

### A cross-project portfolio pass

```text
project-portfolio-manager → pm-dashboard / plate-spin
→ pm-delegate → worker threads → pm-ingest-closeout
```

### A paused or interrupted task

```text
recap or handoff → continue → next-step
```

### A research-to-execution task

```text
token-saver → targeted research → plan-handoff
→ fresh execution task
```

## Skill composition rule

Use one primary workflow skill and only the dependencies needed for the task.

For example:

- primary: `bulk-edits-thread`;
- safety: `codex-safe-run`;
- efficiency: `token-saver`;
- runtime: `spin-up-local`;
- validation: `test`;
- closeout: `collapse-bulk-edits-thread`.

Avoid invoking every apparently related skill. Composition should reduce
ambiguity, not create a second project-management system inside the first one.

## Local versus portable skills

A local catalog may contain project adapters and personal operating
preferences. This public archive contains only generalized workflows, with
secrets, private paths, customer data, and project-specific registries removed.
