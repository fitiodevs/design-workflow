# Discovery — routing output

> Reference loaded by `theme-critique` (Júri) **after** entrevista para emitir plano de ação priorizado.
> Output final do discovery é roteamento, não menu. Plan é apendado a `discovery.md` e ecoado em prosa pro usuário.

## Schema YAML do `plan`

Sempre apendado a `discovery.md` na seção `## Action plan`:

```yaml
plan:
  - rank: 1
    skill: /theme-create
    reason: "palette ainda não existe — bloqueia tudo abaixo"
    eta: "~2h"
    blocks: []
  - rank: 2
    skill: /frontend-design
    reason: "explorar 3 mockups da home antes de portar"
    eta: "~1h"
    blocks: ["1"]
  - rank: 3
    skill: /design-spec compose  # (Onda B — placeholder)
    reason: "selecionar 1 mockup e bater contra palette"
    eta: "~30min"
    blocks: ["1", "2"]
```

### Campos obrigatórios por item

- `rank` — int. 1 = primeira ação. Sequencial.
- `skill` — string. Nome exato (com `/`). Ver lista canônica abaixo.
- `reason` — string. 1 frase ligando a uma resposta da entrevista (ou audit pre-scan).
- `eta` — string. `~30min`, `~1h`, `~2h`, `~half-day`, `~1 day`. Não usar prazo absoluto (datas).
- `blocks` — list de strings. IDs de items (rank) que precisam concluir antes.

## Lista canônica de skills

### Atômicas v0.2.0 (instaladas)
- `/theme-create`
- `/theme-extend`
- `/theme-port`
- `/theme-audit`
- `/theme-critique` (auto-recursão proibida — não roteia para si)
- `/theme-bolder`
- `/theme-quieter`
- `/theme-distill`
- `/theme-motion`
- `/frontend-design`
- `/pena` (alias `/ux-writing`)

### Orchestration (Ondas B+ — marcar como `(Onda B)` no `reason` quando usar)
- `/design-spec compose`
- `/design-spec sequence`
- `/design-spec ship`

### Não-skills (referência, não executável via Júri)
- `/design-spec pause` (Onda C)
- `/design-spec resume` (Onda C)

## Mapa decisão → skill

Use estas heurísticas para preencher `plan`:

| Sintoma da entrevista                                                  | Skill                          | Reason template |
|------------------------------------------------------------------------|--------------------------------|-----------------|
| Greenfield + palette ausente                                           | `/theme-create`                | "palette ainda não existe — bloqueia tudo abaixo" |
| Persona pede recompensa visceral, axis = drenched, palette tímida      | `/theme-bolder`                | "axis drenched no product.md mas palette ainda restrained" |
| Brownfield + audit achou hex_count > 20                                | `/theme-audit` (re-rodar visível) + `/theme-extend` | "drift estrutural — substituir literais por tokens existentes" |
| Brownfield + falha de contraste em ≥1 par token                        | `/theme-extend`                | "ajustar token X para passar WCAG AA em dark" |
| Greenfield, sem mockup ainda, multiple visual options no ar            | `/frontend-design`              | "explorar 2-3 mockups da {{tela_alvo}} antes de portar" |
| Mockup pronto (Figma URL/node-id ou HTML local)                        | `/theme-port [--from-html <path>]` | "porta {{frame}} para Flutter usando tokens" |
| Tela específica precisa juízo agora                                    | `/theme-critique <path>`        | "rodar critique sobre {{path}} antes de refino" |
| Cognitive load alto na tela primária                                   | `/theme-distill`                | "≥4 opções num ponto de decisão — precisa enxugar" |
| Tela agressiva/saturada                                                | `/theme-quieter`                | "intensidade visual passa do alvo para essa persona" |
| Copy fraca/genérica reportada na entrevista                            | `/pena`                         | "tom em P2 vs copy atual divergem — reescrever labels-chave" |
| Estática reportada como problema                                      | `/theme-motion`                 | "feedback de press / transição entre rotas ausente" |

## Como escolher o ranking

Ordem de prioridade (top-down):

1. **Bloqueadores estruturais primeiro.** Palette ausente bloqueia mockup; mockup bloqueia port; port bloqueia critique.
2. **Brownfield: drift antes de novidade.** Não adicionar feature sem limpar drift que já está corrompendo.
3. **Persona-affecting issues > taste calls.** Falha de contraste afeta usuário real; bolder/quieter é taste.
4. **Quick wins ≤30min** podem subir 1 posição se desbloqueam algo maior.

## Anti-padrões

- ❌ Auto-rodar a próxima skill. Júri **sempre** para no plano e devolve ao usuário escolher.
- ❌ ETAs vagas tipo "rápido", "longo". Usar bandas concretas (`~30min`, `~1h`, `~half-day`).
- ❌ Skill names inventados. Lista canônica acima é exclusiva.
- ❌ Mais de 5 itens no plano. Se passa de 5, é sinal de re-priorizar — Júri trunca em top-5 e cita os deferred ao final.
- ❌ Reason genérico ("polish", "improve"). Sempre ligar a uma resposta concreta da entrevista ou um número do audit.
- ❌ `blocks` cíclicos (item 2 bloqueia item 1 que bloqueia item 2). Validar antes de persistir.

## Echo pro usuário (não-YAML)

Após persistir o YAML em `discovery.md`, Júri ecoa em prosa numerada para o usuário escolher:

```
Próximos passos sugeridos (escolha 1 — eu não auto-rodo):

1. /theme-create — palette ainda não existe (bloqueia 2 e 3). ETA ~2h.
2. /frontend-design — explorar 3 mockups da home antes de portar. ETA ~1h. Depende de #1.
3. /design-spec compose [Onda B — não disponível ainda] — selecionar 1 mockup e bater contra palette.

Qual você quer rodar agora?
```

Echo em PT-BR. Tipografia em monospace só para nomes de skill. Sem caveman, sem YAML cru — usuário lê prosa, não protocolo.
