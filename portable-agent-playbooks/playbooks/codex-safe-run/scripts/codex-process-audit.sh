#!/usr/bin/env bash
set -euo pipefail

cat <<'HEADER'
the agent Process Audit
This script only reports process groups. It does not kill anything.
HEADER

printf '\nSwap and memory pressure:\n'
sysctl vm.swapusage 2>/dev/null || true
memory_pressure 2>/dev/null | awk '/System-wide memory free percentage|Pages free|Pages used by compressor/ {print}' || true

printf '\nthe agent roots:\n'
pgrep -alf 'the agent.app/Contents/MacOS/the agent|agent app-server --analytics-default-enabled' || true

printf '\nthe agent/helper process groups:\n'
ps -axo pid,ppid,pgid,%cpu,rss,etime,stat,command |
  awk 'BEGIN{IGNORECASE=1} /the agent|agent|mcp\/server|node_repl|playwright-mcp|SkyComputerUse|Computer Use|gh pr checks --watch| yes / && !/awk/ {print}' |
  sort -nk3,3 -nrk5,5

printf '\nLikely noisy watchers or infinite loops:\n'
pgrep -alf 'gh pr checks .*--watch| yes | watch ' || true
