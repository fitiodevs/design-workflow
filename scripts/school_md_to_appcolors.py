#!/usr/bin/env python3
"""
Translate a `design-systems-schools/<slug>/SCHOOL.md` into a Fitio AppColors proposal.

Constraint-based — schools encode constraints (`accent ≤10% pixels`, `WCAG ≥7:1`,
`single saturated hue`, `dark-mode-default`) rather than literal hex codes. The
translator parses those constraints and synthesizes a 29-token `AppColors`
proposal that satisfies them; OKLCH math drives the synthesis, `check_contrast.py`
validates WCAG.

Outputs (per slug, into --out-dir):
    proposal.json   29 tokens × 2 modes (light + dark) + WCAG report + decision trace
    rationale.md    Source citation, philosophy quote, constraint extraction, mapping table

Usage:
    python3 scripts/school_md_to_appcolors.py design-systems-schools/muller-brockmann/
    python3 scripts/school_md_to_appcolors.py design-systems-schools/brutalism/ --out-dir /tmp/out
    python3 scripts/school_md_to_appcolors.py --validate-all
    python3 scripts/school_md_to_appcolors.py design-systems-schools/memphis/ --dry-run

Phases (per design D-D in design-school-library/design.md):
    1. parse_school_md       Split into 8 sections; capture philosophy nucleus + token-implications.
    2. extract_constraints   Parse token-implications bullets into Constraint objects.
    3. synthesize_palette    OKLCH-iterate values within constraint bounds; bind to 29 tokens.
    4. validate_wcag         12 mandatory pairs × 2 modes; failures repaired via re-iteration.
    5. write_artifacts       proposal.json + rationale.md.

Reuses:
    scripts/check_contrast.contrast_ratio
    scripts/oklch_to_hex.hex_to_oklch / oklch_to_hex
    scripts/design_md_to_appcolors.APPCOLORS_TOKENS / WCAG_PAIRS / USER_INPUT_TOKENS
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

# Reuse the 29-token list and WCAG pairs from the v1.3.0 brand translator.
from design_md_to_appcolors import APPCOLORS_TOKENS, WCAG_PAIRS, USER_INPUT_TOKENS  # noqa: E402


# ---- Phase 1: parse_school_md -----------------------------------------------

@dataclass
class ParsedSchool:
    slug: str
    title: str
    category: str
    philosophy: str
    characteristics: list[str] = field(default_factory=list)
    prompt_dna: str = ""
    token_implications: list[str] = field(default_factory=list)
    matrix: list[tuple[str, str, str]] = field(default_factory=list)  # (scenario, rating, recommendation)
    slop_traps: list[str] = field(default_factory=list)


H1_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$")
H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
CATEGORY_RE = re.compile(r"^>\s*Category:\s*(?P<cat>.+?)\s*$")
BULLET_RE = re.compile(r"^[-*]\s+(?P<body>.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\|\s*(?P<scenario>[^|]+?)\s*\|\s*(?P<rating>[★☆]+)\s*\|\s*(?P<rec>.+?)\s*\|\s*$")


def parse_school_md(path: Path) -> ParsedSchool:
    slug = path.parent.name if path.is_file() else path.name
    if path.is_dir():
        path = path / "SCHOOL.md"
    text = path.read_text(encoding="utf-8")

    title = ""
    category = "Uncategorized"
    section: Optional[str] = None
    section_lines: dict[str, list[str]] = {}

    for line in text.splitlines():
        if not title:
            m = H1_RE.match(line)
            if m:
                title = m.group("title").strip()
                continue
        m = CATEGORY_RE.match(line)
        if m:
            category = m.group("cat").strip()
            continue
        m = H2_RE.match(line)
        if m:
            section = m.group("title").strip()
            section_lines.setdefault(section, [])
            continue
        if section:
            section_lines.setdefault(section, []).append(line)

    def get(name_substr: str) -> list[str]:
        for k, v in section_lines.items():
            if name_substr.lower() in k.lower():
                return v
        return []

    philosophy = "\n".join(l for l in get("Philosophy nucleus") if l.strip()).strip()
    prompt_dna = "\n".join(l for l in get("Prompt DNA") if l.strip()).strip()

    chars = [BULLET_RE.match(l).group("body").strip() for l in get("Core characteristics") if BULLET_RE.match(l)]
    tok_impl = [BULLET_RE.match(l).group("body").strip() for l in get("Token implications") if BULLET_RE.match(l)]
    slop = [BULLET_RE.match(l).group("body").strip() for l in get("Slop traps") if BULLET_RE.match(l)]

    matrix: list[tuple[str, str, str]] = []
    for line in get("Execution-path matrix"):
        m = TABLE_ROW_RE.match(line)
        if m and m.group("scenario") not in ("Scenario", "---"):
            matrix.append((m.group("scenario").strip(), m.group("rating").strip(), m.group("rec").strip()))

    return ParsedSchool(
        slug=slug, title=title, category=category, philosophy=philosophy,
        characteristics=chars, prompt_dna=prompt_dna,
        token_implications=tok_impl, matrix=matrix, slop_traps=slop,
    )


# ---- Phase 2: extract_constraints -------------------------------------------

@dataclass
class Constraint:
    target: str        # e.g. "brandDefault", "bgBase", "*" (global)
    kind: str          # "saturation_min", "saturation_max", "lightness_max",
                       # "lightness_min", "hue_in", "wcag_min", "polarity",
                       # "is_value", "scale", "weight_count"
    value: object      # constraint-specific
    raw: str           # the original bullet for traceability


HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")
TOKEN_HINT_RE = re.compile(r"`([a-zA-Z]+)`")


# Keyword → constraint generator. Each maps a phrase in token-implications
# bullets into a structured Constraint. Order matters (more specific first).
def extract_constraints(parsed: ParsedSchool) -> list[Constraint]:
    constraints: list[Constraint] = []
    body_blob = "\n".join(parsed.token_implications + [parsed.prompt_dna])
    body_low = body_blob.lower()

    # 1. Hex codes mentioned in token-implications, paired with each token name in
    #    that bullet by *adjacency*. Bullets often mention multiple tokens with
    #    multiple hex values (e.g. "`brandDefault` = the accent; `bgBase` = `#fafaf7`").
    #    Walk the bullet token-by-token, assigning each `tokenName` the nearest
    #    following hex (within ~80 chars), if any.
    # Tight pattern: `tokenName` followed by `=` or `:` then `#hex` within 25 chars.
    # Matches `brandDefault = #c96442` or `bgBase: #fafaf7` but not `brandDefault = the accent. ... bgBase = #fafaf7`.
    TOKEN_FOLLOWING_HEX = re.compile(
        r"`(?P<token>[a-zA-Z]+)`\s*[=:]?\s*[^,;`]{0,25}?#(?P<hex>[0-9a-fA-F]{6,8})\b"
    )
    HEX_PRECEDING_TOKEN = re.compile(
        r"#(?P<hex>[0-9a-fA-F]{6,8})\b[^|]{0,15}?`(?P<token>[a-zA-Z]+)`"
    )
    for bullet in parsed.token_implications:
        seen_pairs: set[tuple[str, str]] = set()
        # Forward pass: `token` ... `#hex`
        for m in TOKEN_FOLLOWING_HEX.finditer(bullet):
            token = m.group("token")
            if token in APPCOLORS_TOKENS:
                hex_val = f"#{m.group('hex')[:6].lower()}"
                if (token, hex_val) in seen_pairs:
                    continue
                seen_pairs.add((token, hex_val))
                constraints.append(Constraint(
                    target=token, kind="suggested_hex", value=hex_val, raw=bullet,
                ))
        # Backward pass disabled — too noisy when hex literals appear in
        # parenthetical descriptions before token names ("(`#0a0a0a`). `brandDefault` =").
        # Schools that need the backward direction can use the forward `token = #hex` form.

    # 2. Polarity — does the school live in dark or light mode?
    if any(k in body_low for k in ("dark-native", "dark-mode-default", "lives in dark", "dark canvas (`#0a0a0a`", "dark canvas (`#000000`", "bgbase` = `#000000`")):
        constraints.append(Constraint("bgBase", "polarity", "dark", "polarity:dark inferred"))
    elif any(k in body_low for k in ("paper-cream", "warm-near-white surface", "off-white", "paper canvas", "paper-toned")):
        constraints.append(Constraint("bgBase", "polarity", "light", "polarity:light inferred"))

    # 3. Saturation discipline.
    if any(k in body_low for k in ("100% saturation", "full saturation", "fully saturated", "saturated primary", "100 saturation", "at full saturation")):
        constraints.append(Constraint("brandDefault", "saturation_min", 0.6, "saturation:high"))
    if any(k in body_low for k in ("calm saturation", "muted", "restrained", "dirty", "desaturated", "historic pigment")):
        constraints.append(Constraint("brandDefault", "saturation_max", 0.55, "saturation:calm"))

    # 4. Multiple-accent / single-accent constraint.
    if any(k in body_low for k in ("one accent", "1 accent", "single accent", "1 saturated", "one signature", "1 signature", "1 chromatic", "one chromatic")):
        constraints.append(Constraint("*", "single_accent", True, "accent:single"))
    if any(k in body_low for k in ("4–6 saturated", "4-6 saturated", "1–2 hero", "two saturated", "1-2 saturated")):
        constraints.append(Constraint("*", "single_accent", False, "accent:multiple"))

    # 5. WCAG threshold.
    m = re.search(r"contrast\s*≥\s*(\d+(?:\.\d+)?)", body_low)
    if m:
        constraints.append(Constraint("textPrimary", "wcag_min", float(m.group(1)), f"wcag-min:{m.group(1)} from school"))
    if "wcag" in body_low and "7:1" in body_low:
        constraints.append(Constraint("textPrimary", "wcag_min", 7.0, "wcag-min:7 explicit"))

    # 6. Reduction (no decoration) — affects radius and motion.
    if any(k in body_low for k in ("no rounded corners", "rounded corners ≤4px", "radius.sm = 0", "0px on everything", "sharp corners")):
        constraints.append(Constraint("*", "radius_max", 4, "radius:minimal"))
    if any(k in body_low for k in ("no motion", "no transitions", "no animations", "motion is discouraged", "motion: discouraged", "transition: none everywhere")):
        constraints.append(Constraint("*", "motion_disabled", True, "motion:none"))

    return constraints


# ---- Phase 3: synthesize_palette --------------------------------------------

# Industry-standard fallbacks per role — used when the school doesn't pin a hex.
# These are *seeds* for the OKLCH iterator; the iterator may shift L to satisfy
# WCAG against bgBase/bgSurface.
DEFAULT_LIGHT_SEEDS = {
    "brandDefault":         "#1f4cdc",
    "brandMuted":           "#9eb3f0",
    "brandOnColor":         "#ffffff",
    "bgBase":               "#fafaf6",
    "bgSurface":            "#fafaf6",
    "bgSurfaceRaised":      "#ffffff",
    "bgInput":              "#f4f4ee",
    "textPrimary":          "#0a0a0a",
    "textSecondary":        "#4a4a47",
    "textMuted":            "#7a7a76",
    "textOnBrand":          "#ffffff",
    "borderDefault":        "#d9d8d2",
    "borderStrong":         "#9a9994",
    "borderFocus":          "#1f4cdc",
    "feedbackSuccess":      "#16a34a",
    "feedbackSuccessMuted": "#dcfce7",
    "feedbackWarning":      "#d97706",
    "feedbackWarningMuted": "#fef3c7",
    "feedbackError":        "#dc2626",
    "feedbackErrorMuted":   "#fee2e2",
    "feedbackInfo":         "#2563eb",
    "feedbackInfoMuted":    "#dbeafe",
    "gameAccent":           None,
    "gameAccentMuted":      None,
    "gameAccentOnColor":    None,
    "badgeNew":             None,
    "badgeAlert":           None,
    "badgeReward":          None,
    "badgeOnline":          None,
}

DEFAULT_DARK_SEEDS = {
    "brandDefault":         "#5e7afc",
    "brandMuted":           "#2a3a78",
    "brandOnColor":         "#ffffff",
    "bgBase":               "#0a0a0a",
    "bgSurface":            "#141413",
    "bgSurfaceRaised":      "#1d1d1c",
    "bgInput":              "#171716",
    "textPrimary":          "#f5f4ed",
    "textSecondary":        "#a3a29c",
    "textMuted":            "#6e6d68",
    "textOnBrand":          "#ffffff",
    "borderDefault":        "#34332f",
    "borderStrong":         "#5c5b56",
    "borderFocus":          "#5e7afc",
    "feedbackSuccess":      "#22c55e",
    "feedbackSuccessMuted": "#1f3a25",
    "feedbackWarning":      "#f59e0b",
    "feedbackWarningMuted": "#3a2e1f",
    "feedbackError":        "#ef4444",
    "feedbackErrorMuted":   "#3a1f1f",
    "feedbackInfo":         "#3b82f6",
    "feedbackInfoMuted":    "#1f2a3a",
    "gameAccent":           None,
    "gameAccentMuted":      None,
    "gameAccentOnColor":    None,
    "badgeNew":             None,
    "badgeAlert":           None,
    "badgeReward":          None,
    "badgeOnline":          None,
}


@dataclass
class TokenDecision:
    token: str
    chosen_hex: Optional[str]
    seed_hex: Optional[str]
    constraints_applied: list[str] = field(default_factory=list)
    iterations: int = 0
    final_wcag_pair: Optional[float] = None


def _shift_lightness(hex_color: str, target_L: float) -> str:
    L, C, H = hex_to_oklch(hex_color)
    return oklch_to_hex((target_L, C, H))


def _shift_chroma(hex_color: str, target_C: float) -> str:
    L, C, H = hex_to_oklch(hex_color)
    return oklch_to_hex((L, max(0.0, target_C), H))


def synthesize_palette(parsed: ParsedSchool, constraints: list[Constraint]) -> tuple[dict[str, Optional[str]], dict[str, Optional[str]], list[TokenDecision]]:
    # Detect mode polarity from constraints.
    polarity = "light"
    for c in constraints:
        if c.kind == "polarity":
            polarity = str(c.value)
            break

    # Pick seed map by polarity.
    seeds_native = dict(DEFAULT_DARK_SEEDS) if polarity == "dark" else dict(DEFAULT_LIGHT_SEEDS)
    seeds_other  = dict(DEFAULT_LIGHT_SEEDS) if polarity == "dark" else dict(DEFAULT_DARK_SEEDS)

    # Apply explicit suggested_hex constraints — these override seeds.
    for c in constraints:
        if c.kind == "suggested_hex" and c.target in seeds_native:
            seeds_native[c.target] = str(c.value)

    # Apply saturation constraints to brandDefault.
    sat_min = sat_max = None
    for c in constraints:
        if c.kind == "saturation_min" and c.target == "brandDefault":
            sat_min = float(c.value)
        if c.kind == "saturation_max" and c.target == "brandDefault":
            sat_max = float(c.value)
    if seeds_native.get("brandDefault") and (sat_min or sat_max):
        L, C, H = hex_to_oklch(seeds_native["brandDefault"])
        if sat_min is not None and C < sat_min * 0.4:  # OKLCH chroma maxes ~0.4 for srgb gamut
            C = sat_min * 0.4
        if sat_max is not None and C > sat_max * 0.4:
            C = sat_max * 0.4
        seeds_native["brandDefault"] = oklch_to_hex((L, C, H))

    # WCAG threshold.
    wcag_threshold = 4.5
    for c in constraints:
        if c.kind == "wcag_min":
            wcag_threshold = max(wcag_threshold, float(c.value))

    decisions: list[TokenDecision] = []

    def synth_one(token: str, seeds: dict[str, Optional[str]], bg_for_text: Optional[str], is_light: bool) -> tuple[Optional[str], TokenDecision]:
        seed = seeds.get(token)
        if token in USER_INPUT_TOKENS:
            return None, TokenDecision(token, None, None, ["user-input flagged"], 0, None)
        if seed is None:
            return None, TokenDecision(token, None, None, ["no seed available"], 0, None)

        applied = []
        chosen = seed
        # Apply explicit hex from constraints (override).
        for c in constraints:
            if c.kind == "suggested_hex" and c.target == token:
                chosen = str(c.value)
                applied.append(f"explicit-hex from school ({c.raw[:60]}…)")

        # WCAG repair loop for text-on-bg pairs.
        iters = 0
        final_wcag = None
        if token.startswith("text") and bg_for_text:
            ratio = contrast_ratio(chosen, bg_for_text)
            final_wcag = round(ratio, 2)
            while ratio < wcag_threshold and iters < 5:
                iters += 1
                L, C, H = hex_to_oklch(chosen)
                if is_light:
                    L = max(0.0, L - 0.08)  # darken text on light bg
                else:
                    L = min(1.0, L + 0.08)  # lighten text on dark bg
                chosen = oklch_to_hex((L, C, H))
                ratio = contrast_ratio(chosen, bg_for_text)
                applied.append(f"wcag-repair iter {iters}: ratio={ratio:.2f}")
            final_wcag = round(ratio, 2)
            if ratio < wcag_threshold:
                applied.append(f"DID NOT CONVERGE — final ratio {ratio:.2f} < {wcag_threshold}")

        return chosen, TokenDecision(token, chosen, seed, applied, iters, final_wcag)

    native_proposal: dict[str, Optional[str]] = {}
    bg_native = seeds_native.get("bgBase")
    is_light_native = polarity == "light"
    for tok in APPCOLORS_TOKENS:
        bg_for_text = seeds_native.get("bgBase") if tok in ("textPrimary", "textSecondary", "textMuted") else None
        chosen, dec = synth_one(tok, seeds_native, bg_for_text, is_light_native)
        native_proposal[tok] = chosen
        decisions.append(dec)

    # Other-mode proposal — derive surfaces by polarity-flip seeds, keep brand stable.
    if "brandDefault" in native_proposal and native_proposal["brandDefault"]:
        seeds_other["brandDefault"] = native_proposal["brandDefault"]  # brand persists across modes
    other_proposal: dict[str, Optional[str]] = {}
    is_light_other = not is_light_native
    for tok in APPCOLORS_TOKENS:
        bg_for_text = seeds_other.get("bgBase") if tok in ("textPrimary", "textSecondary", "textMuted") else None
        chosen, _dec = synth_one(tok, seeds_other, bg_for_text, is_light_other)
        other_proposal[tok] = chosen

    # Slot light/dark in the canonical positions.
    if polarity == "light":
        return native_proposal, other_proposal, decisions
    return other_proposal, native_proposal, decisions


# ---- Phase 4: validate_wcag (reuses brand translator's WCAG_PAIRS) ----------

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


def validate_wcag(proposal: dict[str, Optional[str]]) -> list[WCAGRow]:
    rows: list[WCAGRow] = []
    seen: set[tuple[str, str]] = set()
    for fg, bg, req, label in WCAG_PAIRS:
        if (fg, bg) in seen:
            continue
        seen.add((fg, bg))
        if not proposal.get(fg) or not proposal.get(bg):
            continue
        ratio = round(contrast_ratio(proposal[fg], proposal[bg]), 2)
        rows.append(WCAGRow(label, fg, bg, proposal[fg], proposal[bg], ratio, req, ratio >= req))
    return rows


# ---- Phase 5: write_artifacts -----------------------------------------------

RATIONALE_TEMPLATE = """# Rationale: AppColors proposal from school `{slug}`

