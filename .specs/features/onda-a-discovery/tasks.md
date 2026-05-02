# Tasks: onda-a-discovery

> Atomic, sequenced. Cada task ≤30 min. Cada task tem critério de verificação binário.
> Lê depois de spec.md + design.md.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-design-spec-driven` (já criada)

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable with peers

---

## Onda A.1 — Dispatch + sizing (foundation)

### T-01 ⬜ Criar `scripts/detect_mode.py`
- **Action:** escrever script Python conforme design D-03/§C-7. Local: `<repo>/scripts/detect_mode.py`. `chmod +x`.
- **Verify:**
  - `python scripts/detect_mode.py` no próprio repo `design-workflow` (que tem ≥10 commits + dart_files=0 + no product.md) → retorna JSON válido com `"mode": "brownfield"` ou `"greenfield"` (ambos aceitáveis — repo não-Flutter).
  - `python -c "import json; json.load(open('/dev/stdin'))" < <(python scripts/detect_mode.py)` retorna sem erro.
- **Refs:** REQ-A2, design §C-7

### T-02 ⬜ Atualizar `scripts/_sync.sh`
- **Action:** adicionar `[detect_mode.py]="theme-critique"` e `theme-critique` ao mapping de `audit_theme.py`.
- **Verify:**
  - `bash scripts/_sync.sh` roda sem erro
  - `ls skills/theme-critique/scripts/` mostra `detect_mode.py` e `audit_theme.py`
- **Refs:** REQ-A4 (audit reuse), design §C-8

### T-03 ⬜ Criar `references/discovery-sizing.md`
- **Action:** escrever em `skills/theme-critique/references/discovery-sizing.md`:
  - Tabela tier × deliverables (4×4):

    | Tier | Discovery.md | PRD | Skeletons | Pre-scan |
    |---|---|---|---|---|
    | quick | mini (3 perguntas) | não | não | não |
    | light | completo | curto | não | só se brownfield |
    | full | completo | completo | append a docs existentes | sim se brownfield |
    | greenfield | completo | completo | criar 4 skeletons | n/a |

  - Decision tree para conflito detect-vs-override (override vence sempre, mas adiciona warning se discrepância >1 nível).
  - Schema JSON do output do `detect_mode.py`.
- **Verify:** arquivo existe; `wc -l` ≤80; contém literal "tier_recommended" e "override".
- **Refs:** REQ-A2.4, design §C-3

### T-04 ⬜ Atualizar `SKILL.md` — mode dispatch + description
- **Action:** edit `skills/theme-critique/SKILL.md`:
  1. Atualizar description do frontmatter (mantém critique mention, adiciona discovery: "Júri também conduz discovery interview when called without a path." — sem colons no meio do description; usa "Triggered by" para listar `/juri`).
  2. Adicionar (logo após `## Triggers`) seção `## Mode dispatch` com a tabela de D-02.
  3. Adicionar `## Discovery mode (overview)` — 1 parágrafo + pointer pra `references/discovery-protocol.md`.
  4. Adicionar `## Discovery — auto-sizing` — pointer pra `references/discovery-sizing.md`.
- **Verify:**
  - `wc -l skills/theme-critique/SKILL.md` ≤ 350
  - `grep "Mode dispatch" skills/theme-critique/SKILL.md` retorna ≥1
  - `grep "discovery-sizing.md" skills/theme-critique/SKILL.md` retorna ≥1
  - `python <quick_validate>` passa (sem ERROR)
- **Refs:** REQ-A1, design D-02

### T-05 ⬜ Smoke test critique mode (regressão A.1)
- **Action:** rodar mentalmente o fluxo: prompt "critica `lib/features/dummy`" — confirmar que SKILL.md continua dirigindo pro Step 1..5 atual (carregar product.md → 2 assessments → consolidar → relatório). Inspeção visual.
- **Verify:** seções `## Workflow`, `## Setup gates`, `## Inputs`, `## Persona — Júri` intactas (apenas nova seção `## Mode dispatch` adicionada acima delas, não substituindo).
- **Refs:** REQ-A1.2, design D-12

### T-06 ⬜ Commit Onda A.1
- **Action:** `git add scripts/ skills/theme-critique/ && git commit -m "feat(theme-critique): dual-mode dispatch + sizing detection (Onda A.1)"`
- **Verify:** `git log -1 --stat` mostra 4-6 arquivos.

