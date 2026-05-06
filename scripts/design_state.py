#!/usr/bin/env python3
"""design-state — inspect current state of design-spec-driven workflow.

Outputs current feature, phase, task, blocked tasks, last commit.
Reads `.design-spec/features/*/{discovery,compose,sequence,ship}-log.md` + tasks.md.

Usage:
  python scripts/design_state.py             # all features, prose
  python scripts/design_state.py --feature X # one feature
  python scripts/design_state.py --json      # machine-readable
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DESIGN_SPEC = Path(".design-spec")
PHASE_FILES = ("discovery.md", "compose.md", "tasks.md", "ship-log.md")


def _frontmatter(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def _last_commit() -> dict:
    try:
        sha = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        msg = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        return {"sha": sha[:8], "message": msg} if sha else {}
    except (subprocess.SubprocessError, FileNotFoundError):
        return {}


def _parse_tasks(tasks_md: Path) -> dict:
    if not tasks_md.exists():
        return {"tasks": [], "in_progress": None, "blocked": [], "done": 0, "pending": 0}
    text = tasks_md.read_text(encoding="utf-8", errors="replace")
    tasks = []
    for m in re.finditer(r"-\s*id:\s*(T-\d+)[\s\S]*?(?=\n  - id:|\Z)", text):
        block = m.group(0)
        tid = m.group(1)
        status_m = re.search(r"status:\s*(\w+)", block)
        status = status_m.group(1) if status_m else "pending"
        tasks.append({"id": tid, "status": status})
    return {
        "tasks": tasks,
        "in_progress": next((t["id"] for t in tasks if t["status"] == "in_progress"), None),
        "blocked": [t["id"] for t in tasks if t["status"] == "blocked"],
        "done": sum(1 for t in tasks if t["status"] == "done"),
        "pending": sum(1 for t in tasks if t["status"] == "pending"),
        "total": len(tasks),
    }


def feature_state(feature_dir: Path) -> dict:
    name = feature_dir.name
    state = {"feature": name, "phases": {}}
    for phase_file in PHASE_FILES:
        fm = _frontmatter(feature_dir / phase_file)
        if fm:
            state["phases"][phase_file.replace(".md", "")] = {
                "status": fm.get("status"),
                "created": fm.get("created"),
                "phase": fm.get("phase"),
            }
    state["tasks"] = _parse_tasks(feature_dir / "tasks.md")
    return state


def project_state(repo_root: Path = Path(".")) -> dict:
    features_dir = repo_root / DESIGN_SPEC / "features"
    features = []
    if features_dir.exists():
        for d in sorted(features_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                features.append(feature_state(d))
    pause = repo_root / DESIGN_SPEC / "pause-state.yaml"
    return {
        "scanned_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "last_commit": _last_commit(),
        "features": features,
        "pause_state_present": pause.exists(),
    }


def render_prose(state: dict) -> str:
    lines = [f"# design-state — {state['scanned_at']}"]
    lc = state.get("last_commit", {})
    if lc:
        lines.append(f"\nLast commit: {lc.get('sha')} — {lc.get('message')}")
    if state.get("pause_state_present"):
        lines.append("⏸  pause-state.yaml present — `/design-spec resume` to continue.")
    if not state.get("features"):
        lines.append("\nNo features yet. Run `/juri` to start discovery.")
        return "\n".join(lines)
    for f in state["features"]:
        lines.append(f"\n## {f['feature']}")
        for phase, info in f.get("phases", {}).items():
            lines.append(f"  - {phase}: {info.get('status')} (created {info.get('created')})")
        t = f.get("tasks", {})
        if t.get("total"):
            lines.append(
                f"  - tasks: {t['done']}/{t['total']} done · {t['pending']} pending · "
                f"in_progress={t['in_progress']} · blocked={t['blocked']}"
            )
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="design-state inspector")
    p.add_argument("--feature", help="Scope to one feature slug")
    p.add_argument("--json", action="store_true", help="Machine-readable JSON")
    p.add_argument("--root", default=".", help="Repo root (default cwd)")
    args = p.parse_args()
    root = Path(args.root).resolve()
    state = project_state(root)
    if args.feature:
        state["features"] = [f for f in state["features"] if f["feature"] == args.feature]
    if args.json:
        print(json.dumps(state, indent=2))
    else:
        print(render_prose(state))
    return 0


if __name__ == "__main__":
    sys.exit(main())
