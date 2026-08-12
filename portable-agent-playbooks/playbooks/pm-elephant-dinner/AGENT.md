# PM Elephant Dinner Agent Playbook

This is a platform-neutral version of the `pm-elephant-dinner` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

PM Elephant Dinner: use when any project or initiative has too many tasks, commitments, decisions, workstreams, unread threads, dependencies, or spinning plates to reason about safely. Works for software, client delivery, creative, operations, research, events, and personal projects. Gather the relevant live evidence, dedupe the work, interview for the few decisions that change scope, define a shared batch, build a dependency-aware execution plan, create a visual command center when useful, and prepare selectable PM delegation packets without starting gated actions until approved.

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

# PM Elephant Dinner

Turn any overwhelming project or initiative into a bounded set of bites with
owners, order, proof, and a consolidation path.

## Required Skills

Read and follow:

- `$CODEX_HOME/skills/orchestrator-mode/SKILL.md`
- `$CODEX_HOME/skills/session-budget/SKILL.md`
- `$CODEX_HOME/skills/project-portfolio-manager/SKILL.md`
- `$CODEX_HOME/skills/interview-spec/SKILL.md`

Read `$CODEX_HOME/skills/delegate/SKILL.md` when preparing or
executing delegation packets.

For technical branch sprawl, also read:

- `$CODEX_HOME/skills/local-dev-consolidation/SKILL.md`

## Operating Contract

This skill is research and planning first. It does not itself authorize worker
creation, external messages, ClickUp mutation, deploys, production changes,
protected-branch work, paid actions, credential changes, or DB grants,
ownership, roles, permissions, or RLS changes.

Do not force software, customer, ClickUp, Git, sprint, or release concepts onto
a project where they do not apply. Do not open implementation tasks while the
project inventory is still changing. Return selectable delegation candidates
so the decision owner can choose what starts.

## Project-Type Routing

Identify the project type before gathering evidence:

- **Software/product:** repos, environments, releases, QA, security, migrations,
  branches, worktrees, and technical ownership.
- **Client/service:** promises, deliverables, approvals, meetings,
  communications, due dates, dependencies, and acceptance evidence.
- **Creative/marketing/content:** briefs, assets, channels, review rounds,
  production owners, publishing gates, and audience outcomes.
- **Operations/admin/event:** checklists, vendors, logistics, forms, schedules,
  handoffs, recurring work, and completion evidence.
- **Research/strategy:** questions, source quality, decision criteria,
  synthesis, recommendations, and unresolved uncertainty.
- **Personal/non-business:** desired outcome, time and budget constraints,
  purchases, sequencing, dependencies, and a realistic completion rhythm.

Use more than one route for hybrid projects. Skip irrelevant evidence surfaces
and state which routes were selected.

## Workflow

1. **Contain the project.**
   - State the project or initiative, selected project type(s), planning
     horizon, task class, and success bar.
   - The horizon may be a day, week, sprint, milestone, event, launch, recovery
     period, or another bounded interval.
   - Temporarily freeze new execution lanes until the inventory and dependency
     map are coherent.
   - Use `$orchestrator-mode`; launch bounded research subagents when evidence
     slices are independent.

2. **Choose one batch identity.**
   - Pick or propose one unused numerical emoji such as `1️⃣` for all human-facing
     tasks in this project sprawl.
   - Assign a stable ASCII batch ID such as `PROJ-W29` or `EVENT-01`.
   - Delegated worker titles use `<batch emoji> 🧩 <Project>: <task>`.
   - Keep emoji out of machine-readable IDs and, when present, Git branches,
     worktree paths, and filenames.

