---
name: opus-execute
description: Delegates a well-specified implementation task to a Sonnet sub-agent running in an isolated context window (default background) so the main Opus conversation stays open without ever pushing Sonnet over its window. Packages a self-contained brief (5 sections — Context · Files · Acceptance · Constraints · Style) from the current conversation, dispatches via the Agent tool with `model: sonnet, run_in_background: true`, optionally tracks dispatches at `.design-spec/state/opus-execute/<date>.jsonl`. Triggered by `/opusexecute`, `/oe`, "executa com sonnet", "delega pra sonnet", "send this to sonnet", "execute in background". Skip when the task needs interactive choices, exploratory back-and-forth, or when a useful self-contained brief cannot be written.
---

# Skill: opus-execute (`/opusexecute`) — Sonnet worker for an Opus conversation

## Triggers

- **English:** `/opusexecute`, `/oe`, `/opusexecute --from-task <feature>/T-<id>`, "send this to sonnet", "execute on sonnet", "delegate to sonnet", "run this in the background", "fire and forget this implementation", "run task T-X on sonnet"
- **Português:** `/opusexecute`, `/oe`, `/opusexecute --from-task <feature>/T-<id>`, "executa com sonnet", "delega pra sonnet", "manda pra sonnet", "roda em background", "executa a task T-X com sonnet"
- **Natural cue:** the main conversation is on Opus, the next ask is an *implementation* well enough specified that you could write it on paper, and you want to keep talking instead of waiting. The **primary flow** is `Opus → tasks.md → Sonnet executes` (see Pattern 4 below).

## Why this skill exists

Opus 4.7 (1M context) lets a single conversation carry decisions, architectural backstory, and many file reads without overflowing. Sonnet's window is smaller. When `model: opusplan` auto-switches to Sonnet on plan-mode exit, the inherited Opus context can overflow Sonnet — you lose history or the session breaks.

The fix is structural: **never switch the main model.** Keep Opus all the way through the conversation. When implementation time comes, fork a fresh, isolated context running Sonnet (via the `Agent` tool), feed it a self-contained brief, let it work in the background, and continue conversing on Opus.

The `Agent` tool already supports `model: "sonnet"` and `run_in_background: true`. This skill exists because the primitive is easy to misuse — a thin brief produces thin output. This skill enforces the discipline.

## Primary flow: `Opus → tasks.md → Sonnet`

The skill's most common use case:

1. **Opus designs.** Conversational session in Opus produces `.specs/features/<feature>/{spec.md, design.md, tasks.md}` via `/tlc-spec-driven` (or `/Júri` → `/Clara` → `/sequence`). Each task in `tasks.md` is atomic (~30 min), has explicit `Where`, `Done when`, and `Verify` blocks.
2. **Opus dispatches.** `/opusexecute --from-task <feature>/T-<id>` reads the task entry, the spec, and the design, then synthesizes a self-contained brief and fires it to Sonnet in background.
3. **Sonnet executes.** Fresh context, reads only the files declared in `Where`, edits, runs `Verify`, returns a single summary.
4. **Opus continues.** Main conversation never overflowed, never switched model. The result comes back as a notification you read between Opus turns.

This is the canonical loop. Other patterns (free-form briefs, paralllel batches, blocking gates) are supported but secondary.

## Pre-requisite — settings.json model field

For this skill to deliver its value, the main session model must **not** be `opusplan` (which silently falls back to Sonnet on plan-mode exit). Set the model explicitly to `opus`:

```jsonc
// .claude/settings.json or ~/.claude/settings.json
{ "model": "opus" }
```

If the user is on `opusplan` and invokes this skill, surface the trade-off in the first response: *"Você está em `model: opusplan` — esta skill assume `model: opus`. Sem isso, ao sair do Plan Mode você cai pra Sonnet de qualquer jeito e o ganho some. Quer que eu sugira o ajuste em `settings.json`?"*

## Quando usar (e quando NÃO)

| Sinal | Decisão |
|---|---|
| Implementação bem especificada, todos os arquivos identificados, critério de aceitação claro | ✅ Delegar |
| Refactor mecânico, port HTML→Flutter já desenhado, sweep de tokens, adicionar testes | ✅ Delegar |
| 3+ arquivos pra editar com dependências entre eles, mas o caminho está claro | ✅ Delegar |
| Precisa fazer perguntas durante a execução, escolher entre opções em runtime | ❌ Não delegar — sub-agente é fire-and-forget |
| Brief que você não consegue escrever em <10 frases auto-contidas | ❌ Não delegar — significa que você ainda está descobrindo o problema |
| Debugging exploratório, tracing de bug com múltiplas hipóteses | ❌ Não delegar — precisa do back-and-forth |
| Edição trivial (1 linha, 1 arquivo) | ❌ Não delegar — overhead de dispatch passa o ganho |

