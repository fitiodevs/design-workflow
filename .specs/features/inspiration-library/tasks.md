# Tasks: inspiration-library

> Atomic, sequenced. ≤30 min cada. Verificação binária.
> Lê depois de spec.md + design.md.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.2.0` (criar em T-00)
**Target:** v1.2.0
**Depends on:** v1.1.1 shipped (`craft/` exists)

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Safety net + curation decision

### T-00 ⬜ Tag rollback + capture upstream SHA
- **Action:**
  ```bash
  git tag pre-v1.2.0
  UPSTREAM_SHA=$(gh api repos/nexu-io/open-design/branches/main --jq '.commit.sha')
  echo "Upstream SHA: $UPSTREAM_SHA" > /tmp/v1.2.0-source.txt
  ```
- **Verify:** `git tag | grep pre-v1.2.0` returns match; SHA captured.
- **Refs:** spec REQ-01

### T-01 ⬜ Confirm 20-slug list
- **Action:** read upstream `design-systems/README.md` (already cached from earlier session) + sanity-check the proposed 20 in spec.md REQ-01.1 against actual upstream availability. If any of the 20 don't exist or have ASCII slug differences, swap.
- **Verify:** all 20 slugs return non-empty `gh api repos/nexu-io/open-design/contents/design-systems/<slug>/DESIGN.md` (200 OK).
- **Decision:** finalize the 20-slug list in this file under §"Confirmed slugs" before proceeding.
- **Refs:** REQ-01.1

---

## Onda 1 — Fork 20 DESIGN.md files (paralelizável)

> Cada fork é o mesmo padrão. Parallel-safe.

### T-02 🅿️ Fork AI&LLM trio (claude, cohere, mistral-ai)
- **Action:** for each slug, fetch upstream DESIGN.md, prepend attribution header (same template as `craft/`), write to `design-systems/<slug>/DESIGN.md`. Header includes: `> Sourced from: <url>`, `> Upstream attribution: <getdesign or refero or open-design>`, `> License: Apache-2.0 (open-design) | MIT (upstream-of-upstream)`, `> Local path`, `> Last sync: 2026-05-XX at <SHA>`.
- **Verify:** 3 files exist; each first 8 lines contain "Sourced from", "Upstream attribution", "License".
- **Refs:** REQ-01.2

### T-03 🅿️ Fork Dev Tools trio (linear-app, vercel, raycast)
- Same pattern.

### T-04 🅿️ Fork Productivity pair (notion, cal)
- Same pattern.

### T-05 🅿️ Fork Backend/Data pair (supabase, sentry)
- Same pattern.

### T-06 🅿️ Fork Design/Creative pair (figma, framer)
- Same pattern.

### T-07 🅿️ Fork Fintech pair (stripe, revolut)
- Same pattern.

### T-08 🅿️ Fork E-Commerce pair (airbnb, nike)
- Same pattern.

### T-09 🅿️ Fork Media/Consumer pair (apple, spotify)
- Same pattern.

### T-10 🅿️ Fork Automotive solo (tesla)
- Same pattern.

### T-11 🅿️ Fork Editorial solo (atelier-zero)
- Same pattern. Note: this one is hand-authored by open-design itself, not 3rd-party — attribution is `open-design (Apache-2.0)`.

### T-12 ⬜ Write `design-systems/README.md`
- **Action:** category index + mapping table (which skill consumes; for now only `theme-create` via `--inspired-by`). Reference open-design README.md for category metadata. Document the `> Category: <name>` parsing convention.
- **Verify:** 20 entries in the index; categories visible; `wc -l` between 60–100.
- **Refs:** REQ-01.3

---

## Onda 2 — Translator script

### T-13 ⬜ Stub `scripts/design_md_to_appcolors.py` skeleton
- **Action:** scaffolding only — argparse (`<slug>` positional, `--out-dir` optional, `--validate-all` flag), 6 phase functions stubbed (parse / extract / map / derive_dark / validate_wcag / write), each with docstring matching design §"Translator script outline".
- **Verify:** `python3 scripts/design_md_to_appcolors.py --help` runs; `python3 scripts/design_md_to_appcolors.py design-systems/claude/DESIGN.md --dry-run` exits 0 with phase-trace stdout.
- **Refs:** REQ-02.1

### T-14 ⬜ Implement `parse_design_md`
- **Action:** parse markdown into `{sections: {visual_theme: str, color_palette: {primary: [(name,hex,role),...], surface: [...], ...}, typography: {...}, ...}}`. Tolerant — section names vary across upstreams ("Color Palette & Roles" vs "Colors").
- **Verify:** unit-test against `design-systems/claude/DESIGN.md` — extract returns ≥6 hex codes from "Primary" + ≥4 from "Surface & Background"; sections.visual_theme is non-empty paragraph.
- **Refs:** REQ-02.1, design D-C step 1+2

### T-15 ⬜ Implement `map_to_appcolors` inference chain
- **Action:** chain per design D-C: explicit `--<role>` literal > section semantic match > regex order > WCAG-corrected fallback. Each mapping logs decision to a list passed to write_artifacts.
- **Verify:** running on claude → emits 29 tokens for light mode; `brandDefault` = `#c96442` (terracotta); `bgBase` = `#f5f4ed` (parchment); decisions list has ≥29 entries.
- **Refs:** REQ-02.2, REQ-02.3, design D-C

