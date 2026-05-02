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

### Step 5 — Montar pares light + dark dos 29 tokens

O sistema atual (`lib/core/theme/app_colors.dart`) tem **29 tokens em 7 grupos**. Cada um precisa de par light + dark validado.

Tabela de targets por categoria (L = lightness OKLCH, C = chroma):

#### Backgrounds (6 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `bgBase` | 0.96-0.98 | 0.07-0.10 | Page bg, off-white/off-black |
| `bgSurface` | 0.99-1.00 | 0.11-0.14 | Cards, modais, elevado |
| `bgSurfaceRaised` | 0.99-1.00 | 0.11-0.14 | Igual ou +0.01 vs surface |
| `bgInput` | 0.93-0.96 | 0.16-0.19 | Field fill, mais escuro que surface |
| `bgSkeleton` | 0.90-0.93 | 0.17-0.20 | Loading shimmer base |
| `bgOverlay` | rgba(0,0,0,0.6) | rgba(0,0,0,0.6) | Modal scrim, geralmente igual |

#### Brand / Ação (5 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `brandDefault` | 0.30-0.45 | 0.30-0.50 | Pode manter mesma hue/L ou clarear no dark |
| `brandMuted` | 0.92-0.96 | 0.18-0.25 | Bg de chip selecionado, low-sat |
| `brandOnColor` | 0.99-1.00 | 0.99-1.00 | Texto/ícone sobre brand — quase sempre branco |
| `brandPressed` | 0.22-0.30 | 0.55-0.70 | -0.08 do default no light, +0.20 no dark |
| `brandDisabled` | 0.65-0.78 | 0.30-0.40 | Mid, baixa sat, sem WCAG (decorativo) |

#### Texto (4 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `textPrimary` | 0.08-0.18 | 0.95-1.00 | Max contraste, ~21:1 |
| `textSecondary` | 0.30-0.45 | 0.65-0.78 | WCAG AA mín 4.5:1 sobre `bgBase` |
| `textMuted` | 0.50-0.60 | 0.50-0.62 | Captions, helper — AA opcional (small text) |
| `textOnBrand` | 0.99-1.00 | 0.99-1.00 | Branco/quase, contraste sobre `brandDefault` |

#### Bordas (3 tokens)

| Token | Light L | Dark L | Regra |
|-------|--------:|-------:|-------|
| `borderDefault` | 0.86-0.92 | 0.20-0.28 | Card stroke, divider |
| `borderStrong` | 0.74-0.80 | 0.30-0.38 | Outlined input, ênfase |
| `borderFocus` | = `brandDefault` | = `brandDefault` (light) ou variante saturada | Sempre igual ao brand do tema |

#### Feedback semântico (8 tokens — cada um tem `<x>` + `<x>Muted`)

Hue alvo por papel:

| Papel | Hue OKLCH | Light L (cor) | Dark L (cor) | Light L (Muted) | Dark L (Muted) |
|-------|----------:|--------------:|-------------:|----------------:|---------------:|
| `feedbackSuccess` | ~140-150 | 0.50-0.58 | 0.78-0.85 | 0.93-0.96 | 0.18-0.22 |
| `feedbackWarning` | ~65-80 | 0.55-0.65 (não usar amarelo puro — falha AA) | 0.85-0.92 | 0.93-0.96 | 0.16-0.20 |
| `feedbackError` | ~25-30 | 0.50-0.58 | 0.65-0.72 | 0.92-0.96 | 0.16-0.20 |
| `feedbackInfo` | ~245-260 | 0.45-0.55 | 0.70-0.80 | 0.92-0.96 | 0.13-0.18 |

Validar AA (4.5:1) de cada cor sobre `bgBase` em ambos os modos. `*Muted` não precisa AA (é background de badge).

#### Gamificação (3 tokens)

| Token | Light | Dark | Regra |
|-------|-------|------|-------|
| `gameAccent` | hue 35-45, alto C | mesmo ou +0.05 L | Âmbar/dourado/neon decorativo — sem WCAG |
| `gameAccentMuted` | L 0.92-0.96 | L 0.16-0.22 | Bg de badge gamificado |
| `gameAccentOnColor` | L 0.20-0.30 | L 0.85-0.92 | Texto sobre `gameAccent` se aplicável |

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

Antes de commitar, passar por todos os checks:

