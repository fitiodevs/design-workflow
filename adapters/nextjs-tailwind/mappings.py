"""Next.js + Tailwind adapter — role/widget mappings, project detection, paths."""
from __future__ import annotations
import json
import os
import re
from pathlib import Path

# 29 canonical roles → CSS custom property name.
TOKEN_ROLE_MAP: dict[str, str] = {
    "brandDefault":         "--brand-default",
    "brandMuted":           "--brand-muted",
    "brandPressed":         "--brand-pressed",
    "brandDisabled":        "--brand-disabled",
    "brandOnColor":         "--brand-on-color",
    "bgBase":               "--bg-base",
    "bgSurface":            "--bg-surface",
    "bgSurfaceRaised":      "--bg-surface-raised",
    "bgInput":              "--bg-input",
    "bgOverlay":            "--bg-overlay",
    "bgSkeleton":           "--bg-skeleton",
    "borderDefault":        "--border-default",
    "borderStrong":         "--border-strong",
    "borderFocus":          "--border-focus",
    "textPrimary":          "--text-primary",
    "textSecondary":        "--text-secondary",
    "textMuted":            "--text-muted",
    "textOnBrand":          "--text-on-brand",
    "feedbackSuccess":      "--feedback-success",
    "feedbackSuccessMuted": "--feedback-success-muted",
    "feedbackWarning":      "--feedback-warning",
    "feedbackWarningMuted": "--feedback-warning-muted",
    "feedbackError":        "--feedback-error",
    "feedbackErrorMuted":   "--feedback-error-muted",
    "feedbackInfo":         "--feedback-info",
    "feedbackInfoMuted":    "--feedback-info-muted",
    "gameAccent":           "--game-accent",
    "gameAccentMuted":      "--game-accent-muted",
    "gameAccentOnColor":    "--game-accent-on-color",
}


# Tailwind nested colors keyed by camelCase role; emitted as nested objects in
# tailwind.config.ts under theme.extend.colors.
def role_to_tailwind_path(role: str) -> tuple[str, str]:
    """Return (group, leaf) where group is e.g. 'brand' and leaf 'default'."""
    m = re.match(r"^([a-z]+?)([A-Z][a-zA-Z]*)$", role)
    if m:
        group, leaf = m.group(1), m.group(2)
        return group, leaf[0].lower() + leaf[1:]
    return role, "DEFAULT"


# Widget type → JSX element. SHADCN_MAP wins when project has shadcn detected.
WIDGET_TYPE_MAP_PLAIN: dict[str, str] = {
    "button":     "button",
    "text":       "span",
    "container":  "div",
    "form-group": "form",
    "image":      "img",
    "icon":       "span",
    "input":      "input",
    "select":     "select",
    "checkbox":   "input",  # type="checkbox"
    "switch":     "button",  # role="switch"
    "slider":     "input",  # type="range"
    "card":       "div",
    "list":       "ul",
    "list-item":  "li",
    "divider":    "hr",
    "spacer":     "div",
    "link":       "a",
    "badge":      "span",
    "avatar":     "img",
    "progress":   "progress",
}

WIDGET_TYPE_MAP_SHADCN: dict[str, str] = {
    "button":     "Button",
    "input":      "Input",
    "select":     "Select",
    "checkbox":   "Checkbox",
    "switch":     "Switch",
    "slider":     "Slider",
    "card":       "Card",
    "badge":      "Badge",
    "avatar":     "Avatar",
    "progress":   "Progress",
}

SHADCN_IMPORTS: dict[str, str] = {
    "Button":   '@/components/ui/button',
    "Input":    '@/components/ui/input',
    "Select":   '@/components/ui/select',
    "Checkbox":'@/components/ui/checkbox',
    "Switch":   '@/components/ui/switch',
    "Slider":   '@/components/ui/slider',
    "Card":     '@/components/ui/card',
    "Badge":    '@/components/ui/badge',
    "Avatar":   '@/components/ui/avatar',
    "Progress": '@/components/ui/progress',
}


# Spacing → Tailwind class fragment. Tailwind's default scale: spacing.4 = 1rem (16px).
def px_to_tailwind_unit(px: float) -> str:
    """Map pixel value to Tailwind spacing key (assuming default 4px = 1 unit)."""
    if px == 0:
        return "0"
    if px % 4 == 0:
        return str(int(px // 4))
    return f"[{int(px)}px]"


def has_shadcn(project_root: str | Path | None = None) -> bool:
    root = Path(project_root) if project_root else Path.cwd()
    if (root / "components.json").exists():
        return True
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
        except Exception:
            return False
        for section in ("dependencies", "devDependencies"):
            for name in (data.get(section) or {}).keys():
                if name.startswith("@radix-ui/"):
                    return True
    return False


def app_router_or_pages(project_root: str | Path | None = None) -> str:
    root = Path(project_root) if project_root else Path.cwd()
    if (root / "app").exists():
        return "app"
    if (root / "pages").exists():
        return "pages"
    return "app"  # default for greenfield writes


DEFAULT_PATHS_APP: dict[tuple[str, str], str] = {
    ("palette",       "tokens"):      "app/globals.css",
    ("motion",        "tokens"):      "app/globals.css",
    ("design-tokens", "doc-summary"): "docs/design-tokens.md",
}

DEFAULT_PATHS_PAGES: dict[tuple[str, str], str] = {
    ("palette",       "tokens"):      "styles/tokens.css",
    ("motion",        "tokens"):      "styles/tokens.css",
    ("design-tokens", "doc-summary"): "docs/design-tokens.md",
}

TAILWIND_CONFIG_PATH = "tailwind.config.ts"


def resolve_path(action: dict, plan: dict, project: dict, overrides: dict | None = None) -> str:
    overrides = overrides or {}
    role, intent = action["role"], action["intent"]

    if intent == "component":
        feature = plan.get("meta", {}).get("feature", "common")
        components_root = overrides.get("components_root", "components")
        return os.path.join(components_root, feature, f"{action['name']}.tsx")

    if intent == "config":
        return overrides.get("tailwind_config", TAILWIND_CONFIG_PATH)

    table = DEFAULT_PATHS_APP if project.get("router", "app") == "app" else DEFAULT_PATHS_PAGES
    if (role, intent) in overrides:
        return overrides[(role, intent)]
    if role == "palette" and intent == "tokens":
        return overrides.get("tokens_css", table[(role, intent)])
    if (role, intent) in table:
        return table[(role, intent)]
    raise KeyError(f"nextjs-tailwind adapter: no path for role={role!r} intent={intent!r}")
