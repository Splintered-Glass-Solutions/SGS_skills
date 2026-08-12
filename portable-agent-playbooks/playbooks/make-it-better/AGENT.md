# Make It Better Agent Playbook

This is a platform-neutral version of the `make-it-better` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Use when the user asks to broadly improve a project, make it better, audit product quality, UI/UX, design, copy, code quality, testing gaps, graphics, polish, or user delight with orchestrator-mode, autonomous loops, agent-safe-run guardrails, bounded subagents or delegated project threads, active monitoring/review of delegated work, and queued checkpoints instead of early blocking.

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

# Make It Better

## Overview

Use this skill when the request is broadly: make the project better. The goal is
to understand the product and repos, then go as far as possible on product
quality, UI/UX, design, style, copy, code quality, testing, graphics, polish,
performance, accessibility, developer experience, and user delight.

Security is secondary. Flag only obvious trust, privacy, or safety issues that
materially affect product confidence unless the user explicitly asks for a deep
security audit.

Default to pairing this skill with `$orchestrator-mode` and `$agent-safe-run`.
When changes are allowed, also pair it with `$autonomous-feature-build`. If the
work is broad, high-cost, QA-heavy, multi-file, multi-repo, ambiguous, or likely
to benefit from independent review, make an explicit delegation decision and use
bounded subagents or delegated project threads unless there is a concrete reason
not to.

## Success Bar

Produce a decision-ready improvement package, and implement the best safe
improvements when the current request permits edits. The final result must show:

- what the project appears to be
- who it serves
- what is strong
- what is weak
- the best overall improvement direction
- prioritized recommendations
- proof gathered
- loops completed
- questions and checkpoints queued for the next pass

## Operating Mode

Use the strongest available deep-reasoning frontier agent as the main
orchestrator, product reviewer, architect, and final decision-maker.

Use `$orchestrator-mode` as the default operating model. The main thread remains
the orchestrator and keeps decomposition, prioritization, architecture,
tradeoffs, validation strategy, synthesis, and final review.

Use cheaper capable subagents, delegated project threads, or bounded parallel
tool waves for broad scanning, evidence gathering, narrow implementation
research, testing, screenshot review, log reduction, rapid idea generation, and
sidecar code review. Subagents are preferred over doing all broad or noisy work
in the main thread when a slice can be scoped independently.

For substantial work, launch at least one bounded subagent/delegation wave before
final synthesis unless there is a concrete exception such as:

- the task is tiny and single-file
- subagent/thread tooling is unavailable
- the next blocker requires direct main-thread inspection
- the work is privacy/safety-sensitive and should not be delegated

If subagents are skipped, state the reason in the final deliverable.

Keep these in the main thread:

- product interpretation
- creative direction
- prioritization
- tradeoff decisions
- architecture decisions
- final roadmap
- final implementation choices
- final verification standard

Delegate these when independent and bounded:

- repo and app structure inventory
- route and screen inventory
- UI/component inventory
- style-system and design-token scan
- copy and tone inventory
- test-gap scan
- code-quality review
- performance and perceived-speed review
- accessibility and responsive review
- graphics, imagery, chart, and iconography review
- rapid brainstorming
- focused verification and log reduction
- independent code review of the selected patch
- durable worker packets for repo-specific execution
- project-thread follow-up, when a verified project thread is the right owner

When delegation is useful and thread management is available, the orchestrator
may route work through persistent project threads or bounded worker threads. Use
the PM/project delegation pattern when the user asks to delegate or when a
verified project thread clearly owns the work. The main thread must monitor,
manage, and review those threads: define the packet, set authority limits, wait
only when the result is needed, integrate evidence, inspect risky diffs, and
close or summarize worker outputs before final synthesis.

Treat delegated output as evidence, not a verdict. Reopen important files and
inspect key artifacts before relying on them.

## Safe-Run Guardrails

Follow `$agent-safe-run` throughout long or noisy work:

- keep the main thread lean
- prefer targeted `rg`, bounded reads, and short command output
- use file-backed logs for noisy commands
- do not stream watchers, full build logs, full process tables, or repeated
  monitor output
- avoid long-running browser, Playwright, Computer Use, or helper sessions unless
  they are needed
- use one bounded delegation wave at a time, integrate results, then decide
  whether another wave is worth it
- switch to safe-run triage if the agent runtime becomes slow, hot, swap-heavy, or
  helper-heavy

## Autonomy Rule

Do not stop early for normal questions. If there is ambiguity, missing context,
unavailable credentials, unavailable services, unclear product direction, or
uncertain tradeoffs:

1. make the best reasonable assumption
2. continue with other areas
3. queue the question in the final deliverable
4. state what the answer would unlock

Stop only if continuing would be destructive, unsafe, or impossible.

## Implementation Rule

Go as far as the current permission level allows.

If the run is audit-only:

- do not edit files
- produce the strongest possible roadmap and next-pass prompt

If code changes are allowed:

- after the first audit and prioritization loop, implement the highest-confidence,
  lowest-risk improvements first
- prefer improvements that are visible, reversible, testable, and high-leverage
- do not make production changes, deploy, rotate secrets, change database
  permissions, alter billing, or touch risky account-level configuration without
  explicit approval
- queue risky or product-decision-heavy items instead of stopping

## Required Loops

Run several improvement loops, not a single pass.

### Loop 1: Understand

Map repos, app structure, routes, users, flows, design system, styles,
components, tests, scripts, and docs. Identify what the product appears to be
and who it serves. Classify the work, state the objective and success bar, and
make an explicit orchestration/delegation decision before widening the work.

