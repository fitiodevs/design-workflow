# STATE — design-workflow

Persistent state across feature ciclos. Read at session start.

## Decisions

- **D-01 — Frontmatter spec compliance.** Drop `license:` and `triggers:` YAML keys. Move trigger info to a `## Triggers` section in the body. Date: 2026-05-01 (skill-creator-alignment).
- **D-02 — Brand-agnostic descriptions.** Replace literal "Fitio" mentions in skill descriptions/bodies with generic phrasing ("a Flutter app", "the project", "your design system"). Examples and tone preserved. Date: 2026-05-01.
- **D-03 — Scripts copy strategy.** Single source of truth in `<repo>/scripts/`. `scripts/_sync.sh` copies into each consuming skill's `scripts/` subdir; copies are committed so `git clone` + manual use works without running `_sync.sh`. Symlinks rejected (Windows/iCloud sync issues). Date: 2026-05-01.
- **D-04 — Description colon discipline.** YAML frontmatter parsing breaks when descriptions contain "Triggers:", "Persona:", "NOT for:" — colons are interpreted as YAML mapping. Use "Triggered by", "Invokes the X persona", "Skip for" instead. Discovered via `quick_validate.py` after Onda 1. Date: 2026-05-01.
- **D-05 — Description angle-bracket ban.** `quick_validate.py` rejects `<...>` inside descriptions (interpreted as placeholder leakage). Substitute with quoted strings or descriptive prose ("`/theme-port --from-stitch` plus an HTML path"). Date: 2026-05-01.

## Validation runs

### 2026-05-01 — skill-creator `quick_validate.py` (full sweep, 13 skills)

Tool: `/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py`

Result: **13/13 valid**, zero errors, zero warnings.

```
=== skills/frontend-design/ ===   Skill is valid!
=== skills/theme-audit/ ===       Skill is valid!
=== skills/theme-bolder/ ===      Skill is valid!
=== skills/theme-create/ ===      Skill is valid!
=== skills/theme-critique/ ===    Skill is valid!
=== skills/theme-distill/ ===     Skill is valid!
=== skills/theme-extend/ ===      Skill is valid!
=== skills/theme-motion/ ===      Skill is valid!
=== skills/theme-port/ ===        Skill is valid!
=== skills/theme-prompt/ ===      Skill is valid!
=± skills/theme-quieter/ ===      Skill is valid!
=== skills/theme-sandbox/ ===     Skill is valid!
=== skills/ux-writing/ ===        Skill is valid!
```

Iteration history before final: first sweep flagged 8 frontmatter parse errors (colons inside descriptions) and 2 angle-bracket errors (`<path>`, `<html>`). Fixed in commit Onda 3 by rephrasing descriptions per D-04 / D-05.

## Deferred

### Auto-improvement loop (`improve_description.py`)
- **Status:** deferred to next ciclo.
- **Why:** depends on existing `evals.json` per skill; this ciclo only added evals for the 4 verifiable skills (audit/extend/port/create). Loop output for the other 9 would be noise.
- **Next step:** wait until subjective evals exist OR run loop only on the 4 evals-equipped skills as a sanity check.

### Evals for 9 subjective skills
- **Skills missing evals:** `theme-critique`, `frontend-design`, `ux-writing`, `theme-bolder`, `theme-quieter`, `theme-distill`, `theme-motion`, `theme-prompt`, `theme-sandbox`.
- **Why deferred:** outputs are subjective (Nielsen score, AI-slop verdict, copy quality) — assertions need human-review viewer or LLM-as-judge protocol.
- **Next step:** decide between (a) human-review viewer like `skill-creator` ships, (b) LLM-as-judge with rubric in repo, or (c) skip and lean on `improve_description.py` qualitative loop.

### GitHub release v0.2.0
- **Status:** local commit only; no `git push` and no `gh release create` performed in this ciclo.
- **Next step:** owner runs `git push origin main && git push origin v0.2.0` (after tagging) and `gh release create v0.2.0 --notes-from-tag`.

### SKILL.md target ≤200 lines (target, not hard cap)
- **Status:** 4/13 hit target (≤200). Remaining 9 are 201–254 lines (well within 500 hard cap). Spec REQ-03.2 says ≤200 is target, ≤500 is hard cap.
- **Why deferred:** further extraction would split semantically related workflow steps. Marginal value vs. fragmentation cost is unclear.
- **Next step:** revisit if a future skill exceeds 300 lines or if `quick_validate` adds a ≤200 hard rule.

## Open spec features

- `.specs/features/skill-creator-alignment/` — completed 2026-05-01 in 3 commits (Onda 1/2/3). All 8 REQs verified. Acceptance criteria met.

## Conventions reminder

- Source of truth for scripts: `<repo>/scripts/<name>.py`. Edit there, then re-run `bash scripts/_sync.sh`.
- Source of truth for evals: `<repo>/skills/<skill>/evals/evals.json`. Schema follows `skill-creator/references/schemas.md`.
- Spec/design/tasks live in `.specs/features/<feature-name>/`. State (decisions, deferred) lives here.
