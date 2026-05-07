"""React Native adapter — role/widget mappings, project detection, paths.

Mirrors the contract documented in `docs/adapter-protocol.md` and matches the
shape used by `adapters/flutter/` and `adapters/nextjs-tailwind/`. RN is a
*native* paradigm (no CSS, no Tailwind), so token roles map to TypeScript
const accessors and widgets map to RN core components.
"""
from __future__ import annotations
import json
import os
from pathlib import Path

# 29 canonical roles → camelCase accessor on the `colors` const.
# Emitted as `colors.brandDefault` from inside a component:
#     import { useColors } from "@/theme/useColors";
#     const colors = useColors();
#     <Text style={{ color: colors.textPrimary }}>...</Text>
TOKEN_ROLE_MAP: dict[str, str] = {
    "brandDefault":         "colors.brandDefault",
    "brandMuted":           "colors.brandMuted",
    "brandPressed":         "colors.brandPressed",
    "brandDisabled":        "colors.brandDisabled",
    "brandOnColor":         "colors.brandOnColor",
    "bgBase":               "colors.bgBase",
    "bgSurface":            "colors.bgSurface",
    "bgSurfaceRaised":      "colors.bgSurfaceRaised",
    "bgInput":              "colors.bgInput",
    "bgOverlay":            "colors.bgOverlay",
    "bgSkeleton":           "colors.bgSkeleton",
    "borderDefault":        "colors.borderDefault",
    "borderStrong":         "colors.borderStrong",
    "borderFocus":          "colors.borderFocus",
    "textPrimary":          "colors.textPrimary",
    "textSecondary":        "colors.textSecondary",
    "textMuted":            "colors.textMuted",
    "textOnBrand":          "colors.textOnBrand",
    "feedbackSuccess":      "colors.feedbackSuccess",
    "feedbackSuccessMuted": "colors.feedbackSuccessMuted",
    "feedbackWarning":      "colors.feedbackWarning",
    "feedbackWarningMuted": "colors.feedbackWarningMuted",
    "feedbackError":        "colors.feedbackError",
    "feedbackErrorMuted":   "colors.feedbackErrorMuted",
    "feedbackInfo":         "colors.feedbackInfo",
    "feedbackInfoMuted":    "colors.feedbackInfoMuted",
    "gameAccent":           "colors.gameAccent",
    "gameAccentMuted":      "colors.gameAccentMuted",
    "gameAccentOnColor":    "colors.gameAccentOnColor",
}


# RN widget type → React Native core component.
# RN doesn't ship native form primitives (Select, Slider, Checkbox, Switch are
# split between core API and community packages), so we map to either the core
# or a stable convention:
#   - core:        View, Text, Pressable, TextInput, Image, ScrollView, FlatList
#   - community:   @react-native-community/slider for slider; native Switch is core.
WIDGET_TYPE_MAP: dict[str, str] = {
    "button":     "Pressable",     # touch surface; the user-facing label is a child <Text>
    "text":       "Text",
    "container":  "View",
    "form-group": "View",          # RN has no <form>; group with View
    "image":      "Image",
    "icon":       "Text",          # placeholder; icon libs vary (@expo/vector-icons, react-native-vector-icons)
    "input":      "TextInput",
    "select":     "View",          # RN core has no Select; downstream wires @react-native-picker/picker
    "checkbox":   "Pressable",     # RN core has no Checkbox; community package or hand-roll
    "switch":     "Switch",        # RN core
    "slider":     "Slider",        # community: @react-native-community/slider
    "card":       "View",
    "list":       "FlatList",
    "list-item":  "View",
    "divider":    "View",
    "spacer":     "View",
    "link":       "Text",          # links route via onPress + Linking
    "badge":      "View",
    "avatar":     "Image",
    "progress":   "View",          # rendered as bar via View with width style
}


