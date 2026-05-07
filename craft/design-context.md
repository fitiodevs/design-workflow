# Design context — blank-page is last resort

> **Source:** authored from scratch for `design-workflow` v1.2.1.
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) (concept of a context hierarchy preceding generation; prose is original here).
> **License:** Apache-2.0 (same as the rest of `craft/`).
> **Local path:** `craft/design-context.md`.
> **Created:** 2026-05-07.

## Why this matters

Blank-page generation produces **category-reflex** output: ask for a "fitness app palette" and the model writes Strava-green; ask for "fintech" and it writes Robinhood-black-and-mint. The reflex is real because training data clusters category to visual. The way out is not "be more creative" — it is **read the context the user already has** and resist generating until enough exists. This doc codifies the hierarchy and the refusal rule.

## The 5-tier context hierarchy

### Tier 1 — Existing design system

**What it is:** the project's own tokens, components, type scale, brand voice — declared, not inferred.

**Where to look (Flutter):** `lib/core/theme/app_colors.dart`, `lib/core/theme/app_spacing.dart`, `docs/design-tokens.md`, `docs/design-clara.md`, `lib/core/widgets/`.

**Where to look (Next.js + Tailwind):** `app/globals.css` (CSS variables), `tailwind.config.ts` (`theme.extend.colors`), `components/ui/` (shadcn primitives), `docs/design-tokens.md`.

**What to extract:** hex codes verbatim, spacing scale, font families, component definitions (`AppButton`, `<Button>`, etc).

**What NOT to extract:** anything not declared in the system. Don't infer "similar feel" — only use what is literal in the files.

### Tier 2 — Codebase

**What it is:** existing widgets/components that solve adjacent problems.

**Where to look (Flutter):** `lib/features/<related-feature>/presentation/widgets/`. **(Next.js):** `components/<related-feature>/`.

**Why:** matching an existing successful widget keeps the system coherent. A second card in a feed should not be visually unrelated to the first.

**What NOT to do:** copy code verbatim — extract the structural pattern (which tokens, which composition, which states) and adapt with the system's tokens. Verbatim copy ages badly when the source widget evolves.

### Tier 3 — Deployed product

**What it is:** screenshots of what is already shipping.

**Where to look:** `docs/screenshots/`, app stores, browser screenshot tools, internal Notion/Figma libraries of "what we shipped last sprint."

**Use when:** Tier 1 + Tier 2 are absent (the codebase isn't shareable, e.g. a contractor-only review). Screenshots are weaker than tokens because tokens are precise; screenshots invite re-inference.

### Tier 4 — External brief

**What it is:** a Figma frame, an HTML mockup, a written brief in `docs/product.md`.

**Validation:** the brief must declare **tone explicitly** — concrete adjectives that map to decisions, not vague descriptors. "Modern, clean, professional" is vague (every brief says that). "Calm, restrained, no marketing exclamation marks, lowercase headers, ratio-driven typography" is explicit. Refuse the vague version.

### Tier 5 — Vague description (LAST RESORT)

**Action:** STOP. Ask the user to seed at least Tier 4 before generating. Do not synthesize tone from a prompt — that is the failure mode this doc exists to prevent.

## The decision rule

```python
if not (tier_1 or tier_2 or tier_3 or tier_4):
    REFUSE("No design context found. Cannot generate without context.")
    return
```

Always refuse. Synthesizing context from a prompt alone is **the** failure mode. If the user pushes back ("just generate something"), the right answer is still STOP — explain that any output will be category-reflex, then offer to help author a minimal `docs/product.md` §Tone block in 5 minutes.

## Concrete examples

### Example 1: `/theme-port` a Figma frame in a project with no `docs/product.md`

- Tier 1 check: `lib/core/theme/app_colors.dart` exists with >50 lines? Yes → Tier 1 present.
- Tier 4 check: `docs/product.md` exists with a §Tone section? No → Tier 4 absent.
- Tier 1 alone is **not enough for tone** (it tells you which colors exist, not why). Tone synthesis from the frame alone produces category-reflex copy.
- **Action:** REFUSE. Ask the user to seed `docs/product.md` §Tone with 3–5 declared adjectives + 3 banned phrases.

### Example 2: `/theme-create` for a sub-brand

- Tier 1: existing default theme — required as the contrast reference (the new sub-brand must clearly differ from default).
- Tier 4: either an `--inspired-by <slug>` flag pointing at a reference brand, OR the 8 pre-conditions from `theme-create/SKILL.md` answered explicitly.
- If both Tier 1 and Tier 4 absent: REFUSE.

### Example 3: `/theme-extend` a single token

- Tier 1: REQUIRED (must read the existing palette to pick a coherent OKLCH value).
- Tier 4: not strictly required — "add a token for disabled state" is concrete enough.
- If Tier 1 missing (no palette to extend): REFUSE — extending nothing makes no sense.

## Anti-patterns

- ❌ Synthesizing tone from the user's prompt ("Eleve seu jogo" → assumes athletic/aggressive). The prompt is not a brief.
- ❌ Defaulting to Tailwind indigo / Material purple / Strava green when no accent is declared. STOP instead.
- ❌ Assuming "modern/clean/professional" maps to specific visual decisions. It doesn't. Refuse the vague brief.
- ❌ Generating a "neutral gray" fallback palette when no context. Neutral gray is itself a category-reflex (the "design system" reflex), not a neutral position.
- ❌ Treating screenshots (Tier 3) as equivalent to tokens (Tier 1). Screenshots invite re-inference; tokens are precise.

## Integration

This doc is referenced by skills via the `dw.craft.requires: [design-context, ...]` field. Each wired skill carries a "Pre-flight context check" section in its workflow that maps the 5 tiers to **concrete checks for that skill's domain** — e.g. theme-port checks `app_colors.dart` and `docs/product.md` §Tone; theme-create checks `--inspired-by` or 8 pre-conditions; theme-extend checks `app_colors.dart` only.

The skill must STOP and ask the user to seed missing context before proceeding. STOP is sharp. Wishy-washy phrasing ("preferably check context", "ideally read…") is what enabled the slop in the first place.
