> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/takram/SCHOOL.md`
> **Created:** 2026-05-07

# Takram (data-poetic)

> Category: Eastern speculative design · Data as narrative · Calm visualization

## Philosophy nucleus

Data is not information until it is *seen* — and seeing requires the patience of art, not the efficiency of dashboards.

Takram (Tokyo / London speculative-design studio) sits at the intersection of Information Architects' reductive editorial discipline and Kenya Hara's negative-space heritage, applied to *data*. They visualize complex systems (climate models, genome data, fiscal flows, urban movement) as calm, deliberate, almost meditative diagrams — diagrams meant to be sat with, not scanned. The work refuses dashboard-style density; the work refuses chart-junk decoration. Each diagram is a small essay, paced and considered.

The tradition draws from Edward Tufte's information-design discipline filtered through Japanese aesthetic restraint — *ma* (negative space) applied to scatter plots; line-charts that breathe; typography that reads like a quiet annotation rather than a label.

## Core characteristics

- **Calm data visualization**: scatter plots with generous whitespace, line charts at thin (1px) stroke in restrained hue, axes that whisper. No 3D charts, no exploding pie-slices, no decorative gradients on bars.
- **Storytelling sequence**: a Takram piece is a *series* of diagrams pacing through a narrative. The first diagram introduces the dimension; the second adds a second dimension; the third reveals the insight. Sequential reading.
- **Mixed-register typography**: serif for body annotation (Tiempos, Cardo, Source Serif), monospace for numerical labels (JetBrains Mono, Roboto Mono), sans for chrome (Inter, Söhne). Three families, by role.
- **Color as encoding, not decoration**: hues encode data dimensions (a temperature gradient, a category ordinal). Never used decoratively.
- **Reductive accent palette**: warm-near-white paper, near-black ink, 1–2 data-encoding hues at calm saturation (forest green, dusty blue, restrained ochre — never electric).
- **Generous outer margins, asymmetric column composition** — annotation lives in the outer margin, like academic Tufte sidenotes.
- **Photography rare**: when used, is documentary (real environments, real instruments, real subjects), captioned in monospace.

## Prompt DNA

Treat data as narrative material; build a *sequence* of diagrams that paces a reader through a complex system. Reductive composition: warm-near-white paper canvas (`#fafaf6`), warm-near-black ink (`#0a0a0a` or `#141413`) for axes and body, 1–2 data-encoding hues at calm saturation (forest green `#1a4d3a`, dusty blue `#3a5572`, restrained ochre `#9b6829` — never electric, never neon).

Mixed-register typography: serif for body annotation (Tiempos, Cardo, Source Serif Pro), monospace for numerical labels and units (JetBrains Mono, Roboto Mono), sans for chrome only (Inter, Söhne). Each family used by role, not for design contrast. Generous whitespace around charts (≥80px outer padding). Asymmetric annotation lives in the outer margin (Tufte sidenote register). Charts are quiet: 1px stroke lines, 2px tick marks, axes labeled in monospace at modest size.

Refuse dashboard density (the school is anti-dashboard); refuse chart-junk decoration (3D bars, drop-shadowed pie slices, gradient fills on data); refuse decorative color (color is encoding, never ornament); refuse template marketing visual moves. Photography (if used) is documentary and captioned in monospace. Each diagram should reward sitting-with, not scanning.

## Token implications (Flutter)

- **Color**: warm paper surface (`#fafaf6`), warm ink-black text (`#0a0a0a`), 1–2 data-encoding hues at calm saturation (forest green, dusty blue, ochre, brick-red). `brandDefault` = the primary data-encoding hue. `bgBase` = paper. `textPrimary` = ink. `bgSurface` = `bgBase` (single tier). The chart uses a 5–7-step sequential or diverging palette derived from `brandDefault` via OKLCH.
- **Typography**: 3 families — serif (`Source Serif Pro`, `Tiempos`, `Cardo` fallback), monospace (`JetBrains Mono`, `Roboto Mono`), sans for chrome (`Inter`, `Söhne`). 2 weights per family. Multiplier 1.25, 6-size ladder.
- **Spacing**: editorial-academic. AppSpacing generous (8 / 16 / 32 / 64 / 128); outer margins ≥80px desktop for chart breathing room. line-height 1.7 body, 1.4 captions.
- **Radius**: 0–4px on UI; chart elements (data points) are circles with 2–4px radius typically.
- **Border**: structural (chart axes, table cells, sidenote dividers). Hairline at low-opacity warm-gray.
- **Motion**: minimal — chart entry animation ≤300ms ease-out; no kinetic motion in the layout. Reading is calm.
- **Iconography**: 1px stroke line icons, geometric, used sparingly.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★★ | strong for data-narrative apps (climate dashboards, scientific visualization, journalism data tools). Pair with `theme-create --inspired-by-school takram`. |
| HTML mockup (Clara) | ★★★ | direct fit — `frontend-design --school takram` produces calm data-paced layouts; D3 / Observable Plot natural for the chart layer. |
| PPT | ★★★ | strong for academic / scientific / TED data-talk decks. Use HTML→Marp/Slidev with takram CSS. |
| PDF | ★★★ | strongest format — long-form data essays, annual environmental reports, scientific publications. Print-grade. |
| Infographic | ★★☆ | viable for narrative infographics (a multi-page data essay); weak for one-glance "infographic" social-media cards (too dense for Takram's pacing). |
| Cover | ★★☆ | works for academic / scientific / data-book covers; weak for commercial product covers. |
| AI-image-gen | ★☆☆ | weak — generative models cannot produce *intentional restraint*; data-as-narrative requires hand-craft and curation. |

## Slop traps

- ❌ **3D charts** (3D bar, 3D pie, exploded pie). Anti-school.
- ❌ **Drop-shadows on data points** for "depth". Data points are flat.
- ❌ **Decorative gradients on bars / lines**. Color is encoding only.
- ❌ **Saturated electric colors** for data hues. The school requires calm saturation.
- ❌ **Dashboard density** (many charts on one page). The school is sequential narrative; one diagram at a time.
- ❌ **Sans-serif body annotation**. The school requires serif body for the reading register.
- ❌ **Chart-junk** (gridlines that scream, prominent borders, large tick marks). Reduce until what remains is data.

## Best paired with

- **Information Architects** — typography and reading-first DNA shared; both reduce.
- **Müller-Brockmann** — grid + data-narrative is the academic-publication register; both schools support data essays.
- **Kenya Hara** — Eastern-restraint heritage; both use *ma* / negative space as content.
- **Editorial (Wired/Apple-mag)** when the data-narrative is published as a long-form magazine feature.

## Anti-pairs (don't blend)

- **Memphis** — color and pattern as decoration violate data-as-encoding.
- **Sagmeister & Walsh** — theatrical type-as-image violates the calm pacing.
- **Active Theory / Locomotive** — kinetic motion violates the meditative reading.
- **Brutalism** — system-default chart-junk is the opposite of takram's deliberate restraint.
