#!/usr/bin/env python3
"""React Native adapter conformance test.

Runs the 3 example Plans (palette, motion-set, widget-tree) through the
adapter and compares against frozen golden files. Exits 0 on PASS: N/N.

Usage:
    python3 adapters/react-native/tests/conformance.py
    python3 adapters/react-native/tests/conformance.py --update   # rewrite goldens (use carefully)
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_DIR = REPO_ROOT / "adapters" / "react-native"
GOLDEN_DIR = ADAPTER_DIR / "tests" / "golden"
EXAMPLES_DIR = REPO_ROOT / "docs" / "adapter-examples"

sys.path.insert(0, str(ADAPTER_DIR))
from adapter import render  # type: ignore


CASES: list[tuple[str, list[str]]] = [
    ("palette",    ["palette__colors.ts",     "palette__design_tokens.md"]),
    ("motion-set", ["motion-set__motion.ts",  "motion-set__design_tokens.md"]),
    ("widget-tree", ["widget-tree__redeem_coupon_form.tsx"]),
]


def run(update: bool = False) -> int:
    project = {"expo": False, "router": "src"}
    passed = 0
    failed: list[str] = []

    for plan_name, goldens in CASES:
        plan_path = EXAMPLES_DIR / f"{plan_name}.json"
        plan = json.loads(plan_path.read_text())
        actual = render(plan, str(plan_path.relative_to(REPO_ROOT)), project)
        ok = True
        for i, gname in enumerate(goldens):
            golden_path = GOLDEN_DIR / gname
            got = actual[i]
            if update:
                golden_path.write_text(got)
                continue
            expected = golden_path.read_text()
            if expected != got:
                ok = False
                failed.append(f"{plan_name} → {gname} ({len(expected)} vs {len(got)} bytes)")
        if ok:
            passed += 1
        if not update:
            print(f"  {'OK' if ok else 'FAIL'}  {plan_name}")

    if update:
        print(f"updated {sum(len(g) for _, g in CASES)} goldens in {GOLDEN_DIR}")
        return 0

    total = len(CASES)
    print(f"\nPASS: {passed}/{total}")
    if failed:
        print("Failures:")
        for f in failed:
            print(f"  - {f}")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="react-native adapter conformance test")
    parser.add_argument("--update", action="store_true", help="rewrite goldens from current adapter output")
    args = parser.parse_args()
    return run(update=args.update)


if __name__ == "__main__":
    sys.exit(main())