# Imports keyed by component name. Resolved into a single grouped import block
# at top of the rendered component file. Native RN core components share one
# `from "react-native"` import; non-core (e.g. Slider) get their own line.
RN_CORE_IMPORTS = {
    "View", "Text", "Pressable", "TextInput", "Image",
    "ScrollView", "FlatList", "Switch",
    "StyleSheet",  # always imported when StyleSheet.create is emitted
}

RN_COMMUNITY_IMPORTS: dict[str, str] = {
    "Slider": "@react-native-community/slider",
}


# Spacing scale — RN uses raw numbers (DPs, not px). 4-pt grid baseline.
def to_rn_spacing(px: float) -> int | float:
    """Map pixel value to RN style number (no unit; RN treats numbers as DPs)."""
    if px == 0:
        return 0
    if px == int(px):
        return int(px)
    return px


# Curve enum → RN-friendly easing reference.
# Emitted as a string referencing `Easing` from react-native — the consumer
# imports Easing themselves: `import { Easing } from "react-native";`.
CURVE_MAP: dict[str, str] = {
    "linear":     "Easing.linear",
    "easeIn":     "Easing.in(Easing.ease)",
    "easeOut":    "Easing.out(Easing.ease)",
    "easeInOut":  "Easing.inOut(Easing.ease)",
    "spring":     "Easing.elastic(1)",
    "bounce":     "Easing.bounce",
    "anticipate": "Easing.in(Easing.back(1.5))",
    "decelerate": "Easing.out(Easing.cubic)",
}


def has_expo(project_root: str | Path | None = None) -> bool:
    """Detect Expo project (presence of `expo` in package.json deps OR app.json)."""
    root = Path(project_root) if project_root else Path.cwd()
    if (root / "app.json").exists():
        try:
            data = json.loads((root / "app.json").read_text())
            if isinstance(data, dict) and "expo" in data:
                return True
        except Exception:
            pass
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
        except Exception:
            return False
        for section in ("dependencies", "devDependencies"):
            for name in (data.get(section) or {}).keys():
                if name == "expo" or name.startswith("expo-"):
                    return True
    return False


# Project structure detection — Expo prefers `app/` (Expo Router) or `src/`;
# bare RN typically uses `src/` or repo-root. Fall back to `src/` for greenfield.
def app_or_src(project_root: str | Path | None = None) -> str:
    root = Path(project_root) if project_root else Path.cwd()
    if (root / "app").exists() and (root / "app.json").exists():
        return "app"  # Expo Router
    if (root / "src").exists():
        return "src"
    return "src"


# Default emission paths.
DEFAULT_PATHS_SRC: dict[tuple[str, str], str] = {
    ("palette",       "tokens"):      "src/theme/colors.ts",
    ("motion",        "tokens"):      "src/theme/motion.ts",
    ("design-tokens", "doc-summary"): "docs/design-tokens.md",
}

DEFAULT_PATHS_APP: dict[tuple[str, str], str] = {
    ("palette",       "tokens"):      "app/theme/colors.ts",
    ("motion",        "tokens"):      "app/theme/motion.ts",
    ("design-tokens", "doc-summary"): "docs/design-tokens.md",
}


def resolve_path(action: dict, plan: dict, project: dict, overrides: dict | None = None) -> str:
    overrides = overrides or {}
    role, intent = action["role"], action["intent"]

    if intent == "component":
        feature = plan.get("meta", {}).get("feature", "common")
        components_root = overrides.get("components_root", project.get("components_root", "src/components"))
        return os.path.join(components_root, feature, f"{action['name']}.tsx")

    table = DEFAULT_PATHS_APP if project.get("router") == "app" else DEFAULT_PATHS_SRC
    if (role, intent) in overrides:
        return overrides[(role, intent)]
    if (role, intent) in table:
        return overrides.get(intent + "_" + role, table[(role, intent)])
    raise KeyError(f"react-native adapter: no path for role={role!r} intent={intent!r}")
