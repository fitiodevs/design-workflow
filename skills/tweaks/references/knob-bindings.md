# Knob bindings

> Loaded by `skills/tweaks/SKILL.md` when the model needs to explain or debug a knob's behaviour. Dense reference — every knob has its CSS target, value range, validation rule, visual effect, and the tweaks-ready hook that must exist in the input HTML for the knob to do anything.

The 5 knobs are deliberately fixed for v1.4. Adding a 6th requires a spec bump (decision-explosion guidance per `craft/anti-ai-slop.md`).

## Knob 1 — Accent hue

- **Form control:** `<input type="range" id="dw-knob-hue" min="0" max="360" step="1">`
- **CSS target:** `--accent-h` (the H component of an HSL triple).
- **Value range:** integer `[0, 360]`. Out-of-range values clamp to the default `18` per `sanitize()`.
- **Visual effect:** the input HTML must declare `--accent: hsl(var(--accent-h) var(--accent-s) var(--accent-l))` somewhere in `:root`. Any element that uses `var(--accent)` (button bg, link color, focus ring, etc.) shifts hue live.
- **Tweaks-ready hook:** input must contain `var(--accent` references in body styles. If the input bakes `color: #6366f1` directly, sliding does nothing — the skill body's anti-pattern check catches this.
- **Persisted as:** `state.hue` (number).

## Knob 2 — Type scale

- **Form control:** `<input type="radio" name="dw-knob-scale">` with values `1.200`, `1.250`, `1.333`.
- **CSS target:** `--scale` (the multiplicative ratio per `craft/typography.md` 6-8 size cap).
- **Value range:** one of `{1.200, 1.250, 1.333}`. Anything else → default `1.250`.
- **Visual effect:** the input must declare type tokens like `--text-h1: calc(var(--base-size) * pow(var(--scale), 4))`. CSS `pow()` is supported in modern browsers; for graceful degradation, Clara emits a 7-step ladder explicitly: `--text-h1: calc(var(--base-size) * 1.802)` etc., then re-derives via `:root[data-scale="1.333"] { --text-h1: calc(var(--base-size) * 3.157) }` overrides.
- **Tweaks-ready hook:** at least one `var(--text-` reference in the body. Without it, no font-sizes shift.
- **Persisted as:** `state.scale` (string).

## Knob 3 — Density

- **Form control:** `<input type="radio" name="dw-knob-density">` with values `compact`, `comfortable`, `loose`.
- **CSS target:** `--space-unit` (the global spacing base per `craft/spacing.md` if the project ships it; otherwise an 8-px-rooted unit).
- **Value range:** one of `{compact, comfortable, loose}`. Mapped via `densityToUnit()` to `{6px, 8px, 12px}` respectively.
- **Visual effect:** padding/margin/gap declarations in the input must use `calc(var(--space-unit) * N)` (e.g. `padding: calc(var(--space-unit) * 2)`). Stepping the knob multiplies all spacing live.
- **Tweaks-ready hook:** `calc(var(--space-unit)` occurrences in body styles. Inputs with literal `padding: 16px` won't respond.
- **Persisted as:** `state.density` (string).

## Knob 4 — Theme mode

- **Form control:** `<input type="radio" name="dw-knob-mode">` with values `light`, `dark`.
- **CSS target:** the `data-mode` attribute on `:root` (`<html>`).
- **Value range:** one of `{light, dark}`. Anything else → default `light`.
- **Visual effect:** input HTML must ship a `:root[data-mode="dark"] { --bg: …; --fg: …; … }` block that overrides the light defaults. Toggling the knob swaps the attribute, browser re-applies cascade.
- **Tweaks-ready hook:** at least one `:root[data-mode="dark"]` declaration in the input's `<style>`. Without it, the knob still toggles the attribute but nothing visual changes.
- **Persisted as:** `state.mode` (string).

## Knob 5 — Motion

- **Form control:** `<input type="radio" name="dw-knob-motion">` with values `on`, `reduced`.
- **CSS target:** the `data-motion` attribute on `:root`.
- **Value range:** one of `{on, reduced}`. Anything else → default `on`.
- **Visual effect:** the panel ships a CSS rule that, when `:root[data-motion="reduced"]`, neuters every animation/transition (`animation-duration: 0.001ms` per `prefers-reduced-motion: reduce` polyfill conventions). Already shipped in `assets/panel.html` — input needs no extra wiring.
- **Tweaks-ready hook:** none required. The motion knob works on any HTML — the panel's CSS rule has `!important` fallbacks.
- **Persisted as:** `state.motion` (string).

## State shape (localStorage)

```json
{
  "hue": 18,
  "scale": "1.250",
  "density": "comfortable",
  "mode": "light",
  "motion": "on"
}
```

Storage key: `tweaks:<basename>:<sha8(content)>`. Sanitised on read — invalid values fall back to defaults silently.

## Helper functions documented in prose

- **`sanitize(state)`** — clamps numeric fields to safe ranges; rejects non-enum string values back to defaults. Always called on read AND before persist, so corrupted localStorage entries can't paint a white screen on reload (mitigates risk-2 in spec §7).
- **`densityToUnit(density)`** — `compact → "6px"`, `comfortable → "8px"`, `loose → "12px"`. Falls back to `"8px"` on unknown.
- **`applyState(state)`** — single function that mutates `--accent-h`, `--scale`, `--space-unit`, `data-mode`, `data-motion`, AND reflects state back into the form controls (so external state change updates the UI).
- **`readState()` / `persist(state)`** — JSON round-trip via `localStorage.getItem/setItem`. Both wrapped in `try/catch` to survive privacy-mode browsers where localStorage throws.

## Why these 5 and not more

Each knob earns its slot:

- **accent hue** covers the most common "I want a different vibe" exploration — 360° of hue for ~zero UI cost.
- **type scale** exposes the multiplicative-cadence decision; 1.2 vs 1.333 has visible impact across the whole page.
- **density** exposes spacing-unit globally — the second most-asked "make it tighter / looser" knob.
- **theme mode** is a one-bit toggle reusing existing dark-mode overrides; if the input ships them, the knob is free.
- **motion** is the safety knob — kills animations during exploration to reduce noise without re-emitting.

NOT included (spec §5): per-token override, font-family swap, radius scale, line-height multiplier, accent saturation/lightness sliders. Each adds complexity for marginal exploration gain. Add when usage signals demand.
