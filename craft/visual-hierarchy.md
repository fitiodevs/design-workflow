> **Adapted from:** [`wondelai/skills` → `refactoring-ui`](https://github.com/wondelai/skills) (MIT), itself distilling Adam Wathan & Steve Schoger's *Refactoring UI*.
> **License:** MIT
> **Local path:** `craft/visual-hierarchy.md`
> **Note:** Authored for this repo (not auto-synced from `nexu-io/open-design`). Re-tuned for a tokens-first, hybrid-mobile (Flutter iOS+Android) workflow. Edits here are safe — no upstream sync overwrites this file.

---

# Visual hierarchy craft rules

Universal rules for making a screen *read* before it is colored. The
active design system decides the palette and fonts; this file decides
how weight, size, spacing, and elevation arrange them so the eye lands
where it should. Sits alongside `color.md` and `typography.md`, upstream
of any project's tokens.

> Founding insight: **great UI is a system, not a talent.** Design in
> grayscale first; add color last. If the screen doesn't work in gray,
> color is a crutch hiding a hierarchy problem.

## Grayscale-first method

Build and judge the screen with **no brand color** — only a neutral
ramp (background, surface, three text tints, one border). Color is the
last layer, added only once hierarchy already holds. This forces
hierarchy to come from the three durable levers below instead of from
accent paint.

The test: screenshot the screen, desaturate it. If you can still tell
the primary action from the secondary, the heading from the body, the
active row from the rest — the hierarchy is real. If everything flattens,
fix structure before touching `--accent`.

## The three hierarchy levers

Rank every element on a screen into **primary / secondary / tertiary**,
then express that rank with — in order of preference:

1. **Weight** — heavier type or more solid fill pulls forward. Cheapest,
   most robust lever. (Pairs with the three-weight system in
   `typography.md`.)
2. **Size** — bigger reads as more important, but escalates fast; cap at
   the type scale's 6–8 steps. Don't solve every rank with size.
3. **Color / contrast** — *de-emphasize* secondary content rather than
   shouting the primary. A muted gray label beside solid-contrast data
   creates rank without adding a single accent.

> De-emphasis beats emphasis. Most "flat" screens are flat because
> *everything* is full-contrast, not because the primary is too weak.
> Push secondary text to a lighter tint before you make the heading
> bigger.

Don't stack all three levers on one element at full strength — that's
how a screen starts shouting. One or two levers per rank step.

## Spacing & sizing

- Use a **fixed spacing scale** — `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64`
  (logical px / Flutter dp). Every gap, pad, and margin is a step on it.
  An off-scale `13` or `22` is a defect, not a nuance. (Matches the scale
  Clara enforces and the `8`-grid both iOS and Android converge on.)
- **Group spacing > within-group spacing.** Whitespace *is* the grouping
  signal: elements that belong together sit closer than the gap to the
  next group. When a layout reads as "soup", it's almost always equal
  spacing everywhere — proximity carrying no information.
- **Give it more space than feels right, then remove.** Cramped is the
  default failure of dense data UIs; start generous and tighten only
  where density earns it (see Clara's Restrained → Committed → Drenched).
- Constrain body measure to **50–75 characters** (see `typography.md`).

## Depth & elevation

Shadows signal *elevation*, not decoration. Use a small, consistent
shadow scale that maps to layers, not a one-off blur per component:

| Elevation | Use |
|---|---|
| none / hairline border | flat surfaces, list rows, inline cards |
| small shadow | raised buttons, cards that lift on press |
| medium | popovers, dropdowns, snackbars |
| large | modals, sheets, dialogs |

Two-part shadows (one tight + dark, one wide + soft) read more physical
than a single fuzzy blur. On a hybrid app, prefer **elevation tokens**
that resolve to Material elevation on Android and a subtler shadow on
iOS — depth is platform-flavored (see `platform-conventions.md`).
Never use shadow as the *only* affordance for an interactive element —
pair it with a state from `state-coverage.md`.

## Diagnostic — the squint/blur test

Before shipping a screen, run these eight checks:

1. **Squint test** — blur your eyes (or the screenshot). Does one element
   clearly dominate? If two fight, you have two primaries.
2. **Grayscale test** — does hierarchy survive desaturation?
3. **Whitespace** — is there *more* space between groups than within?
4. **De-emphasis** — are labels/metadata pushed back, or all full-contrast?
5. **Spacing on-scale** — every gap a step on `4/8/12/16/24/32/48`?
6. **Measure** — body lines 50–75 chars?
7. **Contrast** — text ≥4.5:1, large text/UI ≥3:1 (floor, not goal)?
8. **Elevation** — does each shadow map to a real layer, or is it noise?

## Symptom → cause → fix

| "It looks…" | Usual cause | Fix |
|---|---|---|
| amateur / generic | no hierarchy — everything same weight & size | rank into primary/secondary/tertiary; de-emphasize secondary |
| flat / lifeless | all text full-contrast; no elevation system | mute secondary tints; add the small/medium/large shadow scale |
| cramped / busy | off-scale and equal spacing; too many decisions | snap to the spacing scale; widen group gaps; cut to ≤4 decisions (`/theme-distill`) |
| cluttered | within-group = between-group spacing | increase spacing *between* groups only |
| colors clash | color doing hierarchy's job | rebuild in grayscale; reintroduce one accent, ≤2 visible uses (`color.md`) |
| weak / timid | primary under-weighted *and* secondary not pushed back | raise primary one lever; lower secondary one tint (`/theme-bolder`) |

## Common mistakes (lint these)

- Solving every rank step with **font size** instead of weight + de-emphasis.
- **Equal spacing** everywhere — proximity carrying no grouping signal.
- Off-scale spacing values (`13`, `22`, `30`).
- Full-contrast secondary text drowning the primary.
- A unique shadow per component instead of a 3-step elevation scale.
- Reaching for **accent color to create hierarchy** the structure should carry.
