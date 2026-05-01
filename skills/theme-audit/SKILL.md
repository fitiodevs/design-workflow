---
name: theme-audit
license: Complete terms in LICENSE.txt
description: Audita o uso do design system Fitio em `lib/`. Detecta hardcode de cores (`Color(0xFF...)`, `Colors.X`), fontSize/fontWeight literais, spacing/radius fora da escala, valida contraste WCAG das combinações semânticas atuais, e mede cobertura por feature. Também funciona como triagem por solicitação visual do usuário — aceita screenshot + descrição de problema visual e roteia para a skill correta. Use quando o usuário pedir auditoria do tema, reportar problema visual ("baixo contraste", "ícone fraco", "cor errada"), ou após `/theme-port` para validar o que foi portado.
triggers:
  - /theme-audit
  - /Lupa
  - /lupa
  - audita(r)? (o )?tema
  - revis(a|ar)? cobertura (do )?design system
  - viola(ç|c)(õ|o)es (de )?tema
  - verifica(r)? hardcode
  - (baixo|pouco) contraste
  - (ícone|icone).*(fraco|pequeno|desalinhado|errado|sumindo)
  - cor.*(errada|fraca|apagada|sumindo)
  - n(ã|a)o (usa|está usando) (o )?tema
---

# Skill: fitio-theme-audit (`/theme-audit`) — persona **Lupa**

Diagnostica saúde do design system. Dois eixos:

1. **Cobertura** — quantos widgets ainda usam hex/literal ao invés de tokens.
2. **Acessibilidade** — WCAG AA/AAA em cada combinação semântica, light + dark.

## Inputs

- **Sem argumento** → scan completo de `lib/`.
- **Path** (`lib/features/marketplace`) → escopo reduzido.
- **`--fail`** → exit code 1 se houver qualquer violação (útil em CI).
- **`--summary`** → só totais, sem lista arquivo-por-arquivo.
- **Solicitação visual** → usuário descreve o problema em linguagem natural (com ou sem screenshot). Ver seção abaixo.

## Solicitação Visual (user request)

Quando o usuário descreve um problema visual em vez de fornecer path/Figma/HTML,
esta skill age como **triagem**: identifica a categoria do problema e roteia para
a skill adequada.

### Como funciona

1. Ler a descrição do usuário (+ screenshot se fornecido via Read de imagem).
2. Classificar o problema com a tabela abaixo.
3. Se o problema for de **contraste ou hardcode** → executar a skill normalmente (Step 1–3).
4. Se o problema for de **qualidade visual/estrutural** → recomendar a skill correta e oferecer invocar.

### Tabela de triagem visual → skill

| Sintoma descrito pelo usuário | Categoria | Skill recomendada |
|---|---|---|
| "baixo contraste", "difícil de ler", "texto sumindo", "ícone fraco no dark" | Contraste WCAG | `/theme-audit --wcag` → `/theme-extend` se falha |
| "ícone pequeno", "ícone desalinhado", "ícone errado", "SVG cortado" | Geometria de asset | Diagnóstico manual SVG → `/theme-port` se estrutural |
| "cor hardcodada", "não usa token", "hex no código" | Cobertura | `/theme-audit` (scan estrutural) |
| "tela fraca", "sem impacto", "apagada", "parece form genérico" | Intensidade baixa | `/theme-critique` → `/theme-bolder` |
| "tela pesada", "agressiva", "gritando", "muito saturada" | Intensidade alta | `/theme-critique` → `/theme-quieter` |
| "coisa demais", "confuso", "carregado", "não sei onde olhar" | Cognitive load | `/theme-critique` → `/theme-distill` |
| "precisa de novo token", "cor faltando para X" | Token ausente | `/theme-extend` direto |
| "tela veio do Figma, porta" | Port | `/theme-port` (Figma) |
| "quero ver variações antes de portar" | Exploração | `/theme-sandbox` |
| "preciso de um mockup novo" | Criação | `/frontend-design` → `/theme-port` |

### Processamento de screenshot

Se o usuário anexar uma imagem (`Read` de screenshot):
1. Ler a imagem via `Read`.
2. Identificar: elementos com baixo contraste, ícones desalinhados/pequenos,
   hierarquia tipográfica inconsistente, saturação excessiva ou ausente.
3. Mapear cada problema identificado para a tabela acima.
4. Relatar diagnóstico + skills sugeridas antes de executar qualquer ação.

**Regra:** nunca executar uma skill de modificação (port/extend/bolder) automaticamente
a partir de screenshot sem confirmação do usuário. Diagnosticar → propor → aguardar OK.

## Workflow

### Step 1 — Scan estrutural

```bash
python scripts/theme/audit_theme.py [path]
```

Detecta (regex-based, ignora `.g.dart`/`.freezed.dart` e comentários):

**Estrutural:**

| Regra | Padrão | Permitido em |
|-------|--------|--------------|
| `hex_color` | `Color(0x[0-9A-Fa-f]{8})` | `lib/core/theme/app_colors.dart`, `app_theme.dart` |
| `material_color` | `Colors.<name>` (exceto `transparent`) | Nenhum widget de feature (justificar caso a caso) |
| `font_size` | `fontSize: <num>` | Nenhum |
| `font_weight` | `fontWeight: FontWeight.w<NNN>` | Nenhum |
| `edge_insets_literal` | `EdgeInsets.*(<num>)` fora da escala `AppSpacing` | Nenhum |
| `radius_literal` | `BorderRadius.circular(<num>)` fora da escala `AppRadius` | Nenhum |

**Anti-slop (`docs/product.md` §4.2 + §9, ativadas por default; `--no-slop` desliga):**

