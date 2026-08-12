---
name: codex-safe-run
description: Run Codex Desktop more safely on macOS when memory, swap, CPU, app-server, MCP helper, node_repl, Computer Use, Browser, or multiple-thread runaway risk is present. Use when the user says to run Codex safely, monitor Codex, use one Codex thread, investigate Codex memory leaks, avoid Codex Desktop crashes, clean up Codex helper processes, switch to CLI because Desktop is unstable, or similar.
---

# Codex Safe Run

Use this skill to keep Codex Desktop from destabilizing the Mac while still getting work done while minimizing token usage.

## Operating Contract

Prefer stability over keeping every Desktop thread alive. Treat the Codex Desktop app-server as part of the risk surface, especially:

- `/Applications/Codex.app/Contents/Resources/codex app-server --analytics-default-enabled`
- stale `codex app-server --listen stdio://`
- stale `node_repl`
- MCP helper processes such as `node ./mcp/server.bundle.mjs`
- Browser, Computer Use, Playwright, Chrome, or other UI automation helpers
- long-running streaming commands such as `watch`, `yes`, `tail -f`, `gh pr checks --watch`, and live monitors

Do not stream large process tables, full command lines, build logs, or repeated monitor output through Codex Desktop. That output is retained by the same app-server that can run away and wastes tokens.

Default to dry-run audits and compact file-backed logging. Kill processes only when:

1. the process is clearly stale or runaway,
2. killing it will not destroy active user work, and
3. the user has approved the cleanup in the current thread, or the process is an obvious accidental infinite loop that is not useful work.

## Token Budget

Minimize token usage as part of safe operation:

- Prefer one compact status update over repeated progress narration.
- Use short command output caps and write verbose logs to files.
- Read only the relevant log tail or targeted file section.
- Avoid broad `cat`, full process dumps, full test logs, and repeated watcher output.
- Summarize large outputs instead of pasting them back into the conversation.
- Run only the next necessary check; do not start broad suites, browser sessions, or MCP-heavy tools unless they are needed for the task.
- When monitoring, poll with one-shot commands or file-backed logs, then report only deltas and actionable findings.

## First Triage

If Codex is already slow, hot, crashing, or showing huge memory in Activity Monitor:

1. Capture a compact snapshot:
   - `scripts/codex-safe-monitor.sh --once`
   - `memory_pressure`
   - `sysctl vm.swapusage`
   - `ps -axo pid,ppid,pgid,%cpu,rss,etime,stat,command | sort -nrk5 | head -40`
2. If a single Codex app-server is hot, sample it before killing if the system can tolerate 5 seconds:
   - `sample PID 5 -file /tmp/codex-app-server-PID-sample.txt`
3. If swap is climbing quickly or the app-server physical footprint is multi-GB, stop interactive monitoring and tell the user to fully quit Codex Desktop.
4. After Codex quits, verify stale helpers:
   - `pgrep -alf 'Codex|codex|node_repl|mcp/server|playwright-mcp|Computer Use|SkyComputerUse'`
5. Only then restart Codex for a clean one-thread run.

Thresholds that should be treated as runaway unless explained by a known heavy command:

- Codex app-server RSS above 6 GB.
- Codex app-server CPU above 150% for more than two samples.
- Swap above 8 GB and rising.
- More than one `codex app-server --analytics-default-enabled`.
- Dozens of `node_repl`, MCP, Playwright, Browser, or Computer Use helpers after threads are idle.

## Safe One-Thread Run

For "run one single thread safely":

1. Fully quit Codex Desktop.
2. Confirm there are no old app-server roots:
   - `pgrep -alf 'codex app-server --analytics-default-enabled'`
3. If stale Codex helper processes remain, ask the user before killing them unless they are obvious orphaned/no-op monitors.
4. Reopen Codex.
5. Open only the needed thread.
6. Avoid starting extra Desktop threads, Browser/Computer Use sessions, or MCP-heavy helpers unless needed.
7. Use compact commands:
   - prefer one-shot checks over watches,
   - redirect long logs to files,
   - summarize log tails rather than streaming full output,
   - set small output limits and avoid printing unchanged repeated status.
8. If work needs long builds, CI watching, large logs, or many concurrent agents, prefer Codex CLI or a normal terminal for that part.

## Monitoring

Use the bundled monitor when possible:

```bash
$CODEX_HOME/skills/codex-safe-run/scripts/codex-safe-monitor.sh --log /tmp/codex-safe-monitor.log --interval 5
```

Read only recent compact output:

```bash
tail -80 /tmp/codex-safe-monitor.log
```

For a one-shot check:

```bash
$CODEX_HOME/skills/codex-safe-run/scripts/codex-safe-monitor.sh --once
```

Do not run verbose `while true` monitors inside Codex Desktop that print full commands every few seconds.

## Cleanup

Before cleanup, classify processes:

- Active work: build/test/deploy/gh commands the user expects.
- Stale thread workers: old `app-server --listen stdio://`, `node_repl`, MCP helpers from closed threads.
- Obvious runaway/noise: `yes`, `watch`, accidental infinite loops, stale `gh pr checks --watch`.
- App root: `Codex`, renderer/service helpers, and `app-server --analytics-default-enabled`.

Prefer this order:

1. Stop obvious runaway/noise process groups.
2. Stop stale helper process groups from closed threads.
3. Quit Codex Desktop normally.
4. If app-server survives quit or remains runaway, kill the app-server root.
5. Reopen Codex only after swap and memory pressure stabilize.

Do not kill active repo commands without explaining likely impact.

## Reporting

End with:

- Current Codex app-server PID(s), CPU, RSS, and whether more than one root exists.
- Swap used and memory free percentage.
- Largest non-Codex memory consumers if relevant.
- Stale helpers found and cleanup performed.
- Whether this was a clean one-thread baseline.
- Recommendation: continue Desktop, restart Desktop, or switch to CLI.
