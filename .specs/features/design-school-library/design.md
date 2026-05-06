# Design: design-school-library

## Decisions

### D-A — Schools and brands are parallel, not nested

`design-systems/` (v1.2.0 brand library) and `design-systems-schools/` (this v1.5 library) are siblings, not parent-child. Reason: they're different abstractions:

- Brand systems = "look like Apple/Stripe" (identity imitation)
- Schools = "follow Müller-Brockmann's philosophy" (principle adherence)

Mixing them in one folder confuses the picker UX and the translator logic. Separating keeps each clean.

File naming reflects the split: `DESIGN.md` (brands) vs `SCHOOL.md` (schools). At a glance, the user knows which abstraction they're touching.

### D-B — Schools encode constraints, not literal hex

A brand's DESIGN.md says `--accent: #c96442`. A school's SCHOOL.md says "accent must be primary or saturated red, ≤10% of pixels, contrast ≥7:1 against neutral background". The translator generates a hex *that satisfies the constraint* (not a hex pulled from the source).

This makes the schools library composable in ways the brand library isn't:

- The same school applied to two different projects produces two different palettes (each respecting the project's brand constraint vs the school constraint).
- Schools can blend in v1.6 by intersecting constraints (Müller-Brockmann + Memphis = "Swiss grid backbone with one Memphis-style accent moment").

### D-C — Multi-target matrix is reference, not commitment

7 columns: Flutter UI · HTML mockup · PPT · PDF · Infographic · Cover · AI-image-gen. We **execute** for Flutter UI and HTML mockup (we have the skills). We **document** for the others (the matrix tells you to use HTML path with Marp/Slidev/Pandoc/Midjourney/etc).

This is honest: we don't pretend to be a multimedia generator. The matrix gives the user agency — they pick the path, we provide the prompt DNA + recommend a known-good tool.

### D-D — Constraint-based translator is harder; ship a fallback

REQ-02.2 promises constraint-based translation. T-09 builds it. If the constraint synthesis produces poor palettes (e.g. too-muted or accidentally violates the school's character), fall back to a hybrid:

- Constraint-driven token generation for 80% of tokens
- For the 20% where constraints are ambiguous, ask user 2 quick disambiguation questions

The fallback is acceptable; the goal is "useful proposal", not "perfect synthesis".

### D-E — Curate 12, not all 20

Coverage > volume. 12 well-authored entries beat 20 thin ones. The mix prioritizes:

- 4 Flutter-strong (Pentagram, IA, Brutalism, Locomotive) — for app design
- 4 Print/Cover-strong (Müller-Brockmann, Kenya Hara, Editorial, Atelier-Zero) — for marketing
- 2 AI-gen-strong (Memphis, Active Theory) — for generative imagery
- 2 Versatile (Sagmeister, Takram) — for cross-target work

If usage signals demand for more (e.g. "someone wants Resn"), add on demand.

### D-F — `--school` flag in Clara is sticky

When the user invokes `frontend-design --school müller-brockmann` once for a feature, the school slug is auto-applied to subsequent invocations on the same feature (via `.design-spec/features/<feature>/active-school.txt`). Reason: one feature should have one school; switching mid-flight rarely makes sense and re-typing the flag is friction.

User can override with `--school <other>` or clear with `--no-school`.

### D-G — External tool recommendations are time-stamped

`docs/design-schools-execution-paths.md` lists external tools (Marp, Slidev, Pandoc, Typst, Midjourney, Stable Diffusion, etc) with a "last validated: YYYY-MM-DD" footer per tool. Tools change; recommendations rot. Time-stamping invites re-validation at sweep cadence.

## Architecture

```
<repo>/
├── design-systems/                          # v1.2.0 brands library (existing)
│   ├── README.md
│   └── claude/DESIGN.md, etc                # 20 brand DESIGN.md files
├── design-systems-schools/                  NEW
│   ├── README.md                            # category index, scenario-strength grouping
│   ├── pentagram/SCHOOL.md
│   ├── muller-brockmann/SCHOOL.md
│   ├── kenya-hara/SCHOOL.md
│   ├── information-architects/SCHOOL.md
│   ├── brutalism/SCHOOL.md
│   ├── memphis/SCHOOL.md
│   ├── sagmeister-walsh/SCHOOL.md
│   ├── active-theory/SCHOOL.md
│   ├── editorial/SCHOOL.md
│   ├── locomotive/SCHOOL.md
│   ├── takram/SCHOOL.md
│   └── atelier-zero/SCHOOL.md
├── scripts/
│   ├── design_md_to_appcolors.py            # v1.2.0 brand translator (existing)
│   └── school_md_to_appcolors.py            NEW: school constraint-based translator
├── skills/
│   ├── theme-create/SKILL.md                # MODIFIED: --inspired-by-school flag + workflow
│   └── frontend-design/SKILL.md             # MODIFIED: --school flag + sticky session
├── docs/
│   └── design-schools-execution-paths.md    NEW: external tool recommendations + matrix usage
├── README.md                                # MODIFIED: §v1.5 + Design schools library section
├── .specs/project/STATE.md                  # MODIFIED: D-20, D-21, D-22
└── .claude-plugin/marketplace.json          # MODIFIED: 1.4.0 → 1.5.0
```

## SCHOOL.md template

```markdown
> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/<slug>/SCHOOL.md`
> **Created:** 2026-MM-DD

# <School Name>

> Category: <Information-architecture | Editorial | Postmodern | Kinetic | Brutalist | …>

## Philosophy nucleus

(One sentence summarizing the school's thesis. Direct, opinionated.)

Example for Müller-Brockmann: "Order is communication — the grid is not decoration; it's the medium that makes information visible."

## Core characteristics

- 4-6 bullets of concrete visual signatures (e.g. "Helvetica or Akzidenz at 1-2 weights only", "8-column grid as the visible structure not the hidden one", "Reds at 100% saturation, never tints").

## Prompt DNA

(1-2 paragraphs the model loads as system-prompt extension when this school is invoked. Concrete enough to drive emission. References tools/concepts the model can act on.)

Example for Müller-Brockmann:
"Communicate through the grid. Compose every section on a strict 8-column or 12-column grid that the user can sense even if not see. Use exactly two type weights — regular and bold — at sizes that follow a 1.25 multiplier. Reduce the palette to neutrals (whites, blacks, single mid-gray) plus one chromatic accent at full saturation, used at most twice per screen. Refuse decorative ornament: borders, gradients, drop-shadows, rounded corners larger than 4px. The composition is the design; the chrome is silence."

## Token implications (Flutter)

- **Color**: 1 accent (saturated primary), 1 mid-gray, white surface, near-black text. brandDefault = the accent. textPrimary = #1a1a1a or similar warm-leaning. bgBase = #ffffff or #fafafa.
- **Typography**: monospace neutral or grotesque sans (Inter, Helvetica, Akzidenz). 2 weights. Multiplier 1.25.
- **Spacing**: 8-column grid → multiples of 8 are natural. AppSpacing = sm/md/lg/xl/xxl on 8/16/24/32/48 ladder.
- **Radius**: minimal. AppRadius.sm = 2-4px max.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★☆ | HTML mockup → theme-port (works, but the school's grid discipline is more visible in HTML) |
| HTML mockup (Clara) | ★★★ | direct — Clara emits with --school müller-brockmann |
| PPT | ★★★ | use HTML mockup as source → Marp or Slidev with the school's CSS as theme |
| PDF | ★★★ | use HTML mockup → Pandoc or Typst with grid-locked layout |
| Infographic | ★★★ | use HTML mockup → static export to PNG/SVG |
| Cover | ★★☆ | use HTML mockup → static export; the school is grid-strong but less imagery-driven than Memphis or Sagmeister |
| AI-image-gen | ★☆☆ | weak — Midjourney/SDXL produce decorative output that violates the school's reduction principle. Don't bother. |

## Slop traps

- ❌ Adding "modern" decorative gradients — anti-school
- ❌ Using more than one accent color
- ❌ Rounding corners >4px
- ❌ Adding drop-shadows for "depth" — the school says depth comes from the grid
- ❌ Using more than two type weights

## Best paired with

- Pentagram (similar typography discipline; can blend in v1.6+)
- Information Architects (typography-first, complements grid-first)

## Anti-pairs (don't blend)

- Memphis (postmodern playfulness directly contradicts the school's reduction)
- Active Theory (kinetic effects are anti-grid)
```

Target length: 150-220 lines per school × 12 schools ≈ 2400-2640 lines of school authoring.

## Translator design (constraint-based)

```python
# scripts/school_md_to_appcolors.py
"""
Convert a design-systems-schools/<slug>/SCHOOL.md into a Flutter AppColors proposal.
Constraint-based: school declares constraints; we satisfy them.
"""

# Phases:
# 1. parse_school_md(path) -> {philosophy, characteristics, prompt_dna, token_implications, matrix, slop_traps}
# 2. extract_constraints(token_implications) -> [Constraint(...), ...]
#    Constraints look like: "accent ≤ 10% of pixels", "neutrals 80%+", "WCAG ≥ 7:1 for body text"
# 3. synthesize_palette(constraints) -> {bgBase, brandDefault, textPrimary, ...}
#    Uses oklch_to_hex.py to generate values that satisfy constraints
# 4. validate_wcag(proposal) -> mark failures, attempt repair
# 5. write_artifacts(proposal, rationale, out_dir)

# Constraint solver phase is the new logic vs v1.2.0's literal-extraction.
```

Constraint synthesis approach:

- Extract constraints from "Token implications" section by parsing each bullet
- Use OKLCH math to find values within the constraint's bounds
- Iterate: if WCAG fails after first synthesis, adjust lightness, re-check
- Cap iterations at 5; if no convergence, emit partial proposal + flag in rationale

## Validation strategy

```bash
# 1. quick_validate.py
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done   # 21/21 valid

# 2. Translator smoke
for school in muller-brockmann brutalism editorial; do
    python3 scripts/school_md_to_appcolors.py design-systems-schools/$school/ --out-dir /tmp/school-test/$school/
    # manual review for sanity
done

# 3. End-to-end
# /theme-create --inspired-by-school müller-brockmann → produces sane Dart AppColors
# /frontend-design --school memphis "milestone slider" → emits HTML with Memphis-character signatures (visible bold colors, geometric patterns, 80s-postmodern type)
```

## Rollback

`git tag pre-v1.5.0` before T-00.

## Estimate

- Curate + finalize 12 schools list: ~30 min
- Author 12 schools (template + content): 12 × 40 min = 8h
- README for school library: ~30 min
- Translator: ~3h (constraint-solver is the heart)
- Skills wires (theme-create + frontend-design flags): ~1h
- docs/design-schools-execution-paths.md: ~1h (research recommended tools, time-stamp)
- STATE/version/validation/commit: ~1h
- **Total: ~15h** (matches 14-18h spec; school authoring is the main cost)
