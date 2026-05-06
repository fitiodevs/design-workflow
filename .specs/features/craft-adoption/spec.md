# Feature: craft-adoption

> Adopt the 5 brand-agnostic methodology docs from [open-design](https://github.com/nexu-io/open-design)'s `craft/` folder (anti-ai-slop, color, state-coverage, typography, animation-discipline) into our repo. Wire them into 5 generation/critique skills via a new `dw.craft.requires:` SKILL.md frontmatter field.

**Status:** Draft (ready for execution)
**Target release:** v1.1.1
**Sized:** Medium (1 session, ~3h, no architecture decisions)
**Owner:** fitiodev
**Created:** 2026-05-05
**Source:** open-design adoption analysis (session 2026-05-05); originating upstream is [refero_skill](https://github.com/referodesign/refero_skill) (MIT) → open-design (Apache-2.0) → us (Apache-2.0)

---

## 1. Context

Open-design ships 5 craft docs that codify universal design rules independent of any brand. Each is checkable, hex-coded where applicable, and categorized by severity (P0 must-fix / P1 should-fix / P2 nice-to-fix). Quality is materially higher than what we maintain across scattered `references/` files in our skills, and they're directly applicable to our generation+critique loop:

- `anti-ai-slop.md` — 7 cardinal sins (hex-coded indigo blocklist, gradient hero, emoji feature icons, sans-on-display, rounded card with colored left-border, invented metrics, filler copy) + soft tells + polish tells.
- `color.md` — palette structure 70/10/5/<1, ≤2 accent uses per screen, contrast minimums, dark theme rules.
- `state-coverage.md` — 5 required states (Loading/Empty/Error/Populated/Edge) + 3 form-specific (Untouched/Dirty-valid/Submitted-pending) + test matrix per surface type.
- `typography.md` — multiplicative scale (1.2/1.25), line-height table, letter-spacing rules.
- `animation-discipline.md` — motion budgets and timing rules.

Adopting them is cheaper than maintaining equivalents and yields higher coverage in our own skills.

## 2. Goal

After this feature, the repo has:

- A top-level `craft/` folder with the 5 docs forked verbatim, prefixed by attribution headers.
- A new optional frontmatter field `dw.craft.requires:` that skills declare to indicate which craft docs they consume.
- 5 skills wired to the relevant docs (`theme-critique`, `theme-create`, `theme-port`, `theme-bolder`, `frontend-design`).
- README documents the craft layer.
- Marketplace bumped 1.1.0 → 1.1.1.

## 3. Non-goals

- **Not** rewriting the craft docs to match Fitio's brand or stack. Verbatim fork; deltas are tracked in a separate `craft/notes-flutter.md` (deferred to v1.2 work).
- **Not** wiring all 19 skills — only the 5 that directly generate or evaluate visual output.
- **Not** building a craft-loader runtime — the `dw.craft.requires:` field is metadata that the model reads via `Read` when invoking the skill. No new tooling.
- **Not** tracking the upstream open-design version — fork freezes at the SHA captured in §6 below; sync is manual on demand.
- **Not** publishing as a separate marketplace plugin.

## 4. Requirements

### REQ-01 — Fork the 5 craft docs verbatim

- **REQ-01.1** Create `craft/` at repo root with `anti-ai-slop.md`, `color.md`, `state-coverage.md`, `typography.md`, `animation-discipline.md`.
- **REQ-01.2** Each doc preserves the original content byte-for-byte under the body.
- **REQ-01.3** Each doc gets a 5-line YAML-ish header with: `> Sourced from: <url>`, `> Upstream attribution: refero_skill (MIT)`, `> License: Apache-2.0`, `> Local path: craft/<name>.md`, `> Last sync: <date> at <SHA>`.
- **REQ-01.4** Add a `craft/README.md` explaining the layer (1 paragraph + table of the 5 docs + which skills load each).
- **Verification:** `wc -l craft/*.md` matches upstream content lengths within ±5 lines (header overhead); `grep -L "Sourced from" craft/*.md` returns empty.

### REQ-02 — Define `dw.craft.requires:` frontmatter field

- **REQ-02.1** Document the field in a new `docs/skill-extensions.md` doc (we choose `dw:` namespace to avoid collision with open-design's `od:`).
- **REQ-02.2** Field shape: `dw.craft.requires: [<name1>, <name2>, ...]` — list of bare doc names (without `.md`, without path).
- **REQ-02.3** Loader contract: when a skill with `dw.craft.requires` runs, it reads each `craft/<name>.md` before generating output. Documented in the skill body (no runtime change).
- **Verification:** `docs/skill-extensions.md` exists and documents the schema; one example skill (`theme-create`) shows the field in action.

### REQ-03 — Wire 5 skills to load relevant craft docs

- **REQ-03.1** `skills/theme-critique/SKILL.md` adds `dw.craft.requires: [anti-ai-slop, color, state-coverage, typography]` and the body adds a "Load craft references" instruction.
- **REQ-03.2** `skills/theme-create/SKILL.md` adds `dw.craft.requires: [color, typography, anti-ai-slop]`.
- **REQ-03.3** `skills/theme-port/SKILL.md` adds `dw.craft.requires: [state-coverage, typography]`.
- **REQ-03.4** `skills/theme-bolder/SKILL.md` adds `dw.craft.requires: [color, anti-ai-slop]`.
- **REQ-03.5** `skills/frontend-design/SKILL.md` adds `dw.craft.requires: [anti-ai-slop, color, state-coverage, typography, animation-discipline]`.
- **Verification:** `grep -l "dw:" skills/*/SKILL.md | wc -l` returns 5; each skill body has a "Load craft references" section pointing at the relevant docs.

### REQ-04 — Update STATE.md with decisions

- **REQ-04.1** Add D-11 — `craft/` adoption (verbatim fork, attribution chain, manual sync).
- **REQ-04.2** Add D-12 — `dw:` namespace for our frontmatter extensions, distinct from open-design's `od:`.

### REQ-05 — README: §What changed in v1.1.1

- **REQ-05.1** New section before §What changed in v1.1.0 documenting the craft adoption.
- **REQ-05.2** Add a 1-line entry in the "Optional companions" section pointing at open-design as the upstream source.

### REQ-06 — Validate + bump

- **REQ-06.1** `quick_validate.py` returns 19/19 valid (the new `dw:` field is custom YAML — must not break the strict validator; if it does, place it under a comment marker the validator ignores).
- **REQ-06.2** `marketplace.json` bumped `1.1.0` → `1.1.1`.

## 5. Out of scope (deferred)

- `craft/notes-flutter.md` Flutter-specific addenda (do we need to amend any rule? probably yes for line-height on display, but verify after using). Tracked in v1.2 work.
- Cross-wire to `theme-quieter`, `theme-distill`, `theme-motion`, `ux-writing`. Lower marginal value; only add when a real problem surfaces.
- Auto-sync from upstream open-design. Manual sync is fine at our cadence.

## 6. Source pin

- Upstream repo: `nexu-io/open-design`
- Upstream branch: `main`
- Upstream SHA at fork time: `26636384a8dc3e9b36029c3b6299d4a2005d255a` (captured T-00, 2026-05-06)
- Upstream license: Apache-2.0
- Original upstream attribution: `refero_skill` (MIT)

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| `dw.craft.requires:` breaks `quick_validate.py` strict frontmatter check | Medium | Test on T-04; if breaks, place field under a comment marker the validator ignores OR put it in body section instead of frontmatter |
| Upstream content drifts in incompatible way next sync | Low | Lock to SHA in REQ-01.3; sync explicitly on demand |
| Skills that already have inline anti-slop notes duplicate the craft docs | Medium | T-09 audits each wired skill for redundant inline content; flag for cleanup but don't delete in this feature (deferred) |

## 8. Acceptance criteria

- [ ] REQ-01 to REQ-06 all verified
- [ ] `quick_validate.py` passes on all 19 skills
- [ ] `craft/` folder content matches upstream byte-for-byte (modulo header)
- [ ] At least one skill (`theme-create`) demonstrates the new field with a working example block
- [ ] STATE.md has D-11 and D-12
- [ ] Single commit with `feat(release): v1.1.1 — craft layer adopted from open-design`
