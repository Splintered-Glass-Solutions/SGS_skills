#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-/Users/preston/.codex}"

mkdir -p "$CODEX_HOME/skills" "$CODEX_HOME/commands" "$CODEX_HOME/portfolio/templates"

rsync -a "$ROOT/skills/pm-delegate/" "$CODEX_HOME/skills/delegate/"
rsync -a "$ROOT/skills/pm-clean-unreads/" "$CODEX_HOME/skills/clean-unreads/"
rsync -a "$ROOT/skills/pm-plate-spin/" "$CODEX_HOME/skills/plate-spin/"
rsync -a "$ROOT/skills/pm-project-portfolio-manager/" "$CODEX_HOME/skills/project-portfolio-manager/"
rsync -a "$ROOT/skills/pm-comms-check/" "$CODEX_HOME/skills/pm-comms-check/"
rsync -a "$ROOT/skills/pm-comms-sync/" "$CODEX_HOME/skills/pm-comms-sync/"
rsync -a "$ROOT/commands/" "$CODEX_HOME/commands/"
rsync -a "$ROOT/portfolio/templates/" "$CODEX_HOME/portfolio/templates/"

echo "Installed PM skills, commands, and templates into $CODEX_HOME"

