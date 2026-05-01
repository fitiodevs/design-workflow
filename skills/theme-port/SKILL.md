---
name: theme-port
license: Complete terms in LICENSE.txt
description: Porta um frame do Figma OU HTML do Stitch para widgets Flutter Fitio. Source fornece SOMENTE estrutura (widths, heights, radii, spacing, hierarquia de texto); cores e fontes vêm do tema (light/dark + A/A+/A++). Use quando o usuário pedir para implementar/portar/migrar um frame ou tela ("porta esse frame", "implementa a tela X do figma", "/theme-port", "/figma-port", "/theme-port --from-stitch <html>").
triggers:
  - /theme-port
  - /figma-port
  - /Arquiteto
  - /arquiteto
  - porta(r)? (esse|este|o) frame
  - implementa(r)? (a tela|a feature|o design) .* figma
  - migra(r)? .* figma .* flutter
  - --from-stitch
---

# Skill: fitio-theme-port (`/theme-port`) — persona **Arquiteto**

Lê um frame Figma **ou HTML do Stitch** e produz Flutter widget usando **tokens existentes** do `AppColors` / `AppSpacing` / `AppRadius` / `TextTheme`. Filosofia: **source = wireframe P&B**. Estrutura da source, identidade do tema.

**Dois modos de input:**

| Modo | Trigger | Source |
|---|---|---|
| Figma | `/theme-port` (default) | figma-bridge MCP |
| Stitch | `/theme-port --from-stitch <html>` | HTML local (gerado por `/theme-sandbox`) |

Ambos seguem o mesmo pipeline Step 2–7. Só o Step 1 muda.

Esta skill é a **entrada** no ciclo. Após portar, o fluxo natural é:

```
/theme-port   →  /theme-audit   →  /theme-extend   (→ /theme-create, se algo novo)
   (lê)           (avalia)         (melhora)          (cria do zero)
```

Ao terminar o port, **sempre** sugira rodar `/theme-audit` na feature recém-portada para validar cobertura e detectar violações residuais.

## Prerequisites

- **`docs/product.md` carregado.** Source of truth de tom, anti-references, scene sentence, color strategy axis. Se ausente/vazio (<2KB), parar e pedir ao usuário criar antes de portar — sem isso o port cai em category-reflex (verde Strava, preto+laranja Nike). Não sintetizar tom a partir do prompt.
- **Modo Figma:** MCP `figma-bridge` conectado. Se `claude mcp list` mostrar ✗, pedir o usuário abrir o Figma em figma-linux e rodar `Plugins → Development → Claude Figma Bridge`. Tools figma-bridge são deferred. Antes da primeira chamada: `ToolSearch` com `select:mcp__figma-bridge__get_selection,mcp__figma-bridge__get_design_context,mcp__figma-bridge__get_node,mcp__figma-bridge__get_screenshot,mcp__figma-bridge__save_screenshots`.
- **Modo Stitch:** path do HTML local existe. Tipicamente `.claude/handoffs/atelier-cache/<ts>/<variation>.html` gerado por `/theme-sandbox`. Sem MCP — só Read.

## Inputs

**Modo Figma (default):**
- **Sem argumento** → lê seleção atual via `get_selection`.
- **Node ID** (`1:234`) → passa para `get_node` / `get_design_context`.
- **Figma URL** → extrai `node-id`, normaliza `-` → `:`.
- **Descrição natural** ("a tela de check-in") → pede para selecionar no Figma, depois segue com `get_selection`.

**Modo Stitch:**
- **`--from-stitch <html-path>`** → lê HTML local. Se path for diretório, listar `*.html` e pedir escolha. Se input for handoff atelier YAML, ler `variations[].cached_at` correspondente.
- **`--from-stitch <html-path> target=<lib-path>`** → declara onde escrever o widget Flutter (path da feature).

## Workflow

### Step 1 — Capture frame

**Modo Figma (default):**

1. Determinar frame alvo pelas regras de Inputs.
2. `mcp__figma-bridge__get_design_context` com `depth: 4`. Salvar árvore estrutural.
3. `mcp__figma-bridge__get_screenshot` em `scale: 1` para referência visual.
4. **NÃO** chamar `get_variable_defs` nem `get_styles`. Tokens do Figma são ignorados — tema é source of truth.

**Modo Stitch (`--from-stitch`):**

1. Read do HTML local. Se path foi handoff atelier YAML, resolver `variations[].cached_at` correspondente; se foi diretório, listar `*.html` e perguntar.
2. Read do `.png` irmão (mesmo basename) pra referência visual — Stitch sempre exporta os dois lado a lado em `atelier-cache/<ts>/`.
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
   - SVGs decorativos sem semântica (placeholders Stitch). Manter só ícones com label.

5. **Mapeamento Tailwind → escala Fitio (referência):**

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
- **Border radius**: snap para `AppRadius.{sm:6, md:10, lg:14, xl:20, pill:999}`. Se Figma estiver >2px de todo token, reportar ao usuário.
- **Padding / gap**: snap para `AppSpacing.{xxs:2, xs:4, sm:8, md:12, lg:16, xl:20, xxl:24, xxxl:32, huge:48}`. Mesma regra.
- **Texto**: capturar ordem relativa de font-size (maior → menor) no frame. Mapear para roles semânticos (tabela abaixo). **Nunca** copiar `fontSize` / `fontWeight` literal.

