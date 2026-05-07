> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/muller-brockmann/SCHOOL.md`
> **Created:** 2026-05-07

# Müller-Brockmann (Swiss grid)

> Category: Information-architecture · Modernist minimalism

## Philosophy nucleus

Order is communication — the grid is not decoration; it is the medium that makes information visible.

Müller-Brockmann's 1981 *Grid Systems* taught a generation that the grid is not a tool for efficiency or restraint; it is the *carrier* of meaning. The columns are not a guide the designer obeys; they are the language the reader decodes. Reduce, align, reduce again — until what remains is information unmediated by ornament. A page that reads itself.

## Core characteristics

- **Grid as the visible structure**, not the hidden one. Compose every section on a strict 8-column or 12-column grid the user can sense even when the lines aren't drawn. Margins, gutters, baseline-alignment all derive from one mathematical rule. Show the columns explicitly when teaching ("here's why the alignment works") — hide them in production but never break them.
- **Two type weights, period.** Helvetica or Akzidenz-Grotesk at regular (400) and bold (700). No italic for emphasis (rotated text breaks the grid); no serifs (foreign register); no light/300 weight (anemic on screen); no extra-bold/900 (1960s typewriter brutalism, different school). Inter is an acceptable modern fallback — Helvetica's geometry without licensing fees.
- **Modular type scale of 1.25**. Sizes locked to a single multiplier from a 16px base. Five sizes maximum: caption (12.8) / body (16) / subhead (20) / head (25) / display (31.25). Sometimes a sixth (39, hero only). More than six sizes = scale violation.
- **Reductive palette: one accent at full saturation**, used at most twice per screen. Neutrals dominate ≥80% of pixels — pure or warm-near-white, warm-near-black (e.g. `#0a0a0a`), one mid-gray. Accent is primary red (`#e30613`-leaning), primary blue (`#005bbb`-leaning), or rarely yellow (`#ffcc00`).
- **Asymmetric balance**. The grid permits asymmetry; the eye composes weight via mass, not centering. A red square in the top-left counter-balances four columns of body in the bottom-right. Never center body text "to be safe" — the grid carries hierarchy.
- **No decoration**. No drop-shadows, no gradients, no rounded corners >4px, no glassmorphism, no skeuomorphic effects, no purely-decorative borders. Borders exist only when structural (separating columns, marking sections, framing data tables). Depth comes from the grid's mathematics, never from chrome.
- **Photography is documentary**, not lifestyle. Black-and-white preferred; if color, full-bleed without overlay text-on-image. Photos are content, not background.

## Prompt DNA

Communicate through the grid. Compose every section on a strict 8-column or 12-column grid the user can sense even if they cannot see it. Use exactly two type weights — regular and bold — at sizes that follow a 1.25 multiplier from a 16px base, capped at five sizes. Reduce the palette to neutrals (warm-near-white, warm-near-black, one mid-gray) plus one chromatic accent at 100% saturation, used at most twice per screen. The accent is primary red, primary blue, or yellow — never both two of those, never tints of the brand color.

Refuse decorative ornament: borders only when structural; drop-shadows never; gradients never; rounded corners ≤4px or sharp; italic only for foreign words and book titles, not for emphasis. The composition IS the design; the chrome is silence. Asymmetry is welcome when it expresses content hierarchy — but every element must align to a column. Photography is documentary, full-bleed, never with text overlay. When in doubt, remove rather than refine. The reader should feel the grid before they read the words.

## Token implications (Flutter)

