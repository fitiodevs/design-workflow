#!/usr/bin/env bash
# Remove design-workflow skills from ~/.claude/skills/
# Only removes skills present in this repo's skills/ folder — leaves
# unrelated skills untouched.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${HOME}/.claude/skills"

if [ ! -d "${SCRIPT_DIR}/skills" ]; then
  echo "error: skills/ directory not found in ${SCRIPT_DIR}" >&2
  exit 1
fi

count=0
for src in "${SCRIPT_DIR}/skills"/*/; do
  name="$(basename "${src}")"
  dest="${TARGET}/${name}"
  if [ -d "${dest}" ]; then
    rm -rf "${dest}"
    echo "  removed: ${name}"
    count=$((count + 1))
  fi
done

echo ""
echo "✓ removed ${count} skill(s) from ${TARGET}"
