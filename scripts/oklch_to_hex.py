#!/usr/bin/env python3
"""
Conversor OKLCH ↔ hex para gerar escalas perceptualmente uniformes.

OKLCH é preferível a HSL quando o objetivo é manter a sensação de
brilho constante entre hues diferentes (ex: neutralizar a sensação de
"verde mais claro que vermelho" com mesma lightness HSL).

Usage:
    # hex → OKLCH
    python scripts/oklch_to_hex.py to-oklch #08179F

    # OKLCH → hex
    python scripts/oklch_to_hex.py to-hex L=0.30 C=0.22 H=265

    # Escala perceptual uniforme (11 stops) mantendo chroma + hue
    python scripts/oklch_to_hex.py scale #08179F
"""

import math
import sys
from typing import Tuple


# ---- sRGB <-> linear ---------------------------------------------------------

def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c: float) -> float:
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


# ---- Linear sRGB <-> OKLab ---------------------------------------------------

def linear_to_oklab(rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
    r, g, b = rgb
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def oklab_to_linear(lab: Tuple[float, float, float]) -> Tuple[float, float, float]:
    L, a, b = lab
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


# ---- OKLCH polar -------------------------------------------------------------

def oklab_to_oklch(lab: Tuple[float, float, float]) -> Tuple[float, float, float]:
    L, a, b = lab
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return (L, C, H)


def oklch_to_oklab(lch: Tuple[float, float, float]) -> Tuple[float, float, float]:
    L, C, H = lch
    h = math.radians(H)
    return (L, C * math.cos(h), C * math.sin(h))


# ---- hex <-> oklch facade ----------------------------------------------------

def hex_to_oklch(h: str) -> Tuple[float, float, float]:
    h = h.lstrip('#')
    rgb_int = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    rgb_lin = tuple(srgb_to_linear(c / 255.0) for c in rgb_int)
    return oklab_to_oklch(linear_to_oklab(rgb_lin))


def oklch_to_hex(lch: Tuple[float, float, float]) -> str:
    rgb_lin = oklab_to_linear(oklch_to_oklab(lch))
    rgb_int = []
    for c in rgb_lin:
        v = linear_to_srgb(max(0.0, min(1.0, c)))
        rgb_int.append(max(0, min(255, round(v * 255))))
    return '#{:02X}{:02X}{:02X}'.format(*rgb_int)


# ---- Escala perceptual -------------------------------------------------------

LIGHTNESS_STOPS = [0.97, 0.93, 0.86, 0.77, 0.66, 0.55, 0.46, 0.38, 0.30, 0.24, 0.16]
LEVELS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]


def perceptual_scale(base_hex: str) -> dict:
    _, C, H = hex_to_oklch(base_hex)
    return {level: oklch_to_hex((L, C, H)) for level, L in zip(LEVELS, LIGHTNESS_STOPS)}


# ---- CLI ---------------------------------------------------------------------

def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1

    cmd = args[0]
    if cmd == "to-oklch" and len(args) == 2:
        L, C, H = hex_to_oklch(args[1])
        print(f"L={L:.4f}  C={C:.4f}  H={H:.2f}")
        return 0
    if cmd == "to-hex" and len(args) == 4:
        parts = {p.split("=")[0]: float(p.split("=")[1]) for p in args[1:]}
        print(oklch_to_hex((parts["L"], parts["C"], parts["H"])))
        return 0
    if cmd == "scale" and len(args) == 2:
        for level, hex_c in perceptual_scale(args[1]).items():
            print(f"  {level:>3}: {hex_c}")
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
