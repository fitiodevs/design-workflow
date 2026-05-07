# design-systems/

Curated subset of [`nexu-io/open-design`](https://github.com/nexu-io/open-design)'s 71-entry `design-systems/` library. Twenty entries, 9 categories, each a complete `DESIGN.md` (Visual Theme · Color Palette & Roles · Typography · Components · Layout · Depth · Do/Don't · Responsive · Agent Prompt Guide).

These references back the `--inspired-by <slug>` and `--browse [<category>]` flags of `/theme-create` (see `skills/theme-create/SKILL.md`). The translator at `scripts/design_md_to_appcolors.py` reads any of these and emits a `proposal.json` + `rationale.md` mapping the source's roles onto our 29-token `AppColors`.

**Status:** static fork. No auto-sync. Re-fork on demand from the SHA pinned in each entry's header.
**License:** every entry retains its upstream attribution chain (see header in each `DESIGN.md`). The local fork is Apache-2.0; upstream-of-upstream lineage is mostly MIT.
**Source SHA at fork time:** `d4b547caa7cafbf328c262cdf08dd275f5bdc4d6` (2026-05-07).

---

## Category index

| Category | Slugs |
|---|---|
| AI & LLM | [`claude`](claude/DESIGN.md) · [`cohere`](cohere/DESIGN.md) · [`mistral-ai`](mistral-ai/DESIGN.md) |
| Developer Tools | [`raycast`](raycast/DESIGN.md) · [`vercel`](vercel/DESIGN.md) |
| Productivity & SaaS | [`cal`](cal/DESIGN.md) · [`linear-app`](linear-app/DESIGN.md) · [`notion`](notion/DESIGN.md) |
| Backend & Data | [`sentry`](sentry/DESIGN.md) · [`supabase`](supabase/DESIGN.md) |
| Design & Creative | [`figma`](figma/DESIGN.md) · [`framer`](framer/DESIGN.md) |
| Fintech & Crypto | [`revolut`](revolut/DESIGN.md) · [`stripe`](stripe/DESIGN.md) |
| E-Commerce & Retail | [`airbnb`](airbnb/DESIGN.md) · [`nike`](nike/DESIGN.md) |
| Media & Consumer | [`apple`](apple/DESIGN.md) · [`spotify`](spotify/DESIGN.md) |
| Automotive | [`tesla`](tesla/DESIGN.md) |
| Editorial · Studio | [`atelier-zero`](atelier-zero/DESIGN.md) |

20 entries · 9 categories. Counts mirror the spec's curation cap (`REQ-01.1`).

---

## File contract

Every `<slug>/DESIGN.md` follows the same shape:

```
> **Sourced from:** <upstream URL at SHA>
> **Upstream attribution:** <chain>
> **License:** <local | upstream>
> **Local path:** design-systems/<slug>/DESIGN.md
> **Last sync:** <YYYY-MM-DD> at <SHA>

---

# Design System Inspired by <Brand>

> Category: <Category Name>
> <one-line characterisation>

## 1. Visual Theme & Atmosphere
## 2. Color Palette & Roles
## 3. Typography
## 4. Component Stylings
## 5. Layout System
## 6. Depth & Elevation
## 7. Do's and Don'ts
## 8. Responsive Behavior
## 9. Agent Prompt Guide
```

The translator depends on three of those sections:

| Section | Used for |
|---|---|
| `> Category: <Name>` (line 2 of body) | `--browse [<category>]` filtering |
| `## 1. Visual Theme & Atmosphere` | rationale doc — pasted as the "source paragraph" |
| `## 2. Color Palette & Roles` | hex extraction + role mapping into `AppColors` |
| `## 3. Typography` | flagged in rationale; not auto-applied to tokens |

The remaining six sections are read by humans (and by future skills) but not by `scripts/design_md_to_appcolors.py`.

---

## Adding a new entry

1. Verify the slug exists upstream: `gh api repos/nexu-io/open-design/contents/design-systems/<slug>/DESIGN.md`.
2. Run the same fork pattern (attribution header + raw body) used by T-02..T-11 in `.specs/features/inspiration-library/tasks.md`.
3. Append the slug to the **Category index** above.
4. Verify the translator runs: `python3 scripts/design_md_to_appcolors.py design-systems/<slug>/DESIGN.md`.

Curation guideline (matches the original 20): cap each category at 3, prefer entries with both light and dark mode hex sets, drop entries that are too brand-coupled to be useful as inspiration (e.g. Bugatti).

---

## Re-syncing from upstream

There is no automated sync. To refresh against a new upstream SHA:

1. Capture the new SHA: `gh api repos/nexu-io/open-design/branches/main --jq '.commit.sha'`.
2. Re-fork the touched slugs (the loop in `tasks.md` is idempotent — it overwrites).
3. Update each header's `Last sync` line and this README's pinned SHA.
4. Re-run `python3 scripts/design_md_to_appcolors.py --validate-all` to catch role-name drift.

---

## Why these 20 (not 71)

20 cover the realistic "next theme to ship" decision space for Fitio without bloating the repo (240KB total). The remaining 51 stay 1 line away — open a backlog item, copy the loop. Mood-blending (`--blend stripe + linear`) is deferred (v1.4 candidate); curation is breadth-first per category, not depth.
