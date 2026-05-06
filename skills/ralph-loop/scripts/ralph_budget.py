#!/usr/bin/env python3
"""ralph_budget — read audit log, summarize cost / tokens / ticks per feature/day."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def _iter_log_files(repo_root: Path, feature: str | None, day: str | None):
    base = repo_root / ".design-spec" / "features"
    if not base.exists():
        return
    feature_dirs = [base / feature] if feature else [d for d in base.iterdir() if d.is_dir()]
    for d in feature_dirs:
        log_dir = d / "loop-log"
        if not log_dir.exists():
            continue
        for f in sorted(log_dir.glob("*.jsonl")):
            if day and f.stem != day:
                continue
            yield d.name, f


def main() -> int:
    p = argparse.ArgumentParser(description="Ralph budget summary")
    p.add_argument("--feature", help="Scope to one feature")
    p.add_argument("--day", help="Scope to one YYYY-MM-DD")
    p.add_argument("--root", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    repo_root = Path(args.root).resolve()
    by_key = defaultdict(lambda: {"ticks": 0, "tokens": 0, "usd": 0.0, "halts": 0})

    for feature, log_file in _iter_log_files(repo_root, args.feature, args.day):
        for line in log_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = (feature, log_file.stem, e.get("tier", "?"))
            by_key[key]["ticks"] += 1
            by_key[key]["tokens"] += int(e.get("input_tokens") or 0) + int(e.get("output_tokens") or 0)
            by_key[key]["usd"] += float(e.get("cost_usd") or 0.0)
            if e.get("halt_reason"):
                by_key[key]["halts"] += 1

    summary = [
        {
            "feature": k[0], "day": k[1], "tier": k[2],
            "ticks": v["ticks"], "tokens": v["tokens"],
            "usd": round(v["usd"], 4), "halts": v["halts"],
        }
        for k, v in sorted(by_key.items())
    ]

    if args.json:
        print(json.dumps(summary, indent=2))
        return 0
    if not summary:
        print("No audit log entries found.")
        return 0
    print(f"{'feature':<25} {'day':<12} {'tier':<12} {'ticks':>6} {'tokens':>10} {'usd':>8} {'halts':>6}")
    for r in summary:
        print(f"{r['feature']:<25} {r['day']:<12} {r['tier']:<12} {r['ticks']:>6} {r['tokens']:>10} {r['usd']:>8} {r['halts']:>6}")
    totals = {
        "ticks": sum(r["ticks"] for r in summary),
        "tokens": sum(r["tokens"] for r in summary),
        "usd": round(sum(r["usd"] for r in summary), 4),
        "halts": sum(r["halts"] for r in summary),
    }
    print(f"{'TOTAL':<25} {'':<12} {'':<12} {totals['ticks']:>6} {totals['tokens']:>10} {totals['usd']:>8} {totals['halts']:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
