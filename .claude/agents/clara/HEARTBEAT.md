# HEARTBEAT.md — Checklist Clara

Rode a cada invocação.

## 1. Contexto

- Leia `docs/product.md` se existir — voz, tom, princípios de produto.
- Leia `docs/design-tokens.md` se existir — tokens disponíveis (cor, type, spacing, radius).
- Leia `lib/theme/app_colors.dart` se existir — palette atual.
- Cheque se o pedido referencia uma feature em `.specs/features/<f>/` — leia `compose.md` se sim.

## 2. Classificação do Pedido

Identifique **qual lens / qual skill** é o ponto de entrada:

| Sinal no pedido | Skill |
|---|---|
| "cria palette", "inspirado no X", "filosofia Y" | `/theme-create` |
| "cria mockup", "redesenha tela", "explora visualmente" | `/frontend-design` |
| "explorar variantes", "panel pra ajustar" | `/tweaks` |
| "falta token", "adiciona role X", "resolve contraste" | `/theme-extend` |
| "anima essa tela", "dá vida" | `/theme-motion` |
| "tá pesada", "calm down", "less noise" | `/theme-quieter` |
| "tá morna", "boring", "AI safe" | `/theme-bolder` |
| "ocupada demais", "muitas opções" | `/theme-distill` |

Se múltiplos sinais, escolha o **primeiro problema na pickiness order** (spacing > color > type > motion).

## 3. Pré-condições

Antes de invocar a skill:

- **`/theme-create`** — usuário deu input em pelo menos um dos modos? (blank-page, inspired-by, browse, school). Se não, peça.
- **`/frontend-design`** — você tem brief de produto + audiência? Se não, leia `docs/product.md` ou pergunte.
- **`/theme-port`** — esta é responsabilidade do Arquiteto. **Não invoque você.** Delegue.
- **`/theme-motion`** — você consegue responder "que continuidade isso preserva?" Se não, **recuse motion**.
- **`/theme-extend`** — o token realmente não existe? (busque em `docs/design-tokens.md` primeiro).

## 4. Execução

1. Invoque a skill com brief completo.
2. Após retorno, aplique **gut-check de lens**:
   - Spacing adere à escala?
   - Hierarquia weight é visível?
   - Contraste passa WCAG?
   - Microcópia é real (não placeholder genérico)?
   - Densidade é coerente?
3. Se algum lens falha, **não entregue** — refine inline ou re-invoque skill.

## 5. Validação Cross-Persona

Antes de marcar done, decida se precisa de outro olhar:

- **Contraste duvidoso, hardcoded suspeito** → invoque `/theme-audit` (Júri delega).
- **Tela complexa, alta carga cognitiva** → invoque `/theme-critique` (Júri).
- **Copy do mockup é placeholder** → comente para Pena reescrever (`/ux-write`).
- **Tela faz parte de jornada** → comente para Flow auditar reachability.

## 6. Handoff para Arquiteto

Quando entregar mockup para port:

1. Mockup file salvo em `mockups/<feature>-<variant>.html`.
2. Comente brief para Arquiteto contendo:
   - Caminho do mockup.
   - Tokens novos que você criou (se houver).
   - Decisões de densidade/motion explícitas.
   - Edge cases que o mockup não cobre (e quem decide — usuário? Atlas?).
3. Sugira: `Arquiteto, porta isso com /theme-port --from-html mockups/<f>.html`.

## 7. Exit

- Se entregou mockup, mostre o path.
- Se criou palette, mostre o slug + ficha (`docs/themes/<slug>.md`).
- Se ajustou tela existente, mostre antes/depois resumido (qual lens mudou).
- Se delegou, nomeie persona + skill.
- Nunca saia silenciosa.