---

## Onda A.2 — Discovery engine

### T-07 🅿️ Criar `references/discovery-protocol.md`
- **Action:** escrever protocolo de entrevista em `skills/theme-critique/references/discovery-protocol.md`:
  - 4 blocos × perguntas concretas (PT-BR canônico):
    - **Bloco 1 — Produto** (3 perguntas): scene sentence; persona primária + 1 trip-up; tarefa principal em 1 frase de "X faz Y para Z".
    - **Bloco 2 — Tom** (3): 3 sensações físicas (não adjetivos); 1 ref concreta (app/site); 1 anti-ref obrigatória.
    - **Bloco 3 — Identidade** (3): paleta direção (warm/cool/neutral × commitment); typography mood; iconografia/forma.
    - **Bloco 4 — Stack** (2-3): framework + UI lib; tema atual (se brownfield, referenciar números do pre-scan); deploy target.
  - Vague-words list (D-05): 12 termos seed.
  - Retry script literal.
  - Tag `quality: weak|medium|strong` por resposta.
  - Stop conditions (2 retries → persiste weak; max 12 perguntas total).
- **Verify:**
  - `wc -l skills/theme-critique/references/discovery-protocol.md` em [120, 250]
  - `grep -c "Bloco" arquivo` = 4
  - `grep -ci "vague\|vago" arquivo` ≥3
- **Refs:** REQ-A3, design §C-2

### T-08 🅿️ Criar `references/discovery-doc-templates.md`
- **Action:** 4 skeletons inline com placeholders `{{var}}`:
  - **`product.md` skeleton:** §1 Visão, §2 Personas (1 primária + 1 secundária + 1 terciária), §3 Jornada, §4 Voz e tom (banidos absolutos), §5.3 Color strategy axis (drenched/restrained/neutral), §7 Anti-references, §8 Princípios estratégicos. Cada §X tem `<!-- preencher: explicação curta -->` + 1 exemplo-comentário PT-BR concreto (ex: "Maria, 32, treina 4×/semana às 6h30").
  - **`design.md` skeleton:** princípios de design system, pointer pra Nielsen + canon visual.
  - **`design-tokens.md` skeleton:** tabelas vazias palette (brand/semantic/neutral), typography roles, spacing scale, radius scale.
  - **`PRD.md` skeleton:** per-intervention. Sections: Problem, Top 3-5 fixes (priorizados), Skills mapping, Success metric, Out of scope.
  - Frontmatter `discovery.md` schema (D-07/D-10).
- **Verify:**
  - Arquivo existe; `wc -l` ≤500.
  - `grep -c "{{" arquivo` ≥10 (placeholders existem).
  - `grep -c "<!-- preencher" arquivo` ≥7 (todas seções de product.md cobertas).
- **Refs:** REQ-A5, design §C-4

### T-09 🅿️ Criar `references/discovery-routing.md`
- **Action:** escrever em `skills/theme-critique/references/discovery-routing.md`:
  - Schema YAML do `plan` (REQ-A6.1).
  - Mapa decisão → skill: 8-12 condições (ex: "palette ausente → /theme-create"; "cor falha contraste → /theme-extend"; "tela pesada → /theme-quieter"; "tela fraca → /theme-bolder"; "Figma URL fornecida → /theme-port"; "queres explorar → /frontend-design ou /theme-sandbox"; "copy fraca → /pena"; "estática → /theme-motion"; "drift estrutural → /theme-audit + Tier 2 Ralph (futuro)").
  - Anti-padrões (auto-run, ETAs vagas, skill names inventados).
  - Skill names exatos: lista das 13 atômicas + 3 orchestration futuras (`/design-spec compose`, `/design-spec sequence`, `/design-spec ship`) marcadas como `(Onda B)`.
- **Verify:**
  - `wc -l` ≤120.
  - `grep -E "^- /" arquivo` lista ≥13 skills (uma por linha).
  - YAML schema válido por inspeção.
- **Refs:** REQ-A6, design §C-5

### T-10 🅿️ Criar `references/discovery-vague-words.md`
- **Action:** lista canônica em `skills/theme-critique/references/discovery-vague-words.md`:
  - 12 termos seed (PT-BR + EN equivalents).
  - 3 templates de retry (variações para não soar repetitivo).
  - Critério de "weak answer" pós-2-retries.
