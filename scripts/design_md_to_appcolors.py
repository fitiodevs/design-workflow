#!/usr/bin/env python3
"""
Translate a `design-systems/<slug>/DESIGN.md` into a Fitio AppColors proposal.

Outputs (per slug, into --out-dir):
    proposal.json   29 tokens × 2 modes (light + dark) + metadata + WCAG report
    rationale.md    Source citation, mapping table, WCAG report, open questions

Usage:
    python3 scripts/design_md_to_appcolors.py design-systems/claude/DESIGN.md
    python3 scripts/design_md_to_appcolors.py design-systems/claude/DESIGN.md --out-dir /tmp/out
    python3 scripts/design_md_to_appcolors.py --validate-all
    python3 scripts/design_md_to_appcolors.py design-systems/claude/DESIGN.md --dry-run

Phases (per design D-A..D-F in inspiration-library/design.md):
    1. parse_design_md    Split into sections (visual_theme, color_palette buckets, typography).
    2. extract_palette    Pull (name, hex, description) tuples per palette subheader.
    3. map_to_appcolors   Inference chain: section semantic > regex order > WCAG fallback.
    4. derive_dark_mode   If source dark-native or has explicit dark-surface hexes, use them; else L-flip.
    5. validate_wcag      12 mandatory pairs × 2 modes; failures flagged + corrected alt proposed.
    6. write_artifacts    proposal.json + rationale.md.

Reuses:
    scripts/check_contrast.contrast_ratio
    scripts/oklch_to_hex.hex_to_oklch / oklch_to_hex
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from check_contrast import contrast_ratio  # noqa: E402
from oklch_to_hex import hex_to_oklch, oklch_to_hex  # noqa: E402

# ---- 29 AppColors tokens -----------------------------------------------------

APPCOLORS_TOKENS: list[str] = [
    "brandDefault", "brandMuted", "brandOnColor",
    "bgBase", "bgSurface", "bgSurfaceRaised", "bgInput",
    "textPrimary", "textSecondary", "textMuted", "textOnBrand",
    "borderDefault", "borderStrong", "borderFocus",
    "feedbackSuccess", "feedbackSuccessMuted",
    "feedbackWarning", "feedbackWarningMuted",
    "feedbackError", "feedbackErrorMuted",
    "feedbackInfo", "feedbackInfoMuted",
    "gameAccent", "gameAccentMuted", "gameAccentOnColor",
    "badgeNew", "badgeAlert", "badgeReward", "badgeOnline",
]
assert len(APPCOLORS_TOKENS) == 29, "AppColors must always have 29 tokens"

# Tokens with no equivalent in a brand DESIGN.md — flagged for user input (D-C step 5).
GAME_TOKENS = {"gameAccent", "gameAccentMuted", "gameAccentOnColor"}
BADGE_TOKENS = {"badgeNew", "badgeAlert", "badgeReward", "badgeOnline"}
USER_INPUT_TOKENS = GAME_TOKENS | BADGE_TOKENS  # 7

# WCAG 12 mandatory pairs (each tuple: (fg, bg, ratio_required, label)).
WCAG_PAIRS: list[tuple[str, str, float, str]] = [
    ("textPrimary",   "bgBase",         4.5, "Primary body on page"),
    ("textPrimary",   "bgSurface",      4.5, "Primary body on card"),
    ("textPrimary",   "bgSurfaceRaised",4.5, "Primary body on raised"),
    ("textSecondary", "bgBase",         4.5, "Secondary on page"),
    ("textSecondary", "bgSurface",      4.5, "Secondary on card"),
    ("textMuted",     "bgBase",         3.0, "Muted on page (large/aux)"),
    ("textMuted",     "bgSurface",      3.0, "Muted on card (large/aux)"),
    ("textOnBrand",   "brandDefault",   4.5, "Text on brand surface"),
    ("textPrimary",   "bgInput",        4.5, "Input field text"),
    ("borderFocus",   "bgBase",         3.0, "Focus ring visibility on page"),
    ("borderStrong",  "bgBase",         3.0, "Strong border on page"),
    ("textPrimary",   "bgInput",        4.5, "Input chrome text"),  # second occurrence allowed
]

# ---- Phase 1: parse_design_md ------------------------------------------------

# Bullet pattern: `- **Name** (\`#hex[hex...]\`): description`
BULLET_RE = re.compile(
    r"^\s*[-*]\s+\*\*(?P<name>[^*]+)\*\*\s*\(`?#(?P<hex>[0-9a-fA-F]{3,8})`?\)\s*:?\s*(?P<desc>.*)$"
)
# Fallback bullet (no bold name): `- \`#hex\` description`
FALLBACK_BULLET_RE = re.compile(
    r"^\s*[-*]\s+`?#(?P<hex>[0-9a-fA-F]{3,8})`?\s*[:\-—]?\s*(?P<desc>.*)$"
)
H2_RE = re.compile(r"^##\s+\d?\.?\s*(?P<title>.+?)\s*$")
H3_RE = re.compile(r"^###\s+(?P<title>.+?)\s*$")
CATEGORY_RE = re.compile(r"^>\s*Category:\s*(?P<cat>.+?)\s*$")
TITLE_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$")


@dataclass
class PaletteEntry:
    name: str
    hex: str
    desc: str
    section: str  # the H3 subheader bucket


@dataclass
class ParsedDoc:
    slug: str
    title: str
    category: str
    visual_theme: str
    palette: list[PaletteEntry] = field(default_factory=list)
    typography_block: str = ""


def _normalize_hex(h: str) -> str:
    h = h.lstrip("#").lower()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8:
        h = h[2:]  # drop alpha
    return f"#{h}"


def parse_design_md(path: Path) -> ParsedDoc:
    """Phase 1: split DESIGN.md into sections + extract palette tuples."""
    slug = path.parent.name
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    category = "Uncategorized"
    cur_h2: Optional[str] = None
    cur_h3: Optional[str] = None
    visual_theme_lines: list[str] = []
    typography_lines: list[str] = []
    palette: list[PaletteEntry] = []

    in_visual_theme = False
    in_color_palette = False
    in_typography = False

    for line in lines:
        if not title:
            mt = TITLE_RE.match(line)
            if mt:
                title = mt.group("title").strip()
                continue
        mc = CATEGORY_RE.match(line)
        if mc:
            category = mc.group("cat").strip()
            continue

        m2 = H2_RE.match(line)
        if m2:
            cur_h2 = m2.group("title").strip().lower()
            cur_h3 = None
            in_visual_theme = "visual theme" in cur_h2 or "atmosphere" in cur_h2
            in_color_palette = "color palette" in cur_h2 or cur_h2.startswith("colors")
            in_typography = "typography" in cur_h2
            continue

        m3 = H3_RE.match(line)
        if m3:
            cur_h3 = m3.group("title").strip()
            continue

        if in_visual_theme:
            visual_theme_lines.append(line)
            continue
        if in_typography:
            typography_lines.append(line)
            continue
        if in_color_palette and cur_h3:
            mb = BULLET_RE.match(line)
            if not mb:
                mb = FALLBACK_BULLET_RE.match(line)
                if mb:
                    palette.append(PaletteEntry(
                        name=f"<unnamed-{len(palette)}>",
                        hex=_normalize_hex(mb.group("hex")),
                        desc=mb.group("desc").strip(),
                        section=cur_h3,
                    ))
                continue
            palette.append(PaletteEntry(
                name=mb.group("name").strip(),
                hex=_normalize_hex(mb.group("hex")),
                desc=mb.group("desc").strip(),
                section=cur_h3,
            ))

    visual_theme = "\n".join(l for l in visual_theme_lines if l.strip()).strip()
    typography_block = "\n".join(l for l in typography_lines if l.strip()).strip()

    return ParsedDoc(
        slug=slug,
        title=title,
        category=category,
        visual_theme=visual_theme,
        palette=palette,
        typography_block=typography_block,
    )


# ---- Phase 2: extract_palette into semantic buckets --------------------------

# Bucket keywords (matched against H3 title, lowercase substring).
BUCKET_KEYWORDS: dict[str, list[str]] = {
    "brand":     ["primary", "brand", "accent"],
    "surface":   ["surface", "background", "backgrounds"],
    "text":      ["text", "neutral", "neutrals", "content", "ink"],
    "border":    ["border", "divider", "dividers", "outline"],
    "feedback":  ["status", "semantic", "feedback", "system color"],
    "interact":  ["interactive", "hover", "press", "active"],
    "shadow":    ["shadow", "shadows", "depth", "elevation"],
}


BUCKET_ORDER = ["feedback", "shadow", "interact", "border", "surface", "text", "brand"]


# Per-entry NAME keyword overrides (highest priority — match entry name first).
NAME_KEYWORD_OVERRIDES: dict[str, list[str]] = {
    "border":   ["border", "outline", "divider", "stroke"],
    "feedback": ["error", "danger", "success", "warn", "alert", "crimson", "destructive"],
    "shadow":   ["shadow"],
    "surface":  ["surface", "background", "canvas", "page", "panel", "card "],
    "text":     ["heading", "label", "body text", "ink"],
}


SURFACE_DESC_HINTS = ("page background", "page bg", "card background", "panel background", "primary background", "main background", "canvas")
TEXT_DESC_HINTS = ("primary text", "headline text", "body text", "body link", "primary headline", "headings", "primary heading")
BRAND_DESC_HINTS = ("brand color", "primary brand", "cta background", "primary cta", "brand accent")


def _override_bucket(entry: PaletteEntry) -> Optional[str]:
    """Strict-name override + description hints, in priority order.

    Order: border > feedback > shadow > surface (name) > text (name) >
    surface (desc) > text (desc) > brand (desc).
    """
    name = entry.name.lower()
    desc = entry.desc.lower()
    for bucket, kws in NAME_KEYWORD_OVERRIDES.items():
        if any(kw in name for kw in kws):
            return bucket
    if any(hint in desc for hint in SURFACE_DESC_HINTS):
        return "surface"
    if any(hint in desc for hint in TEXT_DESC_HINTS):
        return "text"
    # 'black' in name without other hints → text (e.g. "Cohere Black", "Near Black")
    if "black" in name or "white" in name and "background" not in desc:
        return "text" if "black" in name else None
    if any(hint in desc for hint in BRAND_DESC_HINTS):
        return "brand"
    return None


def bucketize(palette: list[PaletteEntry]) -> dict[str, list[PaletteEntry]]:
    """Group palette entries: per-entry name override > section-level keyword.

    Priority order matters: more specific buckets (feedback/border/surface) win
    over general ones (brand/text) so a section like 'Semantic & Accent' lands
    in feedback, not brand. Per-entry overrides catch e.g. 'Border Cream' that
    upstream filed under a Semantic section.
    """
    buckets: dict[str, list[PaletteEntry]] = {k: [] for k in BUCKET_KEYWORDS}
    buckets["other"] = []
    for entry in palette:
        # 1. per-entry name keyword override
        forced = _override_bucket(entry)
        if forced:
            buckets[forced].append(entry)
            continue
        # 2. section-level keyword
        s = entry.section.lower()
        placed = False
        for bucket in BUCKET_ORDER:
            kws = BUCKET_KEYWORDS[bucket]
            if any(kw in s for kw in kws):
                buckets[bucket].append(entry)
                placed = True
                break
        if not placed:
            buckets["other"].append(entry)
    return buckets


# ---- Phase 3: map_to_appcolors -----------------------------------------------

@dataclass
class MappingDecision:
    token: str
    chosen_hex: Optional[str]
    source_name: str
    source_section: str
    reason: str


def hex_luminance(h: str) -> float:
    """Return 0..1 luminance via relative brightness shortcut (good enough for sorting)."""
    rgb = tuple(int(h[i:i+2], 16) / 255.0 for i in (1, 3, 5))
    # sRGB perceived brightness (Rec. 709 weights, gamma-uncorrected — fine for sorting)
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def detect_native_mode(buckets: dict[str, list[PaletteEntry]]) -> str:
    """Return 'light' or 'dark' based on dominant surface luminance."""
    surfaces = buckets.get("surface", [])
    if not surfaces:
        return "light"
    # The first surface entry is typically the page background.
    first = surfaces[0]
    return "dark" if hex_luminance(first.hex) < 0.4 else "light"


def _pick_text_for_mode(text_entries: list[PaletteEntry], mode: str) -> list[PaletteEntry]:
    """Filter text entries by polarity (dark-on-light vs light-on-dark) using luminance."""
    if not text_entries:
        return []
    if mode == "light":
        # dark-on-light: keep entries with luminance < 0.55, sort ascending (darkest first)
        kept = [e for e in text_entries if hex_luminance(e.hex) < 0.55]
        return sorted(kept or text_entries, key=lambda e: hex_luminance(e.hex))
    else:
        # light-on-dark: keep luminance > 0.45, sort descending (lightest first)
        kept = [e for e in text_entries if hex_luminance(e.hex) > 0.45]
        return sorted(kept or text_entries, key=lambda e: -hex_luminance(e.hex))


def _pick_surfaces_for_mode(surfaces: list[PaletteEntry], mode: str) -> list[PaletteEntry]:
    if mode == "light":
        kept = [e for e in surfaces if hex_luminance(e.hex) > 0.55]
        return sorted(kept or surfaces, key=lambda e: -hex_luminance(e.hex))
    kept = [e for e in surfaces if hex_luminance(e.hex) < 0.30]
    return sorted(kept or surfaces, key=lambda e: hex_luminance(e.hex))


def _find_feedback(entries: list[PaletteEntry], hint_keywords: list[str]) -> Optional[PaletteEntry]:
    for e in entries:
        blob = (e.name + " " + e.desc + " " + e.section).lower()
        if any(kw in blob for kw in hint_keywords):
            return e
    return None


def _muted_variant(hex_color: str, mode: str) -> str:
    """Lighten (light mode) or darken (dark mode) a color toward a muted background tint."""
    L, C, H = hex_to_oklch(hex_color)
    if mode == "light":
        L = max(0.0, min(1.0, 0.92 - (1 - L) * 0.10))
        C = C * 0.30
    else:
        L = max(0.0, min(1.0, 0.18 + L * 0.10))
        C = C * 0.45
    return oklch_to_hex((L, C, H))


def _derive_on_color(hex_color: str) -> str:
    """Pick black or white text on a brand color based on contrast."""
    if contrast_ratio("#ffffff", hex_color) >= contrast_ratio("#000000", hex_color):
        return "#ffffff"
    return "#000000"


def map_to_appcolors(
    parsed: ParsedDoc,
    buckets: dict[str, list[PaletteEntry]],
    mode: str,
) -> tuple[dict[str, str], list[MappingDecision]]:
    """Phase 3: produce 29-token AppColors map for the given mode."""
    out: dict[str, str] = {}
    decisions: list[MappingDecision] = []

    def record(token: str, chosen: Optional[str], src_name: str, src_section: str, reason: str) -> None:
        decisions.append(MappingDecision(token, chosen, src_name, src_section, reason))
        if chosen is not None:
            out[token] = chosen

    brand_entries = buckets.get("brand", [])
    surface_entries = _pick_surfaces_for_mode(buckets.get("surface", []), mode)
    text_entries = _pick_text_for_mode(buckets.get("text", []), mode)
    border_entries = buckets.get("border", [])
    feedback_entries = buckets.get("feedback", []) + buckets.get("interact", [])

    # ---- BRAND ----
    if brand_entries:
        # The first brand entry (highest-saturation/most-named) is brandDefault.
        # Skip "near black" entries that sometimes appear under "Primary".
        chosen = next((b for b in brand_entries if hex_luminance(b.hex) > 0.10 and hex_luminance(b.hex) < 0.85), brand_entries[0])
        record("brandDefault", chosen.hex, chosen.name, chosen.section, "first non-extreme brand entry under '" + chosen.section + "'")
        # brandMuted: a softer variant — try second brand entry if hue-similar, else compute
        alt = next((b for b in brand_entries if b is not chosen and hex_luminance(b.hex) > 0.55), None)
        if alt:
            record("brandMuted", alt.hex, alt.name, alt.section, "second brand entry, lighter")
        else:
            muted = _muted_variant(chosen.hex, mode)
            record("brandMuted", muted, "<derived>", "<oklch>", f"derived L+C reduction from brandDefault ({chosen.hex})")
        # brandOnColor: B/W contrast pick
        on = _derive_on_color(chosen.hex)
        record("brandOnColor", on, "<derived>", "<contrast>", f"WCAG-best B/W on brandDefault ({chosen.hex})")
    else:
        record("brandDefault", None, "<missing>", "<missing>", "NO BRAND ENTRY FOUND IN SOURCE — needs user input")
        record("brandMuted", None, "<missing>", "<missing>", "depends on brandDefault")
        record("brandOnColor", None, "<missing>", "<missing>", "depends on brandDefault")

    # ---- SURFACES ----
    s = surface_entries
    bg_base = s[0] if s else None
    bg_surface = s[1] if len(s) > 1 else (s[0] if s else None)
    bg_raised = s[2] if len(s) > 2 else bg_surface
    bg_input = s[1] if len(s) > 1 else bg_base
    for tok, ent, why in [
        ("bgBase",         bg_base,    "first surface entry (mode-sorted)"),
        ("bgSurface",      bg_surface, "second surface entry"),
        ("bgSurfaceRaised",bg_raised,  "third surface entry; falls back to surface"),
        ("bgInput",        bg_input,   "second surface entry; semantic input field"),
    ]:
        if ent:
            record(tok, ent.hex, ent.name, ent.section, why)
        else:
            record(tok, None, "<missing>", "<missing>", "no surface entry available")

    # ---- TEXT ----
    t = text_entries
    text_primary = t[0] if t else None
    text_secondary = t[1] if len(t) > 1 else (t[0] if t else None)
    text_muted = t[2] if len(t) > 2 else text_secondary
    text_on_brand = None
    if "brandDefault" in out:
        text_on_brand = _derive_on_color(out["brandDefault"])
    for tok, ent, why in [
        ("textPrimary",   text_primary,   "first text entry, strongest polarity"),
        ("textSecondary", text_secondary, "second text entry"),
        ("textMuted",     text_muted,     "third text entry; tertiary/footnote tier"),
    ]:
        if ent:
            record(tok, ent.hex, ent.name, ent.section, why)
        else:
            record(tok, None, "<missing>", "<missing>", "no text entry; consider WCAG-derived")
    if text_on_brand:
        record("textOnBrand", text_on_brand, "<derived>", "<contrast>", "B/W chosen for max contrast on brandDefault")
    else:
        record("textOnBrand", None, "<missing>", "<missing>", "depends on brandDefault")

    # ---- BORDERS ----
    b = sorted(border_entries, key=lambda e: hex_luminance(e.hex), reverse=(mode == "light"))
    border_default = b[0] if b else None
    border_strong = b[-1] if b else None
    # Focus ring: try to find an explicit "focus" mention in any bucket
    focus_entry = None
    for entry in parsed.palette:
        blob = (entry.name + " " + entry.desc + " " + entry.section).lower()
        if "focus" in blob or "ring" in blob:
            focus_entry = entry
            break
    if not focus_entry and "brandDefault" in out:
        focus_entry = PaletteEntry(name="<derived from brand>", hex=out["brandDefault"], desc="brand-as-focus fallback", section="<fallback>")
    for tok, ent, why in [
        ("borderDefault", border_default, "first border entry (subtlest in mode)"),
        ("borderStrong",  border_strong,  "last border entry (most prominent)"),
        ("borderFocus",   focus_entry,    "explicit focus/ring mention OR brand fallback"),
    ]:
        if ent:
            record(tok, ent.hex, ent.name, ent.section, why)
        else:
            record(tok, None, "<missing>", "<missing>", "no border entry")

    # ---- FEEDBACK (success, warning, error, info) ----
    # Defaults used only when source has no matching color (e.g. Linear has no error/warning).
    feedback_specs = [
        ("feedbackSuccess", ["success", "green", "ok", "valid", "go"], "#16a34a"),
        ("feedbackWarning", ["warn", "warning", "caution", "yellow", "amber", "alert"], "#d97706"),
        ("feedbackError",   ["error", "danger", "destruct", "fail", "crimson", "red", "negative"], "#dc2626"),
        ("feedbackInfo",    ["info ", "informational", "blue ", "notice", "neutral info"], "#2563eb"),
    ]
    for tok, hints, default_hex in feedback_specs:
        ent = _find_feedback(feedback_entries, hints) or _find_feedback(parsed.palette, hints)
        if ent:
            record(tok, ent.hex, ent.name, ent.section, f"matched hint {hints} in source")
            muted = _muted_variant(ent.hex, mode)
            record(tok + "Muted", muted, "<derived>", "<oklch>", f"derived L+C reduction from {tok}")
        else:
            # Fallback: industry-standard default. Flagged in rationale so user can override.
            record(tok, default_hex, "<default>", "<no source match>",
                   f"no feedback color matched {hints} in source; used neutral default ({default_hex}). User should review.")
            muted = _muted_variant(default_hex, mode)
            record(tok + "Muted", muted, "<derived>", "<oklch>", f"derived L+C reduction from default {tok}")

    # ---- USER-INPUT TOKENS (game/badges) — flag, do not fill ----
    for tok in USER_INPUT_TOKENS:
        record(tok, None, "<user-input>", "<user-input>", "Fitio-specific token — no source equivalent in DESIGN.md (game/badge); user must supply.")

    return out, decisions


# ---- Phase 4: derive_dark_mode -----------------------------------------------

def _lflip_token(tok: str, light_hex: str) -> str:
    """L-flip a single token via OKLCH for dark mode."""
    L, C, H = hex_to_oklch(light_hex)
    if tok.startswith("bg") or (tok.startswith("border") and tok != "borderFocus"):
        new_L = max(0.05, min(0.30, 1.0 - L))
    elif tok.startswith("text"):
        new_L = max(0.70, min(0.99, 1.0 - L))
    else:
        new_L = L
    return oklch_to_hex((new_L, C * 0.85, H))


def derive_dark_proposal(
    parsed: ParsedDoc,
    buckets: dict[str, list[PaletteEntry]],
    light_proposal: dict[str, str],
) -> tuple[dict[str, str], list[MappingDecision], bool]:
    """Phase 4: build dark-mode proposal.

    Strategy: try map_to_appcolors with mode='dark' for each token, and only
    keep the result when (a) the source actually had a dark-polarity entry
    and (b) the result differs from light. Otherwise L-flip from the light
    proposal — this avoids "light text on light surface" when the source has
    too few dark-mode entries to fill all 29 slots.

    Returns (proposal, decisions, source_has_explicit_dark).
    """
    has_explicit_dark = (
        any("dark" in (e.name + " " + e.desc).lower() and hex_luminance(e.hex) < 0.30 for e in parsed.palette)
        or detect_native_mode(buckets) == "dark"
    )

    source_dark, source_decisions = map_to_appcolors(parsed, buckets, mode="dark")

    out: dict[str, str] = {}
    decisions: list[MappingDecision] = []

    for tok in APPCOLORS_TOKENS:
        if tok in USER_INPUT_TOKENS:
            decisions.append(MappingDecision(tok, None, "<user-input>", "<user-input>",
                                             "Fitio-specific (game/badge) — user must supply."))
            continue

        # Find this token's source decision
        src_decision = next((d for d in source_decisions if d.token == tok), None)
        light_hex = light_proposal.get(tok)
        src_hex = source_dark.get(tok)

        # Polarity check: for dark mode, surfaces must be dark; text must be light.
        polarity_ok = True
        if src_hex:
            lum = hex_luminance(src_hex)
            if tok.startswith("bg") and lum > 0.40:
                polarity_ok = False
            if tok.startswith("text") and tok != "textOnBrand" and lum < 0.45:
                polarity_ok = False

        if src_hex and polarity_ok and src_decision and src_decision.source_name not in ("<missing>", "<derived>"):
            # Source-mapped value with correct polarity — keep it.
            out[tok] = src_hex
            decisions.append(MappingDecision(
                tok, src_hex,
                src_decision.source_name, src_decision.source_section,
                "source has explicit dark-polarity entry: " + src_decision.reason,
            ))
        elif light_hex:
            flipped = _lflip_token(tok, light_hex)
            decisions.append(MappingDecision(
                tok, flipped, "<L-flip>", "<derived>",
                f"derived from light {light_hex} via OKLCH L-flip" + ("" if not has_explicit_dark else " (source dark-polarity entry was ambiguous or missing for this slot)"),
            ))
            out[tok] = flipped
        else:
            decisions.append(MappingDecision(tok, None, "<missing>", "<missing>", "light proposal also missing — cannot derive"))

    return out, decisions, has_explicit_dark


# ---- Phase 5: validate_wcag --------------------------------------------------

@dataclass
class WCAGRow:
    pair: str
    fg: str
    bg: str
    fg_hex: str
    bg_hex: str
    ratio: float
    required: float
    pass_: bool


def validate_wcag(proposal: dict[str, str]) -> list[WCAGRow]:
    rows: list[WCAGRow] = []
    seen: set[tuple[str, str]] = set()
    for fg, bg, req, label in WCAG_PAIRS:
        if (fg, bg) in seen:
            continue
        seen.add((fg, bg))
        if fg not in proposal or bg not in proposal:
            continue
        fg_hex = proposal[fg]
        bg_hex = proposal[bg]
        ratio = round(contrast_ratio(fg_hex, bg_hex), 2)
        rows.append(WCAGRow(label, fg, bg, fg_hex, bg_hex, ratio, req, ratio >= req))
    return rows


# ---- Phase 6: write_artifacts ------------------------------------------------

RATIONALE_TEMPLATE = """# Rationale: AppColors proposal from `{slug}`

