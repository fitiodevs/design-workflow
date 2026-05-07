# STATE — design-workflow

Persistent state across feature ciclos. Read at session start.

## Decisions

- **D-01 — Frontmatter spec compliance.** Drop `license:` and `triggers:` YAML keys. Move trigger info to a `## Triggers` section in the body. Date: 2026-05-01 (skill-creator-alignment).
- **D-02 — Brand-agnostic descriptions.** Replace literal "Fitio" mentions in skill descriptions/bodies with generic phrasing ("a Flutter app", "the project", "your design system"). Examples and tone preserved. Date: 2026-05-01.
- **D-03 — Scripts copy strategy.** Single source of truth in `<repo>/scripts/`. `scripts/_sync.sh` copies into each consuming skill's `scripts/` subdir; copies are committed so `git clone` + manual use works without running `_sync.sh`. Symlinks rejected (Windows/iCloud sync issues). Date: 2026-05-01.
- **D-04 — Description colon discipline.** YAML frontmatter parsing breaks when descriptions contain "Triggers:", "Persona:", "NOT for:" — colons are interpreted as YAML mapping. Use "Triggered by", "Invokes the X persona", "Skip for" instead. Discovered via `quick_validate.py` after Onda 1. Date: 2026-05-01.
- **D-05 — Description angle-bracket ban.** `quick_validate.py` rejects `<...>` inside descriptions (interpreted as placeholder leakage). Substitute with quoted strings or descriptive prose ("`/theme-port --from-stitch` plus an HTML path"). Date: 2026-05-01.
- **D-06 — Brand sweep extends to script bodies.** REQ-02 originally scoped only SKILL.md frontmatter+body. 2026-05-05 sweep extended de-branding to script comments (`audit_theme.py`, `check_contrast.py`, `generate_palette.py`) and the `theme-create/evals/evals.json` example prompt ("Fitio Arena" → "<app> Arena"). Rationale: scripts ship in the marketplace install — public users read them. Provenance lines (README §What changed in v1.0, marketplace.json author "Fitio") preserved as attribution. Date: 2026-05-05.
- **D-07 — Personas ship globally as PT+EN pair.** `~/.claude/CLAUDE.md` persona table now lists EN aliases alongside PT names (Lupa/Auditor, Compositor/Composer, Júri/Critic, etc.) so squads multilíngues invocam o mesmo cara. Public-repo SKILL.md descriptions já mencionam ambos por persona. Date: 2026-05-05.
- **D-08 — Stitch-specific naming retired; HTML mode preserved and generalized.** Removed `skills/theme-prompt/` and `skills/theme-sandbox/` (both were Stitch-orchestration-only). On `theme-port`, the flag `--from-stitch` was renamed `--from-html` and the tool-specific assumptions were stripped (no Atelier cache directory expectation; sibling `.png` is now optional, not required). Reason: `theme-port`'s job is "structural source → Flutter using project tokens" — the HTML parser (regex extracts widths/heights/border-radius/padding/gap, maps Tailwind to AppSpacing/AppRadius, discards colors/box-shadow/transitions) is generic and valuable for any HTML mockup source (`/frontend-design`, Figma's HTML export, Penpot, Stitch, hand-written). The two skills removed were truly Stitch-specific and would not generalize without becoming hollow. Affected callers cleaned: `theme-port` SKILL+evals, `frontend-design`, `theme-audit`, `theme-critique/references/discovery-routing.md`, `sequence/evals/evals.json`, `docs/personas.md`, `docs/theme-manager.md`. Date: 2026-05-05.
- **D-09 — Atlas trio promoted to public, paths generalized.** `fitio-status`, `fitio-promote`, `fitio-atlas-save` (private, hardcoded `Fitio/fitio/.specs/` paths and 3-repo monorepo assumption) became public `status`, `promote`, `atlas-save`. Generalizations: `repo` frontmatter is optional (single-repo projects skip the column); Obsidian export is opt-in (`OBSIDIAN_VAULT` env var or `.atlas-save.yaml`); `flutter analyze` references generalized to "the project verify gate". Helper scripts (~1.3k LOC of Python) deferred to v1.2 — v1.1 ships SKILL.md only; the model reads `.specs/` / `docs/backlog/` / `memory/active_work.md` directly. Date: 2026-05-05.
- **D-10 — `promote` recommends but does not depend on tlc lifecycle.** After writing the spec triplet, `promote` recommends `/tlc-spec-driven specify <name>` (refine) and `/tlc-closure <name>` (verify dependency closure). If those skills are not installed, the recommendation degrades to a manual-review hint. Reason: keep `design-workflow` self-contained while making the integrated path obvious. Date: 2026-05-05.
- **D-11 — `craft/` adoption from open-design.** 5 docs (`anti-ai-slop`, `color`, `state-coverage`, `typography`, `animation-discipline`) forked verbatim from `nexu-io/open-design` at SHA `26636384a8dc3e9b36029c3b6299d4a2005d255a` (Apache-2.0; originally derived from `referodesign/refero_skill`, MIT). Each file carries the full attribution chain in its header. Sync is manual on demand — no automated puller. Reason: `craft/` encodes universal design rules upstream from any project's tokens; a fork keeps the rules versioned with our skills while honoring upstream provenance. Date: 2026-05-06.
- **D-12 — `dw:` namespace nested under `metadata:`.** Field is `metadata.dw.craft.requires:` in SKILL.md frontmatter (T-07 probe: top-level `dw:` rejected by `quick_validate.py`; `metadata:` is opaque, accepts arbitrary nested content). Distinct from upstream's `od:` — `dw.*` is owned by this repo and we do not consume `od:`. If a future field has a direct `od:` equivalent, document it in `docs/skill-extensions.md` and keep names parallel. Date: 2026-05-06.
- **D-13 — `install.sh` bundles `craft/` and rewrites refs to absolute paths.** v1.1.1 wired the 5 skills with `craft/<doc>.md` references that resolve project-relative — fine when the user works inside the design-workflow repo, but `install.sh` lands skills globally in `~/.claude/skills/` so `craft/` was unreachable from any other cwd. v1.1.2 fixes by (1) copying `craft/*.md` into `~/.claude/craft/` and (2) running `sed` on the 5 wired SKILL.md copies after install to rewrite `` `craft/<doc>.md` `` → `` `~/.claude/craft/<doc>.md` ``. Source SKILL.md in the repo stays unchanged so the Craft references section reads naturally for users who clone the repo. Discovered while syncing local install on 2026-05-06; deployment bug, no spec needed. Date: 2026-05-06.
- **D-11.1 — `design-context.md` authored from scratch.** huashu-design's license (Personal Use Only) prevented forking; we wrote our own under Apache-2.0 citing the structural idea (5-tier context hierarchy preceding generation). Refusal rule (`STOP if no Tier 1-4 context`) is sharper than upstream's "vague brief is last resort" wording; concrete tier examples are Flutter/Next.js-specific to our stacks. Wired by 5 skills (`theme-port`, `theme-create`, `theme-extend` (NEW), `theme-critique`, `frontend-design`); `theme-extend` gains Tier 1 dependency, `theme-bolder` / `theme-motion` / `ux-writing` stay unwired (they have own context models). Shipped v1.2.1 standalone (v1.1.2 was overtaken by v1.2.0 multi-stack adapter on 2026-05-07). Date: 2026-05-07.

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

