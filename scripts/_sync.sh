#!/usr/bin/env bash
# Sync canonical scripts/ into each skill's scripts/ subdir.
# Source of truth: <repo>/scripts/<x>.py
# Target:          <repo>/skills/<skill>/scripts/<x>.py (committed copies)
#
# Run manually before commit, or wire as a pre-commit hook later.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Map: <script-filename> => <space-separated list of consuming skills>
declare -A USAGE=(
  [audit_theme.py]="theme-audit theme-critique"
  [check_contrast.py]="theme-audit theme-extend theme-create"
  [generate_palette.py]="theme-create"
  [oklch_to_hex.py]="theme-create theme-extend"
  [detect_mode.py]="theme-critique"
)

count=0
for script in "${!USAGE[@]}"; do
  src="${ROOT}/scripts/${script}"
  if [ ! -f "${src}" ]; then
    echo "warn: missing source ${src}" >&2
    continue
  fi
  for skill in ${USAGE[$script]}; do
    dest_dir="${ROOT}/skills/${skill}/scripts"
    mkdir -p "${dest_dir}"
    cp "${src}" "${dest_dir}/${script}"
    count=$((count + 1))
  done
done

echo "✓ synced ${count} script copy(ies) into skills/*/scripts/"