> Generated by `scripts/school_md_to_appcolors.py` on {date}.
> Source school: `{source_path}` (Category: {category})
> Synthesis: constraint-based — schools encode constraints; the translator solves for them.

## 1. Philosophy

> {philosophy}

## 2. Extracted constraints ({n_constraints})

{constraint_table}

## 3. Synthesized palette

Mode: **light** ({n_light_explicit}/29 from explicit school hex · {n_light_derived}/29 from constraint-driven seed)

| Token | Hex | Source / iterations | Rationale |
|---|---|---|---|
{light_table}

Mode: **dark** (derived; brand persists across modes per school convention)

| Token | Hex | Source / iterations | Rationale |
|---|---|---|---|
{dark_table}

## 4. WCAG report

Light mode ({light_pass}/{light_total} pairs ≥ school threshold of {wcag_threshold}):

| Pair | fg ({{fg_token}}) | bg ({{bg_token}}) | Ratio | Required | Pass |
|---|---|---|---|---|---|
{wcag_light_table}

Dark mode ({dark_pass}/{dark_total} pairs ≥ school threshold):

| Pair | fg ({{fg_token}}) | bg ({{bg_token}}) | Ratio | Required | Pass |
|---|---|---|---|---|---|
{wcag_dark_table}

{wcag_failures_block}

