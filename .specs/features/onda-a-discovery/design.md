# Design: onda-a-discovery

> Decisões arquiteturais para executar `spec.md`. Ler depois do spec.

---

## 1. Estratégia de execução

3 ondas internas (não-paralelizáveis entre ondas; paralelizáveis dentro):

```
Onda A.1 — Dispatch + sizing (foundation)
  ├── REQ-A1 dual-mode dispatch (SKILL.md atualizada)
  ├── REQ-A2 detect_mode.py + override flag

Onda A.2 — Discovery engine
  ├── REQ-A3 protocolo entrevista (references/discovery-protocol.md + vague-words.md)
  ├── REQ-A4 brownfield pre-scan (audit_theme.py invocação silent)
  └── REQ-A5 doc generators (references/discovery-doc-templates.md + skeletons inline)

Onda A.3 — Persistence + routing
  ├── REQ-A1.4 resume (parse frontmatter, restore state)
  ├── REQ-A6 routing schema (references/discovery-routing.md)
  └── Verify + STATE update + commit final
```

A.1 é independente e pode rodar isolada (smoke testable). A.2 depende de A.1 (precisa do dispatch). A.3 amarra tudo + verifica regressão.

## 2. Decisões arquiteturais

### D-01 — Discovery extends `theme-critique`, NÃO nova skill

**Decisão:** modo discovery vive em `skills/theme-critique/` com dispatch interno por shape do argumento. Não criamos `skills/discovery/`.

**Por quê:**
- Persona Júri é uma só (memória `decision_juri_dual_mode.md`). Duas skills com mesma persona = drift de voz.
- Trigger `/juri` é único — duas skills competindo pelo mesmo trigger é anti-padrão do harness.
- Reuso máximo: `voice_dna`, gates, persona block, protocolo agent isolado já existem.
- Custo: SKILL.md ganha ~50 linhas de dispatch + pointer pra references; conteúdo denso (interview, doc templates) vai pra `references/` (progressive disclosure D-04 do alignment).

**Alternativa rejeitada:** criar `skills/discovery/` separada. Quebra unicidade do trigger e fragmenta Júri.

**Consequência:** nome do skill continua `theme-critique` mesmo cobrindo discovery. Nome é histórico — descrição clara importa mais que renomear (renomear quebraria backwards compat de instalações existentes).

### D-02 — Dispatch por shape do argumento

**Decisão:** SKILL.md adiciona seção `## Mode dispatch` no topo (logo após `## Triggers`):

```markdown
## Mode dispatch

| Invocation                   | Mode      | Loads                                   |
|------------------------------|-----------|-----------------------------------------|
| `/juri` (no args)            | discovery | references/discovery-protocol.md        |
| `/juri <flutter-path>`       | critique  | references/nielsen-rubric.md (existing) |
| `/juri --discuss <topic>`    | discuss   | (Onda C — scaffold only)                |
| `/juri --resume <feature>`   | resume    | references/discovery-resume.md          |

Resolution order: flag (`--`) → existing path → discovery default.
```

Modelo lê esta seção primeiro, decide modo, carrega só o reference relevante. Mantém SKILL.md fina (≤300 linhas) e modos isolados.

**Por quê:** Claude já é bom em routing por shape de input quando o pattern é explícito. Tabela em vez de prosa elimina ambiguidade.

### D-03 — `detect_mode.py` é determinístico, não LLM

**Decisão:** detecção greenfield/brownfield é um script Python puro com regras booleanas. Modelo lê o JSON e age.

```python
# scripts/detect_mode.py
import json, subprocess, os
from pathlib import Path

def detect(repo_root="."):
    os.chdir(repo_root)
    commits = int(subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip() or "0")
    dart_files = sum(1 for _ in Path("lib").rglob("*.dart")
                     if "generated" not in str(_) and ".g.dart" not in str(_)) if Path("lib").exists() else 0
    product_md = Path("docs/product.md")
    has_product = product_md.exists() and product_md.stat().st_size > 2000
    has_theme = any(Path(p).exists() for p in
                    ["lib/core/theme", "lib/theme", "lib/shared/theme"])

    is_greenfield = commits < 10 and dart_files < 5 and not has_product
    return {
        "mode": "greenfield" if is_greenfield else "brownfield",
        "tier_recommended": "greenfield" if is_greenfield else "full",
        "signals": {
            "commits": commits,
            "dart_files": dart_files,
            "has_product_md": has_product,
            "has_theme_dir": has_theme,
        }
    }

if __name__ == "__main__":
    print(json.dumps(detect(), indent=2))
```

