# Tasks: craft-design-context

> Atomic, sequenced. ≤30 min cada. Verificação binária.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.1.1` (já criada por `craft-adoption`) OU `pre-v1.1.2` se shipping standalone.
**Target:** v1.1.1 (ride along) ou v1.1.2 (standalone) — decisão em T-00.
**Depends on:** decided in T-00.

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Decision: ride along or standalone

### T-00 ⬜ Decide release coupling
- **Action:** check git log:
  ```bash
  git log --oneline -1 origin/correcoes
  git tag | grep pre-v1.1
  ```
- **Decision rule:**
  - If `pre-v1.1.1` exists AND craft-adoption tasks are all ⬜ pending → **ride along v1.1.1**. This feature's tasks merge into craft-adoption's commit.
  - If craft-adoption already shipped (commit on origin) → **standalone v1.1.2**. Create `pre-v1.1.2` tag now; commit at the end.
- **Verify:** decision logged at top of this file (replace "decided in T-00" header).
- **Refs:** design D-B
- **Blocks:** all

---

## Onda 1 — Author the doc

### T-01 ⬜ Write `craft/design-context.md`
- **Action:** ~110 lines per design §"design-context.md outline (target structure)". Read huashu's source ONCE for inspiration, then write top-down from our framing — Flutter-specific Tier 1 paths, sharp refusal rule, 3 concrete examples mapping to our skills.
- **Verify:**
  - `wc -l craft/design-context.md` between 80–140
  - `grep -c "^### Tier" craft/design-context.md` = 5
  - `grep -c "REFUSE\|STOP" craft/design-context.md` ≥ 2 (the rule appears at least twice)
  - First 6 lines contain "Source", "Idea inspired by", "License", "Local path", "Created"
- **Refs:** REQ-01

### T-02 ⬜ Update `craft/README.md` to list 6 docs
- **Action:** edit the mapping table to add a 6th row for `design-context.md` with the 5 wired skills.
- **Verify:**
  - `grep -c "design-context" craft/README.md` ≥ 1
  - Mapping table has 6 doc rows visible
- **Refs:** REQ-02

---

## Onda 2 — Wire 5 skills

### T-03 🅿️ Wire `theme-port`
- **Action:**
  1. Add `design-context` to existing `dw.craft.requires:` array (was `[state-coverage, typography]` per craft-adoption v1.1.1; becomes `[state-coverage, typography, design-context]`).
  2. Add a "## Pre-flight context check" section near the top of Workflow per design D-F template, with theme-port-specific tier checks (Tier 1: AppColors exists, Tier 4: docs/product.md exists with §Tone).
- **Verify:**
  - `python3 $VAL skills/theme-port/` returns valid
  - `grep -c "design-context" skills/theme-port/SKILL.md` ≥ 2
  - `grep -c "Pre-flight" skills/theme-port/SKILL.md` ≥ 1
- **Refs:** REQ-03.1

### T-04 🅿️ Wire `theme-create`
- **Action:** add `design-context` to requires + Pre-flight section. theme-create-specific tier checks: Tier 1 (existing AppColors as contrast ref); Tier 4 (`--inspired-by` flag OR 8 pre-conditions answered).
- **Verify:** valid + greps match.
- **Refs:** REQ-03.2

### T-05 🅿️ Wire `theme-extend` (NEW wire)
- **Action:** add `dw.craft.requires: [design-context]` (was unwired in v1.1.1) + Pre-flight section. Tier 1: AppColors exists (REQUIRED — extending nothing makes no sense).
- **Verify:**
  - `python3 $VAL skills/theme-extend/` valid
  - `grep -c "dw:" skills/theme-extend/SKILL.md` ≥ 1
  - `grep -c "design-context\|Pre-flight" skills/theme-extend/SKILL.md` ≥ 2
- **Refs:** REQ-03.3

### T-06 🅿️ Wire `theme-critique`
- **Action:** add `design-context` to existing requires (was `[anti-ai-slop, color, state-coverage, typography]`; becomes 5-element list with design-context appended).
- **Verify:** valid + grep.
- **Refs:** REQ-03.4

### T-07 🅿️ Wire `frontend-design`
- **Action:** add `design-context` to existing requires (was 5 docs; becomes 6).
- **Verify:** valid + grep.
- **Refs:** REQ-03.4

---

## Onda 3 — STATE + README + commit

### T-08 ⬜ Append D-11.1 to STATE.md
- **Action:** add sub-decision: "**D-11.1 — `design-context.md` authored from scratch**: huashu-design license (Personal Use Only) prevented forking; we wrote our own under Apache-2.0 citing the structural idea. Refusal rule (`STOP if no Tier 1-4 context`) is sharper than upstream's wording."
- **Verify:** `grep "D-11.1" .specs/project/STATE.md` returns match.
- **Refs:** REQ-04

### T-09 ⬜ Update §What changed in v1.1.1 in README
- **Action:** add 1 bullet to existing v1.1.1 section: "**Design context doctrine.** New `craft/design-context.md` codifies the 'blank-page is last resort' rule with a 5-tier context hierarchy and a sharp refusal rule. Authored from scratch, idea inspired by [huashu-design](https://github.com/alchaincyf/huashu-design)."
- **Verify:** `grep -c "design-context" README.md` ≥ 1.
- **Refs:** REQ-05

### T-10 ⬜ Validation sweep
- **Action:** run `quick_validate.py` for all 19 skills.
- **Verify:** 19 lines `Skill is valid!`.
- **Refs:** REQ-06.1

### T-11 ⬜ Commit (or merge into v1.1.1 commit)
- **Action:**
  - If ride-along: stage these changes alongside craft-adoption's stage; single commit `feat(release): v1.1.1 — craft layer adopted from open-design (+ design-context)`.
  - If standalone: stage only this feature's files; commit `feat(release): v1.1.2 — design-context craft doctrine`; bump marketplace.json `1.1.1` → `1.1.2` first.
- **Verify:** `git log -1 --stat` shows `craft/design-context.md` + 5 skill edits + STATE.md + README.md.

---

## Resumo de paralelização

- **Onda 0:** T-00 sequencial.
- **Onda 1:** T-01 → T-02 sequencial (T-02 references T-01's content).
- **Onda 2:** T-03..T-07 paralelizáveis (5 different skills).
- **Onda 3:** T-08..T-09 paralelizáveis; T-10 → T-11 sequencial.

## Estimativa

- Onda 0: 5 min
- Onda 1: 30 min
- Onda 2: 20 min (parallel)
- Onda 3: 10 min
- **Total: ~65 min**

## Como retomar

1. Read spec.md + design.md + tasks.md (this feature)
2. T-00 decision: ride-along vs standalone
3. Confirm correct rollback tag exists
4. Próximo `⬜ pending`
