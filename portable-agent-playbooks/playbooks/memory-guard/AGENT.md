# Memory Guard Agent Playbook

This is a platform-neutral version of the `memory-guard` skill. It is designed
for use with Claude, Claude Code, Cursor, OpenAI agents, or another agent
platform that supports reusable instructions.

## Trigger

Assess macOS memory pressure during sustained work, preserve in-flight operations and reduce only authorized task-owned load when measured capacity crosses a configured threshold.

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

# Memory Guard

Use this cooperative checkpoint during sustained resource-heavy work, or after a
memory-pressure/OOM warning. It is not a background watcher and cannot recover an
idle or terminated agent. Do not install a monitor merely by invoking this skill.

## Inputs and prerequisites

Supply the operating system, available diagnostic tools, task-owned processes,
checkpoint path and a minimum estimated-available-memory threshold in GB.
Choose the threshold for the machine/workload; no personal device or fixed
application-closure policy is assumed. If a threshold is missing, gather a sample
and ask for a policy before disruptive mitigation. macOS commands below are not
portable to other operating systems; use their documented equivalents there.

Example: `Use $memory-guard before this build. Take read-only macOS samples and
checkpoint if estimated available memory falls below the project-configured
threshold. Do not close applications or stop unrelated work.`

## Measure

Take compact one-shot samples at startup and resource-heavy phase boundaries.
During long active operations, use bounded asynchronous checks at a cadence suited
to the workload. Do not start a permanent process or duplicate another monitor.

On macOS, inspect `vm_stat`, `memory_pressure`, `sysctl vm.swapusage` and disk
headroom using available read-only commands. Estimate reclaimable capacity by
adding free and file-backed pages and multiplying by the reported page size;
do not double-count speculative pages. Label this an approximation, not an exact
available-RAM metric. Keep units explicit (GB = 1,000,000,000 bytes).

Record pressure, estimated capacity, swap/change, disk and responsiveness. Unknown
signals stay unknown. Swap use or low unused RAM alone does not establish active
pressure. Compare fresh samples when needed instead of acting on a stale number.

## Respond and resume

If measured capacity crosses the configured boundary or observed OOM/pressure
signals require a policy decision, preserve the current objective, worktree,
writer ownership, in-flight commands, side effects and first incomplete step.
Pause new task-owned heavy work at a safe boundary. Let non-interruptible writes
finish when safe, and reconcile uncertain mutations before retrying.

Reduce concurrency or cancel safely reversible task-owned work only within the
current request's authority. Do not kill unrelated processes, close user apps,
restart agents, stop services/databases, delete data or discard dirty work based
on this public skill. Prepare a concrete action and ask if further authority is
needed. Keep low-cost useful work moving when safe.

After recovery, take fresh samples and recheck runtime/writer state. Resume the
first incomplete step when the configured policy is satisfied and the machine is
responsive; do not replay finished work. Report sample time, evidence, exact
mitigation, remaining limits and resume state. Never claim continuous monitoring
or guaranteed automatic recovery from a one-shot sample.
