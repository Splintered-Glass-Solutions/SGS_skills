#!/usr/bin/env bash
set -euo pipefail

interval=5
log_file=""
once=0

usage() {
  cat <<'USAGE'
Usage:
  agent-safe-monitor.sh --once
  agent-safe-monitor.sh [--log /tmp/agent-safe-monitor.log] [--interval 5]

Writes compact the agent memory/process snapshots. It does not kill processes.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --once)
      once=1
      shift
      ;;
    --log)
      log_file="${2:-}"
      shift 2
      ;;
    --interval)
      interval="${2:-5}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

snapshot() {
  printf '\n=== %s ===\n' "$(date '+%Y-%m-%d %H:%M:%S')"
  sysctl vm.swapusage 2>/dev/null || true
  memory_pressure 2>/dev/null | awk '/System-wide memory free percentage|Pages free|Pages used by compressor/ {print}' || true
  printf '%-8s %-8s %-8s %-10s %-10s %s\n' PID PPID CPU RSS_MB ELAPSED LABEL
  ps -axo pid,ppid,%cpu,rss,etime,command |
    awk '
      BEGIN { IGNORECASE=1 }
      /the agent|agent|mcp\/server|node_repl|playwright-mcp|SkyComputerUse|Computer Use/ && !/awk/ {
        label=$0
        sub(/^ *[0-9]+ +[0-9]+ +[0-9.]+ +[0-9]+ +[^ ]+ +/, "", label)
        if (label ~ /app-server --analytics-default-enabled/) label="agent app-server analytics"
        else if (label ~ /app-server --listen/) label="agent app-server thread"
        else if (label ~ /the agent \(Renderer\)/) label="the agent Renderer"
        else if (label ~ /the agent \(Service\)/) label="the agent Service"
        else if (label ~ /mcp\/server/) label="MCP server"
        else if (label ~ /node_repl/) label="node_repl"
        else if (label ~ /SkyComputerUse|Computer Use/) label="Computer Use helper"
        else if (label ~ /Contents\/MacOS\/the agent$/) label="the agent main"
        printf "%-8s %-8s %-8s %-10.1f %-10s %s\n", $1, $2, $3, $4/1024, $5, label
      }
    ' |
    sort -nrk4 |
    head -30
}

if [[ "$once" -eq 1 ]]; then
  snapshot
  exit 0
fi

if [[ -z "$log_file" ]]; then
  log_file="/tmp/agent-safe-monitor.log"
fi

while true; do
  snapshot >> "$log_file"
  sleep "$interval"
done
