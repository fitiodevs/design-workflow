"""Flutter adapter — role/widget mappings + path resolution.

Token roles map to Dart accessors via TOKEN_ROLE_MAP; widget types map to
Flutter component classes via WIDGET_TYPE_MAP. Path resolution honors
`.design-workflow.yaml` `paths.flutter` overrides; defaults documented in
STACK_NOTES.md.
"""
from __future__ import annotations
import os

# Canonical 29 token roles → Dart accessor (BuildContext extension idiom).
TOKEN_ROLE_MAP: dict[str, str] = {
    "brandDefault":         "context.colors.brandDefault",
    "brandMuted":           "context.colors.brandMuted",
    "brandPressed":         "context.colors.brandPressed",
    "brandDisabled":        "context.colors.brandDisabled",
    "brandOnColor":         "context.colors.brandOnColor",
    "bgBase":               "context.colors.bgBase",
    "bgSurface":            "context.colors.bgSurface",
    "bgSurfaceRaised":      "context.colors.bgSurfaceRaised",
    "bgInput":              "context.colors.bgInput",
    "bgOverlay":            "context.colors.bgOverlay",
    "bgSkeleton":           "context.colors.bgSkeleton",
    "borderDefault":        "context.colors.borderDefault",
    "borderStrong":         "context.colors.borderStrong",
    "borderFocus":          "context.colors.borderFocus",
    "textPrimary":          "context.colors.textPrimary",
    "textSecondary":        "context.colors.textSecondary",
    "textMuted":            "context.colors.textMuted",
    "textOnBrand":          "context.colors.textOnBrand",
    "feedbackSuccess":      "context.colors.feedbackSuccess",
    "feedbackSuccessMuted": "context.colors.feedbackSuccessMuted",
    "feedbackWarning":      "context.colors.feedbackWarning",
    "feedbackWarningMuted": "context.colors.feedbackWarningMuted",
    "feedbackError":        "context.colors.feedbackError",
    "feedbackErrorMuted":   "context.colors.feedbackErrorMuted",
    "feedbackInfo":         "context.colors.feedbackInfo",
    "feedbackInfoMuted":    "context.colors.feedbackInfoMuted",
    "gameAccent":           "context.colors.gameAccent",
    "gameAccentMuted":      "context.colors.gameAccentMuted",
    "gameAccentOnColor":    "context.colors.gameAccentOnColor",
}

# Widget node `type` → Flutter component class. Project-specific App* prefixes
# preferred; bare Material fallback noted but not emitted (v1.2 leaves it as
# a comment for the developer to wire).
WIDGET_TYPE_MAP: dict[str, str] = {
    "button":     "AppButton",
    "text":       "AppText",
    "container":  "Container",
    "form-group": "AppFormGroup",
    "image":      "Image",
    "icon":       "AppIcon",
    "input":      "AppInput",
    "select":     "AppSelect",
    "checkbox":   "AppCheckbox",
    "switch":     "AppSwitch",
    "slider":     "AppSlider",
    "card":       "AppCard",
    "list":       "AppList",
    "list-item":  "AppListItem",
    "divider":    "AppDivider",
    "spacer":     "SizedBox",
    "link":       "AppLink",
    "badge":      "AppBadge",
    "avatar":     "AppAvatar",
    "progress":   "AppProgress",
}

# Default paths per role/intent. Override via paths.flutter in config.
DEFAULT_PATHS: dict[tuple[str, str], str] = {
    ("palette",       "tokens"):      "lib/core/theme/app_colors.dart",
    ("spacing",       "tokens"):      "lib/core/theme/app_spacing.dart",
    ("radius",        "tokens"):      "lib/core/theme/app_radius.dart",
    ("typography",    "tokens"):      "lib/core/theme/text_theme.dart",
    ("motion",        "tokens"):      "lib/core/theme/app_motion.dart",
    ("design-tokens", "doc-summary"): "docs/design-tokens.md",
}


def resolve_path(action: dict, plan: dict, overrides: dict | None = None) -> str:
    """Resolve a Plan action to a concrete file path.

    Order: explicit overrides → DEFAULT_PATHS → component path computed
    from `plan` metadata + action.name.
    """
    overrides = overrides or {}
    role, intent = action["role"], action["intent"]

    if intent == "component":
        name = action["name"]
        feature = plan.get("meta", {}).get("feature", "common")
        snake = _camel_to_snake(name)
        root = overrides.get("widgets_root", "lib/features/{feature}/presentation/widgets")
        root = root.format(feature=feature)
        return os.path.join(root, f"{snake}.dart")

    key = (role, intent)
    if key in overrides:
        return overrides[key]
    if key in DEFAULT_PATHS:
        return DEFAULT_PATHS[key]
    raise KeyError(f"flutter adapter: no path for role={role!r} intent={intent!r}")


def _camel_to_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)
