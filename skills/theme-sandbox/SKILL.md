---
name: theme-sandbox
description: Orchestrator for the visual sandbox cycle. Reads a Critic handoff (P0–P1), invokes `/theme-prompt` to compose the Stitch brief, spawns the Atelier agent that generates N variations via the Stitch MCP, downloads screenshots+HTML, and proposes either re-critique via `/theme-critique` or port via `/theme-port` based on the user's pick. Use when a screen has a pending critique and you want to explore 3 visual paths before porting from Figma. Triggers: `/Orchestrator`, `/Orquestrador`, `/theme-sandbox <critique-path>`, "explore variations", "manda pro Stitch".
---

# Skill: theme-sandbox (`/theme-sandbox`) — persona **Orquestrador** (English: **Orchestrator**)

## Triggers

- **English:** `/Orchestrator`, `/theme-sandbox`, "explore visual variations", "send to Stitch", "3 visual paths", "visual sandbox"
- **Português:** `/Orquestrador`, `/orquestrador`, `/theme-sandbox`, "explora variações", "manda pro stitch", "sandbox visual", "3 caminhos"
- **Natural language:** "I have a critique handoff and want 3 mockup options"; "let's explore before porting"

Orchestrator. Não chama Stitch direto — delega ao agent **Atelier**. Não compõe prompt — delega ao **`/theme-prompt`**. Não critica — delega ao **`/theme-critique`** depois. O job é amarrar o pipeline:

```
Júri (critique) ──▶ /theme-prompt (brief) ──▶ Atelier (gera N) ──▶ /theme-critique (compare) ──▶ user picks ──▶ /theme-port
```

## Posição no ciclo

```
/theme-port (Figma)        ┐
/theme-critique (Júri)     ├─▶ se P0–P1 pesado e exploração visual ajuda
/theme-audit (Lupa)        ┘
                                  │
                                  ▼
                          /theme-sandbox (Atelier)
                                  │
                                  ▼
                          /theme-critique compare
                                  │
                                  ▼
                          /theme-port (porta escolhida)
```

Sandbox é **opcional**. Skip quando:
- Critique já tem fix óbvio (theme-bolder/quieter/distill resolvem direto).
- Budget Stitch apertado (ver Cost section).
- Tela é triagem rápida, não merece 3 caminhos.

Use quando:
- P0 dominante é estrutural ("recompensa invisível", "hero errado", "above-fold mal priorizado") e várias soluções são plausíveis.
- Decisão precisa de mockup pra alinhar com stakeholders/usuário antes de gastar Flutter.
- `/theme-critique` recomendou explicitamente exploração.

## Inputs

- **Path para handoff Júri** (`/theme-sandbox .claude/handoffs/critique-2026-04-28T-explorar.yaml`) — caminho canônico.
- **Target + intent** (`/theme-sandbox lib/features/feed/ "pontos invisivel"`) — fallback quando não há critique.
- **`--variants N`** (default 3, max 5) — controla budget.

## Prerequisites

- **Stitch MCP conectado.** `mcp__stitch__*` deve aparecer em `claude mcp list`. Se ✗, parar e instruir: `npx @_davideast/stitch-mcp init` no host + reiniciar Claude Code.
- **gcloud autenticado** com projeto Stitch ativo. `npx @_davideast/stitch-mcp doctor` deve passar all checks.
- **Tools Stitch deferred.** Antes do spawn Atelier, garantir que tools estão carregadas via `ToolSearch select:mcp__stitch__create_project,mcp__stitch__generate_screen_from_text,mcp__stitch__get_screen,mcp__stitch__get_screen_code,mcp__stitch__get_screen_image`.
- **`docs/product.md` ≥2KB.** Sem isso, `/theme-prompt` falha — sandbox aborta.
- **Agent Atelier disponível.** `.claude/agents/atelier.md` deve existir no projeto.

## Workflow

### Step 1 — Resolver input

1. Se arg é path `.yaml` → assumir handoff Júri. Read e validar (`from_agent: juri`, `consumed: false`, `issues[]` não vazio).
2. Se arg é dir/path Flutter → fallback intent free-text. Pedir ao usuário 1-frase do P0 dominante se não veio em arg.
3. Se sem arg → listar `.claude/handoffs/critique-*.yaml` ordenado por timestamp desc, marcar `consumed: false`, perguntar qual usar.

### Step 2 — Compor brief via `/theme-prompt`

Invocar skill `/theme-prompt` com mesmo input. Resultado:
- `prompt_text` — bloco Content+Style+Layout pronto pra Stitch
- `validation` — checklist (tudo deve passar antes de spawn Atelier)

Se `validation` falhar em qualquer item, parar e reportar ao usuário (não desperdiçar créditos).

### Step 3 — Spawn Atelier agent

Usar Agent tool com `subagent_type: "Atelier"`:

```
Agent({
  description: "Atelier: 3 variations sandbox",
  subagent_type: "Atelier",
  prompt: <<EOF
Critique handoff: <path>
Variants requested: <N>
Brief prompt (Content+Style+Layout):
<prompt_text do Step 2>

Project context:
- target: <target>
- axis: <next_action.axis>
- primary_p0: <P0 dominante caveman>

Eixos sugeridos pras variations (Atelier escolhe combinação distinta):
- A: drenched (color commitment alto)
- B: display-hero (tipografia hero exagerada)
- C: bento-stack (composição modular)

Output: handoff atelier YAML em .claude/handoffs/atelier-<timestamp>.yaml + cache em .claude/handoffs/atelier-cache/<timestamp>/
Lembrete: marcar critique input como consumed: true ao terminar.
EOF
})
```

