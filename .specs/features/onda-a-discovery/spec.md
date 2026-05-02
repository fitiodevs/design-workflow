# Feature: onda-a-discovery

> Onda A do plano `design-spec-driven` (`docs/design-spec-driven-plan.md`). Júri ganha modo Discovery — entrevista estruturada, auto-sizing, pre-scan brownfield, geração de docs (PRD + skeletons) e roteamento priorizado para as 13 skills atômicas.

**Status:** Draft (pronto pra execução)
**Owner:** fitiodev
**Created:** 2026-05-02
**Sized:** Large (novo modo, novos artefatos, gates novos, regressão obrigatória do critique atual)
**Source plan:** `docs/design-spec-driven-plan.md` §5 / REQ-A1..REQ-A6 / §8 acceptance Onda A
**Locked decisions consumidas:** 6 memory files em `~/.claude/projects/.../memory/`. Não contradizer.

---

## 1. Contexto

`design-workflow` v0.2.0 entrega 13 skills atômicas, todas reativas: usuário tem que saber quais rodar e em que ordem. Não há camada de descoberta — em greenfield, não existe `docs/product.md` (gate hard de várias skills); em brownfield, ninguém audita antes de prescrever fix. Resultado: skills são powerful operators sem orquestração — "ferramentas sem mestre de obras".

A persona Júri (skill `theme-critique`) já é a voz de juízo do sistema. O plano (memória `decision_juri_dual_mode.md`) decide: **mesma persona, dois modos**, dispatch por shape do argumento:

- `/juri` (sem args) → Discovery (entrevista, gera PRD, roteia)
- `/juri <flutter-path>` → Critique (Nielsen, AI-slop — preservado)
- `/juri --discuss <topic>` → modo informal (sem docs, scaffolding agora; refino completo em Onda C)
- `/juri --resume <feature>` → retoma entrevista parcial

Onda A constrói o modo Discovery preservando 100% do Critique existente. Sem Discovery, Ondas B/C/D ficam sem fundação ("Ralph rodando em chão de areia" — `decision_ralph_separate_skill.md`).

## 2. Goal

Após esta feature, o repo deve:

- Suportar 4 formas de invocação `/juri` com workflows distintos.
- Detectar greenfield vs brownfield automaticamente (>3 sinais).
- Rodar `/theme-audit` silencioso quando brownfield → entrevista usa números reais.
- Conduzir entrevista de 4 blocos (Produto / Tom / Identidade / Stack), 1 bloco/turno, recusando vago.
- Gerar artefatos por modo: `discovery.md` sempre; `docs/{product,design,design-tokens,PRD}.md` skeletons em greenfield/full; só `discovery.md` + `PRD.md` em brownfield.
- Emitir plano de ação priorizado mapeando para skills existentes — **nunca auto-rodar**.
- Persistir entrevista parcial e suportar resume.
- Não quebrar nenhum trigger ou eval existente do critique.

## 3. Non-goals

- **Não** implementar pause/resume cross-feature de Onda C — Onda A só faz `--resume <feature>` da entrevista atual; pause global fica pra C.
- **Não** implementar discuss-mode completo — só scaffolding do flag `--discuss`. Comportamento socrático completo é REQ-C2.
- **Não** rodar nenhuma das 13 skills automaticamente. Roteamento sai como recomendação ordenada com ETA + skill name.
- **Não** mudar nada do Critique mode — comportamento, output, persona, gates: idênticos.
- **Não** adicionar nova skill no diretório `skills/` (ver design.md §D-01) — Discovery vive dentro de `theme-critique/` via dispatch + references.
- **Não** criar novas personas. Júri é Júri em ambos os modos. `voice_dna` igual.
- **Não** integrar com Stitch/Figma MCP nesta onda. Discovery é texto e questões; visual exploration é Onda B (Compose).
- **Não** auto-aprovar `discovery.md` — sempre nasce `status: draft`. Aprovação humana fica pra Onda B (gate Compose).

## 4. Requirements

### REQ-A1 — Júri dual-mode dispatch

- **REQ-A1.1** `/juri` sem argumentos detecta sinal "sem path" e entra em discovery mode.
- **REQ-A1.2** `/juri <flutter-path>` (path existente em `lib/` ou arquivo `.dart`) entra em critique mode (workflow atual).
- **REQ-A1.3** `/juri --discuss <topic>` entra em discuss mode (scaffolding mínimo; loga "discuss mode em desenvolvimento — Onda C; usa `/juri` para discovery formal").
- **REQ-A1.4** `/juri --resume <feature>` lê `.design-spec/features/<feature>/discovery.md` se status `in_progress`, retoma do bloco onde parou.
- **REQ-A1.5** Ambiguidade (path passado mas começa com `--`) resolve por ordem: flag → path → discovery default.
- **Verificação:**
  - Eval scriptada: 4 prompts (sem args / com path / com `--discuss` / com `--resume`) → 4 dispatches distintos verificáveis por log de entrada do workflow.
  - Regressão: rodar evals atuais do critique (se existirem) ou prompts manuais "critica `lib/features/x`" → workflow critique idêntico.