### Loop 2: Scan

Use cheaper agents or bounded parallel scans across UI/UX, design, copy, code
quality, testing, graphics, performance, accessibility, and developer
experience. Gather evidence, screenshots where useful, file paths, routes,
components, test commands, and examples. For broad or high-cost runs, prefer a
bounded subagent or delegated-thread scan for at least one independent slice,
then integrate that output centrally.

### Loop 3: Ideate

Generate many improvement ideas. Include conservative fixes, medium creative
improvements, and bold product-quality bets. Require weak ideas to be rejected,
not just omitted.

### Loop 4: Select

The main agent reviews the ideas, rejects weak or generic ideas, combines strong
ideas, and chooses the best product direction and first implementation batch.

### Loop 5: Validate

Run targeted checks against the chosen direction. Look for risks, missing
context, better variants, and implementation traps. If implementation is
allowed, make changes and verify them. If implementation is not allowed, produce
a concrete next-pass implementation plan. Use sidecar subagents or delegated
threads for focused verification/log reduction/code review when they can run in
parallel without blocking the main implementation path.

### Loop 6: Refine

Re-prioritize based on evidence and verification. Queue unresolved questions.
Review and reconcile delegated outputs, inspect important diffs or artifacts
yourself, close or summarize worker threads when appropriate, and produce a
final roadmap and next-pass prompt.

## Focus Areas

Inspect the areas that fit the project:

- product clarity and user value
- target audience fit
- core workflows and friction
- UI layout, hierarchy, density, and scanability
- visual style, taste level, polish, and consistency
- typography, spacing, color, contrast, and rhythm
- components, design system, patterns, and duplicated UI
- graphics, illustrations, icons, imagery, charts, and visual storytelling
- delight, microinteractions, feedback, animation, personality, and memorable
  moments
- copy, tone, labels, CTAs, helper text, errors, empty states, and trust language
- onboarding, setup, first-run experience, and activation
- forms, modals, tables, dashboards, navigation, and settings
- mobile, responsive behavior, accessibility, keyboard, and focus risks
- code quality, maintainability, naming, organization, and architecture
- testing gaps, fragile flows, missing coverage, and QA blind spots
- performance, loading behavior, perceived speed, and failure recovery
- developer experience, local setup, CI, scripts, and documentation
- obvious trust and security issues only where they affect product confidence

## Subagent Return Format

Each delegated slice should return:

- area reviewed
- files, routes, or screens inspected
- evidence
- findings
- best improvement ideas
- weak ideas rejected
- assumptions made
- blockers encountered
- questions and checkpoints queued
- confidence level
- what still needs main-agent judgment

## Final Deliverable

Use this shape, trimmed to fit the work actually performed.

### Project Quality Summary

- What this project appears to be:
- Primary users/audiences:
- Current strengths:
- Current weaknesses:
- Best overall improvement direction:
- Biggest UX opportunities:
- Biggest design/style opportunities:
- Biggest code-quality opportunities:
- Biggest testing gaps:
- Biggest delight opportunities:
- Confidence level:
- Repos/surfaces reviewed:
- Repos/surfaces not reviewed and why:

### Work Completed

- Files changed, if implementation was allowed:
- Commands run:
- Tests/checks run:
- Screenshots/browser checks, if any:
- Proof gathered:
- Orchestrator-mode/delegation decision:
- Subagents or delegated threads used:
- Delegated outputs reviewed:
- What was intentionally not changed:

### Top Prioritized Recommendations

For each recommendation:

- ID:
- Priority: P0 / P1 / P2 / P3
- Category: UX / Design / Copy / Code Quality / Testing / Graphics / Delight /
  Performance / Accessibility / DevEx
- Recommendation:
- Evidence:
- Why it matters:
- User impact:
- Proposed solution:
- Creative alternative:
- Tradeoffs:
- Estimated effort:
- Validation plan:
- Assumptions:
- Queued questions/checkpoints:

### Creative Opportunities

- Visual identity opportunities:
- Interaction/delight opportunities:
- Graphics or imagery opportunities:
- Copy and tone opportunities:
- Product-flow opportunities:
- Would-make-this-feel-premium opportunities:

### Code And Testing Opportunities

- Code quality issues:
- Maintainability risks:
- Areas that feel overcomplicated:
- Areas that need better tests:
- Suggested test coverage:
- Suggested refactors:
- Developer-experience improvements:

### Iteration Notes

- Loops completed:
- Orchestration/delegation decision:
- Subagents/thread delegations launched:
- How delegated work was monitored and reviewed:
- Improvement directions considered:
- Ideas rejected and why:
- Ideas combined:
- Final direction chosen:
- Remaining uncertainty:

### Roadmap

- Immediate polish, 0-2 days:
- High-leverage improvements, 1-2 weeks:
- Systematic cleanup, 2-4 weeks:
- Larger creative bets:

### Validation Plan

- Browser/screenshots to capture:
- Responsive checks:
- Accessibility checks:
- Test commands:
- User-flow checks:
- Design review checks:

### Questions And Checkpoints For Next Pass

For each item:

- Question/checkpoint:
- Why it matters:
- What answer would unlock:
- Current assumption:
- Recommended next action if confirmed:
- Recommended next action if rejected:

### Deferred Or Blocked Areas

For each area:

- Area:
- What blocked deeper review:
- What was still reviewed:
- Risk of missing context:
- How to resume:

### Next-Pass Prompt

Write a concise follow-up prompt the user can paste back in after answering the
checkpoint questions so the next agent can continue from this audit without
starting over.
