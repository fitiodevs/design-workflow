# Personas — bilingual map

Each skill has a persona archetype. Personas accept English **and** Portuguese aliases — pick whichever feels natural at invocation.

| Skill | English archetype | Portuguese alias | Role | Triggers |
|---|---|---|---|---|
| `theme-audit` | Auditor | Lupa | Sweeps codebase for hardcoded tokens; validates WCAG | `/Auditor`, `/Lupa`, `/lupa` |
| `theme-create` | Composer | Compositor | Builds palette from scratch (OKLCH-uniform, anti-AI-slop) | `/Composer`, `/Compositor`, `/compositor` |
| `theme-extend` | Surgeon | Cirurgião | Adds or fixes a single token with WCAG-validated light/dark pair | `/Surgeon`, `/Cirurgião`, `/cirurgiao` |
| `theme-port` | Architect | Arquiteto | Ports a Figma frame (or HTML) into widgets using your tokens | `/Architect`, `/Arquiteto`, `/arquiteto` |
| `theme-prompt` | (no persona — sub-skill) | — | Composes Stitch prompt from a critique handoff | `/theme-prompt` |
| `theme-sandbox` | Conductor | Orquestrador | Orchestrates Stitch MCP variations end-to-end | `/Conductor`, `/Orquestrador`, `/orquestrador` |
| `theme-critique` | Critic | Júri | Nielsen 10 + AI-slop verdict + persona walkthrough | `/Critic`, `/Júri`, `/Juri`, `/juri` |
| `theme-bolder` | Amplifier | Brasa | Amplifies a timid screen | `/Amplifier`, `/Brasa`, `/brasa` |
| `theme-quieter` | Refiner | Calma | Calms a shouty screen | `/Refiner`, `/Calma`, `/calma` |
| `theme-distill` | Distiller | Lâmina | Cuts decisions to ≤ 4 | `/Distiller`, `/Lâmina`, `/Lamina`, `/lamina` |
| `theme-motion` | Choreographer | Jack | Adds/tunes motion using motion tokens; refuses motion-for-motion | `/Choreographer`, `/Jack`, `/jack` |
| `frontend-design` | Designer | Clara | Generates HTML/CSS mockups (anti-AI-slop) for `theme-port --from-stitch` | `/Designer`, `/Clara`, `/clara` |
| `ux-writing` | Writer | Pena | UX writing critique + rewrite of labels, CTAs, errors, empty states | `/Writer`, `/Pena`, `/pena`, `/ux-write` |

## Why personas?

Each persona has:
- A **focus** — narrow enough to refuse out-of-scope work and delegate to a sibling persona.
- A **voice** — opinionated. Auditor is mechanical (counts violations). Critic is cutting (no participation trophies). Amplifier is bold (refuses safe). Refiner is calm (resists shouty). Distiller is ruthless (cuts everything that doesn't earn its pixel).
- A **handoff contract** — output structured so the next skill in the pipeline can pick up without re-asking the user.

## Adding new personas

If you ship a skill that introduces a new persona, please:
1. Add an English archetype (the canonical name).
2. Add at least one Portuguese alias (lowercase + accented variants).
3. Document the role here.
4. Wire the triggers in the skill's `description:` field.

## Walkthrough personas (different concept)

`theme-critique` and other refinement skills run a **persona walkthrough** of the screen. Those are *user* personas (your actual users), distinct from the *skill* personas above. Configure them in `.design-workflow.yaml` under `product.personas` (see `config.example.yaml`).