Regra de ouro: **se você não conseguiria mandar o brief pra um colega humano por Slack sem follow-up, não delega.**

## Workflow

### Step 1 — Gather context from the current conversation

Antes de despachar, **você** (Opus na sessão principal) tem que reunir o que o sub-agente precisará:

1. **Files** — todos os paths que o sub-agente vai precisar ler/editar. Liste explicitamente; não diga "the relevant files".
2. **Recent decisions** — se a conversa Opus decidiu X em vez de Y nas últimas mensagens, anota explicitamente. O sub-agente não vai ver o histórico.
3. **Constraints já estabelecidos** — convenções, anti-patterns, tokens, regras de CLAUDE.md aplicáveis. Cite explícito mesmo que pareça óbvio.
4. **Acceptance** — como o sub-agente sabe que terminou? Quais comandos rodar pra validar? Quais saídas esperadas?

Se algum dos 4 está vago, **pare e refine antes de despachar.** Brief ruim → output ruim → dispatch desperdiçado.

### Step 2 — Pack the brief using the recipe

Leia `references/brief-recipe.md` (5 seções obrigatórias com exemplos bad/good). Estrutura mínima:

```
## Context
<1-3 sentences — what's being built and why, the part that matters>

## Files
- <path>:<role>  (e.g. lib/features/x/page.dart:edit, lib/core/theme/app_colors.dart:read-only)
- ...

## Acceptance
- <bullet 1 — observable outcome>
- <bullet 2 — validation command + expected output>
- ...

## Constraints
- <bullet — convention/anti-pattern/token rule>
- ...

## Style
- <terse instruction — verbosity, comments, output format>
```

Refuse to dispatch if any section is empty. A skipped section means the next message back from the sub-agent will be a clarification question — which it can't ask, so it'll guess.

### Step 3 — Dispatch via Agent tool

Default invocation:

```
Agent({
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: <brief from Step 2>,
  run_in_background: true,
  description: "<5-word task summary>"
})
```

**Default flags:**

| Flag | Default | Notes |
|---|---|---|
| `model` | `sonnet` | Sonnet 4.6 (or current) — good balance of capacity + cost. |
| `run_in_background` | `true` | User keeps conversing on Opus. Background task notifies on completion. |
| `subagent_type` | `general-purpose` | Has full tool access. Use a specialized agent (Explore, Júri, Atelier) when the task fits one. |

**User overrides (parse from `$ARGUMENTS`):**

| Flag | Effect |
|---|---|
| `--from-task <feature>/T-<id>` | **Primary flow.** Read `.specs/features/<feature>/tasks.md`, locate task `T-<id>`, expand into a brief using spec/design as Context/Constraints. See Pattern 4 below. |
| `--from-tasks <feature> --range T-XX..T-YY` | Batch dispatch — multiple tasks in parallel as separate sub-agents. Respects `Depends on` field (refuses to dispatch a task whose dependency is incomplete). |
| `--from-tasks <feature> --phase <N>` | Dispatches all tasks of phase N from the `Execution Plan` block (e.g., `--phase 2` of `cadastro-convidado/tasks.md` fires T5+T6 in parallel). |
| `--blocking` | Run in foreground; main session waits. Use when downstream step depends on the result. |
| `--model haiku` | Trivial mechanical task. ~5x cheaper, smaller context. |
| `--model opus` | Critical task that the brief acknowledges Sonnet would struggle with. Rare — usually means you should have implemented inline. |
| `--agent <type>` | Use a specialized subagent (`Júri`, `Atelier`, `Explore`, `Flow`). Honors that agent's tool whitelist. |
| `--no-track` | Skip the dispatch ledger entry. |

### Step 4 — Track the dispatch (optional, on by default)

Append a JSONL entry at `.design-spec/state/opus-execute/<YYYY-MM-DD>.jsonl`:

```json
{"ts":"<ISO>","task_id":"<from Agent return>","model":"sonnet","background":true,"description":"<short>","brief_chars":<n>,"target_files":["..."]}
```

Skip if `--no-track`, or if `.design-spec/` doesn't exist in the project (don't create the dir for tracking alone — that's the project's call).

### Step 5 — Confirm dispatch to the user

Single message back to user, terse:

