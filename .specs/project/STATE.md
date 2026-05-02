# STATE — design-workflow

Persistent state across feature ciclos. Read at session start.

## Decisions

- **D-01 — Frontmatter spec compliance.** Drop `license:` and `triggers:` YAML keys. Move trigger info to a `## Triggers` section in the body. Date: 2026-05-01 (skill-creator-alignment).
- **D-02 — Brand-agnostic descriptions.** Replace literal "Fitio" mentions in skill descriptions/bodies with generic phrasing ("a Flutter app", "the project", "your design system"). Examples and tone preserved. Date: 2026-05-01.
- **D-03 — Scripts copy strategy.** Single source of truth in `<repo>/scripts/`. `scripts/_sync.sh` copies into each consuming skill's `scripts/` subdir; copies are committed so `git clone` + manual use works without running `_sync.sh`. Symlinks rejected (Windows/iCloud sync issues). Date: 2026-05-01.
- **D-04 — Description colon discipline.** YAML frontmatter parsing breaks when descriptions contain "Triggers:", "Persona:", "NOT for:" — colons are interpreted as YAML mapping. Use "Triggered by", "Invokes the X persona", "Skip for" instead. Discovered via `quick_validate.py` after Onda 1. Date: 2026-05-01.
- **D-05 — Description angle-bracket ban.** `quick_validate.py` rejects `<...>` inside descriptions (interpreted as placeholder leakage). Substitute with quoted strings or descriptive prose ("`/theme-port --from-stitch` plus an HTML path"). Date: 2026-05-01.

## Validation runs

### 2026-05-01 — skill-creator `quick_validate.py` (full sweep, 13 skills)

Tool: `/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py`

Result: **13/13 valid**, zero errors, zero warnings.

```
=== skills/frontend-design/ ===   Skill is valid!
=== skills/theme-audit/ ===       Skill is valid!
=== skills/theme-bolder/ ===      Skill is valid!
=== skills/theme-create/ ===      Skill is valid!
=== skills/theme-critique/ ===    Skill is valid!
=== skills/theme-distill/ ===     Skill is valid!
=== skills/theme-extend/ ===      Skill is valid!
=== skills/theme-motion/ ===      Skill is valid!
=== skills/theme-port/ ===        Skill is valid!
=== skills/theme-prompt/ ===      Skill is valid!
=± skills/theme-quieter/ ===      Skill is valid!
=== skills/theme-sandbox/ ===     Skill is valid!
=== skills/ux-writing/ ===        Skill is valid!
```

Iteration history before final: first sweep flagged 8 frontmatter parse errors (colons inside descriptions) and 2 angle-bracket errors (`<path>`, `<html>`). Fixed in commit Onda 3 by rephrasing descriptions per D-04 / D-05.

## Deferred

### Auto-improvement loop (`improve_description.py`)
- **Status:** deferred to next ciclo.
- **Why:** depends on existing `evals.json` per skill; this ciclo only added evals for the 4 verifiable skills (audit/extend/port/create). Loop output for the other 9 would be noise.
- **Next step:** wait until subjective evals exist OR run loop only on the 4 evals-equipped skills as a sanity check.

### Evals for 9 subjective skills
- **Skills missing evals:** `theme-critique`, `frontend-design`, `ux-writing`, `theme-bolder`, `theme-quieter`, `theme-distill`, `theme-motion`, `theme-prompt`, `theme-sandbox`.
- **Why deferred:** outputs are subjective (Nielsen score, AI-slop verdict, copy quality) — assertions need human-review viewer or LLM-as-judge protocol.
- **Next step:** decide between (a) human-review viewer like `skill-creator` ships, (b) LLM-as-judge with rubric in repo, or (c) skip and lean on `improve_description.py` qualitative loop.

### GitHub release v0.2.0
- **Status:** local commit only; no `git push` and no `gh release create` performed in this ciclo.
- **Next step:** owner runs `git push origin main && git push origin v0.2.0` (after tagging) and `gh release create v0.2.0 --notes-from-tag`.