| Role                          | Uso                               | Base |
|-------------------------------|-----------------------------------|-----:|
| `displayLarge/Medium/Small`   | Hero numérico, splash             | 57/45/36 |
| `headlineLarge/Medium/Small`  | Títulos de página                 | 32/28/24 |
| `titleLarge/Medium/Small`     | Títulos de card/seção/AppBar      | 22/18/16 |
| `bodyLarge/Medium/Small`      | Texto corrido                     | 16/14/12 |
| `labelLarge/Medium/Small`     | Botão, chip, caption              | 14/12/11 |

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

Antes de escrever, mapear para design system (`lib/core/widgets/widgets.dart`):

- Tap target com label → `AppButton(variant: primary|secondary|ghost|danger|social)`.
- Input → `AppTextField`.
- **2+ inputs no mesmo bloco lógico → `AppFormGroup`** (regra do Fitio, ver abaixo).
- Card → `Card` com defaults do tema.
- Scaffold completo → `AppScaffold` + `AppAppBar`.
- Estado vazio → `AppEmptyState`.
- Loading → `AppLoading` / `AppSkeleton`.
- Feedback → `AppSnackbar.show` / `AppDialog.confirm`.

Custom só se nenhum component cobre. Coloca em `lib/features/<feature>/presentation/widgets/`.

#### Regra: agrupamento de inputs (`AppFormGroup`)

**Sempre que houver 2+ campos de formulário** (`AppTextField`, dropdown, toggle) que pertencem ao mesmo bloco lógico, envolva em `AppFormGroup`. O resultado visual é **um único card bordado com os campos empilhados separados por dividers** (mesma anatomia de `ProfileSectionContainer` em Configurações).

Spec do `AppFormGroup`:
- `bgSurface` como fill,
- `borderDefault` como contorno externo E como cor dos dividers (token de tema — adapta light/dark automaticamente),
- `AppRadius.lg`,
- sem padding vertical no container; cada filho controla a própria altura via `bare`.

**Os filhos devem usar `AppTextField(bare: true)`** — modo sem outline/fill próprio, padding vertical 14px, hint em `bodyLarge/textSecondary`. Isso evita borda dupla e garante que o card seja a única moldura visível.

```dart
AppFormGroup(
  children: [
    AppTextField(hint: 'Nome', bare: true, controller: nomeCtrl),
    AppTextField(hint: 'Email', bare: true, controller: emailCtrl),
    AppTextField(hint: 'CPF', bare: true, controller: cpfCtrl),
    AppTextField(hint: 'Data de nascimento', bare: true, controller: dataCtrl),
  ],
)
```

Visualmente:
```
┌─────────────────────────┐
│  Nome                   │
├─────────────────────────┤
│  Email                  │
├─────────────────────────┤
│  CPF                    │
├─────────────────────────┤
│  Data de nascimento     │
└─────────────────────────┘
```

**Exceções:**
- 1 campo só → `AppTextField` solto (modo padrão com outline próprio), sem wrapper.
- Campos de seções diferentes (ex: "Dados pessoais" + "Endereço") → 2 `AppFormGroup` separados, cada um com seu título via `ProfileSectionTitle` ou equivalente.
- Input solto fora de form (ex: search bar, single comment) → `AppTextField` padrão (não `bare`).
- **Não** combinar `bare: true` com `prefixIcon` — o ícone fica visualmente desconectado da row. Se precisa de ícone, use o modo padrão num input solto, fora do `AppFormGroup`.

### Step 5 — Implement

- Path: `lib/features/<feature>/presentation/{pages,widgets}/`.
- Import: `package:fitio/core/widgets/widgets.dart`.
- Texto: `Theme.of(context).textTheme.<role>` (ou `context.cappedTextTheme.<role>` para elementos fixos — pills, tabs, badges, texto descritivo de "Cupom disponível" e "Sobre").
- Cores: `context.colors.<role>`.
- Spacing/Radius: `AppSpacing.<t>` / `AppRadius.<t>`.
- Sizes (w/h literal) OK — são estruturais.
- Copy pt-BR; identifiers em inglês.

**Elementos que DEVEM usar `cappedTextTheme` (cap A+):**
Badges, pills, tabs de navegação inferior, títulos de navbar (MARKETPLACE/CUPONS/ARENA), label "Cupom disponível", texto Sobre do patrocinador, chips de status, selo "Grátis", rótulos de ponto/pontos.

### Step 6 — Validate

```bash
flutter analyze
```

Deve retornar `No issues found!`. Se `@freezed` foi tocado: `dart run build_runner build --delete-conflicting-outputs`.

### Step 7 — Report

Terminar com relatório curto:
- Arquivos criados/editados.
- Tokens reutilizados (lista curta).
- **Qualquer fill que não encaixou em token existente** — flag explícito.
- Desvios de radius/spacing fora da escala.
- **Sugestão do próximo passo**: `/theme-audit lib/features/<feature>` para validar cobertura.

## Anti-patterns

- ❌ Hex literal `Color(0xFF...)` em widget.
- ❌ `fontSize:` ou `fontWeight:` literal em widget.
- ❌ Importar Figma Variables via `get_variable_defs`.
- ❌ Copiar Tailwind classes literal (`bg-blue-500`, `text-#FFF`) — descartar, não traduzir cor.
- ❌ Copiar texto em inglês do Stitch — Stitch gera EN; copy final é pt-BR (do handoff Júri / product.md §4).
- ❌ Portar SVG decorativo placeholder do Stitch. Manter só ícone com role semântico.
- ❌ Criar token novo direto aqui — isso é job do `/theme-extend`.
- ❌ Pular `flutter analyze` antes de reportar done.
- ❌ Rodar port modo Figma sem figma-bridge conectado — não chuta o design.
- ❌ Rodar port modo Stitch sem ler o `.png` irmão — texto puro do HTML perde proporção.
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
