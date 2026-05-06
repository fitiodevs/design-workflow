# Feature: craft-design-context

> Add a 6th doc to `craft/`: `design-context.md` — the canonical "blank-page is last resort" doctrine. Codifies the priority hierarchy of context sources for any hi-fi design task (existing design system → codebase → deployed product → Figma/HTML mockup → vague brief). Inspired by [huashu-design](https://github.com/alchaincyf/huashu-design)'s `references/design-context.md`; **written from scratch** (huashu license is "Personal Use Only" — no fork). Wires into 2 additional skills (`theme-port`, `theme-create`) on top of the 5 wired in `craft-adoption`.

**Status:** Draft (ready for execution)
**Target release:** v1.1.1 (rides along with `craft-adoption`)
**Sized:** Small (rolls into existing v1.1.1 release; ~45 min added to that release's effort)
**Owner:** fitiodev
**Created:** 2026-05-05
**Source:** huashu-design analysis (session 2026-05-05); idea/structure inspired by upstream `references/design-context.md`; content authored from scratch under Apache-2.0 to comply with huashu's "Personal Use Only" license.
**Depends on:** `craft-adoption` v1.1.1 (this is an addition to it). If `craft-adoption` ships first as a separate commit, this becomes v1.1.2; otherwise both ride together.

---

## 1. Context

The user pain (paraphrased from session 2026-05-05): "blank page is the most expensive starting point". Today our skills implicitly expect context (`docs/product.md`, `lib/core/theme/`, an existing palette), but the rule "if you don't have context, get it before generating" is **not codified anywhere**. Júri's discovery flow does this for whole-feature scope; individual skill invocations don't. Result: a `/theme-port` invoked on a Figma frame in a project without `docs/product.md` falls into category-reflex (verde Strava, preto-laranja Nike) and the agent silently generates slop.

Huashu-design captures this exact problem in their `references/design-context.md` with a tight one-page doctrine: **good hi-fi never grows from nothing; the priority of context sources is design-system > codebase > deployed product > brief > nothing.** That doc is short enough to internalize and concrete enough to apply.

We can't fork it (license), but we can author our own under Apache-2.0, citing huashu as the source of the idea, and tighten it for our specific stack (Flutter; reads `docs/product.md` + `lib/core/theme/` + `.design-spec/features/<feature>/discovery.md` if Júri already ran).

## 2. Goal

After this feature:

- `craft/design-context.md` exists, ~80–120 lines, structure: "Why this matters" + 5-tier hierarchy (each tier = what counts as context, where to look, what to extract) + decision rule ("when no context found, STOP — don't generate") + Flutter-specific concrete examples.
- `theme-port`, `theme-create`, `frontend-design` (already wired in v1.1.1), and now `theme-extend` skills declare `design-context` in their `dw.craft.requires:` field.
- The skills' bodies have a "Pre-flight context check" section that explicitly references `craft/design-context.md` and refuses to generate when no context is found.
- README §What changed in v1.1.1 mentions the 6th doc.

## 3. Non-goals

- **Not** rewriting Júri's discovery flow. Discovery is for whole-feature initialization; design-context is for individual skill invocations.
- **Not** auto-running a context scan. The doc is a doctrine the model reads and applies — no new tooling.
- **Not** including motion / typography context (those have their own craft docs already). Design-context is specifically about visual identity context (palette, components, brand voice).
- **Not** forking huashu's prose. New writing, citing source as inspiration.
- **Not** wiring into `theme-bolder`, `theme-quieter`, `theme-distill`, `theme-motion` in this scope. They already have inline context awareness via the bolder/quieter/distill rule sets; adding design-context to them adds redundancy. Defer to a later cleanup if a real problem surfaces.

## 4. Requirements

### REQ-01 — Author `craft/design-context.md`

- **REQ-01.1** File at `craft/design-context.md` (~80–120 lines).
- **REQ-01.2** Attribution header (same template as other craft docs):
  ```
  > **Source:** authored from scratch by design-workflow contributors
  > **Idea inspired by:** [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-context.md` (Personal Use Only — not forked, only the structural idea)
  > **License:** Apache-2.0
  > **Local path:** `craft/design-context.md`
  > **Created:** 2026-05-05
  ```
- **REQ-01.3** Body sections:
  - **Why this matters** (1 paragraph) — articulates the blank-page-is-last-resort thesis with a concrete example (e.g. "/theme-port on a Figma frame without `docs/product.md` → category-reflex slop").
  - **The 5-tier context hierarchy** — for each tier: what it is, where to look in a Flutter project, what to extract, what NOT to extract.
    1. Existing design system (`lib/core/theme/`, `docs/design-tokens.md`, `docs/design-clara.md`)
    2. Codebase (other widgets that already implement similar patterns; read for consistency)
    3. Deployed product (screenshots, store screenshots if no codebase access)
    4. External brief (Figma frame, HTML mockup, written brief in `docs/product.md`)
    5. Vague description (last resort — STOP and ask)
  - **The decision rule** — pseudocode: `if no_context_at_tier_1_through_4: STOP; ask_user; do_not_generate`.
  - **Flutter-specific concrete examples** — 3 short examples mapping a typical request ("/theme-port", "/theme-create", "/theme-extend") to which tiers apply.
  - **Anti-patterns** — common ways the rule gets violated (synthesizing tone from prompt; defaulting to Tailwind indigo; assuming user wants "modern/clean").

### REQ-02 — Update `craft/README.md` to list 6 docs

- **REQ-02.1** Mapping table grows to 6 rows: design-context joins anti-ai-slop, color, state-coverage, typography, animation-discipline.
- **REQ-02.2** Each row includes the new doc + which skills load it.

### REQ-03 — Wire `design-context` into 2 additional skills

- **REQ-03.1** `skills/theme-port/SKILL.md` — add `design-context` to `dw.craft.requires:`. Body gains a "Pre-flight context check" section near the top of Workflow that references `craft/design-context.md` and gates Step 1 on having Tier 1-4 context.
- **REQ-03.2** `skills/theme-create/SKILL.md` — same, with `design-context` added to its requires list. The 8-pre-condition flow already does an implicit context check; the doc reference makes it explicit.
- **REQ-03.3** `skills/theme-extend/SKILL.md` — wire it (theme-extend modifies tokens; needs to know the existing palette before extending). NEW wire (was not in `craft-adoption` v1.1.1).
- **REQ-03.4** Skills wired in v1.1.1 (`theme-critique`, `theme-bolder`, `frontend-design`) gain `design-context` in their requires only if a clear use exists; review case-by-case in T-04. (Default: only `theme-critique` and `frontend-design` get it; `theme-bolder` doesn't because by the time bolder runs, the screen exists and context is implicit.)

### REQ-04 — Update STATE.md

- **REQ-04.1** Add D-11.1 (decision sub-entry) — "design-context.md authored from scratch (not forked) due to huashu license; idea attribution via header".

### REQ-05 — Update README §What changed in v1.1.1

- **REQ-05.1** Mention the 6th craft doc and its origin story.

### REQ-06 — Validate

- **REQ-06.1** `quick_validate.py` 19/19 valid post-changes.
- **REQ-06.2** No version bump beyond what `craft-adoption` already does (still v1.1.1) IF this feature ships in the same commit. Otherwise bumps to v1.1.2.

## 5. Out of scope (deferred)

- Migrating Júri discovery to reference `craft/design-context.md` instead of having its own pre-flight rules. Cleanup task for a later sweep.
- Wiring the doc into `theme-motion`, `ux-writing`, `compose`, `sequence`, `ship`. Each has its own context model already; adding design-context creates redundancy.
- Building a context scanner script (`scripts/scan_context.py` that reads `lib/core/theme/`, `docs/product.md`, etc and reports presence). Useful but premature — first see if the prose doctrine alone fixes 80% of cases.

## 6. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Huashu license: are we accidentally close-paraphrasing? | Low | Write the doc top-down from our own framing (Flutter-specific tier 1; explicit refusal rule); never copy-paste; cite huashu only for the *idea*, not for prose. T-01 reviews diff style. |
| Adding a 6th doc bloats `craft/` past readability | Low | 6 docs × ~150 lines avg ≈ 900 lines total. Acceptable. |
| Skills' "Pre-flight context check" sections duplicate existing prereqs already in body | Medium | T-04 audits each wired skill; the new section either replaces existing prereq prose or links to it. No duplication. |
| Doc reads as Flutter-only and excludes future React Native users | Medium | Tier definitions are stack-agnostic; only the "where to look" examples are Flutter-flavored. Future adapter work (v1.4) can add a Tier 1.5 for stack-specific paths. |

## 7. Acceptance criteria

- [ ] REQ-01..REQ-06 all verified
- [ ] `craft/design-context.md` exists, attribution header present, 5-tier hierarchy clear, decision rule explicit
- [ ] `craft/README.md` lists 6 docs
- [ ] `theme-port`, `theme-create`, `theme-extend`, `theme-critique`, `frontend-design` all reference design-context
- [ ] STATE.md has D-11.1 entry
- [ ] If shipping in same commit as craft-adoption: commit message reads `feat(release): v1.1.1 — craft layer adopted from open-design (+ design-context)`. Else: separate commit `feat: add craft/design-context.md doctrine` targeting v1.1.2.
