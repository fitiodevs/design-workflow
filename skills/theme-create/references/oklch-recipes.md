# OKLCH recipes — per-token light/dark targets

Use these tables when running Step 5 of `/theme-create`. Each token gets a light + dark value validated against WCAG (Step 6 of the SKILL).

The reference shape is ~29 tokens in 7 groups (`bg*` 6, `brand*` 5, `text*` 4, `border*` 3, `feedback*` 8 = 4 colors × 2 variants, `gameAccent*` 3). If your project uses a different shape, override in `.design-workflow.yaml`.

L = OKLCH lightness · C = OKLCH chroma.

## Backgrounds (6 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `bgBase` | 0.96-0.98 | 0.07-0.10 | Page bg, off-white/off-black |
| `bgSurface` | 0.99-1.00 | 0.11-0.14 | Cards, modais, elevado |
| `bgSurfaceRaised` | 0.99-1.00 | 0.11-0.14 | Igual ou +0.01 vs surface |
| `bgInput` | 0.93-0.96 | 0.16-0.19 | Field fill, mais escuro que surface |
| `bgSkeleton` | 0.90-0.93 | 0.17-0.20 | Loading shimmer base |
| `bgOverlay` | rgba(0,0,0,0.6) | rgba(0,0,0,0.6) | Modal scrim, geralmente igual |

## Brand / Ação (5 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `brandDefault` | 0.30-0.45 | 0.30-0.50 | Pode manter mesma hue/L ou clarear no dark |
| `brandMuted` | 0.92-0.96 | 0.18-0.25 | Bg de chip selecionado, low-sat |
| `brandOnColor` | 0.99-1.00 | 0.99-1.00 | Texto/ícone sobre brand — quase sempre branco |
| `brandPressed` | 0.22-0.30 | 0.55-0.70 | -0.08 do default no light, +0.20 no dark |
| `brandDisabled` | 0.65-0.78 | 0.30-0.40 | Mid, baixa sat, sem WCAG (decorativo) |

## Texto (4 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `textPrimary` | 0.08-0.18 | 0.95-1.00 | Max contraste, ~21:1 |
| `textSecondary` | 0.30-0.45 | 0.65-0.78 | WCAG AA mín 4.5:1 sobre `bgBase` |
| `textMuted` | 0.50-0.60 | 0.50-0.62 | Captions, helper — AA opcional (small text) |
| `textOnBrand` | 0.99-1.00 | 0.99-1.00 | Branco/quase, contraste sobre `brandDefault` |

## Bordas (3 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `borderDefault` | 0.86-0.92 | 0.20-0.28 | Card stroke, divider |
| `borderStrong` | 0.74-0.80 | 0.30-0.38 | Outlined input, ênfase |
| `borderFocus` | = `brandDefault` | = `brandDefault` (light) ou variante saturada | Sempre igual ao brand do tema |

## Feedback semântico (8 tokens — cada um tem `<x>` + `<x>Muted`)

Hue alvo por papel:

| Papel | Hue OKLCH | Light L (cor) | Dark L (cor) | Light L (Muted) | Dark L (Muted) |
|-------|----------:|--------------:|-------------:|----------------:|---------------:|
| `feedbackSuccess` | ~140-150 | 0.50-0.58 | 0.78-0.85 | 0.93-0.96 | 0.18-0.22 |
| `feedbackWarning` | ~65-80 | 0.55-0.65 (não usar amarelo puro — falha AA) | 0.85-0.92 | 0.93-0.96 | 0.16-0.20 |
| `feedbackError` | ~25-30 | 0.50-0.58 | 0.65-0.72 | 0.92-0.96 | 0.16-0.20 |
| `feedbackInfo` | ~245-260 | 0.45-0.55 | 0.70-0.80 | 0.92-0.96 | 0.13-0.18 |

Validar AA (4.5:1) de cada cor sobre `bgBase` em ambos os modos. `*Muted` não precisa AA (é background de badge).

## Gamificação (3 tokens)

| Token | Light | Dark | Regra |
|-------|-------|------|-------|
| `gameAccent` | hue 35-45, alto C | mesmo ou +0.05 L | Âmbar/dourado/neon decorativo — sem WCAG |
| `gameAccentMuted` | L 0.92-0.96 | L 0.16-0.22 | Bg de badge gamificado |
| `gameAccentOnColor` | L 0.20-0.30 | L 0.85-0.92 | Texto sobre `gameAccent` se aplicável |
