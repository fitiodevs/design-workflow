> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/memphis/SCHOOL.md`
> **Created:** 2026-05-07

# Memphis (postmodern)

> Category: Postmodern · Pattern-bold · Anti-good-taste

## Philosophy nucleus

Good taste is a class signal; reject it for the joy of color, pattern, and disrespectful geometry.

The Memphis Group (Milan, 1981–1988, founded by Ettore Sottsass and others) was the antithesis of the Bauhaus / Swiss / Mid-Century-Modern good-taste consensus. Memphis demanded squiggles, terrazzo, primary colors next to teal, asymmetric polka-dots, and unstable geometric forms — a deliberate refusal of the "less is more" ideology. The work was funny, threatening, energetic. Today's web revival (1990s nostalgia + zoomer postmodernism) carries the same DNA: *the joy of bad taste is good taste*.

## Core characteristics

- **Color: 4–6 saturated hues that "shouldn't" go together**. Hot pink + electric blue + lemon yellow + acid green + black is canonical. NEVER muted, never tinted, always at full saturation.
- **Pattern as a primary visual element**: terrazzo squiggles, polka-dots, zigzags, irregular grids, checkerboards. Patterns appear as backgrounds, as fills, on illustrative shapes — not as accents.
- **Type-as-image**: oversized headlines in geometric sans (Druk, ITC Avant Garde, Right Grotesk) at fragmented angles, sometimes overlapped, sometimes outlined, sometimes filled with pattern.
- **Geometric shapes deployed playfully**: squiggles, half-circles, triangles, asymmetric rectangles. Shapes appear as decorative actors, not as containers.
- **Asymmetric, unstable composition**. Things lean; alignments break; symmetry is forbidden. The page feels like it might tip over.
- **Photography (when used) is collaged**: cut-out subjects on geometric backgrounds, often hand-rendered. Never raw documentary photography.
- **Typography is bold as a default**: 700+ weight for body text on landing/marketing surfaces; subheads in italic-bold with letter-spacing.

## Prompt DNA

Compose joyfully. Use 4–6 saturated colors that aren't supposed to work together — hot pink (`#ff0080`), electric blue (`#0066ff`), lemon yellow (`#ffeb00`), acid green (`#a3ff00`), with black as a frequent contrast and white as the rare neutral. Apply patterns as primary visual elements: terrazzo squiggles in SVG, polka-dot fills, zigzag borders, checkerboards as backgrounds. Patterns are not accent; they are the design.

Type-as-image: headlines in geometric sans (Druk, Right Grotesk, ITC Avant Garde, or Inter Display as fallback) at oversized scales (≥80px), sometimes outlined with no fill, sometimes filled with pattern, sometimes overlapped. Italic-bold for subheadings with letter-spacing. Geometric shapes (squiggles, half-circles, triangles) deployed playfully across compositions, not as accents but as actors. Asymmetric and unstable: alignments break; centering is forbidden; the page should feel like it might tip over. Photography (if used) is collaged — cut-out subjects on patterned backgrounds, never raw documentary.

Refuse "good taste" — refuse muted palettes, refuse single-accent restraint, refuse minimalist whitespace. The joy of color and pattern IS the school. If the work feels too tasteful, add another color or another pattern until it stops being tasteful.

## Token implications (Flutter)

- **Color**: 4–6 saturated hues — hot pink (`#ff0080`), electric blue (`#0066ff`), lemon yellow (`#ffeb00`), acid green (`#a3ff00`), plus black (`#0a0a0a`) and white (`#ffffff`). `brandDefault` = the most-used hue (probably hot pink or electric blue). The other hues populate `gameAccent`, secondary brand tokens, badges. The school *uses* the multi-color tokens we have; it doesn't reduce to one accent.
- **Typography**: Druk, Right Grotesk, ITC Avant Garde, Inter Display fallback. 2 weights (400 + 700+); italic-bold for subheads. Multiplier 1.333 (large jumps for large display). Body sometimes in bold (700) by default.
- **Spacing**: irregular, anti-modular. AppSpacing on 8-base but with deliberate breakings: 8 / 12 / 24 / 36 / 64 — including non-power-of-two intervals to feel unstable.
- **Radius**: variable — sharp on text containers (0px), pill on buttons (9999px), softly rounded on illustrative shapes (8–24px). The school *plays* with radius, doesn't reduce it.
- **Border**: thick (3–6px solid) where present, in saturated brand colors not gray. Often combined with offset (a card with a 4px solid pink border offset 6px from a yellow shadow-block).
- **Motion**: bouncy — 400ms with spring/elastic curves. Hover states do something playful (rotate, pop, swap-color). Loaders are geometric and animated.
- **Iconography**: filled, geometric, multi-color. Stroke-only icons betray the school.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★☆ | viable for entertainment / kids / creative-tool apps; risky for productivity (the visual energy fatigues over long sessions). |
| HTML mockup (Clara) | ★★★ | direct fit for landing pages, event sites, product launches with Memphis-character branding. `frontend-design --school memphis` produces playfully-overstated layouts. |
| PPT | ★★☆ | viable for kid/teen-facing decks, festival decks, brand-launch keynotes. Hard to use without exhausting the audience over a long deck. |
| PDF | ★☆☆ | weak — PDF reading-mode expects polish; Memphis exhausts at full-essay length. Possible for short pamphlets or zines. |
| Infographic | ★★☆ | viable — Memphis pattern-as-fill works well for highlighting one data moment. Use sparingly. |
| Cover | ★★★ | strong fit for music covers, festival posters, kid-product packaging, magazine-issue special editions. |
| AI-image-gen | ★★★ | excellent — Midjourney/Stable Diffusion handle pattern-and-color richness well; the school's geometric-playful vocabulary is one of the few aesthetic languages where AI image-gen is on-style by default. Use prompt DNA verbatim. |

## Slop traps

- ❌ **Pastel "Memphis-influenced"** — the school requires saturated. Pastels betray the joy.
- ❌ **One-accent reduction** — Memphis uses many colors; reducing to "Memphis with one accent" is just a different school.
- ❌ **Symmetric, centered layouts**. The school is unstable on purpose.
- ❌ **Treating patterns as accents** (a small terrazzo divider). Patterns are *primary* visual elements.
- ❌ **Avoiding "tacky" combinations**. The "tacky" is the school. Hot pink + lime green is correct.
- ❌ **Adding gradients for "polish"**. Memphis is flat-color; gradients are the next decade's school.
- ❌ **Refusing the bold-by-default body text** in favor of regular weight on landing surfaces. The school's energy demands the bold default.

## Best paired with

- **Sagmeister & Walsh** — both expressive, both color-bold; share type-as-image vocabulary.
- **Active Theory** — kinetic motion + Memphis pattern is a natural festival-poster combination (when motion is wanted).
- **Editorial (special-issue Wired)** — the magazine register's playful editions can carry Memphis pattern.

## Anti-pairs (don't blend)

- **Müller-Brockmann** — Memphis directly contradicts the school's reduction.
- **Kenya Hara** — Hara's quietness vs. Memphis's noise: opposites.
- **Information Architects** — IA refuses decoration; Memphis IS decoration.
- **Pentagram** — Pentagram permits one big move; Memphis demands many.
- **Brutalism** — both refuse mid-century good-taste, but Brutalism reduces; Memphis multiplies. Different anti-stances.
