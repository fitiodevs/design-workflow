# Feature: skill-creator-alignment

> Alinhar o repo `design-workflow` (13 skills + scripts + install + README) com os padrões oficiais do `skill-creator` (Anthropic). Eliminar fricção de spec, vazamento de marca, falta de progressive disclosure, scripts órfãos, ausência de evals, e inconsistências entre README e SKILL.md.

**Status:** Draft (pronto pra execução)
**Owner:** fitiodev
**Created:** 2026-05-01
**Sized:** Large (multi-componente, ~28 tasks atômicos, dependências cruzadas)
**Source diagnosis:** análise prévia na conversa de origem (sessão `nova-ui-2`, 2026-05-01)

---

## 1. Contexto

`design-workflow` é um marketplace de plugin Claude Code com 13 skills extraídas de uso em produção no app Fitio. Foi publicado como `v0.1.0` no GitHub com posicionamento público, bilíngue e Flutter-first. Diagnóstico via `skill-creator` revelou 6 desvios sistêmicos do spec oficial:

1. Frontmatter carrega 2 campos não-spec (`license:`, `triggers:`) que o harness ignora.
2. As 13 descriptions vazam "Fitio" como marca — contradiz posicionamento público.
3. Nenhuma skill usa progressive disclosure (`references/`, `assets/`); 6 ultrapassam o threshold prático de janela de contexto.
4. Os 4 scripts Python ficam em `<repo>/scripts/` — install copia só `skills/*`, scripts ficam órfãos no destino.
5. Zero `evals/evals.json` — impossível rodar `improve_description.py` ou medir regressão.
6. README promete triggers EN (`/Auditor`, `/Composer`, `/Critic`, etc.) que não existem em nenhum SKILL.md.

## 2. Goal

Após esta feature, o repo `design-workflow` deve:

- Passar 100% nos checks do `quick_validate.py` do skill-creator.
- Disparar com qualidade equivalente em projetos Flutter genéricos (não-Fitio).
- Ter ≤500 linhas em todo SKILL.md, com tabelas/rubricas em `references/`.
- Distribuir scripts auto-contido por skill (cada skill que usa script tem ele em `<skill>/scripts/`).
- Ter `evals/evals.json` mínimo nas 4 skills com output verificável.
- Cumprir o que o README promete (triggers EN funcionais).

## 3. Non-Goals

- **Não** redesenhar a metodologia (Nielsen, OKLCH, slop patterns) — mexem só em forma, não em substância.
- **Não** adicionar skills novas, remover skills existentes, ou renomear personas.
- **Não** rodar a otimização automática `run_loop.py` nesta feature — fica como follow-up depois da limpeza estrutural.
- **Não** publicar release `v0.2.0` no GitHub — execução local + commit, release fica para outro ciclo.
- **Não** quebrar instalações existentes — `install.sh` continua re-runnable e idempotente.

## 4. Requirements

### REQ-01 — Frontmatter spec-compliant

- **REQ-01.1** Toda SKILL.md das 13 skills deve ter frontmatter contendo apenas `name` e `description` (e opcionalmente `compatibility`).
- **REQ-01.2** Os campos `license:` e `triggers:` devem ser removidos do frontmatter.
- **REQ-01.3** A informação útil de `triggers:` (regex aliases PT/EN) deve ser preservada no body do SKILL.md, em seção dedicada `## Triggers` (texto natural, não YAML).
- **REQ-01.4** O template em `template/SKILL.md` deve refletir a mesma estrutura limpa.
- **Verificação:** `grep -L "^license:\|^triggers:" skills/*/SKILL.md` retorna as 13 paths; nenhuma falsa positiva.

### REQ-02 — Descriptions agnósticas de marca

- **REQ-02.1** Substituir todas as 61 menções literais a "Fitio"/"fitio" nas 13 descriptions (frontmatter + body) por categoria genérica ("a Flutter app", "your design system", "the project", etc.).
- **REQ-02.2** Manter exemplos concretos em PT-BR onde adicionam pushiness ("essa tela tá fraca", "manda pro Stitch") — só remover marca, não tom.
- **REQ-02.3** Caminhos hardcoded como `lib/features/marketplace` em exemplos devem virar `lib/features/<feature>` ou `<your-app>/lib/`.
- **REQ-02.4** Referências a `docs/product.md` continuam (é convenção declarada do repo via `config.example.yaml`), mas devem citar config override.
- **Verificação:** `grep -ic "fitio" skills/*/SKILL.md` retorna 0 em todas; 1 menção residual aceitável só em footer de "originated from" se houver.

