# design-workflow

A pipeline of Claude Code skills for designing, auditing, and refining UI in mobile apps — Flutter-first, bilingual (English/Portuguese).

> Heuristics over vibes. Tokens over hardcode. WCAG over guesses. Anti-AI-slop by default.

## What's inside

20 skills, organized as **atomic operators** (one job each) plus an **orchestration layer** that sequences them under explicit phase gates. Persona names are PT primary + EN alias — the same operator answers to both, so multilingual squads converge on the same vocabulary.

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
| `status` | Atlas / Cartographer | Read-only snapshot of active work across `.specs/`, `docs/backlog/`, `memory/active_work.md` plus current branch state. Emits TL;DR + table. |
| `promote` | Atlas Promote / Cartographer Promote | Converts a `docs/backlog/` markdown into a `.specs/features/` triplet, then recommends `/tlc-spec-driven` to refine and `/tlc-closure` to verify dependency closure. |
| `atlas-save` | Atlas Cronista / Cartographer Chronicler | Curated session handoff (decisions, bugs, lessons, sentiment, playbook) into `memory/sessions/`. Obsidian vault mirror is opt-in. |
| `opus-execute` | (Workflow helper) | `/opusexecute` packages the current Opus conversation into a self-contained brief (5 sections — Context · Files · Acceptance · Constraints · Style) and dispatches it to a Sonnet sub-agent in an isolated context window (default background), so the main Opus session never overflows Sonnet. Primary flow: `--from-task <feature>/T-<id>` reads `.specs/features/<feature>/{spec,design,tasks}.md` and synthesizes the brief from the task's structured fields. |
| `caveman` + `cavecrew` + `caveman-{commit,compress,help,review,stats}` | (Communication helpers) | Ultra-compressed communication mode — cuts ~75% of output tokens while keeping technical accuracy. `caveman` toggles caveman speech; `cavecrew` is a delegation guide for caveman-style sub-agents; `caveman-commit/review/compress` apply the same compression to commits, PR review comments, and memory files; `caveman-help/stats` are reference + telemetry. Forked from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). |

Personas don't have to be named to be invoked — every skill answers to the literal slash command (`/theme-audit`, `/theme-port`, `/compose`, `/caveman`, …). Use the persona handle when you want to be explicit about *who* you're calling on; use the slash command when you don't care.

## Optional companions

These skills are not bundled — they live in their own repos because they're useful far beyond design. Recommended when you want the full pipeline:

| Companion | Why it matters here | Repo |
|---|---|---|
| `tlc-spec-driven` | `/promote` recommends it as the next step to refine the auto-decomposed spec/design/tasks. Adaptive 4-phase planning (Specify, Design, Tasks, Execute). Stack-agnostic. | external |
| `tlc-closure` | Walks the task dependency graph after `/promote` + `/tlc-spec-driven`. Lists callers, providers, tests, routes; turns each into a closure subtask; runs auto-RalphLoop until zero loose ends. **Auto-bootstraps `tlc-spec-driven` and `graphify` if not installed.** | `fitiodevs/tlc-closure` |
| `graphify` | Knowledge-graph any input (code, docs, papers, images) into clustered communities + HTML + JSON + audit report. Used internally by `tlc-closure` to build the dependency graph. | external |
| `open-design` | **Upstream of `craft/`.** The 5 universal craft docs (`anti-ai-slop`, `color`, `state-coverage`, `typography`, `animation-discipline`) are forked verbatim from `nexu-io/open-design` (Apache-2.0). Sync is manual on demand — see `craft/README.md`. | `nexu-io/open-design` |

If `/tlc-closure` is not installed, `/promote` falls back to a "review the generated files manually" hint. None of these are hard dependencies of `design-workflow`.

## Install

```bash
git clone https://github.com/fitiodevs/design-workflow.git ~/code/design-workflow
cd ~/code/design-workflow
./install.sh
```

This copies `skills/*` into `~/.claude/skills/` so they become available in Claude Code globally.

Or, if you use the Claude Code plugin marketplace:

