# Discovery — doc templates

> Reference loaded by `theme-critique` (Júri) **after** entrevista termina, para gerar artefatos.
> Skeletons inline com placeholders `{{var}}`. Júri lê este arquivo, substitui vars, escreve via `Write`.

Tier matrix (de `discovery-sizing.md`) define quais skeletons rodar:

- `quick` → só `discovery.md`.
- `light` → `discovery.md` + PRD curto.
- `full` → `discovery.md` + PRD completo + append em `docs/design.md` (se existir).
- `greenfield` → `discovery.md` + PRD + 4 skeletons completos.

---

## `discovery.md` — frontmatter schema (sempre)

```markdown
---
feature: {{feature_slug}}
status: draft  # draft | in_progress | approved | consumed
mode: {{detected_mode}}        # greenfield | brownfield
tier: {{tier}}                 # quick | light | full | greenfield
created: {{iso_date}}
audit_pre_scan: {{bool}}       # true se rodou audit_theme.py
---

# Discovery — {{feature_slug}}

## Block 1 — Produto
**status:** complete
**quality:** {{quality_tag}}

### P1.1 — Scene sentence
> {{answer_p1_1}}

### P1.2 — Persona primária + trip-up
> {{answer_p1_2}}

### P1.3 — Tarefa primária
> {{answer_p1_3}}

## Block 2 — Tom
[...mesmo padrão por bloco...]

## Block 3 — Identidade
[...]

## Block 4 — Stack
[...]

## Brownfield audit (pre-scan)
<!-- só se mode=brownfield. Output completo do audit_theme.py em bloco fenced. -->
```text
{{audit_output}}
```

## Action plan
<!-- YAML com schema de discovery-routing.md -->
```yaml
plan:
  - rank: 1
    skill: {{skill_1}}
    reason: "{{reason_1}}"
    eta: "{{eta_1}}"
    blocks: []
  ...
```
```

---

## `docs/product.md` — skeleton (greenfield only)

```markdown
# Product — {{project_name}}

> Source of truth for product-level decisions (positioning, voice, anti-references, color strategy).
> Voltado a humanos do time. Skills de design (Júri/Compositor/etc.) gateiam aqui antes de qualquer crítica/criação.

## §1 Visão

<!-- preencher: 1 parágrafo sobre o problema central + transformação prometida ao usuário -->
<!-- exemplo: "Para Maria, treinadora recorrente, o app transforma rotina mecânica de academia em pequena economia visível — cada treino vira pontos que viram cupons reais." -->

## §2 Personas

### Persona primária — {{persona_primary_name}}
<!-- preencher: idade, contexto, frequência de uso, motivação central, 1 trip-up concreto -->
<!-- exemplo: "Maria, 32, treina musculação 4×/semana às 6h30am. Tem 30s de paciência durante o estacionamento. Trava em telas que celebram esforço em vez de mostrar recompensa." -->

### Persona secundária — {{persona_secondary_name}}
<!-- preencher: contraste com a primária; momento diferente, motivação frágil, vocabulário diferente -->

### Persona terciária — {{persona_tertiary_name}}
<!-- preencher: presença passiva (parceiro de marca, pai/mãe que paga, etc.). Não é usuário ativo. -->

## §3 Jornada principal

<!-- preencher: 5-7 passos do user flow primário, do gatilho ao reward. Marcar peak emocional. -->
<!-- exemplo:
1. Maria estaciona às 6h25 → abre app
2. Vê saldo de pontos crescendo (peak emocional 1)
3. Toca em "Cupons disponíveis"
4. Escolhe cupom → desbloqueio (peak emocional 2)
5. Salva no wallet → fecha app
-->

## §4 Voz e tom

### §4.1 Tom default
<!-- preencher: 3 sensações físicas (não adjetivos) + 1 ref concreta + 1 anti-ref -->

### §4.2 Banidos absolutos
<!-- preencher: lista de palavras/frases NUNCA aparecem. -->
<!-- exemplo: "parabéns!", "uau", "incrível", emojis em CTAs, vocativo "você merece" -->

### §4.3 Vocativo
<!-- preencher: tu, você, você-impessoal? Nome próprio? Default formal/informal? -->

## §5.3 Color strategy axis

<!-- preencher: drenched | restrained | neutral × warm | cool | neutral. Justificar com persona. -->
<!-- exemplo: "Drenched warm — Maria precisa de recompensa visceral imediata; cor que inunda a tela de comemoração é a métrica de sucesso emocional." -->

## §7 Anti-references

<!-- preencher: 3-5 produtos/sites/marcas que o produto NÃO PODE parecer + razão específica -->
<!-- exemplo: "Não pode parecer banco digital (frio, métrico). Não pode parecer LinkedIn (performático). Não pode parecer wellness app gen-Z (saturado, infantil)." -->

## §8 Princípios estratégicos

<!-- preencher: 5-7 axiomas que orientam decisão quando há tensão entre opções -->
<!-- exemplo:
§8.1 Recompensa > esforço. Tela mostra o que ganhou, não o que fez.
§8.2 Saldo de pontos sempre na primeira dobra.
§8.3 Conteúdo de marca tem peso visual igual a conteúdo próprio (não destacado como ad).
-->
```

