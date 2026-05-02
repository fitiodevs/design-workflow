# Tasks: skill-creator-alignment

> Atomic, sequenced. Cada task ≤30 min de trabalho. Cada task tem critério de verificação binário.
> Lê depois de spec.md + design.md.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-alignment` (criar em T-00)

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable with peers

---

## Onda 0 — Safety net

### T-00 ⬜ Criar tag git de rollback
- **Action:** `cd <repo> && git tag pre-alignment && git push origin pre-alignment` (push opcional se desejar backup remoto)
- **Verify:** `git tag | grep pre-alignment`
- **Refs:** spec REQ rollback; design §5
- **Blocks:** todas as outras tasks

---

## Onda 1 — Limpeza estrutural (REQ-01, REQ-02, REQ-06)

> Cada SKILL.md sofre **uma única edição** consolidando 3 mudanças. Skills são paralelizáveis entre si.

### T-01 🅿️ Limpar SKILL.md de `theme-audit`
- **Action:** No `skills/theme-audit/SKILL.md`:
  1. Remover linhas `license:` e `triggers:` do frontmatter
  2. Substituir todas as 2 menções "Fitio"/"fitio" por categoria genérica (D-02)
  3. Adicionar seção `## Triggers` no body (logo após o título), formato: EN line + PT line + natural language line
  4. Adicionar `/Auditor` à description do frontmatter
- **Verify:**
  - `grep -E "^(license|triggers):" skills/theme-audit/SKILL.md` → 0 resultados
  - `grep -ci "fitio" skills/theme-audit/SKILL.md` → 0
  - `grep "/Auditor" skills/theme-audit/SKILL.md` → ≥1
- **Refs:** REQ-01, REQ-02, REQ-06

### T-02 🅿️ Limpar SKILL.md de `theme-extend`
- Mesma rotina de T-01. Persona EN: `Surgeon`. Manter `/Cirurgião`.
- **Verify:** mesmas 3 checagens.

### T-03 🅿️ Limpar SKILL.md de `theme-port`
- Mesma rotina. Persona EN: `Architect`. Manter `/Arquiteto`.
- **Atenção:** REQ-02.3 — substituir `lib/features/marketplace` exemplos por `lib/features/<feature>`.

### T-04 🅿️ Limpar SKILL.md de `theme-create`
- Mesma rotina. Persona EN: `Composer`. Manter `/Compositor`.
- **Atenção:** 5 menções a Fitio — varrer com cuidado.

### T-05 🅿️ Limpar SKILL.md de `theme-prompt`
- Mesma rotina. Sub-skill, sem persona dedicada — adicionar trigger genérico EN como `/theme-prompt` (já é EN).

### T-06 🅿️ Limpar SKILL.md de `theme-sandbox`
- Mesma rotina. Persona EN: `Orchestrator`. Manter `/Orquestrador`.

### T-07 🅿️ Limpar SKILL.md de `theme-critique`
- Mesma rotina. Persona EN: `Critic`. Manter `/Júri`.

### T-08 🅿️ Limpar SKILL.md de `theme-bolder`
- Mesma rotina. Persona EN: `Amplifier`. Manter `/Brasa`.

### T-09 🅿️ Limpar SKILL.md de `theme-quieter`
- Mesma rotina. Persona EN: `Refiner`. Manter `/Calma`.

### T-10 🅿️ Limpar SKILL.md de `theme-distill`
- Mesma rotina. Persona EN: `Distiller`. Manter `/Lâmina`.
- **Atenção:** 8 menções a Fitio (mais alto do conjunto).

### T-11 🅿️ Limpar SKILL.md de `theme-motion`
- Mesma rotina. Persona EN: `Choreographer`. Manter `/Jack`.

### T-12 🅿️ Limpar SKILL.md de `frontend-design`
- Mesma rotina. Persona EN: `Designer`. Manter `/Clara`.

### T-13 🅿️ Limpar SKILL.md de `ux-writing`
- Mesma rotina. Persona EN: `Writer`. Manter `/Pena`.
- **Atenção:** 10 menções a Fitio (mais alto do conjunto).

### T-14 ⬜ Limpar `template/SKILL.md`
- **Action:** remover `license:` do frontmatter; deixar só `name` + `description`. Atualizar comentário: "Replace with description. Do NOT add `license:` or `triggers:` — both are non-standard."
- **Verify:** `cat template/SKILL.md` mostra frontmatter de 4 linhas.
- **Refs:** REQ-01.4

