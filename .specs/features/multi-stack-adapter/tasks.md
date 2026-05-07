# Tasks: multi-stack-adapter

> Atomic, sequenced. ≤30 min cada. Verificação binária.

**Workspace:** `/media/fitiodev/FITIO/Skill/design-workflow`
**Tag pre-rollback:** `pre-v1.2.0` (criar em T-00)
**Target:** v1.2.0
**Depends on:** v1.1.2 shipped (current).

Legenda: ✅ done · 🔄 in_progress · ⬜ pending · 🅿️ parallelizable

---

## Onda 0 — Safety net + regression baseline

### T-00 ✅ Tag rollback + snapshot pre-v1.2 outputs
- **Action:**
  ```bash
  git tag pre-v1.2.0
  mkdir -p .design-spec/regression-snapshots/pre-v1.2/flutter
  # Capture a known theme-port output for byte-diff in T-13.
  # Use a real Fitio frame already ported (Coupons milestone slider) — copy resulting Dart files to snapshot dir.
  # The exact files vary; intent: 1+ Dart file under app_colors.dart and 1+ widget file.
  ```
- **Verify:** `git tag | grep pre-v1.2.0` matches; snapshot dir non-empty.
- **Refs:** spec §6, design §"Validation strategy" #3
- **Blocks:** all

---

## Onda 1 — Adapter contract (the heart)

### T-01 ✅ Draft `docs/adapter-protocol.md`
- **Action:** write the contract per design §"Adapter Plan format" + §"Architecture". Sections: (1) Why a contract, (2) Plan format with example, (3) Adapter interface (input/output), (4) Conformance test, (5) How to add a new adapter, (6) Path conventions table per stack.
- **Time-budget:** 2h. If exceeded, escape per spec REQ-A risk: ship Plan with tokens-only, defer widgets/actions to v1.3.
- **Verify:** `wc -l docs/adapter-protocol.md` between 200–400; sections 1–6 all present.
- **Refs:** REQ-A.1

### T-02 ✅ Write `docs/adapter-plan.schema.json`
- **Action:** JSON Schema typed for the Plan format. Top-level: version, kind enum, tokens object (palette/typography/spacing/radius/motion), widgets array, actions array. Use Draft 7 for compat.
- **Verify:** `python3 -c "import json,jsonschema; jsonschema.validate(json.load(open('docs/adapter-examples/palette.json')), json.load(open('docs/adapter-plan.schema.json')))"` — feed the palette example, expect zero errors.
- **Refs:** REQ-A.2

### T-03 ✅ Write `docs/adapter-examples/palette.json`
- **Action:** complete Plan example with `kind: palette` — tokens.palette has the canonical 29 semantic tokens × 2 modes (light/dark). Actions: 1 write to `palette` role.
- **Verify:** `jsonschema validate` returns 0 errors against schema.
- **Refs:** REQ-A.3

### T-04 ✅ Write `docs/adapter-examples/widget-tree.json`
- **Action:** complete Plan with `kind: widget-tree` — a button + form group example (covers both leaf widget and container).
- **Verify:** schema validates.
- **Refs:** REQ-A.3

### T-05 ✅ Write `docs/adapter-examples/motion-set.json`
- **Action:** complete Plan with `kind: motion-set` — durations + curves matching current `AppMotion`/`AppCurves`.
- **Verify:** schema validates.
- **Refs:** REQ-A.3

---

## Onda 2 — Flutter adapter (reference, byte-equivalent)

### T-06 ✅ Stub `adapters/flutter/` skeleton
- **Action:** create dirs + stubs:
  ```
  adapters/flutter/
  ├── adapter.py       # entry point
  ├── mappings.py      # role → Dart accessor
  ├── templates/       # 3 .tmpl files (app_colors, widget, design_tokens)
  ├── STACK_NOTES.md   # conventions
  └── tests/
      ├── conformance.py
      └── golden/
  ```
- **Verify:** `find adapters/flutter -type f | wc -l` ≥ 6.
- **Refs:** REQ-B.1

### T-07 ✅ Implement `mappings.py` + 3 templates
- **Action:** TOKEN_ROLE_MAP (29 entries: `brandDefault` → `context.colors.brandDefault`); WIDGET_TYPE_MAP (`button` → `AppButton`, etc); 3 string templates capturing current `AppColors._light` / widget file / design-tokens.md format.
- **Verify:** `python3 -c "from adapters.flutter.mappings import TOKEN_ROLE_MAP; assert len(TOKEN_ROLE_MAP) >= 29"`.
- **Refs:** REQ-B.1

