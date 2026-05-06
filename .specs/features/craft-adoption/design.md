# Design: craft-adoption

> Lightweight feature — no architectural decisions, just a layered fork + frontmatter convention.

## Decisions

### D-A — Verbatim fork, not summary

We fork the 5 docs byte-for-byte, not a "Fitio-flavored" summary. Reason: the value is exactly the precision (hex codes, 70/10/5/<1 ratios, contrast minimums). Summarizing dilutes that. If a rule doesn't fit our stack, the right move is a separate addendum doc, not editing upstream.

### D-B — Top-level `craft/` folder, not nested under `skills/`

Putting it at repo root signals "shared layer" and makes `dw.craft.requires: [<name>]` resolve unambiguously without skill-relative paths. Same shape as open-design.

### D-C — `dw:` namespace, not `od:`

We don't claim compatibility with open-design's `od:` extensions (their fields like `od.preview.type` are UI-coupled to their webapp). Using a distinct `dw:` (design-workflow) namespace lets us evolve our extensions without colliding. The contract: a non-`dw:`-aware agent ignores the field, same way it ignores `od:`.

### D-D — Field placement: frontmatter vs body

`quick_validate.py` validates frontmatter shape; an unknown top-level field MAY break it. Plan:

1. Try `dw.craft.requires:` as a top-level frontmatter field. Validate.
2. If validator rejects, fall back to placing the field under a magic comment in the body that we parse (string-match `<!-- dw.craft.requires: [a, b] -->`).

T-04 decides which path lands.

### D-E — Loading mechanism: prose, not runtime

The `dw.craft.requires:` field is metadata. The actual loading happens because each wired SKILL.md body says "Before generating output, read `craft/<name>.md`". The model executes the read at invocation time. No new tooling needed; we don't ship a craft-loader script.

### D-F — Sync cadence: manual, on-demand

Every 3-6 months we re-sync from upstream open-design SHA, capture diff, decide which deltas to absorb. Recurring `/schedule` task is overkill for content this stable. STATE.md D-11 captures this policy.

## Architecture

```
<repo>/
├── craft/
│   ├── README.md                    # 1-paragraph intro + table
│   ├── anti-ai-slop.md              # forked verbatim + attribution header
│   ├── color.md
│   ├── state-coverage.md
│   ├── typography.md
│   └── animation-discipline.md
├── docs/
│   └── skill-extensions.md          # documents `dw:` namespace
├── skills/
│   ├── theme-critique/SKILL.md      # frontmatter: dw.craft.requires: [anti-ai-slop, color, state-coverage, typography]
│   │                                # body: "Load craft references" section
│   ├── theme-create/SKILL.md        # dw.craft.requires: [color, typography, anti-ai-slop]
│   ├── theme-port/SKILL.md          # dw.craft.requires: [state-coverage, typography]
│   ├── theme-bolder/SKILL.md        # dw.craft.requires: [color, anti-ai-slop]
│   └── frontend-design/SKILL.md     # dw.craft.requires: [anti-ai-slop, color, state-coverage, typography, animation-discipline]
└── .specs/project/STATE.md          # D-11, D-12
```

## Header template for forked docs

```markdown
> **Sourced from:** https://github.com/nexu-io/open-design/blob/<SHA>/craft/<name>.md
> **Upstream attribution:** [refero_skill](https://github.com/referodesign/refero_skill) (MIT)
> **License:** Apache-2.0
> **Local path:** `craft/<name>.md`
> **Last sync:** 2026-05-05 at <SHA>

---

<verbatim upstream content>
```

## SKILL.md "Load craft references" section template

Each wired skill gets this section near the top of the body (after Triggers, before Workflow):

```markdown
## Craft references

Before generating output, read these craft references — they encode universal rules independent of any project:

- `craft/anti-ai-slop.md` — what to avoid (P0 cardinal sins)
- `craft/color.md` — palette structure and accent discipline
- `craft/state-coverage.md` — required states for every interactive surface
- `craft/typography.md` — type scale, line height, letter spacing

These are upstream from any project's design system; the project's own tokens (`AppColors`, `docs/product.md`) override only when they explicitly contradict.
```

(Per-skill, only list the docs declared in `dw.craft.requires:`.)

## Validation strategy

After all edits, run:

```bash
VAL=/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done
```

All 19 must report `Skill is valid!`. If any fails on `dw:`, the design's D-D fallback engages: move the metadata to a body comment marker.

## Rollback

`git tag pre-v1.1.1` before T-01. Single commit at the end means rollback is `git reset --hard pre-v1.1.1`.

## Estimate

- Forks + headers + craft/README: ~30 min
- Skill edits ×5: ~30 min
- docs/skill-extensions.md: ~15 min
- STATE.md + README: ~15 min
- Validation + commit + push: ~15 min
- **Total: ~1.75 h** (under the 3h estimate; buffer for D-D fallback)
