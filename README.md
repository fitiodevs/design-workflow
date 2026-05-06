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

These skills are **Flutter-first**:
- Material 3 + Riverpod
- Tokens at `lib/core/theme/{app_colors,app_spacing,app_motion,app_curves}.dart`
- Project doc at `docs/product.md` (used for persona + AI-slop checks)

You can override paths in `config.example.yaml` → copy to your project as `.design-workflow.yaml`. See [docs/customizing.md](docs/customizing.md).

A subset of skills (`theme-audit`, `theme-critique`, `theme-create`, `frontend-design`, `ux-writing`) is **stack-agnostic** and works on any codebase that uses tokens.

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

**v1.1.0** — minor release: 19 skills total. Atlas trio promoted to public (`status`, `promote`, `atlas-save`) with Fitio-specific paths generalized. Stitch-specific naming retired from `theme-port` — the HTML pathway is preserved and now generic: `--from-stitch` became `--from-html`, accepting any HTML mockup (`/frontend-design`, Figma's HTML export, Penpot, Stitch, hand-written). The two Stitch-only skills (`theme-prompt`, `theme-sandbox`) were removed as their orchestration was tool-specific. 19/19 skills validated by `quick_validate.py`. Extracted from production use in the [Fitio](https://fitio.app) Flutter app. Stack-agnostic adapter is the next-major roadmap item (Onda E).

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
