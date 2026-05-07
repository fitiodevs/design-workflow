---
name: theme-port
description: Ports a structural source (Figma frame OR HTML mockup from any tool — frontend-design, Figma export, Sketch, Penpot, Stitch, hand-written) into Flutter widgets in your project. The source provides ONLY structure (widths, heights, radii, spacing, text hierarchy); colors and fonts come from your theme (light/dark plus A/A+/A++ font scale). Use when the user asks for `/Architect`, `/Arquiteto`, `/theme-port`, `/figma-port`, `/theme-port --from-html` plus an HTML path, "porta esse frame", "implement that frame from Figma", "convert this mockup to Flutter", or "migrate from Figma to Flutter".
metadata:
  dw:
    craft:
      requires: [state-coverage, typography, design-context]
---

# Skill: theme-port (`/theme-port`) — persona **Arquiteto** (English: **Architect**)

## Triggers

- **English:** `/Architect`, `/theme-port`, `/figma-port`, `/theme-port --from-html`, "port this frame", "implement design from Figma", "convert this HTML mockup to Flutter", "migrate Figma to Flutter"
- **Português:** `/Arquiteto`, `/arquiteto`, `/theme-port`, `/figma-port`, "porta esse frame", "implementa a tela X", "converte esse mockup pra Flutter", "migra do figma pro flutter"
- **Natural language:** Figma URL/node-id; HTML mockup path; "build the screen from this design"

Lê uma fonte estrutural (Figma frame **ou** HTML mockup de qualquer origem) e produz Flutter widget usando **tokens existentes** do `AppColors` / `AppSpacing` / `AppRadius` / `TextTheme`. Filosofia: **source = wireframe P&B**. Estrutura da source, identidade do tema.

**Dois modos de input:**

| Modo | Trigger | Source |
|---|---|---|
| Figma | `/theme-port` (default) | figma-bridge MCP |
| HTML | `/theme-port --from-html <path>` | qualquer arquivo `.html` (frontend-design / Clara, export de Figma/Sketch/Penpot, Stitch, hand-written) |

Ambos seguem o mesmo pipeline Step 2–7. Só o Step 1 muda.

Esta skill é a **entrada** no ciclo. Após portar, o fluxo natural é:

```
/theme-port   →  /theme-audit   →  /theme-extend   (→ /theme-create, se algo novo)
   (lê)           (avalia)         (melhora)          (cria do zero)
```

Ao terminar o port, **sempre** sugira rodar `/theme-audit` na feature recém-portada para validar cobertura e detectar violações residuais.

## Craft references

Before porting, read these craft references — they encode universal rules independent of any project:

- `craft/state-coverage.md` — every interactive surface needs default/hover/focus/active/disabled/loading/empty/error states. The source rarely shows them all; infer the missing ones from these rules.
- `craft/typography.md` — type scale, line height, letter spacing. Use to map source font sizes to your `TextTheme` semantic roles instead of porting raw px values.

These are upstream from any project's design system; the project's own tokens (`AppColors`, `docs/product.md`) override only when they explicitly contradict.

## Prerequisites

- **`docs/product.md` carregado.** Source of truth de tom, anti-references, scene sentence, color strategy axis. Se ausente/vazio (<2KB), parar e pedir ao usuário criar antes de portar — sem isso o port cai em category-reflex (verde Strava, preto+laranja Nike). Não sintetizar tom a partir do prompt.
- **Modo Figma:** MCP `figma-bridge` conectado. Se `claude mcp list` mostrar ✗, pedir o usuário abrir o Figma em figma-linux e rodar `Plugins → Development → Claude Figma Bridge`. Tools figma-bridge são deferred. Antes da primeira chamada: `ToolSearch` com `select:mcp__figma-bridge__get_selection,mcp__figma-bridge__get_design_context,mcp__figma-bridge__get_node,mcp__figma-bridge__get_screenshot,mcp__figma-bridge__save_screenshots`.
- **Modo HTML:** path do arquivo `.html` existe. Sem MCP — só `Read`. Screenshot irmão (`.png` com mesmo basename) é opcional mas recomendado quando disponível — ajuda a calibrar proporção de elementos cuja largura/altura não está explícita no HTML.

## Inputs

**Modo Figma (default):**

- **Sem argumento** → lê seleção atual via `get_selection`.
- **Node ID** (`1:234`) → passa para `get_node` / `get_design_context`.
- **Figma URL** → extrai `node-id`, normaliza `-` → `:`.
- **Descrição natural** ("a tela de check-in") → pede para selecionar no Figma, depois segue com `get_selection`.

**Modo HTML (`--from-html`):**

- **`--from-html <path>`** → lê o `.html` apontado. Se path for diretório, listar `*.html` e perguntar qual.
- **`--from-html <path> target=<lib-path>`** → declara onde escrever o widget Flutter (path da feature).
- **Screenshot pair (opcional):** se existir `<basename>.png` ao lado do `.html`, ler também — referência visual ajuda em casos onde a largura/altura literal não está nos atributos.

