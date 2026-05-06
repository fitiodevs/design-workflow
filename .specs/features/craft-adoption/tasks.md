# Tasks: craft-adoption

> Atomic, sequenced. Cada task ≤30 min. Cada task tem critério de verificação binário.
> Lê depois de spec.md + design.md.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.1.1` (criar em T-00)
**Target:** v1.1.1

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Safety net + source pin

### T-00 ✅ Capture upstream SHA + create rollback tag
- **Action:**
  ```bash
  cd /media/fitiodev/FITIO/Skill/design-workflow
  git tag pre-v1.1.1
  UPSTREAM_SHA=$(gh api repos/nexu-io/open-design/branches/main --jq '.commit.sha')
  echo "Upstream SHA: $UPSTREAM_SHA"
  ```
  Save the SHA in a scratch note or in spec.md §6 (replace TBD).
- **Verify:** `git tag | grep pre-v1.1.1` returns match; SHA captured (a 40-char hex).
- **Refs:** spec REQ-01.3, design D-F
- **Blocks:** all other tasks

---

## Onda 1 — Fork the 5 craft docs

### T-01 ✅ Fork `anti-ai-slop.md`
- **Action:**
  ```bash
  mkdir -p craft
  gh api repos/nexu-io/open-design/contents/craft/anti-ai-slop.md --jq '.content' | base64 -d > /tmp/anti-ai-slop-upstream.md
  ```
  Then write `craft/anti-ai-slop.md` with the header template (design.md §"Header template") followed by `cat /tmp/anti-ai-slop-upstream.md`.
- **Verify:** `head -8 craft/anti-ai-slop.md | grep -c "Sourced from\|Upstream attribution\|License\|Last sync"` ≥ 4.
- **Refs:** REQ-01.1, REQ-01.2, REQ-01.3

### T-02 ✅ Fork `color.md`
- **Action:** mesma rotina de T-01, source `craft/color.md`.
- **Verify:** mesma checagem.

### T-03 ✅ Fork `state-coverage.md`
- **Action:** idem.
- **Verify:** mesma checagem.

### T-04 ✅ Fork `typography.md`
- **Action:** idem.
- **Verify:** mesma checagem.

### T-05 ✅ Fork `animation-discipline.md`
- **Action:** idem.
- **Verify:** mesma checagem.

### T-06 ✅ Write `craft/README.md`
- **Action:** 1 paragraph intro + table mapping each `<name>.md` → which skills load it. Reference design.md §Architecture for the mapping.
- **Verify:** `wc -l craft/README.md` between 30–60; contains a markdown table with 5 rows.
- **Refs:** REQ-01.4

---

## Onda 2 — Frontmatter convention + validation probe

### T-07 ✅ Probe: does `quick_validate.py` accept arbitrary top-level frontmatter fields?
**Verdict:** top-level `dw:` REJECTED. Nested `metadata.dw.*` ACCEPTED (validator treats `metadata:` as opaque). All wiring uses `metadata.dw.craft.requires`.
- **Action:** copy `skills/theme-create/SKILL.md` to `/tmp/probe.md`, prepend `dw:\n  craft:\n    requires: [color, typography]\n` to the frontmatter. Run validator.
  ```bash
  VAL=/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py
  mkdir -p /tmp/probe-skill && cp /tmp/probe.md /tmp/probe-skill/SKILL.md
  python3 $VAL /tmp/probe-skill/
  ```
- **Verify:** if output is `Skill is valid!`, decision is **frontmatter path**. If error mentions YAML or unknown field, decision is **body-comment path** (D-D fallback).
- **Refs:** design D-D
- **Decision logged in:** STATE.md (T-12 records the verdict)

### T-08 ✅ Write `docs/skill-extensions.md`
- **Action:** document the `dw:` namespace (initial scope: just `dw.craft.requires:`). Show the path that won in T-07. Include 1 example from a real skill.
- **Verify:** `grep -c "dw:" docs/skill-extensions.md` ≥ 3; the example matches what we'll wire in T-09..T-13.
- **Refs:** REQ-02.1, REQ-02.2, REQ-02.3

---

## Onda 3 — Wire 5 skills

### T-09 ✅ Wire `theme-critique`
- **Action:** edit `skills/theme-critique/SKILL.md`:
  1. Add `dw.craft.requires: [anti-ai-slop, color, state-coverage, typography]` per the path T-07 chose.
  2. Add a "Craft references" section in the body using the template in design.md, listing the 4 declared docs.
- **Verify:**
  - `python3 $VAL skills/theme-critique/` returns `Skill is valid!`
  - `grep -c "craft/" skills/theme-critique/SKILL.md` ≥ 4
- **Refs:** REQ-03.1

### T-10 ✅ Wire `theme-create`
- **Action:** add `dw.craft.requires: [color, typography, anti-ai-slop]` + Craft references section.
- **Verify:** valid + grep ≥ 3.
- **Refs:** REQ-03.2

### T-11 ✅ Wire `theme-port`
- **Action:** `dw.craft.requires: [state-coverage, typography]` + Craft references section.
- **Verify:** valid + grep ≥ 2.
- **Refs:** REQ-03.3

### T-12 ✅ Wire `theme-bolder`
- **Action:** `dw.craft.requires: [color, anti-ai-slop]` + Craft references section.
- **Verify:** valid + grep ≥ 2.
- **Refs:** REQ-03.4

### T-13 ✅ Wire `frontend-design`
- **Action:** `dw.craft.requires: [anti-ai-slop, color, state-coverage, typography, animation-discipline]` + Craft references section.
- **Verify:** valid + grep ≥ 5.
- **Refs:** REQ-03.5

---

## Onda 4 — STATE + README + version

### T-14 ✅ Append D-11 + D-12 to `.specs/project/STATE.md`
- **Action:** add two decision entries below D-10:
  - **D-11 — `craft/` adoption**: forked verbatim from open-design SHA `<X>`, attribution chain documented per file, sync is manual on demand.
  - **D-12 — `dw:` namespace**: distinct from open-design's `od:`; we own this namespace for design-workflow extensions.
- **Verify:** `grep -c "^- \*\*D-1[12]" .specs/project/STATE.md` = 2.
- **Refs:** REQ-04

### T-15 ✅ Add §What changed in v1.1.1 to README + companion link
- **Action:** insert section before §What changed in v1.1.0; explain the craft adoption (3-4 bullets); update the Optional companions table to note open-design as upstream of `craft/`.
- **Verify:** `grep -c "What changed in v1.1.1" README.md` = 1; `grep "open-design" README.md | wc -l` ≥ 1.
- **Refs:** REQ-05

### T-16 ✅ Bump `marketplace.json` version
- **Action:** `1.1.0` → `1.1.1` via Edit on the `version` field.
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `1.1.1`.
- **Refs:** REQ-06.2

---

## Onda 5 — Validation + commit

### T-17 ✅ Full validation sweep
- **Action:**
  ```bash
  VAL=/home/fitiodev/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/scripts/quick_validate.py
  for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done
  ```
- **Verify:** 19 lines, every one ending in `Skill is valid!`.
- **Refs:** REQ-06.1

### T-18 ✅ Cross-ref sanity check
- **Action:**
  ```bash
  echo "=== craft refs in skills ==="
  grep -rln "craft/" skills/*/SKILL.md
  echo "=== dw: in skills ==="
  grep -lE "^dw:|^  dw:" skills/*/SKILL.md
  ```
- **Verify:** first command returns 5 paths (the 5 wired skills); second command returns same 5 paths IF T-07 chose frontmatter path; else returns 0 and the `dw.craft.requires` lives in body comments.

### T-19 ✅ Commit + push (commit `1173fe8`)
- **Action:**
  ```
  git add craft/ docs/skill-extensions.md skills/ .specs/project/STATE.md README.md .claude-plugin/marketplace.json
  git commit -m "feat(release): v1.1.1 — craft layer adopted from open-design"
  git push origin correcoes
  ```
  Message body details the 5 docs forked, 5 skills wired, attribution chain, source SHA.
- **Verify:** `git log -1 --stat` mostra `craft/*.md ×5`, `craft/README.md`, `docs/skill-extensions.md`, 5 skill edits, STATE.md, README.md, marketplace.json. Push exit code 0.

---

## Resumo de paralelização

- **Onda 1:** T-01..T-05 paralelizáveis (5 forks independentes); T-06 sequencial (precisa dos 5 prontos pra mapping table).
- **Onda 2:** T-07 → T-08 sequencial (T-08 depende da decisão de T-07).
- **Onda 3:** T-09..T-13 paralelizáveis (5 skills independentes).
- **Onda 4:** T-14..T-16 paralelizáveis.
- **Onda 5:** T-17 → T-18 → T-19 sequencial.

## Estimativa

- Onda 0: 5 min
- Onda 1: 35 min
- Onda 2: 25 min
- Onda 3: 30 min (paralelo)
- Onda 4: 15 min
- Onda 5: 15 min
- **Total: ~2 h** (vs 3h estimado em spec.md — buffer pro D-D fallback se T-07 forçar)

## Como retomar

Próxima sessão começa lendo:
1. `.specs/features/craft-adoption/spec.md`
2. `.specs/features/craft-adoption/design.md`
3. `.specs/features/craft-adoption/tasks.md`
4. `.specs/project/STATE.md` (last D-XX number)

Identifica primeiro task `⬜ pending` (T-00), confirma rollback tag, segue.
