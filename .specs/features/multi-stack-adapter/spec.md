# Feature: multi-stack-adapter

> Stack-agnostic adapter system. Skills emit a neutral Adapter Plan; per-stack adapters render to native code. v1.2.0 ships **two** reference adapters — Flutter (existing behavior, byte-equivalent) and **Next.js + Tailwind** (new) — proving the contract handles both widget-tree imperative and JSX/utility-first paradigms. Other stacks (React Native, Vue, Svelte, SwiftUI) become additive in v1.3+ with no skill changes.

**Status:** Draft (ready for execution)
**Target release:** v1.2.0 (pulled forward from v1.4.0 per user urgency 2026-05-06; reversal of original ROADMAP §"Out of scope" note that excluded web stacks)
**Sized:** Large (multi-component, ~14h, contract design + 2 adapter implementations + 2 skill migrations + stack-aware audit)
**Owner:** fitiodev
**Created:** 2026-05-05 (as `adapter-and-wireframe`)
**Renamed:** 2026-05-06 → `multi-stack-adapter` (wireframe-sketch portion split out, see `.specs/features/wireframe-sketch/`)
**Source:** original design-workflow ROADMAP §v0.3 ("Adapter system") plus user-driven Next.js+Tailwind requirement.

**Depends on:** v1.1.2 shipped (current). Original v1.2/v1.3 dependencies (inspiration-library, interactive-mockup-stage) DROPPED — those features are orthogonal and pushed back to v1.3/v1.4 respectively.

---

## 1. Context

Today every wired skill that emits code assumes Flutter:
- `theme-port` writes Dart widgets in `lib/features/<feature>/`, references `AppColors`, `AppSpacing`, `AppRadius`, `TextTheme`.
- `theme-extend` writes Dart token files at `lib/core/theme/`.
- `theme-create` emits Dart `AppColors` snippet.
- `theme-motion` writes `AppMotion` / `AppCurves` and `flutter_animate` snippets.
- `theme-audit` greps `lib/` for `Color(0xFF...)`, `fontSize:` literals, etc.

The skill **logic** (token role mappings, structural extraction, motion intent, anti-AI-slop heuristics, state coverage rules) is universal. Only the **emission** is stack-coupled. A Flutter-only repo can't grow into the Next.js apps the user is starting now without rewriting every wired skill — combinatorial explosion.

This was previously roadmapped for v1.4.0 with "Out of scope: Web-first design (Tailwind, MUI). Different aesthetic vocabulary." That note is reversed: anti-AI-slop is the same in JSX as in Dart; only the syntax differs. The adapter system is exactly the right boundary.

User context (2026-05-06): they need to ship Next.js+Tailwind work this week, urgency high. Pulling adapter forward to v1.2 unblocks them; original v1.2 (inspiration-library) and v1.3 (interactive-mockup-stage) shift back one slot each.

## 2. Goal

After this feature:

- **Adapter contract** (`docs/adapter-protocol.md`) defines a stack-agnostic intermediate format: token role mappings, widget tree shape, motion intent, file actions. Any skill emits Plans; any adapter renders Plans.
- **Two reference adapters ship**:
  - `adapters/flutter/` — byte-equivalent to current behavior. Zero regression for the Fitio dogfood path.
  - `adapters/nextjs-tailwind/` — emits CSS custom properties, Tailwind config snippets, and TSX components using shadcn/ui primitives where applicable.
- **`stack:` config field** in `.design-workflow.yaml` (or `STACK` env var) tells skills which adapter to dispatch to. Default: `flutter` for backward compat. Setting `stack: nextjs-tailwind` flips emission for the same skill invocation.
- **`theme-port` and `theme-extend` migrated** to the adapter pattern — emit Plan, dispatch adapter via `Bash`. `theme-create` and `theme-motion` deferred to v1.3 follow-up (`adapter-migration-phase-2`).
- **`theme-audit` becomes stack-aware** — its lint patterns activate or deactivate based on `stack:`. Flutter-only patterns (`Color(0xFF...)`, `Colors.X`) skip when `stack: nextjs-tailwind`; new TSX/Tailwind patterns (`text-[#...]`, `bg-[rgb(...)]`, hardcoded hex in `style={}`) activate.
- **No regression for Fitio.** Flutter-default users see identical output before/after.