### T-16 ⬜ Implement `derive_dark_mode`
- **Action:** if source has explicit dark hex → use; else L-flip via `oklch_to_hex.py`. Always emit a 29-token dark proposal even when source is light-only.
- **Verify:** running on claude → dark mode bgBase ≈ `#141413` (matches "Deep Dark" in source); running on a single-mode source → dark proposal exists + rationale flags it as derived.
- **Refs:** REQ-02.5, design D-D

### T-17 ⬜ Implement `validate_wcag` integration
- **Action:** import `scripts/check_contrast.py` (existing). Run on the 12 mandatory pairs × 2 modes (24 total). Failed pairs (ratio < required threshold) get propose-darkened/lightened alternative emitted as `<token>_corrected` with note in rationale.
- **Verify:** running on claude → reports ≥22/24 pass; rationale lists any failures explicitly.
- **Refs:** REQ-02.4

### T-18 ⬜ Implement `write_artifacts`
- **Action:** emit `<out-dir>/proposal.json` (29 tokens × 2 modes + metadata) + `<out-dir>/rationale.md` (sections: Source citation · Token mapping table · WCAG report · Open questions for user · Fitio-specific tokens needing input).
- **Verify:** files exist with non-empty content; `jq '.tokens.light | length' proposal.json` = 29; `grep -c "^##" rationale.md` ≥ 4.
- **Refs:** REQ-02.6, design D-E

### T-19 ⬜ Smoke-test translator on 3 samples
- **Action:**
  ```bash
  for s in claude linear-app stripe; do
      mkdir -p /tmp/translator-test/$s
      python3 scripts/design_md_to_appcolors.py design-systems/$s/DESIGN.md --out-dir /tmp/translator-test/$s/
  done
  ```
  Manually review each `rationale.md` — does the brand identity map sensibly? Catch any "all tokens defaulted to neutral gray" failures.
- **Verify:** 3 dirs each contain proposal.json + rationale.md; manual review notes captured in `/tmp/translator-test/review.md`; zero "all tokens defaulted" cases.
- **Refs:** spec §8 acceptance

---

## Onda 3 — Wire `/theme-create`

### T-20 ⬜ Update `theme-create/SKILL.md` description + Triggers
- **Action:** description mentions both modes; Triggers section adds `/theme-create --inspired-by <slug>`, `/theme-create --browse`, `/theme-create --browse <category>`.
- **Verify:** `python3 $VAL skills/theme-create/` returns valid; `grep -c "inspired-by" skills/theme-create/SKILL.md` ≥ 3.
- **Refs:** REQ-03.1, REQ-04.1

### T-21 ⬜ Add Workflow section for `--inspired-by`
- **Action:** insert new workflow steps in `theme-create/SKILL.md` body documenting: (1) validate slug, (2) run translator, (3) present rationale to user, (4) ask 4 remaining pre-conditions (purpose/audience/invariants/coexistence) instead of all 8, (5) tweak loop, (6) final emission. Reference design D-F.
- **Verify:** body has a `## Workflow — --inspired-by mode` section; mentions `scripts/design_md_to_appcolors.py`.
- **Refs:** REQ-03.2, REQ-03.3

