# Tasks: adapter-and-wireframe

> Atomic, sequenced. ≤30 min cada. Verificação binária.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.4.0` (criar em T-00)
**Target:** v1.4.0
**Depends on:** v1.1.1, v1.2.0, v1.3.0 all shipped.

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Safety net

### T-00 ⬜ Tag rollback + capture upstream SHA + snapshot pre-v1.4 outputs
- **Action:**
  ```bash
  git tag pre-v1.4.0
  UPSTREAM_SHA=$(gh api repos/nexu-io/open-design/branches/main --jq '.commit.sha')
  echo "Upstream SHA: $UPSTREAM_SHA" >> /tmp/v1.4.0-source.txt
  # Snapshot a known theme-port output for regression diff in T-12
  mkdir -p .design-spec/regression-snapshots/pre-v1.4
  # capture: at this point Fitio's milestone-slider widget exists somewhere; copy to snapshot dir
  ```
- **Verify:** tag exists; SHA + regression snapshot dir captured.
- **Refs:** spec §6, design §"Validation strategy" #3
- **Blocks:** all

---

## Onda 1 — Adapter contract design (the heaviest single task)

### T-01 ⬜ Draft `docs/adapter-protocol.md`
- **Action:** write the contract per design §"Adapter Plan format" + §"Architecture". Sections: (1) Why a contract, (2) Plan format with example, (3) Adapter interface (input/output), (4) Conformance test, (5) How to add a new adapter.
- **Time-budget:** 2h. If exceeded, escape per spec REQ-A risk: ship Plan with tokens-only, defer widgets/actions to v1.5.
- **Verify:** `wc -l docs/adapter-protocol.md` between 200–400; sections 1–5 all present.
- **Refs:** REQ-A.1

### T-02 ⬜ Write `docs/adapter-plan.schema.json`
- **Action:** JSON Schema typed for the Plan format. 3 top branches: tokens, widgets, actions. Use Draft 7 for compat.
- **Verify:** `python3 -c "import json,jsonschema; jsonschema.validate({...}, json.load(open('docs/adapter-plan.schema.json')))"` — feed a valid example and confirm zero errors.
- **Refs:** REQ-A.2

### T-03 🅿️ Write `docs/adapter-examples/palette.json`
- **Action:** complete Plan example with `kind: palette` — tokens.palette has 29 AppColors tokens × 2 modes. actions: write 1 file (`lib/core/theme/app_colors.dart`).
- **Verify:** `jsonschema validate adapter-plan.schema.json docs/adapter-examples/palette.json` returns 0 errors.
- **Refs:** REQ-A.3

### T-04 🅿️ Write `docs/adapter-examples/widget-tree.json`
- **Action:** complete Plan with `kind: widget-tree` — a real example like the milestone slider (4-state tabs, AppButton CTAs, AppFormGroup).
- **Verify:** validates against schema.
- **Refs:** REQ-A.3

### T-05 🅿️ Write `docs/adapter-examples/motion-set.json`
- **Action:** complete Plan with `kind: motion-set` — defines AppMotion durations + AppCurves entries.
- **Verify:** validates against schema.
- **Refs:** REQ-A.3

---

## Onda 2 — Flutter adapter

### T-06 ⬜ Stub `adapters/flutter/` skeleton
- **Action:** create dirs + stubs:
  ```
  adapters/flutter/
  ├── adapter.py       # entry point
  ├── mappings.py      # role → Dart accessor
  ├── templates/       # 3 .tmpl files (app_colors, widget, design_tokens)
  └── tests/
      ├── conformance.py
      └── golden/      # 3 expected output files
  ```
- **Verify:** `find adapters/flutter -type f | wc -l` ≥ 7.
- **Refs:** REQ-B.1

### T-07 ⬜ Implement `mappings.py` + 3 templates
- **Action:** TOKEN_ROLE_MAP (e.g. `brandDefault` → `context.colors.brandDefault`); WIDGET_TYPE_MAP (`AppButton` → `AppButton(...)`); 3 string templates.
- **Verify:** import smoke: `python3 -c "from adapters.flutter.mappings import TOKEN_ROLE_MAP, WIDGET_TYPE_MAP; assert len(TOKEN_ROLE_MAP) == 29"`.
- **Refs:** REQ-B.1

### T-08 ⬜ Implement `adapter.py` main dispatch
- **Action:** entry function `main(plan_path) -> int`; dispatch on `plan["kind"]` to `emit_palette` / `emit_widget_tree` / `emit_motion`. Each emit function calls templates + writes per `actions[]`.
- **Verify:** `python3 adapters/flutter/adapter.py docs/adapter-examples/palette.json --dry-run` prints what would be written without writing.
- **Refs:** REQ-B.1

### T-09 ⬜ Write conformance test + 3 goldens
- **Action:** for each example, manually craft the expected Dart output (golden), commit. `tests/conformance.py`: runs adapter on each example, diffs against golden, prints PASS/FAIL.
- **Verify:** `python3 adapters/flutter/tests/conformance.py` prints `PASS: 3/3`.
- **Refs:** REQ-B.2

### T-10 ⬜ Add `stack:` config + `AGENT_STACK` env var
- **Action:** edit `config.example.yaml` to add `stack: flutter` field (commented as "default; override per-project"); SKILL.md bodies for theme-port + theme-extend read either env or config to choose adapter.
- **Verify:** `grep "stack:" config.example.yaml` returns match; SKILL.md bodies reference the resolution order.
- **Refs:** REQ-B.3

---

## Onda 3 — Migrate theme-port + theme-extend

### T-11 ⬜ Refactor `skills/theme-port/SKILL.md` workflow
- **Action:** restructure Workflow steps per design §"Migration shape for theme-port". Step 5 becomes "Build Adapter Plan"; new Step 6 "Render via adapter"; Step 7 stays validate.
- **Verify:** `python3 $VAL skills/theme-port/` valid; `grep -c "Adapter Plan" skills/theme-port/SKILL.md` ≥ 2.
- **Refs:** REQ-C.1, REQ-C.3

### T-12 ⬜ Regression smoke for theme-port
- **Action:** invoke `/theme-port` on the same Figma frame captured in T-00 snapshot. Diff resulting Dart byte-by-byte against snapshot.
- **Verify:** `diff -r .design-spec/regression-snapshots/pre-v1.4/ <new-output>/` returns zero diff (modulo whitespace formatting).
- **Refs:** REQ-C.2, spec §8

### T-13 ⬜ Update theme-port eval
- **Action:** add assertion to `skills/theme-port/evals/evals.json` that an adapter Plan is emitted (regex detect of `*-plan.json` artifact in stdout or sidecar).
- **Verify:** eval passes manually on the smoke run; `python3 $VAL skills/theme-port/` valid.
- **Refs:** REQ-C.4

### T-14 ⬜ Refactor `skills/theme-extend/SKILL.md`
- **Action:** same shape as theme-port — emit Plan describing token additions, dispatch adapter.
- **Verify:** `python3 $VAL skills/theme-extend/` valid.
- **Refs:** REQ-D.1

### T-15 ⬜ Regression smoke for theme-extend
- **Action:** simulate adding a token (e.g. `feedbackPositive`) — confirm adapter writes to `lib/core/theme/app_colors.dart` + `docs/design-tokens.md` exactly as pre-v1.4.
- **Verify:** byte-equivalent.
- **Refs:** REQ-D.2

---

## Onda 4 — Wireframe-sketch (parallelizable with Onda 3)

### T-16 🅿️ Fork `skills/wireframe-sketch/SKILL.md` from open-design
- **Action:** fetch upstream, add attribution header (Source from open-design + originating huashu-design), copy body verbatim.
- **Verify:** file exists; `head -8` has attribution; `python3 $VAL skills/wireframe-sketch/` valid.
- **Refs:** REQ-E.1

### T-17 🅿️ Add Esboço/Sketcher persona + craft tie-in
- **Action:** edit the forked SKILL.md:
  - Triggers section: add `/Esboço`, `/Sketcher`, "esboço", "rascunho da tela"
  - Update description to mention the persona (PT primary)
  - Body: add a "## Pairing with state coverage" section referencing `craft/state-coverage.md` (each tab = different state)
  - `dw.craft.requires: [state-coverage]`
- **Verify:** `python3 $VAL skills/wireframe-sketch/` valid; `grep -c "Esboço" skills/wireframe-sketch/SKILL.md` ≥ 1; `grep -c "state-coverage" skills/wireframe-sketch/SKILL.md` ≥ 1.
- **Refs:** REQ-E.2, REQ-E.3, REQ-E.4

### T-18 🅿️ Add Sketcher row to `docs/personas.md`
- **Action:** append row: `| wireframe-sketch | Sketcher | Esboço | Generates a hand-drawn lo-fi exploration with N variant tabs (graph paper, marker tone, sticky-note annotations) | /Esboço, /Sketcher, /wireframe-sketch |`.
- **Verify:** `grep -c "Esboço" docs/personas.md` ≥ 1.
- **Refs:** REQ-F.4

### T-19 ⬜ Smoke test wireframe-sketch
- **Action:** `/wireframe-sketch "milestone slider 4 variants"` → confirm output at `.design-spec/wireframes/...html`. Open in browser, confirm: graph paper bg, 4 tabs, marker-toned headlines, sticky-note annotations.
- **Verify:** file opens; visual elements present (manual review noted in `.design-spec/smoke/v1.4.0-...md`).
- **Refs:** spec §8

---

## Onda 5 — Pipeline + STATE + version

### T-20 ⬜ Update `docs/theme-manager.md`
- **Action:** "I'm starting a new app" workflow gains a wireframe step (optional, before frontend-design); "Stack assumptions" section gains adapter notes.
- **Verify:** `grep -c "wireframe-sketch\|Esboço" docs/theme-manager.md` ≥ 1; `grep -c "adapter\|stack:" docs/theme-manager.md` ≥ 2.
- **Refs:** REQ-F.3

### T-21 ⬜ Update README §What changed in v1.4.0 + Adapter system section
- **Action:**
  - new `## What changed in v1.4.0` section (above v1.3.0)
  - new top-level `## Adapter system` section explaining contract + how to add adapters