**Por quê:** sizing é trivial e probabilisticamente fácil; LLM nele é desperdício de token + inconsistência. Script é cacheable + auditável + testable.

**Local canônico:** `<repo>/scripts/detect_mode.py`. Distribuído via `_sync.sh` para `skills/theme-critique/scripts/detect_mode.py`.

### D-04 — `--mode` override sobre detecção

**Decisão:** flag `--mode {quick|light|full|greenfield}` sobre o `mode_recommended`. Override sempre vence (usuário sabe melhor que a heurística em casos de borda — repo brownfield mas projeto novo dentro dele).

Quando ambos faltam: aplica `tier_recommended` do detect_mode.

### D-05 — Vague-words list e protocolo de retry

**Decisão:** lista canônica em `references/discovery-vague-words.md` (12 termos iniciais; estendível). Júri tem 2 retries por pergunta antes de persistir resposta com `quality: weak` e prosseguir.

**Por quê:**
- Hard-fail (loop infinito) frustra usuário em casos legítimos onde a resposta é pobre por contexto.
- Soft-fail silenciosa (aceitar primeira vaga) destrói o sinal da entrevista.
- 2 retries é compromisso: força user a tentar duas vezes, mas não vira interrogatório.

**Formato de retry:** "Você disse 'moderno'. Eu não consigo desenhar 'moderno'. Me dá 1 ref concreta (app/site/objeto) + 1 sensação física + 1 anti-ref (o que não pode parecer)."

### D-06 — Doc generators: skeletons inline em references, não Python

**Decisão:** skeletons (`product.md`, `design.md`, etc.) ficam como **Markdown inline em `references/discovery-doc-templates.md`**. Júri lê o template, substitui placeholders, escreve com `Write` tool. Sem Python para isso.

**Por quê:**
- Skeletons são markdown estático — Python só adiciona indireção.
- Substituições são tipo "{{feature_name}}", "{{persona_primary}}" — 5-10 vars total. LLM faz isso trivialmente.
- Manutenção (ajustar placeholder) é editar markdown, não código Python.

### D-07 — `.design-spec/` é diretório-raiz do estado

**Decisão:** estrutura nova:

```
.design-spec/
├── features/
│   └── <feature-slug>/
│       ├── discovery.md        # frontmatter + content
│       └── (audit-pre-scan.json — futuro)
├── project/
│   ├── STATE.md                # já existe em .specs/, ver D-08
│   └── decisions.md            # placeholder, populated em Onda B
└── halt                        # placeholder, populated em Onda D
```

**Por quê:** isolar runtime state (`.design-spec/`) de planning state (`.specs/`). `.specs/` é spec-driven planning (humanos escrevem); `.design-spec/` é runtime persistence (Júri/Ralph escrevem).

### D-08 — STATE.md fica em `.specs/project/`

**Decisão:** mantém `.specs/project/STATE.md` como single source. Não duplica em `.design-spec/`.

**Por quê:** STATE.md é planning (decisions, deferred, validation runs) — pertence ao território humano. Apenas evita confusão.

### D-09 — Resume valida frontmatter strict

**Decisão:** `--resume <feature>` lê `.design-spec/features/<feature>/discovery.md`, valida:
- Frontmatter parseable
- `status: in_progress` (não `draft`, `approved`, `consumed`)
- `created` ≤14 dias atrás (senão sugere re-discovery — alinha com REQ-C1.3)

Falhou validação → recusa retomar e explica.

### D-10 — Resume preserva ordem de blocos

**Decisão:** `discovery.md` parcial tem seções por bloco com flag `complete: true|false`. Resume lê seções, identifica primeiro bloco `complete: false`, retoma ali.

```markdown
## Block 1 — Produto
**status:** complete

[respostas]

## Block 2 — Tom
**status:** complete

[respostas]

## Block 3 — Identidade
**status:** in_progress

[1ª pergunta respondida]
<!-- continuar pergunta 2 -->
```

### D-11 — Routing schema é YAML, não JSON

**Decisão:** plan output é YAML em `discovery.md` (Markdown-friendly), não JSON.