- **Verify:** arquivo existe; `grep -c "^-" arquivo` ≥12.
- **Refs:** REQ-A3.3, design D-05

### T-11 ⬜ Criar `references/discovery-resume.md`
- **Action:** escrever em `skills/theme-critique/references/discovery-resume.md`:
  - Validação de frontmatter (D-09): status check, age check (≤14 dias).
  - Algoritmo "find first incomplete block" (D-10): parse markdown sections, encontra primeiro `**status:** in_progress`.
  - Mensagens de erro user-facing (5 casos: file ausente, frontmatter inválido, status errado, idade >14d, parse falha).
- **Verify:**
  - `wc -l` ≤80.
  - `grep -c "Erro" arquivo` ≥5.
- **Refs:** REQ-A1.4, design §C-6

### T-12 ⬜ Atualizar `SKILL.md` — discovery sections completas
- **Action:** edit `skills/theme-critique/SKILL.md`:
  1. Expandir `## Discovery mode (overview)` — adicionar workflow steps 1-5 do discovery (Detect mode → Carregar contexto / pre-scan se brownfield → Entrevista 4 blocos → Gerar docs → Routing) com pointers para cada reference.
  2. Adicionar `## Discovery — outputs` com tabela tier × arquivos gerados.
  3. Adicionar `## Discovery — anti-patterns` (auto-run, vagueza tolerada, ordem furada, edits em `lib/`).
- **Verify:**
  - `wc -l skills/theme-critique/SKILL.md` ≤ 400.
  - `grep "discovery-protocol\|discovery-doc-templates\|discovery-routing\|discovery-resume\|discovery-vague-words" skills/theme-critique/SKILL.md` retorna ≥5 matches.
  - `python <quick_validate>` passa.
- **Refs:** REQ-A3-A6, design §C-1

### T-13 ⬜ Criar `.design-spec/` skeleton
- **Action:**
  ```
  mkdir -p .design-spec/features .design-spec/project
  touch .design-spec/.gitkeep .design-spec/features/.gitkeep .design-spec/project/.gitkeep
  ```
  Adicionar `.design-spec/halt` ao `.gitignore` (kill switch é runtime, não versionado).
- **Verify:**
  - `find .design-spec -type f` lista 3 `.gitkeep`.
  - `grep "^.design-spec/halt$" .gitignore` retorna 1.
- **Refs:** design D-07

### T-14 ⬜ Smoke test discovery dispatch (mock)
- **Action:** revisão manual do SKILL.md: confirmar que dispatch table rotula `/juri` (no args) → `references/discovery-protocol.md`. Confirmar que pre-scan brownfield está documentado em `discovery-protocol.md` ou seção dedicada.
- **Verify:** inspeção qualitativa OK; sem TODO/FIXME deixados.

### T-15 ⬜ Commit Onda A.2
- **Action:** `git add skills/theme-critique/ .design-spec/ .gitignore && git commit -m "feat(theme-critique): discovery interview + brownfield pre-scan + doc gen (Onda A.2)"`
- **Verify:** `git log -1 --stat` mostra 6-9 arquivos novos/modificados.

---

## Onda A.3 — Routing + resume + evals + close

### T-16 ⬜ Criar `skills/theme-critique/evals/evals.json`
- **Action:** escrever 5 evals (schema do skill-creator):
  - **eval-1 — critique regression:** prompt "critica lib/features/dummy"; expected_output cita "Veredicto", "Nielsen heuristics", "Priority issues"; assertions qualitative.
  - **eval-2 — critique with screenshot:** prompt "essa tela tá fraca [screenshot]"; expected mention "evidence file:line".
  - **eval-3 — discovery greenfield:** prompt "/juri" em repo greenfield; expected: 4 blocos sequencialmente, gera 4 skeletons + discovery.md.
  - **eval-4 — discovery brownfield:** prompt "/juri" em repo brownfield; expected: pre-scan rodou, perguntas Stack referenciam números reais.
  - **eval-5 — vague refusal:** prompt sequence onde user responde "moderno e clean"; expected: Júri recusa e re-pergunta com formato (ref + sensação + anti-ref).
- **Verify:**
  - `jq '.evals | length' skills/theme-critique/evals/evals.json` = 5.
  - `jq '.skill_name' arquivo` = `"theme-critique"`.
  - Cada eval tem `id`, `prompt`, `expected_output`, `assertions` (≥3).