```
/plugin marketplace add fitiodevs/design-workflow
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

## Design schools library

`design-systems-schools/` ships **12 hand-authored design philosophy schools** — sibling to the `design-systems/` brand library. Where brands encode *identities* ("look like Apple" with literal hex), schools encode *philosophies* ("follow Müller-Brockmann's discipline" with constraints). The same school applied to two projects produces two different palettes — each respecting the project's brand constraints AND the school's principles.

| Category | Schools |
|---|---|
| Flutter-strong (Web ★★★) | `pentagram` · `information-architects` · `brutalism` · `locomotive` |
| Print-strong (PDF / Cover ★★★) | `muller-brockmann` · `kenya-hara` · `editorial` · `atelier-zero` |
| AI-gen-strong (AI-image-gen ★★★) | `memphis` · `active-theory` |
| Versatile (≥4 scenarios ★★★) | `sagmeister-walsh` · `takram` |

**Consumed by** `/theme-create --inspired-by-school <slug>` and `/frontend-design --school <slug>`. The constraint-based translator at `scripts/school_md_to_appcolors.py` reads any school's `SCHOOL.md` and synthesizes a 29-token `AppColors` proposal that satisfies the school's constraints. Each school also ships a 7-column execution-path matrix (Flutter UI / HTML / PPT / PDF / Infographic / Cover / AI-image-gen) — see `docs/design-schools-execution-paths.md` for which external tools to pair with each path.

Schools and brands compose: pick a school for *philosophy* and a brand for *tone*, or pick both from the school library when authoring non-Flutter artifacts.

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
| `react-native` | New in v1.4.1 (bare RN + Expo detection, `makeStyles(colors)` factory, RN core primitives) | `adapters/react-native/` |
| `vue-tailwind`, `svelte-tailwind`, `react-tailwind`, `angular-tailwind`, `swiftui` | v1.5+ backlog (additive, one PR each) | — |

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
- **Elicitation ledger** (`scripts/elicitation.py`): append-only JSONL of `judge_verdict` + `counterexample` events so reviewers (Júri, Lupa) persist slop evidence and generators (Clara, Arquiteto) read it before generating. Pattern from `claude-code-harness` (MIT), adapted Apache-2.0. Doc: `docs/elicitation-ledger.md`.

## Why bilingual

The skills speak both English and Portuguese (`pt-BR`). Persona names default to English archetypes (`Auditor`, `Composer`, `Critic`...) but accept Portuguese aliases (`Lupa`, `Compositor`, `Júri`...). You can invoke any skill with either form. Slash commands and copy follow your project's locale.

## Contributing

Issues and PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE.txt](LICENSE.txt). Each skill folder also carries a `LICENSE.txt` for clarity when distributed individually.

## Status

**v1.5.0** — design schools library. `design-systems-schools/` (12 hand-authored philosophy schools) ships parallel to `design-systems/` (20 brand systems). Where brands say "look like Apple" with literal hex, schools say "follow Müller-Brockmann's discipline" via constraints (saturation, single-accent, WCAG ≥7:1, polarity). The constraint-based translator at `scripts/school_md_to_appcolors.py` solves the constraints to produce different palettes for different projects under the same school. `/theme-create --inspired-by-school <slug>` and `/frontend-design --school <slug>` are the new flags. The 12 schools cover 4 scenario-strength categories — 4 Flutter-strong (Pentagram, IA, Brutalism, Locomotive), 4 Print-strong (Müller-Brockmann, Kenya Hara, Editorial, Atelier-Zero), 2 AI-gen-strong (Memphis, Active Theory), 2 Versatile (Sagmeister-Walsh, Takram). `docs/design-schools-execution-paths.md` documents the multi-target execution matrix and recommended external tools (Marp, Slidev, Pandoc, Typst, Puppeteer, Midjourney, SDXL). 20/20 skills still pass `quick_validate.py`. Built on v1.4.x (RN adapter + interactive mockup stage), v1.3.0 (inspiration library), v1.2.x (multi-stack adapter + design-context). Extracted from production use in the [Fitio](https://fitio.app) Flutter app.

## What changed in v1.5.0

- **12-entry design-school library** at `design-systems-schools/`. Each `<slug>/SCHOOL.md` is hand-authored under Apache-2.0 with 8 standard sections — Philosophy nucleus · Core characteristics · Prompt DNA · Token implications · Execution-path matrix (7 scenarios × ratings) · Slop traps · Best paired with · Anti-pairs. Idea inspired by `alchaincyf/huashu-design` (Personal Use Only — not forked); structure adapted; prose written from scratch.
- **Constraint-based translator** at `scripts/school_md_to_appcolors.py` (~485 LOC). Schools encode constraints (`accent ≤10% pixels`, `saturation_min 0.6`, `WCAG ≥7:1`, `polarity dark`, `single_accent`); the translator parses the bullets, synthesizes a palette via OKLCH iteration that satisfies the constraints, validates WCAG, and emits the same `proposal.json` + `rationale.md` shape as the v1.3.0 brand translator. **Validates 12/12 schools** with 9-10/11 WCAG pairs passing per mode.
- **`/theme-create --inspired-by-school <slug>`** routes to the school translator. Same 4-precondition reduction as `--inspired-by` (purpose / audience / invariants / coexistence; skips the 4 the school encodes).
- **`/frontend-design --school <slug>`** loads the school's `## Prompt DNA` as system-prompt extension for that mockup; appends the school's `## Slop traps` to the auto-revision checklist; stamps `<!-- school: <slug> -->` in `<head>` for traceability. Sticky session via `.design-spec/features/<feature>/active-school.txt`.
- **`docs/design-schools-execution-paths.md`** explains how to read the 7-column matrix (Flutter UI · HTML · PPT · PDF · Infographic · Cover · AI-image-gen), when to pick the in-pipeline HTML path vs an external tool, and lists recommended tools per scenario (with last-validated dates). The pattern is **HTML-as-canonical-source** — author HTML once, convert to PPT/PDF/Cover via Marp/Pandoc/Puppeteer.
- **STATE D-23 + D-24 + D-25 logged.** D-23 documents the schools/brands split (sibling folders, different abstractions); D-24 records the from-scratch authoring under Apache-2.0; D-25 captures the multi-target-matrix-as-reference-only doctrine.

