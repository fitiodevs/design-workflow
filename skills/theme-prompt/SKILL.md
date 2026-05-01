---
name: theme-prompt
license: Complete terms in LICENSE.txt
description: Compõe um Stitch prompt estruturado (Content + Style + Layout) a partir de handoff Júri + docs/product.md + docs/design-tokens.md. Sub-skill puro prompt-engineering — sem chamadas MCP, sem geração. Output é o `intent.brief_prompt` que `/theme-sandbox` envia ao Atelier. Use quando o usuário quer revisar ou ajustar o prompt antes de gastar créditos Stitch ("/theme-prompt critique-...yaml", "monta o prompt sandbox da tela X", "preview Stitch prompt").
triggers:
  - /theme-prompt
  - monta(r)? (o )?prompt (do |pra |para )?stitch
  - preview stitch prompt
  - prompt sandbox
---

# Skill: fitio-theme-prompt (`/theme-prompt`)

Sub-skill estática. Pega 3 fontes (handoff Júri, product.md, design-tokens.md) e devolve **prompt Stitch** com 3 seções obrigatórias: Content + Style + Layout. Anti-AI-slop por construção: anti-references explícitas, color commitment axis nomeado, scene sentence ancorada.

Esta skill não chama Stitch. Ela é **input** do `/theme-sandbox` (que orquestra Atelier) e pode ser invocada sozinha pra debugar/iterar prompt antes de queimar créditos.

## Inputs

Aceita uma de três formas:

1. **Path para handoff Júri** (`/theme-prompt .claude/handoffs/critique-2026-04-28T-explorar.yaml`) — mais comum, mais rico.
2. **Target + intent free-text** (`/theme-prompt lib/features/feed/ "pontos invisivel acima dobra"`) — fallback quando não há critique.
3. **Sem args** — pede ao usuário um dos dois acima.

## Prerequisites

- `docs/product.md` ≥2KB. Se ausente, parar e pedir criação. Sem product.md o prompt cai em SaaS-genérico.
- `docs/design-tokens.md` (referência de roles disponíveis pro rationale, não pra cores no prompt — Stitch é wireframe).
- Handoff Júri (modo 1): YAML válido com `target`, `issues[]` (P0/P1), `next_action.axis`.

## Workflow

### Step 1 — Carregar fontes

1. Read `docs/product.md` — extrair §2 (scene sentence), §4 (tom de voz, banidos), §5.3 (color strategy axis), §7 (anti-references), §8 (recompensa <1s, multimodalidade).
2. Read `docs/design-tokens.md` — só pra citar nomes de roles disponíveis. **Nunca** copiar hex pro prompt.
3. Read input handoff/target.

### Step 2 — Extrair drivers

Do handoff Júri (modo 1):

- `target` → vira **Content scope** (qual tela)
- `issues[]` filtrado por `sev in [P0, P1]` → vira **Content priorities** (o que precisa estar acima da dobra / hero)
- `next_action.axis` → vira **Style axis principal** (cor / tipografia / composição / quantidade)
- `personas.maria/joao/patrocinador` → trava-points viram **Layout requirements** (ex: "30s paciência" → ação primária ≤2 toques)

Do product.md:

- §2 scene sentence → **Style scene anchor** (ex: "Maria 6h30 chega na academia")
- §7 anti-references → **Style anti-references** (ex: "não Strava, não Duolingo, não banking dashboard, não fitness influencer")
- §4.2 banidos absolutos → **Content copy bans** (ex: "não 'atleta!', não 'jornada', não 'eleve'")
- §5.3 color strategy axis → mapear `next_action.axis` em `restrained|committed|full|drenched` narrado

### Step 3 — Compor 3 blocos

```
CONTENT
- Tela: <target em 1 frase>
- Cena: <scene sentence product.md §2>
- Acima da dobra (priority order):
  1. <P0 dominante reformulado positivamente>
  2. <P1 #1>
  3. <P1 #2>
- Copy direction: tom direto, sem vocativo, sem exclamação. Banidos: <lista §4.2>.
- Multimodalidade: <se aplicável, listar modalidades possíveis §8.6>

STYLE
- Color commitment axis: <restrained|committed|full|drenched>. Variar entre variations.
- Tipografia: hierarquia <display|headline|title|body|label> dominante. Hero é <elemento>.
- Densidade: <compact|comfortable|spacious>.
- Anti-references (não imitar): <lista §7>.
- IMPORTANT: este é wireframe estrutural. Sem cores hex específicas. O tema Fitio aplica cores depois via /theme-port.

LAYOUT
- Container: mobile single column, viewport 360×800 (deviceType=MOBILE).
- Above-the-fold: <lista priorizada de Step 2>.
- Cognitive load target: ≤4 pontos de decisão na tela inteira.
- Ação primária: ≤2 toques (Maria 30s paciência).
- Sticky elements: <bottom CTA / FAB / nav, se aplicável>.
- Reflexo / asymmetry: <se axis=composição, sugerir quebra de simetria §8.6>.
```

### Step 4 — Validar prompt

Antes de retornar, checar:

