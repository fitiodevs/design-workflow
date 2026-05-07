#!/usr/bin/env python3
"""React Native adapter — renders Adapter Plans to RN TypeScript.

Usage:
    python3 adapters/react-native/adapter.py <plan.json> [--dry-run] [--app|--src]

Reads the Plan, dispatches by `kind`, renders via templates, writes per
`actions[]`. Stack-neutral palette and motion-set are rendered as TypeScript
const exports; widget-tree is a `.tsx` component using RN core primitives plus
`StyleSheet.create()`.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from string import Template
from pathlib import Path

ADAPTER_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = ADAPTER_DIR / "templates"

if __package__:
    from .mappings import (
        TOKEN_ROLE_MAP,
        WIDGET_TYPE_MAP,
        RN_CORE_IMPORTS,
        RN_COMMUNITY_IMPORTS,
        CURVE_MAP,
        has_expo,
        app_or_src,
        resolve_path,
        to_rn_spacing,
    )
else:
    sys.path.insert(0, str(ADAPTER_DIR))
    from mappings import (  # type: ignore
        TOKEN_ROLE_MAP,
        WIDGET_TYPE_MAP,
        RN_CORE_IMPORTS,
        RN_COMMUNITY_IMPORTS,
        CURVE_MAP,
        has_expo,
        app_or_src,
        resolve_path,
        to_rn_spacing,
    )


def _load(name: str) -> Template:
    return Template((TEMPLATE_DIR / name).read_text())


def _ts() -> str:
    return datetime(2026, 5, 7, tzinfo=timezone.utc).isoformat(timespec="seconds")


# ---- palette ----------------------------------------------------------------

def render_palette(plan: dict, plan_path: str, project: dict) -> dict[int, str]:
    palette = plan["tokens"]["palette"]
    roles = list(palette.keys())

    role_union = "\n".join(f'  | "{r}"' for r in roles).rstrip() + ";"
    light = "\n".join(f'  {r}: "{palette[r]["light"]}",' for r in roles)
    dark  = "\n".join(f'  {r}: "{palette[r]["dark"]}",'  for r in roles)

    ts_file = _load("colors.ts.tmpl").substitute(
        plan_path=plan_path,
        role_union=role_union,
        light_block=light,
        dark_block=dark,
    )

    rows = ["| Role | Light | Dark |", "|---|---|---|"]
    rows += [
        f"| `{r}` | `{palette[r]['light']}` | `{palette[r]['dark']}` |"
        for r in roles
    ]
    doc = _load("design_tokens.md.tmpl").substitute(
        section_title=f"Palette ({len(roles)} roles, RN TS exports)",
        generated_at=_ts(),
        plan_path=plan_path,
        body="\n".join(rows),
    )

    out: dict[int, str] = {}
    for i, action in enumerate(plan["actions"]):
        if action["role"] == "palette" and action["intent"] == "tokens":
            out[i] = ts_file
        elif action["role"] == "design-tokens" and action["intent"] == "doc-summary":
            out[i] = doc
        else:
            raise KeyError(f"react-native palette adapter: unsupported action {action}")
    return out


# ---- motion-set -------------------------------------------------------------

def render_motion(plan: dict, plan_path: str, project: dict) -> dict[int, str]:
    motion = plan["tokens"]["motion"]
    roles = list(motion.keys())

    role_union = "\n".join(f'  | "{r}"' for r in roles).rstrip() + ";"
    motion_lines = []
    for role, m in motion.items():
        motion_lines.append(
            f"  {role}: {{ durationMs: {m['durationMs']}, easing: {CURVE_MAP[m['curve']]} }},"
        )
    ts_file = _load("motion.ts.tmpl").substitute(
        plan_path=plan_path,
        role_union=role_union,
        motion_block="\n".join(motion_lines),
    )

    rows = ["| Role | Duration (ms) | Easing |", "|---|---|---|"]
    rows += [f"| `{r}` | {m['durationMs']} | `{CURVE_MAP[m['curve']]}` |" for r, m in motion.items()]
    doc = _load("design_tokens.md.tmpl").substitute(
        section_title=f"Motion ({len(roles)} roles, RN Easing exports)",
        generated_at=_ts(),
        plan_path=plan_path,
        body="\n".join(rows),
    )

    out: dict[int, str] = {}
    for i, action in enumerate(plan["actions"]):
        if action["role"] == "motion" and action["intent"] == "tokens":
            out[i] = ts_file
        elif action["role"] == "design-tokens" and action["intent"] == "doc-summary":
            out[i] = doc
        else:
            raise KeyError(f"react-native motion adapter: unsupported action {action}")
    return out


# ---- widget-tree ------------------------------------------------------------

def _safe_id(name: str) -> str:
    """Sanitize a widget label or feature into a JS identifier-ish."""
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if cleaned and cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned or "node"


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;")
              .replace('"', "&quot;"))


_BUTTON_VARIANT_STYLE = {
    "primary":   {"bg": "brandDefault",  "fg": "textOnBrand",  "borderWidth": 0},
    "secondary": {"bg": "bgSurface",     "fg": "textPrimary",  "borderWidth": 1, "borderColor": "borderDefault"},
    "ghost":     {"bg": "transparent",   "fg": "textPrimary",  "borderWidth": 0},
}

_BUTTON_SIZE_STYLE = {
    "xs": {"paddingHorizontal": 12, "paddingVertical": 4,  "fontSize": 12},
    "sm": {"paddingHorizontal": 16, "paddingVertical": 8,  "fontSize": 14},
    "md": {"paddingHorizontal": 20, "paddingVertical": 10, "fontSize": 16},
    "lg": {"paddingHorizontal": 24, "paddingVertical": 12, "fontSize": 16},
    "xl": {"paddingHorizontal": 32, "paddingVertical": 16, "fontSize": 18},
}


class _StyleSheet:
    """Accumulates StyleSheet entries; emits them as a `StyleSheet.create({...})` payload."""

    def __init__(self) -> None:
        self._entries: list[tuple[str, dict]] = []
        self._counter = 0

    def add(self, base_name: str, style: dict) -> str:
        self._counter += 1
        key = f"{_safe_id(base_name)}_{self._counter}"
        self._entries.append((key, style))
        return key

    def render(self) -> str:
        if not self._entries:
            return "{}"
        lines = ["{"]
        for key, style in self._entries:
            lines.append(f"  {key}: {{")
            for k, v in style.items():
                if isinstance(v, str) and not v.startswith("colors.") and v != "transparent":
                    lines.append(f'    {k}: "{v}",')
                elif isinstance(v, str) and v.startswith("colors."):
                    lines.append(f"    {k}: {v},")
                elif isinstance(v, str):  # transparent
                    lines.append(f'    {k}: "{v}",')
                else:
                    lines.append(f"    {k}: {v},")
            lines.append("  },")
        lines.append("}")
        return "\n".join(lines)


# Common tone aliases the skills emit as shorthand (`tone: "muted"`) →
# canonical token role. Anything else falls through to literal pass-through.
_TONE_ALIASES = {
    "muted":     "textMuted",
    "secondary": "textSecondary",
    "primary":   "textPrimary",
    "on-brand":  "textOnBrand",
    "success":   "feedbackSuccess",
    "warning":   "feedbackWarning",
    "error":     "feedbackError",
    "info":      "feedbackInfo",
}


def _resolve_color(token_or_literal: str) -> str:
    """Map a token role / tone alias to its accessor, or pass through a literal."""
    canonical = _TONE_ALIASES.get(token_or_literal, token_or_literal)
    if canonical in TOKEN_ROLE_MAP:
        return TOKEN_ROLE_MAP[canonical]
    return canonical


def _render_node(
    node: dict,
    sheet: _StyleSheet,
    imports: set[str],
    depth: int = 2,
) -> str:
    indent = "  " * depth
    type_ = node["type"]
    component = WIDGET_TYPE_MAP.get(type_, "View")
    imports.add(component)
    if component in ("StyleSheet",):
        pass

    props = dict(node.get("props", {}))
    children = node.get("children", [])
    label = props.pop("label", None)
    text_value = props.pop("value", None)

    # Build a style entry for this node.
    style: dict = {}
    if type_ == "button":
        variant = node.get("variant", "primary")
        size = node.get("size", "md")
        v = _BUTTON_VARIANT_STYLE.get(variant, _BUTTON_VARIANT_STYLE["primary"])
        s = _BUTTON_SIZE_STYLE.get(size, _BUTTON_SIZE_STYLE["md"])
        if v["bg"] == "transparent":
            style["backgroundColor"] = "transparent"
        else:
            style["backgroundColor"] = _resolve_color(v["bg"])
        if v.get("borderWidth", 0):
            style["borderWidth"] = v["borderWidth"]
            style["borderColor"] = _resolve_color(v.get("borderColor", "borderDefault"))
        style["paddingHorizontal"] = s["paddingHorizontal"]
        style["paddingVertical"]   = s["paddingVertical"]
        style["borderRadius"]      = 8
        style["alignItems"]        = "center"
        style["justifyContent"]    = "center"
        if props.pop("fullWidth", False):
            style["alignSelf"] = "stretch"

    elif type_ == "text":
        style["color"] = _resolve_color(props.pop("tone", "textPrimary"))

    elif type_ == "input":
        style["borderWidth"]   = 1
        style["borderColor"]   = _resolve_color("borderDefault")
        style["borderRadius"]  = 8
        style["paddingHorizontal"] = 12
        style["paddingVertical"]   = 10
        style["color"]         = _resolve_color("textPrimary")
        style["backgroundColor"] = _resolve_color("bgInput")

    elif type_ in ("container", "form-group", "card"):
        if type_ == "card":
            style["backgroundColor"] = _resolve_color("bgSurfaceRaised")
            style["padding"]         = 16
            style["borderRadius"]    = 12
        else:
            style["gap"] = 8

    elif type_ == "divider":
        style["height"] = 1
        style["backgroundColor"] = _resolve_color("borderDefault")

    elif type_ == "spacer":
        style["height"] = node.get("size", 8) if isinstance(node.get("size"), (int, float)) else 8

    elif type_ == "badge":
        style["paddingHorizontal"] = 8
        style["paddingVertical"]   = 2
        style["borderRadius"]      = 999
        style["backgroundColor"]   = _resolve_color("brandMuted")

    style_key = sheet.add(node.get("variant", type_), style) if style else None

    # Build attribute list.
    attrs: list[str] = []
    if style_key:
        attrs.append(f"style={{styles.{style_key}}}")
    if "variant" in node and type_ not in ("button", "text"):
        attrs.append(f'data-variant="{node["variant"]}"')

    for k, v in props.items():
        if isinstance(v, bool):
            if v:
                attrs.append(k)
        elif isinstance(v, (int, float)):
            attrs.append(f"{k}={{{v}}}")
        elif isinstance(v, str):
            # `placeholder`, `name`, `autocomplete` etc — passed as attributes.
            attrs.append(f'{k}="{_escape(v)}"')
        else:
            attrs.append(f"{k}={{{json.dumps(v)}}}")

    # Inputs (TextInput, Switch, Slider, Checkbox) are *always* self-closing in RN.
    # Their label, when present, is emitted as a sibling <Text> wrapped with the
    # input in a <View> at the same depth — the parent container handles layout.
    INPUT_TYPES = {"input", "checkbox", "switch", "slider"}
    is_input = type_ in INPUT_TYPES

    self_closing = type_ in {"image", "icon", "divider", "spacer", "progress"} and not children
    if is_input:
        self_closing = not children
        # Label cannot be a child of <TextInput>/<Switch>/<Slider>; it goes outside.

    open_tag = component + (" " + " ".join(attrs) if attrs else "")

    if is_input and label is not None:
        # Emit a sibling label + self-closing input wrapped in a View.
        imports.add("Text")
        imports.add("View")
        wrap_key = sheet.add(f"{type_}_field", {"gap": 4})
        label_key = sheet.add(f"{type_}_label", {
            "color": _resolve_color("textSecondary"),
            "fontSize": 13,
            "fontWeight": '500',
        })
        return (
            f"{indent}<View style={{styles.{wrap_key}}}>\n"
            f'{indent}  <Text style={{styles.{label_key}}}>{_escape(str(label))}</Text>\n'
            f"{indent}  <{open_tag} />\n"
            f"{indent}</View>"
        )

    if self_closing and label is None and text_value is None:
        return f"{indent}<{open_tag} />"

    inner_lines: list[str] = []
    if label is not None:
        # Label always rendered as a child <Text> for RN (RN won't accept bare strings outside <Text>).
        if type_ == "button":
            text_color = _BUTTON_VARIANT_STYLE.get(node.get("variant", "primary"), {}).get("fg", "textPrimary")
            text_size  = _BUTTON_SIZE_STYLE.get(node.get("size", "md"), {}).get("fontSize", 16)
            label_style_key = sheet.add(f"{type_}_label", {
                "color": _resolve_color(text_color),
                "fontSize": text_size,
                "fontWeight": '500',
            })
            imports.add("Text")
            inner_lines.append(f'{indent}  <Text style={{styles.{label_style_key}}}>{_escape(str(label))}</Text>')
        elif type_ == "text":
            inner_lines.append(f"{indent}  {_escape(str(label))}")
        else:
            imports.add("Text")
            inner_lines.append(f"{indent}  <Text>{_escape(str(label))}</Text>")
    if text_value is not None:
        inner_lines.append(f"{indent}  {_escape(str(text_value))}")
    for c in children:
        inner_lines.append(_render_node(c, sheet, imports, depth + 1))

    body = "\n".join(inner_lines) if inner_lines else ""
    if body:
        return f"{indent}<{open_tag}>\n{body}\n{indent}</{component}>"
    return f"{indent}<{open_tag}></{component}>"


def render_widget_tree(plan: dict, plan_path: str, project: dict) -> dict[int, str]:
    out: dict[int, str] = {}
    widgets = plan["widgets"]
    components = [a for a in plan["actions"] if a["intent"] == "component"]
    if len(components) != 1 or len(widgets) < 1:
        raise ValueError("react-native widget-tree: expects exactly 1 component action")

    sheet = _StyleSheet()
    imports: set[str] = {"StyleSheet"}
    tree = _render_node(widgets[0], sheet, imports, depth=2)

    core_used = sorted(i for i in imports if i in RN_CORE_IMPORTS)
    community_used = sorted(i for i in imports if i in RN_COMMUNITY_IMPORTS)

    import_lines: list[str] = []
    if core_used:
        import_lines.append(f'import {{ {", ".join(core_used)} }} from "react-native";')
    for name in community_used:
        import_lines.append(f'import {name} from "{RN_COMMUNITY_IMPORTS[name]}";')
    import_block = "\n".join(import_lines)
    if import_block:
        import_block += "\n"

    rendered = _load("component.tsx.tmpl").substitute(
        plan_path=plan_path,
        imports=import_block,
        name=components[0]["name"],
        tree=tree,
        styles_object=sheet.render(),
    )
    for i, action in enumerate(plan["actions"]):
        if action is components[0]:
            out[i] = rendered
    return out


# ---- driver -----------------------------------------------------------------

def render(plan: dict, plan_path: str, project: dict | None = None) -> dict[int, str]:
    project = project or {"expo": False, "router": "src"}
    kind = plan["kind"]
    if kind == "palette":
        return render_palette(plan, plan_path, project)
    if kind == "widget-tree":
        return render_widget_tree(plan, plan_path, project)
    if kind == "motion-set":
        return render_motion(plan, plan_path, project)
    raise KeyError(f"react-native adapter: unknown kind {kind!r}")


def main(plan_path: str, dry_run: bool = False, expo: bool | None = None, router: str | None = None) -> int:
    plan = json.loads(Path(plan_path).read_text())
    project = {
        "expo":   expo if expo is not None else has_expo(),
        "router": router or app_or_src(),
    }
    rendered = render(plan, plan_path, project)
    for i, action in enumerate(plan["actions"]):
        path = resolve_path(action, plan, project)
        content = rendered[i]
        if dry_run:
            print(f"would write: {path} ({len(content)} bytes)")
        else:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            mode = "a" if action.get("op") == "append" else "w"
            with open(path, mode) as f:
                f.write(content)
            print(f"wrote: {path} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="design-workflow react-native adapter")
    parser.add_argument("plan", help="path to Adapter Plan JSON")
    parser.add_argument("--dry-run", action="store_true")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--expo",     action="store_true", help="force Expo conventions")
    g.add_argument("--bare-rn",  action="store_true", help="force bare RN conventions")
    parser.add_argument("--router", choices=["app", "src"], default=None)
    args = parser.parse_args()
    forced = True if args.expo else (False if args.bare_rn else None)
    sys.exit(main(args.plan, dry_run=args.dry_run, expo=forced, router=args.router))
