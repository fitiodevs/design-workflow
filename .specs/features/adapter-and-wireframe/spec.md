# Feature: adapter-and-wireframe

> Two distinct deliverables bundled into v1.4.0:
> **(A) Adapter system foundation** — define a stack-agnostic skill output contract; ship the Flutter adapter as the reference implementation; migrate `theme-port` and `theme-extend` to consume the adapter. Unblocks future React Native / SwiftUI / Web adapters without rewriting skills. (B) **`wireframe-sketch` skill** — fork open-design's lo-fi exploration skill so designers can sketch hand-drawn wireframes (graph paper / marker tone / annotations) before committing to hi-fi mockups in Clara.

**Status:** Draft (ready for execution)
**Target release:** v1.4.0
**Sized:** Large+ (multi-component, ~12-16h, adapter is the heavy item; wireframe-sketch is light add)
**Owner:** fitiodev
**Created:** 2026-05-05
**Source:**
- Adapter system — original design-workflow ROADMAP §v0.3 ("Adapter system"), still pending. Bigger scope: realistic to ship contract + Flutter adapter + 2 migrated skills here; remaining migrations + non-Flutter adapters deferred to v1.5+.
- Wireframe-sketch — fork of `nexu-io/open-design` `skills/wireframe-sketch/` (Apache-2.0).

**Depends on:** v1.1.1 (`craft-adoption`), v1.2.0 (`inspiration-library`), v1.3.0 (`interactive-mockup-stage`) all shipped. Adapter touches `theme-port` which by v1.3 already emits CSS-custom-property mockups (still produces Dart on the Flutter side though).

---

## 1. Context

### Adapter system (the big rock)

Today every skill that produces output assumes Flutter:
- `theme-port` writes Dart widgets in `lib/features/<feature>/`, references `AppColors`, `AppSpacing`, `AppRadius`, `TextTheme`.
- `theme-extend` writes Dart token files at `lib/core/theme/`.
- `theme-create` emits Dart `AppColors` snippet.
- `theme-motion` writes `AppMotion` / `AppCurves` and `flutter_animate` snippets.

Original ROADMAP §v0.3 called for an adapter system that decouples skill **logic** from stack-specific **emission**. Skills decide WHAT (token role mappings, structural extraction, motion intent); adapters decide HOW (`Color(0xFF...)` vs `var(--accent)` vs `Colors.terracotta`). Without this, every new stack means every Flutter-coupled skill gets rewritten — combinatorial explosion.

This is also a **prerequisite for the Inspiration Library to compose with non-Flutter projects** in the future. v1.2.0's translator emits Dart `AppColors`; with adapters, it emits a stack-neutral intermediate, then the active adapter renders to Dart / TS / Swift.

### Wireframe-sketch (the small rock)

Open-design ships a `wireframe-sketch` skill that emits a lo-fi exploration: graph-paper background, pencil/marker tone, hatched fills, sticky-note annotations, multi-tab variant exploration. Use case: before committing to Clara's hi-fi (`/frontend-design`), the designer wants to sketch 4-tab variants in 30 seconds — what's the layout? where's the main affordance? Lo-fi forces decisions about hierarchy that hi-fi can hide behind polish.

Pairs naturally with v1.3's tweaks pipeline: sketch → pick layout → Clara hi-fi → tweaks → port.

## 2. Goal

After this feature:

### Adapter side
- **Adapter contract** (`docs/adapter-protocol.md`) defines a stack-agnostic intermediate format: token role mappings, widget tree shape, motion intent, that any skill can emit and any adapter can render.
- **Flutter adapter** (`adapters/flutter/`) ships as the first reference implementation — receives intermediate, emits Dart code matching current `theme-port` / `theme-extend` / `theme-create` outputs (zero behavior change for existing Fitio users).
- **`theme-port` and `theme-extend` migrated** to the adapter pattern. Other skills (theme-create, theme-motion) tracked as v1.5 follow-up — would over-scope this release.
- **`AGENT_STACK` config** (`config.example.yaml` field, repo-level override) tells the adapter which adapter to use. Default: `flutter`.
- Behavior is byte-equivalent for Fitio. The contract just exists now, ready to grow.

### Wireframe side
- New skill `skills/wireframe-sketch/` forked from open-design with attribution.
- Emits a single `.html` lo-fi sketch with N tabs (default 4) for variant exploration.
- Pairs with `craft/state-coverage.md` (each tab can preview a different state — empty/populated/error).
- README and pipeline docs add the optional sketch step before `/frontend-design`.

