#!/usr/bin/env bash
# Install multi-asset-trader-skills into ~/.claude/skills
# Usage: ./install.sh [--copy]
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MODE="link"
[[ "${1:-}" == "--copy" ]] && MODE="copy"

mkdir -p "$TARGET"
count=0
for skill_md in "$REPO_DIR"/skills/*/*/SKILL.md; do
  skill_dir="$(dirname "$skill_md")"
  name="$(basename "$skill_dir")"
  dest="$TARGET/$name"
  rm -rf "$dest"
  if [[ "$MODE" == "copy" ]]; then
    cp -R "$skill_dir" "$dest"
  else
    ln -s "$skill_dir" "$dest"
  fi
  count=$((count+1))
done
echo "Installed $count skills into $TARGET ($MODE mode)."
echo "Next: connect Lexfi MCP (docs/lexfi-mcp.md), then ask Claude: \"Find me opportunities.\""