### T-15 ⬜ Verificação batch da Onda 1
- **Action:** rodar:
  ```bash
  echo "=== leak Fitio ==="
  grep -ic "fitio" skills/*/SKILL.md
  echo "=== campos não-spec ==="
  grep -lE "^(license|triggers):" skills/*/SKILL.md
  echo "=== triggers EN ==="
  for s in skills/*/SKILL.md; do
    grep -lE "/(Auditor|Composer|Critic|Amplifier|Refiner|Distiller|Choreographer|Designer|Writer|Surgeon|Architect|Orchestrator)" "$s" || echo "FALTA: $s"
  done
  ```
- **Verify:** primeiro grep tudo zero ou só "originated from"; segundo grep vazio; terceiro sem "FALTA:".
- **Refs:** REQ-01, REQ-02, REQ-06 — gates pra commit

### T-16 ⬜ Commit Onda 1
- **Action:** `git add skills/ template/ && git commit -m "chore(skills): clean frontmatter, remove brand leak, add EN triggers"`
- **Verify:** `git log -1 --stat` mostra ~14 arquivos modificados.

---

## Onda 2 — Reorganização (REQ-03, REQ-04)

### T-17 ⬜ Criar `scripts/_sync.sh`
- **Action:** escrever script conforme design §C-1, dar `chmod +x`.
- **Verify:** `bash scripts/_sync.sh && find skills/*/scripts -name "*.py" | sort` lista os 6 (com duplicatas: theme-audit/check_contrast, theme-extend/check_contrast, theme-create/check_contrast, etc).
- **Refs:** REQ-04, design §C-1

### T-18 ⬜ Rodar `_sync.sh` e commitar `skills/<x>/scripts/`
- **Action:** `bash scripts/_sync.sh && git add skills/*/scripts/`
- **Verify:** `git status` mostra ≥6 novos `.py` em skills/.
- **Refs:** REQ-04.4, design D-03

### T-19 ⬜ Atualizar `install.sh` com mensagem informativa
- **Action:** adicionar linha `echo "  scripts bundled per skill"` antes do "Next steps:".
- **Verify:** rodar em `/tmp/test-install/` (CLAUDE_HOME=/tmp/test-install) e ver mensagem.

### T-20 🅿️ Extrair references — `theme-create`
- **Action:**
  1. Identificar 2 seções denses no SKILL.md (OKLCH recipes; slop patterns table)
  2. Mover literal para `skills/theme-create/references/oklch-recipes.md` e `.../slop-patterns.md`
  3. Substituir no SKILL.md por pointer (D-04 pattern)
- **Verify:**
  - `wc -l skills/theme-create/SKILL.md` ≤200
  - `ls skills/theme-create/references/` mostra 2 arquivos
- **Refs:** REQ-03.1, design §C-4

### T-21 🅿️ Extrair references — `theme-port`
- Mesma rotina. Extrair: text-hierarchy table; widget-mapping table.

### T-22 🅿️ Extrair references — `theme-motion`
- Extrair: motion-tokens table; flutter_animate snippets.

### T-23 🅿️ Extrair references — `ux-writing`
- Extrair: 4 quality standards detail; before-after pattern library.

### T-24 🅿️ Extrair references — `frontend-design`
- Extrair: clara auto-revisão checklist.

### T-25 🅿️ Extrair references — `theme-critique`
- Extrair: Nielsen 0–4 rubric (10 heurísticas × scoring guide).

### T-26 ⬜ Verificação batch da Onda 2
- **Action:**
  ```bash
  echo "=== SKILL.md length ==="
  wc -l skills/*/SKILL.md
  echo "=== references count ==="
  find skills/*/references -name "*.md" | wc -l
  echo "=== scripts count ==="
  find skills/*/scripts -name "*.py" | wc -l
  echo "=== install dry run ==="
  TARGET=/tmp/test-install rm -rf $TARGET && mkdir -p $TARGET
  HOME=/tmp HOME_OVERRIDE=/tmp/test-install ./install.sh
  find /tmp/test-install -name "*.py"
  ```
- **Verify:** todas SKILL.md ≤200 linhas; references count ≥9; scripts ≥6 no destino install.