### SKILL.md target ≤200 lines (target, not hard cap)
- **Status:** 4/13 hit target (≤200). Remaining 9 are 201–254 lines (well within 500 hard cap). Spec REQ-03.2 says ≤200 is target, ≤500 is hard cap.
- **Why deferred:** further extraction would split semantically related workflow steps. Marginal value vs. fragmentation cost is unclear.
- **Next step:** revisit if a future skill exceeds 300 lines or if `quick_validate` adds a ≤200 hard rule.

## Open spec features

- `.specs/features/skill-creator-alignment/` — completed 2026-05-01 in 3 commits (Onda 1/2/3). All 8 REQs verified. Acceptance criteria met.
- `.specs/features/onda-a-discovery/` — completed 2026-05-02 in 3 commits (Onda A.1/A.2/A.3). All 6 REQs verified end-to-end via SKILL.md + 5 references + detect_mode.py + 5 evals. Critique mode preserved byte-perfect.

---

## Onda A — Discovery (2026-05-02)

### Decisões locked

- **D-A1 — Discovery extends `theme-critique`, NÃO nova skill.** Persona Júri é uma só; trigger `/juri` é único. Nova skill quebraria unicidade. Discovery vive em `theme-critique/SKILL.md` via dispatch table + `references/discovery-*.md`.
- **D-A2 — Dispatch por shape do argumento.** `/juri` (no args) → discovery; `/juri <flutter-path>` → critique; `/juri --discuss` → placeholder; `/juri --resume <feature>` → resume. Resolution: flag → path → discovery default.
- **D-A3 — `detect_mode.py` é determinístico.** Heurística greenfield: commits<10 AND dart_files<5 AND no docs/product.md (>2KB). Brownfield caso contrário. LLM não decide sizing.
- **D-A4 — Override (`--mode`) sempre vence detecção.** Se discrepa em >1 nível, Júri loga warning antes de prosseguir.
- **D-A5 — Vague-words list + 2 retries.** 12 termos PT-BR + 12 EN. 3 retry templates. Após 2 retries → persiste `quality: weak`, segue. Nunca trava.
- **D-A6 — Skeletons inline em Markdown, não Python.** `discovery-doc-templates.md` carrega templates com placeholders `{{var}}`. Júri substitui via Write tool.
- **D-A7 — `.design-spec/` é runtime; `.specs/` é planning.** Discovery escreve em `.design-spec/features/<feature>/`. STATE.md continua em `.specs/project/`.
- **D-A8 — Resume valida frontmatter strict.** Status `in_progress` obrigatório. Idade >14d → warning (Onda A); regra mais firme em Onda C.
- **D-A9 — Routing schema é YAML em `discovery.md`, não JSON separado.** Human-first. Onda B/D parsam via `yaml.safe_load`.
- **D-A10 — Critique mode preservado byte-perfect.** Nenhuma seção do workflow original alterada; apenas seções novas adicionadas acima dele.
- **D-A11 — Discuss mode (`--discuss`) é placeholder em Onda A.** Imprime mensagem informativa e sai. Comportamento socrático em Onda C.
- **D-A12 — `audit_theme.py` ganha consumer adicional `theme-critique`** (brownfield pre-scan). `_sync.sh` atualizado.
- **D-A13 — Evals discovery + critique** consolidados em 1 `evals.json` no `theme-critique/`. 5 evals (2 critique-regression, 3 discovery scenarios).

### Validation runs

#### 2026-05-02 — Onda A acceptance

- `python3 detect_mode.py` em repo design-workflow: returns valid JSON `{"mode": "greenfield", "tier_recommended": "greenfield", ...}`.
- `bash scripts/_sync.sh`: synced 9 script copies into skills/{theme-audit,theme-critique,theme-extend,theme-create}/scripts/.
- `quick_validate.py skills/theme-critique`: **Skill is valid!** (no errors).
- `wc -l skills/theme-critique/SKILL.md`: 331 lines (≤400 target, ≤500 hard cap).
- `jq '.evals | length' skills/theme-critique/evals/evals.json`: 5.
- Critique-mode regression: SKILL.md §Workflow/Setup gates/Inputs/Persona blocks intact; only new sections inserted before §Persona — Júri.
- `find skills/theme-critique/references/`: nielsen-rubric.md + 5 discovery-*.md = 6 files (target ≥6).