### REQ-03 — Progressive disclosure nas 6 skills longas

- **REQ-03.1** As 6 skills com >220 linhas devem extrair conteúdo de referência denso para `<skill>/references/<topico>.md`:

  | Skill | Atual | Extrair |
  |---|---|---|
  | theme-create | 380 | `references/oklch-recipes.md`, `references/slop-patterns.md` |
  | theme-port | 277 | `references/text-hierarchy.md`, `references/widget-mapping.md` |
  | theme-motion | 276 | `references/motion-tokens.md`, `references/flutter-animate-snippets.md` |
  | ux-writing | 273 | `references/quality-standards.md`, `references/before-after-patterns.md` |
  | frontend-design | 263 | `references/clara-checklist.md` |
  | theme-critique | 259 | `references/nielsen-rubric.md` |

- **REQ-03.2** Cada SKILL.md pós-extração deve ficar ≤200 linhas (target) e ≤500 linhas (hard cap).
- **REQ-03.3** SKILL.md deve apontar para cada arquivo extraído com instrução clara de quando lê-lo (ex: "Para o rubric completo Nielsen 0–4, leia `references/nielsen-rubric.md` antes de scoring").
- **REQ-03.4** Conteúdo extraído deve ser **literal copy** — nenhuma simplificação ou edição não-mecânica nesta feature.
- **Verificação:** `wc -l skills/*/SKILL.md` mostra todas ≤200; `find skills/*/references -name "*.md" | wc -l` ≥ 9.

### REQ-04 — Scripts auto-contidos por skill

- **REQ-04.1** Os 4 scripts em `<repo>/scripts/` devem ser distribuídos em `<skill>/scripts/` conforme uso real:

  | Script | Skills consumidoras (todas recebem cópia) |
  |---|---|
  | `audit_theme.py` | `theme-audit` |
  | `check_contrast.py` | `theme-audit`, `theme-extend`, `theme-create` |
  | `generate_palette.py` | `theme-create` |
  | `oklch_to_hex.py` | `theme-create`, `theme-extend` |

- **REQ-04.2** `<repo>/scripts/` continua existindo como **fonte canônica** (single source of truth) — cópias por skill são geradas via `install.sh` (symlink ou copy físico, decisão na design.md).
- **REQ-04.3** Cada skill que usa script deve referenciar caminho relativo `scripts/<nome>.py` (a partir do diretório da skill), não path absoluto.
- **REQ-04.4** `install.sh` deve garantir que após rodar, cada skill instalada em `~/.claude/skills/<skill>/` tenha seu `scripts/` populado.
- **Verificação:** após `./install.sh`, `find ~/.claude/skills -name "*.py" | wc -l` retorna ≥6 (sem contar duplicatas que vêm de symlinks); `python ~/.claude/skills/theme-audit/scripts/check_contrast.py --help` executa sem ImportError.

### REQ-05 — Evals minimal-viable

- **REQ-05.1** Criar `<skill>/evals/evals.json` para as 4 skills com output objetivamente verificável: `theme-audit`, `theme-extend`, `theme-port`, `theme-create`.
- **REQ-05.2** Cada `evals.json` deve seguir schema do skill-creator (`references/schemas.md`):
  ```json
  {
    "skill_name": "theme-audit",
    "evals": [
      {"id": 1, "prompt": "...", "expected_output": "...", "files": [], "assertions": [...]}
    ]
  }
  ```