| Regra | Detecta |
|-------|---------|
| `filler_copy` | "Eleve seu/sua", "Desbloqueie seu/sua", "Otimizado para", "Jornada fitness", "Próximo nível", "Conquiste seus objetivos", "Sua melhor versão", "Continue assim", "Você é incrível", "Experiência seamless", "Transforme sua rotina" |
| `cliche_vocative` | "atleta!", "campeão!", "guerreiro!" em copy literal |
| `generic_placeholder` | "John Doe", "Jane Doe", "Lorem ipsum", "Acme", "Sarah Chan", "SmartFlow" |
| `em_dash_in_copy` | `—` dentro de string pt-BR (decorativo, raro legítimo) |
| `side_stripe_border` | `BorderSide(width: ≥2)` em border-left/right (cliché de alerta/callout) |
| `gradient_text` | `ShaderMask` aplicado em `Text` com `LinearGradient` |

Slop check é desligado em `lib/core/theme/preview/`, `test/`, `integration_test/` (fixtures legitimamente usam nomes genéricos).

Saída: lista por arquivo + contagens estruturais + totais slop separados.

### Step 2 — Scan de contraste (light + dark)

```bash
python scripts/theme/check_contrast.py --theme
```

Testa 12 pares semânticos × 2 modos (24 combinações). Reporta AA/AAA por par, purpose + rationale. Se algo falha, é candidato a `/theme-extend`.

**Pares padrão testados** (fonte canônica em `scripts/theme/check_contrast.py` > `EXPECTED_PAIRS`):

- `textPrimary`/`textSecondary` sobre `bgBase`/`bgSurface`/`bgInput`
- `textOnBrand` sobre `brandDefault`
- `brandDefault` sobre `bgBase` (large text — para link/destaque)
- `feedbackSuccess`/`feedbackError`/`feedbackWarning`/`feedbackInfo` sobre `bgBase`

**Sistema de tokens atual** (29 tokens em 7 grupos): `bg*` (6), `brand*` (5), `text*` (4), `border*` (3), `feedback*` (8), `gameAccent*` (3). `AppBrandColors` foi eliminado — não validar `context.brandColors.*` (não existe mais).

### Step 3 — Sintetizar relatório

Relatório executivo estruturado em **5 seções**:

#### 🏆 Cobertura por feature

Ranking de `lib/features/<x>/` por densidade de violação (violações ÷ linhas .dart). Top 5 piores, top 5 melhores.

#### 🎨 Violações por regra (totais)

Contagem de cada uma das 6 regras. Priorizar resolução: `hex_color` > `material_color` > `font_*` > `spacing/radius literal`.

#### ♿ Status WCAG AA

Lista de pares que falham AA (por modo). Cada falha é um **candidato explícito a /theme-extend** — sugere ajuste específico (ex: `success` dark ok, mas `success` light falha → escurecer `#22C55E` → algo como `#16A34A`).

#### 🔍 Top offenders (arquivos)

10 arquivos com mais violações. Link direto `file:line`.

#### ⏭️ Sugestão de ações

Checklist priorizada:
- [ ] `/theme-extend` para corrigir pares WCAG que falham
- [ ] Sweep manual para X arquivos top offenders
- [ ] `/theme-create` se identificar necessidade de palette totalmente nova

### Step 4 — Identificar falsos positivos

Alguns casos são legítimos e devem ser tolerados:

- `Colors.transparent` — ignorado pelo regex.
- `Colors.white` em **container de foto de avatar de patrocinador** — documentado em CLAUDE.md (logo transparente exige fundo branco invariante). Reportar mas marcar como known-good.
- `const` palette em arquivos com calendar/form que exigem `const BoxDecoration` (ex: `marketplace_schedule_calendar.dart`). Flag para revisão, não bloqueia.
- Arquivos de preview em `lib/core/theme/preview/`.

Ao apresentar o relatório, separar **violações bloqueantes** de **known-good tolerado**.

## Output example

```
=== audit em lib/features/marketplace ===
...lista de arquivos com violações...

Totais por regra:
         hex_color: 3
   material_color: 1
         font_size: 0
       font_weight: 0

📊 4 violações em 3 arquivos

♿ Status WCAG:
  LIGHT: 4 pares < AA (feedbackSuccess, feedbackWarning, feedbackError, ...)
  DARK:  2 pares < AA (brandDefault on bgBase, textOnBrand on brandDefault, ...)

⏭️  Sugestões:
  [ ] /theme-extend — ajustar feedbackSuccess/Warning/Error no light
  [ ] /theme-extend — rever brandDefault para contraste em dark mode
  [ ] sweep manual em marketplace_filters_page.dart (3 hex restantes)
```

## Anti-patterns

- ❌ Auditar sem light+dark — só light ignora 50% do tema.
- ❌ Ignorar contraste WCAG "porque está visível no emulador" — luminância acidente do dispositivo.
- ❌ Sugerir correção de violação sem validar o novo valor em contraste (handoff direto pro /theme-extend).
- ❌ Contar `Colors.transparent` como violação.

## Quando NÃO rodar

- Após mudança trivial de copy (texto mudou, cores iguais).
- Em PRs de lógica pura (data/domain/controllers sem widget novo).

## Integração com outras skills

| Fluxo | Próximo passo |
|-------|---------------|
| Audit encontrou falha WCAG | `/theme-extend` para ajustar o token |
| Audit encontrou hex legítimo de marca invariante | Adicionar a `AppBrandColors` e re-rodar audit |
| Audit passou 100% em feature crítica | Pronto para merge |
| Audit mostra necessidade de palette totalmente nova | `/theme-create` |
