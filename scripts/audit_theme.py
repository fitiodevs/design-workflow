#!/usr/bin/env python3
"""
Stack-aware theme auditor.

Loads regex pattern sets from `scripts/audit_lint_sets/<stack>.yaml` based
on the resolved `--stack` flag (or env STACK / config.stack via
`scripts/resolve_stack.py`). WCAG contrast logic stays in
`scripts/check_contrast.py` — color math is stack-agnostic.

Detected (Flutter, default lint set):
  - Color(0xFF...) outside lib/core/theme/
  - Colors.<name> in widgets
  - fontSize / fontWeight literals
  - EdgeInsets / BorderRadius numbers off-scale
  - Anti-slop copy patterns (filler, cliche, em-dash, etc.)

Detected (Next.js+Tailwind):
  - text-[#...], bg-[#...], border-[#...] arbitrary values
  - inline style={...} with hex
  - hsl() / hex literals in JSX
  - Generic placeholder names

Usage:
    python3 scripts/audit_theme.py                          # current stack, defaults
    python3 scripts/audit_theme.py --stack flutter
    python3 scripts/audit_theme.py --stack nextjs-tailwind <path>
    python3 scripts/audit_theme.py --summary
    python3 scripts/audit_theme.py --fail
    python3 scripts/audit_theme.py --no-slop
"""
from __future__ import annotations
import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", REPO_ROOT.parent))
LINT_SETS_DIR = REPO_ROOT / "scripts" / "audit_lint_sets"
AVAILABLE_STACKS = ("flutter", "nextjs-tailwind", "react-native")


def _load_lint_set(stack: str) -> dict:
    path = LINT_SETS_DIR / f"{stack}.yaml"
    if not path.exists():
        raise SystemExit(
            f"Error: lint set for stack '{stack}' not found at {path}. "
            f"Available: {', '.join(AVAILABLE_STACKS)}"
        )
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        raise SystemExit("Error: PyYAML required. Install with `pip install pyyaml`.")
    return yaml.safe_load(path.read_text())


def _compile(pattern_dict: dict, flags_dict: dict | None = None) -> dict[str, re.Pattern]:
    flags_dict = flags_dict or {}
    out: dict[str, re.Pattern] = {}
    for name, pat in (pattern_dict or {}).items():
        flag = 0
        for f in (flags_dict.get(name) or "").split("|"):
            f = f.strip()
            if f == "IGNORECASE":
                flag |= re.IGNORECASE
            elif f == "MULTILINE":
                flag |= re.MULTILINE
            elif f == "DOTALL":
                flag |= re.DOTALL
        out[name] = re.compile(pat, flag)
    return out


def _is_allowed(rule: str, rel_path: str, lint: dict) -> bool:
    if rule in {"hex_color", "tailwind_arbitrary_text", "tailwind_arbitrary_bg",
                "tailwind_arbitrary_border", "inline_style_hex", "hex_in_tsx"}:
        return any(rel_path.endswith(p) or rel_path == p for p in lint.get("allow_hex_in", []))
    if rule == "material_color":
        return any(rel_path.endswith(p) for p in lint.get("allow_colors_in", []))
    return False


def _extract_numbers(s: str) -> list[float]:
    return [float(n) for n in re.findall(r"\d+(?:\.\d+)?", s)]


def _filter_off_scale(match: str, allowed: list[float]) -> bool:
    if not allowed:
        return True
    nums = _extract_numbers(match)
    return any(n not in allowed for n in nums)


def _walk(root: Path, lint: dict):
    exts = tuple(lint["file_extensions"])
    bad_suffixes = tuple(lint.get("exclude_suffixes", []))
    for dirpath, _, files in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root) if str(dirpath).startswith(str(root)) else Path(dirpath)
        if any(skip.rstrip("/") in str(rel_dir).split(os.sep) for skip in lint.get("slop_skip", [])
               if skip.endswith("/")):
            continue
        for name in files:
            if not name.endswith(exts):
                continue
            if any(name.endswith(suf) for suf in bad_suffixes):
                continue
            yield Path(dirpath) / name


