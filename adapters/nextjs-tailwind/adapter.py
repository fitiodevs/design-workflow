#!/usr/bin/env python3
"""Next.js + Tailwind adapter — renders Adapter Plans to TSX/CSS.

Usage:
    python3 adapters/nextjs-tailwind/adapter.py <plan.json> [--dry-run] [--shadcn|--plain]

Reads the Plan, dispatches by `kind`, renders via templates (shadcn-aware
when detected), writes per `actions[]`.
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
    from .mappings import (
        TOKEN_ROLE_MAP,
        WIDGET_TYPE_MAP_PLAIN,
        WIDGET_TYPE_MAP_SHADCN,
        SHADCN_IMPORTS,
        has_shadcn,
        app_router_or_pages,
        resolve_path,
        role_to_tailwind_path,
        px_to_tailwind_unit,
    )
else:
    sys.path.insert(0, str(ADAPTER_DIR))
    from mappings import (  # type: ignore
        TOKEN_ROLE_MAP,
        WIDGET_TYPE_MAP_PLAIN,
        WIDGET_TYPE_MAP_SHADCN,
        SHADCN_IMPORTS,
        has_shadcn,
        app_router_or_pages,
        resolve_path,
        role_to_tailwind_path,
        px_to_tailwind_unit,
    )


def _load(name: str) -> Template:
    return Template((TEMPLATE_DIR / name).read_text())


def _ts() -> str:
    return datetime(2026, 5, 7, tzinfo=timezone.utc).isoformat(timespec="seconds")


def render_palette(plan: dict, plan_path: str, project: dict) -> dict[int, str]:
    palette = plan["tokens"]["palette"]
    light = "\n".join(f"  {TOKEN_ROLE_MAP[r]}: {palette[r]['light']};" for r in palette)
    dark  = "\n".join(f"  {TOKEN_ROLE_MAP[r]}: {palette[r]['dark']};"  for r in palette)
    css = _load("tokens.css.tmpl").substitute(
        plan_path=plan_path,
        light_block=light,
        dark_block=dark,
    )

    groups: dict[str, dict[str, str]] = {}
    for r in palette:
        g, leaf = role_to_tailwind_path(r)
        groups.setdefault(g, {})[leaf] = f"var({TOKEN_ROLE_MAP[r]})"
    color_lines = []
    for g in sorted(groups):
        leaves = groups[g]
        color_lines.append(f"  {g}: {{")
        for leaf in sorted(leaves):
            color_lines.append(f'    {leaf!r}: {leaves[leaf]!r},'.replace("'", '"'))
        color_lines.append("  },")
    tw = _load("tailwind.config.ts.tmpl").substitute(
        plan_path=plan_path,
        color_block="\n".join(color_lines),
    )

    rows = ["| Role | CSS var | Light | Dark |", "|---|---|---|---|"]
    rows += [
        f"| `{r}` | `{TOKEN_ROLE_MAP[r]}` | `{palette[r]['light']}` | `{palette[r]['dark']}` |"
        for r in palette
    ]
    doc = _load("design_tokens.md.tmpl").substitute(
        section_title=f"Palette ({len(palette)} roles, CSS vars + Tailwind)",
        generated_at=_ts(),
        plan_path=plan_path,
        body="\n".join(rows),
    )

    out: dict[int, str] = {}
    for i, action in enumerate(plan["actions"]):
        if action["role"] == "palette" and action["intent"] == "tokens":
            out[i] = css
        elif action["role"] == "palette" and action["intent"] == "config":
            out[i] = tw
        elif action["role"] == "design-tokens" and action["intent"] == "doc-summary":
            out[i] = doc
        else:
            raise KeyError(f"nextjs-tailwind palette adapter: unsupported action {action}")
    return out


def render_motion(plan: dict, plan_path: str, project: dict) -> dict[int, str]:
    motion = plan["tokens"]["motion"]

    css_lines = []
    for role, m in motion.items():
        css_lines.append(f"  --motion-{_kebab(role)}-duration: {m['durationMs']}ms;")
        css_lines.append(f"  --motion-{_kebab(role)}-curve: {_curve_to_css(m['curve'])};")
    css = _load("tokens.css.tmpl").substitute(
        plan_path=plan_path,
        light_block="\n".join(css_lines),
        dark_block="\n".join(css_lines),  # motion identical across modes
    )

    rows = ["| Role | Duration | Curve |", "|---|---|---|"]
    rows += [f"| `{r}` | {m['durationMs']}ms | `{_curve_to_css(m['curve'])}` |" for r, m in motion.items()]
    doc = _load("design_tokens.md.tmpl").substitute(
        section_title=f"Motion ({len(motion)} roles, CSS vars)",
        generated_at=_ts(),
        plan_path=plan_path,
        body="\n".join(rows),
    )

    out: dict[int, str] = {}
    for i, action in enumerate(plan["actions"]):
        if action["role"] == "motion" and action["intent"] == "tokens":
            out[i] = css
        elif action["role"] == "design-tokens" and action["intent"] == "doc-summary":
            out[i] = doc
        else:
            raise KeyError(f"nextjs-tailwind motion adapter: unsupported action {action}")
    return out


def _curve_to_css(curve: str) -> str:
    return {
        "linear":     "linear",
        "easeIn":     "cubic-bezier(0.42, 0, 1, 1)",
        "easeOut":    "cubic-bezier(0, 0, 0.58, 1)",
        "easeInOut":  "cubic-bezier(0.42, 0, 0.58, 1)",
        "spring":     "cubic-bezier(0.34, 1.56, 0.64, 1)",
        "bounce":     "cubic-bezier(0.68, -0.55, 0.27, 1.55)",
        "anticipate": "cubic-bezier(0.6, -0.28, 0.74, 0.05)",
        "decelerate": "cubic-bezier(0, 0, 0.2, 1)",
    }[curve]


def _kebab(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out.append("-")
        out.append(ch.lower())
    return "".join(out)


def _render_node(node: dict, project: dict, depth: int = 2) -> tuple[str, set[str]]:
    indent = "  " * depth
    shadcn = project.get("shadcn", False)
    type_ = node["type"]
    imports: set[str] = set()

    klass: str
    if shadcn and type_ in WIDGET_TYPE_MAP_SHADCN:
        klass = WIDGET_TYPE_MAP_SHADCN[type_]
        imports.add(klass)
    else:
        klass = WIDGET_TYPE_MAP_PLAIN.get(type_, "div")

    props = dict(node.get("props", {}))
    children = node.get("children", [])

    label = props.pop("label", None)
    text_value = props.pop("value", None)

    attrs: list[str] = []
    if "variant" in node:
        if shadcn and klass == "Button":
            mapped = {"primary": "default", "secondary": "secondary", "ghost": "ghost"}.get(node["variant"], node["variant"])
            attrs.append(f'variant="{mapped}"')
        elif not shadcn and klass == "button":
            class_pieces = _button_classes(node)
            attrs.append(f'className="{class_pieces}"')
        else:
            attrs.append(f'data-variant="{node["variant"]}"')
    if "size" in node:
        if shadcn and klass in {"Button", "Input"}:
            attrs.append(f'size="{node["size"]}"')

    for k, v in props.items():
        if isinstance(v, bool):
            if v:
                attrs.append(_bool_attr(k))
        elif isinstance(v, str):
            attrs.append(f'{_jsx_attr(k)}="{_escape(v)}"')
        else:
            attrs.append(f'{_jsx_attr(k)}={{{json.dumps(v)}}}')

    self_closing = type_ in {"input", "image", "icon", "divider", "spacer", "checkbox", "switch", "slider", "progress"} and not children and label is None and text_value is None

    open_tag = klass + (" " + " ".join(attrs) if attrs else "")
    if self_closing:
        return f"{indent}<{open_tag} />", imports

    inner_lines: list[str] = []
    if label is not None:
        inner_lines.append(f"{indent}  {_escape(label)}")
    if text_value is not None:
        inner_lines.append(f"{indent}  {_escape(text_value)}")
    for c in children:
        rendered, child_imports = _render_node(c, project, depth + 1)
        inner_lines.append(rendered)
        imports |= child_imports

    body = "\n".join(inner_lines) if inner_lines else ""
    if body:
        return f"{indent}<{open_tag}>\n{body}\n{indent}</{klass}>", imports
    return f"{indent}<{open_tag}></{klass}>", imports


def _button_classes(node: dict) -> str:
    variant = node.get("variant", "primary")
    size = node.get("size", "md")
    base = "rounded-lg font-medium transition-colors"
    variant_classes = {
        "primary":   "bg-brand-default text-text-on-brand hover:bg-brand-pressed",
        "secondary": "bg-bg-surface text-text-primary border border-border-default",
        "ghost":     "bg-transparent text-text-primary hover:bg-bg-surface",
    }.get(variant, "bg-brand-default text-text-on-brand")
    size_classes = {
        "xs": "px-3 py-1 text-xs",
        "sm": "px-4 py-2 text-sm",
        "md": "px-5 py-2.5 text-base",
        "lg": "px-6 py-3 text-base",
        "xl": "px-8 py-4 text-lg",
    }.get(size, "px-5 py-2.5 text-base")
    pieces = [base, variant_classes, size_classes]
    if node.get("props", {}).get("fullWidth"):
        pieces.append("w-full")
    return " ".join(pieces)


def _jsx_attr(name: str) -> str:
    if name == "class":
        return "className"
    if name == "for":
        return "htmlFor"
    return name


def _bool_attr(name: str) -> str:
    return _jsx_attr(name)


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;")
              .replace('"', "&quot;"))


def render_widget_tree(plan: dict, plan_path: str, project: dict) -> dict[int, str]:
    out: dict[int, str] = {}
    widgets = plan["widgets"]
    components = [a for a in plan["actions"] if a["intent"] == "component"]

    if len(components) != 1 or len(widgets) < 1:
        raise ValueError("nextjs-tailwind widget-tree: expects exactly 1 component action")

    tree, imports = _render_node(widgets[0], project, depth=2)
    if project.get("shadcn"):
        import_lines = "\n".join(
            f'import {{ {name} }} from "{SHADCN_IMPORTS[name]}";'
            for name in sorted(imports) if name in SHADCN_IMPORTS
        )
        if import_lines:
            import_lines += "\n"
        tmpl_name = "component-shadcn.tsx.tmpl"
    else:
        import_lines = ""
        tmpl_name = "component.tsx.tmpl"

    rendered = _load(tmpl_name).substitute(
        plan_path=plan_path,
        imports=import_lines,
        name=components[0]["name"],
        tree=tree,
    )
    for i, action in enumerate(plan["actions"]):
        if action is components[0]:
            out[i] = rendered
    return out


def render(plan: dict, plan_path: str, project: dict | None = None) -> dict[int, str]:
    project = project or {"shadcn": False, "router": "app"}
    kind = plan["kind"]
    if kind == "palette":
        return render_palette(plan, plan_path, project)
    if kind == "widget-tree":
        return render_widget_tree(plan, plan_path, project)
    if kind == "motion-set":
        return render_motion(plan, plan_path, project)
    raise KeyError(f"nextjs-tailwind adapter: unknown kind {kind!r}")


def main(plan_path: str, dry_run: bool = False, shadcn: bool | None = None, router: str | None = None) -> int:
    plan = json.loads(Path(plan_path).read_text())
    project = {
        "shadcn": shadcn if shadcn is not None else has_shadcn(),
        "router": router or app_router_or_pages(),
    }
    rendered = render(plan, plan_path, project)
    for i, action in enumerate(plan["actions"]):
        path = resolve_path(action, plan, project)
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
    parser = argparse.ArgumentParser(description="design-workflow Next.js+Tailwind adapter")
    parser.add_argument("plan", help="path to Adapter Plan JSON")
    parser.add_argument("--dry-run", action="store_true")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--shadcn", action="store_true", help="force shadcn variant")
    g.add_argument("--plain",  action="store_true", help="force plain Tailwind variant")
    parser.add_argument("--router", choices=["app", "pages"], default=None)
    args = parser.parse_args()
    forced = True if args.shadcn else (False if args.plain else None)
    sys.exit(main(args.plan, dry_run=args.dry_run, shadcn=forced, router=args.router))