### REQ-A2 — Auto-sizing detection

- **REQ-A2.1** Script `scripts/detect_mode.py` detecta greenfield vs brownfield via:
  - `git log --oneline | wc -l` (commits totais)
  - `find lib -name "*.dart" -not -path "*/generated/*" | wc -l` (Dart files reais)
  - `test -f docs/product.md && wc -c < docs/product.md` (presença + tamanho)
  - `test -d lib/core/theme || lib/theme || lib/shared/theme` (tema estabelecido)
  Heurística: greenfield se commits<10 AND dart_files<5 AND product.md ausente. Brownfield caso contrário.
- **REQ-A2.2** Modo recomendado mapeia para tier: greenfield→`full+greenfield`, brownfield→`full` (com pre-scan).
- **REQ-A2.3** Override via `/juri --mode quick|light|full|greenfield` (pula detecção).
- **REQ-A2.4** Tier sizing dirige output:
  - **quick**: só `discovery.md` mini (3 perguntas) + recomendação top-3.
  - **light**: `discovery.md` completo + PRD curto, sem skeletons.
  - **full**: `discovery.md` + `PRD.md` per-intervention + appends a `docs/design.md` (brownfield) ou skeletons (greenfield).
  - **greenfield**: `discovery.md` + skeletons completos `docs/{product,design,design-tokens,PRD}.md`.
- **Verificação:**
  - `python scripts/detect_mode.py` em repo vazio → emite `{"mode": "greenfield", ...}`.
  - Mesmo script em repo com 100 commits + 50 dart files + product.md presente → `brownfield`.
  - Override `--mode quick` em greenfield gera só mini-discovery (sem skeletons).

### REQ-A3 — Structured interview protocol

- **REQ-A3.1** Júri faz 4 blocos em ordem fixa: **Produto** (3 perguntas) → **Tom** (3) → **Identidade** (3) → **Stack** (2-3). Total 11–12.
- **REQ-A3.2** 1 bloco por turno; pausa pra resposta antes do próximo bloco. Nunca despeja todas as perguntas.
- **REQ-A3.3** Recusa respostas vagas com lista de 12 termos banidos (`reference/discovery-vague-words.md`): "moderno", "clean", "tech", "profissional", "vibrante", "minimalista", "bonito", "user-friendly", "intuitivo", "premium", "elegante", "natural". Re-pergunta pedindo: "exemplo concreto de app/site" + "1 sensação física específica" + "1 anti-reference (o que não pode parecer)".
- **REQ-A3.4** Primeira pergunta é sempre Produto (scene sentence: "Quem usa, em que momento, pra resolver o quê?"). Stack só no bloco 4 — sem `frontmatter` técnico antes de identidade.
- **REQ-A3.5** Cada resposta vaga gera 1 retry; após 2 retries ainda-vagos, Júri persiste a resposta com tag `quality: weak` e move pro próximo bloco (não trava).
- **Verificação:**
  - Eval `vague-user.json` com 12 respostas vagas pré-definidas → Júri recusa ≥10/12 (≥80%) e re-pergunta com formato dado.
  - Inspeção manual: rodar discovery → confirmar ordem Produto→Tom→Identidade→Stack e 1 bloco/turno.

### REQ-A4 — Brownfield pre-scan

- **REQ-A4.1** Modo brownfield: antes da primeira pergunta, Júri roda `python scripts/audit_theme.py lib/` silenciosamente (não exibe ao usuário) e armazena stdout/json em buffer.
- **REQ-A4.2** Perguntas no bloco Stack referenciam achados concretos do audit: "achei 47 hex literals em `lib/features/<x>/` — drift acidental ou cor de marca proposital?" Se audit falha, Júri loga warning e prossegue sem números.
- **REQ-A4.3** Audit completo é apendado a `discovery.md` na seção `## Brownfield audit (pre-scan)`.
- **Verificação:**
  - Repo brownfield com hardcode plantado → discovery output contém grep do número exato em pelo menos 1 pergunta.
  - Repo greenfield → audit não roda; nenhuma pergunta cita números.

### REQ-A5 — Doc generation

- **REQ-A5.1** Júri sempre escreve `.design-spec/features/<feature>/discovery.md` com frontmatter:
  ```yaml
  ---
  feature: <slug>
  status: draft  # draft | in_progress | approved | consumed
  mode: greenfield|brownfield
  tier: quick|light|full|greenfield
  created: <ISO date>
  ---
  ```
- **REQ-A5.2** Tier `greenfield` adicionalmente escreve skeletons em `docs/`:
  - `docs/product.md` — §1 visão / §2 personas / §3 jornada / §4 voz/tom / §5.3 color strategy axis / §7 anti-references / §8 princípios estratégicos. Cada seção tem placeholder `<!-- preencher: ... -->` + 1 exemplo-comentário em PT-BR.
  - `docs/design.md` — princípios de design system (não tokens), pointers para Nielsen + canon visual.
  - `docs/design-tokens.md` — tabelas vazias para palette / typography / spacing / radius.