## 3. Non-goals

- **Not** shipping React Native, Vue, Svelte, SwiftUI, or plain-React adapters in v1.2. The contract is designed to support them; concrete adapters land in v1.3+ when there's a real consumer (one PR per stack, ~1 day each).
- **Not** migrating `theme-create`, `theme-motion`, `theme-bolder`, `theme-quieter`, `theme-distill` to adapter pattern. They still work — Flutter-coupled — until v1.3 phase-2.
- **Not** running multi-stack output simultaneously (one Plan emits both Dart and TSX). Possible in v1.4+ once 2 adapters exist.
- **Not** building wireframe-sketch (was bundled in original `adapter-and-wireframe`). Split out to `.specs/features/wireframe-sketch/` as v1.5+ candidate. Reason: wireframe-sketch is orthogonal to stack support and the user has urgency on adapter only.
- **Not** breaking the existing CLI surface. `/theme-port` still works for Fitio without any config change. `stack:` defaults to `flutter`.
- **Not** building a registry / plugin marketplace for adapters. They live in-repo in v1.2; community-contributed adapters are a v1.5+ design exercise.
- **Not** creating a separate `web-design-workflow` repo (originally suggested in ROADMAP §Out of scope). The adapter pattern keeps everything in one repo without diluting brand or aesthetic.

## 4. Requirements

### REQ-A — Adapter contract definition

- **REQ-A.1** Write `docs/adapter-protocol.md` documenting:
  - The intermediate format (an Adapter Plan) — token roles, widget tree shape, motion intent, file outputs
  - The adapter interface — input (Adapter Plan + project context) → output (file writes)
  - The conformance test suite (one Plan, all adapters must produce equivalent visual results in their idiom)
  - "How to add a new adapter" guide — what files to create, how to wire conformance tests
- **REQ-A.2** Define the Plan as a typed JSON Schema in `docs/adapter-plan.schema.json`. Three top-level branches: `tokens` (palette / typography / spacing / radius / motion), `widgets` (structural tree from theme-port), `actions` (file writes the adapter performs).
- **REQ-A.3** Document at least 3 example Plans in `docs/adapter-examples/` (`palette.json`, `widget-tree.json`, `motion-set.json`) — these are the test fixtures used by both adapters.

### REQ-B — Flutter adapter (reference, byte-equivalent)

- **REQ-B.1** `adapters/flutter/` directory with:
  - `adapter.py` — main entry: `python3 adapters/flutter/adapter.py <plan.json>` reads Plan, emits Flutter files matching current behavior of `theme-port` / `theme-extend`.
  - `templates/` — Dart string templates per output type (`app_colors.dart.tmpl`, `widget.dart.tmpl`, `design_tokens.md.tmpl`).
  - `mappings.py` — token role → Dart accessor (`brandDefault` → `context.colors.brandDefault`), widget element → component (`<button>` → `AppButton`).
- **REQ-B.2** Conformance test: feed each `docs/adapter-examples/*.json` through `adapters/flutter/adapter.py`; output must match a known-good golden file in `adapters/flutter/tests/golden/`.
- **REQ-B.3** Adapter is selected via `stack: flutter` in `.design-workflow.yaml`, `STACK=flutter` env var, or default (no config). Unknown stack → error with explicit message listing available adapters.

### REQ-C — Next.js + Tailwind adapter

- **REQ-C.1** `adapters/nextjs-tailwind/` directory with parallel structure to Flutter adapter:
  - `adapter.py` — same entry shape, emits TSX + CSS + Tailwind config.
  - `templates/` — `tokens.css.tmpl` (CSS custom properties), `tailwind.config.ts.tmpl` (theme.extend snippet), `component.tsx.tmpl` (functional component with shadcn/ui primitives + Tailwind classes), `design_tokens.md.tmpl`.
  - `mappings.py` — token role → CSS variable name (`brandDefault` → `--brand-default`); widget element → JSX/shadcn (`<button>` → `<Button>` from `@/components/ui/button` if shadcn available, else `<button className="...">`); spacing scale → Tailwind class (`spacing.4` → `p-4`).