- **Refs:** REQ-A1.2 verification, design §C-11

### T-17 ⬜ Atualizar `.specs/project/STATE.md`
- **Action:** apendar seção "## Onda A — Discovery (2026-05-02)":
  - Decisões D-01..D-13 resumidas (1 linha cada).
  - Validation runs: critique regression smoke, vague-refusal eval, detect_mode synthetic.
  - Deferred: discuss-mode completo (Onda C); cross-feature pause (Onda C); evals subjetivas adicionais (Onda B+).
- **Verify:**
  - `grep -c "D-0\|D-1" .specs/project/STATE.md` ≥10 nessa seção.
  - `grep "Onda A — Discovery" .specs/project/STATE.md` retorna 1.

### T-18 ⬜ Atualizar memory (`MEMORY.md` + project file)
- **Action:**
  - Atualizar `~/.claude/projects/-media-fitiodev-FITIO-Skill-design-workflow/memory/project_design_spec_driven.md` com status Onda A: implementada (3 commits).
  - Adicionar nova memory `decision_discovery_extends_critique.md` registrando D-01 (extends, não cria nova skill).
  - Atualizar `MEMORY.md` index com 1 linha nova.
- **Verify:**
  - Arquivo de memória novo existe.
  - `MEMORY.md` line count ≤ index lines + 1.

### T-19 ⬜ Verificação batch da Onda A
- **Action:** rodar:
  ```bash
  echo "=== validate ==="
  python /home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py skills/theme-critique
  echo "=== SKILL length ==="
  wc -l skills/theme-critique/SKILL.md
  echo "=== references ==="
  ls skills/theme-critique/references/
  echo "=== scripts ==="
  ls skills/theme-critique/scripts/
  echo "=== evals ==="
  jq '.evals | length' skills/theme-critique/evals/evals.json
  echo "=== detect_mode ==="
  python scripts/detect_mode.py
  echo "=== gitignore ==="
  grep "^.design-spec/halt$" .gitignore
  ```
- **Verify:**
  - quick_validate: 0 ERROR.
  - SKILL.md ≤400 linhas.
  - references count ≥6 (nielsen-rubric + 5 discovery-*).
  - scripts ≥2 (audit + detect_mode).
  - evals length = 5.
  - detect_mode JSON válido.
- **Refs:** REQ-A1..A6, spec §7

### T-20 ⬜ Commit Onda A.3 + tag
- **Action:**
  ```
  git add .
  git commit -m "feat(theme-critique): discovery routing + resume + evals (Onda A.3)"
  git tag onda-a
  ```
- **Verify:**
  - `git tag | grep onda-a` retorna match.
  - `git log -3 --oneline` mostra 3 commits Onda A.

### T-21 ⬜ Sign-off final
- **Action:** percorrer spec §7 acceptance criteria, marcar cada checkbox em `spec.md`. Reportar resultado.
- **Verify:** todos os 9 checks passam ou têm justificativa documentada.

---

## Resumo de paralelização

- **Onda A.1:** T-01 → T-02 → T-03 → T-04 → T-05 → T-06 (sequencial; SKILL.md depende de references existentes).
- **Onda A.2:** T-07/T-08/T-09/T-10 paralelizáveis (4 references novas independentes). T-11 depende de A.1. T-12 depende de T-07..T-11. T-13 paralelo. T-14..T-15 finais.
- **Onda A.3:** T-16 → T-17 → T-18 → T-19 → T-20 → T-21 (sequencial).

## Estimativa

- A.1: ~1.5h (script + SKILL edit + smoke).
- A.2: ~3h (5 references novas — content denso).
- A.3: ~1.5h (evals + STATE + memory + verify + commit).
- **Total:** ~6h serial. Não compressível pelo paralelismo dentro de A.2 (mesmo Claude editando 5 arquivos sequencial é ~mesma latência).

## Como retomar

Próxima sessão começa lendo:
1. `.specs/features/onda-a-discovery/spec.md`
2. `.specs/features/onda-a-discovery/design.md`
3. `.specs/features/onda-a-discovery/tasks.md` (este arquivo)
4. `.specs/project/STATE.md`

Identifica primeiro task `⬜ pending` e procede em ordem.
