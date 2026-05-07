---
name: tweaks
description: Wraps any tweaks-ready HTML mockup with a side panel of live CSS-custom-property knobs (accent hue, type scale, density, theme mode, motion) persisting to localStorage. The user opens the wrapped file in any browser and explores N variants without re-prompting Clara. Output is a sibling file `[input].tweaks.html`; original input is untouched. Refuses to wrap inputs that bake decisions in literal hex/px (recommends `/frontend-design` refit first). Use after `/frontend-design` and before `/theme-port`. Triggered by `/tweaks`, `/Tweaker`, "wrap with knobs", "tweak panel", "explore variants", "manda os botões", "panel pra explorar".
metadata:
  dw:
    craft:
      requires: [color, typography, anti-ai-slop]
---

# Skill: tweaks (`/tweaks`) — persona **Tweaker** (no PT alias — functional skill)

## Triggers

- **English:** `/tweaks <path>`, `/Tweaker`, "wrap with knobs", "tweak panel", "explore variants", "give me the slider", "knobify"
- **Português:** `/tweaks <path>`, "manda os botões", "panel pra explorar", "vamos mexer nesses parâmetros", "quero variar"
- **Natural language:** any time the user has an HTML mockup and wants to ride sliders before committing to a final state. Common phrasing: "I'll know it when I see it" / "gostei mas não sei o que mudar".

`tweaks` exists to break the articulate-before-see loop: today the user must articulate a tweak ("um pouco mais quente, escala maior") before getting a new render; the skill flips that — render first, articulate by sliding.

## What it does (and what it doesn't)

`tweaks` is a **transformer**. It reads an HTML file, identifies CSS custom properties already declared at `:root`, and emits a sibling file `<input>.tweaks.html` that injects a side panel binding form controls to those properties. The panel persists to localStorage so reloading keeps the user's exploration.

**It does not:**

- Author HTML. Use `/frontend-design` (Clara) for that.
- Mutate the input file. Output is always a sibling.
- Run a server. The wrapped file is a single self-contained HTML; works offline forever.
- Generate Dart/TSX. Use `/theme-port --from-html` after the user picks a state.
- Diff two saved states. Deferred (v1.5+).

## Workflow

1. **Validate the input.** Refuse with the message in §"When to refuse" if the input bakes literal `#hex` or `px` outside `:root`. Otherwise continue.
2. **Compute the localStorage key.** `tweaks:<basename>:<sha8(content)>` — content-hashed so re-running on an updated mockup forks state intentionally.
3. **Load the panel template.** `Read skills/tweaks/assets/panel.html`. Replace `%BASENAME%` with the input filename and `%CONTENT_SHA%` with `sha8(content)`.
4. **Inject before `</body>`.** The panel is one `<aside>` + one `<style>` block + one `<script>` block. Insertion is the last thing before `</body>`; everything else in the input stays byte-equivalent.
5. **Write the sibling.** `<input-without-ext>.tweaks.html`. Never overwrite if it already exists — append `.N.tweaks.html` instead.
6. **Tell the user how to open.** Print the absolute path and a one-liner: "Open in any browser to drive the 5 knobs (accent hue · type scale · density · theme mode · motion). State persists per file."

## Knob set (v1.4 fixed)

`Read skills/tweaks/references/knob-bindings.md` for which CSS custom property each knob mutates and what value range applies. The 5 knobs are deliberately fixed for v1.4 — adding more without usage signal violates `craft/anti-ai-slop.md` decision-explosion guidance:

| Knob | Form control | CSS target |
|---|---|---|
| Accent hue | `<input type=range>` 0..360 | `--accent-h` (HSL hue) |
| Type scale | `<input type=radio>` 1.200 / 1.250 / 1.333 | `--scale` |
| Density | `<input type=radio>` compact / comfortable / loose | `--space-unit` (6 / 8 / 12 px) |
| Theme mode | `<input type=radio>` light / dark | `:root[data-mode]` attribute |
| Motion | `<input type=radio>` on / reduced | `:root[data-motion]` attribute |

## When to refuse

Tweaks only works when the input HTML uses **CSS custom properties as the single source of visual decisions**. If the input bakes hex literals (`color: #6366f1`) or pixel literals (`padding: 16px`) outside the `:root` block, the panel cannot mutate them — sliding the accent knob would do nothing.

Refuse with this exact message:

> This HTML has visual decisions baked into literal hex (or px) outside `:root`. The tweaks panel needs CSS custom properties to bind to. Run `/frontend-design --refit <path>` (or re-emit from scratch with `/frontend-design`) so all colors and spacing are `var(--…)` references, then re-run `/tweaks`. Specifically: lines [N..M] use `color: #…` directly.