## 3. Non-goals

- **Not** shipping React Native, SwiftUI, or Web adapters in v1.4. The contract is designed to support them; concrete adapters land in v1.5/v1.6 when there's a real consumer.
- **Not** migrating `theme-create` or `theme-motion` to adapter pattern. Defer to v1.5 (`adapter-migration-phase-2`). Reason: each skill migration is its own design exercise and v1.4 already carries the contract definition + 2 migrations.
- **Not** rewriting `references/` content for adapter-aware skills. References stay Flutter-flavored in v1.4 because they're internal docs, not user-facing emission.
- **Not** breaking the existing CLI surface. `/theme-port` still works for Fitio without any config change (the adapter defaults to flutter).
- **Not** running `/wireframe-sketch` automatically before `/frontend-design`. It's an opt-in step the user invokes when they want lo-fi exploration first.
- **Not** building a DSL for the intermediate format. Plain JSON-serialisable Python dicts; if too verbose later, DSL is a separate v1.5+ exercise.

## 4. Requirements

### REQ-A — Adapter contract definition

- **REQ-A.1** Write `docs/adapter-protocol.md` documenting:
  - The intermediate format (an Adapter Plan) — token roles, widget tree shape, motion intent, file outputs
  - The adapter interface — input (Adapter Plan + project context) → output (file writes)
  - The conformance test suite (one Plan, all adapters must produce equivalent visual results)
- **REQ-A.2** Define the Plan as a typed JSON Schema in `docs/adapter-plan.schema.json`. Three top-level branches: `tokens` (palette/typography/spacing/radius/motion), `widgets` (structural tree from theme-port), `actions` (file writes the adapter performs).
- **REQ-A.3** Document at least 3 example Plans in `docs/adapter-examples/` (`palette.json`, `widget-tree.json`, `motion-set.json`) — these are the test fixtures.

### REQ-B — Flutter adapter implementation

- **REQ-B.1** `adapters/flutter/` directory with:
  - `adapter.py` — main entry: `python adapters/flutter/adapter.py <plan.json>` reads Plan, emits Flutter files matching current behavior of theme-port/theme-extend.
  - `templates/` — Dart string templates per output type (AppColors snippet, widget file, AppSpacing, etc).
  - `mappings.py` — token role → Dart accessor (`brandDefault` → `context.colors.brandDefault`), widget element → component (`<button>` → `AppButton`).
- **REQ-B.2** Conformance test: feed each `docs/adapter-examples/*.json` through `adapters/flutter/adapter.py`; output must match a known-good golden file in `adapters/flutter/tests/golden/`.
- **REQ-B.3** Adapter is configurable via `AGENT_STACK` env var or `.design-workflow.yaml` `stack:` field. Default: `flutter`. Unknown stack → error with explicit message.

### REQ-C — Migrate `theme-port` to adapter pattern

- **REQ-C.1** `theme-port` SKILL.md body refactored: extract the "emit Dart widget" logic into "emit Adapter Plan", then dispatch to adapter via `Bash`.
- **REQ-C.2** Functional outcome unchanged: a Figma frame port produces the same Dart files at the same paths as before v1.4.
- **REQ-C.3** A new internal step "Step 7.5 — Render via adapter" in the workflow.
- **REQ-C.4** Eval (theme-port/evals/evals.json) gets one new assertion: "Adapter Plan was emitted" (regex-detect a JSON file in stdout or sidecar).

### REQ-D — Migrate `theme-extend` to adapter pattern

- **REQ-D.1** Same shape as REQ-C — `theme-extend` emits a Plan describing token additions, adapter renders to `lib/core/theme/app_colors.dart` + `docs/design-tokens.md`.
- **REQ-D.2** Behavior byte-equivalent for Fitio.

### REQ-E — `wireframe-sketch` skill

- **REQ-E.1** Fork `skills/wireframe-sketch/SKILL.md` from open-design with full attribution header.
- **REQ-E.2** Update body to reference our craft (`craft/state-coverage.md` — useful for "each tab is a different state") and our pipeline (after sketch, route to `/frontend-design` for hi-fi).
- **REQ-E.3** Persona: Esboço (PT) / Sketcher (EN). New persona row in `docs/personas.md`.
- **REQ-E.4** Triggers: `/wireframe-sketch`, `/Esboço`, `/Sketcher`, "lo-fi mockup", "wireframe", "esboço", "rascunho da tela".

