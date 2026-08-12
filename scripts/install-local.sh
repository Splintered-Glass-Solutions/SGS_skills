#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

command -v rsync >/dev/null 2>&1 || {
  echo "rsync is required to install the archived resources." >&2
  exit 1
}

mkdir -p "$CODEX_HOME/skills" "$CODEX_HOME/commands" "$CODEX_HOME/portfolio/templates"

for skill_dir in "$ROOT"/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"

  # Preserve current local folder names for PM skills whose SKILL.md names were
  # prefixed after the original command wrappers were created.
  case "$skill_name" in
    pm-delegate) target_name="delegate" ;;
    pm-clean-unreads) target_name="clean-unreads" ;;
    pm-plate-spin) target_name="plate-spin" ;;
    pm-project-portfolio-manager) target_name="project-portfolio-manager" ;;
    *) target_name="$skill_name" ;;
  esac

  rsync -a "$skill_dir/" "$CODEX_HOME/skills/$target_name/"
done

rsync -a "$ROOT/commands/" "$CODEX_HOME/commands/"
rsync -a "$ROOT/portfolio/templates/" "$CODEX_HOME/portfolio/templates/"

echo "Installed archived skills, commands, and templates into $CODEX_HOME"
echo "Existing local files were preserved unless the same archived path was updated."