**Cor**
- [ ] NÃO é purple+blue gradient padrão (`#6366F1` → `#8B5CF6`).
- [ ] NÃO é orange+teal (`#F97316` + `#14B8A6`).
- [ ] NÃO usa defaults do Tailwind/Material direto sem modificação.
- [ ] Inspiração rastreável a algo real (brand existente, fotografia, cultura específica).
- [ ] Tem pelo menos UMA cor "inesperada" que distingue do domínio padrão.
- [ ] Saturação varia entre roles (não todos high-sat, não todos muted).
- [ ] `bgBase` não é `#FFFFFF` puro nem `#000000` puro.
- [ ] Dark mode tem personalidade — não é só inversão de light.
- [ ] Distribuição é dominante+accent, não evenly-distributed.

**Tipografia (caso a palette inclua proposta de fonte)**
- [ ] NÃO é Inter, Roboto, Arial, Helvetica, Space Grotesk, ou system-ui como fonte principal.
- [ ] Display font tem caráter (serif com swash, geometric com idiossincrasia, mono opinionada).
- [ ] Body font legível em 12-16px no dispositivo (não só em desktop).
- [ ] `fontFamilyFallback` declarado (cobre quando a fonte custom não carrega).

**Execução**
- [ ] Implementação combina com a tone declarada (minimal não tem 9 cores, maximalist não tem 3).
- [ ] Differentiation declarada no Step 0 está visualmente expressa em pelo menos 1 token.

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

Para cada palette criada, gerar `docs/themes/<theme-name>.md` no formato:

```markdown
# <Theme Name>

<Uma frase de descrição evocativa — 10-20 palavras.>

## Color Palette (light)

- **<Token role>** (`<TokenName>`): `#XXXXXX` — <papel em uma frase>
- **<Token role>**: `#XXXXXX` — <papel>
- **<Accent>**: `#XXXXXX` — <papel>
- **<Background>**: `#XXXXXX` — <papel>

## Color Palette (dark)

- **<mesma estrutura, hexes do dark>**

## Typography

- **Headers**: <font + fallback>
- **Body**: <font + fallback>

## Best Used For

<Frase descrevendo contextos onde esse tema brilha — ex: "Sub-brand competitivo da Arena, eventos de duelo, telas de leaderboard com energia visual alta.">

## Anti-patterns evitados

- <O que esse tema explicitamente NÃO faz — ex: "Não usa purple-on-white nem Inter, evitando tech-SaaS genérico.">

## Inspiração

<Referência rastreável real — ex: "Sinalização de pista de atletismo (lane lines amarelas + concrete cinza)", "Capa do álbum X de Y", "Bandeira de Z".>
```

Esse formato é navegável (vira tabela de conteúdo de `docs/themes/index.md`) e força documentação anti-slop (campos "Anti-patterns evitados" e "Inspiração" são obrigatórios).

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

## Referência — palettes inspiracionais por mood (domain-agnostic, não copiar)

Ponto de partida para inspecionar a hue ideal por mood pretendido. Nomear após o caráter, não o hue.

| Mood | Hue dominante | Saturação | Exemplo |
|------|---------------|-----------|---------|
| Energia / competição | 350-20 (vermelho/coral) ou 55-75 (amarelo) | Alta | Arena, corrida, duelo |
| Confiança / serenidade | 200-250 (azul) | Média | Healthcare, finance |
| Sofisticação / premium | 270-310 (roxo/magenta) ou neutros | Baixa | Luxo, assinatura |
| Natureza / saudável | 120-160 (verde) | Média-alta | Nutrição, bem-estar |
| Warmth / comunidade | 20-50 (laranja/âmbar) | Média | Social, indicação |
| Tech edge | 180-220 (ciano/azul) com dark base | Alta | Dev tools, power users |
| Editorial / printed | 0 + 1 saturated jewel | Baixa-média | Long-form, magazine |
| Brutalist / signage | 60 (yellow) + 0 (black) + concrete | Extrema | Industrial, hi-vis |

## Integração

| Antes | Skill | Depois |
|-------|-------|--------|
| Design flagou necessidade de sub-brand | `/theme-create` | Coexiste via 3ª instância em `AppColors` |
| Refresh total de identidade | `/theme-create` | Substitui `AppColors.navyBlue` → `/theme-audit` global |
| Só precisa resolver contraste | NÃO use `/theme-create` — use `/theme-extend` |

Sempre terminar emitindo um `/theme-audit` sugerido para a rota/feature afetada.
