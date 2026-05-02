# Motion tokens — durations, curves, canonical patterns

Use this reference in Steps 2–3 of `/theme-motion`. Always pull from `AppMotion.*` (durations) and `AppCurves.*` (easings); never literal `Duration(milliseconds: N)` or built-in `Curves.*` directly.

## Required curves

- `AppCurves.enter` (≈ `Curves.easeOutQuart`) — entrances, fade-in, scale-in
- `AppCurves.exit` (≈ `Curves.easeInQuart`) — exits, dismiss
- `AppCurves.move` (≈ `Curves.easeInOutCubic`) — sustained motion (translate, slide)

## Banned curves (Jack refuses)

- `Curves.bounce*`
- `Curves.elastic*`
- Built-in `Curves.ease*` (use `AppCurves.enter`/`exit`/`move` instead — they're tuned)
- Linear in non-shimmer contexts (linear is for loops only)

## Picking a duration

| Token | Range | Use |
|---|---|---|
| `AppMotion.fast` | 80–120ms | Press feedback, snap |
| `AppMotion.normal` | 200–300ms | Fade in, scale, route transitions |
| `AppMotion.slow` | 400–600ms | Hero choreography, celebration enter |
| `AppMotion.shimmer` | 1.8–2.4s | Loading shimmer (linear, infinite) |
| `AppMotion.celebration` | ≤1200ms total | Milestone-hit sequence (Rive or composed) |

If the token you need doesn't exist yet, **create it first** in `lib/core/theme/app_motion.dart` or `app_curves.dart`, then use.

## Canonical patterns (`docs/motion.md` §4 references)

Before inventing, check whether your case fits one of these:

- §4.1 **Press feedback** — `scale 0.97`, 80ms, `AppCurves.enter`. Default for any tappable card/chip without it.
- §4.2 **Shimmer** — track shimmer for live progress feedback. 2.4s linear, infinite.
- §4.3 **Pulse** — pulse on the next-target node. 1.8s `AppCurves.enter`, reverse.
- §4.4 **Stagger** — list-item enter. 30–80ms between items, ≤8 items only.
- §4.5 **Hero number entry** — fade + scale 0.95→1.0, `AppMotion.normal`.
- §4.6 **Milestone hit (celebration)** — composed sequence ≤1200ms, optionally Rive.
- §4.7 **Route transitions** — `CustomTransitionPage` with `AppMotion.route` (~300ms).
- §4.8 **Scroll-driven** — auto-scroll, parallax effects.

If your case doesn't fit any of the 8, invent a new pattern only with documented justification in `docs/motion.md`.

## Performance guardrails

- **GPU-only properties:** `transform` and `opacity`. Animating `width`/`height`/`top`/`left` triggers reflow → lag.
- **`RepaintBoundary`** around any animated child inside `ListView.builder` / `GridView`.
- **`onPlay: (c) => c.repeat()`** loops need a controller dispose path or `flutter_animate` to manage it.
- **Reduce-motion contract** is non-optional — read Step 6 of the SKILL.
