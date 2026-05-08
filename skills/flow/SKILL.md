---
name: flow
description: Flow persona — orquestrador de auditoria de fluxo UX cross-tela. Audita rotas, jornadas e features contra 10 heurísticas (docs/flow-heuristics.md), emite relatório combinado (deterministic + LLM), dispatcha issues para Clara/Júri/Brasa/Pena em paralelo. Com --dispatch, gera audit-sequence-{date}.md compatível com /sequence. Triggered by /flow, /Flow, "audita fluxo", "mapa de UX".
---

# Skill: flow (`/flow`) — Flow persona

## Triggers

- **English:** `/flow`, `/Flow`, `/flow <journey>`, `/flow <feature>`, `/flow --all`, `/flow --dispatch`, `/flow --quick`, "audit UX flow", "map user journey", "where does the user get stuck"
- **Português:** `/flow`, `/Flow`, `/flow <jornada>`, `/flow <feature>`, "audita fluxo", "mapa de UX", "onde o usuário trava", "analisa jornada", "verifica o fluxo"
- **Natural language:** journey slug (`01-cadastro`, `02-comprar-cupom`), feature name (`coupons`, `marketplace`), `--dispatch` pra gerar sequence.md.

## Flag protocol

| Invocation | Scope | Extra output |
|---|---|---|
| `/flow` | todas jornadas curadas em `docs/flows/` | — |
| `/flow <journey>` | jornada específica (ex: `01-cadastro`) | — |
| `/flow <feature>` | feature slug (ex: `coupons`, `marketplace`) | — |
| `/flow --all` | catálogo inteiro (inclui jornadas sem doc curado) | — |
| `/flow --dispatch` | todas jornadas + catálogo | skills spawned em paralelo + `audit-sequence-{date}.md` |
| `/flow <journey> --dispatch` | jornada específica | skills spawned em paralelo + `audit-sequence-{date}.md` |
| `/flow --quick` | todas jornadas — pula Phase 2 (LLM) | — |

## Modo de execução

`/flow` é **wrapper de orquestração em 4 phases**. Phase 1 roda via Bash/Grep (deterministic, sem LLM). Phase 2 delega ao agent `Flow` (`.claude/agents/flow.md`) via `Agent` tool. Phase 3 combina resultados. Phase 4 (com `--dispatch`) spawna skills correctoras em paralelo.

**Nunca auditar em-cabeça neste arquivo** — a auditoria LLM é sempre delegada ao agent Flow.

## Setup gates (não-opcionais)

| Gate | Verificação | Se falha |
|---|---|---|
| Catálogo | `docs/flows/_catalog.md` existe | Sugerir `python3 scripts/generate_screen_catalog.py` |
| Product | `docs/product.md` existe com >2KB | Parar. Fonte de vocab e personas. |
| Heurísticas | `docs/flow-heuristics.md` existe | Sugerir criar o arquivo canon. |
| Target | Jornada/feature especificada existe em `docs/flows/` ou no catálogo | Listar disponíveis e pedir escolha. |

## Phase 0 — Setup

1. Verificar gates acima.
2. Identificar escopo: `<journey>`, `<feature>`, `--all`, ou default (todas as jornadas curadas).
3. Listar arquivos de jornada relevantes em `docs/flows/` (padrão `NN-*.md`, exceto `_catalog.md` e `README.md`).
4. Comunicar ao usuário: "Auditando <X>. Phase 1 deterministic → Phase 2 LLM → Phase 3 combine[→ Phase 4 dispatch]. Aguarde."

## Phase 1 — Deterministic checks

Rodar sem LLM — rápido e barato. Quatro verificações via Bash/Grep:

### 1.1 · Orphan routes
```bash
grep -A 50 "## Anomalias" docs/flows/_catalog.md | grep "^\- \`"
```
Toda órfã = issue P1 `reachability`.

### 1.2 · State.extra fragility
```bash
grep -n "state\.extra as " lib/router/app_router.dart
```
Cada hit: P1 se rota mencionada em `DeepLinkService`, P2 se navegação interna apenas.

### 1.3 · Vocabulary violations
```bash
grep -rn \
  -e 'Text("[^"]*\bcomprar\b' \
  -e 'Text("[^"]*\bresgatar\b' \
  -e 'Text("[^"]*\bmissão\b' \
  -e 'Text("[^"]*\bdesbloquear\b' \
  -e 'Text("[^"]*\bmirar\b' \
  lib/features/
```
Cada match = issue P1 `vocab` (revisar falsos positivos em comentários antes de reportar).