Detection heuristic: count `#[0-9a-fA-F]{3,8}` occurrences outside the first `<style>:root{…}` block. If non-zero AND no `var(--` references in the body, refuse.

## Anti-patterns

- **Wrapping a Clara mockup pre-v1.4.** Older mockups bake hex inline. Refuse per above.
- **Adding a 6th knob "just in case".** Decision-explosion. New knob = new spec.
- **Persisting state to a server.** Out of scope — local-only.
- **Mutating the original file.** Always emit a sibling. Reversible by deletion.
- **Wrapping a non-HTML artifact** (Dart preview, PPTX, PDF). Tweaks is HTML-only by design.

## Output template summary

```
input.html (mockup, untouched)
input.tweaks.html ← <body>...original... <aside id="dw-tweaks-panel">…</aside><style>…</style><script>…</script></body>
```

The panel sits `position: fixed; right: 16px; top: 16px;` so it overlays the mockup. Drag handle is deferred — v1.4 ships fixed-position only.

## Pipeline

`tweaks` slots between `/frontend-design` (Clara emits the mockup with CSS custom properties) and `/theme-port --from-html` (after the user picks a state):

```
/frontend-design "milestone slider"
        ↓
/tmp/milestone.html
        ↓
/tweaks /tmp/milestone.html
        ↓
/tmp/milestone.tweaks.html  →  user opens, slides, picks
        ↓
/theme-critique --mode 5dim /tmp/milestone.html
        ↓
/theme-port --from-html /tmp/milestone.html
```

## Integração

- **Upstream of:** `/theme-critique` (5dim mode evaluates the chosen state), `/theme-port --from-html` (consumes the static HTML, not the wrapped one — the user copies the inline `<style>` overrides into the original or re-emits via Clara).
- **Downstream of:** `/frontend-design` (Clara's mockup must be tweaks-ready — see Clara's `## Tweaks-ready output` section).

## Don'ts

- **Don't** wrap the same input twice into the same output path. Append `.N.tweaks.html` if it exists.
- **Don't** alter the input's `<head>` — only `<body>` gets the panel injected before `</body>`.
- **Don't** touch the input's existing `<script>` tags. The panel script is namespaced under `dw-tweaks-` to avoid collisions.
- **Don't** assume the user has a build step. The output must be a single self-contained `.html` file — no external CSS/JS imports.
- **Don't** add a `--tweaks-ready` flag to `/frontend-design` unless the user asks. Clara's default emission already follows the rules per `## Tweaks-ready output` in her SKILL.md.
- **Don't** change the panel layout (position, knob order, default values) without bumping the skill's spec. The 5 knobs and their order are part of the contract; clients (the user's muscle memory, the smoke test) depend on it.
- **Don't** ship a "freeze" flag in this version. v1.5+ may add `/tweaks --freeze <path>` to bake a chosen state back into the source HTML; until then, the user does it by hand or re-runs `/frontend-design` with the chosen knob values as a brief.

## FAQ

**Q: My panel doesn't appear.** Most likely the input has no closing `</body>` (Clara always emits one; hand-written HTML may not). The skill body checks for `</body>` before injecting.

**Q: Slider does nothing visually.** The input's CSS doesn't reference `var(--accent)` etc. Re-emit via `/frontend-design` (Clara) — see her `## Tweaks-ready output` section.

**Q: localStorage state leaks between two mockups.** It shouldn't — keys include `sha8(content)`. If two files have byte-identical bodies, they share state intentionally (regenerating Clara on the same prompt should preserve user's exploration).

**Q: The panel covers the mockup's top-right CTA.** Drag-to-reposition is deferred. Workaround: temporarily edit the panel's `right: 16px` in the wrapped HTML's `<style>` block, OR add a "panel position" knob in v1.5.

**Q: How do I "save" a chosen state?** Click "Export current state" in the panel; copy the JSON. Apply by writing the values into the input's `:root` block manually, then re-run `/frontend-design` to keep generated mockups consistent. v1.5+ ships `--freeze`.

## Attribution

Skill design adopted from `nexu-io/open-design`'s `tweaks` skill (Apache-2.0), originating in [`huashu-design`](https://github.com/alchaincyf/huashu-design) by @alchaincyf. Local implementation in `assets/panel.html` is a clean-room rewrite tailored to the design-workflow `data-od-id` convention and the 5 fixed knobs above. Pinned at upstream SHA `9c64ef1b2bb2cffafb0ad6167d6a3831bdc0ba11` (2026-05-07).