## 5. Open questions for user

The translator picked these via constraint synthesis — confirm or override:

- **brandDefault** matches the school's character (saturation, hue family). If the project's brand is opinionated otherwise, override.
- **bgBase polarity** ({polarity_inferred}) was inferred from the school's prompt DNA. If the project requires the opposite polarity as default, swap modes.
- **WCAG threshold** ({wcag_threshold}) was inferred from the school's reduction discipline. Some schools (Brutalism, Müller-Brockmann) demand AAA; others (Pentagram, Editorial) accept AA.

## 6. Fitio-specific tokens needing input

These are not constrained by any school's vocabulary and remain user-input:

- `gameAccent` · `gameAccentMuted` · `gameAccentOnColor` — game-state highlights
- `badgeNew` · `badgeAlert` · `badgeReward` · `badgeOnline` — status pip colors

Common pairings: pull `gameAccent` from the school's secondary brand if present (Memphis), or from `feedbackInfo` if the school is single-accent (Müller-Brockmann), or from a lower-saturation derivation of `brandDefault`.

## 7. Apply

When approved, paste the AppColors snippet into `lib/theme/app_colors.dart` per project convention. Re-run `python3 scripts/check_contrast.py --theme` to confirm.
"""


def _format_constraint_table(constraints: list[Constraint]) -> str:
    if not constraints:
        return "_(no parseable constraints — using neutral defaults)_"
    rows = ["| Target | Kind | Value | Source bullet |", "|---|---|---|---|"]
    for c in constraints:
        raw_short = c.raw if len(c.raw) <= 80 else c.raw[:77] + "…"
        rows.append(f"| `{c.target}` | `{c.kind}` | `{c.value}` | {raw_short} |")
    return "\n".join(rows)


def _format_decisions(decisions: list[TokenDecision], proposal: dict[str, Optional[str]]) -> str:
    rows = []
    for d in decisions:
        if d.token not in APPCOLORS_TOKENS:
            continue
        hexv = proposal.get(d.token) or "_(missing)_"
        applied = "; ".join(d.constraints_applied) if d.constraints_applied else "(seed default)"
        rows.append(f"| `{d.token}` | `{hexv}` | iters={d.iterations} | {applied} |")
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
        lines.append(f"- `{r.fg}` on `{r.bg}` is {r.ratio}, needs {r.required}.")
    return "\n".join(lines)


def write_artifacts(
    parsed: ParsedSchool,
    constraints: list[Constraint],
    light_proposal: dict[str, Optional[str]],
    dark_proposal: dict[str, Optional[str]],
    decisions: list[TokenDecision],
    wcag_light: list[WCAGRow],
    wcag_dark: list[WCAGRow],
    out_dir: Path,
    source_path: Path,
    wcag_threshold: float,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    # proposal.json
    payload = {
        "metadata": {
            "slug": parsed.slug,
            "title": parsed.title,
            "category": parsed.category,
            "source_path": str(source_path),
            "polarity": "dark" if any(c.kind == "polarity" and c.value == "dark" for c in constraints) else "light",
            "wcag_threshold": wcag_threshold,
            "tokens_count": 29,
        },
        "philosophy": parsed.philosophy,
        "constraints": [asdict(c) for c in constraints],
        "tokens": {
            "light": {tok: light_proposal.get(tok) for tok in APPCOLORS_TOKENS},
            "dark":  {tok: dark_proposal.get(tok)  for tok in APPCOLORS_TOKENS},
        },
        "wcag": {
            "light": [asdict(r) for r in wcag_light],
            "dark":  [asdict(r) for r in wcag_dark],
        },
        "decisions": [asdict(d) for d in decisions],
    }
    (out_dir / "proposal.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # rationale.md
    from datetime import date
    n_light_explicit = sum(
        1 for d in decisions
        if any("explicit-hex" in c for c in d.constraints_applied)
    )
    n_light_derived = sum(
        1 for d in decisions
        if d.token in APPCOLORS_TOKENS and d.token not in USER_INPUT_TOKENS
        and not any("explicit-hex" in c for c in d.constraints_applied)
    )
    polarity_inferred = next((str(c.value) for c in constraints if c.kind == "polarity"), "light (default)")

    body = RATIONALE_TEMPLATE.format(
        slug=parsed.slug,
        date=date.today().isoformat(),
        source_path=source_path,
        category=parsed.category,
        philosophy=parsed.philosophy.replace("\n\n", "\n\n").strip() or "_(no philosophy nucleus parsed)_",
        n_constraints=len(constraints),
        constraint_table=_format_constraint_table(constraints),
        n_light_explicit=n_light_explicit,
        n_light_derived=n_light_derived,
        light_table=_format_decisions(decisions, light_proposal),
        dark_table=_format_decisions(decisions, dark_proposal),
        wcag_threshold=wcag_threshold,
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
        polarity_inferred=polarity_inferred,
    )
    (out_dir / "rationale.md").write_text(body, encoding="utf-8")


# ---- Driver -----------------------------------------------------------------

def run_one(source: Path, out_dir: Path, dry_run: bool = False) -> int:
    if source.is_dir():
        source = source / "SCHOOL.md"
    if not source.exists():
        print(f"ERROR: source not found: {source}", file=sys.stderr)
        return 2

    if dry_run:
        print(f"[dry-run] phase 1 parse → {source}")
    parsed = parse_school_md(source)
    if dry_run:
        print(f"[dry-run] parsed school={parsed.slug!r} title={parsed.title!r}; "
              f"{len(parsed.token_implications)} token-impl bullets, "
              f"{len(parsed.matrix)} matrix rows, {len(parsed.slop_traps)} slop traps")

    if dry_run:
        print(f"[dry-run] phase 2 extract constraints")
    constraints = extract_constraints(parsed)
    if dry_run:
        print(f"[dry-run] {len(constraints)} constraints extracted")
        for c in constraints[:8]:
            print(f"   - {c.kind}: target={c.target} value={c.value}")

    if dry_run:
        print(f"[dry-run] phase 3 synthesize palette")
    light_proposal, dark_proposal, decisions = synthesize_palette(parsed, constraints)

    wcag_threshold = 4.5
    for c in constraints:
        if c.kind == "wcag_min":
            wcag_threshold = max(wcag_threshold, float(c.value))

    if dry_run:
        print(f"[dry-run] phase 4 wcag")
    wcag_light = validate_wcag(light_proposal)
    wcag_dark  = validate_wcag(dark_proposal)

    if dry_run:
        n_light = len([t for t in light_proposal.values() if t])
        n_dark = len([t for t in dark_proposal.values() if t])
        print(f"[dry-run] light tokens populated: {n_light}/29; dark: {n_dark}/29")
        print(f"[dry-run] light wcag pass: {sum(1 for r in wcag_light if r.pass_)}/{len(wcag_light)}; "
              f"dark: {sum(1 for r in wcag_dark if r.pass_)}/{len(wcag_dark)} (threshold={wcag_threshold})")
        return 0

    write_artifacts(
        parsed, constraints, light_proposal, dark_proposal,
        decisions, wcag_light, wcag_dark, out_dir, source, wcag_threshold,
    )
    n_light = len([t for t in light_proposal.values() if t])
    n_dark = len([t for t in dark_proposal.values() if t])
    print(f"OK  {parsed.slug}: light={n_light}/29 dark={n_dark}/29 "
          f"wcagL={sum(1 for r in wcag_light if r.pass_)}/{len(wcag_light)} "
          f"wcagD={sum(1 for r in wcag_dark if r.pass_)}/{len(wcag_dark)} "
          f"constraints={len(constraints)} → {out_dir}")
    return 0


def run_validate_all() -> int:
    base = REPO_ROOT / "design-systems-schools"
    failures = 0
    total = 0
    for d in sorted(base.iterdir()):
        if not d.is_dir():
            continue
        src = d / "SCHOOL.md"
        if not src.exists():
            continue
        total += 1
        out = REPO_ROOT / ".tmp" / "school-translator-validate-all" / d.name
        rc = run_one(src, out, dry_run=False)
        if rc != 0:
            failures += 1
    print(f"\nvalidate-all: {total - failures}/{total} OK")
    return 0 if failures == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", help="Path to design-systems-schools/<slug>/ or its SCHOOL.md")
    ap.add_argument("--out-dir", default=None, help="Output directory (default: .tmp/school-translator/<slug>/)")
    ap.add_argument("--validate-all", action="store_true", help="Run translator across all 12 schools")
    ap.add_argument("--dry-run", action="store_true", help="Phase trace without writing artifacts")
    args = ap.parse_args()

    if args.validate_all:
        return run_validate_all()
    if not args.source:
        ap.error("source path required (or use --validate-all)")

    src = Path(args.source).resolve()
    out = Path(args.out_dir).resolve() if args.out_dir else (REPO_ROOT / ".tmp" / "school-translator" / (src.name if src.is_dir() else src.parent.name))
    return run_one(src, out, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