> Generated by `scripts/design_md_to_appcolors.py` on {date}.
> Source: `{source_path}` (Category: {category})

## 1. Source citation

**Title:** {title}

**Visual theme paragraph (verbatim from source §1):**

{visual_theme}

## 2. Token mapping table

Mode: **light** ({n_light_explicit}/29 mapped from source · {n_light_derived}/29 derived · {n_light_user}/29 awaiting user input)

| Token | Hex | Source | Section | Reason |
|---|---|---|---|---|
{light_table}

Mode: **dark** ({mode_origin})

| Token | Hex | Source | Section | Reason |
|---|---|---|---|---|
{dark_table}

## 3. WCAG report

Light mode ({light_pass}/{light_total} pairs ≥ AA threshold):

| Pair | fg ({{fg_token}}) | bg ({{bg_token}}) | Ratio | Required | Pass |
|---|---|---|---|---|---|
{wcag_light_table}

Dark mode ({dark_pass}/{dark_total} pairs ≥ AA threshold):

| Pair | fg ({{fg_token}}) | bg ({{bg_token}}) | Ratio | Required | Pass |
|---|---|---|---|---|---|
{wcag_dark_table}

{wcag_failures_block}

## 4. Open questions for user

The translator picked these via heuristics — confirm or override:

- **brandMuted**: derived from `brandDefault` via OKLCH unless source had a second brand entry. If your sub-brand needs a deliberate hue shift (warmer/cooler), edit before pasting.
- **bgInput**: aliased to `bgSurface` when the source has fewer than 3 surface tiers. Decide whether inputs should sit deeper than cards or match them.
- **borderFocus**: defaults to `brandDefault` when no explicit focus/ring entry exists in source. Some brands intentionally use a contrasting accent (e.g. blue-on-warm) for accessibility.