### T-08 ✅ Implement `adapter.py` main dispatch
- **Action:** entry function `main(plan_path, dry_run=False) -> int`; dispatch on `plan["kind"]` to `emit_palette` / `emit_widget_tree` / `emit_motion`. Each emit calls templates + writes per `actions[]`.
- **Verify:** `python3 adapters/flutter/adapter.py docs/adapter-examples/palette.json --dry-run` prints expected paths without writing.
- **Refs:** REQ-B.1

### T-09 ✅ Write conformance test + 3 goldens
- **Action:** for each example, manually craft expected Dart output (golden), commit. `tests/conformance.py`: runs adapter on each example with `--dry-run` capture, diffs against golden, prints PASS/FAIL.
- **Verify:** `python3 adapters/flutter/tests/conformance.py` prints `PASS: 3/3`.
- **Refs:** REQ-B.2

---

## Onda 3 — Next.js+Tailwind adapter (the new one)

### T-10 ⬜ Stub `adapters/nextjs-tailwind/` skeleton
- **Action:** mirror Flutter skeleton structure with `tokens.css.tmpl`, `tailwind.config.ts.tmpl`, `component.tsx.tmpl`, `component-shadcn.tsx.tmpl`, `design_tokens.md.tmpl`.
- **Verify:** `find adapters/nextjs-tailwind -type f | wc -l` ≥ 8.
- **Refs:** REQ-C.1