### REQ-F — Pipeline + docs

- **REQ-F.1** README §What changed in v1.4.0 documents adapter system + wireframe-sketch.
- **REQ-F.2** New top-level "Adapter system" section in README explaining the contract + how to add adapters.
- **REQ-F.3** `docs/theme-manager.md` updates: add wireframe step in "I'm starting a new app", add adapter notes in "Stack assumptions".
- **REQ-F.4** `docs/personas.md` adds Sketcher row.

### REQ-G — STATE.md decisions

- **REQ-G.1** D-18 — Adapter contract: stack-agnostic intermediate format (Adapter Plan), Flutter adapter as reference, byte-equivalent migration for theme-port + theme-extend, others deferred.
- **REQ-G.2** D-19 — Wireframe-sketch as opt-in early-exploration: lo-fi sketch step is optional in the pipeline, useful for "I don't know the layout yet" cases.

### REQ-H — Validate + bump

- **REQ-H.1** `quick_validate.py` 21/21 valid (was 20; +1 for wireframe-sketch).
- **REQ-H.2** Conformance test passes: all 3 example Plans through the Flutter adapter match goldens.
- **REQ-H.3** Regression smoke: invoke `theme-port` on a real Fitio frame; verify Dart output matches pre-v1.4 byte-for-byte (modulo file timestamp / formatting whitespace).
- **REQ-H.4** `marketplace.json` bumped 1.3.0 → 1.4.0 + add `./skills/wireframe-sketch`.

## 5. Out of scope (deferred)

- **React Native / SwiftUI / Web adapters** — separate releases (v1.5+ each).
- **`theme-create`, `theme-motion` migrations to adapter** — v1.5 candidate (`adapter-migration-phase-2`).
- **Multi-stack output simultaneously** (a Plan emits both Dart and Swift). Possible in v1.6 once 2+ adapters exist.
- **Adapter discovery via plugin marketplace**. Adapters live in-repo in v1.4; a registry mechanism is its own design.
- **Wireframe-sketch with auto-export to Clara**. The user picks the chosen sketch tab manually and prompts Clara separately. v1.5 candidate.
- **Co-locate craft/anti-ai-slop with adapter checks** (linter). Currently craft is reference-only; making it executable is a separate effort.

## 6. Source pin

- Upstream repo: `nexu-io/open-design`
- Upstream branch: `main`
- Upstream SHA at fork time: **TBD — capture during T-00**
- Upstream license: Apache-2.0
- For wireframe-sketch: originating attribution in upstream skill body (likely `huashu-design`).

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Adapter Plan format proves insufficient for real cases — bikeshedding the schema delays release | High | T-01 reviews 5 real cases (port + extend + a hypothetical RN port + a hypothetical SwiftUI port) before locking the schema; fallback if blocked: ship Plan minimally (just tokens), defer widgets/actions to v1.5 (still meaningful release) |
| theme-port migration breaks Fitio in subtle way (wrong path, wrong import) | Medium | T-12 runs the regression smoke comparing pre-v1.4 output byte-for-byte; only commits when match. |
| Wireframe-sketch doesn't add value (users skip the step) | Medium | Ship as opt-in, no auto-trigger. If usage stays at zero after 1 release cycle, deprecate cleanly. |
| 12-16h estimate is optimistic for adapter contract design | Medium | Spec explicitly defers `theme-create`/`theme-motion` migrations to v1.5. If T-01 design exceeds 4h, bail to "Plan tokens only, defer widgets/actions" path. |
| New `AGENT_STACK` config breaks existing `.design-workflow.yaml` users | Low | Default to `flutter` if missing; only error on explicit unknown value. |

## 8. Acceptance criteria

- [ ] REQ-A..REQ-H all verified
- [ ] Adapter contract documented with 3 example Plans
- [ ] Flutter adapter passes conformance test on all 3 example Plans
- [ ] `theme-port` and `theme-extend` migrated; regression smoke matches pre-v1.4
- [ ] `wireframe-sketch` skill ships and `/wireframe-sketch` invocation produces a sensible lo-fi HTML
- [ ] STATE.md has D-18, D-19
- [ ] All 21 skills pass `quick_validate.py`
- [ ] Single commit: `feat(release): v1.4.0 — adapter system foundation + wireframe-sketch`
