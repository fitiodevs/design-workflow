# Feature: inspiration-library

> Curate ~20 of open-design's 71 `DESIGN.md` brand systems into our `design-systems/` folder, build a translator from DESIGN.md (CSS custom properties) to AppColors (Flutter), and add `--inspired-by <slug>` plus `--browse [<category>]` flags to `/theme-create` so palette creation starts from a characterized reference instead of a blank page.

**Status:** Draft (ready for execution)
**Target release:** v1.2.0
**Sized:** Large (multi-component, ~6-8h, translator + library + skill integration)
**Owner:** fitiodev
**Created:** 2026-05-05
**Source:** open-design adoption analysis (session 2026-05-05); upstream `nexu-io/open-design` design-systems folder (Apache-2.0); originating sources cited per-file.
**Depends on:** v1.1.1 (`craft-adoption`) shipped — this feature wires craft references into the new flags' workflow.

---

## 1. Context

Today `/theme-create` solves the blank-page problem with an 8-step pre-condition interview (purpose, audience, tone-extreme, invariants, differentiation, coexistence, color strategy, anti-category-reflex). It works but is expensive — every new theme costs the user 5-10 minutes of articulation before the first hex shows up. The user's stated pain (session 2026-05-05): "hoje só temos 2 temas (claro+escuro), ter os 71 do open-design como inspiração corta o esforço de decidir qual tema será o próximo."

Open-design ships 71 `DESIGN.md` files (Apache-2.0), each a complete 9-section spec covering Visual Theme & Atmosphere · Color Palette & Roles · Typography · Component Stylings · Layout · Depth/Elevation · Do's and Don'ts · Responsive · Agent Prompt Guide. Categorized in 9 buckets: AI&LLM, Dev Tools, Productivity, Backend/Data, Design/Creative, Fintech, E-Commerce, Media, Automotive.

The library is genuinely high-quality (each entry is a paragraph of caracterização + 30+ tokens with hex + roles + usage rationale). But it's CSS-first (`--accent`, `--bg`, `--fg`) and we're Flutter-first (`brandDefault`, `bgSurface`, `textPrimary` × 29 tokens). A translator bridges the gap.

## 2. Goal

After this feature, `/theme-create` has three modes:

1. **From scratch (existing flow)** — 8 pre-conditions → OKLCH → output. Unchanged.
2. **`--inspired-by <slug>`** — read `design-systems/<slug>/DESIGN.md`, run the translator, present the resulting `AppColors` proposal + a rationale doc citing the inspiration, validate WCAG, ask user to approve.
3. **`--browse [<category>]`** — list available design systems (filtered by category if given), let user pick one, then drop into mode 2.

## 3. Non-goals

- **Not** forking all 71. Curate 20 — broad coverage of categories, drop entries that overlap heavily (e.g. only one fintech example) or are too brand-coupled to make sense as inspiration (Bugatti, BMW — keep one Automotive max).
- **Not** automating mood-blending (e.g. "Stripe + Linear hybrid"). v1.3 candidate; needs synthesis logic that's its own feature.
- **Not** importing the rest of the 9 sections (Components/Layout/Depth/Responsive). Phase 1 only consumes Visual Theme + Color Palette + Typography. Other sections get cited in the rationale doc but not auto-applied to AppColors.
- **Not** auto-syncing from upstream — manual sync at sweep cadence (same as `craft/`).
- **Not** a UI for browse — `--browse` is a CLI/text interaction (list, ask, pick).
- **Not** changing the existing 8-pre-condition flow when `--inspired-by` is absent.

## 4. Requirements

### REQ-01 — Curate 20 DESIGN.md files

- **REQ-01.1** Pick 20 entries from upstream's 71 that maximize spread:

  | Category | Count | Picks (proposed; finalized in T-01) |
  |---|---|---|
  | AI & LLM | 3 | claude · cohere · mistral-ai |
  | Dev Tools | 3 | linear-app · vercel · raycast |
  | Productivity / SaaS | 2 | notion · cal |
  | Backend / Data | 2 | supabase · sentry |
  | Design / Creative | 2 | figma · framer |
  | Fintech | 2 | stripe · revolut |
  | E-Commerce / Retail | 2 | airbnb · nike |
  | Media / Consumer | 2 | apple · spotify |
  | Automotive | 1 | tesla |
  | Editorial / Hand-curated | 1 | atelier-zero (open-design hand-author) |

