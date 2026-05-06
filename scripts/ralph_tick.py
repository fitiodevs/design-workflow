#!/usr/bin/env python3
"""ralph_tick — single iteration of the Ralph autonomy loop.

Ralph principle: dumb loop, smart prompt, hard halts. This file is the dumb loop.

Usage:
  python scripts/ralph_tick.py --tier watch --feature coupon-unlocked
  python scripts/ralph_tick.py --tier composer --feature coupon-unlocked --loop

The "smart" part is the SKILL.md prompt that the orchestration model reads when
spawned by the harness. This script is the deterministic skeleton: halt checks,
budget tracker, audit log writer, idempotency.

What this script DOES NOT do:
- Spawn Claude / Anthropic SDK calls (left to the model invoking the skill via the
  harness; this script provides scaffolding the model can call).
- Make decisions about which task to run next (the model reads tasks.md).
- Auto-merge PRs (hard rule REQ-D4.4).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

DEFAULT_BUDGET = {
    "max_tokens_per_loop": 200_000,
    "max_minutes_per_loop": 30,
    "max_usd_per_day": 5.00,
    "max_iterations_per_loop": 50,
    "cycle_window": 3,
}


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _today_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def _load_budget(repo_root: Path, tier: str) -> dict:
    bf = repo_root / "budget.yaml"
    budget = dict(DEFAULT_BUDGET)
    if not bf.exists():
        return budget
    # Minimal YAML reader to avoid PyYAML dependency. Supports flat keys + tier overrides.
    section = None
    for raw in bf.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("tiers:"):
            section = "tiers"
            continue
        if section == "tiers" and not line.startswith(" "):
            section = None
        stripped = line.strip()
        if section is None and ":" in stripped:
            k, _, v = stripped.partition(":")
            v = v.strip()
            if v:
                budget[k.strip()] = _coerce(v)
        elif section == "tiers" and line.startswith(f"  {tier}:"):
            section = f"tiers.{tier}"
        elif section == f"tiers.{tier}" and line.startswith("    ") and ":" in stripped:
            k, _, v = stripped.partition(":")
            budget[k.strip()] = _coerce(v.strip())
        elif section and section.startswith("tiers.") and line.startswith("  ") and ":" in stripped and not line.startswith("    "):
            section = "tiers"
    return budget


def _coerce(s: str):
    s = s.strip().strip('"').strip("'")
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s


def _halt_file_present(repo_root: Path) -> bool:
    return (repo_root / ".design-spec" / "halt").exists()


def _audit_log_path(repo_root: Path, feature: str) -> Path:
    p = repo_root / ".design-spec" / "features" / feature / "loop-log"
    p.mkdir(parents=True, exist_ok=True)
    return p / f"{_today_utc()}.jsonl"


def _append_log(path: Path, entry: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")


def _last_commit_sha(repo_root: Path) -> str | None:
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            cwd=repo_root, capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip()[:8] or None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


class BudgetState:
    def __init__(self, caps: dict):
        self.caps = caps
        self.tokens = 0
        self.usd = 0.0
        self.ticks = 0
        self.start = time.monotonic()

    @property
    def minutes(self) -> float:
        return (time.monotonic() - self.start) / 60.0

    def snapshot(self) -> dict:
        return {
            "tokens": self.tokens,
            "usd": round(self.usd, 4),
            "ticks": self.ticks,
            "minutes": round(self.minutes, 2),
            "caps": self.caps,
        }

    def add(self, tokens: int = 0, usd: float = 0.0):
        self.tokens += tokens
        self.usd += usd
        self.ticks += 1

    def status(self) -> tuple[str, str | None]:
        for cap_key, current in (
            ("max_tokens_per_loop", self.tokens),
            ("max_usd_per_day", self.usd),
            ("max_iterations_per_loop", self.ticks),
        ):
            if cap_key in self.caps and current >= self.caps[cap_key]:
                return "halt", f"budget_exceeded:{cap_key}"
        if self.minutes >= self.caps.get("max_minutes_per_loop", 9999):
            return "halt", "budget_exceeded:minutes"
        for cap_key, current in (
            ("max_tokens_per_loop", self.tokens),
            ("max_usd_per_day", self.usd),
            ("max_iterations_per_loop", self.ticks),
        ):
            if cap_key in self.caps and current >= 0.8 * self.caps[cap_key]:
                return "warn", f"budget_80pct:{cap_key}"
        return "ok", None


def tick(args, repo_root: Path, budget: BudgetState, log_path: Path, loop_id: str) -> dict:
    """Run a single tick. Returns entry dict (already appended to log)."""
    tick_index = budget.ticks + 1
    entry: dict = {
        "ts": _now_iso(),
        "tier": args.tier,
        "tick_index": tick_index,
        "loop_id": loop_id,
        "task_id": None,
        "skill": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost_usd": 0.0,
        "duration_ms": 0,
        "verify_result": "n/a",
        "verify_command": None,
        "commit_hash": _last_commit_sha(repo_root),
        "halt_reason": None,
        "files_touched": [],
        "warnings": [],
    }

    if _halt_file_present(repo_root):
        entry["halt_reason"] = "halt_file"
        _append_log(log_path, entry)
        return entry

    bstatus, breason = budget.status()
    if bstatus == "halt":
        entry["halt_reason"] = breason
        _append_log(log_path, entry)
        return entry
    if bstatus == "warn":
        entry["warnings"].append(breason)

    # The actual skill spawn + verify is performed by the orchestration model
    # invoking this skill via the harness. This script provides the skeleton;
    # the model is expected to:
    #   1. Read SKILL.md tier section.
    #   2. Re-load voice_dna.
    #   3. Pick the next task (Tier 3) or audit/critique target (Tier 1/2).
    #   4. Spawn the skill, capture verify result.
    #   5. Update budget (call this script with --report tokens=N usd=X).
    #
    # In CI, the GH Action wraps this via `claude-action` (or equivalent) that
    # passes tier + feature + budget caps to the model.

    entry["warnings"].append("skeleton_tick: actual skill spawn happens via harness model")
    budget.add(tokens=0, usd=0.0)
    _append_log(log_path, entry)
    return entry


def main() -> int:
    p = argparse.ArgumentParser(description="Ralph autonomy loop tick")
    p.add_argument("--tier", required=True, choices=["watch", "mechanical", "composer"])
    p.add_argument("--feature", required=True, help="Feature slug")
    p.add_argument("--loop", action="store_true", help="Run until halt or budget")
    p.add_argument("--root", default=".", help="Repo root")
    args = p.parse_args()

    repo_root = Path(args.root).resolve()
    caps = _load_budget(repo_root, args.tier)
    budget = BudgetState(caps)
    log_path = _audit_log_path(repo_root, args.feature)
    loop_id = str(uuid.uuid4())

    halted = False
    def _sig_handler(_signum, _frame):
        nonlocal halted
        halted = True
    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)

    while True:
        entry = tick(args, repo_root, budget, log_path, loop_id)
        if entry.get("halt_reason"):
            print(f"halt: {entry['halt_reason']}", file=sys.stderr)
            return 0 if entry["halt_reason"].startswith(("halt_file", "budget_exceeded")) else 1
        if not args.loop:
            return 0
        if halted:
            entry = {"ts": _now_iso(), "tier": args.tier, "tick_index": budget.ticks + 1,
                     "loop_id": loop_id, "halt_reason": "external_signal"}
            _append_log(log_path, entry)
            print("halt: external_signal", file=sys.stderr)
            return 0
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