### T-11 ⬜ Implement `mappings.py` + project-detection helpers
- **Action:**
  - TOKEN_ROLE_MAP: 29 entries mapping role → CSS variable name (`brandDefault` → `--brand-default`).
  - WIDGET_TYPE_MAP: with shadcn variants vs plain Tailwind (`button` → `<Button>` vs `<button className=...>`).
  - SPACING_MAP / RADIUS_MAP: numeric value → Tailwind class (`16` → `4` in `p-4`, since Tailwind's spacing.4 = 1rem = 16px).
  - `has_shadcn()`: checks `components.json` exists OR `package.json.dependencies` contains any `@radix-ui/*`.
  - `app_router_or_pages()`: returns `"app"` if `app/` dir exists, else `"pages"`.
- **Verify:** `python3 -c "from adapters.nextjs_tailwind.mappings import TOKEN_ROLE_MAP, has_shadcn; assert len(TOKEN_ROLE_MAP) >= 29; print(has_shadcn())"` runs without error.
- **Refs:** REQ-C.1, REQ-C.4

### T-12 ⬜ Implement `adapter.py` for Next.js+Tailwind
- **Action:** entry `main(plan_path, dry_run=False)`. Detects project (shadcn? router?), picks templates accordingly, writes:
  - palette → `app/globals.css` (App Router) or `styles/tokens.css` (Pages) PLUS appends `theme.extend.colors` to `tailwind.config.ts`
  - widget-tree → `components/<feature>/<name>.tsx`
  - motion-set → CSS keyframes block in tokens file + Tailwind transitions config
- **Verify:** `python3 adapters/nextjs-tailwind/adapter.py docs/adapter-examples/palette.json --dry-run` prints sensible paths.
- **Refs:** REQ-C.1, REQ-C.2

### T-13 🅿️ Conformance test + 3 goldens (plain Tailwind variant)
- **Action:** craft expected outputs for plain Tailwind mode (no shadcn): `palette.css`, `widget-tree.tsx`, `motion-set.css`. Conformance script forces `shadcn=False`.
- **Verify:** `python3 adapters/nextjs-tailwind/tests/conformance.py --plain` prints `PASS: 3/3`.
- **Refs:** REQ-C.3

### T-14 🅿️ Conformance test + 1 shadcn golden (variant detection)
- **Action:** craft `widget-tree-shadcn.tsx` golden using `<Button>` from shadcn. Conformance script forces `shadcn=True`.
- **Verify:** `python3 adapters/nextjs-tailwind/tests/conformance.py --shadcn` prints `PASS: 3/3` (palette + motion identical, widget-tree picks shadcn variant).
- **Refs:** REQ-C.3, REQ-C.4

---

## Onda 4 — Stack config + dispatch

### T-15 ⬜ Add `stack:` + `paths:` to `config.example.yaml`
- **Action:** edit `config.example.yaml`:
  ```yaml
  # Active stack — selects the adapter for code emission.
  # Valid values: flutter (default), nextjs-tailwind. Other adapters land in v1.3+.
  stack: flutter

  # Optional path overrides per stack. Defaults documented in adapters/<stack>/STACK_NOTES.md.
  # paths:
  #   nextjs_tailwind:
  #     tokens_css: app/globals.css
  #     tailwind_config: tailwind.config.ts
  #     components_root: components
  ```
- **Verify:** `grep -E "^stack:" config.example.yaml` returns `stack: flutter`; `paths:` block present (commented).
- **Refs:** REQ-G.1

### T-16 ⬜ Resolution helper script
- **Action:** create `scripts/resolve_stack.py` — reads `STACK` env, falls back to `.design-workflow.yaml` `stack:`, falls back to `flutter`. Emits resolved value to stdout. Errors on unknown.
- **Verify:** `STACK=nextjs-tailwind python3 scripts/resolve_stack.py` prints `nextjs-tailwind`; `STACK=react-native python3 scripts/resolve_stack.py` exits non-zero with "available adapters: flutter, nextjs-tailwind".
- **Refs:** REQ-B.3

---

## Onda 5 — Migrate skills to adapter dispatch

### T-17 ⬜ Refactor `skills/theme-port/SKILL.md` workflow
- **Action:** restructure Workflow steps per design §"Migration shape for theme-port". Step 5 becomes "Build Adapter Plan"; new Step 6 "Resolve active stack"; Step 7 "Render via adapter"; Step 7.5 "Verify outputs"; Step 8 "Validate per stack" with branch flutter/nextjs-tailwind.
- **Verify:** `python3 $VAL skills/theme-port/` valid; `grep -c "Adapter Plan" skills/theme-port/SKILL.md` ≥ 2; `grep -c "stack:" skills/theme-port/SKILL.md` ≥ 1.
- **Refs:** REQ-D.1, REQ-D.4

### T-18 ⬜ Flutter regression smoke for theme-port
- **Action:** with `stack: flutter`, invoke `/theme-port` on the frame snapshotted in T-00. Diff resulting Dart byte-by-byte (modulo whitespace) against snapshot.
- **Verify:** `diff -r --strip-trailing-cr .design-spec/regression-snapshots/pre-v1.2/flutter/ <new-output>/` returns zero diff.
- **Refs:** REQ-D.2, REQ-I.3

### T-19 ⬜ Next.js+Tailwind manual smoke for theme-port
- **Action:** spin up minimal Next.js + Tailwind project (`npx create-next-app@latest --ts --tailwind --app /tmp/nextjs-smoke`). Set `stack: nextjs-tailwind` in `.design-workflow.yaml`. Invoke `/theme-port` on same Figma frame. Confirm: `app/globals.css` has CSS vars, `tailwind.config.ts` has `theme.extend.colors` from CSS vars, `components/<feature>/<name>.tsx` renders structure. Screenshot saved at `.design-spec/smoke/v1.2.0-nextjs-port.md`.
- **Verify:** smoke file exists with 3 ✅ checkboxes (CSS vars / Tailwind config / TSX component); manual visual check passed.
- **Refs:** REQ-D.3, REQ-I.4

### T-20 ⬜ Update theme-port eval
- **Action:** add assertion to `skills/theme-port/evals/evals.json`: an Adapter Plan JSON sidecar exists after invocation. Add per-stack expected output checks.
- **Verify:** eval passes manually on smokes from T-18 + T-19; `python3 $VAL skills/theme-port/` valid.
- **Refs:** REQ-D.5

### T-21 ⬜ Refactor `skills/theme-extend/SKILL.md`
- **Action:** same shape as theme-port — emit Plan describing token additions, dispatch adapter.
- **Verify:** `python3 $VAL skills/theme-extend/` valid; `grep -c "Adapter Plan" skills/theme-extend/SKILL.md` ≥ 1.
- **Refs:** REQ-E.1

### T-22 ⬜ Regression smoke for theme-extend (Flutter)
- **Action:** simulate adding a token (e.g. `feedbackPositive`) with `stack: flutter`. Confirm adapter writes to `lib/core/theme/app_colors.dart` + `docs/design-tokens.md` exactly as pre-v1.2.
- **Verify:** byte-equivalent against pre-v1.2 baseline (manually captured).
- **Refs:** REQ-E.2

### T-23 🅿️ Smoke for theme-extend (Next.js)
- **Action:** same token addition with `stack: nextjs-tailwind`. Confirm CSS var + Tailwind config update + design-tokens.md update.
- **Verify:** all 3 files updated correctly (manual review logged).
- **Refs:** REQ-E.1

---

## Onda 6 — Stack-aware audit

### T-24 ⬜ Refactor `scripts/audit_theme.py` for `--stack` flag
- **Action:** accept `--stack <flutter|nextjs-tailwind>`. Read lint regex set from `scripts/audit_lint_sets/<stack>.yaml`. WCAG logic intact.
- **Verify:** `python3 scripts/audit_theme.py --stack flutter --help` shows the flag; `--stack invalid` errors with available list.
- **Refs:** REQ-F.2

### T-25 🅿️ Write `audit_lint_sets/flutter.yaml`
- **Action:** YAML file with regex patterns currently hardcoded in audit_theme.py (move them).
- **Verify:** YAML loads cleanly; same patterns as before; audit on Fitio still flags same issues.
- **Refs:** REQ-F.1

### T-26 🅿️ Write `audit_lint_sets/nextjs-tailwind.yaml`
- **Action:** new patterns for Tailwind/JSX:
  - `text-\[#[0-9a-fA-F]+\]` (Tailwind arbitrary value with hex)
  - `bg-\[(#|rgb)` (Tailwind arbitrary bg)
  - `style=\{\{\s*\w+:\s*['"]#[0-9a-fA-F]` (inline style hex)
  - `from-\[#`, `to-\[#` (gradient arbitrary)
  - `hsl\(\s*\d` outside CSS variable definition
- **Verify:** YAML loads; manual smoke against `/tmp/nextjs-smoke/` finds at least 0 false positives + 0 missed obvious ones (sample test file with intentional violations).
- **Refs:** REQ-F.1

### T-27 ⬜ Update `skills/theme-audit/SKILL.md`
- **Action:** SKILL.md body reads resolved stack and passes `--stack` to script. Documents the per-stack pattern set.
- **Verify:** `python3 $VAL skills/theme-audit/` valid; `grep -c "stack:" skills/theme-audit/SKILL.md` ≥ 1.
- **Refs:** REQ-F.1, REQ-F.2

---

## Onda 7 — Docs + STATE + version

### T-28 🅿️ Update `docs/ROADMAP.md`
- **Action:** reverse the "Web-first design (Tailwind, MUI). Different aesthetic vocabulary; would require a separate web-design-workflow repo" entry — replace with date-marked note: "**Reversed 2026-05-06 in v1.2.0** — adapter pattern enabled web stacks in-repo, see `.specs/features/multi-stack-adapter/`." Add a v1.3+ adapter backlog list (React Native, Vue+Tailwind, Svelte+Tailwind, plain-React, SwiftUI).
- **Verify:** `grep -c "Reversed 2026-05-06" docs/ROADMAP.md` = 1; backlog list contains ≥ 4 stacks.
- **Refs:** REQ-G.3

### T-29 🅿️ Update README §What changed in v1.2.0 + Stack support section
- **Action:**
  - new `## What changed in v1.2.0` (above v1.1.2)
  - new top-level `## Stack support` listing Flutter + Next.js/Tailwind, link to `docs/adapter-protocol.md` for adding stacks
- **Verify:** `grep -c "What changed in v1.2.0" README.md` = 1; `grep -c "## Stack support" README.md` = 1.
- **Refs:** REQ-G.2, REQ-G.4

### T-30 🅿️ Append D-14, D-15, D-16 to STATE.md
- **Action:** D-14 (adapter contract: 2 reference adapters in v1.2), D-15 (reverse Web-out-of-scope ROADMAP entry), D-16 (roadmap reorder rationale).
- **Verify:** `grep -c "^- \*\*D-1[456]" .specs/project/STATE.md` = 3.
- **Refs:** REQ-H

### T-31 🅿️ Bump `marketplace.json` 1.1.2 → 1.2.0
- **Action:** Edit `version` field; update top-level description to mention multi-stack support.
- **Verify:** `jq -r '.metadata.version' .claude-plugin/marketplace.json` = `1.2.0`.
- **Refs:** REQ-I.5

---

## Onda 8 — Final validation + ship

### T-32 ⬜ Full validation sweep
- **Action:** `quick_validate.py` for all 19 skills.
- **Verify:** 19/19 `Skill is valid!`.
- **Refs:** REQ-I.1

### T-33 ⬜ Run all conformance + regression smokes
- **Action:**
  ```bash
  python3 adapters/flutter/tests/conformance.py            # PASS: 3/3
  python3 adapters/nextjs-tailwind/tests/conformance.py    # PASS: 3/3 (plain) + 1 shadcn
  # T-18, T-19, T-22, T-23 smokes already captured
  ```
- **Verify:** all green.
- **Refs:** REQ-I.2, REQ-I.3, REQ-I.4

### T-34 ⬜ Commit + push
- **Action:**
  ```bash
  git add adapters/ docs/adapter-protocol.md docs/adapter-plan.schema.json docs/adapter-examples/ \
          docs/ROADMAP.md scripts/audit_theme.py scripts/audit_lint_sets/ scripts/resolve_stack.py \
          skills/theme-port/ skills/theme-extend/ skills/theme-audit/ \
          README.md .specs/project/STATE.md .claude-plugin/marketplace.json config.example.yaml \
          .design-spec/regression-snapshots/ .design-spec/smoke/
  git commit -m "feat(release): v1.2.0 — multi-stack adapter (Flutter + Next.js/Tailwind)"
  git push origin correcoes
  ```
- **Verify:** push exit 0; `git log -1 --stat` shows expected file list (adapters/ ×2, docs/ ×3, scripts/ ×3, skills/ ×3, etc).

### T-35 ⬜ Tag + GitHub release
- **Action:** `git tag -a v1.2.0 <commit-sha> -m "..."` + push tag + `gh release create v1.2.0 --latest --notes ...`.
- **Verify:** `gh release list --limit 5` shows v1.2.0 as Latest.

---

## Resumo de paralelização

- **Onda 0:** T-00 sequencial.
- **Onda 1:** T-01 → T-02 sequencial; T-03..T-05 paralelizáveis.
- **Onda 2:** T-06 → T-07 → T-08 → T-09 sequencial.
- **Onda 3:** T-10 → T-11 → T-12 sequencial; T-13 + T-14 paralelizáveis.
- **Onda 4:** T-15 + T-16 paralelizáveis após Onda 3.
- **Onda 5:** T-17 → T-18 → T-19 → T-20 sequencial (theme-port track); T-21 → T-22 sequencial (theme-extend track); **theme-port track e theme-extend track paralelizáveis entre si**; T-23 paralelizável após T-21.
- **Onda 6:** T-24 → T-27 sequencial; T-25 + T-26 paralelizáveis após T-24.
- **Onda 7:** T-28..T-31 paralelizáveis.
- **Onda 8:** T-32 → T-33 → T-34 → T-35 sequencial.

## Estimativa

- Onda 0: 30 min
- Onda 1: 3.5h (contract is the heart)
- Onda 2: 3h (Flutter adapter)
- Onda 3: 4h (Next.js adapter, the new ground)
- Onda 4: 30 min
- Onda 5: 3h (2 migrations × 2 stacks of smokes)
- Onda 6: 1h
- Onda 7: 1h
- Onda 8: 30 min
- **Total: ~16.5h** (matches Large sizing; defer-to-tokens-only escape hatch keeps it bounded)

## Como retomar

1. Read spec.md + design.md + tasks.md
2. Confirm `pre-v1.2.0` tag + check that v1.1.2 shipped (`git tag -l v1.*` shows v1.1.2 plus pre-v1.2.0 in local)
3. Próximo `⬜ pending`
4. Time-check at T-01: if contract design exceeds 4h, invoke escape per spec REQ-A risk (tokens-only Plan, defer widgets/actions)

## Como testar Next.js+Tailwind end-to-end (quick path para o user)

Depois de Onda 5 fechar:
```bash
# Em qualquer Next.js + Tailwind project:
echo "stack: nextjs-tailwind" > .design-workflow.yaml
# No Claude Code:
/theme-port https://figma.com/design/...?node-id=...
# Espera: components/<feature>/<name>.tsx + atualizações em app/globals.css + tailwind.config.ts
```