## Deferred (Onda A → consumed in B/C)

### Discuss-mode completo (REQ-C2)
- **Status:** scaffolding apenas em Onda A (placeholder mensagem).
- **Why:** complexidade do socratic dialog merece onda dedicada (Onda C — productivity).
- **Next step:** Onda C — `/juri discuss <topic>` informal, zero file diffs, transição com consent para `specify`.

### Cross-feature pause/resume (REQ-C1)
- **Status:** Onda A só implementa `--resume <feature>` da entrevista atual. Pause global de feature em qualquer fase fica para Onda C.
- **Next step:** Onda C — `/design-spec pause` + `pause-state.yaml`.

### Decisões tracking (`decisions.md`) — REQ-B4
- **Status:** Júri Discovery escreve respostas-decisão em `discovery.md` (e.g. axis = drenched). Formato `decisions.md` formal com schema `{id, decision, reason, date, supersedes?}` é Onda B.
- **Next step:** Onda B — refining skills (Brasa/Calma/Lâmina/Jack) leem `decisions.md` antes de propor mudança.

### Stack-agnostic adapter
- **Status:** Onda A é Flutter-first hard-coded (`detect_mode.py` busca `lib/*.dart`). Adapter para React Native / SwiftUI / web fica para Onda E pós-v1.0.

## Onda B — Spec-driven workflow (2026-05-02)

### Decisões locked

- **D-B1 — 3 wrapper skills, não 1 mega-skill.** `compose`, `sequence`, `ship` separadas. Cada uma é fina (~125 linhas SKILL.md) e responsável por 1 phase + gate.
- **D-B2 — Phase gate é hard-stop.** Cada wrapper recusa iniciar se o input phase está com `status` != `approved`. Sem fallback "auto-aprovar com flag".
- **D-B3 — `decisions.md` schema YAML em `.design-spec/project/decisions.md`.** Schema canônico em `skills/compose/references/decisions-schema.md`. Refining skills (Brasa/Calma/Lâmina/Jack) ler antes de propor mudança em fase futura (lockable em Onda D).
- **D-B4 — Atomic commits com `Refs: <feature>/<T-id>` footer.** Squash forbidden during Ship (preserves rollback granularity).
- **D-B5 — `--interactive` e `--dry-run` em Ship.** Default é auto-execute; flags pra stakes altos / debug.
- **D-B6 — Ship NUNCA auto-merges PR.** Hard rule (REQ-D4.4 já antecipa para Ralph). Ship só commita; merge é humano.

### Validation runs (2026-05-02)

- 3 new skills (`compose`, `sequence`, `ship`) — quick_validate: all valid.
- SKILL.md sizes: 121 / 125 / 127 (≤200 target).
- Each skill has 1+ references + evals.json (3 evals each).
- `decisions.md.template` seed em `.design-spec/project/`.

### Deferred (Onda B → Onda C/D)

- **`/design-spec approve <phase> <feature>` convenience command** — Onda C (Productivity).
- **Refining-skill enforcement leitura `decisions.md`** — Onda D (Ralph) lockable; em Onda B é norma documentada não-mecanizada.

## Onda C — Productivity layer (2026-05-02)

### Decisões locked

- **D-C1 — Pause/resume são thin orchestrators numa skill `productivity`.** Não merecem skill própria cada — cohesion alta (todos lidam com state inspection / state mutation). Subcommands na mesma skill.
- **D-C2 — `pause-state.yaml` é deletado após resume "continue".** Re-prioritize preserva (com `superseded_by`). Re-uso confuso é pior que perder estado.
- **D-C3 — 14 dias é o cutoff de re-discovery suggestion.** Hard rule no resume; `/juri --mode light` é o sugerido.
- **D-C4 — `design_state.py` é determinístico, paralelo a `detect_mode.py`.** Read-only, sem LLM. JSON ou prose.
- **D-C5 — `/design-spec approve` valida schema antes de flipar status.** Convenience é gate, não bypass.
- **D-C6 — `discuss` mode é stateless por design.** Zero file diffs em `discovery-discuss.md`. Transition para `specify` é por consent explícito.
- **D-C7 — `specify` é alias do discovery default com slug pré-definido.** Mantém superfície fina; sem novo dispatch path.

