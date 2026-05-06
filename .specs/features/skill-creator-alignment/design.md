# Design: skill-creator-alignment

> Decisões arquiteturais para executar `spec.md`. Lê depois do spec.

---

## 1. Estratégia de execução

Trabalho em **3 ondas sequenciais** (não-paralelizáveis entre ondas, paralelizáveis dentro):

```
Onda 1 — Limpeza estrutural (independente, paralelizável internamente)
  ├── REQ-01 frontmatter cleanup
  ├── REQ-02 desFitiotização
  └── REQ-06 triggers EN

Onda 2 — Reorganização de assets
  ├── REQ-03 progressive disclosure
  └── REQ-04 scripts por skill

Onda 3 — Adições novas
  ├── REQ-05 evals minimal
  ├── REQ-07 validação skill-creator
  └── REQ-08 README + version bump
```

**Por que sequencial entre ondas:** Onda 2 mexe em paths que Onda 1 normaliza; Onda 3 valida o que Onda 2 produziu. Dentro da onda, skills são independentes (skill A não importa de skill B), então paralelizável.

## 2. Decisões arquiteturais

### D-01 — `triggers:` YAML vs body section

**Decisão:** mover para body em seção `## Triggers` no topo do SKILL.md, logo após o título.

**Por quê:** spec do skill-creator não suporta o YAML; mas a info é útil pra leitor humano e pra re-encoding futuro em description. Body é o lugar canônico.

**Alternativa rejeitada:** apagar de vez. Perde-se a documentação de aliases regex.

### D-02 — Estratégia "desFitiotização"

**Decisão:** substituição mecânica via tabela de mapping, não rewriting livre:

```
Fitio          → your app / the project / a Flutter app
fitio          → your app / the project
lib/           → lib/ (mantém — é convenção Flutter)
docs/product.md → docs/product.md (mantém — é convenção declarada do repo)
AppColors      → AppColors (mantém — é nome de classe convencional)
```

**Por quê:** preserva exemplos concretos (que dão pushiness) sem inventar texto novo. Mecânico = revisável.

**Edge case:** menções com contexto histórico ("originated from Fitio") podem ficar — só num parágrafo "Origin" se aparecer.

### D-03 — Scripts: copy vs symlink

**Decisão:** **copy físico** via `install.sh`, fonte canônica em `<repo>/scripts/`.

**Por quê:**
- Symlinks quebram em Windows/iCloud sync; copy funciona em todo lugar.
- Skill-creator espera skill auto-contida ao instalar; user pode mover diretório individual.
- Custo: ~40KB duplicação total — irrelevante.

**Workflow:**
1. Editor mexe sempre em `<repo>/scripts/<x>.py`.
2. `install.sh` copia para `~/.claude/skills/<skill>/scripts/<x>.py`.
3. CI hook (futuro, não nesta feature) pode espelhar pra `<repo>/skills/<skill>/scripts/` no commit pra deixar disponível mesmo sem install.

**Decisão complementar:** **commitar cópias dentro de `<repo>/skills/<skill>/scripts/`** para que `git clone` + uso direto funcione. Fonte canônica continua em `<repo>/scripts/`; cópias commitadas são geradas via novo target `make sync-scripts` ou `./scripts/_sync.sh`.

### D-04 — Estrutura de `references/` por skill

**Decisão:** SKILL.md sempre referencia com este padrão:

```markdown
## OKLCH palette generation

Para a tabela completa de recipes (warm/cool/neutral × 3 commitment levels),
leia `references/oklch-recipes.md` antes de gerar.

Resumo: ...
```

**Por quê:** o resumo no SKILL.md mantém o fluxo claro; `references/` carrega só quando necessário. Modelo decide se precisa ler baseado na situação.

### D-05 — Evals: schema + ferramenta

**Decisão:** seguir `schemas.md` do skill-creator literalmente. Cada `evals.json`:

```json
{
  "skill_name": "<skill>",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user prompt that mentions specific files/numbers/context",
      "expected_output": "What we'd expect to see (1-2 sentences)",
      "files": [],
      "assertions": [
        {"text": "Output mentions WCAG ratio for at least 3 color pairs", "type": "qualitative"},
        {"text": "File AppColors.dart was read", "type": "tool_use"}
      ]
    }
  ]
}
```

**Tipos de assertion:** `qualitative` (grader humano/LLM), `tool_use` (programmatic), `regex_match` (programmatic).

### D-06 — Versionamento e commit strategy

**Decisão:** commit por onda (3 commits), não por skill (que daria 13×4 = absurdo) e não único (que perde rollback granular).

```
commit 1: chore(skills): clean frontmatter, remove brand leak, add EN triggers
commit 2: refactor(skills): progressive disclosure + scripts per skill
commit 3: feat(skills): add minimal evals + bump v0.2.0
```