### 2026-05-05 — quick_validate.py (v1.1 sweep, 19 skills, post Stitch retirement + Atlas promotion)

Result: **19/19 valid**, zero errors, zero warnings. Reflects v1.1.0 state: 11 atomic operators (theme-* minus theme-prompt/theme-sandbox + frontend-design + ux-writing), 5 orchestration layer skills (compose, sequence, ship, productivity, ralph-loop), 3 productivity helpers promoted from Atlas trio (status, promote, atlas-save).

```
atlas-save: Skill is valid!
compose: Skill is valid!
frontend-design: Skill is valid!
productivity: Skill is valid!
promote: Skill is valid!
ralph-loop: Skill is valid!
sequence: Skill is valid!
ship: Skill is valid!
status: Skill is valid!
theme-audit: Skill is valid!
theme-bolder: Skill is valid!
theme-create: Skill is valid!
theme-critique: Skill is valid!
theme-distill: Skill is valid!
theme-extend: Skill is valid!
theme-motion: Skill is valid!
theme-port: Skill is valid!
theme-quieter: Skill is valid!
ux-writing: Skill is valid!
```

### 2026-05-05 — quick_validate.py (full sweep, 18 skills, post brand-sweep)

Result: **18/18 valid**, zero errors, zero warnings. Includes the 5 layer skills shipped in v1.0 (compose, sequence, ship, productivity, ralph-loop) plus the 13 originals after the script-comment + evals brand sweep (D-06).