### T-27 ⬜ Commit Onda 2
- **Action:** `git add . && git commit -m "refactor(skills): progressive disclosure + scripts per skill"`

---

## Onda 3 — Adições novas (REQ-05, REQ-07, REQ-08)

### T-28 🅿️ Criar `evals.json` para `theme-audit`
- **Action:** escrever 3 prompts realistas + 4-5 assertions cada (D-05 schema).
  - Prompt 1: "rode audit no `lib/features/marketplace`"
  - Prompt 2: "screenshot mostrando ícone fraco no dark mode"
  - Prompt 3: "valida WCAG das combinações brand/onBrand"
- **Verify:** `jq '.evals | length' skills/theme-audit/evals/evals.json` = 3
- **Refs:** REQ-05, design §C-3

### T-29 🅿️ Criar `evals.json` para `theme-extend`
- 3 prompts: "adiciona token disabled", "resolve contraste de outline em dark", "muda `success` 1 step mais escuro".

### T-30 🅿️ Criar `evals.json` para `theme-port`
- 3 prompts: Figma URL, HTML do Stitch, screenshot description.

### T-31 🅿️ Criar `evals.json` para `theme-create`
- 3 prompts: "palette para sub-brand de academia", "modo natalino", "rebrand minimalista".

### T-32 ⬜ Rodar `quick_validate.py` nas 13 skills
- **Action:** localizar script no skill-creator instalado, ex: `/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py`. Rodar em loop:
  ```bash
  for s in skills/*/; do
    python <path-to-quick_validate> "$s"
  done > /tmp/validation.log 2>&1
  ```
- **Verify:** `grep -c ERROR /tmp/validation.log` = 0
- **Refs:** REQ-07

### T-33 ⬜ Atualizar README §What changed in v0.2
- **Action:** adicionar seção logo após `## Status` listando as 6 frentes (1 bullet cada). Manter §Quickstart intacta — agora é verdade.
- **Verify:** `grep "What changed in v0.2" README.md` retorna match.

### T-34 ⬜ Bump version em `marketplace.json`
- **Action:** edit `0.1.0` → `0.2.0` em `.claude-plugin/marketplace.json`.
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `0.2.0`

### T-35 ⬜ Criar `.specs/project/STATE.md` com follow-ups
- **Action:** documentar:
  - Validation runs (T-32 output summary)
  - Deferred: rodar `improve_description.py` em todas as 13 (depende de evals existentes)
  - Deferred: evals para 9 skills subjetivas (precisa human-review viewer)
  - Deferred: publish release v0.2.0 no GitHub
- **Verify:** arquivo existe com seções `## Decisions`, `## Validation runs`, `## Deferred`.

### T-36 ⬜ Commit Onda 3
- **Action:** `git add . && git commit -m "feat(skills): add minimal evals + bump v0.2.0"`

### T-37 ⬜ Verificação final + sign-off
- **Action:** rodar todos os greps de spec §7 (acceptance criteria); checar cada checkbox; relatar resultado.
- **Verify:** todos os 8 checks REQ-XX passam.

---

## Resumo de paralelização

- **Onda 1:** T-01..T-13 paralelizáveis (13 skills independentes). T-14 sequencial. T-15..T-16 finais.
- **Onda 2:** T-17→T-18→T-19 sequenciais (depende dos scripts). T-20..T-25 paralelizáveis. T-26..T-27 finais.
- **Onda 3:** T-28..T-31 paralelizáveis. T-32..T-37 sequenciais.

## Estimativa

- Onda 1: ~3h (13 skills × ~12 min cada, mais rápido se paralelizar com agents)
- Onda 2: ~2h (extrair conteúdo é leitura+copy, não criação)
- Onda 3: ~1.5h (evals demandam pensar em prompts realistas)
- **Total:** ~6.5h serial; ~3h se paralelizar Onda 1 com 4 agents.

## Como retomar

Próxima sessão começa lendo:
1. `.specs/features/skill-creator-alignment/spec.md`
2. `.specs/features/skill-creator-alignment/design.md`
3. `.specs/features/skill-creator-alignment/tasks.md`
4. `.specs/project/STATE.md` (se já criado em corrida prévia)

Identifica primeiro task `⬜ pending` e procede em ordem.
