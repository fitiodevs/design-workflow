# Design: interactive-mockup-stage

## Decisions

### D-A — `tweaks` is a transformer, not a generator

The skill's job is to take an existing HTML file and emit a derivative HTML file with knobs. It does NOT author UI from scratch. Composability gain: works on Clara mockups, on Figma's HTML export, on any hand-written HTML. Cost: requires the input to already be CSS-custom-property-driven (REQ-02 refits Clara to make this true going forward).

### D-B — Wrapper output is a sibling file, not in-place edit

`<input>.tweaks.html` is the output. Original input is untouched. Reason: tweaks should be reversible by deletion. If user wants to "freeze" a tweaks state into a clean HTML, they save the localStorage state and we'd ship a `--freeze` flag in v1.4.

### D-C — Vanilla JS, no framework

300 lines max. Reason: loading React/Vue inflates the artifact 200KB+ and adds a build step. Vanilla JS keeps the wrapped HTML <100KB total and works offline forever.

### D-D — localStorage key derived from content hash

Multiple tweaks-wrapped files in the same browser shouldn't share state. Key shape: `tweaks:<basename>:<sha8(content)>`. SHA on content (not on path) means re-generating Clara's mockup with same content keeps the user's tweaks; regenerating with different content forks the state.

### D-E — Knob set is fixed and minimal in v1.3

5 knobs: accent hue, type scale, density, theme mode, motion. Why these 5:

- **accent hue** — covers the most common "I want a different vibe" exploration
- **type scale** — exposes the multiplicative scale decision (1.2 vs 1.25 vs 1.333 has visible impact)
- **density** — exposes spacing-unit globally (compact vs comfortable vs loose)
- **theme mode** — light/dark toggle, reuses existing `:root[data-mode="dark"]` overrides
- **motion** — on/off, lets user kill animations during exploration (reduce noise)

NOT in v1.3: per-token override, font-family swap, radius scale, line-height multiplier. Each adds complexity for marginal gain. Add when usage signals demand.

### D-F — `data-od-id` reuse over `data-dw-id` invention

Open-design ships `data-od-id` for "comment mode can target sections". We don't have comment mode yet, but if we ever did, bidirectional compat with their tooling is free if we share the attribute name. Cost: zero (one identifier name). Benefit: future-proof.

### D-G — `5dim` is a mode flag, not a separate skill

User invokes `/theme-critique <path>` and gets Nielsen 10 (default) OR `--mode 5dim` for the alternative. Reason: routing decision should be "is this critique?" not "is this Nielsen-style or 5dim-style?". The mode is a parameter of an existing skill.

Trade-off: theme-critique SKILL.md grows. Mitigation: 5dim rubric content lives in `references/5dim-rubric.md`, body just dispatches.

### D-H — Critique reports go to `.design-spec/critique/`, never overwrite

Each invocation writes a timestamped HTML report. Path: `.design-spec/critique/<feature-slug>/<YYYY-MM-DD-HHMM>-<mode>.html`. Reason: design exploration produces N critiques over time; overwriting loses history.

`.design-spec/` is the runtime state dir per `docs/design-spec-driven-plan.md` §"PERSISTENT STATE" — already canonical.

## Architecture

```
<repo>/
├── skills/
│   ├── tweaks/                                NEW
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   │   └── panel.html                     # the side-panel template (~250 lines vanilla)
│   │   ├── references/
│   │   │   └── knob-bindings.md               # which knob mutates which CSS custom property
│   │   └── evals/
│   │       └── evals.json                     # 3 prompts × 4-5 assertions
│   ├── frontend-design/
│   │   ├── SKILL.md                           # MODIFIED: tweaks-ready emission rules
│   │   └── references/
│   │       └── clara-checklist.md             # MODIFIED: add 2 checklist items
│   └── theme-critique/
│       ├── SKILL.md                           # MODIFIED: --mode flag, dispatch
│       └── references/
│           ├── nielsen-rubric.md              # existing
│           └── 5dim-rubric.md                 # NEW: forked from open-design
├── docs/
│   ├── personas.md                            # MODIFIED: add Tweaker row
│   └── theme-manager.md                       # MODIFIED: pipeline includes /tweaks
├── README.md                                  # MODIFIED: §What changed in v1.4.0
├── .specs/project/STATE.md                    # MODIFIED: D-19, D-20, D-21
└── .claude-plugin/marketplace.json            # MODIFIED: add ./skills/tweaks, bump 1.4.0
```

## Panel HTML template structure