**Por quê:**
- Discovery.md é human-first — YAML lê melhor que JSON em prosa.
- Onda B (compose) e D (Ralph) podem fazer `yaml.safe_load` igualmente fácil.
- Ecoar pro usuário em prosa não-YAML mantém UX humano.

### D-12 — Critique mode preservado byte-perfect

**Decisão:** dispatch novo é wrapper externo. Quando shape = "<flutter-path>", o workflow original do critique roda **idêntico** ao atual — mesmas referências, mesmo handoff, mesmo agent isolado. Zero alterações em conteúdo da seção crítica.

**Por quê:** memória `feedback_design_spec_layering.md` lock: layer above não toca layer below. Modo critique é layer below; dispatch é layer above.

**Verificação:** smoke test com prompt idêntico antes/depois → output qualitativamente igual.

### D-13 — `--discuss` é placeholder em Onda A

**Decisão:** SKILL.md menciona o flag e seu modo, mas o handler só imprime: "Discuss mode chega na Onda C. Para entrevista formal, use `/juri` sem args. Para crítica, passe path." E sai.

**Por quê:** evita esquecer de adicionar suporte em A.1 dispatch (critique mode validaria flag não-conhecido?). Mantém superfície estável.

## 3. Components (novos arquivos)

### C-1 `skills/theme-critique/SKILL.md` (modificado)

Adiciona, do topo pra baixo, 4 seções novas:

1. `## Mode dispatch` (D-02)
2. `## Discovery mode` — pointer pra `references/discovery-protocol.md` + 1-paragraph overview
3. `## Discovery — auto-sizing` — pointer pra `references/discovery-sizing.md`
4. `## Discovery — output` — pointer pra `references/discovery-routing.md`

Tamanho-alvo pós-edição: ≤350 linhas (atual = 254; +~100 linhas é ok). Hard cap continua 500.

### C-2 `skills/theme-critique/references/discovery-protocol.md` (novo)

- Os 4 blocos × 11-12 perguntas exatas (PT-BR canônico).
- Vague-words list inline (REQ-A3.3 seed).
- Retry script literal.
- Tag schema `quality: weak|medium|strong`.
- Stop conditions (2 retries, max blocks).

### C-3 `skills/theme-critique/references/discovery-sizing.md` (novo)

- Tabela tier × deliverables (matriz 4×4).
- Override semantics.
- Decision tree para "qual tier escolher se detect e user discordam".

### C-4 `skills/theme-critique/references/discovery-doc-templates.md` (novo)

- 4 skeletons inline com placeholders `{{var}}`:
  - `product.md` (§1/§2/§3/§4/§5.3/§7/§8 sections, com 1 example-comment cada)
  - `design.md` (princípios)
  - `design-tokens.md` (tabelas vazias)
  - `PRD.md` (template per-intervention)
- Frontmatter schema do `discovery.md` (D-07/D-10).

### C-5 `skills/theme-critique/references/discovery-routing.md` (novo)

- Schema YAML `plan` (REQ-A6).
- Mapa decisão → skill (taxonomia condições → skills atômicas).
- Anti-padrões (auto-run, ETAs vagas, skill names inventados).

### C-6 `skills/theme-critique/references/discovery-resume.md` (novo)

- Validação de frontmatter (D-09).
- Algoritmo "find first incomplete block".
- Mensagens de erro user-facing quando resume falha.

### C-7 `scripts/detect_mode.py` (novo, canônico)

Script Python conforme D-03. Distribuído via `_sync.sh` atualizado.

### C-8 `scripts/_sync.sh` (modificado)

Adiciona `detect_mode.py` ao mapping:

```bash
declare -A USAGE=(
  [audit_theme.py]="theme-audit"
  [check_contrast.py]="theme-audit theme-extend theme-create"
  [generate_palette.py]="theme-create"
  [oklch_to_hex.py]="theme-create theme-extend"
  [detect_mode.py]="theme-critique"
)
```

E também `audit_theme.py` ganha um consumidor a mais (theme-critique usa em modo brownfield):

```bash
  [audit_theme.py]="theme-audit theme-critique"
```

### C-9 `.design-spec/.gitkeep` + `.design-spec/features/.gitkeep`

