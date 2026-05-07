#!/usr/bin/env python3
"""Next.js+Tailwind adapter conformance test.

Modes:
  --plain  (default): forces shadcn=False, runs all 3 example Plans.
  --shadcn: forces shadcn=True, runs widget-tree against shadcn golden;
            palette and motion-set are stack-mode-invariant so they reuse
            plain goldens — semantic equivalence preserved.

Exits 0 on PASS: N/N, 1 otherwise.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_DIR = REPO_ROOT / "adapters" / "nextjs-tailwind"
GOLDEN_DIR = ADAPTER_DIR / "tests" / "golden"
EXAMPLES_DIR = REPO_ROOT / "docs" / "adapter-examples"

sys.path.insert(0, str(ADAPTER_DIR))
from adapter import render  # type: ignore


def cases(shadcn: bool) -> list[tuple[str, list[str]]]:
    widget = ["widget-tree__redeem_coupon_form.shadcn.tsx"] if shadcn else ["widget-tree__redeem_coupon_form.tsx"]
    return [
        ("palette",     ["palette__globals.css",     "palette__design_tokens.md"]),
        ("motion-set",  ["motion-set__globals.css",  "motion-set__design_tokens.md"]),
        ("widget-tree", widget),
    ]


def run(shadcn: bool) -> int:
    project = {"shadcn": shadcn, "router": "app"}
    label = "shadcn" if shadcn else "plain"
    passed = 0
    failed: list[str] = []

    for plan_name, goldens in cases(shadcn):
        plan_path = EXAMPLES_DIR / f"{plan_name}.json"
        plan = json.loads(plan_path.read_text())
        actual = render(plan, str(plan_path.relative_to(REPO_ROOT)), project)
        ok = True
        for i, gname in enumerate(goldens):
            expected = (GOLDEN_DIR / gname).read_text()
            got = actual[i]
            if expected != got:
                ok = False
                failed.append(f"{plan_name} → {gname} ({len(expected)} vs {len(got)} bytes)")
        if ok:
            passed += 1
        print(f"  {'OK' if ok else 'FAIL'}  {plan_name}  [{label}]")

    total = len(cases(shadcn))
    print(f"\nPASS ({label}): {passed}/{total}")
    if failed:
        print("Failures:")
        for f in failed:
            print(f"  - {f}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--plain",  action="store_true", default=False)
    g.add_argument("--shadcn", action="store_true", default=False)
    args = parser.parse_args()
    shadcn = args.shadcn
    sys.exit(run(shadcn))
