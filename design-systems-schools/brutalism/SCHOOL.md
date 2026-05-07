> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/brutalism/SCHOOL.md`
> **Created:** 2026-05-07

# Brutalism (web brutalist)

> Category: Anti-school · Raw default · Honest material

## Philosophy nucleus

Show the building's concrete; the design polish was the lie.

Web Brutalism (the 2014–present movement, exemplified by sites like brutalist-websites.com, balenciaga.com circa 2020, Hassan Rahim's portfolio, the original Drudge Report) treats the polished SaaS template as a corporate fiction. The school's premise is honest: the browser ships with system fonts, sharp default form controls, blue underlined links. *That's the truth*. Every layer of "design" applied on top is a softening — a beige Helvetica veneer over a raw structure. Brutalism strips the veneer and shows the concrete.

The result is functional, fast, weirdly memorable, and politically anti-corporate. It rejects the seamless gradient gloss in favor of the system-font-stack look-of-a-1996-personal-site, deliberately.

## Core characteristics

- **System font stack as the typeface**. `font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` — whatever the user's OS provides. Or monospace (Courier, Menlo) for a more typewriter register. Never web-loaded fonts.
- **Default browser form controls**. Sharp-cornered inputs, blue-square checkboxes, OS-native scrollbars. The school refuses to style these.
- **Asymmetric, unjustified layouts**. Text aligned left only; ragged right edges; no centering for safety. Blocks of content sit where they sit; the eye works.
- **Hex-extreme palette**: pure white `#ffffff` + pure black `#000000` + one saturated default color (link blue `#0000ee`, danger red `#ff0000`, system-yellow `#ffff00`). No tint variations.
- **No transitions, no animations, no easing**. Click happens instantly. Hover changes the underline. That's the entire interaction vocabulary.
- **Borders are 1px solid black**, drawn to communicate structure (table cells, form fieldsets) — not for decoration.
- **Typography is functional**, not expressive. One face, two sizes (body + heading), 700 for emphasis.
- **Imagery is unedited**: stock-grade JPEGs at full resolution, sometimes pixelated by intent. No filters, no overlays.

## Prompt DNA

Build as if it's 1998 and the design industry hasn't invented "design polish" yet. Use the system font stack — never web-loaded fonts. Default browser form controls (sharp inputs, blue checkboxes, native scrollbars). Asymmetric, left-aligned, ragged-right layouts; nothing centered for visual safety. Palette is extreme: pure white background, pure black text, one saturated default color for links and danger states (link-blue `#0000ee` or system-red `#ff0000`).

No transitions, no animations, no eased hover effects — click happens instantly; hover changes the link underline; that's the entire interaction vocabulary. Borders are 1px solid black where they communicate structure (form fields, table cells) and absent everywhere else. Typography is functional: one font (system stack OR monospace), two sizes (body 16px and heading 24–32px), 700-weight for emphasis only. Imagery is unedited and full-fidelity — no tinted overlays, no rounded corners, no filters. Refuse drop-shadows, gradients, glassmorphism, rounded corners >0px, marketing-template visual moves. Every "design move" is a softening; show the structure raw.

## Token implications (Flutter)

- **Color**: pure white surface (`#ffffff`); pure black text (`#000000`); 1 saturated link/danger color (link `#0000ee` OR red `#ff0000`). `brandDefault` = the saturated. `bgBase` = `#ffffff`. `textPrimary` = `#000000`. No tint variations; no `bgSurface` differentiation.
- **Typography**: system-ui stack OR Courier/Menlo monospace. 1 family. 2 sizes (body 16, heading 28). 2 weights (400 + 700). line-height 1.4.
- **Spacing**: rectangular and unconcerned with rhythm. AppSpacing tier irregular by intent: 4 / 8 / 16 / 32. The school does not respect modular scales.
- **Radius**: 0px on EVERYTHING. Sharp corners everywhere — buttons, inputs, cards (if any), avatars (squares).
- **Border**: 1px solid `#000000`, structural only. No decorative borders, no hairlines.
- **Motion**: NONE. transition: none everywhere. The school refuses easing.
- **Iconography**: text or system Unicode symbols (←→✓✗) where possible. If SVG, monochrome 2px stroke, 0px radius caps.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★★ | strong fit for opinionated tool apps (a Vim-spirit text editor, a developer-utility, a privacy-respecting service). Refuses Material Design's softness; users self-select. |
| HTML mockup (Clara) | ★★★ | the school was *born* on HTML. `frontend-design --school brutalism` produces immediately credible 1996-respect output. |
| PPT | ★☆☆ | weak — PPT's medium fights brutalism (slides imply rehearsal; the school is anti-rehearsed). Possible for confrontational/manifesto decks. |
| PDF | ★☆☆ | weak — PDF reading expects polish. Possible for zines, manifestos, academic papers in CS theory tradition (the LaTeX aesthetic is brutalism-adjacent). |
| Infographic | ★☆☆ | weak — infographics need data hierarchy; brutalism refuses hierarchy. |
| Cover | ★★☆ | works for art-book / academic-zine / counter-culture covers; weak for commercial product covers. |
| AI-image-gen | ★★☆ | medium — Midjourney can produce "raw" imagery (unedited textures, unfiltered photos); pair with Stable Diffusion XL for fidelity over polish. |

## Slop traps

- ❌ **Adding a custom font**. Defeats the point — the school requires the system stack.
- ❌ **Soft drop-shadow "to make it pop"**. The pop IS the rawness; softening kills it.
- ❌ **Rounded corners** anywhere. 0px on everything. Soft = corporate = anti-school.
- ❌ **Pastel colors** for "calm". The palette is hex-extreme; pastels betray the school.
- ❌ **Animated transitions** "for polish". Polish IS the lie.
- ❌ **Centered everything for safety**. Brutalism is asymmetric; centering everything is corporate-template.
- ❌ **Marketing-template visual moves** — three feature columns, hero with gradient, "trusted by [logo grid]". Brutalism refuses these.
- ❌ **Tinted variations of the saturated color** ("primary 90", "primary 50"). The school uses ONE saturated value.

## Best paired with

- **Information Architects** — adjacent reduction; both refuse decoration but for different reasons (IA serves the content; Brutalism shows the system). Compatible if the work is reading-heavy.
- **Müller-Brockmann** — both refuse decoration; the grid is foreign to brutalism but the discipline is shared. Compatible only when brutalism is being deliberately disciplined.

## Anti-pairs (don't blend)

- **Memphis** — color-bold pattern is the polish brutalism rejects.
- **Sagmeister & Walsh** — expressive type-as-image is the polish brutalism rejects.
- **Pentagram** — Pentagram is *all* polish (the polish that survived skeptical review); brutalism refuses the review.
- **Active Theory / Locomotive** — kinetic motion is the polish brutalism rejects.
- **Editorial (Wired/Apple-mag)** — magazine register is exactly what brutalism is anti.
- **Kenya Hara** — both reduce, but Hara reduces TO craft; brutalism reduces FROM polish. They contradict at intent.