- **Color**: 1 saturated accent (primary red `#e30613`-leaning OR primary blue `#005bbb`-leaning OR yellow `#ffcc00`); 1 mid-gray (`#7a7a7a`); warm-near-white surface (`#fafaf7`); warm-near-black text (`#0a0a0a`). `brandDefault` = the accent. `textPrimary` = near-black. `bgBase` = warm-white. `bgSurface` = `bgBase` (single surface tier; the school discourages elevation hierarchy beyond background/foreground).
- **Typography**: Helvetica, Akzidenz-Grotesk, or Inter as fallback. 2 weights only (400 + 700). Multiplier 1.25, 5-size ladder. line-height 1.4 for body; 1.1 for display; 1.5 for long-form reading.
- **Spacing**: 8-column grid → all spacing on multiples of 8. AppSpacing ladder = 8 / 16 / 24 / 32 / 48 / 64 / 96. No half-units (4px), no 12px, no 18px. The whole layout breathes on a single base unit.
- **Radius**: minimal. AppRadius.sm = 0–2px max. AppRadius.md = 4px (rare). Most surfaces are sharp-cornered. Circles for avatars only.
- **Border**: structural only. `borderDefault` = mid-gray at 30% opacity (subtle column dividers); `borderStrong` = the same mid-gray solid (data-table separators). No 1px hairlines for purely-decorative panels.
- **Motion**: discouraged. If present, ≤120ms linear ease — the grid does not animate. No spring curves; springs are signature of a different school (Active Theory).
- **Iconography**: minimal stroke at 1.5–2px, no fills, no rounded line caps, geometric forms (circles + squares + lines, no hand-drawn shapes).

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★☆ | viable but the school's grid discipline is more legible in HTML where columns are easier to expose. Use `theme-port --from-html` after Clara emits the structure. Pure-Flutter implementations tend to lose the grid feeling once `Container`s nest. |
| HTML mockup (Clara) | ★★★ | direct fit — `frontend-design --school muller-brockmann` produces grid-locked layouts naturally because CSS Grid + the column-counted classes are the natural medium. |
| PPT | ★★★ | use HTML as source → Marp or Slidev with the school's CSS as theme. Annual reports / academic decks / corporate communications flourish here — the school was *invented* for the printed annual report. |
| PDF | ★★★ | use HTML → Pandoc, Typst, or Prince with grid-locked layout. The school's print legacy is fundamental — Müller-Brockmann himself worked PDF-equivalent (offset litho) end of career. |
| Infographic | ★★★ | data-explanation work shines: HTML → static export to PNG/SVG. Tufte-aligned. The grid carries data hierarchy with zero visual noise — exactly what a good chart needs. |
| Cover | ★★☆ | grid-strong but less imagery-driven than Memphis or Sagmeister. Works for editorial covers (book / magazine / monograph), weak for product/lifestyle covers where photography needs to dominate. |
| AI-image-gen | ★☆☆ | weak — Midjourney/SDXL produce decorative output that violates the school's reduction principle. Even with explicit prompts ("no decoration, no gradients, only one red accent"), generative models default to ornament. Don't bother — author by hand. |

## Slop traps

- ❌ **Adding "modern" decorative gradients, glassmorphism, soft drop-shadows for "depth".** The school refuses to fake dimensionality; gradients are the most-violated rule when implementations drift toward "but it looked too plain".
- ❌ **Using more than one chromatic accent.** Two saturated colors instantly break the school. If you need success/error/warning, render them in the same accent value-shifted (e.g. red for danger, dark-red for warning) — never green + red + amber together.
- ❌ **Rounding corners >4px** — soft corners read as 2010s SaaS, not 1960s Swiss. Even on photos, sharp corners.
- ❌ **More than two type weights** — adding a 300/light or italic immediately reads as marketing-template. If something needs emphasis beyond bold, it shouldn't exist (cut copy until bold suffices).
- ❌ **Centering everything for safety.** The grid permits asymmetry; centering all body for visual comfort is a different school (Information Architects, where text is the figure). Müller-Brockmann demands the column you commit to.
- ❌ **Decorative borders, hairlines, "dividers"**. Borders only when they separate two distinct content zones; never to make a card "feel like a card".
- ❌ **Lifestyle/people photography with text overlaid**. Photos run full-bleed without copy on top — text lives in the next column, not over the image.

## Best paired with

- **Pentagram** (similar typography discipline; can blend in v1.6+ — Pentagram adds editorial wit on top of the grid without violating it).
- **Information Architects** (typography-first complements grid-first; the two schools share neutrals discipline and reductive accent).
- **Kenya Hara** (negative-space first; both reduce, but Hara permits emptiness as content while Müller-Brockmann mandates the grid as content). Compatible because both refuse decoration.
- **Editorial** (Wired-style magazine pacing) — when the grid hosts long-form reading rather than a dashboard, Editorial provides the typographic moves Müller-Brockmann is austere about.

## Anti-pairs (don't blend)

- **Memphis** — postmodern playfulness directly contradicts the school's reduction; blending produces Memphis-with-guilt: neither playful nor disciplined.
- **Active Theory / Locomotive** — kinetic effects are anti-grid; the eye reads motion before composition, breaking the school's first promise.
- **Sagmeister & Walsh** — expressive type-as-image violates the "two weights, period" rule. Sagmeister wants type to *be* the image; Müller-Brockmann wants type to be the *carrier* of the image.
- **Brutalism** — adjacent but distinct: Brutalism shares the no-decoration ethos but refuses the grid's mathematical perfection. They can be compatible in spirit but produce visually opposed work.
