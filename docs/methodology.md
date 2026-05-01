# Methodology

The opinionated bits behind the skills. If a skill seems "too strict", this is why.

## OKLCH for palettes

`theme-create` and `theme-extend` generate colors in [OKLCH](https://bottosson.github.io/posts/colorpicker/) (a perceptually-uniform color space) and convert to sRGB hex.

Why: scaling lightness in HSL produces visibly uneven steps (e.g. `hsl(220, 50%, 30%)` and `hsl(220, 50%, 70%)` aren't symmetrically spaced perceptually). OKLCH fixes this — equal `L` differences look equal to humans.

Math: `scripts/oklch_to_hex.py` and `scripts/generate_palette.py` implement the OKLCH → linear sRGB → gamma-corrected sRGB pipeline.

## WCAG 2.1 contrast

`scripts/check_contrast.py` validates pairs against:
- AA normal text: 4.5:1
- AA large text: 3:1
- AAA normal: 7:1
- AAA large: 4.5:1

`theme-extend` blocks merge if a new token combination falls below AA. `theme-audit` reports violations in current code.

## Nielsen 10 heuristics

`theme-critique` scores each screen 0–4 across:

1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, recover from errors
10. Help and documentation

A screen averaging < 2.5 ships only with explicit waiver.

## Anti-AI-slop verdict

`scripts/audit_theme.py` and `theme-critique` look for 7 archetypal slop patterns:

1. **Glassmorphism on every surface** — translucent backdrop blur as decoration, not function.
2. **Pastel-everything palette** — saturation low across the board, no committed color.
3. **Gradient text on every heading** — gradient as default, not as exception.
4. **Same icon style applied uniformly** — usually rounded-thin outlines, no system intent.
5. **Floating cards over abstract gradient bg** — Dribbble-style non-context.
6. **Generic mascot blob** — purple/blue gradient amorphous shape with eyes.
7. **Header-card-card-card-CTA** template repeated across screens.

A screen flagged for ≥ 3 of these earns the "AI slop" verdict. The `bolder`/`quieter`/`distill` skills exist to remove these patterns directionally.

## Cognitive load

Counted as **distinct decisions per viewport**. A decision = anything that asks the user to choose, click, evaluate, or comprehend.

- Tabs in a tab bar: each = 1 decision
- Navigation items: each = 1
- Cards with separate CTAs: each = 1
- Toggle switches: each = 1
- Headers / labels / static images: 0

If a screen exceeds 4 decisions per viewport, `theme-distill` is recommended.

## Persona walkthrough

Configurable in `.design-workflow.yaml`. Each persona walks the screen and reports:
- "Where do my eyes land first?" (visual hierarchy check)
- "What do I think this screen does?" (intent clarity)
- "What's my next action?" (CTA clarity)
- "Anything confusing?" (cognitive load check)

A screen where all 3 personas land on the wrong primary action fails the walkthrough.

## Color commitment levels

Used by `theme-bolder` and `theme-quieter` to scale visual intensity:

| Level | Use | Example |
|---|---|---|
| **Restrained** | Functional screens (forms, lists, settings) | white surface, subtle accents |
| **Committed** | Hero screens (onboarding, feature reveal) | brand color in headers, strong CTAs |
| **Drenched** | Celebration moments (rare, ≤ 2 screens per app) | full surface in brand color, max saturation |

`bolder` moves a screen up the ladder; `quieter` moves it down. The default is **Restrained** — `Drenched` requires justification.

## Motion philosophy

`theme-motion` (`Choreographer` / `Jack`) refuses motion-for-motion's-sake. Every animation must answer:
- **What does this movement teach the user?** (causal chain — A → B because of action X)
- **What would break if removed?** (if nothing — remove it)
- **Does this match the screen's emotional register?** (no celebration motion on a settings screen)

Motion tokens are timing-based (`AppMotion.fast`, `.normal`, `.slow`, `.celebration`) and curve-based (`AppCurves.enter`, `.exit`, `.move`, `.celebrate`). No raw `Duration(milliseconds: 300)` in skills' output.

## Why these constraints

The skills are designed to push back. AI assistants default to "agreeable" — they ship what looks fine. The personas exist to refuse that. A timid screen is a slop screen. A shouty screen is fatiguing. A correct screen is calibrated.
