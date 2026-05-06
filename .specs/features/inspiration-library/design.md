# Design: inspiration-library

## Decisions

### D-A — Curate, don't fork-all

20 entries balance category coverage vs maintenance burden. 71 entries × periodic re-sync = noise. 20 chosen with cap-per-category prevents AI/SaaS overload (cap 3) and keeps the picker presentable in a CLI list.

### D-B — Translator owns the bridge, not the skill body

Mapping CSS roles → 29 AppColors tokens is mechanical and benefits from being a separate Python script:
- Reproducible (same source → same proposal)
- Testable (5 sample sources × known expected mappings)
- Debuggable independent from the skill
- Reusable (later: `theme-extend --inspired-by` could call the same mapper for one role)

The skill body orchestrates: read source, run script, present to user, ask for tweaks, emit Dart.

### D-C — Inference chain over rigid mapping

DESIGN.md doesn't enforce role names — Claude calls its accent "Terracotta Brand" not `--accent`. So the translator can't lookup-by-name. Chain:

1. **Explicit `--<role>` literal** in DESIGN.md → use as-is.
2. **Section header semantic match** — under "## Color Palette > Primary" → first hex is brand. Under "## Color Palette > Surface & Background" → first hex is `bgBase`, second is `bgSurface`.
3. **Regex on hex codes** in the body, ordered by appearance in canonical sections.
4. **WCAG re-check** — if derived `textPrimary` on `bgBase` fails 4.5:1, propose darkening textPrimary by 100 OKLCH lightness points and flag in rationale.
5. **Fallback flag** — Fitio-specific tokens (`gameAccent`, `gameAccentMuted`, `gameAccentOnColor`, badge colors) have no source equivalent → flagged for user input, never silently picked.

T-04 implements this chain; T-08 tests it on 3 samples.

### D-D — Light/dark inference

Most sources have explicit dark-mode hex. Translator detects:
- Section header "## Dark mode" / "Dark Theme" → use those hex.
- "Dark Surface" + "Deep Dark" mentioned → those map to bgSurface/bgBase in dark mode.
- Single-mode source → derive other mode by OKLCH L-flip (existing `oklch_to_hex.py`), flag prominently in rationale.

### D-E — Rationale doc is non-negotiable

Even if the translator output is "perfect", the rationale doc:
- Forces the model to explain mapping decisions (catches bad inferences).
- Gives the user evidence to argue with ("source says terracotta is `#c96442`, you proposed `#d97757` — why?").
- Records origin for future audit ("why does our seasonal-paywall theme look 30% lighter than Stripe?").

Format: `docs/themes/<slug>-rationale.md`. Required sections: Source citation · Token mapping table · WCAG report · Open questions for user.

### D-F — `--inspired-by` skips 6 of 8 pre-conditions

Original 8 pre-conditions: purpose, audience, tone (extreme), invariants, differentiation, coexistence, color strategy commitment, anti-category-reflex check.

When `--inspired-by` is set, the source already encodes:
- ✅ tone (extreme picked) — source's Visual Theme paragraph
- ✅ differentiation — implicit in choosing the source over alternatives
- ✅ color strategy commitment — explicit in source's palette structure
- ✅ anti-category-reflex — implicit (user picked a non-default reference)

Still asked:
- ⚠️ purpose — what's this theme FOR (sub-brand? seasonal? sponsor?)
- ⚠️ audience — same
- ⚠️ invariants — what must NOT change vs current default theme
- ⚠️ coexistence — does this replace default, or live alongside as a 3rd `AppColors` instance?

Result: 8 questions → 4. ~2 minutes saved per invocation, but more importantly the user starts from a non-blank reference.

## Architecture

```
<repo>/
├── design-systems/
│   ├── README.md                    # category index + mapping → which skill consumes
│   ├── claude/DESIGN.md             # 20 forks, each with attribution header
│   ├── linear-app/DESIGN.md
│   ├── stripe/DESIGN.md
│   ├── … (17 more)
│   └── atelier-zero/DESIGN.md       # 1 hand-curated from open-design (not 3rd-party)
├── scripts/
│   └── design_md_to_appcolors.py    # NEW: translator (REQ-02)
├── skills/theme-create/
│   ├── SKILL.md                     # Triggers/Workflow updated for new flags
│   └── references/
│       └── inspiration-flow.md      # NEW: explains the --inspired-by + --browse workflow in depth
└── .specs/project/STATE.md          # D-13, D-14
```

## Translator script outline

```python
# scripts/design_md_to_appcolors.py
"""
Convert a design-systems/<slug>/DESIGN.md into a Fitio AppColors proposal.
Outputs: proposal.json (29 tokens × 2 modes) + rationale.md.

Usage:
    python3 scripts/design_md_to_appcolors.py <slug> [--out-dir <dir>]
    python3 scripts/design_md_to_appcolors.py --validate-all   # smoke-test all 20
"""

# Phases:
# 1. parse_design_md(path) -> {sections: {color_palette: [...], typography: {...}, ...}}
# 2. extract_palette(sections) -> {primary: [hex,...], surface: [...], text: [...], ...}
# 3. map_to_appcolors(palette) -> {brandDefault, bgBase, ..., textPrimary, ...}
# 4. derive_dark_mode(light_palette, source) -> {dark variant of all 29}
# 5. validate_wcag(proposal) -> {pair: ratio} + flagged failures
# 6. write_artifacts(proposal, rationale, out_dir)

# Inference chain implemented in map_to_appcolors per design D-C.
# Each mapping decision logs to rationale.md with: source_role, source_hex, target_token, reason.
```

Estimated size: ~250-300 LOC Python. Reuses `scripts/check_contrast.py` (WCAG) and `scripts/oklch_to_hex.py` (color math).

## Testing strategy

- **3 sanity samples** for translator (T-08): claude (warm/serif/single-accent), linear-app (cool/sans/multi-tone), stripe (purple-ish/dense).
- For each: translator output reviewed manually for: (a) all 29 tokens populated or flagged, (b) WCAG 12 mandatory pairs at AA, (c) rationale citations match source.
- No automated assertion — review is human judgment for v1.2.

## Validation strategy

After all edits:

```bash
# 1. quick_validate.py for skills (theme-create only changed)
VAL=/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done   # 19/19 valid

# 2. translator smoke test
for s in claude linear-app stripe; do
    python3 scripts/design_md_to_appcolors.py design-systems/$s/DESIGN.md --out-dir /tmp/translator-test/$s/
    python3 scripts/check_contrast.py --json /tmp/translator-test/$s/proposal.json
done

# 3. browse smoke test (manual: invoke /theme-create --browse fintech and confirm Stripe + Revolut listed)
```

## Rollback

`git tag pre-v1.2.0` before T-00. Single commit at the end.

## Estimate

- Curate (read upstreams + pick 20 + verify mix): ~1.5h
- Fork 20 with attribution headers: ~1h (mostly automation)
- Translator script: ~3h (mapping logic + WCAG integration + rationale generation)
- Translator smoke tests on 3 samples: ~1h
- Skill body update + references: ~1h
- STATE/README/version: ~30min
- Validation + commit: ~30min
- **Total: ~8.5h** (matches the 6-8h estimate; could compress by 1h via parallel forks)