**Tag git:** `pre-alignment` antes de qualquer mudança (rollback safety).

### D-07 — Triggers EN no frontmatter description

**Decisão:** adicionar 1 trigger EN na description sem remover triggers PT existentes. Exemplo:

```yaml
description: ...Use when the user asks for "/Auditor", "/Lupa", "audit the theme",
"verify hardcoded colors", "check WCAG", or reports a visual issue.
```

**Por quê:** description é o único campo que dispara skill. Não-mencionar EN = README mente. Mencionar PT continua funcionando.

## 3. Components

### C-1 `scripts/_sync.sh` (novo)

```bash
#!/usr/bin/env bash
# Sync canonical scripts/ into each skill's scripts/ subdir
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

declare -A USAGE=(
  [audit_theme.py]="theme-audit"
  [check_contrast.py]="theme-audit theme-extend theme-create"
  [generate_palette.py]="theme-create"
  [oklch_to_hex.py]="theme-create theme-extend"
)

for script in "${!USAGE[@]}"; do
  for skill in ${USAGE[$script]}; do
    mkdir -p "${ROOT}/skills/${skill}/scripts"
    cp "${ROOT}/scripts/${script}" "${ROOT}/skills/${skill}/scripts/${script}"
  done
done
```

Roda: manual antes de commit, ou hook pre-commit (futuro).

### C-2 `install.sh` (modificado)

Mantém o loop atual (`cp -R skills/*/`). Como `_sync.sh` já populou `skills/<x>/scripts/`, install não precisa lógica extra.

Adicionar no final:
```bash
echo "  scripts bundled per skill (sourced from <repo>/scripts/)"
```

### C-3 `evals/` por skill (novo, 4 instâncias)

```
skills/theme-audit/evals/evals.json
skills/theme-extend/evals/evals.json
skills/theme-port/evals/evals.json
skills/theme-create/evals/evals.json
```

Sem subdiretório `iteration-N/` ainda — isso é gerado pelo workflow do skill-creator quando rodado.

### C-4 `references/` por skill (novo, 6 skills, ~9 arquivos)

```
skills/theme-create/references/oklch-recipes.md
skills/theme-create/references/slop-patterns.md
skills/theme-port/references/text-hierarchy.md
skills/theme-port/references/widget-mapping.md
skills/theme-motion/references/motion-tokens.md
skills/theme-motion/references/flutter-animate-snippets.md
skills/ux-writing/references/quality-standards.md
skills/ux-writing/references/before-after-patterns.md
skills/frontend-design/references/clara-checklist.md
skills/theme-critique/references/nielsen-rubric.md
```

Conteúdo é cópia literal das seções correspondentes do SKILL.md atual.

### C-5 STATE.md (novo, em `.specs/project/`)

Memória pós-execução: validação rodada, follow-ups deferred (description optimizer, evals subjetivas, release v0.2.0).

## 4. Verification strategy

| Camada | Como validar | Quando |
|---|---|---|
| Frontmatter compliance | `grep -L` + `python -m scripts.quick_validate` | Pós-Onda 1 |
| Length cap | `wc -l skills/*/SKILL.md` | Pós-Onda 2 |
| Brand leak | `grep -ic "fitio"` | Pós-Onda 1 |
| Trigger EN presence | grep tabular | Pós-Onda 1 |
| Script availability | `find ~/.claude/skills -name "*.py"` após install em `/tmp/test/` | Pós-Onda 2 |
| Evals valid JSON | `jq '.evals | length'` | Pós-Onda 3 |
| Install idempotente | `./install.sh && ./install.sh` (2x) sem erro | Pós-Onda 3 |

## 5. Rollback

```bash
git checkout pre-alignment -- .
```

Tag criada antes da Task 1 da Onda 1 (ver tasks.md, T-00).

## 6. Order of operations dentro de cada skill

Para evitar editar mesmo arquivo 3x:

1. Ler SKILL.md atual
2. Identificar seções a extrair (REQ-03)
3. Em **uma única edição** do SKILL.md:
   - Remover `triggers:` e `license:` do frontmatter
   - Substituir Fitio → genérico
   - Adicionar `## Triggers` (PT+EN) no body
   - Substituir tabelas longas por pointer pra `references/`
   - Adicionar 1 trigger EN no description
4. Em ediçõe(s) novas, criar `references/<x>.md` com conteúdo extraído (literal)
5. Se aplica REQ-04: criar `scripts/<x>.py` (cópia)
6. Se aplica REQ-05: criar `evals/evals.json`

Isso garante que cada SKILL.md sofre **1 edit** por skill, e os arquivos novos são `Write` puros.
