#!/usr/bin/env python3
"""Flutter adapter — renders Adapter Plans to Dart files.

Usage:
    python3 adapters/flutter/adapter.py <plan.json> [--dry-run]

Reads the Plan, dispatches by `kind`, renders via templates, writes per
`actions[]`. With --dry-run prints planned writes without touching disk.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from string import Template
from pathlib import Path

ADAPTER_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = ADAPTER_DIR / "templates"

if __package__:
    from .mappings import TOKEN_ROLE_MAP, WIDGET_TYPE_MAP, resolve_path
else:
    sys.path.insert(0, str(ADAPTER_DIR))
    from mappings import TOKEN_ROLE_MAP, WIDGET_TYPE_MAP, resolve_path  # type: ignore


CURVE_MAP = {
    "linear":     "Curves.linear",
    "easeIn":     "Curves.easeIn",
    "easeOut":    "Curves.easeOut",
    "easeInOut": "Curves.easeInOut",
    "spring":     "Curves.elasticOut",
    "bounce":     "Curves.bounceOut",
    "anticipate": "Curves.easeInBack",
    "decelerate": "Curves.decelerate",
}


def _hex_to_dart(hex_str: str) -> str:
    h = hex_str.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 6:
        h = "FF" + h
    return f"Color(0x{h.upper()})"


def _load_template(name: str) -> Template:
    return Template((TEMPLATE_DIR / name).read_text())


def render_palette(plan: dict, plan_path: str) -> dict[int, str]:
    palette = plan["tokens"]["palette"]
    roles = list(palette.keys())

    indent = "    "
    light_fields = ",\n".join(f"{indent}{r}: {_hex_to_dart(palette[r]['light'])}" for r in roles)
    dark_fields  = ",\n".join(f"{indent}{r}: {_hex_to_dart(palette[r]['dark'])}"  for r in roles)
    ctor_params  = ",\n".join(f"{indent}required this.{r}" for r in roles)
    field_decls  = "\n".join(f"  final Color {r};" for r in roles)

    tmpl = _load_template("app_colors.dart.tmpl")
    colors_dart = tmpl.substitute(
        plan_path=plan_path,
        role_count=str(len(roles)),
        light_fields=light_fields,
        dark_fields=dark_fields,
        ctor_params=ctor_params,
        field_decls=field_decls,
    )

    rows = ["| Role | Light | Dark |", "|---|---|---|"]
    rows += [f"| `{r}` | `{palette[r]['light']}` | `{palette[r]['dark']}` |" for r in roles]
    body = "\n".join(rows)
    doc = _load_template("design_tokens.md.tmpl").substitute(
        section_title=f"Palette ({len(roles)} roles)",
        generated_at=_ts(),
        plan_path=plan_path,
        body=body,
    )

    out: dict[int, str] = {}
    for i, action in enumerate(plan["actions"]):
        if action["role"] == "palette" and action["intent"] == "tokens":
            out[i] = colors_dart
        elif action["role"] == "design-tokens" and action["intent"] == "doc-summary":
            out[i] = doc
        else:
            raise KeyError(f"flutter palette adapter: unsupported action {action}")
    return out


def _render_node(node: dict, depth: int = 2) -> str:
    indent = "  " * depth
    klass = WIDGET_TYPE_MAP.get(node["type"], f"/* TODO unsupported: {node['type']} */ Container")
    props = node.get("props", {})
    children = node.get("children", [])

    args: list[str] = []
    for k in ("variant", "size"):
        if k in node:
            args.append(f"{k}: {klass}{k.capitalize()}.{node[k]}")
    for k, v in props.items():
        if isinstance(v, str):
            args.append(f"{k}: '{_escape(v)}'")
        elif isinstance(v, bool):
            args.append(f"{k}: {'true' if v else 'false'}")
        else:
            args.append(f"{k}: {v}")
    if children:
        body = ",\n".join(_render_node(c, depth + 2) for c in children)
        args.append(f"children: [\n{body},\n{indent}  ]")

    if not args:
        return f"{indent}{klass}()"
    body = ",\n".join(f"{indent}  {a}" for a in args)
    return f"{indent}{klass}(\n{body},\n{indent})"


def _escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def render_widget_tree(plan: dict, plan_path: str) -> dict[int, str]:
    out: dict[int, str] = {}
    widgets = plan["widgets"]
    components = [a for a in plan["actions"] if a["intent"] == "component"]
    if len(widgets) != len(components):
        # Single component: wrap all widgets under the named action.
        if len(components) == 1 and len(widgets) >= 1:
            tree = _render_node(widgets[0], depth=2).lstrip()
            tmpl = _load_template("widget.dart.tmpl")
            for i, action in enumerate(plan["actions"]):
                if action is components[0]:
                    out[i] = tmpl.substitute(
                        name=action["name"],
                        plan_path=plan_path,
                        tree=tree.rstrip(),
                    )
        else:
            raise ValueError("widget-tree Plan: widgets/components arity mismatch")
    else:
        tmpl = _load_template("widget.dart.tmpl")
        for i, action in enumerate(plan["actions"]):
            if action["intent"] != "component":
                continue
            idx = components.index(action)
            tree = _render_node(widgets[idx], depth=2).lstrip()
            out[i] = tmpl.substitute(
                name=action["name"],
                plan_path=plan_path,
                tree=tree.rstrip(),
            )
    return out


def render_motion(plan: dict, plan_path: str) -> dict[int, str]:
    motion = plan["tokens"]["motion"]
    duration_fields = "\n".join(
        f"  static const {role} = Duration(milliseconds: {m['durationMs']});"
        for role, m in motion.items()
    )
    curve_fields = "\n".join(
        f"  static const {role} = {CURVE_MAP[m['curve']]};"
        for role, m in motion.items()
    )
    motion_dart = _load_template("app_motion.dart.tmpl").substitute(
        plan_path=plan_path,
        duration_fields=duration_fields,
        curve_fields=curve_fields,
    )

    rows = ["| Role | Duration (ms) | Curve |", "|---|---|---|"]
    rows += [f"| `{r}` | {m['durationMs']} | `{m['curve']}` |" for r, m in motion.items()]
    body = "\n".join(rows)
    doc = _load_template("design_tokens.md.tmpl").substitute(
        section_title=f"Motion ({len(motion)} roles)",
        generated_at=_ts(),
        plan_path=plan_path,
        body=body,
    )

    out: dict[int, str] = {}
    for i, action in enumerate(plan["actions"]):
        if action["role"] == "motion" and action["intent"] == "tokens":
            out[i] = motion_dart
        elif action["role"] == "design-tokens" and action["intent"] == "doc-summary":
            out[i] = doc
        else:
            raise KeyError(f"flutter motion adapter: unsupported action {action}")
    return out


def _ts() -> str:
    return datetime(2026, 5, 7, tzinfo=timezone.utc).isoformat(timespec="seconds")


def render(plan: dict, plan_path: str) -> dict[int, str]:
    kind = plan["kind"]
    if kind == "palette":
        return render_palette(plan, plan_path)
    if kind == "widget-tree":
        return render_widget_tree(plan, plan_path)
    if kind == "motion-set":
        return render_motion(plan, plan_path)
    raise KeyError(f"flutter adapter: unknown kind {kind!r}")


def main(plan_path: str, dry_run: bool = False) -> int:
    plan = json.loads(Path(plan_path).read_text())
    rendered = render(plan, plan_path)
    for i, action in enumerate(plan["actions"]):
        path = resolve_path(action, plan)
        content = rendered[i]
        if dry_run:
            print(f"would write: {path} ({len(content)} bytes)")
        else:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            mode = "a" if action["op"] == "append" else "w"
            with open(path, mode) as f:
                f.write(content)
            print(f"wrote: {path} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="design-workflow Flutter adapter")
    parser.add_argument("plan", help="path to Adapter Plan JSON")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    sys.exit(main(args.plan, dry_run=args.dry_run))