---

## `docs/design.md` — skeleton (greenfield only)

```markdown
# Design system — {{project_name}}

> Princípios de design system. Não confundir com `design-tokens.md` (valores) ou `product.md` (positioning).

## Princípios

### 1. Hierarquia primeiro
<!-- preencher: como decisão de tamanho/peso/cor codifica importância -->

### 2. Consistência > criatividade
<!-- preencher: padrões antes de exceções; exceções precisam justificar -->

### 3. Acessibilidade como default
<!-- preencher: WCAG AA mínimo; AAA onde possível; contraste sempre validado -->

## Canon visual

Pointer pra `docs/design-tokens.md` — todos os valores numéricos vivem lá.

## Heurísticas (Nielsen)

`/theme-critique` aplica Nielsen 0–4 × 10 heurísticas. Veja `references/nielsen-rubric.md`.

## Ciclo de design

```
/juri (discovery) → /theme-create (palette) → /frontend-design (mockups)
  → /theme-port (Flutter) → /theme-audit (estrutural) → /theme-critique (juízo)
  → /theme-{bolder,quieter,distill,extend,motion} (refino)
```
```

---

## `docs/design-tokens.md` — skeleton (greenfield only)

```markdown
# Design tokens — {{project_name}}

> Single source of truth para valores numéricos do design system.
> `/theme-extend` adiciona/ajusta entries aqui; `/theme-port` consome.

## Palette — brand

| Token         | Light       | Dark        | Use                               |
|---------------|-------------|-------------|-----------------------------------|
| `brand`       | `<!-- preencher -->` | `<!-- preencher -->` | Cor primária da marca |
| `onBrand`     |             |             | Texto/ícone sobre `brand`         |
| `brandMuted`  |             |             | Variant atenuada                  |

## Palette — semantic

| Token             | Light | Dark | Use |
|-------------------|-------|------|-----|
| `feedbackSuccess` |       |      | Estados de sucesso |
| `feedbackError`   |       |      | Erros |
| `feedbackWarning` |       |      | Atenção |
| `feedbackInfo`    |       |      | Neutro informativo |

## Palette — neutral

| Token       | Light | Dark | Use |
|-------------|-------|------|-----|
| `bgBase`    |       |      | Fundo principal |
| `bgSurface` |       |      | Cards, surfaces elevadas |
| `textPrimary`   |   |      | Texto principal |
| `textSecondary` |   |      | Texto auxiliar |
| `textTertiary`  |   |      | Disabled, hint |

## Typography roles

| Role          | Family | Size | Weight | Line-height | Use |
|---------------|--------|------|--------|-------------|-----|
| `displayLarge`|        |      |        |             |     |
| `headlineLarge`|       |      |        |             |     |
| `titleMedium` |        |      |        |             |     |
| `bodyLarge`   |        |      |        |             |     |
| `bodyMedium`  |        |      |        |             |     |
| `labelLarge`  |        |      |        |             |     |

## Spacing scale

`<!-- preencher: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 — ou variação -->`

## Radius scale

`<!-- preencher: 0 / 4 / 8 / 12 / 999 -->`

## Contrast tiers (acessibilidade)

| Tier | WCAG contrast | Use case |
|------|---------------|----------|
| A    | ≥4.5:1        | Default |
| A+   | ≥7:1          | Idosos, baixa visão |
| A++  | ≥10:1         | Alto contraste forçado |
```

