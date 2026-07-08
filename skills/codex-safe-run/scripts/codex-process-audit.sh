#!/usr/bin/env bash
set -euo pipefail

cat <<'HEADER'
Codex Process Audit
This script only reports process groups. It does not kill anything.
HEADER

printf '\nSwap and memory pressure:\n'
sysctl vm.swapusage 2>/dev/null || true
memory_pressure 2>/dev/null | awk '/System-wide memory free percentage|Pages free|Pages used by compressor/ {print}' || true

printf '\nCodex roots:\n'
pgrep -alf 'Codex.app/Contents/MacOS/Codex|codex app-server --analytics-default-enabled' || true

printf '\nCodex/helper process groups:\n'
ps -axo pid,ppid,pgid,%cpu,rss,etime,stat,command |
  awk 'BEGIN{IGNORECASE=1} /Codex|codex|mcp\/server|node_repl|playwright-mcp|SkyComputerUse|Computer Use|gh pr checks --watch| yes / && !/awk/ {print}' |
  sort -nk3,3 -nrk5,5

printf '\nLikely noisy watchers or infinite loops:\n'
pgrep -alf 'gh pr checks .*--watch| yes | watch ' || true
