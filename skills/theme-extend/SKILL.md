---
name: theme-extend
description: Adds or tweaks semantic tokens in the project's design system (colors, typography roles, spacing, radius). Generates WCAG-validated light/dark pairs, updates `AppColors`, `docs/design-tokens.md` and suggests where to apply. Use to resolve contrast failures detected by `/theme-audit`, add a new semantic role, or tune an existing value. Use when the user asks for `/Surgeon`, `/Cirurgião`, `/theme-extend`, "adiciona um token", "add a token", "resolve contraste de X", "fix contrast", "melhora o tema".
---

# Skill: theme-extend (`/theme-extend`) — persona **Cirurgião** (English: **Surgeon**)

## Triggers

- **English:** `/Surgeon`, `/theme-extend`, "add a semantic token", "extend the theme", "resolve contrast for X", "tune semantic color"
- **Português:** `/Cirurgião`, `/Cirurgiao`, `/cirurgião`, `/cirurgiao`, `/theme-extend`, "adiciona um token", "resolve contraste", "melhora o tema", "ajusta cor semântica"
- **Natural language:** WCAG fail flagged by audit; "I need a new role for X"; "the success green looks too light"

Modifica o tema de forma cirúrgica. Dois cenários principais:

1. **Adicionar novo semantic role** (ex: `chipSelectedBg`, `runningHero`, `levelGold`) quando nenhum dos 29 tokens atuais encaixa.
2. **Ajustar valor existente** (ex: `feedbackSuccess` muito claro no light → escurecer mantendo a hue).

Nunca toca em widgets — só no theme layer. Widgets depois consomem via `context.colors.<token>`.

**Reference token system (project-default):** ~29 tokens grouped as `bg*` (6), `brand*` (5), `text*` (4), `border*` (3), `feedback*` (8 = 4 colors × 2 variants), `gameAccent*` (3). Domain-invariant tokens (chip, running, pass) live in `AppColors` itself; do not reintroduce a separate `AppBrandColors` class. Override in `.design-workflow.yaml` when your project's token shape differs.

## Pré-condições

Antes de estender, responder:

- **Por que o token existente não serve?** Se `brand` cobre, não crie `primary`. Evitar proliferação.
- **Qual o papel semântico?** Descrever em uma frase. Se a descrição é "a cor X tal", está errado — precisa ser um papel (ex: "destaque em card de desafio sponsorado").
- **Onde vai ser usado?** Listar 2-3 call sites pretendidos. Se só 1, reconsiderar se token é necessário ou se é invariante de marca → `AppBrandColors`.

## Workflow

### Cenário A — Adicionar novo semantic role

#### Step A1 — Propor hue de partida

Se o usuário já tem a cor em mente, usar. Senão:

```bash
# Gerar escala OKLCH (perceptualmente uniforme) a partir de brand
python scripts/theme/oklch_to_hex.py scale "#08179F"

# Ou um par light/dark a partir de uma cor candidata
python scripts/theme/generate_palette.py pair "#8B5CF6" --name accent
```

O modo `pair` gera light (saturado, L~0.45) e dark (menos saturado, L~0.70, para destacar em fundo escuro) automaticamente.

#### Step A2 — Validar contraste

```bash
python scripts/theme/check_contrast.py <novo_hex_light> <surface_light>
python scripts/theme/check_contrast.py <novo_hex_dark> <surface_dark>
```

Também testar contra `card` e o uso pretendido (ex: se for fg de botão, contra `brand`).

Se falhar AA:
- Escurecer a versão light (aumentar `L` no OKLCH).
- Clarear a versão dark.
- Repetir até passar.

#### Step A3 — Build Adapter Plan + dispatch

Em vez de editar `app_colors.dart` diretamente, emit um **Adapter Plan** `kind: palette` e delegue ao adapter da stack ativa.

```bash
# 1. Resolve active stack — STACK env > config.stack > flutter
STACK=$(python3 scripts/resolve_stack.py)

# 2. Emit Plan (extends current palette with the new role)
cat > /tmp/extend-<novoToken>-plan.json <<EOF
{
  "version": "1.0",
  "kind": "palette",
  "tokens": {
    "palette": {
      "<novoToken>": {"light": "#XXXXXX", "dark": "#YYYYYY"}
      /* + outros 29 roles existentes (read from current AppColors / globals.css) */
    }
  },
  "actions": [
    {"op": "patch",  "role": "palette",       "intent": "tokens"},
    {"op": "append", "role": "design-tokens", "intent": "doc-summary"}
  ]
}
EOF

# 3. Adapter renders to native:
python3 adapters/$STACK/adapter.py /tmp/extend-<novoToken>-plan.json
```

Por stack:

- **flutter:** o adapter atualiza `lib/core/theme/app_colors.dart` (field, constructor, light/dark instances, `copyWith`, `lerp` — os 6 lugares ficam responsabilidade do template). Token de feedback (`feedbackXxx` + `feedbackXxxMuted`) requer **2 entradas** no Plan.
- **nextjs-tailwind:** o adapter atualiza `app/globals.css` (`:root` + `.dark` blocks) e regenera o snippet `tailwind.config.ts.tmpl` para `theme.extend.colors`.

Se o token novo for badge, manter compat com `AppBadgeColors.fromAppColors()` em Flutter — o adapter ainda não cobre badge derivation (planned v1.3); o Plan declara o role base e o operador faz o passo manual.

O script `generate_palette.py pair` continua útil para gerar o par light/dark hex que vai dentro do Plan.

#### Step A4 — Atualizar `docs/design-tokens.md`

Adicionar linha à tabela de § 1 no formato:

```
| `<novoRole>` | <papel semântico em uma frase> | `#XXXXXX` | `#YYYYYY` |
```

Manter a ordem alfabética por categoria (estrutural primeiro, depois texto, depois semantic).

#### Step A5 — Validar

```bash
flutter analyze                                 # zero issue
python scripts/theme/check_contrast.py --theme  # ver novo role no relatório
```

Se contraste geral regrediu, reverter e refazer Step A1-A2.

### Cenário B — Ajustar token existente

#### Step B1 — Diagnóstico

`/theme-audit` identifica o par problemático. Exemplo:

```
LIGHT: feedbackSuccess on bgBase   2.18:1  AA ✗   (atual: #22C55E on #F5F6FE)
```

#### Step B2 — Propor novo valor

Manter a hue (para reconhecimento), ajustar lightness/chroma:

```bash
# Ver a hue atual
python scripts/theme/oklch_to_hex.py to-oklch "#22C55E"
# → L=0.7860 C=0.1772 H=142.50

# Gerar versão com L menor (mais escura) mantendo chroma e hue
python scripts/theme/oklch_to_hex.py to-hex L=0.55 C=0.17 H=142.5
# → #16A34A

# Validar
python scripts/theme/check_contrast.py "#16A34A" "#F5F6FE"
# → 4.63:1 AA ✓
```

#### Step B3 — Impacto lateral

**Antes de editar**: verificar onde `feedbackSuccess` (ou o token em questão) é usado:

```bash
grep -rn "colors.feedbackSuccess" lib/
```

Avaliar se o novo tom ainda funciona em todos os contextos (fundo claro E fundo escuro). Como `AppColors.navyBlue` (light) e `AppColors.darkBlue` (dark) são instâncias separadas, você ajusta cada uma independentemente. Se badge derivado também é afetado (ex: `feedbackSuccess` muda → `abertoText` muda automaticamente via `AppBadgeColors.fromAppColors`), validar nas screens que consomem badge também.

#### Step B4 — Editar + atualizar doc

Trocar apenas o hex em `AppColors.navyBlue` (light) e/ou `AppColors.darkBlue` (dark). Atualizar tabela em `docs/design-tokens.md`. `copyWith`/`lerp` não mudam.

#### Step B5 — Validar

```bash
flutter analyze
python scripts/theme/check_contrast.py --theme
```

Diff visual no app: rodar em light + dark, verificar feature que consome o token (ex: toasts de success, badges de arena).

## Typography extend

Novo role **raramente** é necessário — os 13 M3 roles cobrem quase tudo. Considerar antes:

- Tamanho intermediário? Provavelmente o role imediatamente acima ou abaixo já atende.
- Peso diferente? Role base + `.copyWith(fontWeight: ...)` no widget (ou, se recorrente, proposto como ajuste do `buildAppTextTheme`).
- Família diferente? Já temos Plus Jakarta (display/headline/title) e MSJH (body/label). Terceira família só se a identidade exigir.

Se realmente necessário, editar `lib/core/theme/app_typography.dart > buildAppTextTheme`. E lembrar: qualquer mudança de base-size propaga no FontScale A/A+/A++ automaticamente.

## Spacing / Radius extend

A escala atual (`AppSpacing` 9 valores, `AppRadius` 5 valores) cobre 95% dos casos. Antes de adicionar:

- Conferir se o Figma pode snap para o token mais próximo (±2px).
- Se o valor aparece em ≥3 lugares, é candidato legítimo a token novo.

Adicionar em `lib/core/theme/app_spacing.dart`. Atualizar `docs/design-tokens.md`.

## Anti-patterns

- ❌ Adicionar token só porque "aparece bonito em um frame específico".
- ❌ Esquecer dark value — Figma é light, tema é light+dark.
- ❌ Pular WCAG — token semântico que falha AA é tecnicamente inacessível.
- ❌ Renomear token existente (breaks: refactor manual em vez de rename automático).
- ❌ Editar `app_typography.dart` sem conferir o impacto nos 3 FontScale steps.
- ❌ Duplicar conceito: `primary`/`brand`/`mainColor` são todos a mesma coisa — só `brandDefault` existe.
- ❌ Restaurar `AppBrandColors` — foi eliminado. Tokens novos vão direto no `AppColors`.

## Decision table — onde colocar o token novo

| Tipo de token | Grupo no AppColors | Exemplo | WCAG necessário? |
|---|---|---|---|
| Background (page/card/modal) | `bg*` | `bgInput`, `bgSurfaceRaised` | Não diretamente, mas afeta contraste de texto que vai sobre ele |
| Cor de marca / ação primária | `brand*` | `brandPressed`, `brandDisabled` | Texto sobre brand precisa AA |
| Texto | `text*` | `textMuted` | Sim — AA mín sobre `bgBase` |
| Borda / divider | `border*` | `borderFocus` | Não obrigatório (visual cue) |
| Status semântico (success/warning/error/info) | `feedback*` | `feedbackSuccess` + `feedbackSuccessMuted` | Sim — AA sobre `bgBase` |
| Decorativo / gamificação | `gameAccent*` | `gameAccent` | Não (uso decorativo) |
| Status de marketplace/coupon | `AppBadgeColors` (derivado via factory) | `abertoBg/Text/Border` | Derivado — herda do feedback |

## Integração

| Entrada | Saída |
|---------|-------|
| `/theme-audit` flagou falha WCAG | `/theme-extend` cenário B ajusta token |
| `/theme-port` parou porque fill não encaixou | `/theme-extend` cenário A adiciona role |
| `/theme-create` entregou palette nova | Não precisa `/theme-extend` imediatamente |

Após extend, sempre sugerir re-rodar `/theme-audit` no escopo afetado.