Atelier roda isolado (stateless, contexto próprio). Retorna handoff atelier path.

### Step 4 — Validar handoff atelier

1. Read handoff retornado. Validar:
   - `from_agent: atelier`
   - `variations[]` length == requested
   - Cada variation tem `screenshot_url`, `html_url`, `cached_at` populados
   - `cached_at` files existem no disco
2. Se algo faltar, mostrar warning e proceder com o que tem.

### Step 5 — Re-critica compare (opcional, recomendado)

Sugerir ao usuário rodar `/theme-critique` em modo compare:

```
Suggested: /theme-critique --compare .claude/handoffs/atelier-<timestamp>.yaml
```

Esse modo do critique (Júri compara variations side-by-side, pontua cada uma Nielsen, aponta winner ou suggested merge) ainda não existe — se user aceitar, criar issue/TODO. Por enquanto, Júri pode rodar standalone em cada variation HTML, mas custa.

**Atalho prático até `--compare` existir:** abrir os 3 screenshots no visualizador do OS e deixar user escolher. Listar paths absolutos pro user clicar:

```
Variations geradas:
  A. .claude/handoffs/atelier-cache/<ts>/hero-pontos-drenched.png — pontos display + surface gameAccent drenched
  B. .claude/handoffs/atelier-cache/<ts>/cupom-bento-stack.png — cupom card hero, chips abaixo
  C. .claude/handoffs/atelier-cache/<ts>/checkin-fab-restrained.png — FAB check-in fixo, surface limpa

Qual seguir? (A/B/C/regen)
```

### Step 6 — Pick + handoff a `/theme-port`

Quando user escolhe (ex: "B"):

1. Read `cached_at` do HTML correspondente.
2. Marcar `consumed: true` no handoff atelier (Edit YAML).
3. Sugerir comando final:

```
Suggested: /theme-port --from-stitch .claude/handoffs/atelier-cache/<ts>/cupom-bento-stack.html target=<target>
```

Esse modo `--from-stitch` do `/theme-port` (extrai widths/heights/hierarquia do HTML, descarta Tailwind classes, aplica o tema do projeto) é o passo 5 do plano sandbox e ainda não existe. Por enquanto, abrir o HTML no browser e usar como referência manual pro `/theme-port` regular.

### Step 7 — Report

```
Sandbox completo:
- Critique: <path> (P0: <primary_p0>)
- Variations geradas: <N>
- Cache: .claude/handoffs/atelier-cache/<ts>/
- Créditos usados: <N>
- Próximo: /theme-port --from-stitch ... (ou re-rodar /theme-sandbox --variants 5 se nenhuma serviu)
```

## Cost / Budget

Stitch free tier = **400 créditos/dia**. Cada `generate_screen_from_text` = 1 crédito.

| Variants | Créditos | % do dia |
|---|---|---|
| 3 | 3 | 0.75% |
| 5 | 5 | 1.25% |
| 1 feature × 5 telas × 3 variants | 15 | 3.75% |

Hard cap default 3. Aceitar `--variants 5` só quando user pede explícito. **Nunca** loop automático regenerando — sempre confirmar com user.

## Error handling

| Erro | Ação |
|---|---|
| Stitch MCP não conectado | Parar, instruir `npx @_davideast/stitch-mcp init` |
| 401 / auth | `gcloud auth login` + `npx @_davideast/stitch-mcp doctor` |
| 429 / rate limit | Reportar créditos restantes, sugerir voltar amanhã |
| Variation com screenshot vazio | Skip variation no relatório, reportar warning, não regenerar automaticamente |
| Atelier retorna handoff malformado | Mostrar erro, oferecer re-spawn (custa créditos novos) |

## Anti-patterns

- ❌ Regenerar automaticamente quando user diz "nenhuma serve". Sempre pedir intent ajustada antes — pode ser problema do prompt, não do Stitch.
- ❌ Spawn Atelier sem validar `/theme-prompt`. Brief ruim = créditos queimados.
- ❌ Pular cache local. URLs Stitch expiram (24h). Cache `.claude/handoffs/atelier-cache/` é canônico.
- ❌ Esquecer de marcar critique input `consumed: true` após sandbox completar. Atelier deveria fazer; sandbox confirma.
- ❌ Tentar portar HTML class-by-class. HTML Stitch é **estrutural**; cores e fonts vêm do tema do projeto via `/theme-port`.
- ❌ Rodar sandbox em telas onde fix é óbvio (rename, swap token, ajuste de spacing). Sandbox é pra exploração estrutural, não polish.
- ❌ Aceitar `--variants 6+`. Cap é 5 — força disciplina criativa em cima de budget e atenção do user.

## Saída esperada (resumo final ao user)

```
✓ Sandbox: lib/features/feed/presentation/
  Critique: .claude/handoffs/critique-2026-04-28T-explorar.yaml (P0: pontos invisivel + cupom abaixo dobra)
  Variants: 3 (drenched / display-hero / bento-stack)
  Cache:    .claude/handoffs/atelier-cache/2026-04-28T16-30/
  Crédito:  3/400 usados hoje

A. hero-pontos-drenched.png      — pontos display + surface gameAccent
B. cupom-bento-stack.png         — cupom hero, chips abaixo
C. checkin-fab-restrained.png    — FAB check-in fixo, surface limpa

Qual seguir? (A/B/C — depois /theme-port --from-stitch <html>)
```