```
compose: Skill is valid!
frontend-design: Skill is valid!
productivity: Skill is valid!
ralph-loop: Skill is valid!
sequence: Skill is valid!
ship: Skill is valid!
theme-audit: Skill is valid!
theme-bolder: Skill is valid!
theme-create: Skill is valid!
theme-critique: Skill is valid!
theme-distill: Skill is valid!
theme-extend: Skill is valid!
theme-motion: Skill is valid!
theme-port: Skill is valid!
theme-prompt: Skill is valid!
theme-quieter: Skill is valid!
theme-sandbox: Skill is valid!
ux-writing: Skill is valid!
```

## Deferred

### Atlas trio helper scripts (v1.2)
- **Status:** deferred from v1.1.
- **Why:** The originating Fitio repo has ~1.3k LOC of Python supporting the Atlas trio (`scan_active_work.py`, `mark_task.py`, `normalize_tasks.py`, `save_session.py`). Porting them generically (config-driven repo discovery, no Fitio-specific path assumptions, no monorepo-specific marker code) is a half-day effort and was scoped out of v1.1 to keep the release small. v1.1 ships SKILL.md only — the model executes the algorithm by reading `.specs/`/`docs/backlog/`/`memory/active_work.md` directly with `Read` + `Bash`.
- **Next step:** port the 4 scripts to `skills/{status,promote,atlas-save}/scripts/` with config-driven repo discovery; ship as v1.2.

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

## Onda E — Multi-stack adapter (2026-05-07, v1.2.0)

### Decisões locked

- **D-14 — Adapter contract: stack-agnostic Plan + 2 reference adapters in v1.2.** `docs/adapter-protocol.md` + `docs/adapter-plan.schema.json` define an intermediate format (token roles, widget tree, motion intent, file actions). `adapters/flutter/` ships byte-equivalent to pre-v1.2 (Fitio dogfood path unchanged). `adapters/nextjs-tailwind/` is new — emits CSS custom properties + Tailwind config snippet + TSX (shadcn-aware). `theme-port` and `theme-extend` migrated; `theme-create` / `theme-motion` / `theme-bolder` / `theme-quieter` / `theme-distill` deferred to v1.3 phase-2 (`adapter-migration-phase-2`). Other stacks (React Native, Vue, Svelte, plain-React, Angular, SwiftUI) are additive in v1.3+, one PR each.
- **D-15 — Reverse "Web out of scope" ROADMAP entry.** Original ROADMAP §"Out of scope" rejected Tailwind/MUI on the basis of "different aesthetic vocabulary, would require a separate web-design-workflow repo." That premise was wrong — anti-AI-slop and craft references are the same in JSX as in Dart; only emission syntax differs. Adapter pattern keeps everything in-repo without diluting brand. Entry struck through with date marker; v1.3+ adapter backlog listed.
- **D-16 — Roadmap reorder: adapter pulled forward 2 versions.** Originally `multi-stack-adapter` was scheduled v1.4.0; user urgency on Next.js+Tailwind pulled it to v1.2.0. Original v1.2 (`inspiration-library`) shifted to v1.3, original v1.3 (`interactive-mockup-stage`) shifted to v1.4. Reason: weak dependency between specs (inspiration-library and interactive-mockup-stage are orthogonal to stack support); user blocked on Next.js work.
- **D-17 — DESIGN.md library: 20-entry curated subset of upstream `nexu-io/open-design`'s 71.** Cap-per-category prevents AI/SaaS overload (cap 3) and keeps `--browse` presentable; coverage is breadth-first across 10 buckets (AI&LLM · Dev Tools · Productivity · Backend/Data · Design/Creative · Fintech · E-Commerce · Media · Automotive · Editorial). Attribution chain is per-file (header section: Sourced from / Upstream / License / Local path / Last sync). Sync is **manual** — re-fork by re-running the loop in `.specs/features/inspiration-library/tasks.md` against a new SHA. Pinned at `d4b547caa7cafbf328c262cdf08dd275f5bdc4d6` (2026-05-07). Date: 2026-05-07.
- **D-18 — Translator semantics: inference chain priority + always-flag failures.** `scripts/design_md_to_appcolors.py` maps DESIGN.md → 29-token AppColors using priority chain — (1) per-entry NAME keyword override (matches `Border Cream`, `Pure White`, `Cohere Black`), (2) section-level keyword (matches `### Surface & Background` → surface), (3) description hint (catches "Page background" in description text), (4) WCAG-corrected fallback. Native-mode detection from first surface luminance: dark-native sources (Linear, Apple, Sentry, Spotify, Supabase, Raycast, Framer) build dark proposal from source and L-flip light; light-native sources do the inverse. **Never silently picks for the 7 game/badge tokens** — those are flagged as `<user-input>` in the rationale. Industry-standard defaults fill missing feedback colors when source has no warning/error (e.g. Linear) — also flagged. Brand-on-text WCAG failures surfaced explicitly, never silenced. Validates 22/22 sources with 8-11/{10,11} pairs passing per mode. Date: 2026-05-07.
- **D-19 — Tweaks is a transformer, not a generator.** `/tweaks <input>` reads an existing HTML and emits a sibling `<input>.tweaks.html` with a side panel injected before `</body>`; original input is untouched. **Why:** composability — works on Clara mockups, on Figma's HTML export, on hand-written HTML, not just on what we control. Reversible by deletion of the sibling. Cost: input must already be CSS-custom-property-driven (REQ-02 refits Clara to make this true going forward; older static-hex mockups are refused with a recommendation to re-emit). Pinned at upstream SHA `9c64ef1b2bb2cffafb0ad6167d6a3831bdc0ba11` (2026-05-07). Date: 2026-05-07.
- **D-20 — `data-od-id` attribute reused from open-design verbatim.** Clara's tweaks-ready emission stamps every major section with `<section data-od-id="<role>">` instead of inventing `data-dw-id`. **Why:** future bidirectional compatibility — open-design's critique skill could read our mockups; ours could read theirs; section anchors transfer between toolchains for free. Cost: zero (one identifier name). Risk: collision with user's own data attributes — mitigated by documentation; future `--id-attribute` flag deferred. Date: 2026-05-07.
- **D-21 — `theme-critique --mode 5dim` is a flag, not a separate skill.** The 5-dimension rubric (Philosophy / Hierarchy / Detail / Functionality / Innovation, scored 0–10 with HTML radar-chart report) ships as `--mode 5dim` inside `theme-critique`, not as a new `theme-critique-5dim` skill. **Why:** routing decision should be "is this critique?", not "is this Nielsen-style or 5dim-style?"; same persona (Júri), same input shape (a path), different rubric. Trade-off: SKILL.md grows. Mitigation: 5dim rubric content lives in `references/5dim-rubric.md` (forked from open-design under Apache-2.0); SKILL.md body just dispatches on `--mode`. Output paths split (`*-nielsen.html` vs `*-5dim.html`) so each invocation appends history under `.design-spec/critique/<feature>/`, never overwrites. Date: 2026-05-07.