### Validation runs (2026-05-02)

- `quick_validate skills/productivity`: valid (após remover `<...>` do description — recorrência D-05).
- `quick_validate skills/theme-critique`: valid (regression — adicionado discuss + specify modes).
- `python scripts/design_state.py --json`: válido em <1s no repo `design-workflow`.
- SKILL.md sizes: productivity=75, theme-critique=337 (≤400 target).

### Deferred (Onda C → Onda D)

- **Cycle detection no resume** quando ramos de discovery foram superseded mas ainda referenciados em decisions.md (Onda D budget+audit fortalece).

## Onda D — Ralph autonomy (2026-05-02)

### Decisões locked

- **D-D1 — Skill `ralph-loop/` é skill nova, não modo de skill existente** (alinhado com memory `decision_ralph_separate_skill.md`). Thin orchestrator; gating + budget + audit são primários.
- **D-D2 — Loop é dumb, prompt é smart, halts são duros.** `ralph_tick.py` é skeleton determinístico; spawn da skill via harness model.
- **D-D3 — `.design-spec/halt` é checked PRIMEIRO em cada tick.** Antes de budget. Antes de tudo. Halt-file = exit imediato.
- **D-D4 — Tier 2 e Tier 3 NUNCA auto-merge.** Sempre PR draft. Hard rule (REQ-D4.4). Mesma regra para Tier 2 (não só Tier 3).
- **D-D5 — `budget.yaml` é human-set, Ralph nunca muta.** 100% halt; 80% warn. Per-tier overrides opcionais.
- **D-D6 — Audit log é JSONL append-only.** `loop-log/<YYYY-MM-DD>.jsonl` por feature. Greppable + DuckDB-friendly. Ops gerencia retention.
- **D-D7 — Persona injection per tick.** `voice_dna` re-loaded da SKILL.md spawned, sem confiar contexto. Drift detection a cada 10 ticks.
- **D-D8 — Cycle detection com janela de 3 ticks.** Operator + file tuple; oscilação Brasa↔Calma halts.
- **D-D9 — 3 GH Workflow templates** em `skills/ralph-loop/workflows/` (não em `.github/workflows/` direto — adopters copiam).
- **D-D10 — Mínimo YAML reader nativo no `ralph_tick.py`** para evitar PyYAML dep. Suporta caps + per-tier overrides.

### Validation runs (2026-05-02)

- `quick_validate skills/ralph-loop`: valid.
- SKILL.md = 148 linhas.
- 5 references (budget, halt-conditions, persona-injection, cycle-detection, audit-log-schema).
- 3 workflow templates (watch / pre-merge / sprint).
- 2 scripts (ralph_tick.py, ralph_budget.py) sincronizados.
- 5 evals (3 tier scenarios + halt-file + cycle-detection).
- `python scripts/ralph_budget.py`: roda em <1s, output esperado quando log vazio.

### Deferred (Onda D → pós-v1.0)

- **Persona drift quantitative threshold tuning.** Marcado em `persona-injection.md`; baseline empírico depende de dados de produção.
- **Cost calibration por modelo.** Estimates em `budget-protocol.md` são para Sonnet-class; Opus/Haiku bumps deferred.
- **Stack-agnostic adapter.** Onda E pós-v1.0.

## Conventions reminder

- Source of truth for scripts: `<repo>/scripts/<name>.py`. Edit there, then re-run `bash scripts/_sync.sh`.
- Source of truth for evals: `<repo>/skills/<skill>/evals/evals.json`. Schema follows `skill-creator/references/schemas.md`.
- Spec/design/tasks live in `.specs/features/<feature-name>/`. State (decisions, deferred) lives here.
