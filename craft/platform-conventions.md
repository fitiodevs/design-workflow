> **Adapted from:** [`wondelai/skills` → `ios-hig-design`](https://github.com/wondelai/skills) (MIT), cross-referenced with Apple's Human Interface Guidelines and Google's Material Design.
> **License:** MIT
> **Local path:** `craft/platform-conventions.md`
> **Note:** Authored for this repo (not auto-synced). **Re-scoped for hybrid mobile** — one Flutter codebase shipping the same product to iOS *and* Android. SwiftUI/UIKit-specific API guidance from the source is dropped; what remains is the platform-*idiom* best practice that a hybrid app must respect on each OS. Edits here are safe.

---

# Platform conventions craft rules (hybrid iOS + Android)

A hybrid app ships one product to two platforms whose users have
different muscle memory. The goal is **not** a single look forced onto
both, nor two separate designs — it's a shared structure that *adapts its
idiom* per platform where the convention is load-bearing. Apple's three
words (clarity, deference, depth) and Material's emphasis on motion +
elevation both reduce to: **content first, the chrome defers, navigation
is where users already expect it.**

> Token rule still holds: express these as adaptive tokens / platform
> checks, never hardcoded per-screen. Depth is platform-flavored — see
> `visual-hierarchy.md`.

## Touch targets & layout

- **Minimum touch target: 44pt (iOS) / 48dp (Android).** Use the larger
  when in doubt; never ship a tap target below it. List rows ≥ that height.
- **Respect safe areas / insets** — notch, Dynamic Island, status bar,
  home indicator (iOS) and gesture/nav bars + cutouts (Android). Content
  inside insets; only backgrounds bleed edge-to-edge.
- **Design smallest-first** (≈360–375 logical px wide), then scale up to
  tablets/foldables. Standard edge margins 16–20.
- Spacing on the shared `8`-grid (`8/16/24…`, see `visual-hierarchy.md`).

## Navigation

- **Bottom tab bar for 2–5 top destinations**, always visible, remembers
  state per tab. Idiomatic on *both* platforms.
- **Avoid the hamburger menu** as primary navigation — it hides structure
  and tanks discoverability on mobile. Use it only for genuinely
  secondary/overflow items.
- Title + back affordance at top; primary screen action top-right or in a
  bottom action bar.
- **Modals/sheets for focused, interruptive tasks**; dismissable by the
  platform gesture.

## Gestures you must not override

Breaking these breaks muscle memory and feels foreign:

| Gesture | iOS | Android |
|---|---|---|
| Back | swipe from left edge | system Back / **predictive back** (gesture-progress, animates the destination behind the current screen) |
| Dismiss sheet | swipe down | swipe down / Back |
| Refresh | pull down | pull down |
| Row actions | swipe left/right | swipe left/right |
| Context menu | long-press | long-press |

Custom gestures are *supplementary only* — never the sole path to an
action. (Motion details for these live in `animation-discipline.md` §
cross-platform handoff.)

## Type & dynamic scaling

- **Honor the OS font-size setting** (Dynamic Type / Android font scale).
  Use semantic text roles that scale, never hardcoded sizes — a layout
  that breaks at the largest accessibility size is a defect.
- Left-aligned, non-justified body (see `typography.md`).
- Minimum body ~11pt floor; readable line length 35–50 chars on phone.

## Color, dark mode & icons

- **Dark mode is first-class, not optional polish.** Ship and test both
  appearances; maintain ≥4.5:1 text contrast in each.
- Prefer **semantic / system colors** that resolve per platform and per
  appearance (label, background, separator, system tint, destructive-red)
  over fixed hex — they keep you correct in dark mode and respect user
  accessibility overrides. Brand accent layers on top with discipline
  (`color.md`).
- Use the platform's **system icon set where one exists** (SF Symbols feel
  native on iOS; Material Symbols on Android) — they scale with text and
  match weight. Monoline, consistent stroke, `currentColor` (per
  `anti-ai-slop.md`).

## Controls, haptics & feedback

- Prefer **native-feeling controls** (switches, pickers, sheets) over
  bespoke reinventions — they carry built-in accessibility and platform
  behavior.
- Destructive actions: red + confirmation.
- Match keyboard type to input (email, number, phone, URL) and enable
  autofill / content-type hints.
- **Haptics: subtle and meaningful, never constant.** Impact for physical
  actions, notification for outcomes, selection for discrete UI changes.
  Constant buzz trains users to ignore it.

## Accessibility (both screen readers)

- Test complete flows with **VoiceOver (iOS) and TalkBack (Android)** —
  not just the happy path.
- Every interactive element needs an accessible **label**; state and
  effect get value/hint. Group related nodes so the reader doesn't
  announce noise.
- **Never convey meaning by color alone** — pair with icon/label/position.
- Touch targets and contrast floors above are accessibility requirements,
  not nice-to-haves.

## Diagnostic — hybrid readiness

1. Layout respects safe areas/insets on a notched iPhone *and* a
   gesture-nav Android?
2. Every tap target ≥44pt / 48dp?
3. Fully usable in dark mode on both?
4. Layout survives the largest OS font-scale setting?
5. Navigation is bottom-tab (not hamburger) for primaries?
6. No standard platform gesture overridden?
7. VoiceOver *and* TalkBack complete every task?

## Common mistakes (lint these)

- One platform's idiom forced on the other (iOS-only patterns on Android
  or vice-versa) — or a hamburger replacing tab bars.
- Touch targets below 44pt / 48dp.
- Ignoring safe areas / insets (content under the notch or nav bar).
- Skipping dark mode or testing only one appearance.
- Hardcoded font sizes that break Dynamic Type / font scaling.
- Overriding edge-back, pull-refresh, or swipe-dismiss.
- Meaning carried by color alone.
- Constant or decorative haptics.
- Testing with only one screen reader.
