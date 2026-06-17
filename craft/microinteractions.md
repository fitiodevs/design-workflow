> **Adapted from:** [`wondelai/skills` → `microinteractions`](https://github.com/wondelai/skills) (MIT), distilling Dan Saffer's *Microinteractions*.
> **License:** MIT
> **Local path:** `craft/microinteractions.md`
> **Note:** Authored for this repo (not auto-synced from `nexu-io/open-design`). Companion to `animation-discipline.md`: that file decides *whether motion runs and at what duration/easing*; this file decides the *anatomy of a single interaction*. Edits here are safe — no upstream sync overwrites this file.

---

# Microinteraction craft rules

A microinteraction is a single, contained moment built around one task:
a toggle, a pull-to-refresh, a form-field validation, a like, a copy
button. The whole product is judged on these — "the difference between a
product you tolerate and one you love is almost always in the
microinteractions." This file gives them a structure so they're
*designed*, not improvised.

> Use with `animation-discipline.md` (timing/easing/reduced-motion) and
> `state-coverage.md` (every state the interaction can be in).

## The four parts (Saffer's model)

Every microinteraction has four parts. Spec all four before building —
a missing part is the usual defect.

1. **Trigger** — what starts it.
   - *Manual*: user acts (tap, swipe, long-press, focus, text entry).
   - *System*: a condition fires (data arrived, timer elapsed, threshold crossed, came online).
   - The trigger affordance must be obvious and consistent: the same
     gesture does the same thing everywhere (see `platform-conventions.md`
     for gestures you must not override).

2. **Rules** — what can happen, and in what order.
   - Define the valid states and the allowed transitions between them.
   - Use **opinionated defaults** — the best microinteraction often needs
     zero configuration. Decide for the user where you safely can.
   - Rules also decide what *can't* happen (disabled, rate-limited,
     requires confirmation for destructive actions).

3. **Feedback** — how the user knows what the rules are doing.
   - Feedback *confirms* a state change that already happened; it does not
     *perform* it (optimistic UI first, motion second — see
     `animation-discipline.md`).
   - Use the lightest channel that carries the message: a color/position
     change before an animation, an animation before a haptic, a haptic
     before a sound.
   - Never make motion the *only* signal — reduced-motion and
     screen-reader users must still get the state (pair with a static
     affordance + accessibility announcement).
   - Feedback for frequent actions must be cheap (≤200 ms; see durations
     in `animation-discipline.md`).

4. **Loops & Modes** — behavior over time.
   - *Loops*: what happens on repeat / over a long duration (does the
     "undo" linger, does the counter keep climbing, does the shimmer stop
     when content lands?). Define when the loop ends — ambient loops need
     a stop (WCAG 2.2.2) and reward bursts are one-shot.
   - *Modes*: a temporary fork in behavior (edit mode, selection mode).
     Use sparingly — a mode the user can forget they're in is a bug
     factory. Prefer a spring-back to the default state.

## Designing one — checklist

For each interactive element, answer:

- **Trigger:** manual or system? Is the affordance obvious and standard?
- **Rules:** what are the states? what's the opinionated default? what's
  forbidden / needs confirmation?
- **Feedback:** what's the lightest channel that confirms each transition?
  what does a reduced-motion / screen-reader user get?
- **Loop/Mode:** does it repeat or persist? when does it end? does it
  enter a mode, and how does the user get out?

## Where microinteractions earn their keep

Toggles & switches · form-field validation (inline, on blur, not on every
keystroke) · pull-to-refresh · button press feedback · copy-to-clipboard
confirmation · like / save / bookmark · empty-state first action ·
optimistic submit with rollback · drag handles · selection & long-press
menus.

The "one micro-interaction the user will remember" from `anti-ai-slop.md`
lives here — but exactly **one** per screen. The rest should be quiet and
correct.

## Common mistakes (lint these)

- Specifying only the Trigger and Feedback, leaving **Rules** and
  **Loop/Mode** implicit (the source of "why did it do that?" bugs).
- Validation that fires **on every keystroke** instead of on blur / submit.
- Feedback that **performs** the state change instead of confirming an
  already-applied optimistic update.
- Motion as the **only** feedback channel (fails reduced-motion + a11y).
- A **mode** with no obvious exit, or one the user can't tell they're in.
- Ambient **loops** with no end condition (shimmer/spinner forever — cap
  per `animation-discipline.md` + `state-coverage.md`).
- More than one "delight" microinteraction per screen — delight inflation
  reads as noise.
