#!/usr/bin/env python3
"""
Auditor de tema. Varre `lib/` e reporta violações de tokens semânticos
e anti-patterns de copy/layout (regras de `docs/product.md`).

Detecta (estrutural):
  - `Color(0xFF...)` fora de `lib/core/theme/`
  - `Colors.<name>` (exceto transparent / withValues / utility) em widgets
  - `fontSize:` literal
  - `fontWeight: FontWeight.w<NNN>` literal
  - `EdgeInsets.*(<number>)` com número cru (não token AppSpacing)
  - `BorderRadius.circular(<number>)` fora da escala AppRadius

Detecta (anti-slop, conforme `docs/product.md` §4.2 e §9):
  - filler words em copy ("Eleve", "Jornada fitness", "Otimizado"...)
  - vocativos clichê ("atleta!", "campeão!", "guerreiro!")
  - em-dash decorativo em strings pt-BR
  - side-stripe borders (border-left/right > 1px)
  - generic placeholder names ("John Doe", "Acme", "Lorem ipsum")
  - gradient text decorativo (ShaderMask + LinearGradient + Text)

Usage:
    python scripts/audit_theme.py              # relatório completo
    python scripts/audit_theme.py --summary    # só contagens
    python scripts/audit_theme.py --fail       # exit 1 se houver violação
    python scripts/audit_theme.py --no-slop    # só estrutural (legacy)
    python scripts/audit_theme.py lib/features/marketplace  # subpath
"""

import os
import re
import sys
from collections import defaultdict
from typing import List, Tuple, Dict


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_SCAN = os.path.join(PROJECT_ROOT, "lib")

# Arquivos onde hex hardcoded é legítimo (source of truth do tema)
ALLOW_HEX_IN = (
    "lib/core/theme/app_colors.dart",
    "lib/core/theme/app_theme.dart",
)

# Arquivos onde cores Colors.X crua é justificável (cache: avatar patrocinador)
# Ajuste manual — lista fechada.
ALLOW_COLORS_IN = (
    # vazio por enquanto; `Colors.white` para avatar de patrocinador documentado
)

EXCLUDE_SUFFIXES = (".g.dart", ".freezed.dart")

PATTERNS: Dict[str, re.Pattern] = {
    "hex_color": re.compile(r"Color\(0x[0-9A-Fa-f]{8}\)"),
    "material_color": re.compile(r"\bColors\.(?!transparent\b)[a-zA-Z]+"),
    "font_size": re.compile(r"\bfontSize\s*:\s*[0-9]"),
    "font_weight": re.compile(r"fontWeight\s*:\s*FontWeight\.w[0-9]+"),
    "edge_insets_literal": re.compile(
        r"EdgeInsets\.(?:all|symmetric|only|fromLTRB)\([^)]*\b\d{1,3}(?:\.\d+)?\b"
    ),
    "radius_literal": re.compile(r"BorderRadius\.circular\(\s*\d+(?:\.\d+)?\s*\)"),
}

# Regras anti-slop (product.md §4.2 + §9). Operam sobre conteúdo de strings (entre aspas)
# ou em decoration. Ativadas por default; desligar com --no-slop.
SLOP_PATTERNS: Dict[str, re.Pattern] = {
    # filler words (case-insensitive, substring match dentro de strings literais "..." ou '...')
    "filler_copy": re.compile(
        r'''["'][^"']*\b(?:'''
        r'eleve\s+(?:seu|sua)|'
        r'desbloqueie\s+(?:seu|sua)|'
        r'liberte\s+(?:o\s+atleta|seu)|'
        r'otimizad[oa]\s+para|'
        r'sem\s+fric(?:c|ç)(?:a|ã)o|'
        r'jornada\s+fitness|'
        r'transforme\s+sua\s+rotina|'
        r'pr(?:o|ó)ximo\s+n(?:i|í)vel|'
        r'conquiste\s+seus?\s+objetivos?|'
        r'sua\s+melhor\s+vers(?:a|ã)o|'
        r'continue\s+assim|'
        r'voc(?:e|ê)\s+(?:e|é)\s+incr(?:i|í)vel|'
        r'experi(?:e|ê)ncia\s+seamless'
        r''')\b[^"']*["']''',
        re.IGNORECASE,
    ),
    # vocativos clichê em copy (com vírgula, exclamação, ou no início)
    "cliche_vocative": re.compile(
        r'''["'][^"']*\b(?:atleta|campe(?:a|ã)o|guerreir[oa])[!,.][^"']*["']''',
        re.IGNORECASE,
    ),
    # generic placeholder names em strings
    "generic_placeholder": re.compile(
        r'''["'][^"']*\b(?:John\s+Doe|Jane\s+Doe|Lorem\s+ipsum|Acme(?:\s+Corp)?|Sarah\s+Chan|SmartFlow)\b[^"']*["']''',
        re.IGNORECASE,
    ),
    # em-dash em string pt-BR (em copy, decorativo). Strings de comentário e `—` técnico ignorados pela linha-comment-skip
    "em_dash_in_copy": re.compile(r'''["'][^"']*—[^"']*["']'''),
    # side-stripe border (border-left/right > 1px usado decorativo)
    "side_stripe_border": re.compile(
        r"BorderSide\([^)]*width\s*:\s*[2-9](?:\.\d+)?\s*[,)]"
    ),
    # gradient text decorativo: ShaderMask aplicado em Text com LinearGradient explícito
    # heurística: linha contém ShaderMask E LinearGradient (multi-line ShaderMask escapará — ok, é regra rápida)
    "gradient_text": re.compile(r"ShaderMask\s*\([^)]*LinearGradient", re.DOTALL),
}

