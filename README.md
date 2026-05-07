# design-workflow

A pipeline of Claude Code skills for designing, auditing, and refining UI in mobile apps — Flutter-first, bilingual (English/Portuguese).

> Heuristics over vibes. Tokens over hardcode. WCAG over guesses. Anti-AI-slop by default.

## What's inside

19 skills, organized as **atomic operators** (one job each) plus an **orchestration layer** that sequences them under explicit phase gates. Persona names are PT primary + EN alias — the same operator answers to both, so multilingual squads converge on the same vocabulary.

### Skill / persona / what it does

| Skill | Persona (PT / EN) | What it does |
|---|---|---|
| `theme-audit` | Lupa / Auditor | Sweeps `lib/` for hardcoded colors, fonts, off-scale spacing; validates WCAG; measures coverage. Also triages screenshots. |
| `theme-extend` | Cirurgião / Surgeon | Adds or tweaks a semantic token (color, typography, spacing, radius). Generates light/dark pairs validated against WCAG. |
| `theme-port` | Arquiteto / Architect | Ports a structural source (Figma frame OR HTML mockup from any tool — `/frontend-design`, Figma's HTML export, Stitch, Penpot, hand-written) into Flutter widgets using your existing tokens. Source provides structure; theme provides identity. |
| `theme-create` | Compositor / Composer | Builds a complete palette from scratch (brand + semantic + neutral) in OKLCH with anti-AI-slop checklist + WCAG. |
| `theme-critique` | Júri / Critic | Nielsen 0–4 × 10 heuristics, AI-slop verdict, persona walkthrough, cognitive load, P0–P3 issue map. Also drives Discovery (no args). |
| `theme-bolder` | Brasa / Amplifier | Amplifies a bland/timid screen — raises color commitment, breaks reflexive symmetry, intensifies hierarchy. |
| `theme-quieter` | Calma / Refiner | Calms an aggressive screen — lowers commitment, desaturates accents, drops typographic weight. |
| `theme-distill` | Lâmina / Distiller | Cuts decisions to ≤4. Forces progressive disclosure. Removes anything that doesn't earn its pixel. |
| `theme-motion` | Jack / Choreographer | Adds or tunes motion using motion tokens + `flutter_animate`. Refuses motion-for-motion. |
| `frontend-design` | Clara / Designer | Generates production-grade HTML/CSS/JS mockups consumed directly by `/theme-port --from-html` for conversion to Flutter widgets. |
| `ux-writing` | Pena / Writer | UX writing critique + rewrite of labels, CTAs, errors, empty states, success messages. Delivers before/after with copy-paste strings. |
| `compose` | (Compose phase) | Reads approved discovery, sequences `/theme-create` + `/frontend-design` under a phase gate, has Clara review. Output: `compose.md`. |
| `sequence` | Arquiteto / Architect (Sequence phase) | Reads approved compose, emits `tasks.md` with atomic ≤30-min tasks, each with a binary `verify:` block. |
| `ship` | (Ship phase) | Executes tasks one by one — spawn skill, run verify, commit on pass with `Refs feature/T-id`, halt cleanly on fail. Closes with audit + critique re-run. |
| `productivity` | (Productivity helpers) | `/design-spec pause` (checkpoint), `/resume` (sumariza, sugere re-discovery se >14d), `/status`, `/approve <phase> <feature>`. |
| `ralph-loop` | Ralph (autonomy layer) | 3 tiers: **Watch** (read-only audit + critique), **Mechanical** (deterministic fixes, opens PR draft, never auto-merge), **Composer** (executes approved sequence with halt + budget cap). |
| `status` | Atlas / Cartographer | Read-only snapshot of active work across `.specs/`, `docs/backlog/`, `memory/active_work.md` plus current branch state. Emits TL;DR + table. |
| `promote` | Atlas Promote / Cartographer Promote | Converts a `docs/backlog/` markdown into a `.specs/features/` triplet, then recommends `/tlc-spec-driven` to refine and `/tlc-closure` to verify dependency closure. |
| `atlas-save` | Atlas Cronista / Cartographer Chronicler | Curated session handoff (decisions, bugs, lessons, sentiment, playbook) into `memory/sessions/`. Obsidian vault mirror is opt-in. |

Personas don't have to be named to be invoked — every skill answers to the literal slash command (`/theme-audit`, `/theme-port`, `/compose`, `/ralph`, …). Use the persona handle when you want to be explicit about *who* you're calling on; use the slash command when you don't care.

## Optional companions

These skills are not bundled — they live in their own repos because they're useful far beyond design. Recommended when you want the full pipeline:

| Companion | Why it matters here | Repo |
|---|---|---|
| `tlc-spec-driven` | `/promote` recommends it as the next step to refine the auto-decomposed spec/design/tasks. Adaptive 4-phase planning (Specify, Design, Tasks, Execute). Stack-agnostic. | external |
| `tlc-closure` | Walks the task dependency graph after `/promote` + `/tlc-spec-driven`. Lists callers, providers, tests, routes; turns each into a closure subtask; runs auto-RalphLoop until zero loose ends. **Auto-bootstraps `tlc-spec-driven` and `graphify` if not installed.** | `fitiodevs/tlc-closure` |
| `graphify` | Knowledge-graph any input (code, docs, papers, images) into clustered communities + HTML + JSON + audit report. Used internally by `tlc-closure` to build the dependency graph. | external |
| `caveman` | Ultra-compressed communication mode (~75% fewer tokens) when you need to ship a long autonomous loop on a budget. | external |
| `open-design` | **Upstream of `craft/`.** The 5 universal craft docs (`anti-ai-slop`, `color`, `state-coverage`, `typography`, `animation-discipline`) are forked verbatim from `nexu-io/open-design` (Apache-2.0). Sync is manual on demand — see `craft/README.md`. | `nexu-io/open-design` |

If `/tlc-closure` is not installed, `/promote` falls back to a "review the generated files manually" hint. None of these are hard dependencies of `design-workflow`.

## Install

```bash
git clone https://github.com/<your-handle>/design-workflow.git ~/code/design-workflow
cd ~/code/design-workflow
./install.sh
```

This copies `skills/*` into `~/.claude/skills/` so they become available in Claude Code globally.

Or, if you use the Claude Code plugin marketplace:

```
/plugin marketplace add <your-handle>/design-workflow
/plugin install design-workflow@design-workflow-marketplace
```

## Quickstart

In any Flutter project (Material 3 + Riverpod recommended):

```
/theme-audit          # baseline
/theme-create         # if you don't have a palette yet
/theme-port <figma>   # turn a frame into widgets
/theme-critique       # is the screen good?
/theme-bolder         # if it's timid
/theme-quieter        # if it's shouty
/theme-distill        # if it's overloaded
/theme-motion         # if it's flat
```

Each skill has a persona triggerable directly: `/Auditor`, `/Composer`, `/Critic`, `/Amplifier`, `/Refiner`, `/Distiller`, `/Choreographer`, `/Designer`, `/Writer`, `/Surgeon`, `/Architect`, `/Cartographer`. Portuguese aliases also work: `/Lupa`, `/Compositor`, `/Júri`, `/Brasa`, `/Calma`, `/Lâmina`, `/Jack`, `/Clara`, `/Pena`, `/Cirurgião`, `/Arquiteto`, `/Atlas`. See [docs/personas.md](docs/personas.md).

## Stack assumptions

These skills emit code through **stack adapters**. v1.2.0 ships two reference adapters:

- **flutter** (default) — Material 3 + Riverpod; tokens at `lib/core/theme/`; widgets at `lib/features/<feature>/presentation/widgets/`.
- **nextjs-tailwind** — App Router or Pages; tokens as CSS custom properties in `app/globals.css` (or `styles/tokens.css`); Tailwind config snippet for `theme.extend.colors`; shadcn/ui detected via `components.json` or `@radix-ui/*` deps; widgets at `components/<feature>/<name>.tsx`.

Project doc at `docs/product.md` is shared (used for persona + AI-slop checks across stacks).

You can override paths in `config.example.yaml` → copy to your project as `.design-workflow.yaml`. Set `stack: flutter` or `stack: nextjs-tailwind` to select the adapter (default: `flutter`). Override per-invocation with the `STACK` env var. See [docs/customizing.md](docs/customizing.md) and [docs/adapter-protocol.md](docs/adapter-protocol.md).

A subset of skills (`theme-critique`, `theme-create`, `frontend-design`, `ux-writing`) is **stack-agnostic** and works on any codebase that uses tokens.

## Inspiration library

`design-systems/` ships a 20-entry curated subset of [`nexu-io/open-design`](https://github.com/nexu-io/open-design)'s 71 brand `DESIGN.md` references. Each entry is a complete 9-section spec (Visual Theme · Color Palette · Typography · Components · Layout · Depth · Do/Don't · Responsive · Agent Prompt) with full upstream attribution headers (Apache-2.0 / MIT lineage). Pinned at SHA `d4b547c` (2026-05-07).

| Category | Slugs |
|---|---|
| AI & LLM | `claude` · `cohere` · `mistral-ai` |
| Developer Tools | `raycast` · `vercel` |
| Productivity & SaaS | `cal` · `linear-app` · `notion` |
| Backend & Data | `sentry` · `supabase` |
| Design & Creative | `figma` · `framer` |
| Fintech & Crypto | `revolut` · `stripe` |
| E-Commerce & Retail | `airbnb` · `nike` |
| Media & Consumer | `apple` · `spotify` |
| Automotive | `tesla` |
| Editorial · Studio | `atelier-zero` |

**Consumed by** `/theme-create --inspired-by <slug>` and `/theme-create --browse [<category>]` via the translator at `scripts/design_md_to_appcolors.py`. The translator emits a `proposal.json` (29 tokens × 2 modes + WCAG report) plus a human-readable `rationale.md` for any of the 20 sources. See `design-systems/README.md` for the file contract and re-sync instructions.

## Stack support

| Stack | Status | Adapter |
|---|---|---|
| `flutter` | Stable since v1.0 | `adapters/flutter/` |
| `nextjs-tailwind` | New in v1.2.0 (App Router + Pages, shadcn/ui aware) | `adapters/nextjs-tailwind/` |
| `react-native`, `vue-tailwind`, `svelte-tailwind`, `react-tailwind`, `angular-tailwind`, `swiftui` | v1.3+ backlog (additive, one PR each) | — |

Each adapter ships:
- `adapter.py` (entry point, dispatches by Plan `kind`)
- `mappings.py` (29-role TOKEN_ROLE_MAP + widget type map)
- `templates/` (string templates per output type)
- `STACK_NOTES.md` (path conventions + override hints)
- `tests/conformance.py` + golden files (CI gate)

To add a new stack, see `docs/adapter-protocol.md` §"How to add a new adapter".

## Methodology

- **OKLCH** for perceptually uniform palette generation (`scripts/oklch_to_hex.py`, `scripts/generate_palette.py`)
- **WCAG 2.1** AA/AAA contrast validation (`scripts/check_contrast.py`)
- **Nielsen 10 heuristics** scored 0–4 in `theme-critique`
- **Anti-AI-slop** verdict: detects 7 archetypal patterns (`scripts/audit_theme.py` slop_patterns)
- **Cognitive load**: counts decisions per viewport, flags >4
- **Persona walkthrough**: walks 3 user personas through the screen (configure yours in `docs/personas.md`)

## Why bilingual

The skills speak both English and Portuguese (`pt-BR`). Persona names default to English archetypes (`Auditor`, `Composer`, `Critic`...) but accept Portuguese aliases (`Lupa`, `Compositor`, `Júri`...). You can invoke any skill with either form. Slash commands and copy follow your project's locale.

## Contributing

Issues and PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE.txt](LICENSE.txt). Each skill folder also carries a `LICENSE.txt` for clarity when distributed individually.

## Status

**v1.3.0** — inspiration library: a curated 20-entry subset of [`nexu-io/open-design`](https://github.com/nexu-io/open-design)'s 71 brand `DESIGN.md` references lives at `design-systems/`, plus a translator at `scripts/design_md_to_appcolors.py` that maps any source's CSS-style palette onto the Fitio 29-token `AppColors`. `/theme-create` gains two flags — `--inspired-by <slug>` (skip 4 of 8 pre-conditions, source already encodes them) and `--browse [<category>]` (discover before picking). 19/19 skills still pass `quick_validate.py`. Built on v1.2.1 (design-context doctrine) and v1.2.0 (multi-stack adapter). Extracted from production use in the [Fitio](https://fitio.app) Flutter app.

## What changed in v1.3.0

- **20-entry curated inspiration library.** `design-systems/<slug>/DESIGN.md` ships forks of 20 reference brand systems from upstream `nexu-io/open-design` — covering AI&LLM (Claude, Cohere, Mistral), Dev Tools (Vercel, Raycast), Productivity (Linear, Notion, Cal), Backend/Data (Supabase, Sentry), Design/Creative (Figma, Framer), Fintech (Stripe, Revolut), E-Commerce (Airbnb, Nike), Media (Apple, Spotify), Automotive (Tesla), and Editorial (Atelier Zero). Each entry retains its full attribution chain (Apache-2.0 / MIT lineage) and is pinned at upstream SHA `d4b547c`.
- **Translator: DESIGN.md → AppColors.** `scripts/design_md_to_appcolors.py` reads any of the 20 sources and emits a `proposal.json` (29 tokens × 2 modes + WCAG report + decision trace) plus a human-readable `rationale.md` (source citation + mapping table + open questions + Fitio-specific tokens needing input). Inference chain: per-entry name override → section keyword → description hint → WCAG-corrected fallback. Native-mode detection (light vs dark) drives whether the source IS the dark proposal (Linear, Apple, Sentry) or the light one. Industry-standard defaults fill missing feedback colors and are flagged.
- **`/theme-create --inspired-by <slug>`.** New flag skips 4 of the original 8 pre-conditions (tone, differentiation, color-strategy commitment, anti-category-reflex — the source already encodes them). User answers only purpose, audience, invariants, coexistence. The translator's rationale doc drives the conversation.
- **`/theme-create --browse [<category>]`.** Discovery wrapper — lists the 20 entries grouped by category, lets the user pick, then drops into `--inspired-by`. With a category arg (`--browse fintech`), filters to that bucket.
- **STATE D-17 + D-18 logged.** D-17 documents the curation cap and attribution chain; D-18 captures the translator's inference chain priority and the always-flag-failures rule.

## What changed in v1.2.1

- **Design context doctrine.** New `craft/design-context.md` codifies the "blank-page is last resort" rule with a 5-tier context hierarchy (existing design system → codebase → deployed product → external brief → vague description) and a sharp refusal rule: STOP if Tier 1–4 absent. Authored from scratch under Apache-2.0; idea inspired by [huashu-design](https://github.com/alchaincyf/huashu-design).
- **5 wired skills, 1 net-new wire.** `theme-port`, `theme-create`, `theme-critique`, `frontend-design` get `design-context` appended to existing `dw.craft.requires:`. `theme-extend` becomes wired for the first time (Tier 1 dependency only — extending nothing is meaningless). `theme-port`, `theme-create`, `theme-extend` gain a "Pre-flight context check" section with skill-specific tier checks before Workflow Step 1.
- **STATE D-11.1 logged.** Sub-decision under D-11 (craft adoption) records the from-scratch authoring + 5-skill wiring.

## What changed in v1.2.0

- **Adapter contract.** New `docs/adapter-protocol.md` + `docs/adapter-plan.schema.json` define a stack-neutral intermediate format ("Adapter Plan"). Skills that emit code now produce a Plan; per-stack adapters render it to native syntax.
- **Two reference adapters.** `adapters/flutter/` is byte-equivalent to pre-v1.2 output (Fitio dogfood path unchanged). `adapters/nextjs-tailwind/` is new — emits CSS custom properties, Tailwind config snippet, and TSX (shadcn-aware when detected).
- **`stack:` config field.** Top-level `stack: flutter | nextjs-tailwind` in `.design-workflow.yaml`. Override per-invocation with `STACK` env var. Default `flutter` keeps existing setups working.
- **Migrated skills.** `theme-port` and `theme-extend` emit Plans and dispatch to the active adapter. Remaining 5 wired skills (`theme-create`, `theme-motion`, `theme-bolder`, `theme-quieter`, `theme-distill`) are deferred to v1.3 phase-2.
- **Stack-aware audit.** `theme-audit` reads `scripts/audit_lint_sets/<stack>.yaml` for regex sets; Tailwind arbitrary-hex patterns + inline-style hex etc. activate when `stack: nextjs-tailwind`. WCAG contrast logic is shared.
- **ROADMAP reversed.** "Web-first design out of scope" entry struck through; adapter pattern keeps all stacks in-repo.

## What changed in v1.1.2

- **`install.sh` bundles `craft/` and rewrites refs.** Copies `craft/*.md` → `~/.claude/craft/` then `sed`-rewrites `` `craft/<doc>.md` `` → `` `~/.claude/craft/<doc>.md` `` in the 5 wired SKILL.md copies post-install. Source SKILL.md stays project-relative so users who clone the repo and work inside it still see clean references.
- **STATE.md D-13 logged.** Deployment bug + fix documented in `.specs/project/STATE.md`.

## What changed in v1.1.1

- **`craft/` adoption.** 5 docs (`anti-ai-slop`, `color`, `state-coverage`, `typography`, `animation-discipline`) forked verbatim from upstream `nexu-io/open-design` at SHA `26636384a8dc3e9b36029c3b6299d4a2005d255a` with full attribution chain in each header. Sync is manual on demand.
- **`metadata.dw.craft.requires:` field wired in 5 skills.** Validator probe (T-07) ruled out top-level `dw:` and chose nesting under the officially-allowed `metadata:` key. See `docs/skill-extensions.md` for the namespace spec.
- **Per-skill "Craft references" body section.** Each wired skill carries a prose section listing only the docs it declared, near the top of the body so the model loads them before generating output. Project tokens (`AppColors`, `docs/product.md`) still override when they explicitly contradict.
- **STATE.md D-11 + D-12 logged.** Adoption decision and namespace decision documented in `.specs/project/STATE.md`.

## What changed in v1.1.0

- **Atlas trio promoted to public.** `status` (read-only project state inspector), `promote` (backlog → `.specs/features/` triplet, recommends `/tlc-spec-driven` + `/tlc-closure`), and `atlas-save` (curated session handoff with opt-in Obsidian mirror). Persona Atlas / Cartographer.
- **`theme-port` HTML mode generalized.** The flag `--from-stitch` was renamed `--from-html` and any tool-specific assumptions were stripped (no Atelier cache paths, no required `.png` sibling). Same regex-based parser works for any HTML mockup — `/frontend-design`, Figma's HTML export, Stitch, Penpot, hand-written. The two Stitch-only orchestration skills (`theme-prompt`, `theme-sandbox`) were removed because their value was tool-specific and the rest of the pipeline didn't depend on them.
- **Optional companions documented.** `tlc-spec-driven`, `tlc-closure`, `graphify`, `caveman` are not bundled — they live in their own repos. The README now declares which composes well with what, and `promote` falls back gracefully when `tlc-closure` is not installed.

## What changed in v1.0.1

- **Brand sweep, scripts edition.** The v0.2 brand pass cleaned every SKILL.md and reference file but left "Fitio" mentions in 7 script header comments (`audit_theme.py`, `check_contrast.py`, `generate_palette.py`) and in one example prompt (`theme-create/evals/evals.json` — "Fitio Arena"). v1.0.1 finishes the job: scripts read as project-agnostic, examples use `<app>` placeholders. Provenance lines stay (README "extracted from Fitio", marketplace.json author "Fitio") because attribution ≠ coupling.
- **Personas as a PT+EN pair, globally.** The 13 atomic operators already shipped both names in their SKILL.md descriptions (`Triggered by /Auditor, /Lupa, ...`). The pair is now wired into Claude Code's user-level `CLAUDE.md` persona table so squads multilíngues invoke the same operator with whichever name they learned first. See `.specs/project/STATE.md` D-07.
- **Validation, full sweep.** `quick_validate.py` ran across all **18 skills** (13 originals + 5 layer skills from v1.0): zero errors, zero warnings. STATE.md §Validation runs has the 2026-05-05 entry.

## What changed in v1.0

The 13 atomic skills become **operators**. A new orchestration layer wraps them with phase gates, decisions tracking, and an autonomous execution loop. Four ondas (waves) shipped:

- **Onda A — Discovery foundation.** Júri (`theme-critique`) gains a Discovery mode dispatched by `/juri` (no args). Auto-sizes greenfield vs brownfield via `scripts/detect_mode.py`, runs `/theme-audit` silently in brownfield to bring real numbers to the interview, conducts a 4-block structured interview (Produto / Tom / Identidade / Stack — 1 block per turn, refuses vague answers with 2-retry cap), generates `.design-spec/features/<feature>/discovery.md` plus tier-appropriate skeletons in `docs/`, and emits a priority-ordered routing plan into the next skill — never auto-runs. `/juri --resume <feature>`, `/juri specify <feature>`, `/juri discuss <topic>` (Socratic, stateless), `/juri --mode <tier>` flags supported. Critique mode preserved byte-perfect.

- **Onda B — Spec-driven workflow.** Three new wrapper skills with hard phase gates: `compose` (reads approved discovery → `/theme-create` + `/frontend-design` + Clara review → `compose.md`), `sequence` (Arquiteto persona — atomic ≤30min tasks each with binary `verify:` blocks), `ship` (executes tasks one by one, 1 commit per task with `Refs: <feature>/<task-id>` footer, halts cleanly on verify fail, finalizes with `/theme-audit` + `/theme-critique` re-run). `decisions.md` schema with supersedes-based audit trail prevents refining skills from contradicting prior locked decisions.

- **Onda C — Productivity layer.** `productivity` skill bundling `/design-spec pause`, `/design-spec resume` (suggests light re-discovery after 14 days), `/design-spec status` (calls `scripts/design_state.py` — JSON or prose, `<2s`), and `/design-spec approve <phase> <feature>` (validates schema before flipping `draft → approved`). Júri's discuss mode upgraded from placeholder to real Socratic informal mode.

- **Onda D — Ralph autonomy.** New `ralph-loop` skill with 3 tiers: **Watch** (read-only audit + critique, emits issue payload), **Mechanical** (deterministic regex-replaceable fixes, opens PR draft, never merges), **Composer** (executes approved `tasks.md`, halts on 2× verify fail / `requires_human` / branch protection / halt file / budget). Hard rules: never auto-merge any tier; `.design-spec/halt` checked first each tick; `budget.yaml` is human-set; persona injection per tick (re-loads `voice_dna` from SKILL.md); cycle detection within 3-tick window. Ships JSONL append-only audit log per feature/day, `scripts/ralph_tick.py` (skeleton) + `scripts/ralph_budget.py` (cost dashboard, DuckDB-friendly), and 3 GitHub Actions workflow templates (`design-watch.yml` daily, `design-pre-merge.yml` on PR, `design-sprint.yml` weekly Tier 2 sweep).

`.design-spec/` is the runtime state directory (features per-phase, project-level decisions, audit logs, halt switch). `.specs/` continues to hold human-written planning artifacts (spec/design/tasks per feature). See `docs/design-spec-driven-plan.md` for the full plan and `.specs/project/STATE.md` for locked decisions and validation runs.

## What changed in v0.2

- **Spec-compliant frontmatter.** Removed non-standard `license:` and `triggers:` keys from all 13 SKILL.md files. Frontmatter now carries only `name` and `description` (and optionally `compatibility`), matching the official `skill-creator` schema.
- **English persona triggers actually exist.** Added a `## Triggers` section in every SKILL.md body listing English aliases (`/Auditor`, `/Composer`, `/Critic`, `/Amplifier`, `/Refiner`, `/Distiller`, `/Choreographer`, `/Designer`, `/Writer`, `/Surgeon`, `/Architect`, `/Orchestrator`) plus Portuguese aliases plus natural-language phrases. Description fields mention at least one EN trigger so the harness can dispatch via `/Auditor` etc.
- **Brand-agnostic descriptions.** Replaced every literal `Fitio` mention in the 13 skill descriptions/bodies with generic phrasing ("a Flutter app", "the project", "your design system") so the skills work in any Flutter project. Tone, examples and pushiness preserved — only marca removed.
- **Progressive disclosure.** Extracted dense reference material from 6 long skills into `<skill>/references/<topic>.md` (10 files total — `oklch-recipes`, `slop-patterns`, `text-hierarchy`, `widget-mapping`, `motion-tokens`, `flutter-animate-snippets`, `quality-standards`, `before-after-patterns`, `clara-checklist`, `nielsen-rubric`). SKILL.md bodies are tighter; the model loads the references only when needed.
- **Scripts bundled per skill.** Added `scripts/_sync.sh` that copies the canonical scripts in `<repo>/scripts/` into each consuming skill's own `scripts/` subdir. After install, `theme-audit/`, `theme-extend/`, `theme-create/` each carry the Python scripts they need (no more orphaned scripts at install time).
- **Minimal evals.** Added `evals.json` (3 prompts × 4–6 assertions) to the 4 skills with objectively verifiable output: `theme-audit`, `theme-extend`, `theme-port`, `theme-create`. Nine subjective skills (critique/refine/motion/writing/sandbox/prompt) ship without evals — see `.specs/project/STATE.md` for the deferred follow-up.
