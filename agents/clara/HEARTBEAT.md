# HEARTBEAT.md — Checklist Clara

Rode a cada invocação.

## 1. Contexto

- Leia `docs/product.md` se existir — voz, tom, princípios de produto.
- Leia `docs/design-tokens.md` se existir — tokens disponíveis (cor, type, spacing, radius).
- Leia `lib/theme/app_colors.dart` (Flutter) / `app/globals.css` (Next) / `theme/colors.ts` (RN) — palette atual.
- Se o pedido vem de uma feature spec (ex: `.specs/features/<f>/compose.md`), leia a section visual relevante. Esse arquivo é mantido pelo product-workflow (opcional companion) — ignore se não estiver presente.

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
- **`/theme-port`** — você invoca (executor: Elo), mas o port em si é mecânico (HTML/Figma → widgets). Se a sessão tem product-workflow instalado, prefira delegar pro Petro via `/sequence` quando o port for parte de uma tasks.md.
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

- **Contraste duvidoso, hardcoded suspeito** → invoque `/theme-audit` (Olavo delega).
- **Tela complexa, alta carga cognitiva** → invoque `/theme-critique` (Olavo).
- **Copy do mockup é placeholder** → comente para Pena reescrever (`/ux-write`).
- **Tela faz parte de jornada** → comente para Flavio auditar reachability.

## 6. Handoff para port

Quando entregar mockup para port (Flutter/RN/Next):

1. Mockup file salvo em `mockups/<feature>-<variant>.html`.
2. Comente brief contendo:
   - Caminho do mockup.
   - Tokens novos que você criou (se houver).
   - Decisões de densidade/motion explícitas.
   - Edge cases que o mockup não cobre.
3. Próximo passo: `/theme-port --from-html mockups/<f>.html` (rodar você mesma — executor: Elo — ou, se product-workflow está instalado, pedir pro Petro via /sequence pra virar task).

## 7. Exit

- Se entregou mockup, mostre o path.
- Se criou palette, mostre o slug + ficha (`docs/themes/<slug>.md`).
- Se ajustou tela existente, mostre antes/depois resumido (qual lens mudou).
- Se delegou, nomeie persona + skill.
- Nunca saia silenciosa.
