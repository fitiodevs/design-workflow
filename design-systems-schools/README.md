# design-systems-schools/

Library of **12 design philosophy schools** — sibling to `design-systems/` (brand systems library, v1.2.0). Authored from scratch under Apache-2.0; structural idea inspired by [`alchaincyf/huashu-design`](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked).

## Schools vs brands — the split

| Library | Captures | Use when |
|---|---|---|
| `design-systems/` (brand library) | Specific brand identities — Apple, Stripe, Notion, Linear, Claude. 20 entries with explicit hex codes. | "Make it look like X" — identity imitation; you want a specific tone vocabulary cribbed from a real product. |
| `design-systems-schools/` (school library) | Aesthetic philosophies — Müller-Brockmann, Pentagram, Brutalism, Memphis. 12 entries with constraints, not hex. | "Follow X's principles" — the *philosophy* drives palette generation; same school produces different palettes for different projects. |

Schools encode constraints (`accent must be saturated primary, ≤10% pixels, contrast ≥7:1`); the translator at `scripts/school_md_to_appcolors.py` synthesizes a palette that satisfies the constraints. Brands encode literal hex; the translator at `scripts/design_md_to_appcolors.py` extracts directly. Both translators emit the same `proposal.json` + `rationale.md` shape.

## Category index — grouped by primary scenario strength

### Flutter-strong (best for app UI, Web ★★★)

| Slug | School | One-line philosophy |
|---|---|---|
| `pentagram` | [Pentagram (Bierut)](pentagram/SCHOOL.md) | A design that earns its space; every element is the result of an argument the designer won. |
| `information-architects` | [Information Architects](information-architects/SCHOOL.md) | Content has dignity; the design's only job is to keep faith with it. |
| `brutalism` | [Brutalism (web)](brutalism/SCHOOL.md) | Show the building's concrete; the design polish was the lie. |
| `locomotive` | [Locomotive](locomotive/SCHOOL.md) | Scroll is the story; pace it like a film cut. |

### Print-strong (best for PDF · Cover · Infographic, Print scenarios ★★★)

| Slug | School | One-line philosophy |
|---|---|---|
| `muller-brockmann` | [Müller-Brockmann](muller-brockmann/SCHOOL.md) | Order is communication — the grid is not decoration; it is the medium that makes information visible. |
| `kenya-hara` | [Kenya Hara](kenya-hara/SCHOOL.md) | Emptiness is not absence — it is content; the white space carries the meaning the type cannot. |
| `editorial` | [Editorial (Wired/Apple-mag)](editorial/SCHOOL.md) | The page is a magazine spread; the reader is here to read, and the design should pace the reading like a great editor. |
| `atelier-zero` | [Atelier Zero](atelier-zero/SCHOOL.md) | Paper has memory; design lives in the marks of process — torn edges, plaster dust, marker scribbles, Roman numerals. |

### AI-gen-strong (best for generative imagery, AI-image-gen ★★★)

| Slug | School | One-line philosophy |
|---|---|---|
| `memphis` | [Memphis (postmodern)](memphis/SCHOOL.md) | Good taste is a class signal; reject it for the joy of color, pattern, and disrespectful geometry. |
| `active-theory` | [Active Theory](active-theory/SCHOOL.md) | The screen is a stage; everything that arrives must arrive choreographed. |

### Versatile (≥4 scenarios at ★★★)

| Slug | School | One-line philosophy |
|---|---|---|
| `sagmeister-walsh` | [Sagmeister & Walsh](sagmeister-walsh/SCHOOL.md) | Design that doesn't make you feel something is design that's failed. |
| `takram` | [Takram](takram/SCHOOL.md) | Data is not information until it is *seen* — and seeing requires the patience of art, not the efficiency of dashboards. |

12 entries · 4 categories · spread tuned to maximize coverage across Flutter UI · HTML mockup · PPT · PDF · Infographic · Cover · AI-image-gen.

## File contract

Every `<slug>/SCHOOL.md` follows this shape (8 sections + attribution header, target ~80–150 lines):

```
> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** huashu-design / open-design (per origin)
> **License:** Apache-2.0
> **Local path:** design-systems-schools/<slug>/SCHOOL.md
> **Created:** YYYY-MM-DD

# <School Name>

> Category: <free-text categorization>

## Philosophy nucleus               # 1-paragraph thesis
## Core characteristics             # 4-7 bullets — concrete visual signatures
## Prompt DNA                        # 1-2 paragraphs — system-prompt extension
## Token implications (Flutter)     # 5-8 bullets — color/type/spacing/radius/border/motion/iconography
## Execution-path matrix            # 7-row table (Flutter UI · HTML · PPT · PDF · Infographic · Cover · AI-image-gen)
## Slop traps                       # 5-8 bullets — concrete failure modes (❌ X)
## Best paired with                 # 2-4 schools that compose well
## Anti-pairs (don't blend)         # 2-5 schools that conflict
```

The constraint translator (`scripts/school_md_to_appcolors.py`) consumes **Token implications** + **Philosophy nucleus** to synthesize a Flutter `AppColors` proposal. Other sections inform Clara's `--school <slug>` flag and the rationale doc.

## Adding a new school

1. Pick a slug (kebab-case).
2. Copy an existing `SCHOOL.md` and replace content. Aim for ≥75 substantive lines across the 8 sections; quality beats line count.
3. Run the translator to ensure constraint extraction works: `python3 scripts/school_md_to_appcolors.py design-systems-schools/<slug>/`.
4. Append slug to the appropriate category table above.

Curation guideline: cap each category at 4. Prefer schools that fill an unrepresented scenario column over duplicates of well-covered ones.

## Re-syncing / drift

Schools don't drift the way brands do — Müller-Brockmann's principles in 2026 are the same as in 1981. There's no upstream SHA to track. The only re-validation cadence is for the **execution-path matrix** external-tool recommendations (Marp / Slidev / Pandoc / Midjourney references in `docs/design-schools-execution-paths.md`); those rot and need quarterly review.

## Why these 12 (not all 20)

Coverage > volume. 12 well-authored entries beat 20 thin ones. The mix prioritizes scenario spread (4 Flutter-strong, 4 Print-strong, 2 AI-gen-strong, 2 Versatile). If usage signals demand more (e.g. someone needs Resn or Field.io), add on demand — the file contract is well-defined and additions are 1-PR per school.
