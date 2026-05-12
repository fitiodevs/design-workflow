#!/usr/bin/env python3
"""elicitation — append-only ledger of weak-supervision events.

Ported pattern from claude-code-harness (`docs/sandbagging-aware-weak-supervision.md`,
MIT). Adapted for design-workflow: review skills (Júri/Lupa) append evidence
when they spot AI-slop; generator skills (Clara/Arquiteto) read the ledger
before generating so prior failures are not repeated.

Storage convention (per-project, append-only):

    .design-spec/state/elicitation/<YYYY-MM-DD>.jsonl

One JSONL line per event. Each event conforms to `elicitation-event.v1`.

CLI:

    elicitation.py append <kind> --target <path> --source <skill> \\
        [--severity critical|major|minor|info] \\
        [--verdict APPROVE|REQUEST_CHANGES|NEUTRAL] \\
        [--summary "..."] [--evidence file:line,file:line] \\
        [--slop-pattern name] [--privacy-tag do_not_train]

    elicitation.py read --target <path> [--days 30] [--kind k1,k2]
        → JSON array of matching events

    elicitation.py summarize --target <path> [--days 30]
        → Markdown summary for generator preamble (prior counterexamples
          + last verdict + recurring slop patterns)

Exit codes:
    0  ok
    1  validation error (bad kind, missing required field)
    2  i/o error
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = "elicitation-event.v1"
LEDGER_ROOT = Path(".design-spec") / "state" / "elicitation"

ALLOWED_KINDS = {
    "capability_probe",   # a question/probe presented to the user or to a sub-agent
    "weak_label",         # a noisy/inconclusive label (audit saw a hint, no proof)
    "judge_verdict",      # a reviewer reached a verdict (Júri/Lupa output rolled up)
    "eval_result",        # a scored evaluation (audit_theme.py coverage, WCAG pass-rate)
    "counterexample",     # a failing case with concrete evidence (file:line)
}

ALLOWED_SEVERITY = {"critical", "major", "minor", "info"}
ALLOWED_VERDICT = {"APPROVE", "REQUEST_CHANGES", "NEUTRAL"}
ALLOWED_PRIVACY = {"do_not_train", "may_train", "synthetic_only", "legal_hold"}
DEFAULT_PRIVACY = ["do_not_train"]


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _today_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def _ledger_path(repo_root: Path, day: str | None = None) -> Path:
    p = repo_root / LEDGER_ROOT
    p.mkdir(parents=True, exist_ok=True)
    return p / f"{day or _today_utc()}.jsonl"


def _validate(event: dict) -> None:
    if event.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    kind = event.get("kind")
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"kind must be one of {sorted(ALLOWED_KINDS)}, got {kind!r}")
    for required in ("ts", "target", "source", "summary"):
        if not event.get(required):
            raise ValueError(f"missing required field: {required}")
    sev = event.get("severity")
    if sev is not None and sev not in ALLOWED_SEVERITY:
        raise ValueError(f"severity must be one of {sorted(ALLOWED_SEVERITY)}")
    verdict = event.get("verdict")
    if verdict is not None and verdict not in ALLOWED_VERDICT:
        raise ValueError(f"verdict must be one of {sorted(ALLOWED_VERDICT)}")
    tags = event.get("privacy_tags") or []
    if not isinstance(tags, list):
        raise ValueError("privacy_tags must be a list")
    for t in tags:
        if t not in ALLOWED_PRIVACY:
            raise ValueError(f"privacy_tag {t!r} not allowed")


def append_event(event: dict, repo_root: Path = Path(".")) -> Path:
    event.setdefault("schema_version", SCHEMA_VERSION)
    event.setdefault("ts", _now_iso())
    event.setdefault("privacy_tags", list(DEFAULT_PRIVACY))
    _validate(event)
    path = _ledger_path(repo_root)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, separators=(",", ":"), ensure_ascii=False) + "\n")
    return path


def _iter_ledger_files(repo_root: Path, days: int) -> Iterable[Path]:
    root = repo_root / LEDGER_ROOT
    if not root.exists():
        return []
    cutoff = dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=days)
    for p in sorted(root.glob("*.jsonl")):
        try:
            d = dt.date.fromisoformat(p.stem)
        except ValueError:
            continue
        if d >= cutoff:
            yield p


def read_events(
    repo_root: Path = Path("."),
    target: str | None = None,
    kinds: set[str] | None = None,
    days: int = 30,
) -> list[dict]:
    out: list[dict] = []
    for path in _iter_ledger_files(repo_root, days):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if target and not _target_matches(event.get("target", ""), target):
                continue
            if kinds and event.get("kind") not in kinds:
                continue
            out.append(event)
    return out


def _target_matches(event_target: str, query: str) -> bool:
    if not event_target or not query:
        return False
    # Match if query is a substring of the event target, OR vice-versa
    # (so /juri lib/features/x and /clara lib/features/x/page.dart share evidence).
    return query in event_target or event_target in query


def summarize_for_preamble(
    repo_root: Path = Path("."),
    target: str | None = None,
    days: int = 30,
    max_items: int = 8,
) -> str:
    events = read_events(repo_root=repo_root, target=target, days=days)
    if not events:
        return ""
    verdicts = [e for e in events if e.get("kind") == "judge_verdict"]
    counters = [e for e in events if e.get("kind") == "counterexample"]
    evals = [e for e in events if e.get("kind") == "eval_result"]

    lines: list[str] = []
    lines.append(f"### Prior evidence on `{target}` (last {days}d)")
    lines.append("")
    if verdicts:
        latest = max(verdicts, key=lambda e: e.get("ts", ""))
        v = latest.get("verdict", "?")
        s = latest.get("summary", "")
        src = latest.get("source", "?")
        ts = latest.get("ts", "")[:10]
        lines.append(f"- **Last verdict** ({src}, {ts}): `{v}` — {s}")
    if evals:
        latest = max(evals, key=lambda e: e.get("ts", ""))
        lines.append(f"- **Last audit** ({latest.get('source','?')}): {latest.get('summary','')}")
    if counters:
        # Recurring slop patterns
        pattern_counts: dict[str, int] = {}
        for e in counters:
            sp = e.get("slop_pattern")
            if sp:
                pattern_counts[sp] = pattern_counts.get(sp, 0) + 1
        if pattern_counts:
            top = sorted(pattern_counts.items(), key=lambda kv: -kv[1])[:5]
            patterns = ", ".join(f"{p} ×{n}" for p, n in top)
            lines.append(f"- **Recurring slop patterns:** {patterns}")
        lines.append("")
        lines.append(f"**Counterexamples to avoid** ({len(counters)} total, showing top {min(max_items, len(counters))}):")
        for e in counters[-max_items:]:
            sev = e.get("severity") or "?"
            sp = e.get("slop_pattern") or "—"
            refs = ", ".join(e.get("evidence_refs") or []) or "—"
            lines.append(f"  - [{sev}] {e.get('summary','')} · pattern: `{sp}` · refs: {refs}")
    lines.append("")
    lines.append("> Treat counterexamples above as **slop traps**. If the new output would repeat any pattern, revise before delivering.")
    return "\n".join(lines)


def _build_event_from_args(args) -> dict:
    event: dict = {
        "kind": args.kind,
        "target": args.target,
        "source": args.source,
        "summary": args.summary or "",
    }
    if args.severity:
        event["severity"] = args.severity
    if args.verdict:
        event["verdict"] = args.verdict
    if args.evidence:
        event["evidence_refs"] = [r.strip() for r in args.evidence.split(",") if r.strip()]
    if args.slop_pattern:
        event["slop_pattern"] = args.slop_pattern
    if args.privacy_tag:
        event["privacy_tags"] = [t.strip() for t in args.privacy_tag.split(",") if t.strip()]
    if args.extra:
        try:
            event.update(json.loads(args.extra))
        except json.JSONDecodeError as e:
            raise ValueError(f"--extra must be valid JSON: {e}")
    return event


def _cmd_append(args) -> int:
    try:
        event = _build_event_from_args(args)
        path = append_event(event, repo_root=Path(args.repo_root))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"i/o error: {e}", file=sys.stderr)
        return 2
    print(str(path))
    return 0


def _cmd_read(args) -> int:
    kinds = set(args.kind.split(",")) if args.kind else None
    events = read_events(
        repo_root=Path(args.repo_root),
        target=args.target,
        kinds=kinds,
        days=args.days,
    )
    print(json.dumps(events, indent=2, ensure_ascii=False))
    return 0


def _cmd_summarize(args) -> int:
    text = summarize_for_preamble(
        repo_root=Path(args.repo_root),
        target=args.target,
        days=args.days,
        max_items=args.max_items,
    )
    if text:
        print(text)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="elicitation", description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo-root", default=".", help="repo root (default: cwd)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("append", help="append a new event to today's ledger")
    a.add_argument("kind", choices=sorted(ALLOWED_KINDS))
    a.add_argument("--target", required=True, help="path or feature slug under review")
    a.add_argument("--source", required=True, help="skill name (e.g. theme-critique)")
    a.add_argument("--summary", default="", help="one-line summary")
    a.add_argument("--severity", choices=sorted(ALLOWED_SEVERITY))
    a.add_argument("--verdict", choices=sorted(ALLOWED_VERDICT))
    a.add_argument("--evidence", help="comma-separated file:line refs")
    a.add_argument("--slop-pattern", help="cardinal sin name (matches anti-ai-slop.md)")
    a.add_argument("--privacy-tag", default=",".join(DEFAULT_PRIVACY), help="comma-separated privacy tags")
    a.add_argument("--extra", help='extra JSON fields, e.g. \'{"score": 28}\'')
    a.set_defaults(func=_cmd_append)

    r = sub.add_parser("read", help="read events matching target/kind/days")
    r.add_argument("--target", help="filter by target substring match")
    r.add_argument("--kind", help="comma-separated kinds to include")
    r.add_argument("--days", type=int, default=30, help="lookback window in days (default 30)")
    r.set_defaults(func=_cmd_read)

    s = sub.add_parser("summarize", help="emit markdown preamble for generator skills")
    s.add_argument("--target", required=True, help="target path/slug")
    s.add_argument("--days", type=int, default=30)
    s.add_argument("--max-items", type=int, default=8)
    s.set_defaults(func=_cmd_summarize)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