---

## `docs/PRD.md` — skeleton (per-intervention; light/full/greenfield)

```markdown
# PRD — {{intervention_slug}}

**Created:** {{iso_date}}
**Source:** discovery em `.design-spec/features/{{feature_slug}}/discovery.md`
**Tier:** {{tier}}

## Problem

<!-- preencher: 1 parágrafo. O quê precisa mudar e por quê. Cite persona afetada. -->

## Top fixes (priorizados)

### Fix 1 — {{fix_1_title}}
- **Sintoma:** <!-- evidence file:line ou descrição -->
- **Skill:** `<!-- /theme-extend, /theme-bolder, etc. -->`
- **ETA:** <!-- ~1h, ~2h -->
- **Block:** <!-- IDs de outros fixes que precisam vir antes, ou [] -->

### Fix 2 — {{fix_2_title}}
[...]

### Fix 3 — {{fix_3_title}}
[...]

## Skills mapping

| Fix | Skill | Reason |
|-----|-------|--------|
| 1   |       |        |
| 2   |       |        |
| 3   |       |        |

## Success metric

<!-- preencher: como saber se a intervenção funcionou. Pode ser qualitativo ("Maria entende em 5s onde tá o saldo") ou quantitativo ("≥1 contrast pair acima de 4.5:1"). -->

## Out of scope

<!-- preencher: o que esta intervenção explicitamente NÃO resolve, mas alguém vai perguntar. -->
```

---

## Vars de substituição (mapping completo)

| Var                       | Origem                                                  |
|---------------------------|---------------------------------------------------------|
| `{{feature_slug}}`        | argumento de `/juri` ou perguntado se ausente          |
| `{{project_name}}`        | derivado de `pubspec.yaml`/`package.json`/dir name      |
| `{{detected_mode}}`       | output de `detect_mode.py`                              |
| `{{tier}}`                | tier escolhido (auto ou override)                       |
| `{{iso_date}}`            | `date -u +"%Y-%m-%d"`                                   |
| `{{persona_primary_name}}`| resposta P1.2                                           |
| `{{audit_output}}`        | stdout de `audit_theme.py` (brownfield)                 |
| `{{quality_tag}}`         | derivado das respostas (strong/medium/weak)             |
| `{{answer_pX_Y}}`         | resposta literal do usuário                             |
| `{{skill_N}}` / `{{reason_N}}` / `{{eta_N}}` | derivados de `discovery-routing.md`     |

## Anti-padrões na geração

- ❌ Sobrescrever `docs/product.md` existente em greenfield sem confirmar (REQ-A5.5).
- ❌ Persistir `<!-- preencher -->` literal em `discovery.md` (placeholder do template, não do output) — substitua sempre.
- ❌ Gerar PRD sem `Top fixes` quando tier ≥ light.
- ❌ Inventar persona/scene-sentence se usuário não respondeu — em vez disso, deixa `<!-- preencher -->` no skeleton e marca `quality: weak`.
- ❌ Renomear arquivos `docs/*.md` (a convenção é canônica do repo via `config.example.yaml`).