- **REQ-A5.3** Tier `full` (brownfield) escreve `docs/PRD.md` per-intervention (top 3-5 fixes priorizados) e appenda a `docs/design.md` se existir (não sobrescreve).
- **REQ-A5.4** Júri **NUNCA** edita arquivos em `lib/`. Read-only em código; write-only em `docs/` + `.design-spec/`.
- **REQ-A5.5** Se arquivos `docs/*.md` existirem em greenfield, Júri pergunta antes de sobrescrever. Default = não sobrescrever (recusa).
- **Verificação:**
  - Pós-discovery em greenfield: `git diff lib/` vazio; `ls docs/*.md` lista os 4 arquivos novos.
  - Pós-discovery em brownfield: `git diff lib/` vazio; só `docs/PRD.md` novo + `.design-spec/` populado.
  - Cada skeleton contém placeholders `<!-- preencher` e ≥1 comentário-exemplo.

### REQ-A6 — Routing output

- **REQ-A6.1** Output final do discovery é um plano de ação priorizado (não menu). Schema:
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
  ```
- **REQ-A6.2** Cada item tem `rank, skill, reason, eta, blocks`. Skill names são exatamente das 13 atômicas existentes ou de Ondas futuras (`/design-spec compose`, `/design-spec sequence`, `/design-spec ship`) — não inventa.
- **REQ-A6.3** Júri **nunca** auto-roda a próxima skill (preserva controle do usuário, idêntico ao critique mode).
- **REQ-A6.4** Plan é apendado a `discovery.md` na seção `## Action plan` e ecoado em prosa pro usuário (não mostra YAML cru).
- **Verificação:**
  - Pós-discovery: schema valida via Python `yaml.safe_load`.
  - Skill names em `plan` ⊂ {13 atômicas + 3 orchestration futuras}.
  - Nenhum log de invocação de skill secundária no mesmo turno.

## 5. Out of scope (deferred)

- Discuss-mode completo (REQ-C2 / Onda C).
- Pause cross-feature (REQ-C1 / Onda C).
- Compose/Sequence/Ship phases (Onda B).
- Skill `discovery/` separada — descartado em favor de extensão `theme-critique` (ver design.md §D-01).
- Stack-agnostic adapter (Onda E pós-v1.0).
- Voz/áudio na entrevista — futuro distante.

## 6. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Critique mode regrede silenciosamente após dispatch novo | Média | Alta | Smoke test obrigatório em T-final da Onda; tag `pre-design-spec-driven` para rollback granular |
| Discovery vira burocracia que usuário pula | Alta | Alta | Auto-sizing agressivo; `--mode quick` legítimo; Júri recusa full quando contexto não pede |
| Recusa de respostas vagas frustra usuário e ele desiste | Média | Média | Cap de 2 retries por pergunta + tag `quality: weak` em vez de loop infinito |
| Skeletons gerados em greenfield ficam genéricos demais | Média | Média | Cada `<!-- preencher -->` tem 1 exemplo-comentário PT-BR concreto (Maria-style) |
| `quick_validate.py` reprova nova description (colons / `<...>`) | Alta | Baixa | Aplica D-04/D-05 do skill-creator-alignment desde o draft |
| Audit silencioso falha em repo grande e trava entrevista | Baixa | Média | Timeout 30s; falha → warning + prossegue sem números |
| `--resume` corrompe estado parcial se discovery.md foi editado manualmente | Média | Média | Resume valida frontmatter `status: in_progress` antes de retomar; senão recomeça com aviso |
| `docs/product.md` greenfield colide com convenção do projeto adopter | Média | Média | REQ-A5.5 — nunca sobrescreve sem confirmação; oferece nome alternativo (`product.draft.md`) |

## 7. Acceptance criteria (sign-off Onda A)

- [ ] REQ-A1..REQ-A6 todos verificados (greps + evals + walkthroughs).
- [ ] Greenfield walkthrough: repo Flutter vazio (>>>0 dart files, >>>0 commits) → `/juri` → entrevista 4 blocos → 4 docs gerados + plan, em ≤60min de wall clock.
- [ ] Brownfield walkthrough: repo Flutter médio clonado (≥50 dart files, ≥1 commit + product.md) → `/juri` → audit silencioso + entrevista referencia números reais + PRD top 3-5 fixes.
- [ ] Critique regression: `/juri lib/features/<x>` continua produzindo o output atual (Veredicto + Nielsen table + Persona + Priority issues + Action plan).
- [ ] Júri recusa ≥80% das respostas vagas no eval scripted.
- [ ] `lib/` git-diff pós-discovery sempre vazio em todos os tiers.
- [ ] `python scripts/detect_mode.py` retorna JSON válido em repos sintéticos cobrindo greenfield + brownfield.
- [ ] STATE.md ganha entrada Onda A com decisões + deferred (discuss-mode, pause cross-feature).
- [ ] `quick_validate.py` valida `theme-critique/` (description atualizada inclusive).
- [ ] Tag `onda-a` criada após commit final.