- **Verify:** `grep -c "What changed in v1.4.0" README.md` = 1; `grep -c "## Adapter system" README.md` = 1.
- **Refs:** REQ-F.1, REQ-F.2

### T-22 ⬜ Append D-18, D-19 to STATE.md
- **Action:** D-18 (adapter contract: stack-agnostic intermediate, Flutter as reference, byte-equivalent migration) + D-19 (wireframe-sketch as opt-in early-exploration).
- **Verify:** `grep -c "^- \*\*D-1[89]" .specs/project/STATE.md` = 2.
- **Refs:** REQ-G

### T-23 ⬜ Update `marketplace.json`
- **Action:** add `./skills/wireframe-sketch`; bump version `1.3.0` → `1.4.0`; update top-level description.
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `1.4.0`; `jq '.plugins[0].skills | length'` = 21.
- **Refs:** REQ-H.4

---

## Onda 6 — Final validation + commit

### T-24 ⬜ Full validation sweep
- **Action:** `quick_validate.py` for all 21 skills.
- **Verify:** 21 lines `Skill is valid!`.
- **Refs:** REQ-H.1

### T-25 ⬜ Run conformance + regression smokes
- **Action:**
  ```bash
  python3 adapters/flutter/tests/conformance.py        # PASS: 3/3
  # plus T-12 + T-15 regression smokes already captured
  ```