## What changed in v1.4.1

- **`adapters/react-native/` (additive — no skill changes).** New stack adapter follows the same shape as `adapters/flutter/` and `adapters/nextjs-tailwind/` (`adapter.py` + `mappings.py` + `templates/` + `STACK_NOTES.md` + `tests/conformance.py` + 5 frozen goldens). Renders all 3 Plan kinds (palette, motion-set, widget-tree). Conformance: **3/3 green**.
- **`scripts/resolve_stack.py`** now lists `react-native` alongside `flutter` and `nextjs-tailwind`; `STACK=react-native python3 scripts/resolve_stack.py` exits 0.
- **`scripts/audit_theme.py`** accepts `--stack react-native`; lint set at `scripts/audit_lint_sets/react-native.yaml` (catches `"#hex"` strings outside `theme/`, inline `style={{ color: '#…' }}`, `rgba()` literals, `Color(0x…)` Android-API copy-paste).
- **Skill bodies extended** — `theme-port`, `theme-extend`, `theme-audit` add a `react-native` row to their per-stack tables. No new triggers, no behavioural change for existing flutter / nextjs-tailwind users.
- **What it does NOT ship** — the `useColors()` hook (downstream wires it to `useColorScheme()` or a store), `npx expo install` automation, image source resolution, or Reanimated worklets. See `adapters/react-native/STACK_NOTES.md` for the full non-goal list.

## What changed in v1.4.0