def _scan_file(path: Path, scan_root: Path, lint: dict, structural: dict[str, re.Pattern],
               slop: dict[str, re.Pattern], check_slop: bool) -> dict[str, list[tuple[int, str]]]:
    hits: dict[str, list[tuple[int, str]]] = defaultdict(list)
    rel = str(path.relative_to(scan_root)).replace(os.sep, "/")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return hits

    slop_active = check_slop and not any(skip in rel for skip in lint.get("slop_skip", []))
    allowed_spacing = lint.get("allowed_spacing", [])
    allowed_radius = lint.get("allowed_radius", [])

    for i, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith(("//", "#")):
            continue
        for rule, pattern in structural.items():
            if _is_allowed(rule, rel, lint):
                continue
            for m in pattern.finditer(line):
                text = m.group(0)
                if rule == "edge_insets_literal" and not _filter_off_scale(text, allowed_spacing):
                    continue
                if rule == "radius_literal" and not _filter_off_scale(text, allowed_radius):
                    continue
                hits[rule].append((i, line.rstrip()))
        if slop_active:
            for rule, pattern in slop.items():
                if pattern.search(line):
                    hits[rule].append((i, line.rstrip()))
    return hits


def _resolve_stack_from_env() -> str:
    env = os.environ.get("STACK", "").strip()
    if env:
        return env
    return "flutter"


def main() -> int:
    parser = argparse.ArgumentParser(description="design-workflow stack-aware audit")
    parser.add_argument("--stack", choices=AVAILABLE_STACKS, default=None,
                        help="Active stack lint set. Default: STACK env or 'flutter'.")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--fail", dest="fail_on_hit", action="store_true")
    parser.add_argument("--no-slop", action="store_true")
    parser.add_argument("path", nargs="?", default=None)
    args = parser.parse_args()

    stack = args.stack or _resolve_stack_from_env()
    if stack not in AVAILABLE_STACKS:
        print(f"Error: unknown stack '{stack}'. Available: {', '.join(AVAILABLE_STACKS)}", file=sys.stderr)
        return 2

    lint = _load_lint_set(stack)
    structural = _compile(lint.get("structural", {}))
    slop = _compile(lint.get("slop", {}), lint.get("slop_flags", {}))

    scan_root = Path(args.path).resolve() if args.path else (PROJECT_ROOT / lint.get("default_scan", ".")).resolve()
    if not scan_root.exists():
        print(f"Note: scan root {scan_root} does not exist (skill repo without project context). "
              f"Use --stack and a path arg, or set PROJECT_ROOT.", file=sys.stderr)
        return 0

    totals: dict[str, int] = defaultdict(int)
    per_file: dict[str, dict[str, list[tuple[int, str]]]] = {}
    for path in _walk(scan_root, lint):
        hits = _scan_file(path, scan_root, lint, structural, slop, check_slop=not args.no_slop)
        if any(hits.values()):
            rel = str(path.relative_to(scan_root)).replace(os.sep, "/")
            per_file[rel] = hits
            for rule, xs in hits.items():
                totals[rule] += len(xs)

    rel_root = str(scan_root.relative_to(scan_root.parent) if scan_root != Path("/") else scan_root)
    print(f"\n=== audit em {rel_root}  [stack: {stack}] ===\n")

    if not per_file:
        print("✅ Nenhuma violação encontrada.")
        return 0

    if not args.summary:
        for rel, hits in sorted(per_file.items()):
            total = sum(len(xs) for xs in hits.values())
            print(f"📄 {rel}  ({total})")
            for rule, xs in hits.items():
                for line_no, line in xs:
                    print(f"   {rule:>26}  L{line_no:<5}  {line.strip()[:90]}")
            print()

    if structural:
        print("Totais por regra (estrutural):")
        for rule in structural:
            print(f"  {rule:>26}: {totals.get(rule, 0)}")

    if not args.no_slop and slop:
        slop_total = sum(totals.get(r, 0) for r in slop)
        if slop_total:
            print("\nTotais por regra (anti-slop):")
            for rule in slop:
                print(f"  {rule:>26}: {totals.get(rule, 0)}")

    total_hits = sum(totals.values())
    print(f"\n📊 {total_hits} violações em {len(per_file)} arquivos")
    return 1 if (args.fail_on_hit and total_hits) else 0


if __name__ == "__main__":
    sys.exit(main())