```
Despachado pra Sonnet em background — task_id: <id>.
Brief: <2-line summary>.
Notificação chega quando terminar; pode seguir conversando.
```

If `--blocking`, instead say: *"Rodando em foreground; te aviso quando voltar."* and wait.

## Brief-recipe — quick reference

Full recipe with bad/good examples at `references/brief-recipe.md`. Cheat sheet:

| Section | Length | Bad | Good |
|---|---|---|---|
| Context | 1–3 sentences | "Implementa o novo modal" | "Modal de confirmação de resgate de cupom. Substitui o `showDialog` atual em coupons/page.dart:142. Decidimos AlertDialog em vez de bottom sheet porque a ação é destrutiva." |
| Files | 1 line each | "Os arquivos da feature de cupons" | "lib/features/coupons/presentation/pages/coupon_detail_page.dart:edit · lib/core/widgets/app_dialog.dart:reference-only · docs/design-tokens.md:read-only" |
| Acceptance | Observable | "Funcionar" | "`flutter analyze` sem warnings; modal renderiza em light+dark; tap fora não fecha; CTA `Resgatar agora` aciona `couponController.redeem()`." |
| Constraints | Explicit | "Seguir o tema" | "Usar `AppDialog` (não Material `AlertDialog`); copy pt-BR do `docs/product.md` §4.5 (arco Querer→Pegar→É seu); sem `Color(0xFF...)`." |
| Style | Terse | — | "Não escreva comentários explicando o que o código faz. Sem TODOs. Sem prints. Sem warnings." |

## Patterns

### Pattern 1 — Sequenced background dispatches

User pediu 3 tasks independentes em sequência:

1. Dispatch all three with `run_in_background: true` in a single message (parallel).
2. Main Opus session continues — discuss next steps, plan next batch.
3. As each completes, notification surfaces; merge results back into conversation context.

This is the highest-ROI usage: 3 sub-agentes trabalhando em paralelo enquanto a conversa principal continua.

### Pattern 2 — Specialized sub-agent with `--agent`

For a design critique, `--agent Júri` honors the Júri agent's tool whitelist (Read/Grep/Glob, no Edit/Write/Bash). Same dispatch pattern, but the sub-agent's behavior is shaped by `.claude/agents/juri.md` instead of the bare general-purpose contract.

### Pattern 3 — Blocking for sequential gate

When step B depends on step A's result, dispatch A with `--blocking`, await, then dispatch B with the result encoded in B's brief.

### Pattern 4 — Dispatch from `tasks.md` (primary flow)

The shape user uses most often. `.specs/features/<feature>/tasks.md` (tlc-spec-driven format) carries atomic tasks with structured `What` / `Where` / `Done when` / `Verify` fields. Each task is already 80% of a brief — this pattern fills the remaining 20% from `spec.md` and `design.md` automatically.

#### Invocation

```
/opusexecute --from-task cadastro-convidado/T-01
/opusexecute --from-tasks cadastro-convidado --range T-01..T-04
/opusexecute --from-tasks cadastro-convidado --phase 2
```

#### Workflow

1. **Locate feature.** Parse `<feature>` from arg. Verify `.specs/features/<feature>/` exists. If not, halt with friendly error.
2. **Read structured inputs (3 files):**
   - `.specs/features/<feature>/tasks.md` — find the task entry (`### T<id>: <title>`)
   - `.specs/features/<feature>/spec.md` — extract problem statement / requirements (Context for brief)
   - `.specs/features/<feature>/design.md` — extract decisions / patterns / anti-patterns (Constraints for brief)
3. **Parse task block.** Extract:
   - `What` → first line of Context section
   - `Where` → Files section (every path becomes a row with `:edit` or `:read-only` inferred)
   - `Depends on` → if any T-id listed is NOT marked complete, **halt** with warning: "T-<id> depends on T-<dep>, which is not complete. Run dispatch on T-<dep> first."
   - `Reuses` → add referenced files as `:reference-only` in Files
   - `Done when` → Acceptance section bullets (verbatim)
   - `Verify` → final bullet in Acceptance, with the command literal
   - `Commit` → goes into the brief's Style section as "When done, suggest commit message: `<verbatim>`"
4. **Synthesize 5-section brief** using `references/brief-recipe.md` template:
   - Context: `What` + 1–2 sentence summary from `spec.md` problem statement
   - Files: `Where` paths + `Reuses` refs
   - Acceptance: `Done when` bullets + `Verify` command
   - Constraints: project-wide (CLAUDE.md baseline) + relevant `design.md` decisions filtered by task scope
   - Style: defaults + commit message suggestion
