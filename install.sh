#!/usr/bin/env bash
# Install design-workflow skills into ~/.claude/skills/
# Re-runnable: existing destination directories are replaced.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${HOME}/.claude/skills"

if [ ! -d "${SCRIPT_DIR}/skills" ]; then
  echo "error: skills/ directory not found in ${SCRIPT_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET}"

count=0
for src in "${SCRIPT_DIR}/skills"/*/; do
  name="$(basename "${src}")"
  dest="${TARGET}/${name}"
  rm -rf "${dest}"
  cp -R "${src}" "${dest}"
  echo "  installed: ${name}"
  count=$((count + 1))
done

echo ""
echo "✓ installed ${count} skill(s) into ${TARGET}"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code in a Flutter project"
echo "  2. (Optional) Drop config.example.yaml as .design-workflow.yaml in the project root"
echo "  3. Try: /theme-audit  (or /Lupa)"