### T-22 ⬜ Add Workflow section for `--browse`
- **Action:** document --browse flow in skill body: list categories from `design-systems/README.md` index, ask user to pick category (or skip filter), list entries, ask pick, drop into `--inspired-by`.
- **Verify:** body has `## Workflow — --browse mode`; references parsing of `> Category:` line.
- **Refs:** REQ-04.2, REQ-04.3, REQ-04.4

### T-23 ⬜ Create `skills/theme-create/references/inspiration-flow.md`
- **Action:** ~80-line dense reference detailing the inspiration workflow — what the rationale doc looks like, what user is shown, how tweaks work, how WCAG warnings are surfaced. SKILL.md body points at this with a single `Read` instruction.
- **Verify:** file exists; SKILL.md references it.
- **Refs:** design D-E, REQ-03.2

---

## Onda 4 — STATE + README + bump

### T-24 ⬜ Append D-13 + D-14 to `.specs/project/STATE.md`
- **Action:**
  - **D-13 — DESIGN.md library**: 20 entries curated from upstream open-design's 71, attribution chain documented per file, sync manual on demand at SHA `<X>`.
  - **D-14 — Translator semantics**: inference chain priority (explicit role > section match > regex > WCAG-corrected fallback); failed mappings always flagged in rationale, never silent; Fitio-specific tokens (gameAccent etc) flagged for user input.
- **Verify:** `grep -c "^- \*\*D-1[34]" .specs/project/STATE.md` = 2.
- **Refs:** REQ-05

### T-25 ⬜ Add §What changed in v1.2.0 + Inspiration library section to README
- **Action:** new release section above v1.1.1; new top-level "## Inspiration library" with 20-entry category table.
- **Verify:** `grep -c "What changed in v1.2.0" README.md` = 1; `grep -c "Inspiration library" README.md` ≥ 1; table has 9 categories.
- **Refs:** REQ-06.1, REQ-06.2

### T-26 ⬜ Bump `marketplace.json`
- **Action:** `1.1.1` → `1.2.0` via Edit on `version`.
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `1.2.0`.
- **Refs:** REQ-07.3

---

## Onda 5 — Validation + commit

### T-27 ⬜ Full validation sweep
- **Action:** run `quick_validate.py` for all 19 skills.
- **Verify:** 19 lines `Skill is valid!`.
- **Refs:** REQ-07.1

### T-28 ⬜ Translator regression sweep
- **Action:** `python3 scripts/design_md_to_appcolors.py --validate-all` — runs the translator against all 20 forks, reports any that fail (no proposal.json produced or WCAG report empty).
- **Verify:** 20/20 produce a valid proposal + rationale.
- **Refs:** REQ-07.2

### T-29 ⬜ Commit + push
- **Action:**
  ```
  git add design-systems/ scripts/design_md_to_appcolors.py skills/theme-create/ .specs/project/STATE.md README.md .claude-plugin/marketplace.json
  git commit -m "feat(release): v1.2.0 — DESIGN.md inspiration library + translator"
  git push origin correcoes
  ```
- **Verify:** push exit 0; `git log -1 --stat` shows 20 design-system dirs + translator + skill edits.

---

## Resumo de paralelização

- **Onda 0:** T-00 → T-01 sequencial.
- **Onda 1:** T-02..T-11 paralelizáveis (10 fork tasks); T-12 depende de todos.
- **Onda 2:** T-13 → T-14..T-18 sequencial (each builds on previous); T-19 depends on all.
- **Onda 3:** T-20 → T-21 → T-22 → T-23 sequenciais (mesmo arquivo).
- **Onda 4:** T-24..T-26 paralelizáveis (arquivos diferentes).
- **Onda 5:** T-27..T-29 sequencial.

## Estimativa

- Onda 0: 15 min
- Onda 1: 1.5h (paralelizado pode cair pra ~30min)
- Onda 2: 4h (translator é o coração)
- Onda 3: 1h
- Onda 4: 30 min
- Onda 5: 30 min
- **Total: 7.75h** (alinhado com 6-8h da spec)

## Como retomar

Próxima sessão:
1. Read spec.md + design.md + tasks.md desta feature
2. Confirma `pre-v1.2.0` tag exists; senão volta pro T-00
3. Identifica primeiro `⬜ pending`, segue