```html
<!-- skills/tweaks/assets/panel.html (template) -->
<!-- This is the snippet injected into <body> of any input HTML. -->

<aside id="dw-tweaks-panel" class="dw-tweaks">
  <h2>Tweak the design</h2>
  <fieldset>
    <legend>Accent hue</legend>
    <input type="range" name="accent-hue" min="0" max="360" />
    <output name="accent-hue-value"></output>
  </fieldset>
  <fieldset>
    <legend>Type scale</legend>
    <label><input type="radio" name="scale" value="1.200" /> 1.2 (compact)</label>
    <label><input type="radio" name="scale" value="1.250" checked /> 1.25 (default)</label>
    <label><input type="radio" name="scale" value="1.333" /> 1.333 (open)</label>
  </fieldset>
  <fieldset>
    <legend>Density</legend>
    <!-- compact / comfortable / loose -->
  </fieldset>
  <fieldset>
    <legend>Theme</legend>
    <!-- light / dark toggle -->
  </fieldset>
  <fieldset>
    <legend>Motion</legend>
    <!-- on / reduced -->
  </fieldset>
  <button id="dw-tweaks-reset">Reset</button>
  <details>
    <summary>Export current state</summary>
    <pre id="dw-tweaks-state"></pre>
  </details>
</aside>

<style>
  :root {
    --accent-h: 18;
    --accent: hsl(var(--accent-h) 70% 50%);
    --scale: 1.250;
    --space-unit: 8px;
  }
  .dw-tweaks {
    position: fixed; right: 16px; top: 16px; width: 280px;
    padding: 16px; background: var(--surface, #fff); border: 1px solid var(--border, #ddd);
    border-radius: 8px; font-family: system-ui; font-size: 13px;
    z-index: 9999;
  }
</style>

<script>
  // Bind form -> CSS custom properties + localStorage
  const STORAGE_KEY = 'tweaks:%BASENAME%:%CONTENT_SHA%';  // replaced at injection time
  const root = document.documentElement;

  function applyState(state) {
    if (state.accentHue != null) root.style.setProperty('--accent-h', state.accentHue);
    if (state.scale != null) root.style.setProperty('--scale', state.scale);
    if (state.density != null) root.style.setProperty('--space-unit', densityToUnit(state.density));
    if (state.mode) root.dataset.mode = state.mode;
    if (state.motion === 'reduced') root.dataset.motion = 'reduced';
  }

  function densityToUnit(density) {
    return ({compact: 6, comfortable: 8, loose: 12})[density] + 'px';
  }

  // Restore from localStorage on load
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  applyState(saved);

  // Bind change events on every form control
  document.querySelectorAll('#dw-tweaks-panel input').forEach(input => {
    input.addEventListener('input', e => {
      // ... clamp + apply + persist
    });
  });
</script>
```

Final size estimate: ~250 lines including the script logic and validation/clamping for input bounds (REQ-07.5 risk).

## Refit rules for `frontend-design`

Concrete additions to Clara's existing emission rules:

1. **All hex literals → CSS custom properties.** Generator emits a `:root { --accent: <hex>; --bg: <hex>; ... }` block at top, then references via `var()` everywhere. Never `color: #6366f1` in the body.
2. **All spacing → `calc()`.** `padding: 16px` becomes `padding: calc(var(--space-unit) * 2)`. `gap: 8px` becomes `gap: var(--space-unit)`.
3. **All font-size → multiplicative scale.** Per `craft/typography.md` 6-8 size cap, define 7 named tokens at top: `--text-display: calc(var(--base) * pow(var(--scale), 4))`, etc. Use `var(--text-h1)` everywhere.
4. **`data-od-id` on every section.** Generator assigns `<section data-od-id="hero">`, `<section data-od-id="features">`, etc.
5. **Dark mode via attribute.** `:root[data-mode="dark"] { --bg: <dark-hex>; ... }` block separate from light defaults.

These are documented in `skills/frontend-design/references/clara-checklist.md` as 5 checklist items.

## 5dim rubric reference

Forked from open-design's critique skill body. Each dimension has 4 paragraphs:

- **What it scores** (the prompt to the critic)
- **Evidence to look for** (concrete signals)
- **Anti-patterns** (what drops the score)
- **Score bands** (0-4 / 5-6 / 7-8 / 9-10 with examples)

The `theme-critique` skill body, when in 5dim mode, reads `references/5dim-rubric.md` before scoring.

## Validation strategy

```bash
VAL=/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py

# 1. quick_validate.py 20/20 valid
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done

# 2. End-to-end smoke (manual but documented)
#    a. /frontend-design "milestone slider with 5 cupom states" → /tmp/milestone.html
#    b. /tweaks /tmp/milestone.html → /tmp/milestone.tweaks.html
#    c. open /tmp/milestone.tweaks.html in Chrome → mutate accent slider → confirm visual change
#    d. reload → state persists
#    e. open in Firefox → same outcome

# 3. 5dim critique smoke
#    /theme-critique --mode 5dim /tmp/milestone.html → confirm output at .design-spec/critique/.../5dim.html
```

## Rollback

`git tag pre-v1.4.0` before T-00.

## Estimate

- Tweaks skill (SKILL.md + assets/panel.html + references): ~5h
- Clara refit + checklist: ~2h
- 5dim mode in theme-critique + rubric reference: ~3h
- Pipeline doc updates (README, theme-manager, personas): ~1h
- STATE/version/validation/commit: ~1h
- **Total: ~12h** (matches the 10-12h estimate; tweaks is the heaviest)
