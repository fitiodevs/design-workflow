#!/usr/bin/env python3
"""Flutter adapter conformance test.

Runs the adapter on each example Plan in docs/adapter-examples/, compares
output byte-for-byte against goldens in tests/golden/. Prints PASS: N/M.
Exits 0 if all match, 1 otherwise.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_DIR = REPO_ROOT / "adapters" / "flutter"
GOLDEN_DIR = ADAPTER_DIR / "tests" / "golden"
EXAMPLES_DIR = REPO_ROOT / "docs" / "adapter-examples"

sys.path.insert(0, str(ADAPTER_DIR))
from adapter import render  # type: ignore


CASES: list[tuple[str, list[str]]] = [
    ("palette",     ["palette__app_colors.dart",      "palette__design_tokens.md"]),
    ("motion-set",  ["motion-set__app_motion.dart",   "motion-set__design_tokens.md"]),
    ("widget-tree", ["widget-tree__redeem_coupon_form.dart"]),
]


def run() -> int:
    passed = 0
    failed: list[str] = []
    for plan_name, goldens in CASES:
        plan_path = EXAMPLES_DIR / f"{plan_name}.json"
        plan = json.loads(plan_path.read_text())
        actual = render(plan, str(plan_path.relative_to(REPO_ROOT)))

        ok = True
        for i, gname in enumerate(goldens):
            expected = (GOLDEN_DIR / gname).read_text()
            got = actual[i]
            if expected != got:
                ok = False
                failed.append(f"{plan_name} → {gname} ({len(expected)} vs {len(got)} bytes)")
        if ok:
            passed += 1
        print(f"  {'OK' if ok else 'FAIL'}  {plan_name}")

    total = len(CASES)
    print(f"\nPASS: {passed}/{total}")
    if failed:
        print("Failures:")
        for f in failed:
            print(f"  - {f}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run())