- **REQ-01.2** Each curated DESIGN.md is forked verbatim into `design-systems/<slug>/DESIGN.md` with the same attribution-header convention as `craft/`.
- **REQ-01.3** `design-systems/README.md` documents the library — what's bundled, the category index, how `--inspired-by` consumes them.
- **Verification:** `ls design-systems/ | grep -v README.md | wc -l` = 20; each subdir has a `DESIGN.md` whose first 8 lines match the attribution header template.

### REQ-02 — Build the translator script

- **REQ-02.1** `scripts/design_md_to_appcolors.py` reads a `design-systems/<slug>/DESIGN.md` and emits two artifacts:
  1. A `proposal.json` mapping the 29 `AppColors` tokens to hex values inferred from the source.
  2. A `rationale.md` citing which source token mapped to which AppColors token + which Fitio-specific tokens (gameAccent etc) need user input because the source doesn't cover them.
- **REQ-02.2** Mapping table baseline:

  | DESIGN.md role | AppColors token |
  |---|---|
  | `--accent` / Primary brand | `brandDefault` |
  | (variant warmer) | `brandMuted` |
  | (light text-on-brand) | `brandOnColor` |
  | `--bg` / Page background | `bgBase` |
  | `--surface` / Card surface | `bgSurface` |
  | (raised surface) | `bgSurfaceRaised` |
  | (input surface) | `bgInput` |
  | `--fg` / Primary text | `textPrimary` |
  | `--muted` / Secondary text | `textSecondary` |
  | (tertiary text) | `textMuted` |
  | (text on brand surface) | `textOnBrand` |
  | `--border` / Default border | `borderDefault` |
  | (strong border) | `borderStrong` |
  | (focus ring) | `borderFocus` |
  | `--success` / `--warn` / `--danger` | `feedbackSuccess` / `feedbackWarning` / `feedbackError` |
  | (`--info`) | `feedbackInfo` |
  | (muted variants) | `feedbackXxxMuted` |
  | Game-specific (no source) | flag for user input |

- **REQ-02.3** Inference order: (1) explicit role mention in DESIGN.md, (2) hex extracted from "Color Palette & Roles" section by regex, (3) WCAG check on derived pair → if fails, propose a darkened/lightened alternative + note it.
- **REQ-02.4** Run WCAG re-validation on the 12 mandatory pairs × 2 modes (24 total) using existing `scripts/check_contrast.py`. Failed pairs are flagged in `rationale.md`, never silently emitted.
- **REQ-02.5** Light/dark inference:
  - If source has both modes (most do — Apple, Notion, Linear), translate both.
  - If source has only one mode, derive the other by L flip (OKLCH lightness flip via existing `scripts/oklch_to_hex.py`) and flag in rationale.
- **REQ-02.6** Output is a Dart `AppColors` snippet ready to paste, OR a JSON proposal the skill body presents to user for tweaks.
- **Verification:**
  - `python3 scripts/design_md_to_appcolors.py design-systems/claude/DESIGN.md > /tmp/out.json` exits 0.
  - `jq '.tokens.light | length' /tmp/out.json` = 29.
  - `python3 scripts/check_contrast.py --json /tmp/out.json` reports zero AA failures (or each failure is in the rationale).

### REQ-03 — Add `--inspired-by <slug>` flag to `/theme-create`

- **REQ-03.1** `skills/theme-create/SKILL.md` body documents the flag in Triggers + workflow.
- **REQ-03.2** Workflow when flag is present:
  1. Validate slug exists (`design-systems/<slug>/DESIGN.md`).
  2. Read DESIGN.md + run translator → `proposal.json` + `rationale.md`.
  3. Present rationale to user, highlighting: (a) the visual theme paragraph from source, (b) the 29 mapped tokens, (c) any Fitio-specific tokens needing user input, (d) any WCAG warnings.
  4. Ask user to approve as-is OR tweak specific tokens before emitting Dart snippet.
  5. On approval, run the standard `/theme-create` final steps (anti-AI-slop checklist, ficha in `docs/themes/<slug>.md`, rollout plan).
- **REQ-03.3** Skip the 8 pre-conditions when `--inspired-by` is set (the source already encodes most of them; only the project-specific ones — invariants, coexistence — are still asked).

