---
name: theme-create
description: Creates a complete palette from scratch (brand + semantic + neutral) or an alternative visual identity (sub-brand, seasonal mode, sponsor skin) for a Flutter app. Uses OKLCH for perceptually-uniform scales, validates WCAG automatically, emits a ready-to-paste `AppColors` plus anti-AI-slop rationale plus reference sheet in `docs/themes/`. Use when no incremental tweak fits and identity must be redesigned. Triggers: `/Composer`, `/Compositor`, `/theme-create`, "cria palette nova", "nova identidade visual", "create a new palette", "sub-brand for X".
---

# Skill: theme-create (`/theme-create`) — persona **Compositor** (English: **Composer**)

## Triggers

- **English:** `/Composer`, `/theme-create`, "create a new palette", "new visual identity", "sub-brand", "palette from scratch"
- **Português:** `/Compositor`, `/compositor`, `/theme-create`, "cria palette nova", "nova identidade visual", "sub-brand", "palette do zero"
- **Natural language:** seasonal skin (Black Friday); sponsor branded event; full identity refresh

Creates a complete palette from scratch. **Use sparingly** — most projects already have a base theme (e.g. ~29 semantic tokens organized as light/dark instances) and `/theme-extend` covers most needs. Legitimate scenarios:

- Sub-brand (vertical/sub-product with distinct identity).
- Seasonal mode (Black Friday, Copa do Mundo) with a temporary skin.
- Sponsor skin (branded event).
- Full refresh (rare — coordinate with design).

## Filosofia (anti-AI-slop)

Match implementation complexity to vision. **Maximalismo precisa de execução elaborada** (animações, gradient meshes, microinterações). **Minimalismo precisa de precisão** (spacing, typography, sutilezas). Elegância vem de executar a visão escolhida com convicção — não de baixar a intensidade.

Princípios não-negociáveis:

- **Dominância + accent agudo** > paleta evenly-distributed. Um tema "70% brand + 20% neutral + 10% accent" sempre supera "5 cores em 20% cada".
- **Surface nunca é branco/preto puros.** Off-white (`#F5F6FE`+) e off-black (`#0D0F1A`-) dão personalidade.
- **Dark mode tem personalidade própria** — não é inversão mecânica do light.
- **Saturação varia entre roles.** Tudo em high-sat = ruído visual; tudo em low-sat = tema "tech genérico".
- **Inspiração precisa ser rastreável** a algo real (brand existente, fotografia específica, cultura, material físico). Sem rastreio = AI-slop.

## Pré-condições (responder em uma frase cada antes de gerar)

**Gate 0 — `docs/product.md` carregado.** Se ausente/vazio (<2KB), parar. Source of truth de tom, anti-references e anti category-reflex (§5.1). Sem isso, palette cai em verde Strava / preto+laranja Nike / roxo AI por reflexo.

1. **Purpose / domínio** — Fitness? Evento? Patrocinador? Sub-vertical? Que problema visual resolve?
2. **Audiência** — Mesma do app principal ou nicho específico? O que ela já consome?
3. **Tone / mood** — Pegue um extremo da lista abaixo. Genéricos como "moderno/clean/profissional" são bandeira vermelha.
4. **Invariantes de marca** — Algo fixo do projeto que precisa aparecer (ex: `brandDefault` como base, `gameAccent` decorativo)?
5. **Differentiation** — Em uma frase: **o que torna esse tema inesquecível?** Qual é a UMA coisa que alguém vai lembrar? (Sem resposta concreta = palette genérica.)
6. **Coexistência** — Substitui o tema atual ou é alternativo por contexto/rota?
7. **Color strategy commitment** (`docs/product.md` §5.3) — Restrained, Committed, Full palette ou Drenched? Surface por surface, mas a palette tem que suportar todos os 4 níveis.
8. **Anti category-reflex check** — Se alguém adivinha a palette pelo nome do domínio ("app fitness brasileiro → preto + verde-limão"), refazer. Comparar com anti-references de `docs/product.md` §7.

Se qualquer resposta for vaga, parar e perguntar. Criar palette sem direção → AI-slop garantido.

### Vocabulário de tone (escolher UM extremo, não meio-termo)

| Tone | Como se manifesta em paleta |
|------|-----------------------------|
| Brutally minimal | 2-3 cores, off-white + 1 ink + 1 accent saturado |
| Maximalist chaos | 5+ hues conflituosas, layers, contraste extremo |
| Retro-futuristic | Neons sobre dark, navy + magenta/cyan/lime |
| Organic / natural | Earth tones, baixa sat, textura de pigmento |
| Luxury / refined | Off-black + cream + 1 metálico (ouro velho, bronze) |
| Playful / toy-like | Pastéis saturados, contornos grossos, candy palette |
| Editorial / magazine | Tipo dominante, cor minimalista, cream + ink + 1 accent |
| Brutalist / raw | Concrete grays, yellow safety, terminal green |
| Art deco / geometric | Black + gold + jewel tones, simetria |
| Soft / pastel | Hue ampla mas C baixo, sem preto, sem white puro |
| Industrial / utilitarian | Hi-vis, signage tones, mono-cinza + 1 hi-contrast |