- **REQ-C.2** Path conventions for Next.js App Router: tokens land in `app/globals.css` (or `styles/tokens.css` if user has classic Pages Router), components land in `components/<feature>/<name>.tsx`. Configurable via `.design-workflow.yaml` `paths:` section.
- **REQ-C.3** Conformance test: same 3 example Plans from REQ-A.3, output Next.js/Tailwind goldens in `adapters/nextjs-tailwind/tests/golden/`. Different files (e.g., `palette.css` instead of `palette.dart`), same semantic equivalence.
- **REQ-C.4** Detect shadcn/ui presence via `package.json` `dependencies.@radix-ui/*` or `components.json` file. If present, prefer shadcn primitives; if absent, emit plain `<button>` with Tailwind utility classes.

### REQ-D — Migrate `theme-port` to adapter pattern

- **REQ-D.1** `theme-port` SKILL.md body refactored: extract "emit Dart widget" logic into "emit Adapter Plan", then dispatch to active adapter via `Bash`. Single source-of-truth for structural extraction; emission is adapter's job.
- **REQ-D.2** Functional outcome unchanged for `stack: flutter`: a Figma frame port produces the same Dart files at the same paths as v1.1.2.
- **REQ-D.3** With `stack: nextjs-tailwind`, the same Figma frame produces TSX + CSS at Next.js conventions.
- **REQ-D.4** New internal step "Step 7.5 — Render via adapter" in the workflow.
- **REQ-D.5** Eval (`theme-port/evals/evals.json`) gets one new assertion: "Adapter Plan was emitted" (regex-detect a JSON file in stdout or sidecar).

### REQ-E — Migrate `theme-extend` to adapter pattern

- **REQ-E.1** Same shape as REQ-D — `theme-extend` emits a Plan describing token additions; adapter renders to whichever target (Dart `app_colors.dart` + `docs/design-tokens.md` for Flutter; CSS variables + Tailwind config + `docs/design-tokens.md` for Next.js).
- **REQ-E.2** Behavior byte-equivalent for Fitio (Flutter stack default).

### REQ-F — Stack-aware `theme-audit`

- **REQ-F.1** `theme-audit` reads `stack:` from config and activates the relevant lint pattern set:
  - **Flutter:** `Color(0xFF...)`, `Colors\.[a-z]+`, literal `fontSize:`, hardcoded paddings.
  - **Next.js+Tailwind:** `text-\[#[0-9a-f]+\]`, `bg-\[rgb`, hex literals in `style={}`, `tailwind.config.ts` colors not from CSS variables.
- **REQ-F.2** Audit script (`scripts/audit_theme.py`) accepts `--stack <flutter|nextjs-tailwind>` flag; SKILL.md picks based on resolved stack.
- **REQ-F.3** WCAG contrast logic stays identical (color comparison is stack-agnostic).

### REQ-G — Config + ROADMAP + docs

- **REQ-G.1** `config.example.yaml` adds `stack: flutter` (commented as "default; override per-project"). Documents valid values.
- **REQ-G.2** README gains top-level `## Stack support` section listing supported stacks + how to add one.
- **REQ-G.3** `docs/ROADMAP.md` reverses the "Out of scope: Web-first design" note (with date marker), and lists concrete v1.3+ additive adapters as backlog items (React Native, Vue+Tailwind, Svelte+Tailwind, SwiftUI).
- **REQ-G.4** README §What changed in v1.2.0 documents the adapter system + Next.js/Tailwind support.

### REQ-H — STATE.md decisions

- **REQ-H.1** D-14 — Adapter contract: stack-agnostic intermediate format (Adapter Plan), 2 reference adapters (Flutter + Next.js/Tailwind), byte-equivalent Flutter migration, other stacks deferred to v1.3+.
- **REQ-H.2** D-15 — Reverse "Web out of scope" ROADMAP entry; adapter pattern enables it cleanly.
- **REQ-H.3** D-16 — Roadmap reorder: adapter pulled forward 2 versions; inspiration-library v1.2→v1.3, interactive-mockup-stage v1.3→v1.4. Reason: user urgency on Next.js stack, weak dependency between specs.

### REQ-I — Validate + bump

