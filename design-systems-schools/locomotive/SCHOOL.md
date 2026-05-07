> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/locomotive/SCHOOL.md`
> **Created:** 2026-05-07

# Locomotive (kinetic-narrative web)

> Category: Kinetic narrative · Scroll-driven storytelling · Awwwards register

## Philosophy nucleus

Scroll is the story; pace it like a film cut.

Locomotive (Montreal-based studio + the eponymous `locomotive-scroll` library that defined a decade of award-site scroll behaviour) treats the scroll position as the narrative timeline. Where Active Theory builds 3D theatre, Locomotive builds 2D filmic scrolling — text reveals itself line-by-line on scroll, images parallax at different speeds, transitions between sections happen *because* the user scrolled to them. The Awwwards consensus on what a "premium portfolio" or "premium product launch" should feel like is largely Locomotive-shaped.

Less expensive than Active Theory (no WebGL required); more accessible (most behaviours degrade to static gracefully); more reproducible (the patterns are now well-documented).

## Core characteristics

- **Smooth scrolling**: scroll lerps to position rather than snapping; gives a momentum-feel. `locomotive-scroll`, `lenis`, `gsap-smoothScroll`.
- **Scroll-revealed text**: each line of body fades in / slides up / scrambles into place as it crosses the viewport threshold. Headlines appear word-by-word.
- **Parallax imagery**: foreground and background scroll at different speeds; images reveal themselves with mask-clip animations.
- **Section transitions on scroll**: pinning sections that animate before unpinning (GSAP ScrollTrigger pin-spacing). Background colors shift between sections.
- **Oversized typography** with kinetic entrance — display sizes ≥120px, often outlined / split into characters / animated letter-by-letter.
- **Dark mode is default**, light mode rare. Black canvas + saturated accent (red, electric blue, hot pink) + white type.
- **Cursor customization**: large custom cursor that morphs near interactive elements. Optional but signature.
- **Pre-loader as choreography**: progress-bar splash that sets the kinetic register from the first frame.

## Prompt DNA

Treat scroll position as the narrative timeline. Implement smooth scrolling via `lenis` or `locomotive-scroll`. Reveal each line of body / each headline word-by-word as it crosses the viewport threshold (use `scroll-timeline` CSS or `IntersectionObserver` + class toggle + CSS transition). Parallax imagery: foreground and background at different scroll speeds. Section transitions via GSAP ScrollTrigger pinning — sections pin and animate internal content before unpinning.

Oversized typography: display ≥120px on desktop, often in stencil / outlined / split-character variants (Druk Wide, GT Cinetype, Apoc, Romie, or Inter Display fallback at 800-weight). Dark canvas (`#0a0a0a` or `#000000`) with one saturated accent (electric red, electric blue, hot pink) and warm-white type (`#fafafa`). Custom cursor (large dot or square that morphs to text on interactive hover). Pre-loader as choreography (progress bar / count-up / kinetic-text animation that sets the register from frame zero).

Refuse static-frame design (every state should arrive choreographed); refuse light-mode-by-default (the school lives in dark); refuse instant-snap scrolling (the smoothness IS the school); refuse SaaS-template visual moves. Always provide a `prefers-reduced-motion` static fallback.

## Token implications (Flutter)

- **Color**: dark-native — `#0a0a0a` or `#000000` surface; warm-white text (`#fafafa`); 1 saturated accent (electric red `#ff2244`, electric blue `#0044ff`, hot pink `#ff0080`). `brandDefault` = the accent. `bgBase` = the dark. `textPrimary` = warm-white.
- **Typography**: 1 display family (Druk Wide, GT Cinetype, Apoc, Romie, Inter Display fallback) + 1 functional sans (Inter, Söhne) for body. Display 800-weight at 120px+ desktop. Multiplier 1.5 for display jumps; 1.25 for body. Tight line-height on display (1.0–1.1).
- **Spacing**: cinematic. AppSpacing generous (8 / 16 / 32 / 64 / 128); but motion timing is co-equal with spacing for layout rhythm.
- **Radius**: 0px on UI; soft (8–16px) on photographic frames; pill (9999px) on CTA buttons (single exception).
- **Border**: rare; LED-glow 1–2px in saturated accent for interactive surfaces.
- **Motion**: signature — `flutter_animate` + Rive territory. Curves: `easeOutQuart` for entrances, `easeInQuart` for exits, springs for hover micro-moments. Durations 400–1200ms for hero / scroll-reveal; 150–250ms for hover.
- **Iconography**: linear, 2px stroke, monochromatic in accent or warm-white.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★★ | strong for portfolio-style / product-launch / premium-brand mobile-and-web apps. `theme-motion` skill is the natural pair; `flutter_animate` covers most behaviours. |
| HTML mockup (Clara) | ★★☆ | medium — Clara emits static; the school evaluates on motion. Mock the static states; spec the motion in caption. |
| PPT | ★☆☆ | weak — PPT motion is rudimentary; export a video of the live site for a keynote slide instead. |
| PDF | ★☆☆ | weak — PDF is static. Hero-frame screenshots with caption-described-motion. |
| Infographic | ★☆☆ | weak — infographic reading is static-page; the school is scroll-narrative. |
| Cover | ★★☆ | viable for portfolio-cover stills (a hero frame freeze); not for product covers. |
| AI-image-gen | ★★☆ | medium — generative video models capture the register. Generative stills (Midjourney with cinematic prompts) less so. |

## Slop traps

- ❌ **Skipping smooth scroll**. The lerped-momentum scroll IS the school's signature; native browser scroll feels off-school.
- ❌ **Light-mode-by-default**. The school lives in dark mode.
- ❌ **Instant text reveals**. Each line/word should arrive on scroll; instant reveals lose the kinetic register.
- ❌ **Forgetting `prefers-reduced-motion`**. The only ethical concession; skipping it is a failure.
- ❌ **Linear easing**. The school's signature curves are eased (cubic, quart, sometimes quint).
- ❌ **Skeleton-screen loaders**. The pre-loader IS the choreography.
- ❌ **Muted "professional" accent**. The accent is electric / saturated; muted accent reads as Editorial or Pentagram.
- ❌ **Symmetric, balanced compositions**. The school is asymmetric and kinetic.

## Best paired with

- **Active Theory** — same kinetic-narrative DNA; Active Theory more 3D, Locomotive more 2D-filmic. Compatible.
- **Sagmeister & Walsh** — emotional + kinetic = theatrical events; brand-launch territory.
- **Memphis** — kinetic Memphis pattern is festival-launch-site territory.

## Anti-pairs (don't blend)

- **Müller-Brockmann** — kinetic motion is anti-grid.
- **Information Architects** — reading-first violates scroll-as-narrative.
- **Kenya Hara** — meditative pacing violates cinematic timing.
- **Brutalism** — refuses polish; Locomotive IS polish-as-narrative.
- **Editorial** — magazine reading-pacing differs from filmic scroll-pacing; the schools are positions on opposite ends of "what scrolling means".
