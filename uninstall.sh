#!/usr/bin/env bash
# Remove design-workflow skills from ~/.claude/skills/ and agents from ~/.claude/agents/.
# Only removes items present in this repo's skills/ and agents/ folders —
# leaves unrelated skills/agents untouched.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_TARGET="${HOME}/.claude/skills"
AGENT_TARGET="${HOME}/.claude/agents"

if [ ! -d "${SCRIPT_DIR}/skills" ]; then
  echo "error: skills/ directory not found in ${SCRIPT_DIR}" >&2
  exit 1
fi

count=0
for src in "${SCRIPT_DIR}/skills"/*/; do
  name="$(basename "${src}")"
  dest="${SKILL_TARGET}/${name}"
  if [ -d "${dest}" ]; then
    rm -rf "${dest}"
    echo "  removed skill: ${name}"
    count=$((count + 1))
  fi
done

agent_count=0
if [ -d "${SCRIPT_DIR}/agents" ]; then
  for entry in "${SCRIPT_DIR}/agents"/*.md; do
    [ -f "${entry}" ] || continue
    name="$(basename "${entry}" .md)"
    removed=0
    if [ -f "${AGENT_TARGET}/${name}.md" ]; then
      rm -f "${AGENT_TARGET}/${name}.md"
      removed=1
    fi
    if [ -d "${AGENT_TARGET}/${name}" ]; then
      rm -rf "${AGENT_TARGET}/${name}"
      removed=1
    fi
    if [ "${removed}" -eq 1 ]; then
      echo "  removed agent: ${name}"
      agent_count=$((agent_count + 1))
    fi
  done
fi

echo ""
echo "✓ removed ${count} skill(s) from ${SKILL_TARGET}"
if [ "${agent_count}" -gt 0 ]; then
  echo "✓ removed ${agent_count} agent(s) from ${AGENT_TARGET}"
fi