- **Verify:** all green.
- **Refs:** REQ-H.2, REQ-H.3

### T-26 ⬜ Commit + push
- **Action:**
  ```
  git add adapters/ docs/adapter-protocol.md docs/adapter-plan.schema.json docs/adapter-examples/ skills/theme-port skills/theme-extend skills/wireframe-sketch docs/personas.md docs/theme-manager.md README.md .specs/project/STATE.md .claude-plugin/marketplace.json config.example.yaml .design-spec/regression-snapshots/ .design-spec/smoke/
  git commit -m "feat(release): v1.4.0 — adapter system foundation + wireframe-sketch"
  git push origin correcoes
  ```
- **Verify:** push exit 0.

---

## Resumo de paralelização

- **Onda 0:** T-00 sequencial.
- **Onda 1:** T-01 → T-02 sequencial; T-03..T-05 paralelizáveis.
- **Onda 2:** T-06 → T-07 → T-08 → T-09 sequencial; T-10 paralelizável após T-08.
- **Onda 3:** T-11 → T-12 → T-13 sequencial; T-14 → T-15 sequencial. Onda 3 paralelizável internamente (theme-port track vs theme-extend track).
- **Onda 4:** T-16 → T-17 → T-18 → T-19 sequencial; **toda a Onda 4 paralelizável com Onda 3** (independent files).
- **Onda 5:** T-20..T-23 paralelizáveis.
- **Onda 6:** T-24 → T-25 → T-26 sequencial.

## Estimativa

- Onda 0: 30 min
- Onda 1: 4h (contract is the heart)
- Onda 2: 4h (adapter implementation + golden tests)
- Onda 3: 3h (2 migrations + smokes)
- Onda 4: 2h (wireframe straightforward fork)
- Onda 5: 1.5h
- Onda 6: 1h
- **Total: 16h** (matches 12-16h spec; v1.4 is the heaviest release in the plan)

## Como retomar

1. Read spec.md + design.md + tasks.md
2. Confirm `pre-v1.4.0` tag + check that v1.1.1/1.2.0/1.3.0 all shipped (`git tag` shows pre-v1.X.X for each)
3. Próximo `⬜ pending`
4. Time-check at T-01: if contract design exceeds 2h, invoke escape per spec REQ-A risk
