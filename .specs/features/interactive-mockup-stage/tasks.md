# Tasks: interactive-mockup-stage

> Atomic, sequenced. ≤30 min cada. Verificação binária.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.4.0` (criar em T-00)
**Target:** v1.4.0
**Depends on:** v1.1.1 shipped (`craft/` exists). Recommended: v1.2.0 shipped (mas não bloqueia).

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Safety net + source pin

### T-00 ✅ Tag rollback + capture upstream SHA
- **Action:**
  ```bash
  git tag pre-v1.4.0
  UPSTREAM_SHA=$(gh api repos/nexu-io/open-design/branches/main --jq '.commit.sha')
  echo "Upstream SHA: $UPSTREAM_SHA" >> /tmp/v1.4.0-source.txt
  ```
- **Verify:** tag exists; SHA captured.
- **Refs:** spec §6
- **Blocks:** all

---

## Onda 1 — `tweaks` skill structure

### T-01 ✅ Create skill directory
- **Action:** `mkdir -p skills/tweaks/{assets,references,evals}` and stub README in each subdir.
- **Verify:** 4 dirs exist; `find skills/tweaks -type d` returns 4.
- **Refs:** REQ-01

### T-02 ✅ Write `skills/tweaks/SKILL.md`
- **Action:** frontmatter (name, description per spec, no triggers field, optional `dw.craft.requires: [color, anti-ai-slop, typography]`); body covers Triggers section, Workflow (parse input → identify visual decisions → inject panel → emit `<input>.tweaks.html`), Anti-patterns (REQ-01.6), Output template, Don'ts.
- **Verify:** `python3 $VAL skills/tweaks/` returns valid; `wc -l skills/tweaks/SKILL.md` between 120–200.
- **Refs:** REQ-01.1, REQ-01.2

### T-03 ✅ Write `skills/tweaks/assets/panel.html`
- **Action:** the panel template per design §"Panel HTML template structure". Includes: `<aside>` markup, `<style>` with CSS custom property defaults, `<script>` with bind+persist+restore logic. Use `%BASENAME%` and `%CONTENT_SHA%` placeholders for runtime substitution.
- **Verify:** file exists; `wc -l` between 200–300; opens in browser standalone (sanity check via `xdg-open` or manual).
- **Refs:** REQ-01.3, design §"Panel HTML template structure"

### T-04 ✅ Write `skills/tweaks/references/knob-bindings.md`
- **Action:** dense reference doc (~80 lines) — for each of the 5 knobs: which CSS custom property it binds to, what value range, what visual effect. Includes the densityToUnit / scaleToFontSize functions documented in prose.
- **Verify:** 5 sections (one per knob); `wc -l` between 60–100.
- **Refs:** REQ-01.4, design D-E

### T-05 ✅ Write `skills/tweaks/evals/evals.json`
- **Action:** 3 prompts:
  1. "/tweaks /tmp/landing.html" — verify the wrapped HTML has the panel markup + CSS custom properties + script
  2. "/tweaks /tmp/dashboard.html — only accent and theme knobs" — verify subset support (deferred? maybe too ambitious for v1.3)
  3. "/tweaks /tmp/already-static-hex.html" — verify it errors gracefully + recommends refit per REQ-01.6
- **Verify:** `jq '.evals | length' skills/tweaks/evals/evals.json` = 3; `python3 $VAL skills/tweaks/` returns valid.
- **Refs:** REQ-01.6

---

## Onda 2 — Refit `frontend-design`

### T-06 ✅ Update `frontend-design/SKILL.md` body emission rules
- **Action:** add a section "## Tweaks-ready output" documenting the 5 refit rules per design §"Refit rules for `frontend-design`": (1) hex → custom props, (2) spacing → calc, (3) font-size → multiplicative, (4) data-od-id, (5) dark mode via attribute. Reference `craft/color.md` for token names.
- **Verify:** `grep -c "Tweaks-ready" skills/frontend-design/SKILL.md` ≥ 1; `python3 $VAL skills/frontend-design/` valid.
- **Refs:** REQ-02.1

### T-07 ✅ Update Clara's checklist
- **Action:** edit `skills/frontend-design/references/clara-checklist.md` to add 5 checklist items matching the 5 refit rules.
- **Verify:** `grep -c "data-od-id" skills/frontend-design/references/clara-checklist.md` ≥ 1; `grep -c "var(--" skills/frontend-design/references/clara-checklist.md` ≥ 1.
- **Refs:** REQ-02.3

### T-08 ⏭️ deferred (no evals/ dir for frontend-design) Update Clara's eval (if exists)
- **Action:** `skills/frontend-design/evals/evals.json` — does it exist? If yes, add assertions for tweaks-ready emission (CSS custom properties in :root, data-od-id on sections, no literal hex outside :root). If no, defer (Clara has subjective output per spec REQ-05.4 of skill-creator-alignment).
- **Verify:** if eval exists, `grep -c "data-od-id\|var(--" skills/frontend-design/evals/evals.json` ≥ 2. If not, document deferral in T-19 commit message.
- **Refs:** REQ-02.4

### T-09 ✅ Anti-pattern check + recommendation flow
- **Action:** add to `skills/tweaks/SKILL.md` body the anti-pattern detection logic — when input HTML has `<style>:root { --foo: #hex }` literals OR no CSS custom properties at all, refuse and recommend refit. Document the exact error message.
- **Verify:** SKILL.md body has section "## When to refuse" with explicit recommendation message.
- **Refs:** REQ-01.6, REQ-02.5

---

## Onda 3 — `theme-critique --mode 5dim` flag

### T-10 ✅ Fork `5dim-rubric.md` from open-design
- **Action:** fetch upstream `skills/critique/SKILL.md`, extract the 5-dimension scoring section, write to `skills/theme-critique/references/5dim-rubric.md` with attribution header (Source from open-design + originating huashu-design).
- **Verify:** file exists; `grep -c "^### " skills/theme-critique/references/5dim-rubric.md` ≥ 5 (one per dimension); attribution header present.
- **Refs:** REQ-03.3

### T-11 ✅ Add `--mode` flag to `theme-critique` SKILL.md
- **Action:** edit `skills/theme-critique/SKILL.md`:
  - Triggers: add `/theme-critique --mode 5dim <path>`
  - Workflow: dispatch on `--mode` → if absent or `nielsen`, existing Nielsen 10 flow; if `5dim`, read `references/5dim-rubric.md`, score 5 dimensions, emit HTML report at `.design-spec/critique/<feature>/<timestamp>-5dim.html`.
  - Update description to mention both modes.
- **Verify:** `python3 $VAL skills/theme-critique/` valid; `grep -c "5dim" skills/theme-critique/SKILL.md` ≥ 3.
- **Refs:** REQ-03.1, REQ-03.2

### T-12 ✅ Add HTML report template description in SKILL.md
- **Action:** in the body, document the report layout (header → radar SVG → 5 dimension cards → combined Keep/Fix/Quick-wins lists). Reference upstream open-design critique skill output as the visual goal. Ship as Markdown prose, not as HTML asset (the model emits the HTML at invocation).
- **Verify:** body has section "## 5dim report layout"; mentions `radar chart inline SVG` and `Keep/Fix/Quick-wins`.
- **Refs:** REQ-03.2 third bullet

### T-13 ✅ Update path conventions — separate `nielsen` and `5dim` outputs
- **Action:** in SKILL.md body, update output path: when Nielsen mode runs, write to `.design-spec/critique/<feature>/<timestamp>-nielsen.html`. When 5dim runs, `.design-spec/critique/<feature>/<timestamp>-5dim.html`. Never overwrite.
- **Verify:** body documents both paths.
- **Refs:** REQ-03.4, design D-H

---

## Onda 4 — Pipeline docs

### T-14 ✅ Update README §What changed in v1.4.0
- **Action:** new release section above v1.2.0; document the 3 components (tweaks skill, Clara refit, 5dim mode). Include 6-line ASCII diagram of new pipeline.
- **Verify:** `grep -c "What changed in v1.4.0" README.md` = 1; pipeline diagram present (look for "/tweaks" between "/frontend-design" and "/theme-port").
- **Refs:** REQ-04.1

### T-15 ✅ Update `docs/theme-manager.md` workflow
- **Action:** edit "I'm starting a new app" workflow — insert `/tweaks <path>` step between `/frontend-design` and `/theme-port --from-html`.
- **Verify:** `grep -c "tweaks" docs/theme-manager.md` ≥ 2.
- **Refs:** REQ-04.2

### T-16 ✅ Add Tweaker persona to `docs/personas.md`
- **Action:** add row: `| tweaks | Tweaker | — (no PT alias) | Wraps any tweaks-ready HTML with a side panel of live CSS-custom-property knobs persisting to localStorage | /tweaks |`. Update the §Why personas? text if Tweaker doesn't fit the "voice" framing — this skill is functional, not persona-driven.
- **Verify:** `grep -c "Tweaker" docs/personas.md` ≥ 1.
- **Refs:** REQ-04.3

---

## Onda 5 — STATE + marketplace

### T-17 ✅ Append D-19, D-20, D-21 to STATE.md
- **Action:** add 3 decisions per spec REQ-05.
- **Verify:** `grep -cE "^- \*\*D-(19\|20\|21)" .specs/project/STATE.md` = 3.
- **Refs:** REQ-05

### T-18 ✅ Update `marketplace.json`
- **Action:** add `./skills/tweaks` to skills array; bump version `1.2.0` → `1.4.0`; update top-level description to mention "20 atomic operators + interactive mockup stage" (or current count).
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `1.4.0`; `jq '.plugins[0].skills | length' .claude-plugin/marketplace.json` = 20.
- **Refs:** REQ-06.3

---

## Onda 6 — Validation + smoke + commit

### T-19 ✅ Full validation sweep
- **Action:** run `quick_validate.py` for all 20 skills.
- **Verify:** 20 lines `Skill is valid!`.
- **Refs:** REQ-06.1

### T-20 ✅ End-to-end smoke test (manual)
- **Action:** sequence:
  1. `/frontend-design` → emit a milestone slider mockup at `/tmp/milestone.html`
  2. `/tweaks /tmp/milestone.html` → `/tmp/milestone.tweaks.html`
  3. Open in Chrome (`xdg-open /tmp/milestone.tweaks.html`)
  4. Mutate accent slider → confirm header color changes live
  5. Reload tab → confirm state persists
  6. Open in Firefox (`firefox /tmp/milestone.tweaks.html &`) → confirm same behavior
  7. Test reset button → confirm localStorage cleared
- **Verify:** all 7 steps documented in a manual log file `.design-spec/smoke/v1.4.0-2026-XX-XX.md`. Any browser-specific issues caught surface as new tasks (or get fixed inline if simple).
- **Refs:** REQ-06.2, design §"Validation strategy"

### T-21 ✅ End-to-end smoke for 5dim critique
- **Action:** `/theme-critique --mode 5dim /tmp/milestone.html` → confirm output exists at `.design-spec/critique/milestone/2026-XX-XX-HHMM-5dim.html`. Open report — confirm radar chart + 5 cards + Keep/Fix/Quick-wins lists.
- **Verify:** report file exists; opens in browser; has visible radar chart (look for `<svg`).

### T-22 ✅ Commit + push
- **Action:**
  ```
  git add skills/tweaks skills/frontend-design skills/theme-critique docs/personas.md docs/theme-manager.md README.md .specs/project/STATE.md .claude-plugin/marketplace.json .design-spec/smoke/
  git commit -m "feat(release): v1.4.0 — interactive mockup stage (tweaks + 5dim critique)"
  git push origin correcoes
  ```
- **Verify:** push exit 0; commit message lists the 3 sub-features.

---

## Resumo de paralelização

- **Onda 0:** T-00 sequencial.
- **Onda 1:** T-01 → T-02..T-05 sequencial (alguns dependem do skeleton); T-03 e T-04 paralelizáveis após T-02.
- **Onda 2:** T-06, T-07 paralelizáveis; T-08 depende de T-07; T-09 paralelizável com Onda 1 final.
- **Onda 3:** T-10 → T-11 → T-12 → T-13 sequencial (mesmo arquivo).
- **Onda 4:** T-14, T-15, T-16 paralelizáveis (arquivos diferentes).
- **Onda 5:** T-17, T-18 paralelizáveis.
- **Onda 6:** T-19 → T-20 → T-21 → T-22 sequencial (smoke depende de skill funcionando; commit final).

## Estimativa

- Onda 0: 5 min
- Onda 1: 4h (tweaks panel.html + skill body são o coração)
- Onda 2: 2h
- Onda 3: 2h
- Onda 4: 1h
- Onda 5: 30 min
- Onda 6: 1.5h (smoke ocupa tempo real, não é só validação automatizada)
- **Total: ~11h** (alinhado com 10-12h da spec)

## Como retomar

1. Read spec.md + design.md + tasks.md
2. `git tag | grep pre-v1.4.0` — se ausente, T-00
3. Próximo `⬜ pending` na Onda atual