### Validation runs (2026-05-07)

- `quick_validate skills/theme-port`: valid; `grep "Adapter Plan"` ≥ 2; `grep "stack:"` ≥ 1.
- `quick_validate skills/theme-extend`: valid; `grep "Adapter Plan"` ≥ 1.
- `quick_validate skills/theme-audit`: valid; `grep "stack:"` ≥ 1.
- `python3 adapters/flutter/tests/conformance.py`: PASS 3/3 (palette + widget-tree + motion-set, byte-equivalent goldens).
- `python3 adapters/nextjs-tailwind/tests/conformance.py --plain`: PASS 3/3.
- `python3 adapters/nextjs-tailwind/tests/conformance.py --shadcn`: PASS 3/3 (variant detection switches widget-tree golden; palette + motion stack-mode-invariant).
- `python3 scripts/audit_theme.py --stack flutter --help` shows `--stack`; `--stack react-native` errors with available list.
- `python3 scripts/resolve_stack.py` resolves env > config > default flutter; errors on unknown.
- All 3 example Plans validate against `docs/adapter-plan.schema.json` (zero errors).

### Deferred (Onda E → v1.3+)

- **Migrate remaining 5 wired skills** — `adapter-migration-phase-2`. theme-create / theme-motion / theme-bolder / theme-quieter / theme-distill. v1.2 dogfood feedback informs simplification.
- **Additive adapters** — React Native, Vue+Tailwind, Svelte+Tailwind, plain-React, Angular+Tailwind, SwiftUI. Each is ~1 PR.
- **Multi-stack output simultaneously** (one Plan emits both Dart and TSX). v1.4+ candidate once 2 adapters proven.
- **Adapter discovery via plugin marketplace.** v1.5+ design exercise.
- **shadcn/ui auto-install.** Adapter detects shadcn but doesn't run `npx shadcn add`. Stays user-driven.

## Conventions reminder

- Source of truth for scripts: `<repo>/scripts/<name>.py`. Edit there, then re-run `bash scripts/_sync.sh`.
- Source of truth for evals: `<repo>/skills/<skill>/evals/evals.json`. Schema follows `skill-creator/references/schemas.md`.
- Spec/design/tasks live in `.specs/features/<feature-name>/`. State (decisions, deferred) lives here.
