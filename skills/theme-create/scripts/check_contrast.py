#!/usr/bin/env python3
"""
WCAG contrast validator for Fitio semantic tokens.

Usage:
    # Single pair
    python scripts/check_contrast.py #1E272E #FFFFFF [normal|large]

    # All theme pairs (default Fitio semantic combinations, light + dark)
    python scripts/check_contrast.py --theme

    # Specific role on both light and dark
    python scripts/check_contrast.py --role textPrimary-on-surface
"""

import sys
from typing import Tuple, Dict, List


# ---- Color math --------------------------------------------------------------

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.lstrip('#')
    if len(h) == 8:  # strip alpha if present (ARGB → RGB)
        h = h[2:]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def relative_luminance(rgb: Tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        v = c / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1 = relative_luminance(hex_to_rgb(fg))
    l2 = relative_luminance(hex_to_rgb(bg))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def compliance(ratio: float, size: str = "normal") -> Dict[str, bool]:
    if size == "large":
        return {"aa": ratio >= 3.0, "aaa": ratio >= 4.5, "ui": ratio >= 3.0}
    return {"aa": ratio >= 4.5, "aaa": ratio >= 7.0, "ui": ratio >= 3.0}


# ---- Fitio theme registry ----------------------------------------------------
# Fonte canônica: lib/core/theme/app_colors.dart. Mantenha sincronizado.

LIGHT = {
    "brand": "#08179F", "brandMuted": "#E6E9FA", "surface": "#F9FAFB",
    "surfaceVariant": "#F4F4F4", "card": "#FFFFFF", "border": "#E0E0E0",
    "textPrimary": "#1E272E", "textSecondary": "#636363", "textInverted": "#FFFFFF",
    "success": "#22C55E", "warning": "#F59E0B", "danger": "#FF3B30",
    "info": "#3A58FA", "skeleton": "#E9EBEE",
}

DARK = {
    "brand": "#08179F", "brandMuted": "#2A1A5E", "surface": "#121212",
    "surfaceVariant": "#1E1E1E", "card": "#1E1E1E", "border": "#2A3240",
    "textPrimary": "#FFFFFF", "textSecondary": "#B0B0B0", "textInverted": "#1E272E",
    "success": "#22C55E", "warning": "#F59E0B", "danger": "#FF6B60",
    "info": "#6E9BFF", "skeleton": "#2A2F36",
}

# (fg, bg, text_size, purpose)
EXPECTED_PAIRS: List[Tuple[str, str, str, str]] = [
    ("textPrimary", "surface", "normal", "texto corpo sobre scaffold"),
    ("textPrimary", "card", "normal", "texto corpo sobre card"),
    ("textPrimary", "surfaceVariant", "normal", "texto corpo sobre field"),
    ("textSecondary", "surface", "normal", "texto auxiliar sobre scaffold"),
    ("textSecondary", "card", "normal", "texto auxiliar sobre card"),
    ("textInverted", "brand", "normal", "texto de botão primário"),
    ("brand", "surface", "large", "destaque/link em título"),
    ("brand", "card", "large", "destaque em card"),
    ("success", "surface", "normal", "feedback positivo"),
    ("danger", "surface", "normal", "feedback erro"),
    ("warning", "surface", "normal", "alerta"),
    ("info", "surface", "normal", "info neutro"),
]


# ---- Reporters ---------------------------------------------------------------

def fmt_line(fg: str, bg: str, fg_hex: str, bg_hex: str, size: str, purpose: str) -> str:
    ratio = contrast_ratio(fg_hex, bg_hex)
    r = compliance(ratio, size)
    mark_aa = "✓" if r["aa"] else "✗"
    mark_aaa = "✓" if r["aaa"] else "✗"
    label = f"{fg} on {bg}"
    return f"  {label:<38} {ratio:>5.2f}:1  AA {mark_aa}  AAA {mark_aaa}  [{size}] — {purpose}"


def run_theme_report() -> int:
    fail = 0
    for mode, table in [("LIGHT", LIGHT), ("DARK", DARK)]:
        print(f"\n=== {mode} ===")
        for fg, bg, size, purpose in EXPECTED_PAIRS:
            fg_hex, bg_hex = table[fg], table[bg]
            print(fmt_line(fg, bg, fg_hex, bg_hex, size, purpose))
            ratio = contrast_ratio(fg_hex, bg_hex)
            if not compliance(ratio, size)["aa"]:
                fail += 1
    print()
    if fail:
        print(f"⚠️  {fail} pares abaixo de WCAG AA. Ajustar ou documentar exceção.")
        return 1
    print("✅ Todos os pares passam WCAG AA.")
    return 0


def run_pair(fg: str, bg: str, size: str) -> int:
    ratio = contrast_ratio(fg, bg)
    r = compliance(ratio, size)
    print(f"\n{fg} on {bg} ({size}): {ratio:.2f}:1")
    print(f"  AA:  {'✓ PASS' if r['aa'] else '✗ FAIL'}")
    print(f"  AAA: {'✓ PASS' if r['aaa'] else '✗ FAIL'}")
    print(f"  UI:  {'✓ PASS' if r['ui'] else '✗ FAIL'} (3:1)")
    return 0 if r["aa"] else 1


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    if args[0] == "--theme":
        return run_theme_report()
    if args[0] == "--role" and len(args) >= 2:
        try:
            fg_name, bg_name = args[1].split("-on-")
        except ValueError:
            print("Use: --role <fg>-on-<bg>")
            return 1
        size = args[2] if len(args) > 2 else "normal"
        fail = 0
        for mode, table in [("LIGHT", LIGHT), ("DARK", DARK)]:
            if fg_name not in table or bg_name not in table:
                print(f"[{mode}] role não existe: {fg_name} ou {bg_name}")
                fail += 1
                continue
            print(f"[{mode}] ", end="")
            fail += run_pair(table[fg_name], table[bg_name], size)
        return 1 if fail else 0
    if len(args) >= 2 and args[0].startswith("#"):
        return run_pair(args[0], args[1], args[2] if len(args) > 2 else "normal")
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