## Workflow

### Step 1 — Mood board verbal

Descrever a palette em 3-5 palavras concretas **antes** de escolher cores. Exemplos válidos:

- "Arena neon, competitivo, urbano, alta energia" → cores vivas, alto chroma, possível dark-first.
- "Marketplace premium, sereno, confiável, produto físico" → tons terrosos muted, baixa saturação, foco em produto.
- "Black Friday agressivo, urgência, desconto" → alto contraste, accent vermelho/laranja, timer-driven.

**Red flags de AI-slop** (parar e reformular se aparece):

- "Moderno, clean, minimalista" — sem direção.
- "Tech/SaaS profissional" — gera purple-blue gradient padrão.
- "Vibrante e alegre" — orange+teal quase garantido.
- "Inspirado em [grande tech]" — cópia, não identidade.

### Step 2 — Escolher base color

Ponto de partida tem 3 fontes válidas:

- **A.** Existente da marca: `brandDefault`, `gameAccent`, ou hex histórico já estabelecido do projeto.
- **B.** Cor de uma referência real (foto, cultura, material físico). Extrair manualmente, informar hex + a referência.
- **C.** Cor proposta pelo usuário/design.

**Nunca** usar defaults do Tailwind/Material Design (`#3B82F6`, `#8B5CF6`, `#10B981`, `#EF4444`) como base — é AI-slop direto.

### Step 3 — Gerar escala perceptual

```bash
python scripts/theme/oklch_to_hex.py scale "<base_hex>"
```

OKLCH produz escala perceptualmente uniforme (lightness consistente entre hues), diferente do HSL que "afunda" azuis/roxos. Saída: 11 stops (50, 100, 200, ..., 950).

Usar 500 como base, 50/100 como surface muted, 900/950 como texto em fundo claro.

### Step 4 — Estratégia de paleta

Três abordagens. Escolher UMA com base no tone:

#### A. Monocromática + neutral (tone: minimal, refined, editorial)

Uma hue só + escala de cinza neutra.

```
brand: base + escala 50-950
neutral: OKLCH com C=0.01, mesma L da escala
feedback: success/warning/error/info com hue dominante leve
```

#### B. Complementar — brand + accent (tone: competitivo, brutalist, retro-futuristic)

```bash
python scripts/theme/generate_palette.py complementary "<base_hex>"
```

Alto contraste intencional. Uso do accent ≤10% (regra 60-30-10).

#### C. Analógica — brand + 2 próximas (tone: organic, soft, premium sereno)

```bash
python scripts/theme/generate_palette.py analogous "<base_hex>"
```

Suave, harmonioso. Evitar em contextos competitivos/urgentes.

**Triadic/split**: disponíveis mas raramente apropriados — risco de "carnaval de cores". Use só com direção explícita de design.

### Step 5 — Montar pares light + dark dos ~29 tokens

Reference shape: ~29 tokens in 7 groups (`bg*` 6, `brand*` 5, `text*` 4, `border*` 3, `feedback*` 8 = 4 cores × 2 variants, `gameAccent*` 3). Each token needs a validated light + dark pair.

**Read `references/oklch-recipes.md` before generating** — it carries the per-token L/C target tables for each group, plus per-feedback hue ranges. Without those tables, lightness picks become guesswork and WCAG fails recur in Step 6.

### Step 6 — Validar WCAG

```bash
python scripts/theme/check_contrast.py --theme
```

**Pares obrigatórios AA (24 totais = 12 pares × 2 modos):**

- `textPrimary` × `bgBase` / `bgSurface` / `bgInput`
- `textSecondary` × `bgBase` / `bgSurface`
- `textOnBrand` × `brandDefault`
- `feedbackSuccess` / `feedbackWarning` / `feedbackError` / `feedbackInfo` × `bgBase`
- `brandDefault` × `bgBase` (large text apenas — link/destaque)

Se algum falha: voltar ao Step 5, ajustar L/C do role ofensor, revalidar. **Não releasar palette com WCAG-fail em par obrigatório.**

### Step 7 — Anti-AI-slop checklist final

Antes de commitar, **leia e percorra `references/slop-patterns.md`** — ele carrega o checklist completo (cor + tipografia + execução) com cada item ticável. Não pular: a maior parte dos AI-slop incidents pega na lista de cor ("não é purple-blue gradient", "tem cor inesperada", "dark não é só inverso do light").