## Pre-flight context check

Before generating, verify Tier 1–4 context exists per `craft/design-context.md`. Concrete checks for theme-port:

- **Tier 1** — `lib/core/theme/app_colors.dart` exists and has >50 lines? (the 29-role token system must be in place to map fills semantically)
- **Tier 2** — at least one similar widget exists in `lib/features/<related>/`? (matching coherent precedent keeps the system together)
- **Tier 3** — screenshots in `docs/screenshots/` or deployed product reachable? (optional fallback when codebase is contractor-blind)
- **Tier 4** — `docs/product.md` exists and has §Tone with declared adjectives + banned phrases? (required for copy + microcopy decisions)

If Tier 1 missing → STOP. Without `AppColors` there are no semantic roles to map; emitting raw hex re-introduces the slop. Ask the user to seed the palette via `/theme-create` first.

If Tier 4 missing → STOP. Without declared tone, copy in the ported widget will be category-reflex ("Eleve seu jogo", "Sua jornada começa"). Ask the user to seed `docs/product.md` §Tone before proceeding (5 minutes; the doc lists the 4–7 questions).

The decision rule is binary — STOP, not "ideally check". See `craft/design-context.md` §"The decision rule".

## Workflow

### Step 1 — Capture frame

**Modo Figma (default):**

1. Determinar frame alvo pelas regras de Inputs.
2. `mcp__figma-bridge__get_design_context` com `depth: 4`. Salvar árvore estrutural.
3. `mcp__figma-bridge__get_screenshot` em `scale: 1` para referência visual.
4. **NÃO** chamar `get_variable_defs` nem `get_styles`. Tokens do Figma são ignorados — tema é source of truth.

**Modo HTML (`--from-html`):**

1. `Read` do HTML local. Se path for diretório, listar `*.html` e perguntar qual.
2. Se existir um `.png` com mesmo basename ao lado, `Read` ele também — referência visual opcional pra calibrar proporção.
3. **Parser HTML** (sem dependências; regex/string ops bastam pra extrair estrutura):

   | Extrair | De | Como |
   |---|---|---|
   | Widths/heights | `style="width:Xpx; height:Ypx"` ou Tailwind `w-N`/`h-N` | px literal (estrutural) |
   | Border radius | `border-radius:Xpx` ou `rounded-N` | snap pra `AppRadius` (sm/md/lg/xl/pill) |
   | Padding/margin/gap | `padding:`, `gap:`, ou `p-N`/`m-N`/`gap-N` | snap pra `AppSpacing` |
   | Hierarquia de texto | `text-Nxl`/`text-Npx` | ordenar maior→menor → mapear roles (display/headline/title/body/label) |
   | Tipo de elemento | tag + role semântico | `<button>` → `AppButton`; `<input>` → `AppTextField`; `<header>` → `AppAppBar`; etc. |

4. **Descartar:**
   - Cores hex (`bg-blue-500`, `text-#FFF`, `style="color:#..."`) — wireframe-only.
   - `font-family` — tema cuida.
   - `box-shadow` — só anota presença/ausência; valor vem do tema.
   - `transition`, `hover:`, animations — não portar.
   - SVGs decorativos sem semântica (placeholders comuns de geradores HTML). Manter só ícones com label.

5. **Tailwind → project spacing/radius scale (reference):**

   | Tailwind | Aprox px | AppSpacing |
   |---|---|---|
   | `p-1`/`gap-1` | 4 | xs |
   | `p-2` | 8 | sm |
   | `p-3` | 12 | md |
   | `p-4` | 16 | lg |
   | `p-5` | 20 | xl |
   | `p-6` | 24 | xxl |
   | `p-8` | 32 | xxxl |
   | `p-12` | 48 | huge |

   | Tailwind | Aprox px | AppRadius |
   |---|---|---|
   | `rounded-sm` | 6 | sm |
   | `rounded-md` | 10 | md |
   | `rounded-lg` | 14 | lg |
   | `rounded-xl`/`rounded-2xl` | 20 | xl |
   | `rounded-full` | 999 | pill |

   Se distância >2px de qualquer token, reportar ao usuário (mesma regra do modo Figma).

6. Salvar árvore estrutural normalizada (mesmo formato do Step 2 do modo Figma) — daí o pipeline converge.

### Step 2 — Extract structure

Para cada container/leaf extrair:

- **Width / height**: px literal (são estruturais).
- **Border radius**: snap para `AppRadius.{sm:6, md:10, lg:14, xl:20, pill:999}`. Se source estiver >2px de todo token, reportar ao usuário.
- **Padding / gap**: snap para `AppSpacing.{xxs:2, xs:4, sm:8, md:12, lg:16, xl:20, xxl:24, xxxl:32, huge:48}`. Mesma regra.
- **Texto**: capturar ordem relativa de font-size (maior → menor) no frame. Mapear para roles semânticos. **Nunca** copiar `fontSize` / `fontWeight` literal. Para a tabela completa de roles + bases + regras de hierarquia (ratio adjacente ≥1.25, anchor único, `cappedTextTheme` para layout fixo), leia `references/text-hierarchy.md`.

### Step 3 — Identify color semantic roles

Para cada fill/stroke/shadow:

1. **Inferir** o papel semântico. Tokens disponíveis em `lib/core/theme/app_colors.dart` (29 tokens em 7 grupos):
   - **Backgrounds**: `bgBase`, `bgSurface`, `bgSurfaceRaised`, `bgInput`, `bgSkeleton`, `bgOverlay`
   - **Brand / Ação**: `brandDefault`, `brandMuted`, `brandOnColor`, `brandPressed`, `brandDisabled`
   - **Texto**: `textPrimary`, `textSecondary`, `textMuted`, `textOnBrand`
   - **Bordas**: `borderDefault`, `borderStrong`, `borderFocus`
   - **Feedback**: `feedbackSuccess`/`feedbackSuccessMuted`, `feedbackWarning`/`feedbackWarningMuted`, `feedbackError`/`feedbackErrorMuted`, `feedbackInfo`/`feedbackInfoMuted`
   - **Gamificação**: `gameAccent`, `gameAccentMuted`, `gameAccentOnColor`

   **Badges**: `context.badgeColors.<status><Bg|Text|Border>` (8 status × 3 propriedades, derivado de `feedbackXxx`).

2. `AppBrandColors` foi **eliminado** (refator NavyBlue). Não use `context.brandColors.<x>` — todo acesso via `context.colors.<token>`.

3. Se **nenhum token existente encaixa**: **NÃO inventar hex no widget.** Parar e sugerir `/theme-extend` para adicionar o role, OU pedir confirmação ao usuário antes de adicionar.

4. **Proibido**: `Color(0xFF...)` em widget. Todo acesso via `context.colors.<token>` ou `context.badgeColors.<x>`.

### Step 4 — Widget composition

Antes de escrever código, mapear cada elemento da source para um component do design system (`AppButton`, `AppTextField`, `AppFormGroup`, `AppScaffold`, `AppAppBar`, `AppEmptyState`, `AppSnackbar`, `AppDialog`, etc). Para a tabela completa source → component + a regra de agrupamento de inputs (`AppFormGroup` com filhos `AppTextField(bare: true)`, exceções e anti-patterns como combinar `bare: true` com `prefixIcon`), leia `references/widget-mapping.md` antes de compor.

Custom só se nenhum component cobre. Coloca em `lib/features/<feature>/presentation/widgets/`.

### Step 5 — Build Adapter Plan

Em vez de escrever Dart diretamente, emit um **Adapter Plan** (formato neutro entre stacks). O Plan é um JSON conforme `docs/adapter-plan.schema.json`:

```json
{
  "version": "1.0",
  "kind": "widget-tree",
  "meta": {"feature": "<feature-slug>"},
  "widgets": [
    {"type": "form-group", "variant": "stacked", "size": "md",
     "props": {"title": "..."}, "children": [/* ... */]}
  ],
  "actions": [
    {"op": "write", "role": "widget-tree", "intent": "component", "name": "MilestoneCta"}
  ]
}
```

Salvar em `/tmp/<feature>-plan.json`. Esse arquivo é o **único artefato direto da skill** — toda emissão de código é responsabilidade do adapter.

Token roles (cores/spacing/radius/typography) **continuam sendo decididos aqui** (Step 3 / Step 4) — o Plan os referencia por nome canônico (ex: `brandDefault`, `bgSurface`). O adapter resolve para a sintaxe da stack ativa (`context.colors.brandDefault` em Flutter, `var(--brand-default)` em Tailwind).

Copy pt-BR; identifiers em inglês — independe do stack.

### Step 6 — Resolve active stack

Resolução em ordem (executar via Bash) — `STACK` env var → `.design-workflow.yaml` `stack:` field → `flutter`:

```bash
STACK=$(python3 scripts/resolve_stack.py)   # STACK env > config.stack > "flutter"
```

Se `resolve_stack.py` falhar (stack desconhecido), parar e reportar — não chutar.

### Step 7 — Render via adapter

```bash
python3 adapters/$STACK/adapter.py /tmp/<feature>-plan.json
```

O adapter consume o Plan, renderiza via templates, escreve nos paths convencionais:

- **flutter:** `lib/features/<feature>/presentation/widgets/<name>.dart` + atualiza `lib/core/theme/app_colors.dart` se kind=palette.
- **nextjs-tailwind:** `components/<feature>/<name>.tsx` + atualiza `app/globals.css` (App Router) ou `styles/tokens.css` (Pages) se kind=palette.

