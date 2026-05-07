> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/editorial/SCHOOL.md`
> **Created:** 2026-05-07

# Editorial (Wired / Apple-mag)

> Category: Magazine pacing · Long-form respect · Mixed-register typography

## Philosophy nucleus

The page is a magazine spread; the reader is here to read, and the design should pace the reading like a great editor.

The editorial school descends from the great print magazines (*Wired*, *The New Yorker*, *Apple's Newsroom*, *Bloomberg Businessweek*, *The Atlantic*, *MIT Technology Review*) translated to web. It assumes long-form content with imagery, pull-quotes, captions, marginalia, and asymmetric pacing. Every section is a visual paragraph; every spread breathes. The reader scrolls; the page rewards scrolling with intentional pacing — moments of visual quiet, moments of scale change, moments where typography becomes image.

Distinct from Information Architects: editorial *welcomes* imagery, captions, pull-quotes, marginalia; IA reduces to text-only. Distinct from Pentagram: editorial is the *magazine instance*, Pentagram the *corporate-identity instance* of the same shared vocabulary.

## Core characteristics

- **Mixed-register typography**: serif for body (Mercury, Tiempos, Lyon, Source Serif), grotesque for chrome (Söhne, Inter, Untitled Sans), monospace for metadata/captions (JetBrains Mono, Roboto Mono). Three families, used by *role*, not contrast.
- **Pull-quotes break the column**: oversized italic-bold quotes set across two columns, often with bracket / em-dash typographic ornamentation. Pull-quotes are the school's signature.
- **Drop caps**: the first letter of an article is set 3–5x body size, often in serif italic. Optional but signature.
- **Generous full-bleed photography** with captions in monospace sans below. Caption typography is restrained and authored — never lifestyle stock.
- **Asymmetric column breaks**: a section may use a single column at 65ch; the next a two-column with image; the next a wide hero with caption. Pacing is rhythmic, not consistent.
- **Marginalia**: footnotes, side-notes, link-attribution in the outer margin. Tufte-influenced when academic; Wired-influenced when magazine.
- **Reduced palette with 1 editorial accent**: warm-near-white paper, near-black ink, one chromatic accent (signature magazine red, navy, ochre — never saturated brand colors).

## Prompt DNA

Compose like a magazine editor pacing a 4,000-word feature article. Mixed-register typography: serif (Mercury, Tiempos, Lyon, Source Serif) for body; grotesque (Söhne, Untitled Sans, Inter) for chrome; monospace (JetBrains Mono) for metadata and captions. Three families, used by role, not for design contrast.

Long-form body sets in a single column at 65–72ch measure. Pull-quotes break the column — set in italic display serif at 2–3x body size, sometimes spanning two columns, sometimes with em-dash/bracket ornamentation. Drop cap on the first letter of the article (3–5x body size, serif italic). Photography is full-bleed and authored (never lifestyle stock); captions in monospace sans below. Asymmetric column breaks: single column → two-column with image → wide hero, rhythmically. Marginalia: footnotes and link-attribution live in the outer margin (≥120px wide on desktop).

Reduced palette: warm-near-white paper (`#fafaf6`), warm-near-black ink, one editorial accent (Wired-red `#d00b1d`, navy `#1a3a5c`, ochre `#9b6829`). Refuse decorative ornament beyond the editorial vocabulary (drop caps, pull-quotes, captions are *content* ornament, not chrome ornament). Refuse SaaS-template visual moves (three feature columns, "trusted by" logo grids, gradient hero sections — anti-school).

## Token implications (Flutter)

- **Color**: warm paper (`#fafaf6`) surface, warm ink-black text (`#0a0a0a`), 1 editorial accent (Wired-red `#d00b1d`, navy `#1a3a5c`, ochre `#9b6829`, or forest `#1a4d3a`). `brandDefault` = the accent. `bgBase` = paper. `textPrimary` = ink. `bgSurface` = `bgBase` (single tier; differentiation via typographic hierarchy not background).
- **Typography**: 3 families — serif (`Source Serif Pro`, `Tiempos`, `Mercury` fallback), grotesque (`Söhne`, `Untitled Sans`, `Inter`), monospace (`JetBrains Mono`). 2 weights per family + italic on serif. Multiplier 1.333 (editorial step). 7-size ladder including drop-cap and pull-quote special tiers.
- **Spacing**: editorial. AppSpacing on 8-base, generous outer margins. line-height 1.7 body, 1.4 captions, 1.2 display.
- **Radius**: 0–4px. The page is sharp.
- **Border**: structural (table separators, code-block backgrounds, rule-lines under captions). Hairline at low-opacity warm-gray.
- **Motion**: ≤200ms eased; reading is gently animated, never theatrical. Page transitions favor crossfade.
- **Iconography**: linear, 1.5px stroke. Used sparingly — most affordances are typographic.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★☆ | viable for reader / news / journal apps; weaker for productivity. The school's column/pacing translates to mobile via single-column scroll. |
| HTML mockup (Clara) | ★★★ | direct fit — the school is the natural HTML medium. `frontend-design --school editorial` produces magazine-paced layouts. |
| PPT | ★★★ | strong for keynote-as-essay decks (TED-style talks where the deck is essay). Use HTML→Marp/Slidev with editorial CSS. |
| PDF | ★★★ | strongest format — long-form articles, white papers, monographs. The school's print legacy is fundamental. |
| Infographic | ★★★ | strong for data-essay infographics (a multi-page Bloomberg-style data feature). Tufte + editorial pacing combine. |
| Cover | ★★★ | magazine covers ARE the school. Book covers, special-issue covers, conference covers. |
| AI-image-gen | ★★☆ | medium — generative imagery for magazine illustrations works well; the school welcomes authored imagery. |

## Slop traps

- ❌ **Single-family typography** — the school requires the three-register pairing.
- ❌ **Pull-quotes set in body weight without typographic distinction**. The pull-quote is the school's signature; treat it like one.
- ❌ **Stock lifestyle photography**. The school requires authored or documentary imagery.
- ❌ **Centered hero sections with three feature columns**. SaaS-template; anti-school.
- ❌ **Gradient backgrounds** for "magazine glow". Magazine paper is matte; mimic that.
- ❌ **Tight body line-height (≤1.5)**. The school is reading-first; leading must be 1.6+.
- ❌ **Saturated brand colors** for the editorial accent. The accent is restrained — magazine-red is dirty (`#d00b1d`), not saturated (`#ff0000`). The hue's serif-friendly cast is the choice.

## Best paired with

- **Information Architects** — IA is the austere instance, Editorial the magazine instance. Compatible.
- **Pentagram** — editorial vocabulary shared; Pentagram permits more wit, Editorial more long-form pacing.
- **Müller-Brockmann** — when the editorial layout uses the grid as the underlying structure (annual report register).
- **Kenya Hara** — quiet editorial subset (Apple-mag direction).

## Anti-pairs (don't blend)

- **Memphis** — postmodern energy violates editorial pacing.
- **Sagmeister & Walsh** — theatrical type-as-image violates the magazine register (though Sagmeister sometimes does *work for* magazines, the schools are distinct positions).
- **Active Theory / Locomotive** — kinetic motion violates reading pacing.
- **Brutalism** — refuses the polish editorial requires.
