> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/information-architects/SCHOOL.md`
> **Created:** 2026-05-07

# Information Architects (typography-first)

> Category: Information-architecture · Reading-first · Type-led discipline

## Philosophy nucleus

Content has dignity; the design's only job is to keep faith with it.

Information Architects (the Zurich/NYC studio behind iA Writer and the *Web Trend Map* posters) treat typography not as a design layer but as the *interface itself*. The reader is the user; the user is reading; therefore the typeface, leading, measure, and hierarchy ARE the product. Decoration is a betrayal of the content. The reading interface is monastic — generous margins, single-column body, modest type sizes, and a strict refusal of any element that does not earn its space by improving comprehension.

## Core characteristics

- **Single-column body, optimal measure**. 60–75 characters per line, period. Wider columns are illegible (the eye loses the line return); narrower waste vertical space and break flow. The line-length decision is the most important visual decision.
- **Editorial type pairing: serif for body, monospace or grotesque for chrome**. Serif (Tiempos, Source Serif, Iowan, Charter) for content; monospace (iA Writer Duospace, JetBrains Mono) for metadata, code, and timestamps; grotesque (Söhne, Inter) for navigation only.
- **Modular scale 1.25, capped at 6 sizes**. Body / subhead / head / display / hero (rare) / caption-mono. The modesty of the scale is the school's signal: nothing screams.
- **Generous leading (line-height 1.6–1.8 for body)**. The page must feel like a book, not a screen.
- **Reductive palette: paper-white, ink-black, one accent for hyperlinks/CTAs.** Ink is warm-near-black; paper is warm-near-white; accent is restrained (a calm blue, a forest green, a muted ochre — never a saturated brand color).
- **Asymmetric typographic composition**. The text sits in a single column with one wide outer margin (left or right) where metadata, footnotes, and navigation live. The asymmetry is the navigation.
- **No decorative ornamentation, period.** No dividers (whitespace separates), no cards (typography hierarchies separate), no drop-shadows (the page is paper).

## Prompt DNA

Treat the typography as the interface. Single-column body at exactly 60–75 characters per line measure (use `max-width: 65ch`); pick a serif (Source Serif, Tiempos, Iowan, or Charter) for body and a monospace (JetBrains Mono, iA Writer Duospace) for metadata, code, timestamps. Navigation uses a grotesque (Söhne, Inter) at small size with letter-spacing to register as chrome. Modular scale of 1.25 from a 17px base (slightly larger than 16 — the iA tradition); cap the size ladder at six tiers.

Body line-height 1.7. Generous outer margin on one side (≥120px on desktop) where metadata, footnotes, and reading aids live. Reductive palette: warm paper-white (`#fafaf6`-ish), warm ink-black (`#0a0a0a` to `#141413`), one restrained accent for links/CTAs (calm blue `#0454ab`, forest green `#1a4d3a`, or muted ochre `#9b6829` — never saturated brand colors). Refuse decorative ornament: no cards, no shadows, no borders except where they clarify content (table separators, code-block backgrounds at very-low-opacity neutral). The whitespace separates; the typography hierarchies separate; nothing else needs to.

## Token implications (Flutter)

- **Color**: warm paper-white surface (`#fafaf6`), warm ink-black text (`#0a0a0a` or `#141413`), 1 restrained accent (calm blue / forest green / ochre at desaturated values). `brandDefault` = the link/CTA accent. `bgBase` = paper. `textPrimary` = ink. `bgSurface` = `bgBase` (single tier).
- **Typography**: 3 families — serif for body (`Source Serif Pro`, `Tiempos`, `Iowan` fallback), monospace for metadata (`JetBrains Mono`, `iA Writer Duospace`), grotesque for navigation (`Söhne`, `Inter`). 2 weights per family (400 + 600 for serif; 400 + 500 for mono). Multiplier 1.25, 6-size ladder.
- **Spacing**: editorial, with asymmetry budget. AppSpacing on 8-base; outer margins 120px+ desktop, 24px mobile. line-height 1.7 for body.
- **Radius**: 0–2px. The page does not have rounded corners.
- **Border**: structural — table separators, code-block backgrounds. Never decorative.
- **Motion**: ≤120ms linear. Reading is not animated.
- **Iconography**: linear, 1.5px stroke, geometric. Used sparingly — most affordances are typographic (a hyperlink, an italic).

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★★ | natural fit for reading-first apps: writing tools, document readers, journaling, RSS clients. iA Writer is the canonical example. |
| HTML mockup (Clara) | ★★★ | direct fit — `frontend-design --school information-architects` produces single-column reading layouts that are immediately credible. |
| PPT | ★☆☆ | weak — the school is reading-first; PPT is summary-first. Forcing IA into slides produces overly text-heavy decks (which often look great but exhaust readers). |
| PDF | ★★★ | strongest format — long-form essays, research papers, manifestos. The school's print legacy is fundamental. |
| Infographic | ★☆☆ | weak — IA refuses the data-density that infographics require. Use Müller-Brockmann or Takram. |
| Cover | ★☆☆ | weak — covers need imagery; IA is reading-only. The "Web Trend Map" posters are the exception. |
| AI-image-gen | ★☆☆ | very weak — generative models cannot resist decoration; the school's reading-first ethos is alien to them. Hand-author. |

## Slop traps

- ❌ **Body text wider than 75 characters**. The line-length decision is the school's signature. Wider = illegible.
- ❌ **Adding a sans-serif body "for modernity"**. The school requires serif body for the reading experience; sans body reads as web 2.0 corporate.
- ❌ **Decorative cards / drop-shadows / gradients**. Anti-school.
- ❌ **Multiple accent colors**. One link color, period. If you have success/error/warning, render them in different *type weights* or *italic*, not different colors.
- ❌ **Cramming the outer margin with sidebars**. The asymmetric margin is for ONE thing (metadata or footnotes), not for a navigation sidebar + a related-articles sidebar + a sponsored sidebar.
- ❌ **Insufficient leading**. Tight body line-heights (≤1.5) read as web-corporate, not as reading. The school demands 1.6–1.8.
- ❌ **Font size below 17px for body**. Smaller than that breaks the reading-first promise on standard screens.

## Best paired with

- **Müller-Brockmann** — typography-first complements grid-first; both reduce; both refuse decoration.
- **Pentagram** — Pentagram permits a touch more wit; IA permits a touch more austerity. Compatible if the wit is purely typographic.
- **Kenya Hara** — both are reading-first / quietness-first; Hara permits more empty, IA permits more text.
- **Editorial (Wired/Apple-mag)** — different positions on the same continuum; Editorial allows imagery + chrome that IA refuses.

## Anti-pairs (don't blend)

- **Memphis** — color and pattern violate IA's reductive premise.
- **Sagmeister & Walsh** — expressive type as image is the opposite of IA's "type as service to content".
- **Active Theory / Locomotive** — motion in the reading flow is anti-school.
- **Brutalism** — adjacent on reduction but opposed on intent: Brutalism shows the system; IA serves the content. They can produce visually-similar work for different reasons, but blending muddles both.
