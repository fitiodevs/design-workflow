# Tasks: design-school-library

> Atomic, sequenced. ≤30 min cada. Verificação binária.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.5.0` (criar em T-00)
**Target:** v1.5.0
**Depends on:** v1.4.0 shipped (recommended; not strict).

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Safety net + scope confirm

### T-00 ✅ Tag rollback + finalize 12-school list
- **Action:**
  ```bash
  git tag pre-v1.5.0
  ```
  Then finalize the 12 slugs (per spec REQ-01.1) — confirm each maps to either a real upstream entry in huashu OR an open-design hand-curated entry (atelier-zero). Lock the list under §"Confirmed slugs" header in this file. Decisions logged.
- **Verify:** tag exists; 12 confirmed slugs documented.
- **Refs:** spec REQ-01.1
- **Blocks:** all

### T-01 ✅ Read huashu's `design-styles.md` once for reference
- **Action:** `gh api repos/alchaincyf/huashu-design/contents/references/design-styles.md --jq '.content' | base64 -d > /tmp/huashu-design-styles.md` — read it through carefully, take mental notes per the 12 picked schools. **Close the file before authoring** to avoid prose-similarity.
- **Verify:** notes captured at top of this file (or in `/tmp/v1.5-notes.md`); decision: each school's philosophy nucleus has been internalized in our own words before authoring.
- **Refs:** spec §6 risk "huashu license"

### T-02 ✅ Author SCHOOL.md template
- **Action:** create `/tmp/school-template.md` matching design §"SCHOOL.md template". This template gets copied for each school in T-03..T-14.
- **Verify:** template file exists with all 8 sections + attribution header + matrix scaffold.
- **Refs:** spec REQ-01.3

---

## Onda 1 — Author 12 school entries (paralelizável but sequence by category for QA)

> Each school takes ~30-40 min. Pair-author when possible (1 fully done before moving on, to refine the template).

### T-03 ✅ Author Müller-Brockmann (Swiss grid)
- **Action:** copy template, fill all 8 sections; this is the canonical "constraint-rich" school — use it to validate the template structure. Time-box 45 min.
- **Verify:** `wc -l design-systems-schools/muller-brockmann/SCHOOL.md` ≥ 150; all 8 sections present; matrix has 7-column row; constraints in "Token implications" are concrete and parseable.
- **Refs:** REQ-01.2

### T-04 ✅ Author Pentagram (Bierut)
- **Action:** copy template, fill in. Note: typography-led; less constraint-heavy than Müller-Brockmann, more about discipline.
- **Verify:** mesma checagem.

### T-05 ✅ Author Kenya Hara (negative space)
- **Action:** template + content. Distinct character: Japanese minimalism, ample whitespace, refined neutrals.

### T-06 ✅ Author Information Architects
- **Action:** typography-first, data-respect-first.

### T-07 ✅ Author Brutalism (web brutalist)
- **Action:** anti-school → opinionated. Concrete: monospace, raw HTML aesthetic, asymmetric, system fonts, no-radius.

### T-08 ✅ Author Memphis (postmodern)
- **Action:** color-bold, geometric pattern, 80s-postmodern.

### T-09 ✅ Author Sagmeister & Walsh (expressive)
- **Action:** type-as-image, hand-rendered moments, color-saturated.

### T-10 ✅ Author Active Theory (kinetic)
- **Action:** motion-first, AI-gen-friendly per matrix; heavy on Locomotive-style transitions.

### T-11 ✅ Author Editorial (Wired/Apple-mag)
- **Action:** magazine pacing, serif headlines, broad imagery, generous spacing.

### T-12 ✅ Author Locomotive (kinetic-narrative web)
- **Action:** scroll-driven storytelling, parallax, animated entries.

### T-13 ✅ Author Takram (data-poetic)
- **Action:** data-as-art, calm visualization, narrative diagrams.

### T-14 ✅ Author Atelier-Zero (collage-editorial — open-design hand-curated)
- **Action:** distinct attribution (open-design's own hand-author, not 3rd-party); collage paper canvas, plaster imagery, oversized italic-mixed display, Roman-numeral markers.

### T-15 ✅ Write `design-systems-schools/README.md`
- **Action:** category index grouping the 12 by primary scenario strength (Flutter / Print / AI-gen / Versatile); 1-paragraph philosophy per school for the picker.
- **Verify:** index has 12 rows; grouped by 4 categories.
- **Refs:** REQ-01.4

---

## Onda 2 — Translator

### ### T-16 ⬜ Stub `scripts/school_md_to_appcolors.py`
- **Action:** scaffolding per design §"Translator design (constraint-based)". Argparse + 5 phase stubs.
- **Verify:** `python3 scripts/school_md_to_appcolors.py --help` runs; `--dry-run` exits 0.
- **Refs:** REQ-02.1

### ### T-17 ⬜ Implement `parse_school_md`
- **Action:** parse the 8 sections; extract token-implications bullets specifically.
- **Verify:** running on Müller-Brockmann returns ≥4 token-implications bullets parsed.
- **Refs:** REQ-02

### ### T-18 ⬜ Implement `extract_constraints`
- **Action:** translate each token-implications bullet into a Constraint dataclass: {target_token, operator, value} (e.g. `{"target": "brandDefault", "constraint": "saturation_min", "value": 0.8}`).
- **Verify:** running on Müller-Brockmann returns ≥6 Constraints extracted.
- **Refs:** REQ-02.2

### ### T-19 ⬜ Implement `synthesize_palette` constraint solver
- **Action:** for each token, OKLCH-iterate values within constraint bounds until WCAG passes. Cap iterations at 5; emit partial + flag if no convergence.
- **Verify:** running on Müller-Brockmann emits a valid 29-token AppColors proposal with no convergence failures.
- **Refs:** REQ-02.2, design D-D

### T-20 ✅ Implement `validate_wcag` + `write_artifacts`
- **Action:** reuse `scripts/check_contrast.py`; emit proposal.json + rationale.md per v1.2.0 conventions.
- **Verify:** files exist; rationale cites school philosophy + which constraints drove which token choices.
- **Refs:** REQ-02.3, REQ-02.5

### T-21 ✅ Smoke test on 3 schools
- **Action:** run translator on Müller-Brockmann, Brutalism, Editorial. Manual review for: (a) palette character matches school description, (b) no AI-default colors (no Tailwind indigo), (c) WCAG on 12 mandatory pairs all pass.
- **Verify:** 3 dirs in `/tmp/school-test/`; manual review notes saved; zero "all-neutral-gray fallback" cases.
- **Refs:** spec §8

---

## Onda 3 — Wire `theme-create` + `frontend-design`

### T-22 ✅ Add `--inspired-by-school <slug>` to theme-create
- **Action:** edit `skills/theme-create/SKILL.md`:
  - description mentions both `--inspired-by` and `--inspired-by-school`
  - Triggers section adds the new flag
  - new "## Workflow — --inspired-by-school mode" section: validate slug exists in `design-systems-schools/`, run translator, present rationale, ask 4 remaining pre-conditions, emit Dart
- **Verify:** `python3 $VAL skills/theme-create/` valid; `grep -c "inspired-by-school" skills/theme-create/SKILL.md` ≥ 3.
- **Refs:** REQ-03

### T-23 ✅ Add `--school <slug>` to frontend-design (Clara)
- **Action:** edit `skills/frontend-design/SKILL.md`:
  - Triggers section adds `--school <slug>`
  - new "## --school mode" section explaining: load school's Prompt DNA into system prompt, emit `<!-- school: <slug> -->` HTML comment, sticky session via `.design-spec/features/<feature>/active-school.txt`.
- **Verify:** valid + `grep -c "--school" skills/frontend-design/SKILL.md` ≥ 3; `grep -c "Prompt DNA" skills/frontend-design/SKILL.md` ≥ 1.
- **Refs:** REQ-04, design D-F

---

## Onda 4 — Execution-path doc

### T-24 ✅ Write `docs/design-schools-execution-paths.md`
- **Action:** sections:
  1. How to read the 7-column matrix
  2. When HTML path (in our pipeline) vs external tool
  3. **Recommended external tools** (with last-validated date):
     - PPT: Marp, Slidev — use HTML mockup as source, school CSS as theme
     - PDF: Pandoc with HTML→PDF, Typst, Prince
     - Infographic: HTML→static export (Puppeteer/Playwright screenshot)
     - Cover: HTML→static export (same)
     - AI-image-gen: Midjourney prompts (use Prompt DNA), Stable Diffusion XL with school-flavored prompt
  4. Caveat: "tools change; recommendations rot. Last validated 2026-MM-DD."
  5. How a marketing user would use this doc end-to-end
- **Verify:** `wc -l docs/design-schools-execution-paths.md` between 100–200; all 5 sections present.
- **Refs:** REQ-05

---

## Onda 5 — STATE + README + version

### T-25 ✅ Append D-23, D-24, D-25 to STATE.md
- **Action:** 3 decisions per spec REQ-06.
- **Verify:** `grep -c "^- \*\*D-2[345]" .specs/project/STATE.md` = 3.
- **Refs:** REQ-06

### T-26 ✅ Update README §What changed in v1.5.0 + Design schools library section
- **Action:** new release section + new top-level "## Design schools library" section explaining philosophy-vs-brand split + 12-entry table grouped by scenario strength.
- **Verify:** `grep -c "What changed in v1.5.0" README.md` = 1; `grep -c "Design schools library" README.md` ≥ 1; table has 12 rows.
- **Refs:** REQ-07.1, REQ-07.2

### T-27 ✅ Bump `marketplace.json`
- **Action:** `1.4.0` → `1.5.0`.
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `1.5.0`.
- **Refs:** REQ-08.3

---

## Onda 6 — Validation + commit

### T-28 ✅ Full validation sweep
- **Action:** run `quick_validate.py` for all 20 skills.
- **Verify:** 21 lines `Skill is valid!`.
- **Refs:** REQ-08.1

### T-29 ✅ Translator regression sweep
- **Action:** run translator against all 12 schools. Confirm each produces a non-empty, WCAG-valid proposal.
- **Verify:** `python3 scripts/school_md_to_appcolors.py --validate-all` reports 12/12 valid.
- **Refs:** REQ-08.2

### T-30 ✅ Commit + push
- **Action:**
  ```
  git add design-systems-schools/ scripts/school_md_to_appcolors.py skills/theme-create skills/frontend-design docs/design-schools-execution-paths.md README.md .specs/project/STATE.md .claude-plugin/marketplace.json
  git commit -m "feat(release): v1.5.0 — design schools library + multi-target execution paths"
  git push origin correcoes
  ```
- **Verify:** push exit 0; commit shows 12 SCHOOL.md files + translator + 2 skill edits + execution-path doc.

---

## Resumo de paralelização

- **Onda 0:** T-00 → T-01 → T-02 sequencial.
- **Onda 1:** T-03 sequencial (template-validating); T-04..T-14 paralelizáveis (11 schools); T-15 depende de todas.
- **Onda 2:** T-16 → T-17 → T-18 → T-19 → T-20 sequencial; T-21 final.
- **Onda 3:** T-22, T-23 paralelizáveis (different files).
- **Onda 4:** T-24 standalone.
- **Onda 5:** T-25, T-26, T-27 paralelizáveis.
- **Onda 6:** T-28 → T-29 → T-30 sequencial.

## Estimativa

- Onda 0: 30 min
- Onda 1: 8.5h (12 schools × ~40 min + index)
- Onda 2: 3h (translator)
- Onda 3: 1h
- Onda 4: 1h
- Onda 5: 30 min
- Onda 6: 1h
- **Total: ~15h** (matches 14-18h spec)

## Como retomar

1. Read spec.md + design.md + tasks.md (this feature)
2. Confirm v1.4.0 shipped (recommended) — `git tag | grep pre-v1.5.0`
3. Próximo `⬜ pending`
4. Time-check no T-03: if Müller-Brockmann auth excede 60 min, signal that 12-school plan precisa cortar pra 8.

## Confirmed slugs (locked at T-00 on 2026-05-07)

| # | Slug | School name | Primary scenario strength |
|---|---|---|---|
| 01 | `pentagram` | Pentagram (Bierut) | Versatile (Web ★★★, HTML ★★★, Cover ★★★) |
| 02 | `muller-brockmann` | Müller-Brockmann (Swiss grid) | Print-strong (PDF ★★★, Infographic ★★★) |
| 03 | `kenya-hara` | Kenya Hara (negative space) | Print-strong (PDF ★★★, HTML ★★★) |
| 04 | `information-architects` | Information Architects (typography) | Flutter-strong (Web ★★★, HTML ★★★) |
| 05 | `brutalism` | Brutalism (web brutalist) | Flutter-strong (Web ★★★, HTML ★★★) |
| 06 | `memphis` | Memphis (postmodern) | AI-gen-strong (AI ★★★, Cover ★★★) |
| 07 | `sagmeister-walsh` | Sagmeister & Walsh (expressive) | Versatile (HTML ★★★, AI ★★★) |
| 08 | `active-theory` | Active Theory (kinetic) | AI-gen-strong (AI ★★★, Web ★★★) |
| 09 | `editorial` | Editorial (Wired/Apple-mag) | Versatile (HTML/PPT/PDF/Infographic/Cover all ★★★) |
| 10 | `locomotive` | Locomotive (kinetic-narrative web) | Flutter-strong (Web ★★★) |
| 11 | `takram` | Takram (data-poetic) | Versatile (Web/HTML/PPT/PDF all ★★★) |
| 12 | `atelier-zero` | Atelier-Zero (collage-editorial) | Print-strong (open-design's hand-curated; HTML/PPT/PDF/Cover ★★★) |

12/12 locked. No swaps from spec REQ-01.1 — coverage spread accepted.
