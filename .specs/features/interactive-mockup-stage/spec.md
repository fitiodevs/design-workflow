# Feature: interactive-mockup-stage

> Convert Clara's HTML mockup output from "static artifact → re-prompt loop" to "interactive exploration → final pick". Ship 3 components: (1) a new `tweaks` skill that wraps any HTML with a side panel of live CSS-custom-property knobs persisted to localStorage; (2) refit `frontend-design` to emit "tweaks-ready" HTML (CSS custom properties as the source of all visual decisions); (3) add `theme-critique --mode 5dim` flag for evidence-based scoring across 5 dimensions with a single-file HTML report (radar chart + Keep/Fix/Quick-wins).

**Status:** Draft (ready for execution)
**Target release:** v1.4.0 (pushed back from v1.3.0 on 2026-05-06 — multi-stack-adapter pulled forward to v1.2.0 per user urgency on Next.js+Tailwind)
**Sized:** Large (3 sub-features, ~10-12h, mix of skill creation + script + skill refit)
**Owner:** fitiodev
**Created:** 2026-05-05
**Source:** open-design adoption analysis (session 2026-05-05); upstream skills `tweaks` and `critique` from `nexu-io/open-design` (Apache-2.0); originating upstream is [`huashu-design`](https://github.com/alchaincyf/huashu-design).
**Depends on:** v1.1.1 (`craft-adoption`) — `tweaks` and `frontend-design` reference `craft/anti-ai-slop.md` + `craft/color.md` for knob defaults and validation. v1.2.0 not strictly required but preferred (lets user combine `--inspired-by` palette with `--tweaks` exploration).

---

## 1. Context

Pain stated by user (session 2026-05-05): "estou travado numa feature [milestone slider de cupons]... acredito que com mais possibilidades conseguiria mostrar o que não sei". The "I'll know it when I see it" problem. Today's loop:

```
/frontend-design → 1 HTML mockup → user reads → user articulates tweak → re-prompt → 1 HTML mockup → ...
```

Each iteration costs tokens and forces the user to articulate **before** seeing. The articulate-before-see step is exactly what blocks discovery — the user often *cannot* articulate what they want until they see options.

Open-design ships two complementary skills that flip the loop:

- **`tweaks`** wraps any HTML with a side panel binding form controls to CSS custom properties (`--accent`, `--scale`, `--density`, `--mode`, `--motion`), persisting to localStorage. User explores 20 variants in 5 minutes, no re-prompt. Self-contained HTML — no daemon, no server. Just `Read` the HTML in a browser.
- **`critique` 5-dim** scores any HTML across Philosophy / Hierarchy / Detail / Function / Innovation, outputs a self-contained HTML report with inline-SVG radar chart + Keep/Fix/Quick-wins. Complements (not replaces) our Nielsen 10 critique with a different framework better suited to early-stage exploration.

The third piece is internal to us: `frontend-design` (Clara) currently emits HTML where visual decisions are baked in (literal `color: #6366f1`, `font-size: 18px`, etc). For `tweaks` to bind knobs to those decisions, the mockup must use CSS custom properties from the start. So we refit Clara to emit `--accent`, `--bg`, `--scale`, `--density` references everywhere (already partially aligned because we adopted `craft/color.md` palette discipline in v1.1.1).

## 2. Goal

After this feature, the visual exploration pipeline is:

```
/theme-create [--inspired-by]    # picks palette
       ↓
/frontend-design                  # emits "tweaks-ready" HTML
       ↓
/tweaks <html-path>               # wraps with knob panel → user opens in browser → explores N variants
       ↓
/theme-critique --mode 5dim       # scores any candidate, evidence-based pick
       ↓
/theme-port --from-html           # ports the chosen variant
```

3 user-facing additions: 1 new skill (`tweaks`), 1 mode flag (`theme-critique --mode 5dim`), 1 quality-of-life refit (Clara emits tweaks-ready HTML).

## 3. Non-goals

- **Not** building a server or webapp. `tweaks` and `critique 5dim` outputs are single self-contained HTML files; user opens locally.
- **Not** auto-applying tweaks. The user picks; the chosen state goes into theme-port. Tweaks doesn't write Dart.
- **Not** replacing `theme-critique` (Nielsen 10). 5dim is a `--mode` flag, default stays Nielsen.
- **Not** persistence beyond localStorage. No server-side state, no project-level "saved variants" feature in v1.3.
- **Not** comparing two HTML files side-by-side in tweaks. v1.4 candidate; needs different UI.
- **Not** generating animations as knobs (the `--motion` knob toggles motion-on/off; it doesn't author motion curves). theme-motion handles authoring.
- **Not** tweaks for non-HTML artifacts (Dart widget preview, PDF, etc).

## 4. Requirements

### REQ-01 — `tweaks` skill (the wrapper)

- **REQ-01.1** Create `skills/tweaks/SKILL.md` with persona "Tweaker" (no PT-equivalent persona — keep functional). Triggers: `/tweaks <path>`, `/tweaks --variants <path>`, "wrap with knobs", "tweak panel", "explore variants", "manda os botões".
- **REQ-01.2** SKILL.md body teaches the model how to wrap any input HTML: parse → identify visual decisions → rewrite to CSS custom properties → inject the panel template → persist localStorage key derived from filepath.
- **REQ-01.3** Ship `skills/tweaks/assets/panel.html` template (the actual side-panel HTML+CSS+JS that gets injected). ~200-300 lines vanilla JS, no framework, no dependencies.
- **REQ-01.4** Standard knobs (in this exact order, no more for v1.3):
  - **Accent hue** (slider 0–360, persists to `--accent` HSL)
  - **Type scale** (radio: 1.2 / 1.25 / 1.333)
  - **Density** (radio: compact / comfortable / loose, drives `--space-unit`)
  - **Theme mode** (toggle: light / dark, drives `--mode` data attribute)
  - **Motion** (toggle: on / reduced, drives `prefers-reduced-motion` polyfill)
- **REQ-01.5** Output: a single new HTML file `<input-path>.tweaks.html` (don't overwrite original); user opens in any browser. localStorage key: `tweaks:<basename>:<sha-of-content>` so different mockups don't collide.
- **REQ-01.6** Anti-pattern: never wrap an HTML that already declares a `<style>` block targeting `:root` with literal hex (would conflict). Skill body documents this — if detected, recommends running `/frontend-design --tweaks-ready` first OR refit the input.

### REQ-02 — Refit `frontend-design` to emit tweaks-ready HTML

- **REQ-02.1** Mockups generated by Clara use CSS custom properties as the **only** source of visual decisions:
  - All colors via `var(--<role>)` — never literal hex
  - All spacing via `calc(var(--space-unit) * <multiplier>)` — never literal `px` outside structural width/height
  - Type sizes via `calc(var(--base-size) * pow(var(--scale), N))` — never literal `font-size: 18px`
  - Theme mode via `:root[data-mode="dark"] { ... }` overrides
- **REQ-02.2** Every section gets a stable `data-od-id` attribute (we adopt this from open-design — same name, simpler than inventing `data-dw-id`).
- **REQ-02.3** Clara updates her self-revisão checklist (in `references/clara-checklist.md`) to add: "Are all visual decisions CSS-custom-property-driven?" and "Does every major section have data-od-id?".
- **REQ-02.4** Update Clara's eval (when present) to verify these in output.
- **REQ-02.5** Backward compat: if user pipes a non-tweaks-ready HTML into `/tweaks`, the skill body's REQ-01.6 anti-pattern applies — error gracefully with a "refit first" recommendation.

### REQ-03 — `theme-critique --mode 5dim` flag

- **REQ-03.1** `skills/theme-critique/SKILL.md` documents the flag; default mode stays Nielsen 10.
- **REQ-03.2** When `--mode 5dim`, theme-critique:
  - Scores 5 dimensions 0–10: Philosophy / Visual hierarchy / Detail / Functionality / Innovation. Bands: 0–4 Broken · 5–6 Functional · 7–8 Strong · 9–10 Exceptional.
  - Emits a single self-contained HTML report at `.design-spec/critique/<feature>/<timestamp>-5dim.html`.
  - Report layout: Header (artifact reviewed, date, 1-line verdict) → inline-SVG radar chart → 5 dimension cards (each with score, band label, evidence paragraph citing specific elements/files/lines, 1 Keep/Fix/Quick-win bullet) → combined Keep/Fix/Quick-wins lists.
- **REQ-03.3** Adapt the rubric reference: `skills/theme-critique/references/5dim-rubric.md` (forked from open-design's critique skill body, attribution header).
- **REQ-03.4** Existing Nielsen 10 mode unchanged; output path `.design-spec/critique/<feature>/<timestamp>-nielsen.html` instead of overwriting.

### REQ-04 — Pipeline doc updates

- **REQ-04.1** README: §What changed in v1.3.0 documents the loop — frontend-design → tweaks → theme-port. Includes a small ASCII diagram of the pipeline.
- **REQ-04.2** `docs/theme-manager.md` "I'm starting a new app" workflow updated to include `/tweaks` between `/frontend-design` and `/theme-port`.
- **REQ-04.3** `docs/personas.md` adds Tweaker persona row (no PT alias — keep `/tweaks` as the only trigger).

### REQ-05 — STATE.md decisions

- **REQ-05.1** D-15 — Tweaks as wrapper, not generator: tweaks doesn't author HTML; it wraps existing. Rationale: composability — works on any HTML, not just Clara's.
- **REQ-05.2** D-16 — `data-od-id` reuse: we adopt open-design's attribute name verbatim instead of inventing `data-dw-id`. Reason: future bidirectional compatibility (their critique skill could read our mockups; ours could read theirs).
- **REQ-05.3** D-17 — Critique mode flag, not separate skill: `--mode 5dim` instead of new `theme-critique-5dim` skill. Reason: same input, different rubric — keeping them unified keeps the routing decision simple ("when in doubt, /theme-critique").

### REQ-06 — Validate + bump

- **REQ-06.1** `quick_validate.py` returns 20/20 valid (was 19; +1 for `tweaks`).
- **REQ-06.2** End-to-end smoke test: generate a mockup with Clara → wrap with tweaks → open in browser → confirm panel appears + accent slider mutates the header color + localStorage persists across reload.
- **REQ-06.3** `marketplace.json` bumped 1.2.0 → 1.3.0 + add `./skills/tweaks` to skills array.

## 5. Out of scope (deferred)

- **Diff mode for tweaks** (compare 2 saved states side-by-side). Future v1.4 candidate.
- **Per-token override** (knob to override one specific token without changing the global scale). Possible v1.4.
- **Tweaks for stack-other-than-HTML** (Dart widget preview, PPTX). Different pipeline, deferred indefinitely.
- **Backporting CSS-custom-property structure to historical Fitio mockups**. Only new mockups from v1.3+ are guaranteed tweaks-ready.
- **Critique 5dim auto-comparison of two artifacts**. Open-design's skill notes this is for "comparing two variants of the same design"; we ship single-artifact mode in v1.3, comparison in v1.4 if there's demand.
- **Sharing a tweaks state via URL param** (would need a server). Local-only for v1.3.

## 6. Source pin

- Upstream repo: `nexu-io/open-design`
- Upstream branch: `main`
- Upstream SHA at fork time: **TBD — capture during T-00**
- Upstream license: Apache-2.0
- Originating upstream: [huashu-design](https://github.com/alchaincyf/huashu-design) (we re-attribute to both)

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Refitting Clara breaks all existing eval tests / examples | High | T-09 audits Clara's evals/eval.json; T-10 explicitly updates assertions to match new output. |
| Vanilla-JS panel breaks in Safari/Firefox edge cases | Medium | Use only well-supported features (CSS custom properties, localStorage, FormData) — no fancy APIs. T-15 smoke-tests in 2 browsers. |
| `data-od-id` conflicts with user's own data attributes | Low | Document in skill body; user can override via `--id-attribute <name>` flag (deferred, not in v1.3). |
| 5dim radar chart inline SVG looks bad with extreme score spread (e.g. 9/9/9/9/2) | Low | Use percentile rather than raw 0-10 axis if the spread exceeds 5; T-19 tests this. |
| Tweaks HTML grows huge (panel + JS + bound CSS) → loads slowly | Low | Vanilla JS keeps it ~50KB. Compare against typical mockup ~200KB. |
| Race condition: localStorage persists invalid hue (e.g. 720) → white screen on reload | Medium | T-12 implements input validation in the bridge; out-of-range values clamp to nearest valid. |

## 8. Acceptance criteria

- [ ] REQ-01..REQ-06 all verified
- [ ] `tweaks` skill ships with working panel.html template
- [ ] Clara's mockup output is byte-for-byte tweaks-ready (CSS custom properties as the only visual source + every section has data-od-id)
- [ ] End-to-end smoke: create mockup → wrap → open in 2 browsers (Chrome + Firefox) → all 5 knobs mutate live → reload → state persists
- [ ] `theme-critique --mode 5dim cupom-milestone-slider.html` produces a self-contained HTML report with radar chart
- [ ] STATE.md has D-15, D-16, D-17
- [ ] Single commit: `feat(release): v1.3.0 — interactive mockup stage (tweaks + 5dim critique)`