### Step 7.5 — Verify outputs

Confirmar que cada `action` do Plan resultou num arquivo no path esperado. Listar paths absolutos no relatório (Step 9).

### Step 8 — Validate per stack

| Stack | Comando | Esperado |
|---|---|---|
| `flutter` | `flutter analyze` | `No issues found!` (rodar `dart run build_runner build` se `@freezed` foi tocado) |
| `nextjs-tailwind` | `npx tsc --noEmit && npx eslint <component-path>` | exit 0 |

Se a validação falhar, **não reportar done** — fix-and-retry ou escalar para o usuário.

### Step 9 — Report

Terminar com relatório curto:
- Stack resolvido (`flutter` / `nextjs-tailwind`).
- Plan emitido em `/tmp/<feature>-plan.json` (anexar ao relatório).
- Arquivos criados/editados pelo adapter (output de Step 7).
- Tokens reutilizados (lista curta).
- **Qualquer fill que não encaixou em token existente** — flag explícito.
- Desvios de radius/spacing fora da escala.
- **Sugestão do próximo passo**: `/theme-audit lib/features/<feature>` (Flutter) ou `/theme-audit components/<feature>` (Next.js) para validar cobertura.

**Elementos que DEVEM usar `cappedTextTheme` (cap A+, Flutter only):**
Badges, pills, bottom-nav tabs, navbar section titles, status chips, short label/caption text, point/score labels — anything where uncapped scaling at A++ would break the fixed layout. (Sem equivalente direto em Tailwind; resolvido via `clamp()` quando o adapter Next.js implementar typography em v1.3+.)

## Anti-patterns

- ❌ Hex literal `Color(0xFF...)` em widget.
- ❌ `fontSize:` ou `fontWeight:` literal em widget.
- ❌ Importar Figma Variables via `get_variable_defs`.
- ❌ Copiar Tailwind classes literal (`bg-blue-500`, `text-#FFF`) — descartar, não traduzir cor.
- ❌ Copiar texto em inglês do source — copy final é pt-BR (do handoff Júri / `docs/product.md` §4); se o HTML veio de gerador EN-only, traduzir.
- ❌ Portar SVG decorativo placeholder do source. Manter só ícone com role semântico.
- ❌ Criar token novo direto aqui — isso é job do `/theme-extend`.
- ❌ Pular `flutter analyze` antes de reportar done.
- ❌ Rodar port modo Figma sem figma-bridge conectado — não chuta o design.
- ❌ Rodar port sem `docs/product.md` — copy/tom cai em filler/vocativo cliché.
- ❌ Esquecer `cappedTextTheme` em elementos de layout fixo.
- ❌ Usar copy slop (banidos em `docs/product.md` §4.2: "Eleve seu jogo", "Jornada fitness", "atleta!", "campeão!") em strings hardcoded.

## Referência rápida — tokens

| Categoria | Arquivo | Acesso |
|-----------|---------|--------|
| Cores semânticas (29 tokens) | `lib/core/theme/app_colors.dart` | `context.colors.<token>` |
| Badge colors (8 status) | `lib/core/theme/app_colors.dart` (`AppBadgeColors`) | `context.badgeColors.<status><Bg\|Text\|Border>` |
| Typography (FontScale A/A+/A++) | `lib/core/theme/app_typography.dart` | `Theme.of(context).textTheme.<role>` |
| Typography (cap A+) | `lib/core/theme/capped_text_theme.dart` | `context.cappedTextTheme.<role>` |
| Spacing | `lib/core/theme/app_spacing.dart` | `AppSpacing.<t>` |
| Radius | `lib/core/theme/app_spacing.dart` | `AppRadius.<t>` |

**Mapeamento OLD → NEW** (caso encontre código pré-refactor): `card→bgSurface`, `border→borderDefault`, `surface→bgBase`, `surfaceVariant→bgInput`, `skeleton→bgSkeleton`, `brand→brandDefault`, `success→feedbackSuccess`, `danger→feedbackError`, `info→feedbackInfo`, `warning→feedbackWarning`, `overlay→bgOverlay`, `textInverted→textOnBrand`. `context.brandColors.*` foi eliminado — substitua por `context.colors.brandDefault` ou `gameAccent` conforme o caso.

## figma-bridge MCP quick reference

| Tool | Uso |
|------|-----|
| `get_selection` | Seleção atual (entry point default) |
| `get_node` | Fetch por ID |
| `get_design_context` | Árvore estrutural com depth |
| `get_screenshot` | PNG/SVG base64 |
| `save_screenshots` | Exportar pra filesystem |
| `get_metadata` | File/page info |

Prefira `get_design_context` (menor) sobre `get_document`.
