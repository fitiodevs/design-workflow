# Feature: design-school-library

> Build a library of 12 **design philosophy schools** (Pentagram / Müller-Brockmann / Kenya Hara / Brutalism / Memphis / Active Theory / etc) parallel to the v1.2.0 brand-systems library. Each school captures: philosophy nucleus, prompt DNA, token implications, slop traps, and an **execution-path matrix** rating viability across 7 scenarios (Flutter UI · HTML mockup · PPT · PDF · Infographic · Cover · AI-image-gen). Inspired by [huashu-design](https://github.com/alchaincyf/huashu-design)'s `references/design-styles.md`; **written from scratch** under Apache-2.0 (huashu license forbids fork).

**Status:** Draft (ready for execution; v1.5 release; defer until v1.4 ships)
**Target release:** v1.5.0
**Sized:** Large (~14-18h, comparable to v1.2.0 in shape but content-authoring-heavy)
**Owner:** fitiodev
**Created:** 2026-05-05
**Source:** huashu-design analysis (session 2026-05-05); structural idea inspired by upstream `references/design-styles.md` (Personal Use Only — not forked).
**Depends on:** v1.4.0 shipped (the adapter contract simplifies the Flutter-emission step). Strongly preferred but not strictly required — the library is consumable as-is for HTML mockups (Clara), PDF/PPT (external tools), and as a reference doc.

---

## 1. Context

The v1.2.0 inspiration library covers **brand systems** (Apple, Stripe, Notion, Linear, Claude, …). 71 entries, each one a specific company's identity. Useful for "make it look like X". But:

- Brand systems can't blend cleanly. "Stripe + Notion" doesn't compose because both are specific identities.
- Brand systems are a snapshot. Linear's design will drift; our fork freezes a moment.
- For non-app artifacts (marketing decks, sponsorship pitch PDFs, event covers, product launch infographics), brand-imitation is rarely the goal — the user wants the *aesthetic philosophy* of an actual design school.

Huashu-design captures this gap with 20 design schools — Pentagram (Bierut), Müller-Brockmann (Swiss grid), Kenya Hara (negative space), Active Theory (kinetic), Memphis, Brutalism, etc. Each school comes with:

1. **Philosophy nucleus** — 1 sentence summarizing the school's thesis ("dados não são decoração; são material de construção" for Information Architects).
2. **Core characteristics** — 4-6 bullets of concrete visual signatures.
3. **Prompt DNA** — a paragraph the agent uses verbatim as part of the system prompt.
4. **Execution-path matrix** — star ratings across 7 scenarios + best path recommendation (HTML / AI-gen / hybrid).

The matrix is the most useful piece — it tells you "Pentagram is HTML-best for web, AI-gen-poor"; "Active Theory is AI-gen-best, HTML-poor". It composes brilliantly with our pipeline because we have HTML-side (Clara → tweaks → theme-port) AND can recommend AI-gen tools without bundling them.

The user (session 2026-05-05) explicitly wants the matrix to **keep all 7 columns** — even the PPT/PDF columns that don't apply to Flutter — because marketing/commercial use of the library is a real use case. We accommodate by treating the library as a **multi-target reference**: Flutter+HTML are *executable* (we ship the path); PPT/PDF/Infographic/Cover are *guidance* (matrix tells you "use HTML path with [external tool]").

## 2. Goal

After this feature:

- `design-systems-schools/` folder (separate from `design-systems/` brands library) contains 12 hand-authored school entries in standardized format.
- Each entry has: philosophy + characteristics + prompt DNA + token implications (Flutter) + execution-path matrix + slop traps.
- A new translator path: `theme-create --inspired-by-school <slug>` reads a school file, runs translator (similar shape to v1.2.0 but driven by prompt DNA + token implications instead of explicit hex), emits AppColors proposal.
- Clara (`/frontend-design`) gets a `--school <slug>` flag that loads the school's prompt DNA into her HTML emission.
- The execution-path matrix is referenced from a top-level `docs/design-schools-execution-paths.md` doc explaining how to use each path (HTML stays in our pipeline; PPT/PDF/AI-gen routes to recommended external tools).
- README documents the school library + how it composes with brand library.
- Marketplace bumped 1.4.0 → 1.5.0.

## 3. Non-goals

- **Not** building PPT/PDF/Infographic/Cover/AI-image generators. The matrix points at those scenarios; user picks an external tool (we recommend known-good ones in the docs).
- **Not** forking huashu's prose. New writing per school, citing huashu as idea source.
- **Not** all 20 of huashu's schools. Curate 12 maximizing scenario coverage.
- **Not** auto-blending schools (`--school müller-brockmann + memphis`). v1.6 candidate; needs synthesis logic.
- **Not** replacing the brand library (v1.2.0). Schools and brands serve different needs; both stay.
- **Not** generating animations/motion from school metadata. Future v1.6 work.
- **Not** ranking schools by quality (every school is "good" for its scenario by definition).

## 4. Requirements

### REQ-01 — Curate 12 schools

- **REQ-01.1** Pick schools maximizing spread across scenario column ratings:

  | School | Web (Flutter UI) | HTML mockup | PPT | PDF | Infographic | Cover | AI-image-gen |
  |---|---|---|---|---|---|---|---|
  | 01 Pentagram (Bierut) | ★★★ | ★★★ | ★★★ | ★★☆ | ★★☆ | ★★★ | ★☆☆ |
  | 02 Müller-Brockmann (Swiss grid) | ★★☆ | ★★★ | ★★★ | ★★★ | ★★★ | ★★☆ | ★☆☆ |
  | 03 Kenya Hara (negative space) | ★★☆ | ★★★ | ★★★ | ★★★ | ★☆☆ | ★★★ | ★☆☆ |
  | 04 Information Architects (typography) | ★★★ | ★★★ | ★☆☆ | ★★★ | ★☆☆ | ★☆☆ | ★☆☆ |
  | 05 Brutalism (web brutalist) | ★★★ | ★★★ | ★☆☆ | ★☆☆ | ★☆☆ | ★★☆ | ★★☆ |
  | 06 Memphis (postmodern) | ★★☆ | ★★★ | ★★☆ | ★☆☆ | ★★☆ | ★★★ | ★★★ |
  | 07 Sagmeister & Walsh (expressive) | ★★☆ | ★★★ | ★★★ | ★☆☆ | ★★☆ | ★★★ | ★★★ |
  | 08 Active Theory (kinetic) | ★★★ | ★☆☆ | ★☆☆ | ★☆☆ | ★☆☆ | ★★☆ | ★★★ |
  | 09 Editorial (Wired/Apple-mag) | ★★☆ | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★☆ |
  | 10 Locomotive (kinetic-narrative web) | ★★★ | ★★☆ | ★☆☆ | ★☆☆ | ★☆☆ | ★★☆ | ★★☆ |
  | 11 Takram (data-poetic) | ★★★ | ★★★ | ★★★ | ★★★ | ★★☆ | ★★☆ | ★☆☆ |
  | 12 Atelier-Zero (collage-editorial) | ★★☆ | ★★★ | ★★★ | ★★★ | ★★☆ | ★★★ | ★★☆ |

  Coverage rationale: 4 schools strong on Flutter (Pentagram, IA, Brutalism, Locomotive, Active Theory, Takram); 8 schools strong on PPT/PDF/Cover (Müller-Brockmann, Kenya Hara, Pentagram, Editorial, Sagmeister, Memphis, Atelier-Zero, Takram); 4 schools strong on AI-gen (Memphis, Sagmeister, Active Theory) — broad spread.

- **REQ-01.2** Each school authored from scratch in `design-systems-schools/<slug>/SCHOOL.md` (different filename from `DESIGN.md` of brands library to avoid confusion).
- **REQ-01.3** Standard sections per file:
  1. Attribution header (idea inspired by huashu, authored under Apache-2.0)
  2. Philosophy nucleus (1 sentence)
  3. Core characteristics (4-6 bullets)
  4. Prompt DNA (1-2 paragraphs the model loads as system prompt extension)
  5. Token implications (Flutter-specific: which AppColors roles dominate, type pair recommendation, spacing scale tendency)
  6. Execution-path matrix (7-column table with the school's row, plus prose for each non-zero scenario explaining the recommended approach)
  7. Slop traps (3-5 bullets — concrete failure modes)
  8. Best paired with (other schools in the library that compose well)
- **REQ-01.4** `design-systems-schools/README.md` — index, category table (group by primary scenario strength: Flutter-strong / Print-strong / AI-gen-strong / Versatile), philosophy summary per school.

### REQ-02 — Build the school translator

- **REQ-02.1** `scripts/school_md_to_appcolors.py` reads a `SCHOOL.md` and emits a Flutter-only proposal: AppColors values inferred from the school's "Token implications" section + Flutter-specific tier-1 defaults; rationale citing the school philosophy.
- **REQ-02.2** Inference is **constraint-based, not literal**: schools don't declare hex codes (those are brand-specific); they declare *constraints* ("Müller-Brockmann = neutrals 80%+, accent <10%, accent must be primary or saturated red, contrast ≥7:1"). Translator generates a palette that **satisfies the constraints**.
- **REQ-02.3** Re-uses existing `scripts/check_contrast.py` and `scripts/oklch_to_hex.py`.
- **REQ-02.4** Output format: same `proposal.json` + `rationale.md` shape as v1.2.0 for consistency. Rationale cites school philosophy + which constraints drove which token choices.
- **REQ-02.5** WCAG re-validation always runs (REQ-A.4 carry-over from v1.2.0 spec).

### REQ-03 — Add `--inspired-by-school <slug>` to `theme-create`

- **REQ-03.1** Flag analogous to v1.2.0's `--inspired-by` but routes to school translator.
- **REQ-03.2** Workflow: read school file → run translator → present rationale → ask 4 remaining pre-conditions (purpose/audience/invariants/coexistence) → emit Dart.
- **REQ-03.3** Skill body documents both flags side-by-side; user reads the school library README to choose.
- **REQ-03.4** Optional: `--inspired-by-school <slug-A> + <slug-B>` blend support is **out of scope** for v1.5. Defer to v1.6.

### REQ-04 — Add `--school <slug>` to `frontend-design` (Clara)

- **REQ-04.1** When `--school <slug>` is set, Clara loads the school's prompt DNA section into her system prompt for that invocation.
- **REQ-04.2** Output HTML mockup carries `<!-- school: <slug> -->` comment in head for traceability.
- **REQ-04.3** Pairs with `theme-create --inspired-by-school` — recommended workflow: same school for palette + mockup keeps coherence.

### REQ-05 — Execution-path doc

- **REQ-05.1** `docs/design-schools-execution-paths.md` — top-level doc explaining: how to read the matrix; when to pick HTML path (in our pipeline) vs external tool (PPT/PDF/AI-gen); recommendations for external tools (Marp/Slidev for PPT, Pandoc/Typst for PDF, Midjourney/SDXL for AI-image, etc).
- **REQ-05.2** This doc bridges the gap between "you picked Müller-Brockmann for an annual report PDF" and "what tool produces the PDF" — we explicitly DO NOT ship the PDF generator but we recommend a known-good one and provide a Markdown template seeded with the school's prompt DNA.

### REQ-06 — STATE.md decisions

- **REQ-06.1** D-23 — Schools library separate from brands library: different folder (`design-systems-schools/` vs `design-systems/`), different file (`SCHOOL.md` vs `DESIGN.md`), different translator. Rationale: different abstraction layer (philosophy vs identity).
- **REQ-06.2** D-24 — School entries authored from scratch (huashu license); Apache-2.0 citation in attribution header.
- **REQ-06.3** D-25 — Multi-target matrix is reference-only for non-Flutter rows; we don't ship PPT/PDF/AI-gen generators, only recommend external tools.

### REQ-07 — README + theme-create + frontend-design updates

- **REQ-07.1** README §What changed in v1.5.0 documents the schools library + flags + execution-path doc.
- **REQ-07.2** New top-level "Design schools library" section above the v1.2.0 "Inspiration library" section. Explains philosophy-vs-brand split.
- **REQ-07.3** `skills/theme-create/SKILL.md` Triggers section adds new flag.
- **REQ-07.4** `skills/frontend-design/SKILL.md` Triggers section adds new flag.

### REQ-08 — Validate + bump

- **REQ-08.1** `quick_validate.py` 20/20 valid (no skill count change in v1.5; only flag additions).
- **REQ-08.2** Translator smoke test on 3 sample schools (Müller-Brockmann, Brutalism, Editorial) — manual review for sanity.
- **REQ-08.3** `marketplace.json` bumped 1.4.0 → 1.5.0.

## 5. Out of scope (deferred)

- **School blending** (`--inspired-by-school müller-brockmann + memphis`) — v1.6.
- **Auto-import 8 remaining huashu schools** (Stamen, Locomotive, Resn, Field.io, Experimental Jetset, Build, Zach Lieberman, Raven Kwok, Ash Thorp, Territory Studio, Irma Boom, Neo Shen) — add on demand if usage patterns surface.
- **Build PPT/PDF/Infographic/Cover/AI-gen generators in-repo** — explicit non-goal. We document; we don't ship multimedia.
- **Mood-board image library** — schools are described in text; no bundled imagery.
- **Live-preview of school's prompt DNA in Clara** — frontend-design + tweaks already cover the explore-variants story.

## 6. Source pin

- Idea source: [huashu-design](https://github.com/alchaincyf/huashu-design) `references/design-styles.md` (Personal Use Only)
- Our license: Apache-2.0
- Authoring: from scratch per school; idea attribution in each file's header
- 12 picked from huashu's 20: Pentagram, Müller-Brockmann, Kenya Hara, Information Architects, Brutalism (open category), Memphis (open), Sagmeister, Active Theory, Editorial (open), Locomotive, Takram, Atelier-Zero (the last is open-design's hand-curated, not huashu's; but pairs naturally)

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Authoring 12 school entries from scratch is content-heavy and quality varies | High | Time-box each entry to 30-45 min; use a template (T-02 ships); review each against huashu reading once before finalizing. If quality drops, ship 8 schools first as v1.5.0, defer 4 to v1.5.1. |
| Constraint-based translator harder than v1.2.0's literal-mapping | High | Start with 1 school (Müller-Brockmann is most rule-based) as proof; if constraints synthesize sane palettes, scale to 12. If not, fall back to "translator emits a partial proposal + lots of user pre-conditions". |
| Matrix columns we don't ship (PPT/PDF/AI-gen) confuse users — they may expect we generate those | High | Clear language in `docs/design-schools-execution-paths.md` and README; the matrix says "★★★ = strong fit" not "★★★ = we generate it". Recommend external tools by name. |
| Schools library overlaps with `craft/` philosophical content (color discipline, etc) | Low | Schools are *aesthetic philosophies* (visual identity choices); craft is *checkable rules* (anti-slop, contrast minimums). Different layers. T-01 review enforces non-overlap. |
| 12 school entries are too many — readability of the picker degrades | Low | Test with `theme-create --browse-schools` showing the 12 grouped by primary scenario; if hard to navigate, reduce to 8. |
| Adding a parallel translator doubles maintenance burden | Medium | T-09 keeps both translators sharing helpers (`scripts/check_contrast.py`, `scripts/oklch_to_hex.py`); only the inference layer differs. |

## 8. Acceptance criteria

- [ ] REQ-01..REQ-08 all verified
- [ ] 12 school entries in `design-systems-schools/<slug>/SCHOOL.md`, each ≥150 lines with all 8 standard sections
- [ ] Translator produces sane proposals for Müller-Brockmann, Brutalism, Editorial samples (manual review)
- [ ] `theme-create --inspired-by-school müller-brockmann` works end-to-end
- [ ] `frontend-design --school memphis` produces a mockup whose visual character matches Memphis (manual review)
- [ ] `docs/design-schools-execution-paths.md` exists with external-tool recommendations
- [ ] STATE.md has D-23, D-24, D-25
- [ ] Single commit: `feat(release): v1.5.0 — design schools library + multi-target execution paths`