- **REQ-I.1** `quick_validate.py` 19/19 valid (no new skills in v1.2, only refactors).
- **REQ-I.2** Conformance test passes: 3 example Plans through both adapters match their respective goldens. `python3 adapters/flutter/tests/conformance.py` → `PASS: 3/3`. `python3 adapters/nextjs-tailwind/tests/conformance.py` → `PASS: 3/3`.
- **REQ-I.3** Regression smoke: invoke `theme-port` on a real Fitio frame with `stack: flutter`; verify Dart output matches pre-v1.2 byte-for-byte (modulo formatting whitespace).
- **REQ-I.4** Smoke for Next.js: invoke `theme-port` with `stack: nextjs-tailwind` on the same frame; verify TSX/CSS output renders correctly (manual review, screenshot logged).
- **REQ-I.5** `marketplace.json` bumped 1.1.2 → 1.2.0.

## 5. Out of scope (deferred)

- **`wireframe-sketch` skill** — moved to `.specs/features/wireframe-sketch/` as v1.5+ candidate.
- **`theme-create`, `theme-motion`, `theme-bolder`, `theme-quieter`, `theme-distill` migrations to adapter** — v1.3 candidate (`adapter-migration-phase-2`).
- **React Native, Vue+Tailwind, Svelte+Tailwind, SwiftUI, plain-React adapters** — additive, one-PR-each follow-up. Listed in ROADMAP for v1.3+.
- **Multi-stack output simultaneously** (a Plan emits both Dart and TSX). v1.4+ once 2 adapters proven.
- **Adapter discovery via plugin marketplace.** Adapters live in-repo in v1.2; registry mechanism is its own design.
- **shadcn/ui auto-install** — if the user's Next.js project doesn't have shadcn, we emit plain Tailwind; we don't auto-run `npx shadcn add`.
- **Co-locate craft/anti-ai-slop with adapter checks** (linter). Currently craft is reference-only; making it executable is separate.

## 6. Source pin

- Upstream repo (for any forks): `nexu-io/open-design`
- Upstream branch: `main`
- Upstream SHA at fork time: **TBD — capture during T-00**
- Upstream license: Apache-2.0
- shadcn/ui reference: https://ui.shadcn.com/ (MIT) — used as a target convention, not bundled.

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Adapter Plan format insufficient for both Flutter widget tree AND JSX (different paradigms) — bikeshed delays release | High | T-01 reviews 5 real cases per stack (palette + 2 widget patterns + motion + responsive layout) before locking schema. Escape hatch: ship Plan with tokens-only first, defer widgets/actions to v1.3 (still meaningful release with Next.js token sync). |
| Flutter migration breaks Fitio in subtle way (wrong path, wrong import) | Medium | T-13 runs regression smoke comparing pre-v1.2 output byte-for-byte; only commits when match. |
| Next.js adapter shadcn detection unreliable | Medium | Two-mode emission: shadcn-aware (preferred when detected) and plain-Tailwind (fallback). Both tested via conformance goldens. |
| 14h estimate optimistic given 2-adapter scope | Medium | Spec defers 4 skill migrations to v1.3. If T-01 design exceeds 4h, bail to "tokens-only Plan, widgets deferred". |
| `stack:` config breaks existing `.design-workflow.yaml` users | Low | Default to `flutter` if missing; only error on explicit unknown value. |
| User reports Next.js adapter doesn't match their project's conventions | Medium | `paths:` section in config lets user override. Emit a `STACK_NOTES.md` per-stack documenting assumed conventions. |

## 8. Acceptance criteria

- [ ] REQ-A..REQ-I all verified
- [ ] Adapter contract documented with 3 example Plans
- [ ] Flutter adapter passes conformance on 3 example Plans (byte-equivalent goldens)
- [ ] Next.js+Tailwind adapter passes conformance on 3 example Plans (semantic-equivalent goldens)
- [ ] `theme-port` and `theme-extend` migrated; Flutter regression smoke matches pre-v1.2
- [ ] `theme-port` produces working TSX/CSS for `stack: nextjs-tailwind` on a real frame (manual smoke logged)
- [ ] `theme-audit` activates correct lint set per stack
- [ ] STATE.md has D-14, D-15, D-16
- [ ] ROADMAP.md updated (Tailwind no longer out-of-scope)
- [ ] All 19 skills pass `quick_validate.py`
- [ ] Single commit: `feat(release): v1.2.0 — multi-stack adapter (Flutter + Next.js/Tailwind)`