ALLOWED_SPACING = {0, 1, 2, 4, 8, 12, 16, 20, 24, 32, 48, 64}  # AppSpacing + extras comuns
ALLOWED_RADIUS = {0, 6, 10, 14, 20, 999}  # AppRadius

# Arquivos onde slop check é desligado (i18n source-of-truth, fixtures de teste com nomes genéricos)
SLOP_SKIP = (
    "lib/core/theme/preview/",
    "test/",
    "integration_test/",
)


def relpath(path: str) -> str:
    return os.path.relpath(path, PROJECT_ROOT).replace(os.sep, "/")


def is_allowed_for(rule: str, rel_path: str) -> bool:
    if rule == "hex_color":
        return any(rel_path.endswith(p) or rel_path == p for p in ALLOW_HEX_IN)
    if rule == "material_color":
        return any(rel_path.endswith(p) for p in ALLOW_COLORS_IN)
    return False


def extract_number(s: str) -> List[float]:
    return [float(n) for n in re.findall(r"\d+(?:\.\d+)?", s)]


def filter_literal_spacing(match: str) -> bool:
    """Retorna True se o literal encontrado contém um número fora da escala."""
    nums = extract_number(match)
    return any(n not in ALLOWED_SPACING for n in nums)


def filter_literal_radius(match: str) -> bool:
    nums = extract_number(match)
    return any(n not in ALLOWED_RADIUS for n in nums)


def scan_file(path: str, check_slop: bool = True) -> Dict[str, List[Tuple[int, str]]]:
    hits: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
    rel = relpath(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError):
        return hits

    slop_active = check_slop and not any(skip in rel for skip in SLOP_SKIP)

    for i, line in enumerate(lines, start=1):
        if line.lstrip().startswith("//"):
            continue
        for rule, pattern in PATTERNS.items():
            if is_allowed_for(rule, rel):
                continue
            for m in pattern.finditer(line):
                text = m.group(0)
                if rule == "edge_insets_literal" and not filter_literal_spacing(text):
                    continue
                if rule == "radius_literal" and not filter_literal_radius(text):
                    continue
                hits[rule].append((i, line.rstrip()))
        if slop_active:
            for rule, pattern in SLOP_PATTERNS.items():
                if pattern.search(line):
                    hits[rule].append((i, line.rstrip()))
    return hits


def walk_dart(root: str):
    for dirpath, _, files in os.walk(root):
        for name in files:
            if not name.endswith(".dart"):
                continue
            if any(name.endswith(suf) for suf in EXCLUDE_SUFFIXES):
                continue
            yield os.path.join(dirpath, name)


def main() -> int:
    args = sys.argv[1:]
    summary_only = "--summary" in args
    fail_on_hit = "--fail" in args
    no_slop = "--no-slop" in args
    paths = [a for a in args if not a.startswith("--")]
    scan_root = paths[0] if paths else DEFAULT_SCAN
    scan_root = os.path.abspath(scan_root)

    totals: Dict[str, int] = defaultdict(int)
    per_file: Dict[str, Dict[str, List[Tuple[int, str]]]] = {}

    for path in walk_dart(scan_root):
        hits = scan_file(path, check_slop=not no_slop)
        if any(hits.values()):
            per_file[relpath(path)] = hits
            for rule, xs in hits.items():
                totals[rule] += len(xs)

    print(f"\n=== audit em {relpath(scan_root)} ===\n")

    if not per_file:
        print("✅ Nenhuma violação encontrada.")
        return 0

    if not summary_only:
        for rel, hits in sorted(per_file.items()):
            total = sum(len(xs) for xs in hits.values())
            print(f"📄 {rel}  ({total})")
            for rule, xs in hits.items():
                for line_no, line in xs:
                    print(f"   {rule:>22}  L{line_no:<5}  {line.strip()[:90]}")
            print()

    print("Totais por regra (estrutural):")
    for rule in PATTERNS.keys():
        print(f"  {rule:>22}: {totals.get(rule, 0)}")

    if not no_slop:
        slop_total = sum(totals.get(r, 0) for r in SLOP_PATTERNS.keys())
        if slop_total:
            print("\nTotais por regra (anti-slop):")
            for rule in SLOP_PATTERNS.keys():
                print(f"  {rule:>22}: {totals.get(rule, 0)}")

    total_hits = sum(totals.values())
    total_files = len(per_file)
    print(f"\n📊 {total_hits} violações em {total_files} arquivos")

    return 1 if (fail_on_hit and total_hits) else 0


if __name__ == "__main__":
    sys.exit(main())
