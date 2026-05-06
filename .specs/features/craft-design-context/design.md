# Design: craft-design-context

## Decisions

### D-A — Author from scratch, cite for idea attribution

Huashu's license forbids redistribution. We write our own doc top-down, citing huashu only as **idea source** in the header (not as prose source). Concretely: read huashu's doc once for inspiration, close it, write ours from our own framing (Flutter-specific tier examples, explicit refusal rule that huashu doesn't have, integration with our `dw.craft.requires:` field).

If reviewers later think the prose looks too close, we revise. The risk is low because:
- Our tier 1 mentions Flutter-specific paths (`lib/core/theme/`, `docs/design-clara.md`) huashu doesn't have
- Our refusal rule is sharper ("STOP and ask" vs huashu's "vague brief is last resort")
- Our examples reference our skills (`/theme-port`, `/theme-create`)

### D-B — Ride along v1.1.1 vs ship as v1.1.2

Two paths:

- **Ride along**: merge tasks into the v1.1.1 commit. Pro: one release, less ceremony. Con: spec for v1.1.1 was already written ignoring this; reviewer might conflate the two efforts.
- **Ship separate**: this becomes v1.1.2 right after v1.1.1. Pro: clean separation in git history. Con: 2 commits + 2 release sections in README.

Default to **ride along** if work is done in the same session as `craft-adoption`. Default to **separate v1.1.2** if `craft-adoption` shipped first and we're coming back. T-00 captures which mode we're in.

### D-C — Tier hierarchy is 5 levels, not more

Resist over-engineering. 5 tiers cover real cases:

1. Existing design system → highest signal, most reusable
2. Codebase → second highest (existing patterns)
3. Deployed product → screenshots when codebase isn't shareable
4. External brief → Figma/HTML/written
5. Vague brief → STOP

Adding "deployed competitor product" or "moodboard image" or other tiers complicates without adding decision quality. Skip.

### D-D — Decision rule is binary: STOP or proceed

The doc must end with a clear "if no Tier 1-4 context, STOP" statement. Wishy-washy phrasing ("preferably check context") is what enabled the slop in the first place. Sharp rule = sharp behavior.

### D-E — Wire 5 skills total in this feature

Add to `craft-adoption` v1.1.1's 5 wires:

- `theme-port`: keep wired (already in v1.1.1) + ADD design-context
- `theme-create`: keep wired (already in v1.1.1) + ADD design-context
- `theme-critique`: keep wired (already in v1.1.1) + ADD design-context
- `frontend-design`: keep wired (already in v1.1.1) + ADD design-context
- `theme-extend`: NEW wire (not in v1.1.1) — gets `design-context` only

`theme-bolder` does NOT get design-context. By the time bolder runs, the screen already exists; context is implicit in the screen itself.

`theme-motion`, `ux-writing` don't get it either — they have their own context models already (`flutter_animate` patterns, `docs/product.md` §4 voice).

### D-F — "Pre-flight context check" section pattern

In each wired skill, just before the workflow Step 1, insert:

```markdown
## Pre-flight context check

Before generating, verify Tier 1-4 context exists per `craft/design-context.md`. Concrete check for this skill:

- Tier 1: `lib/core/theme/app_colors.dart` exists and is non-trivial (>50 lines)?
- Tier 2: similar widgets exist in `lib/features/<related>/`?
- Tier 3: existing screenshots in `docs/screenshots/` or deployed product accessible?
- Tier 4: `docs/product.md` exists and has a §Tone section?

If all four are absent, STOP and ask the user to seed at least Tier 4 (`docs/product.md`) before proceeding.
```

Per-skill, the concrete checks vary. T-04 customizes for each.

## Architecture

```
<repo>/
├── craft/
│   ├── README.md                # MODIFIED: 6-row table
│   ├── anti-ai-slop.md
│   ├── animation-discipline.md
│   ├── color.md
│   ├── design-context.md        # NEW (this feature)
│   ├── state-coverage.md
│   └── typography.md
├── skills/
│   ├── theme-port/SKILL.md      # MODIFIED: add design-context to requires + Pre-flight section
│   ├── theme-create/SKILL.md    # MODIFIED: same
│   ├── theme-extend/SKILL.md    # MODIFIED: NEW wire (was unwired in v1.1.1)
│   ├── theme-critique/SKILL.md  # MODIFIED: add design-context
│   └── frontend-design/SKILL.md # MODIFIED: same
├── README.md                    # MODIFIED: §v1.1.1 mentions 6th doc
└── .specs/project/STATE.md      # MODIFIED: D-11.1
```

## design-context.md outline (target structure)

```markdown
# Design context — blank-page is last resort

> [attribution header]

## Why this matters

(1 paragraph: blank-page generation produces category-reflex output. Concrete example: /theme-port without docs/product.md → green Strava-clone.)

## The 5-tier context hierarchy

### Tier 1 — Existing design system
**What it is:** the project's own tokens, components, type scale, brand voice.
**Where to look (Flutter):** `lib/core/theme/`, `docs/design-tokens.md`, `docs/design-clara.md`, `lib/core/widgets/`.
**What to extract:** hex codes verbatim, spacing scale, font families, AppButton/AppCard component definitions.
**What NOT to extract:** anything not declared in the system (don't infer "similar feel" — only use what's literal).

### Tier 2 — Codebase
**What it is:** existing widgets that solve adjacent problems.
**Where to look:** `lib/features/<related-feature>/`.
**Why:** matching an existing successful widget keeps the system coherent.
**What NOT to do:** copy code verbatim — extract patterns and adapt with the system's tokens.

### Tier 3 — Deployed product
**What it is:** screenshots of what's already shipping.
**Where to look:** `docs/screenshots/`, app stores, browser screenshot tool.
**Use when:** Tier 1+2 absent (no shared codebase).

### Tier 4 — External brief
**What it is:** Figma frame, HTML mockup, written brief in `docs/product.md`.
**Validation:** brief must have explicit tone declarations, not vague descriptors ("modern" / "clean" / "professional" are vague).

### Tier 5 — Vague description (LAST RESORT)
**Action:** STOP. Ask the user to seed at least Tier 4 before generating.

## The decision rule

```python
if not (tier_1 or tier_2 or tier_3 or tier_4):
    REFUSE("No design context found. Cannot generate without context.")
    return
```

Always refuse. Synthesizing context from prompt-only is the failure mode.

## Concrete examples

### Example 1: /theme-port a Figma frame in a project with no docs/product.md
- Tier 1 check: `lib/core/theme/app_colors.dart` exists? Yes.
- Tier 4 check: `docs/product.md` exists? No → REFUSE. Tone synthesis from frame alone produces category-reflex.

### Example 2: /theme-create for a sub-brand
- Tier 1: existing default theme as the contrast reference.
- Tier 4: `--inspired-by <slug>` flag or 8 pre-conditions.
- If both absent: REFUSE.

### Example 3: /theme-extend a single token
- Tier 1: required (must read existing palette to pick a coherent value).
- Tier 4: not strictly required (the request "add a token for disabled" is concrete).

## Anti-patterns

- ❌ Synthesizing tone from the user's prompt ("Eleve seu jogo" → assumes athletic/aggressive)
- ❌ Defaulting to Tailwind indigo when no accent is declared
- ❌ Assuming "modern/clean/professional" maps to specific visual decisions
- ❌ Generating fallback "neutral gray" palette when no context — neutral gray is a category-reflex, not a fallback

## Integration

This doc is referenced by skills via `dw.craft.requires: [design-context, ...]`. Each skill's "Pre-flight context check" section maps the 5 tiers to concrete checks for that skill's domain.
```

Total target: ~110 lines.

## Validation strategy

```bash
# 1. Doc exists with attribution + 5 tiers
test -f craft/design-context.md
grep -c "^### Tier" craft/design-context.md     # should be 5

# 2. Wired skills reference it
grep -l "design-context" skills/*/SKILL.md      # 5 skills

# 3. quick_validate.py
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done   # 19/19 valid

# 4. craft/README.md lists 6 docs
grep -c "^\- " craft/README.md   # ≥ 6 list items in the table or list
```

## Rollback

Same `pre-v1.1.1` tag if shipping with craft-adoption. Otherwise `pre-v1.1.2` if shipping standalone.

## Estimate

- Author design-context.md: ~25 min
- Update craft/README.md: ~5 min
- Wire 5 skills (mostly Edit + Pre-flight section): ~20 min total
- STATE.md + README: ~5 min
- Validation: ~5 min
- **Total: ~60 min** (rolls into v1.1.1's overall ~3h budget)
