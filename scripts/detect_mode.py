#!/usr/bin/env python3
"""Detect greenfield vs brownfield Flutter repo for `/juri` discovery sizing.

Heuristic (REQ-A2.1):
- greenfield  if commits<10 AND dart_files<5 AND no docs/product.md (>2KB)
- brownfield  otherwise

Outputs JSON to stdout. Used by `theme-critique` skill in discovery mode.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _git_commit_count(cwd: Path) -> int:
    try:
        out = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return int((out.stdout or "0").strip() or "0")
    except (subprocess.SubprocessError, ValueError, FileNotFoundError):
        return 0


def _dart_files(lib_dir: Path) -> int:
    if not lib_dir.exists():
        return 0
    count = 0
    for p in lib_dir.rglob("*.dart"):
        s = str(p)
        if "generated" in s or s.endswith(".g.dart") or s.endswith(".freezed.dart"):
            continue
        count += 1
    return count


def _has_product_md(repo_root: Path) -> bool:
    p = repo_root / "docs" / "product.md"
    return p.exists() and p.stat().st_size > 2000


def _has_theme_dir(repo_root: Path) -> bool:
    for rel in ("lib/core/theme", "lib/theme", "lib/shared/theme", "lib/design_system"):
        if (repo_root / rel).exists():
            return True
    return False


def detect(repo_root: str | os.PathLike[str] = ".") -> dict:
    root = Path(repo_root).resolve()
    commits = _git_commit_count(root)
    dart_files = _dart_files(root / "lib")
    has_product = _has_product_md(root)
    has_theme = _has_theme_dir(root)

    is_greenfield = commits < 10 and dart_files < 5 and not has_product

    return {
        "mode": "greenfield" if is_greenfield else "brownfield",
        "tier_recommended": "greenfield" if is_greenfield else "full",
        "signals": {
            "commits": commits,
            "dart_files": dart_files,
            "has_product_md": has_product,
            "has_theme_dir": has_theme,
        },
        "repo_root": str(root),
    }


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(detect(target), indent=2))
