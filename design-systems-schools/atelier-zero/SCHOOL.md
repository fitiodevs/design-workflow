> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [open-design](https://github.com/nexu-io/open-design) hand-curated entry (Apache-2.0); not 3rd-party derivation
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/atelier-zero/SCHOOL.md`
> **Created:** 2026-05-07

# Atelier Zero (collage-editorial)

> Category: Editorial · Studio · Collage-paper canvas

## Philosophy nucleus

Paper has memory; design lives in the marks of process — torn edges, plaster dust, marker scribbles, Roman numerals.

Atelier Zero is open-design's hand-curated school: a collage-editorial register that imagines the page as a sketchbook spread or a curated studio wall. Where the Editorial school is *magazine* register, Atelier Zero is *atelier* register — the room where the magazine is being designed. Visible craft: torn paper edges, plaster textures, photographed Roman-numeral markers, hand-marker annotations layered over typed body. The work has the texture of a designer's process board photographed for a monograph.

The school is distinct enough from huashu's 20 to merit inclusion: no other school in the library captures the *studio-wall-aesthetic* — at the intersection of editorial discipline (typography, hierarchy) and collage assembly (textures, found materials).

## Core characteristics

- **Paper canvas with material texture**: the background is off-white *paper* with subtle grain (a Photoshop-paper-grain layer or a CSS noise filter at low opacity). Never pure white digital surface; never pure flat color.
- **Torn-edge / cut-out compositional elements**: photographed paper torn at the edge, used as section dividers; magazine cut-outs serving as imagery; tape strips on top of layered elements.
- **Mixed display typography**: oversized Roman serif (Caslon, Garamond, Bodoni — heritage typefaces) intercut with hand-rendered marker writing or condensed sans for chrome.
- **Italic-mixed sentences**: bodies of text mix italic and roman intentionally (an italic word inside a roman sentence, or vice versa), echoing handwritten emphasis on paper.
- **Roman-numeral section markers**: I / II / III set in oversized serif at section heads. Pagination uses Roman numerals.
- **Plaster / pigment texture imagery**: photographs of clay, plaster, paint, raw fabric — material-poetic; not lifestyle.
- **Generous outer margins** with handwritten-style marginalia (italic hand-script font) — annotations as content.
- **Color: paper-cream + warm-near-black + 1–2 pigment hues**: terra-cotta, indigo, ochre — historic-pigment tones, not modern brand colors.

## Prompt DNA

Compose the page as a designer's studio wall photographed for a monograph. Background is *paper* — off-white (`#fbf8ee`, `#f7f1de` — warm cream tones) with subtle paper-grain (CSS noise filter at very-low opacity, or a tileable subtle texture image). Never pure white; never pure flat color.

Mixed display typography: heritage Roman serif (Caslon, Garamond, Bodoni; Cardo or EB Garamond as web fallbacks) at oversized sizes (≥80px desktop) for headlines and Roman-numeral section markers (I, II, III). Body text in serif with deliberate italic-mixed sentences. Hand-rendered marker writing (Caveat, Permanent Marker, or hand-drawn SVG) for marginalia and annotations in outer margin. Condensed sans (Söhne Condensed, Inter Tight) for chrome only.

Compositional elements include torn-paper edges (SVG masks of torn paper), magazine cut-outs (irregular-edged photographs), tape strips (small photographic SVG of masking tape) layered over content. Imagery is *material* — photographed plaster, clay, raw pigment, fabric, ink-on-paper — never lifestyle stock.

Color palette: paper-cream surface, warm-near-black ink, 1–2 historic pigment hues (terra-cotta `#a0552a`, indigo `#3d4d6b`, ochre `#9b6829`, raw umber `#5b4636`). Refuse modern brand colors (no electric blue, no neon pink); refuse digital-flat backgrounds; refuse decoration that doesn't reference physical material craft.

## Token implications (Flutter)

- **Color**: paper-cream surface (`#fbf8ee` or `#f7f1de` — choose the warmer side), warm-near-black ink (`#1a1612` to give the ink a brown cast, not blue-black), 1–2 historic pigments (terra-cotta `#a0552a`, indigo `#3d4d6b`, ochre `#9b6829`). `brandDefault` = the primary pigment. `bgBase` = paper-cream. `textPrimary` = warm-near-black. `bgSurface` = `bgBase` (single tier; differentiation via texture, not background-tone).
- **Typography**: 3 families — heritage serif (`Cardo`, `EB Garamond`, `Caslon` fallback) for display + body; hand-script (`Caveat`, `Permanent Marker`, `Architects Daughter`) for marginalia; condensed sans (`Söhne Condensed`, `Inter Tight`) for chrome. Italic permitted and welcomed. Multiplier 1.5 for display jumps; 1.25 for body. Roman-numeral section markers at hero size (≥120px).
- **Spacing**: editorial with generous handwritten-margin allowance. AppSpacing generous; outer margins ≥120px desktop for marginalia.
- **Radius**: irregular — torn-paper edges (clip-path) on photographic frames; sharp on type containers; pill on rare CTA buttons.
- **Border**: rare; when present, hairline in pigment color, often deliberately offset (the tape-strip register).
- **Motion**: ≤300ms eased; gentle. Page transitions favor crossfade with subtle horizontal-shift (paper-page-turn register).
- **Iconography**: hand-drawn or referenced from heritage prints (vintage etchings, woodcut). If SVG, irregular line-weight to suggest handcraft.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★☆ | viable for arts / craft / heritage / boutique-brand apps; weaker for productivity (the texture/craft register fatigues at app density). |
| HTML mockup (Clara) | ★★★ | direct fit — `frontend-design --school atelier-zero` produces collage-editorial layouts; CSS noise filters + clip-path for torn edges. |
| PPT | ★★★ | strong for monograph / studio-portfolio / cultural-org / heritage-institution decks. |
| PDF | ★★★ | art books, exhibition catalogs, monographs — the school's natural medium. Pair with Pandoc/Typst with paper-textured layout. |
| Infographic | ★★☆ | viable for art-org / heritage-data infographics; weak for tech / corporate data. |
| Cover | ★★★ | book covers, exhibition catalogs, magazine special editions, music covers (vinyl reissues especially). |
| AI-image-gen | ★★☆ | medium — generative models can produce paper / plaster textures and pigment palettes; pair with hand-edit pass for the typography overlay. |

## Slop traps

- ❌ **Pure white digital background.** The school requires paper-cream with material texture.
- ❌ **Modern brand colors** (electric blue, neon pink). The pigment palette is heritage-restricted.
- ❌ **Sans-serif body** (other than chrome). The school is serif-led.
- ❌ **Lifestyle photography** (people smiling at laptops). Material-photography only.
- ❌ **Symmetric, "clean" layouts**. The school is studio-wall messy-on-purpose; symmetric reads as corporate.
- ❌ **Forgetting the marginalia / handwriting layer**. Without the hand-script annotations, the school reads as Editorial-without-personality.
- ❌ **Drop-shadows for "depth"**. The school's depth is in *texture* (paper grain, torn edges, layered elements), not in chrome.

## Best paired with

- **Editorial (Wired/Apple-mag)** — adjacent on the typographic axis; Editorial is the publication register, Atelier Zero the studio register.
- **Kenya Hara** — quietness + craft heritage shared.
- **Müller-Brockmann** — when the studio wall hosts disciplined data-essays beneath the collage; the grid lives underneath the texture.
- **Pentagram** — Pentagram's editorial wit can survive the studio register; both treat type with reverence.

## Anti-pairs (don't blend)

- **Active Theory / Locomotive** — kinetic motion violates the static-paper register.
- **Brutalism** — system-default refuses craft; atelier-zero IS craft.
- **Memphis** — postmodern-color violates the heritage-pigment palette.
- **Sagmeister & Walsh** — adjacent on craft, but Sagmeister is *more* theatrical, atelier-zero is *more* contemplative; blending muddles both.