## 5. Fitio-specific tokens needing input

These have no DESIGN.md equivalent and are flagged in the proposal:

- `gameAccent` — primary game-state highlight (e.g. active turn marker)
- `gameAccentMuted` — disabled/idle state of the same
- `gameAccentOnColor` — text on `gameAccent` surface
- `badgeNew` · `badgeAlert` · `badgeReward` · `badgeOnline` — status pip colors

Suggest: pull from `feedbackInfo`/`feedbackSuccess` if you don't want a unique game palette, OR commission a 4-color sub-system from the brand entry.

## 6. Apply

When approved, paste into `lib/theme/app_colors.dart` per project convention. Re-run `python3 scripts/check_contrast.py --theme` to confirm.
"""


def _format_mapping_row(decisions: list[MappingDecision], proposal: dict[str, str]) -> str:
    rows = []
    for d in decisions:
        if d.token not in APPCOLORS_TOKENS:
            continue
        hexv = proposal.get(d.token) or "_(missing)_"
        rows.append(f"| `{d.token}` | `{hexv}` | {d.source_name} | {d.source_section} | {d.reason} |")
    return "\n".join(rows)


def _format_wcag_table(rows: list[WCAGRow]) -> str:
    return "\n".join(
        f"| {r.pair} | `{r.fg}` (`{r.fg_hex}`) | `{r.bg}` (`{r.bg_hex}`) | {r.ratio} | {r.required} | {'✅' if r.pass_ else '❌'} |"
        for r in rows
    )


def _format_failures(label: str, rows: list[WCAGRow]) -> str:
    fails = [r for r in rows if not r.pass_]
    if not fails:
        return ""
    lines = [f"### {label} failures (must address before shipping)"]
    for r in fails:
        lines.append(f"- `{r.fg}` on `{r.bg}` is {r.ratio}, needs {r.required}. Suggest: darken `{r.fg}` or lighten `{r.bg}` until pair clears.")
    return "\n".join(lines)


def write_artifacts(
    parsed: ParsedDoc,
    light_proposal: dict[str, str],
    dark_proposal: dict[str, str],
    light_decisions: list[MappingDecision],
    dark_decisions: list[MappingDecision],
    wcag_light: list[WCAGRow],
    wcag_dark: list[WCAGRow],
    dark_from_source: bool,
    out_dir: Path,
    source_path: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # proposal.json
    payload = {
        "metadata": {
            "slug": parsed.slug,
            "title": parsed.title,
            "category": parsed.category,
            "source_path": str(source_path),
            "dark_mode_origin": "source-explicit" if dark_from_source else "derived (L-flip)",
            "tokens_count": 29,
        },
        "tokens": {
            "light": {tok: light_proposal.get(tok) for tok in APPCOLORS_TOKENS},
            "dark":  {tok: dark_proposal.get(tok)  for tok in APPCOLORS_TOKENS},
        },
        "wcag": {
            "light": [asdict(r) for r in wcag_light],
            "dark":  [asdict(r) for r in wcag_dark],
        },
        "decisions": {
            "light": [asdict(d) for d in light_decisions],
            "dark":  [asdict(d) for d in dark_decisions],
        },
    }
    (out_dir / "proposal.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # rationale.md
    from datetime import date
    n_light_explicit = sum(1 for d in light_decisions if d.source_name not in ("<derived>", "<missing>", "<user-input>", "<L-flip>"))
    n_light_derived  = sum(1 for d in light_decisions if d.source_name in ("<derived>", "<L-flip>"))
    n_light_user     = sum(1 for d in light_decisions if d.source_name == "<user-input>")
    body = RATIONALE_TEMPLATE.format(
        slug=parsed.slug,
        date=date.today().isoformat(),
        source_path=source_path,
        category=parsed.category,
        title=parsed.title or parsed.slug,
        visual_theme=parsed.visual_theme.replace("\n\n", "\n\n").strip() or "_(no visual theme paragraph found)_",
        n_light_explicit=n_light_explicit,
        n_light_derived=n_light_derived,
        n_light_user=n_light_user,
        light_table=_format_mapping_row(light_decisions, light_proposal),
        mode_origin="explicit hex from source" if dark_from_source else "derived from light proposal via OKLCH L-flip",
        dark_table=_format_mapping_row(dark_decisions, dark_proposal),
        light_pass=sum(1 for r in wcag_light if r.pass_),
        light_total=len(wcag_light),
        dark_pass=sum(1 for r in wcag_dark if r.pass_),
        dark_total=len(wcag_dark),
        wcag_light_table=_format_wcag_table(wcag_light),
        wcag_dark_table=_format_wcag_table(wcag_dark),
        wcag_failures_block="\n\n".join(filter(None, [
            _format_failures("Light mode", wcag_light),
            _format_failures("Dark mode", wcag_dark),
        ])),
    )
    (out_dir / "rationale.md").write_text(body, encoding="utf-8")


# ---- Driver ------------------------------------------------------------------

def _lflip_proposal(native_proposal: dict[str, str], from_mode: str) -> tuple[dict[str, str], list[MappingDecision]]:
    """Derive a full proposal from the native one by per-token OKLCH L-flip."""
    out: dict[str, str] = {}
    decisions: list[MappingDecision] = []
    for tok in APPCOLORS_TOKENS:
        if tok in USER_INPUT_TOKENS:
            decisions.append(MappingDecision(tok, None, "<user-input>", "<user-input>",
                                             "Fitio-specific (game/badge) — user must supply."))
            continue
        src = native_proposal.get(tok)
        if not src:
            decisions.append(MappingDecision(tok, None, "<missing>", "<missing>", "native proposal also missing"))
            continue
        L, C, H = hex_to_oklch(src)
        if tok.startswith("bg") or (tok.startswith("border") and tok != "borderFocus"):
            new_L = max(0.05, min(0.30, 1.0 - L)) if from_mode == "light" else max(0.92, min(1.00, 1.0 - L))
        elif tok.startswith("text"):
            new_L = max(0.70, min(0.99, 1.0 - L)) if from_mode == "light" else max(0.05, min(0.30, 1.0 - L))
        else:
            new_L = L
        out[tok] = oklch_to_hex((new_L, C * 0.85, H))
        decisions.append(MappingDecision(tok, out[tok], "<L-flip>", "<derived>",
                                         f"derived from {from_mode} {src} via OKLCH L-flip"))
    return out, decisions


def run_one(source: Path, out_dir: Path, dry_run: bool = False) -> int:
    if not source.exists():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        return 2

    if dry_run:
        print(f"[dry-run] phase 1 parse → {source}")
    parsed = parse_design_md(source)
    if dry_run:
        print(f"[dry-run] parsed {len(parsed.palette)} palette entries across {len(set(e.section for e in parsed.palette))} sections")

    if dry_run:
        print(f"[dry-run] phase 2 bucketize")
    buckets = bucketize(parsed.palette)
    if dry_run:
        for k, v in buckets.items():
            if v:
                print(f"  {k}: {len(v)} entries")

    native = detect_native_mode(buckets)
    if dry_run:
        print(f"[dry-run] phase 3 map (native={native})")

    # 1. Build the native proposal from source.
    native_proposal, native_decisions = map_to_appcolors(parsed, buckets, mode=native)

    # 2. The other mode: try source first (for light-native sources that have explicit dark hexes),
    #    fall back to L-flip when that produces a wrong-polarity result.
    other = "dark" if native == "light" else "light"
    if dry_run:
        print(f"[dry-run] phase 4 derive {other}")
    if native == "light":
        # Existing source-then-flip strategy (covers e.g. Claude with "Dark Surface" entries).
        other_proposal, other_decisions, has_explicit = derive_dark_proposal(parsed, buckets, native_proposal)
        dark_from_source = has_explicit
    else:
        # Dark-native source: skip source mapping for light (would just return the same dark hexes).
        # L-flip from the dark native proposal.
        other_proposal, other_decisions = _lflip_proposal(native_proposal, from_mode="dark")
        dark_from_source = True  # the dark side IS the source

    if native == "light":
        light_proposal, light_decisions = native_proposal, native_decisions
        dark_proposal, dark_decisions = other_proposal, other_decisions
    else:
        dark_proposal, dark_decisions = native_proposal, native_decisions
        light_proposal, light_decisions = other_proposal, other_decisions

    if dry_run:
        print(f"[dry-run] phase 5 wcag")
    wcag_light = validate_wcag(light_proposal)
    wcag_dark = validate_wcag(dark_proposal)

    if dry_run:
        print(f"[dry-run] phase 6 write skipped")
        print(f"[dry-run] light tokens populated: {len(light_proposal)}/29; dark: {len(dark_proposal)}/29")
        print(f"[dry-run] light wcag pass: {sum(1 for r in wcag_light if r.pass_)}/{len(wcag_light)}; dark: {sum(1 for r in wcag_dark if r.pass_)}/{len(wcag_dark)}")
        return 0

    write_artifacts(
        parsed, light_proposal, dark_proposal,
        light_decisions, dark_decisions,
        wcag_light, wcag_dark, dark_from_source,
        out_dir, source,
    )
    print(f"OK  {parsed.slug}: light={len(light_proposal)}/29 dark={len(dark_proposal)}/29 wcagL={sum(1 for r in wcag_light if r.pass_)}/{len(wcag_light)} wcagD={sum(1 for r in wcag_dark if r.pass_)}/{len(wcag_dark)} → {out_dir} (native={native})")
    return 0


def run_validate_all() -> int:
    base = REPO_ROOT / "design-systems"
    failures = 0
    total = 0
    for d in sorted(base.iterdir()):
        if not d.is_dir():
            continue
        src = d / "DESIGN.md"
        if not src.exists():
            continue
        total += 1
        out = REPO_ROOT / ".tmp" / "translator-validate-all" / d.name
        rc = run_one(src, out, dry_run=False)
        if rc != 0:
            failures += 1
    print(f"\nvalidate-all: {total - failures}/{total} OK")
    return 0 if failures == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", help="Path to design-systems/<slug>/DESIGN.md")
    ap.add_argument("--out-dir", default=None, help="Output directory (default: .tmp/translator/<slug>/)")
    ap.add_argument("--validate-all", action="store_true", help="Run translator across all 20 forks")
    ap.add_argument("--dry-run", action="store_true", help="Phase trace without writing artifacts")
    args = ap.parse_args()

    if args.validate_all:
        return run_validate_all()

    if not args.source:
        ap.error("source path required (or use --validate-all)")

    src = Path(args.source).resolve()
    out = Path(args.out_dir).resolve() if args.out_dir else (REPO_ROOT / ".tmp" / "translator" / src.parent.name)
    return run_one(src, out, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