Diretórios versionados vazios para estabelecer hierarquia. `.design-spec/halt` NÃO é versionado (é runtime kill switch — Onda D).

### C-10 STATE.md (modificado)

Adiciona seção Onda A com decisões D-01..D-13 + deferred (discuss-mode, cross-feature pause, evals subjetivas Onda A).

### C-11 `evals/evals.json` para `theme-critique` (novo)

Adiciona evals discovery + critique:
- 2 critique evals (regression-grade) — output qualitative.
- 3 discovery evals: 1 greenfield walkthrough, 1 brownfield audit-referenced question, 1 vague-answer recusa.

(`theme-critique` evals foram deferred no skill-creator-alignment ciclo. Onda A é momento natural de criar — discovery agora exige cobertura.)

## 4. Verification strategy

| Camada | Como validar | Quando |
|---|---|---|
| Dispatch correctness | 4 prompts × 4 modos → log do modo escolhido | Pós-A.1 |
| `detect_mode.py` corretude | Repo sintético greenfield + brownfield + override | Pós-A.1 |
| Critique regression | Smoke prompt idêntico antes/depois; comparar Veredicto + Nielsen table presence | Pós-A.1 e final |
| Interview ordering | Inspeção manual de 1 walkthrough greenfield | Pós-A.2 |
| Vague-answer refusal rate | Eval `vague-user.json` 12 prompts → ≥80% recuse | Pós-A.2 |
| Doc generation | `git diff lib/` vazio; `ls docs/*.md` count por tier | Pós-A.2 |
| Brownfield audit reference | Grep number from audit em pergunta de stack block | Pós-A.2 |
| Routing schema | `python -c "import yaml; yaml.safe_load(open('discovery.md'))"` | Pós-A.3 |
| Resume correctness | Pause mid-block → `--resume` → continua bloco certo | Pós-A.3 |
| `quick_validate.py` | Script oficial passa sobre `theme-critique/` | Pós-A.3 |

## 5. Rollback

Tag `pre-design-spec-driven` já criada (T-00 do plano). Rollback se onda A falhar:

```bash
git checkout pre-design-spec-driven -- skills/theme-critique scripts/_sync.sh scripts/detect_mode.py
git checkout pre-design-spec-driven -- .design-spec  # se existir
git checkout pre-design-spec-driven -- .specs/project/STATE.md
```

Onda B/C/D depende de A — não há onda parcial: A passa todo ou volta ao tag.

## 6. Order of operations dentro de cada arquivo

Para evitar editar mesmo arquivo múltiplas vezes:

1. Criar todos os `references/discovery-*.md` (5 arquivos novos) primeiro.
2. Criar `scripts/detect_mode.py` + atualizar `_sync.sh` + rodar sync.
3. **Em uma única edição** de `skills/theme-critique/SKILL.md`:
   - Adicionar `## Mode dispatch`
   - Adicionar 3 pointers (`## Discovery mode`, `## Discovery — auto-sizing`, `## Discovery — output`)
   - Atualizar description do frontmatter (mencionar discovery, novos triggers `/Critic` mode-aware)
4. Criar `evals/evals.json` (após SKILL.md final, para alinhar prompts).
5. Criar `.design-spec/.gitkeep` + features dir.
6. Atualizar `STATE.md`.

## 7. Commit strategy

3 commits, espelhando A.1 / A.2 / A.3 (consistente com pattern do skill-creator-alignment):

```
commit 1: feat(theme-critique): dual-mode dispatch + sizing detection (Onda A.1)
commit 2: feat(theme-critique): discovery interview + brownfield pre-scan + doc gen (Onda A.2)
commit 3: feat(theme-critique): discovery routing + resume + evals (Onda A.3)
```

Após o último: `git tag onda-a` (espelha tag `pre-alignment` do ciclo anterior).

## 8. Não fazer (lições do alignment)

- ❌ Colons em description do frontmatter (D-04 do STATE.md). Usa "Triggered by", "Skip for".
- ❌ `<...>` em description (D-05). Usa "a Flutter path" em vez de `<path>`.
- ❌ Skill body >500 linhas (REQ-03 do alignment).
- ❌ Brand leak ("Fitio") — mantém genérico, mesmo que persona Júri venha do projeto Fitio.
- ❌ Auto-rodar próximo skill — Júri sempre devolve recomendação, usuário escolhe (REQ-A6.3).
