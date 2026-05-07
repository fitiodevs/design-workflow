> **Source:** authored from scratch under Apache-2.0 by design-workflow contributors
> **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only — not forked, only structural idea)
> **License:** Apache-2.0
> **Local path:** `design-systems-schools/active-theory/SCHOOL.md`
> **Created:** 2026-05-07

# Active Theory (kinetic)

> Category: Kinetic · Three-dimensional · WebGL-poetic

## Philosophy nucleus

The screen is a stage; everything that arrives must arrive choreographed.

Active Theory (LA-based digital studio, behind Beats by Dre, Google Doodles, brand-launch sites for HBO, NBA, etc.) treats the browser as a 3D theatre. Every element has an entrance, a behaviour, an exit. Scrolling triggers choreographed sequences. Typography rotates, scales, breaks apart and reforms in WebGL. The school's heart is *cinematic timing* — frames-per-second matter, easing curves are arguments, the hero animation is the pitch.

The work is technically expensive, almost always anti-accessibility (motion-disabled users get a vastly degraded experience), and reserved for sites whose budgets justify the production.

## Core characteristics

- **3D / WebGL-driven hero scenes**: a rotating product, a particle field reacting to mouse, an animated typeface where each letter has its own physics. Three.js, GSAP, custom shaders.
- **Scroll-driven choreography**: scrolling is not page advancement; it's playhead-scrubbing through a cinematic sequence. Pin-and-animate, parallax-as-narrative, scroll-mapped camera moves.
- **Type-in-motion**: letterforms that appear, scatter, reform, leave. The typography is the animated subject, not a label on the animation.
- **Asymmetric kinetic compositions**: no element settles; everything is in motion or just-arrived. Static frames feel wrong.
- **Color-saturated cinematic palette**: hero color + secondary at full saturation, plus pure black for the cinematic-stage register. Light-mode work is rare; the school lives in dark mode.
- **Photography is rare; rendered 3D objects dominate**. When photography appears, it's video — looping, color-graded, treated as motion footage.
- **Sound-design optional but present**: subtle whooshes, clicks, ambient pad. The site has audio identity.
- **Loading states are part of the show**: skeleton screens are anti-school; the loader IS the entrance choreography.

## Prompt DNA

Treat the browser as a 3D theatre. Build the hero as a WebGL scene (Three.js, react-three-fiber, GSAP-animated) where one product / typographic moment / particle field is the stage. Scroll triggers choreographed sequences via ScrollTrigger or Lenis-smooth-scroll: scrolling is playhead-scrubbing, not page advancement. Type-in-motion: letterforms appear, scatter, reform; typography is the animated subject not a label.

Asymmetric kinetic compositions; nothing settles. Color-saturated cinematic palette (electric blue + magenta + black; or hot orange + acid green + black; or a single chromatic ID + black). Dark mode is default; light mode is exceptional. Photography is video — looping, color-graded, treated as motion footage. Loading states ARE the entrance choreography (no skeleton screens). Optional sound-design. Refuse static-frame design (every state has motion); refuse muted "professional" palettes (the school is theatrical); refuse template-marketing visual moves (the school competes with Pixar trailers, not Drift email templates).

Always provide a `prefers-reduced-motion` static fallback — the school is anti-accessibility by default and respecting the OS setting is the only ethical concession.

## Token implications (Flutter)

- **Color**: 1–2 saturated hero colors + pure black (`#000000`) for the cinematic stage. `brandDefault` = the hero. `bgBase` = `#000000` (dark-native by default). `bgSurface` = barely-lighter (`#0a0a0a`). `textPrimary` = warm-white or off-white (`#fafafa`). Light-mode rare.
- **Typography**: 1 display family (Druk Wide, GT Cinetype, Apoc, or Inter Display fallback) at oversized sizes (≥80px hero); 1 functional sans for body. Multiplier 1.5+ for display jumps. line-height 1.0 for hero (tight cinematic).
- **Spacing**: variable, cinematic. AppSpacing scales generous (8 / 16 / 32 / 64 / 128) but motion timing is the primary "spacing" — inter-element rhythm is temporal, not spatial.
- **Radius**: 0–4px on UI; sphere/cylinder/extruded geometry on 3D scene shapes.
- **Border**: rare; when present, glowing 1–2px line in saturated hero color (LED register).
- **Motion**: 200–800ms with eased curves; springs and elastic permitted; chaining via GSAP timeline; scroll-driven via ScrollTrigger. **Motion is the school's signature; this token tier matters most.**
- **Iconography**: 3D-rendered or animated SVG; static line icons feel out-of-school.

## Execution-path matrix

| Scenario | Rating | Recommended approach |
|---|:---:|---|
| Flutter UI | ★★★ | strong for product-launch / brand-event apps where the hero animation IS the product. Flutter's `flutter_animate` + Rive integration handles much of this; `theme-motion` skill is the natural pair. |
| HTML mockup (Clara) | ★☆☆ | weak — Clara emits static HTML; the school IS motion. Possible to mock the static states (loading, hero-rest, scrolled-position-N) but the school evaluates on motion which static can't show. |
| PPT | ★☆☆ | weak — PPT motion is rudimentary; the school competes with Pixar trailers, not transitions. Use video-export of the live site instead. |
| PDF | ★☆☆ | weak — PDF is static. Strong static screenshots from the live site can substitute for an art-direction PDF. |
| Infographic | ★☆☆ | weak — infographics are reading-first; the school is watching-first. |
| Cover | ★★☆ | viable as a still pulled from the kinetic sequence (a hero frame); dependent on the cinematography of the freeze-frame. |
| AI-image-gen | ★★★ | strong — generative video models (Runway, Sora, Gen-3) and 3D-style still images (Midjourney with cinematic prompts) capture the school's register. The school uses AI imagery comfortably as concept-art. |

## Slop traps

- ❌ **Animation-for-animation's-sake**: motion that doesn't carry meaning is school-violation. Each animation should communicate (entrance / state-change / hierarchy).
- ❌ **Linear easing**. The school's signature is the cubic-bezier curves; linear reads as Material Design default.
- ❌ **Skeleton-screen loaders** ("shimmer" placeholders). Loaders ARE the choreography; skeleton-screens admit defeat.
- ❌ **Static fallback as the primary experience**. The kinetic IS the school; the static fallback is an accessibility concession, not the work.
- ❌ **Forgetting `prefers-reduced-motion`**. The only ethical concession the school must make. Skipping this is a failure.
- ❌ **Light-mode-by-default**. The school lives in dark mode; light mode is exceptional.
- ❌ **Refusing the audio register**. Optional, not required — but if the site has no sound, be deliberate about that.

## Best paired with

- **Locomotive** — same kinetic-narrative DNA; Locomotive is more scroll-driven-storytelling, Active Theory more 3D-cinematic. Compatible.
- **Sagmeister & Walsh** — emotional + kinetic = theatrical events; festival-poster territory.
- **Memphis** — kinetic Memphis pattern is festival-launch-site territory.

## Anti-pairs (don't blend)

- **Müller-Brockmann** — kinetic motion is anti-grid; the school's first promise is broken.
- **Information Architects** — reading-first IS anti-watching-first.
- **Kenya Hara** — meditative pacing IS anti-cinematic timing.
- **Brutalism** — anti-polish IS anti-cinematic-polish.
- **Pentagram** — editorial register IS anti-theatrical.