3. **Gather live evidence.**
   - Read the applicable project registry, PM state, approval and work ledgers,
     task system, recent project tasks, unread work, plans, and source docs.
   - Gather commitments from relevant meetings and communication channels when
     authorized and available; these may be customer, teammate, vendor, family,
     or self-commitments.
   - For technical projects, inspect repo status, environment evidence,
     branches, worktrees, stashes, release artifacts, and validation state.
   - For nontechnical projects, inspect the applicable briefs, schedules,
     inventories, budgets, deliverables, logistics, or research sources.
   - Keep source IDs, dates, task/thread IDs, and proof links.
   - Record blocked sources instead of silently treating them as clear.

4. **Dedupe the elephant.**
   - Collapse duplicate promises, notifications, worker tasks, and planning
     threads into one canonical work item.
   - Separate `must finish`, `should finish`, `conditional`, and `defer`.
   - Derive work categories from the selected project type instead of using a
     fixed software or customer taxonomy.

5. **Build the dependency graph.**
   - Identify the critical path and independent parallel lanes.
   - Set an explicit WIP limit. Default to three concurrent lanes; allow four
     technical lanes when they are genuinely isolated.
   - Name overlap zones so two owners do not modify the same files, assets,
     decisions, contacts, locations, or contracts.
   - Put independent preparation work beside the critical path when it can
     proceed without waiting for the main deliverable.

6. **Interview for only high-leverage decisions.**
   - Ask 1-3 questions at a time when user interaction is active.
   - Prioritize finish line, scope slice, owner, target date or milestone,
     acceptance criteria, constraints, and gated actions.
   - Maintain confirmed decisions, assumptions, and open questions separately.
   - Do not infer approval from silence.

7. **Define each bite.**
   - Give every item a stable work ID, priority, owner route, project/context,
     objective, dependencies, authority limits, finish line, validation, stop
     conditions, and source evidence.
   - Phrase the title so the decision owner can select it and invoke
     `$pm-delegate` when delegation is appropriate.

8. **Design execution isolation.**
   - For every project, define ownership boundaries, handoff points, shared
     resources, integration order, and a completion/cleanup rule.
   - For technical projects only:
     - Freeze the appropriate current clean integration baseline before feature
       work.
     - Create a registry plan linking work ID, task/thread ID, repo, baseline
       SHA, branch, worktree, owner, overlap zone, validation artifact,
       closeout, integration status, and cleanup status.
     - Use ASCII branches such as `agent/<batch-id>-<slug>`.
     - Require `ready_to_integrate` before `$local-dev-consolidation` can include
       a lane.
     - Do not clean worktrees until integration and proof are recorded.
   - For nontechnical projects, replace branches/worktrees with the relevant
     version, draft, asset, schedule, location, or handoff registry.

9. **Create the command center.**
   - Save a decision-ready Markdown plan and source ledger.
   - For broad plans, create a compact local dashboard with filters, priorities,
     decisions, timeline, critical path, and copyable delegation prompts.
   - Prefer a standalone HTML artifact when no server is needed.

10. **Stop at the decision gate.**
    - Return the compact plan and selectable delegation backlog.
    - List the exact decisions blocking motion and name each decision owner.
    - Create or message tasks only after the authorized decision owner selects
      or approves them.

## Output Shape

Use icon-prefixed sections:

```text
🐘 PROJECT:
🧭 PROJECT TYPE / HORIZON:
🎯 TARGET OUTCOME:
🔢 BATCH MARKER:
🚦 CRITICAL PATH:
🧩 PARALLEL LANES:
🤝 COMMITMENTS / DEPENDENCIES:
👤 OWNERSHIP:
🟡 DECISIONS NEEDED:
📅 OPERATING RHYTHM:
🌿 ISOLATION / INTEGRATION PLAN:
🔒 SAFETY BOUNDARY:
📎 ARTIFACTS:
```

For every selectable item include:

```text
WORK_ID:
TITLE:
PRIORITY:
OWNER_ROUTE:
PROJECT/CONTEXT:
OBJECTIVE:
DEPENDENCIES:
FINISH_LINE:
VALIDATION:
AUTHORITY:
STOP_CONDITIONS:
SOURCE_EVIDENCE:
```
