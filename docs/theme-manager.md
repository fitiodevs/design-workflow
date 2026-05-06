# Theme manager — human-readable guide

A friendly walkthrough of the design pipeline. Read this if you're new to the workflow and want the "why before how".

## The shape of the workflow

```
        ┌──────────────────┐
        │   theme-audit    │  ← start here
        │     (Auditor)    │  measures violations + WCAG
        └────────┬─────────┘
                 │
       ┌─────────┼─────────┐
       │         │         │
       ▼         ▼         ▼
   create     extend     port
   (palette  (single    (Figma →
    from      token      widgets)
    scratch)  fix)
       │         │         │
       └─────────┼─────────┘
                 ▼
       ┌──────────────────┐
       │  theme-critique  │  ← scores Nielsen + AI-slop
       │     (Critic)     │
       └────────┬─────────┘
                │
        ┌───────┼────────┐
        │       │        │
        ▼       ▼        ▼
     bolder  quieter  distill
     (timid) (shouty) (overload)
        │       │        │
        └───────┼────────┘
                ▼
       ┌──────────────────┐
       │  theme-motion    │  if static-too-much
       │ (Choreographer)  │
       └──────────────────┘
```

## Workflow patterns

### "I'm starting a new app"

```
/theme-create                    # Composer: palette from scratch
/frontend-design                 # Designer: HTML mockup of the first screens
/theme-port --from-html <path>   # Architect: HTML → Flutter using tokens
/theme-audit                     # Auditor: measures coverage
```

### "I have a Figma frame and need it implemented"

```
/theme-port <figma-link>
/theme-critique
# if critique flags issues → bolder/quieter/distill as needed
```

### "Something looks off but I can't say what"

```
/theme-critique
```

It returns scored Nielsen heuristics + AI-slop verdict + persona walkthrough + cognitive load count + P0–P3 issue list with delegation suggestions. Read the verdict, follow the suggested next skill.

### "Low contrast in dark mode"

```
/theme-audit         # confirms which combinations fail WCAG
/theme-extend        # Surgeon: fixes the failing token
```

### "Mockup looks great but Flutter version doesn't match"

```
# 1. Generate the mockup
/frontend-design

# 2. Port the HTML directly (no Figma round-trip needed)
/theme-port --from-html /tmp/<feature>_mockup.html
```

`frontend-design` (Designer / Clara) generates HTML mockups; `theme-port` (Architect / Arquiteto) converts them — or any other HTML source, or a Figma frame — into widgets using your tokens. The Designer + Architect handoff is intentional: Designer obsesses over typography rhythm, alignment, microcopy; Architect translates structure to code. Same skill handles HTML from Stitch, Penpot, Figma's HTML export, or hand-written.

## How personas refuse work

Each persona has a clear "NOT for" list. If you ask the wrong one, they delegate:

- Auditor refuses palette decisions → routes to Composer
- Composer refuses single-token tweaks → routes to Surgeon
- Critic refuses to write code → routes to Architect / Surgeon / etc.
- Choreographer refuses motion-for-motion → recommends just shipping the static screen
- Designer refuses Flutter code → routes to Architect
- Distiller refuses to add features → only removes

This isn't bureaucracy. It's a way to keep each skill *narrow enough* to actually be opinionated.

## When to use which "calmer/bolder/distill"

After a critique:

- **Screen feels timid / "AI safe" / no impact** → `theme-bolder` (Amplifier / Brasa)
- **Screen feels aggressive / shouty / oversaturated** → `theme-quieter` (Refiner / Calma)
- **Screen feels overloaded / >4 decisions / I don't know where to look** → `theme-distill` (Distiller / Lâmina)

If 2 of these apply, do them in this order: `distill` → `bolder` (or `quieter`). Reducing decisions first reveals what actually needs amplification or calming.

## Anti-AI-slop primer

The scoring is calibrated against [Anthropic's design tone guide](https://www.anthropic.com/) plus 7 archetypal slop patterns (see [methodology.md](methodology.md)). Three positive signals counter slop:

1. **Committed color** — no pastel-everything; pick a hero color and ride it.
2. **Earned motion** — every animation teaches something; otherwise remove.
3. **Type as image** — display-size headlines that compete with hero illustrations, not whisper labels.

A screen with all three signals + ≤ 4 decisions + WCAG passing rarely fails critique.
