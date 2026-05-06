#!/usr/bin/env python3
"""
Gerador de paletas com saída pronta pra `AppColors` (estrutura Flutter).

Usage:
    # Escala Tailwind 50..950 a partir de uma base
    python scripts/generate_palette.py scale #08179F

    # Paleta harmônica (complementary / triadic / analogous / split)
    python scripts/generate_palette.py triadic #08179F

    # Par light+dark pronto para um novo semantic role (+ Dart snippet)
    python scripts/generate_palette.py pair #08179F --name accent

    # Paleta de marca completa (primary + neutral + semantic) em Dart
    python scripts/generate_palette.py brand #08179F
"""

import sys
import colorsys
from typing import Tuple, Dict


# ---- Color math --------------------------------------------------------------

def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return '#{:02X}{:02X}{:02X}'.format(*[max(0, min(255, int(c))) for c in rgb])


def rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360, s, l)


def hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
    h, s, l = hsl
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


# ---- Palette operations ------------------------------------------------------

LIGHTNESS_MAP = {
    50: 0.97, 100: 0.94, 200: 0.86, 300: 0.77, 400: 0.65,
    500: 0.50, 600: 0.42, 700: 0.34, 800: 0.27, 900: 0.23, 950: 0.15,
}


def generate_scale(base_hex: str, base_level: int = 500) -> Dict[int, str]:
    h, s, l = rgb_to_hsl(hex_to_rgb(base_hex))
    offset = l - LIGHTNESS_MAP[base_level]
    scale: Dict[int, str] = {}
    for level, target in LIGHTNESS_MAP.items():
        adj_l = max(0.0, min(1.0, target + offset))
        if level >= 600:
            adj_s = min(1.0, s * (1.0 + (level - 500) * 0.0003))
        else:
            adj_s = max(0.0, s * (1.0 - (500 - level) * 0.0005))
        scale[level] = rgb_to_hex(hsl_to_rgb((h, adj_s, adj_l)))
    return scale


def harmonic(base_hex: str, mode: str) -> Dict[str, str]:
    h, s, l = rgb_to_hsl(hex_to_rgb(base_hex))
    if mode == "complementary":
        return {"primary": base_hex, "complementary": rgb_to_hex(hsl_to_rgb(((h + 180) % 360, s, l)))}
    if mode == "triadic":
        return {
            "primary": base_hex,
            "secondary": rgb_to_hex(hsl_to_rgb(((h + 120) % 360, s, l))),
            "tertiary": rgb_to_hex(hsl_to_rgb(((h + 240) % 360, s, l))),
        }
    if mode == "analogous":
        return {
            "left": rgb_to_hex(hsl_to_rgb(((h - 30) % 360, s, l))),
            "base": base_hex,
            "right": rgb_to_hex(hsl_to_rgb(((h + 30) % 360, s, l))),
        }
    if mode == "split":
        return {
            "primary": base_hex,
            "split_a": rgb_to_hex(hsl_to_rgb(((h + 150) % 360, s, l))),
            "split_b": rgb_to_hex(hsl_to_rgb(((h + 210) % 360, s, l))),
        }
    raise ValueError(mode)


def light_dark_pair(base_hex: str) -> Tuple[str, str]:
    """Gera par (light, dark) para um semantic role novo.

    Light: base saturado, lightness ~0.45
    Dark:  mesma hue, saturação levemente reduzida, lightness ~0.70 (pop contra fundo escuro)
    """
    h, s, l = rgb_to_hsl(hex_to_rgb(base_hex))
    light = rgb_to_hex(hsl_to_rgb((h, min(1.0, s * 1.05), 0.45)))
    dark = rgb_to_hex(hsl_to_rgb((h, max(0.0, s * 0.85), 0.70)))
    return (light, dark)


# ---- Dart output -------------------------------------------------------------

def fmt_dart_color(hex_str: str) -> str:
    return f"Color(0xFF{hex_str.lstrip('#').upper()})"


def print_pair_dart(role_name: str, light: str, dark: str) -> None:
    print("\n// 1. Em AppColors adicione o campo:")
    print(f"  final Color {role_name};")
    print("\n// 2. No constructor:")
    print(f"  required this.{role_name},")
    print("\n// 3. Em AppColors.light:")
    print(f"  {role_name}: {fmt_dart_color(light)},")
    print("\n// 4. Em AppColors.dark:")
    print(f"  {role_name}: {fmt_dart_color(dark)},")
    print("\n// 5. copyWith / lerp: adicione a linha correspondente (siga o padrão do arquivo).")
    print("\n// 6. docs/design-tokens.md: adicione uma linha na tabela de § 1.")


def print_brand_dart(primary: str) -> None:
    scale = generate_scale(primary)
    print(f"\n// Paleta sugerida para brand = {primary}")
    print("// Propõe pares light/dark compatíveis com AppColors.")
    print()
    print("static const AppColors light = AppColors(")
    print(f"  brand: {fmt_dart_color(primary)},")
    print(f"  brandMuted: {fmt_dart_color(scale[100])},")
    print(f"  surface: {fmt_dart_color(scale[50])},")
    print(f"  surfaceVariant: {fmt_dart_color('#F4F4F4')},")
    print(f"  card: Colors.white,")
    print(f"  border: {fmt_dart_color('#E0E0E0')},")
    print(f"  textPrimary: {fmt_dart_color('#1E272E')},")
    print(f"  textSecondary: {fmt_dart_color('#636363')},")
    print(f"  textInverted: Colors.white,")
    print(f"  success: {fmt_dart_color('#22C55E')},")
    print(f"  warning: {fmt_dart_color('#F59E0B')},")
    print(f"  danger: {fmt_dart_color('#FF3B30')},")
    print(f"  info: {fmt_dart_color(scale[500])},")
    print(f"  overlay: Color(0x80000000),")
    print(f"  skeleton: {fmt_dart_color('#E9EBEE')},")
    print(");")


# ---- CLI ---------------------------------------------------------------------

def main() -> int:
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 1

    mode, base = args[0], args[1]

    if mode == "scale":
        scale = generate_scale(base)
        print(f"\nEscala para {base}:")
        for level, hex_c in scale.items():
            print(f"  {level:>3}: {hex_c}")
        return 0

    if mode in ("complementary", "triadic", "analogous", "split"):
        p = harmonic(base, mode)
        print(f"\n{mode.capitalize()}:")
        for k, v in p.items():
            print(f"  {k:>14}: {v}")
        return 0

    if mode == "pair":
        name = "accent"
        if "--name" in args:
            name = args[args.index("--name") + 1]
        light, dark = light_dark_pair(base)
        print(f"\nPar semantic para '{name}':")
        print(f"  light: {light}")
        print(f"  dark:  {dark}")
        print_pair_dart(name, light, dark)
        return 0

    if mode == "brand":
        print_brand_dart(base)
        return 0

    print(f"Modo desconhecido: {mode}")
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
