#!/usr/bin/env bash
# Install design-workflow skills into ~/.claude/skills/ and craft/ docs into ~/.claude/craft/.
# Re-runnable: existing destination directories are replaced.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_TARGET="${HOME}/.claude/skills"
CRAFT_TARGET="${HOME}/.claude/craft"

if [ ! -d "${SCRIPT_DIR}/skills" ]; then
  echo "error: skills/ directory not found in ${SCRIPT_DIR}" >&2
  exit 1
fi

mkdir -p "${SKILL_TARGET}"

count=0
for src in "${SCRIPT_DIR}/skills"/*/; do
  name="$(basename "${src}")"
  dest="${SKILL_TARGET}/${name}"
  rm -rf "${dest}"
  cp -R "${src}" "${dest}"
  echo "  installed: ${name}"
  count=$((count + 1))
done

# craft/ — universal design rule docs loaded by 5 wired skills
# (theme-critique, theme-create, theme-port, theme-bolder, frontend-design).
# The skills reference these as `craft/<doc>.md` (project-relative); since
# install lands them globally outside any project, we copy craft/ to a stable
# global location and rewrite the references in the installed SKILL.md copies
# to absolute paths so the model can resolve them from any cwd.
craft_count=0
if [ -d "${SCRIPT_DIR}/craft" ]; then
  rm -rf "${CRAFT_TARGET}"
  mkdir -p "${CRAFT_TARGET}"
  cp "${SCRIPT_DIR}/craft"/*.md "${CRAFT_TARGET}/"
  craft_count=$(ls "${CRAFT_TARGET}"/*.md 2>/dev/null | wc -l)
  echo ""
  echo "  installed: craft/ (${craft_count} docs → ${CRAFT_TARGET})"

  for s in theme-critique theme-create theme-port theme-bolder frontend-design; do
    skill_md="${SKILL_TARGET}/${s}/SKILL.md"
    if [ -f "${skill_md}" ]; then
      # `craft/anti-ai-slop.md` → `~/.claude/craft/anti-ai-slop.md`
      sed -i.bak 's|`craft/\([a-z-]*\)\.md`|`~/.claude/craft/\1.md`|g' "${skill_md}"
      rm -f "${skill_md}.bak"
    fi
  done
  echo "  rewrote: craft/ refs → ~/.claude/craft/ in 5 wired skills"
fi

echo ""
echo "✓ installed ${count} skill(s) into ${SKILL_TARGET}"
if [ "${craft_count}" -gt 0 ]; then
  echo "✓ installed ${craft_count} craft doc(s) into ${CRAFT_TARGET}"
fi
echo "  scripts bundled per skill (sourced from <repo>/scripts/ via _sync.sh)"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code in a Flutter project"
echo "  2. (Optional) Drop config.example.yaml as .design-workflow.yaml in the project root"
echo "  3. Try: /theme-audit  (or /Lupa, or /Auditor)"