- **REQ-05.3** Cada eval contém 3 prompts realistas + 4-5 assertions objetivas (regex match, file existence, contrast ratio threshold, etc.).
- **REQ-05.4** Skills com output subjetivo (`theme-critique`, `frontend-design`, `ux-writing`, `theme-bolder`, `theme-quieter`, `theme-distill`, `theme-motion`, `theme-prompt`, `theme-sandbox`) NÃO ganham evals nesta feature — fica como TODO em STATE.md.
- **Verificação:** `find skills/*/evals -name "evals.json" | wc -l` = 4; cada `evals.json` valida contra `jq '.evals | length >= 3'`.

### REQ-06 — Triggers EN no body do SKILL.md

- **REQ-06.1** Cada uma das 13 skills deve declarar no body, na seção `## Triggers`, ambas linhas EN e PT:
  ```
  ## Triggers
  English: /Auditor, /audit-theme
  Português: /Lupa, /lupa, /theme-audit
  Natural language: "audita o tema", "scan hardcode", ...
  ```
- **REQ-06.2** Mapeamento EN ↔ PT segue tabela do README §Quickstart:

  | PT | EN |
  |---|---|
  | Lupa | Auditor |
  | Compositor | Composer |
  | Júri | Critic |
  | Brasa | Amplifier |
  | Calma | Refiner |
  | Lâmina | Distiller |
  | Jack | Choreographer |
  | Clara | Designer |
  | Pena | Writer |
  | Cirurgião | Surgeon |
  | Arquiteto | Architect |
  | Orquestrador | Orchestrator |

- **REQ-06.3** A description do frontmatter deve mencionar pelo menos 1 trigger EN além dos PT existentes (para que disparo via `/Auditor` funcione).
- **Verificação:** para cada skill, `grep -E "/(Auditor|Composer|Critic|Amplifier|Refiner|Distiller|Choreographer|Designer|Writer|Surgeon|Architect|Orchestrator)" skills/<skill>/SKILL.md` retorna ≥1 linha.

### REQ-07 — Validação spec via skill-creator

- **REQ-07.1** Após todas as mudanças, rodar `python -m scripts.quick_validate <skill-path>` (do skill-creator) nas 13 skills.
- **REQ-07.2** Todas as 13 devem passar; warnings aceitáveis, errors não.
- **REQ-07.3** Documentar resultado em `STATE.md` na seção `Validation runs`.
- **Verificação:** sem erros em nenhum dos 13 outputs.

### REQ-08 — README e marketplace.json sincronizados

- **REQ-08.1** README §Quickstart já promete triggers EN; agora que existem, validar redação.
- **REQ-08.2** `marketplace.json` continua válido (não muda lista de plugins).
- **REQ-08.3** Adicionar seção em README "What changed in v0.2" com bullet das 6 frentes.
- **REQ-08.4** Bumpar version em `marketplace.json` de `0.1.0` para `0.2.0`.
- **Verificação:** `jq '.metadata.version' .claude-plugin/marketplace.json` retorna `"0.2.0"`.

## 5. Out of scope (deferred)

- Rodar `improve_description.py` (loop de otimização) — depende de evals existentes; tracker em STATE.md.
- Evals para 9 skills subjetivas — exige human-review viewer; tracker em STATE.md.
- Internacionalizar README e docs — mantém PT/EN mistos; outro ciclo.
- Publicar release GitHub `v0.2.0` — execução manual pelo owner pós-merge.

## 6. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Editar 13 frontmatters quebra triggering em workflows ativos do Fitio | Média | Snapshot do estado atual em git tag `pre-alignment` antes de começar |
| Extração para `references/` perde fidelidade do conteúdo | Baixa | REQ-03.4 exige cópia literal; review diff por skill |
| `install.sh` fica complexo demais lidando com scripts | Média | Decisão symlink-vs-copy na design.md; manter ≤30 linhas |
| Triggers EN colidem com outros plugins do usuário | Baixa | Slugs são específicos (`/Auditor`, `/Choreographer`); colisão improvável |

## 7. Acceptance criteria (sign-off)

- [ ] REQ-01 a REQ-08 todos verificados
- [ ] `flutter analyze` (não aplicável — repo é skills, não Flutter)
- [ ] Diff de cada SKILL.md revisado
- [ ] `install.sh` testado em diretório limpo (`/tmp/test-install/`)
- [ ] Commit único bem mensageado, ou commit por requirement (decisão na design.md)