### 1.4 · Deep link gaps
```bash
grep -n "fitio://" lib/core/services/deep_link_service.dart
```
Cruzar contra rotas estáveis no catálogo (sem path param, sem state.extra) — gap = issue P2 `happy_path`.

**Output Phase 1:** lista numerada de findings com `file:line`. Se nenhum encontrado, registrar "Phase 1: limpo".

## Phase 2 — LLM audit (agent Flow)

> Pular com `--quick`.

Spawnar agent:

```
Agent({
  description: "Flow audita jornada UX",
  subagent_type: "Flow",   // .claude/agents/flow.md
  prompt: "Audita <target>. Contexto deterministic phase 1: <phase1_findings>. Carrega docs/flows/_catalog.md + docs/flows/<target>.md + docs/product.md + docs/flow-heuristics.md. Retorna handoff caveman YAML."
})
```

Flow agent é **stateless com tool whitelist** (Read, Grep, Glob — sem Edit/Write/Bash). Retorna handoff YAML caveman com `journey_health` + `issues[]` + `personas`.

## Phase 3 — Combine

Fundir Phase 1 (deterministic) + Phase 2 (LLM). Regras de fusão:

- P1+P2 concordam na mesma `where` → confiança alta, manter sev mais alta.
- Só Phase 1 detectou → finding estrutural (vocab grep, state.extra). Manter.
- Só Phase 2 detectou → taste call LLM (dead end, goodwill, consistency). Manter, marcar `source: llm`.
- Phase 2 flag, Phase 1 limpo → possível falso positivo; investigar antes de reportar como issue.

**Persistir relatório** em `docs/flows/audit-<YYYY-MM-DD>.md`.

### Formato do relatório

```markdown
# Flow Audit — <target> (<date>)

> Gerado por `/flow`. Deterministic + LLM combinados.

## journey_health
- Score: <N>/10 · Banda: <ship|polish|needs_work|redesign>
- Reachability: pass|fail · Dead ends: <N> · Vocab violations: <N> · State.extra fragile: <N>

## Issues

### P0
<issues P0 — se nenhum, omitir seção>

### P1
<issues P1>

### P2–P3
<issues P2–P3>

## AI-slop de fluxo
<S1–S5 findings, ou "Nenhum detectado">

## Personas
- **Diego** (ativo 4×/sem): <1-frase trava ou ok>
- **Vini** (iniciante): <1-frase trava ou ok>
- **Aline** (avançada): <1-frase trava ou ok>

## Wins
<2–3 pontos positivos da jornada>

## Vocab violations
| Copy banida | Where | Correto |
|---|---|---|
<tabela ou "Nenhuma">

## Deep link gaps
<rotas estáveis sem mapeamento, ou "Nenhum">

## Next actions
<dispatch sugerido por issue, ordenado por sev>
```

## Phase 4 — Dispatch paralelo (`--dispatch`)

> Só roda se `--dispatch` passado. **Nunca auto-executar sem flag explícita.**

Após Phase 3, classificar issues por tipo e spawnar skills corretoras **em paralelo** (single message, múltiplos Agent calls):

### Mapa issue → skill agent

| Tipo de issue | Skill agent | Persona |
|---|---|---|
| `vocab` — copy banida (`resgatar`, `comprar`) | `/ux-writing` via Agent | Pena |
| `dead_end`, `missing_cta`, `goodwill_depletion` | `/frontend-design` via Agent | Clara |
| Nielsen score ≤ 2 em tela específica | `/theme-critique` via Agent | Júri |
| `celebration_weak`, `reward_flat` | `/theme-bolder` via Agent | Brasa |
| `confetti_spam`, `overload`, `noise` | `/theme-distill` via Agent | — |
| `state_extra_fragility`, `orphan_route` | Reportar a Maestro — não spawnar agent | — |

### Protocolo de spawn paralelo

Agrupar todos os dispatches em **uma única mensagem** com múltiplos `Agent({...})` calls simultâneos. Exemplo com 3 issues:

```
// Dispatchar em paralelo — single message
Agent({
  description: "Pena reescreve copy banida",
  subagent_type: "general-purpose",
  prompt: "Você é Pena (ux-writing skill). Reescreve copy banida encontrada no flow audit <date>. Issues: <vocab_issues_list>. Siga o protocolo de /ux-writing."
})

Agent({
  description: "Clara redesenha dead end",
  subagent_type: "general-purpose",
  prompt: "Você é Clara (frontend-design skill). Cria mockup para dead end em <where>. Issues: <dead_end_issues>. Siga o protocolo de /frontend-design."
})

Agent({
  description: "Júri critica tela com Nielsen baixo",
  subagent_type: "Júri",   // .claude/agents/juri.md
  prompt: "Critica <path> encontrado no flow audit <date> com score Nielsen ≤ 2. Carrega docs/product.md. Retorna handoff caveman."
})
```

**Regras do dispatch paralelo:**
- Máx 4 agents simultâneos — não overloading.
- Não spawnar agent para `state_extra_fragility` / `orphan_route` — esses são Maestro, reportar manualmente.
- Aguardar todos os agents completarem antes de consolidar.
- Consolidar resultados em `docs/flows/dispatch-<date>.md`.

### Gerar sequence.md

Após consolidar, gerar `docs/flows/audit-sequence-<YYYY-MM-DD>.md` no formato compatível com `/sequence`:

```markdown
---
feature: flow-audit-<date>
status: draft
phase: sequence
created: <ISO>
audit_ref: docs/flows/audit-<date>.md
dispatch_ref: docs/flows/dispatch-<date>.md
---

# Audit Sequence — <date>

> Gerado por `/flow --dispatch`. Executar com `/sequence`.

## T-01 [P0] <título curto>
- **Dispatch:** <persona> (<skill>)
- **Where:** <file:line ou route>
- **Fix:** <ação concreta>
- **Verify:** <check binário>

## T-02 [P1] <título curto>
...
```

Tasks ordenadas: P0 → P1 → P2 → P3. Dentro do mesmo sev, vocab violations antes de dead ends.

**Nunca auto-executar o sequence.md.** Usuário aprova e roda `/sequence` manualmente.

## Output final para o usuário

Após Phase 3 (ou Phase 1 se `--quick`):

```
Flow audit completo — <target>

Saúde: <N>/10 · <banda>
Issues: <N P0> · <N P1> · <N P2–P3>

Top 3:
1. [P0/P1] <what> → dispatch: <quem>
2. [P1] <what> → dispatch: <quem>
3. [P1/P2] <what> → dispatch: <quem>

Relatório: docs/flows/audit-<date>.md
[se --dispatch] Dispatch: docs/flows/dispatch-<date>.md
[se --dispatch] Sequence: docs/flows/audit-sequence-<date>.md → rodar com /sequence

Próximo passo sugerido:
/<skill> <args>  — <1-frase motivo>
```

**Nunca** auto-rodar a próxima skill. Usuário escolhe.

## Anti-patterns desta skill

- ❌ Rodar sem `docs/product.md` — vocab audit fica cego.
- ❌ Pular Phase 1 (deterministic) — vocab grep e state.extra scan são baratos e precisos.
- ❌ Auditar em-cabeça — sempre delegar ao agent Flow (Phase 2).
- ❌ Auto-executar dispatch ou sequence. Flow diagnostica; dispatch só com `--dispatch` explícito.
- ❌ Spawnar agents de dispatch sequencialmente — devem ser paralelos (single message).
- ❌ Gerar sequence.md sem `--dispatch` flag — custo extra sem consentimento.
- ❌ Persistir `audit-{date}.md` sem combinar Phase 1 + Phase 2 — relatório parcial.
- ❌ Dispatchar `state_extra_fragility`/`orphan_route` para agent — são Maestro.

## Integração com outras skills

| Output do audit | Próxima skill |
|---|---|
| Vocab violation (`resgatar`, `comprar`) | `/ux-writing` (Pena) |
| Dead end, missing CTA, goodwill depletion | `/frontend-design` (Clara) |
| Tela específica Nielsen ≤ 2 | `/theme-critique` (Júri) |
| State.extra fragility, orphan route | Maestro (manual) |
| Celebração tímida mid-journey | `/theme-bolder` |
| Confetti-spam em todo success | `/theme-distill` |

## Quando NÃO rodar

- Feature nova sem telas construídas — sem código pra auditar.
- Logo após port grande (`/theme-port`) — deixa assentar antes de auditar o fluxo.
- Critique de tela única — `/theme-critique` tem Nielsen 10 e é mais cirúrgico.
- Em PR de lógica pura (data/domain/controllers sem widget novo).