- **`tweaks` skill (new — 20th in the marketplace).** `/tweaks <path>` wraps any tweaks-ready HTML with a fixed side panel of 5 knobs binding to CSS custom properties + localStorage persistence. Output is a sibling `<input>.tweaks.html` (original untouched). Refuses to wrap inputs that bake hex/px outside `:root` and tells the user to re-emit via `/frontend-design`. Vanilla JS, ~250 lines, no framework, no server — single self-contained HTML. Persona: **Tweaker** (functional skill, no PT alias).
- **Clara refit: tweaks-ready emission contract.** `/frontend-design` (Clara / Designer) now ships HTML where every visual decision is a CSS custom property reference: colors via `var(--accent)`, spacing via `calc(var(--space-unit) * N)`, font-sizes via the multiplicative scale ladder, dark mode via `:root[data-mode="dark"]` overrides, every major section gets `data-od-id`. The auto-revisão checklist gains 5 boolean items. Mockups produced from v1.4 forward pipe directly into `/tweaks` without refit.
- **`theme-critique --mode 5dim`.** Alternative rubric forked from `nexu-io/open-design` (originating in `huashu-design`) — 5 dimensions scored 0–10 (Philosophy / Visual hierarchy / Detail / Functionality / Innovation), each with evidence + a Keep/Fix/Quick-win bullet. Output is a self-contained HTML report at `.design-spec/critique/<feature>/<timestamp>-5dim.html` with inline-SVG radar chart. Default mode stays Nielsen 10. Use 5dim for early-stage exploration; Nielsen for shipping-readiness.
- **Pipeline (new step between Clara and Architect):**

  ```
  /theme-create [--inspired-by]          # palette
       ↓
  /frontend-design                       # tweaks-ready HTML mockup
       ↓
  /tweaks <path>                         # NEW v1.4 — knob panel, explore N variants
       ↓
  /theme-critique --mode 5dim <path>     # NEW v1.4 — radar-chart review of chosen state
       ↓
  /theme-port --from-html <path>         # HTML → Flutter using tokens
  ```

- **STATE D-19 + D-20 + D-21 logged.** D-19 records tweaks-as-wrapper-not-generator; D-20 records `data-od-id` reuse over inventing `data-dw-id`; D-21 records `--mode 5dim` as a flag rather than a separate skill.

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

- **Onda D — _(removed in v1.5.3)_** the autonomous `ralph-loop` skill and its scripts were dropped because we weren't using them in practice. History remains in git.

`.design-spec/` is the runtime state directory (features per-phase, project-level decisions, audit logs, halt switch). `.specs/` continues to hold human-written planning artifacts (spec/design/tasks per feature). See `docs/design-spec-driven-plan.md` for the full plan and `.specs/project/STATE.md` for locked decisions and validation runs.

## What changed in v0.2

- **Spec-compliant frontmatter.** Removed non-standard `license:` and `triggers:` keys from all 13 SKILL.md files. Frontmatter now carries only `name` and `description` (and optionally `compatibility`), matching the official `skill-creator` schema.
- **English persona triggers actually exist.** Added a `## Triggers` section in every SKILL.md body listing English aliases (`/Auditor`, `/Composer`, `/Critic`, `/Amplifier`, `/Refiner`, `/Distiller`, `/Choreographer`, `/Designer`, `/Writer`, `/Surgeon`, `/Architect`, `/Orchestrator`) plus Portuguese aliases plus natural-language phrases. Description fields mention at least one EN trigger so the harness can dispatch via `/Auditor` etc.
- **Brand-agnostic descriptions.** Replaced every literal `Fitio` mention in the 13 skill descriptions/bodies with generic phrasing ("a Flutter app", "the project", "your design system") so the skills work in any Flutter project. Tone, examples and pushiness preserved — only marca removed.
- **Progressive disclosure.** Extracted dense reference material from 6 long skills into `<skill>/references/<topic>.md` (10 files total — `oklch-recipes`, `slop-patterns`, `text-hierarchy`, `widget-mapping`, `motion-tokens`, `flutter-animate-snippets`, `quality-standards`, `before-after-patterns`, `clara-checklist`, `nielsen-rubric`). SKILL.md bodies are tighter; the model loads the references only when needed.
- **Scripts bundled per skill.** Added `scripts/_sync.sh` that copies the canonical scripts in `<repo>/scripts/` into each consuming skill's own `scripts/` subdir. After install, `theme-audit/`, `theme-extend/`, `theme-create/` each carry the Python scripts they need (no more orphaned scripts at install time).
- **Minimal evals.** Added `evals.json` (3 prompts × 4–6 assertions) to the 4 skills with objectively verifiable output: `theme-audit`, `theme-extend`, `theme-port`, `theme-create`. Nine subjective skills (critique/refine/motion/writing/sandbox/prompt) ship without evals — see `.specs/project/STATE.md` for the deferred follow-up.