### Step 8 — Emitir artefatos

Saída completa da skill deve conter:

1. **Mood board verbal** (Step 1 recap) com Differentiation explícita.
2. **Rationale por role** — por que essa hue/L para cada token (mínimo: brand, bgBase, textPrimary, feedback × 4, gameAccent).
3. **Tabela de contraste** — 24 pares com ratios reais.
4. **Snippet Dart** — `AppColors.<themeName>` (light) + `AppColors.dark<ThemeName>` (dark) prontos para paste, seguindo o shape do `app_colors.dart` atual (29 fields).
5. **Atualização para `docs/design-tokens.md`** (se substitui o tema atual) — diff ou seção nova.
6. **Ficha de referência** em `docs/themes/<theme-name>.md` (Step 8.5 abaixo).
7. **Diff conceitual vs tema atual** — o que muda, o que mantém.
8. **Plano de rollout** — substitui ou coexiste (feature flag, rota específica, `ThemeData` alternativo).

#### Step 8.5 — Ficha de referência em `docs/themes/`

Para cada palette criada, gerar `docs/themes/<theme-name>.md` seguindo o template em `references/slop-patterns.md` § "docs/themes ficha template" (campos obrigatórios: descrição evocativa, palette light, palette dark, typography, "Best used for", "Anti-patterns evitados", "Inspiração"). Os dois últimos campos forçam rastreio anti-slop e são não-opcionais.

### Step 9 — Implementação

**Dois caminhos de rollout:**

#### 9a. Substituir o tema atual

Editar `lib/core/theme/app_colors.dart` trocando os valores de `AppColors.navyBlue` e/ou `AppColors.darkBlue` (são os dois `static const` atuais). Impacto: todo app. Precedido de audit completo + review visual screen-by-screen.

```dart
static const AppColors navyBlue = AppColors(
  bgBase:          Color(0xFF...),
  bgSurface:       Color(0xFF...),
  // ... 29 tokens
);
```

#### 9b. Tema alternativo coexistente (recomendado para sub-brand / sazonal)

Adicionar uma terceira instância `static const` no mesmo `AppColors` e trocar o `themeMode` no `MaterialApp.router` ou aplicar via `Theme(data: ..., child: ...)` em rotas específicas:

```dart
// Em app_colors.dart
static const AppColors arenaNeon = AppColors(
  bgBase:    Color(0xFF...),
  // ... 29 tokens com identidade Arena
);

// Em app_theme.dart
static ThemeData arenaNeon({FontScale scale = FontScale.normal}) {
  // ... clone de navyBlue() trocando .extensions
}

// Em app_router.dart, rota específica:
ShellRoute(
  builder: (_, __, child) => Theme(
    data: AppTheme.arenaNeon(),
    child: child,
  ),
  routes: [/* arena routes */],
)
```

### Step 10 — Report final

- Snippet completo `AppColors.<name>` + `dark<Name>`.
- Ficha em `docs/themes/<name>.md` criada.
- Atualização de `docs/design-tokens.md` (caso substitua) ou link para a ficha (caso coexista).
- `flutter analyze` verde.
- **Sugestão obrigatória**: `/theme-audit` global para ver impacto em todas as features.

## Anti-patterns

- ❌ Criar palette sem responder as 6 pré-condições (especialmente Differentiation).
- ❌ Usar HSL em vez de OKLCH para escala (hue-drift visível).
- ❌ Definir tokens sem validar WCAG nos 24 pares obrigatórios.
- ❌ Mesma palette light + dark (dark mode sempre precisa ajuste de L).
- ❌ Adicionar token novo no `/theme-create` — isso é escopo de `/theme-extend`.
- ❌ Seguir paletas curadas "Tech/SaaS profissional" sem adaptar — gera AI-slop direto.
- ❌ Copiar hex do Material Design guide sem diferenciar do default.
- ❌ Propor fonte Inter/Roboto/Space Grotesk sem alternativa de caráter.
- ❌ Pular a ficha em `docs/themes/` — sem documentação não há rastreio anti-slop.

## Referência — palettes inspiracionais por mood

Para a tabela domain-agnostic de hues por mood (energia, confiança, sofisticação, etc.) e como nomear o resultado pelo caráter (não pelo hue), leia `references/slop-patterns.md` § "Inspirational palettes by mood".

## Integração

| Antes | Skill | Depois |
|-------|-------|--------|
| Design flagou necessidade de sub-brand | `/theme-create` | Coexiste via 3ª instância em `AppColors` |
| Refresh total de identidade | `/theme-create` | Substitui `AppColors.navyBlue` → `/theme-audit` global |
| Só precisa resolver contraste | NÃO use `/theme-create` — use `/theme-extend` |

Sempre terminar emitindo um `/theme-audit` sugerido para a rota/feature afetada.