5. **Dispatch.** Same `Agent({ model: "sonnet", run_in_background: true, ... })` call as base workflow.
6. **Track.** Ledger entry includes `feature` and `task_id` fields so progress can be tied back to `tasks.md`.

#### Confirmation message

```
Despachado T-<id> de <feature> pra Sonnet — task_id: <agent-id>.
What: <task title>.
Where: <N> file(s) to edit, <M> reference(s).
Verify: <command>.
Pode seguir conversando; notificação chega ao terminar.
```

#### Batch dispatch (`--range` / `--phase`)

When dispatching multiple tasks in one invocation:

- Tasks **without** mutual dependencies fire in parallel (one `Agent` call per task, all in a single message → CC runs them concurrently).
- Tasks **with** dependencies must run sequentially. If `--range` includes such a chain, halt and ask user to confirm: "T-05 depends on T-04. I can dispatch T-04 blocking, then T-05 in background. OK?" — never auto-serialize without consent.
- Each sub-agent in the batch gets an independent brief (same recipe), so failure of one doesn't poison the others.
- `--phase N` reads the `Execution Plan` block at the top of `tasks.md` to find phase N's task list. Lighter than `--range` for users with structured plans.

#### Anti-pattern specific to this flow

- ❌ Dispatching a task whose `Done when` is vague ("funciona", "passa nos testes" sem comando concreto). Halt and ask user to refine the task before dispatching — bad tasks produce bad dispatches.
- ❌ Ignoring `Depends on`. Even if user insists, surface the warning explicitly: "T-05 depends on T-04 which is incomplete — dispatching anyway?" One round-trip cheap; broken state expensive.
- ❌ Dispatching all of `tasks.md` in a single `--range T-01..T-N`. Phase-by-phase is the discipline; `tasks.md` is structured around phases for a reason.

## Anti-patterns

- ❌ Dispatching with a thin brief ("implementa isso aí") — Sonnet vai inventar. Brief precisa carregar TUDO que o histórico Opus carregaria.
- ❌ Dispatchar e ficar em `--blocking` por hábito — anula o ganho de paralelismo. Default é background; bloqueante é exceção.
- ❌ Usar `--model opus` rotineiramente — se o trabalho exige Opus, não delega; faz inline.
- ❌ Pular acceptance — sub-agente "termina" quando achar que terminou. Sem critério explícito, output fica meia-boca.
- ❌ Embedar comentários da conversa Opus no brief sem editar ("o usuário disse X, depois mudou de ideia, depois pediu Y") — passa pro Sonnet ruído. Filtra.
- ❌ Dispatchar pra mudança de arquitetura ("redesenha a feature de cupom inteira") — escopo enorme com decisões implícitas. Quebra em N tasks bem-especificadas.

## Integração com outras skills

| Vindo de | Sinal | Despacho típico |
|---|---|---|
| `/tlc-spec-driven` produziu `.specs/features/<f>/tasks.md` | tasks aprovadas, prontas pra executar | `/opusexecute --from-tasks <f> --phase 1` — fase por fase |
| `/sequence` emitiu tasks.md atômicas | 1 task = 1 dispatch | `--from-task <f>/T-<id>` (ou `--range` em phase sem dependência) |
| `/theme-critique` (Júri) emitiu Issues P0/P1 | Cada P0 vira 1 dispatch | `--agent Júri` p/ re-critique pós-fix; default p/ fix mecânico |
| `/theme-port` ports HTML→Flutter | Conversão por widget | Default sonnet; `--blocking` se port crítico que feed o próximo port |
| `/theme-audit` listou top offenders | Sweep mecânico de hardcode | Default sonnet, `--no-track` ok p/ sweeps repetitivos |
| `/Clara` produziu mockup HTML | Aguarda critique antes de port | NÃO despachar /theme-port até Júri APPROVE |

## Output esperado

Apenas 1 mensagem por dispatch, terse:

```
Despachado pra <model> em <background|foreground> — task_id: <id>.
Brief: <2-line summary>.
<contexto extra de quando|onde a notificação chega>
```

E, em paralelo, o append no ledger se `.design-spec/state/opus-execute/` existir.

## Referência rápida — settings recommendation

```jsonc
// ~/.claude/settings.json — recomendado p/ usuários frequentes desta skill
{
  "model": "opus",                  // não opusplan; mantém Opus o tempo todo
  "permissions": {
    "allow": ["Agent"]              // já deve estar liberado, mas explícito não machuca
  }
}
```

`/opusexecute` não força esse setting (não tem como), mas avisa quando detecta `opusplan`.