### REQ-04 — Add `--browse [<category>]` flag to `/theme-create`

- **REQ-04.1** When `--browse` is invoked without args: list all 20 design systems grouped by category, ask user to pick a slug.
- **REQ-04.2** When `--browse <category>` is invoked: list only that category's entries, ask user to pick.
- **REQ-04.3** After pick, drop into the `--inspired-by <slug>` workflow above.
- **REQ-04.4** Categories sourced from each DESIGN.md's `> Category: <name>` line (parsed in T-09 helper).

### REQ-05 — STATE.md decisions

- **REQ-05.1** D-13 — DESIGN.md library: 20-entry curated subset of upstream open-design 71, attribution chain, manual sync.
- **REQ-05.2** D-14 — Translator semantics: priority order (explicit role > regex > WCAG-corrected fallback); failed mappings always flagged, never silent.

### REQ-06 — README + theme-create updates

- **REQ-06.1** README §What changed in v1.2.0 documents the library + flags.
- **REQ-06.2** Add a top-level "Inspiration library" section with the category table.
- **REQ-06.3** `skills/theme-create/SKILL.md` Triggers section adds the new flags; description mentions both modes.

### REQ-07 — Validate + bump

- **REQ-07.1** `quick_validate.py` 19/19 valid post-changes.
- **REQ-07.2** Translator unit-tested via at least 3 source samples (claude, linear-app, stripe) — outputs reviewed for sanity.
- **REQ-07.3** `marketplace.json` bumped 1.1.1 → 1.2.0.

## 5. Out of scope (deferred)

- **Mood blending** (`--blend stripe + linear`) — needs synthesis logic + user-facing arbitration. v1.3 candidate.
- **Auto-import 9 non-color sections** (components/layout/depth/responsive) — these inform the rationale doc but don't affect AppColors. Touching them needs a different design.
- **Live HTML preview of inspiration** — that's the `tweaks` job (v1.3.0).
- **Adding remaining 51 systems** — open as 1-line backlog items, add on demand.
- **Validating against AppMotion / AppCurves** — DESIGN.md has motion notes but mapping to Flutter motion tokens is a separate skill (`theme-motion` adapter work, deferred to v1.4).

## 6. Source pin

- Upstream repo: `nexu-io/open-design`
- Upstream branch: `main`
- Upstream SHA at fork time: **TBD — capture during T-00**
- Upstream path: `design-systems/<slug>/DESIGN.md`
- Original attribution per file: cited in upstream README.md (mostly `bergside/awesome-design-skills` MIT and `VoltAgent/awesome-design-md` via `getdesign@latest` MIT, plus `tw93/kami` MIT).

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| DESIGN.md role names don't match cleanly to AppColors (e.g. source uses "Coral Accent" with no `--accent` literal) | High | REQ-02.3 inference chain: regex on "Color Palette & Roles" section is tolerant; failures flagged in rationale, never silent. T-04 builds the regex against 5 real samples. |
| Translator produces tokens that fail WCAG even after L-flip | Medium | REQ-02.4 always re-validates; failed pairs are surfaced; user decides if to accept (sometimes a sub-brand intentionally fails AAA on display). |
| Curated set of 20 over-represents AI/SaaS | Medium | REQ-01.1 caps each category; cross-check at T-01 before forking. |
| Source's typography names don't exist in our project (e.g. `Anthropic Serif` is a custom face) | Low | DESIGN.md has fallback hints (Georgia for serif, Inter for sans). Translator emits font tokens as comments + flags. User decides. |
| 20 design systems × 9 sections = ~600KB of markdown — bloats repo | Low | 20 × ~12KB = 240KB total. Acceptable. |

## 8. Acceptance criteria

- [ ] REQ-01..REQ-07 all verified
- [ ] 20 DESIGN.md files in `design-systems/`, each with attribution header
- [ ] Translator script unit-tested on claude, linear-app, stripe — outputs sane
- [ ] `theme-create --inspired-by claude` runs end-to-end and produces a Dart `AppColors` snippet
- [ ] `theme-create --browse fintech` lists 2 entries (stripe, revolut)
- [ ] STATE.md has D-13 + D-14
- [ ] Single commit: `feat(release): v1.2.0 — DESIGN.md inspiration library + translator`
