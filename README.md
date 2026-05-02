# design-workflow

A pipeline of Claude Code skills for designing, auditing, and refining UI in mobile apps — Flutter-first, bilingual (English/Portuguese).

> Heuristics over vibes. Tokens over hardcode. WCAG over guesses. Anti-AI-slop by default.

## What's inside

13 skills that compose into a full design workflow:

### Theme manager (build & maintain a design system)
- **theme-create** — palette from scratch (OKLCH-uniform, anti-AI-slop, WCAG-validated)
- **theme-extend** — add or fix a single semantic token (light/dark pair, contrast-validated)
- **theme-audit** — sweep your codebase for hardcoded colors, typography, spacing; validate WCAG
- **theme-port** — port a Figma frame (or HTML mockup) into Flutter widgets using your tokens
- **theme-prompt** — compose a structured Stitch prompt (Content + Style + Layout) from a critique handoff
- **theme-sandbox** — orchestrate Stitch MCP variations end-to-end (critique → prompt → N variants → port)

### Critique & refine
- **theme-critique** — Nielsen 10 + AI-slop verdict + persona walkthrough + cognitive load count
- **theme-bolder** — amplify a timid screen (Restrained → Committed/Drenched, break symmetry)
- **theme-quieter** — calm a shouty screen (Drenched → Restrained, desaturate, remove cards)
- **theme-distill** — cut decisions to ≤4 (`/lamina`) — remove anything that doesn't earn its pixel
- **theme-motion** — add or tune motion using motion tokens + flutter_animate; refuses motion-for-motion's-sake

### Companion craft
- **frontend-design** — generate distinctive HTML/CSS mockups (anti-AI-slop) that feed `theme-port --from-stitch`
- **ux-writing** — UX writing critique + rewrite for labels, CTAs, empty states, errors

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

Each skill has a persona triggerable directly: `/Auditor`, `/Composer`, `/Critic`, `/Amplifier`, `/Refiner`, `/Distiller`, `/Choreographer`, `/Designer`, `/Writer`. Portuguese aliases also work: `/Lupa`, `/Compositor`, `/Júri`, `/Brasa`, `/Calma`, `/Lâmina`, `/Jack`, `/Clara`, `/Pena`. See [docs/personas.md](docs/personas.md).

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

v0.2.0 — extracted from production use in the [Fitio](https://fitio.app) Flutter app. Stack-agnosticism and additional examples are roadmap items.

## What changed in v0.2

- **Spec-compliant frontmatter.** Removed non-standard `license:` and `triggers:` keys from all 13 SKILL.md files. Frontmatter now carries only `name` and `description` (and optionally `compatibility`), matching the official `skill-creator` schema.
- **English persona triggers actually exist.** Added a `## Triggers` section in every SKILL.md body listing English aliases (`/Auditor`, `/Composer`, `/Critic`, `/Amplifier`, `/Refiner`, `/Distiller`, `/Choreographer`, `/Designer`, `/Writer`, `/Surgeon`, `/Architect`, `/Orchestrator`) plus Portuguese aliases plus natural-language phrases. Description fields mention at least one EN trigger so the harness can dispatch via `/Auditor` etc.
- **Brand-agnostic descriptions.** Replaced every literal `Fitio` mention in the 13 skill descriptions/bodies with generic phrasing ("a Flutter app", "the project", "your design system") so the skills work in any Flutter project. Tone, examples and pushiness preserved — only marca removed.
- **Progressive disclosure.** Extracted dense reference material from 6 long skills into `<skill>/references/<topic>.md` (10 files total — `oklch-recipes`, `slop-patterns`, `text-hierarchy`, `widget-mapping`, `motion-tokens`, `flutter-animate-snippets`, `quality-standards`, `before-after-patterns`, `clara-checklist`, `nielsen-rubric`). SKILL.md bodies are tighter; the model loads the references only when needed.
- **Scripts bundled per skill.** Added `scripts/_sync.sh` that copies the canonical scripts in `<repo>/scripts/` into each consuming skill's own `scripts/` subdir. After install, `theme-audit/`, `theme-extend/`, `theme-create/` each carry the Python scripts they need (no more orphaned scripts at install time).
- **Minimal evals.** Added `evals.json` (3 prompts × 4–6 assertions) to the 4 skills with objectively verifiable output: `theme-audit`, `theme-extend`, `theme-port`, `theme-create`. Nine subjective skills (critique/refine/motion/writing/sandbox/prompt) ship without evals — see `.specs/project/STATE.md` for the deferred follow-up.