- [ ] Scene sentence presente e bate com product.md §2?
- [ ] Anti-references explícitas (≥3 do §7)?
- [ ] Banidos copy listados?
- [ ] Color axis nomeado (não "moderno", não "clean")?
- [ ] Cognitive load target declarado?
- [ ] Wireframe-only declarado (sem hex)?
- [ ] Hero element identificado (do P0 do Júri)?

Se qualquer item falhar, refazer o bloco antes de output.

### Step 5 — Output

Retornar dois artefatos:

1. **Prompt Stitch (texto cru)** — pronto pra colar em `mcp__stitch__generate_screen_from_text`.
2. **Validation summary (caveman)** — 1 linha por checklist item passou/falhou.

Se chamado por `/theme-sandbox`, output vai pro `intent.brief_prompt` do handoff atelier. Se chamado standalone, mostrar pro usuário pra revisão.

## Anti-patterns

- ❌ Hex colors no prompt. Wireframe-only.
- ❌ Tailwind class names. Não cole `bg-blue-500`.
- ❌ Hype words ("clean", "moderno", "vibe", "sleek"). Substituir por axis técnico.
- ❌ Esquecer anti-references. Sem isso = category-reflex garantido (verde Strava, gradiente Duolingo).
- ❌ Copy literal pt-BR no prompt. Stitch gera em inglês; copy pt-BR vem depois via `/theme-port` + tema.
- ❌ Ignorar `next_action.axis` do Júri. Prompt sem axis = Atelier gera 3 versões iguais.
- ❌ Mais de 3 P0/P1 acima da dobra. ≤4 cognitive load = ≤4 priorities.
- ❌ Inventar scene sentence. Vem do product.md §2, não do agent.

## Exemplo (Explorar / handoff 2026-04-28)

Input: `.claude/handoffs/critique-2026-04-28T-explorar.yaml`
- target: `lib/features/feed/presentation/`
- P0a: pontos titleSmall — recompensa invisível
- P0b: zero cupom acima da dobra
- next_action.axis: composição

Output (resumido):

```
CONTENT
- Tela: Home Fitio (feed) pós-login
- Cena: Maria, 6h30, chega na academia, abre app esperando reforço imediato
- Acima da dobra:
  1. Pontos acumulados (hero — leitura <1s, contexto: "X moedas" não só número)
  2. Próximo cupom desbloqueável (faltam Y check-ins) — antes dos chips
  3. Atalho check-in (1 toque, sem scroll)
- Copy: tom direto. Banidos: "atleta!", "campeão!", "jornada", "Bom dia/tarde/noite", vocativo.
- Multimodalidade: chip ativo + "Mais" expansível (musculação, corrida, yoga, natação, dança, luta).

STYLE
- Color commitment axis: variar (drenched / committed / restrained nas 3 variations).
- Tipografia: pontos é hero displayMedium-ish; cupom é titleMedium; resto bodyMedium.
- Densidade: comfortable (não compact — Maria não lê micro-text correndo).
- Anti-references: não Strava (nenhum verde-limão hero metric template), não Duolingo (sem mascote, sem vocativo), não banking dashboard (sem saudação horária), não fitness influencer (sem motivação aspiracional).
- Wireframe estrutural. Sem hex. Tema Fitio aplica cores depois.

LAYOUT
- Mobile single column 360×800.
- Above-the-fold: pontos hero → cupom card → atalho check-in.
- Cognitive load: ≤4 (pontos / cupom / check-in / chips secundários).
- Ação primária: check-in em ≤2 toques.
- Sticky: bottom nav.
- Reflexo: cupom card pode quebrar simetria — desalinhado vs grid de chips.
```

## Saída esperada

```yaml
prompt_text: |
  <texto cru do Step 3>
validation:
  scene_sentence: pass
  anti_references: pass (4 listadas)
  copy_bans: pass
  color_axis: pass (drenched/committed/restrained)
  cognitive_load: pass (≤4)
  wireframe_only: pass
  hero_element: pass (pontos)
ready_for_atelier: yes
```

## Integração com frontend-design

Ao compor o bloco `STYLE:`, aplique os princípios da skill `frontend-design` traduzidos
para o vocabulário wireframe (sem hex, sem font-families específicas):

| frontend-design | Equivalente no bloco STYLE: |
|---|---|
| Typography (characterful) | `Tipografia: hierarquia <role> dominante. Hero é <elemento>. Evitar hierarquia flat.` |
| Spatial Composition | `Composição: assimetria intencional. <elemento> quebra grid. Negative space generoso em <área>.` |
| Density (controlled) | `Densidade: <compact/comfortable/spacious>. Razão: <persona + contexto de uso>.` |
| Motion intent | `Motion hint: stagger <N>ms entre cards. Hover state em <elemento>. (Implementar via flutter_animate no port.)` |
| Anti-references | Já coberto pelo anti-references de product.md §7 — complementar com referências web se aplicável. |

**Nunca** copiar classes Tailwind ou hex do output de `frontend-design` para o prompt Stitch.
O `frontend-design` é fonte de **direção estética**, não de código a copiar.

Quando o output final for alimentar `/theme-port --from-stitch`, o HTML gerado por
`frontend-design` deve usar viewport 360px e `px` explícito em layout (ver SKILL.md de
`frontend-design` § Pipeline Fitio).
