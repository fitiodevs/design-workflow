# `/theme-create --inspired-by` and `--browse` flow

> Loaded by SKILL.md when the user invokes either flag. ~80 lines, dense, no padding.

## Why this branch exists

The 8-precondition gate exists to avoid blank-page AI-slop. When the user names a real reference (`/theme-create --inspired-by stripe`), 4 of those preconditions are pre-answered by the source's `## 1. Visual Theme & Atmosphere` paragraph + its `## 2. Color Palette & Roles` structure. We ask only the 4 that are project-specific.

## File contract for `design-systems/<slug>/DESIGN.md`

Every entry begins with a 5-line attribution header (Sourced from / Upstream / License / Local path / Last sync), then the body is a 9-section spec — Visual Theme · Color Palette · Typography · Components · Layout · Depth · Do/Don't · Responsive · Agent Prompt. The translator only consumes the first three.

The category line (`> Category: <Name>`, on line 2 of the body after the header) is what `--browse <category>` filters on. Read `design-systems/README.md` for the category index.

## Translator outputs

```
.tmp/theme-create/<slug>/
├── proposal.json   29 tokens × 2 modes + metadata + WCAG report + decisions trace
└── rationale.md    Source citation · Token mapping · WCAG · Open questions · Game/badge user input
```

`proposal.json.tokens.light` and `.dark` each contain 22 hex strings + 7 `null`s — the nulls are the Fitio-specific game/badge tokens; never silently fill them. `proposal.json.wcag.{light,dark}` is the row-level report; show it to the user.

## What to show the user (in order)

1. **Source paragraph (verbatim).** Pull from the rationale doc's §1. This is the user's gut-check that the translator parsed the right brand.
2. **Token mapping table.** Use the rationale's §2 (already formatted). Highlight any `<derived>` rows — the user needs to know what the translator inferred vs what came from source.
3. **WCAG report.** Pass-rate per mode + each failed pair. Failed pairs are not a halt condition — sub-brands sometimes intentionally trade contrast for identity — but the user must acknowledge.
4. **Game/badge prompt.** "These 7 tokens have no source equivalent: [list]. Suggest A/B/C — which fits this theme?"

## The 4 surviving pre-conditions

| Question | Why still asked |
|---|---|
| Purpose | A "Stripe-inspired Black Friday skin" and a "Stripe-inspired sponsor screen" are different themes. |
| Audience | Same default audience or niche? Affects whether to strengthen contrast or stay close to source. |
| Invariants | Project-specific tokens (`gameAccent`, brand if shared with default) that must persist regardless of inspiration. |
| Coexistence | Does this *replace* the default `AppColors`, or live as a 3rd instance loaded by route? |

## Tweak protocol

The user may want to override specific tokens. Common tweaks:

- **Swap `feedbackError`** to match an existing project red.
- **Pull `borderFocus`** to a contrasting hue when source uses brand-as-focus and that fails 3:1.
- **Saturation drop on `brandMuted`** when the translator's OKLCH derivation is too desaturated.
- **Surface depth** (`bgSurface` vs `bgSurfaceRaised`) — sources with only 2 surface tiers leave both at the same hex; user picks whether to derive a 3rd or accept flatness.

When the user says "actually use #1c2c4a for borderFocus", update the `proposal.json` in-place under `.tmp/theme-create/<slug>/`, re-run `python3 scripts/check_contrast.py --json …` to confirm WCAG holds, and re-emit the Dart snippet.

## Final emission

After tweaks accepted:

1. Convert `proposal.json.tokens.{light,dark}` to a Dart `AppColors` snippet (project's existing `lib/theme/app_colors.dart` shape).
2. Write the ficha to `docs/themes/<slug>.md` — must cite the inspiration: `> Inspired by: design-systems/<slug>/DESIGN.md (sourced from <upstream URL>)`.
3. Append the rationale doc verbatim into the ficha as the §"Mapping rationale" section, so future audits can trace the choice.
4. Run anti-AI-slop checklist (`craft/anti-ai-slop.md`) — purple gradients, glassy reflexes, evenly-distributed 5-color palettes — and flag any violations as fix-before-merge.
5. Output the rollout plan (which screens to repaint first, what to verify in dev).

## What `--browse` adds

`--browse` is purely a discovery shell over `--inspired-by`. It exists because the user often doesn't know which slug to ask for. The bullet:

- Read `design-systems/README.md` (the category index) **OR** scan `design-systems/*/DESIGN.md` for `> Category:` lines if README is stale.
- Filter by category (case-insensitive substring on the user's argument).
- Present a numbered list with the slug + title + the line under `> Category:` (the one-line characterisation).
- Pick → drop into `--inspired-by <picked>`.

## Refusals

- **Mood-blend** ("Stripe + Linear hybrid") — that's the deferred `--blend` feature (post-v1.3). Refuse; pick one slug.
- **Slug not in the curated 20** — offer closest match. Don't auto-fork from upstream mid-flow; that's a separate one-line backlog item.
- **User wants to skip the 4 pre-conditions too** — refuse. Those 4 are project-specific and the source can't answer them.
