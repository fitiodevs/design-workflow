# Roadmap

Tracking iterations for `design-workflow`. Items are not promises — they
record intent and priority. PRs welcome on any of them.

## v0.1.0 — shipped

- 13 skills extracted from Fitio production app
- 4 Python scripts (OKLCH, WCAG, audit, palette gen)
- Bilingual persona docs (EN canonical + PT aliases)
- Flutter-first config (`config.example.yaml`)
- Apache 2.0 license

## v0.2 — Genericization pass

Status: **planned** · target: when first external user files an issue.

- [ ] Replace `Fitio`-branded copy in skill `description:` fields with project-agnostic language. Preserve persona names (Lupa/Compositor/etc — they are brand).
- [ ] Replace hardcoded paths in skill body (`docs/product.md`, `lib/core/theme/...`) with config-resolved placeholders or env vars.
- [ ] Strip references to Fitio-specific user personas (Diego/Marina/Léo). Move to `examples/` as illustrative.
- [ ] Strip references to `BackendConfig.current`, `Supabase`, and other Fitio-stack assumptions in body text.
- [ ] Add a `STACK_HINTS.md` doc enumerating which lines of each skill are stack-coupled, to prepare for v0.3 adapters.

## v0.3 — Adapter system

Status: **planned** · effort: large.

Skills today emit Dart hardcoded. To support React Native, SwiftUI, web, etc.:

- [ ] Define `adapters/` folder with one adapter per stack (`flutter.yaml`, `react-native.yaml`, `web.yaml`).
- [ ] Each adapter declares: token file format, widget naming, motion API, contrast helper.
- [ ] Skills read adapter at invocation, route output through it.
- [ ] Migrate `theme-port`, `theme-extend`, `theme-motion`, `theme-bolder`, `theme-quieter`, `theme-distill` to adapter-based output.
- [ ] Keep current Flutter behaviour as the default adapter.

## v0.4 — CI + tooling

Status: **planned** · effort: medium.

- [ ] GitHub Actions: lint markdown frontmatter (every `SKILL.md` has `name`, `description`, `license`).
- [ ] Dry-run `install.sh` in CI to catch path bugs.
- [ ] Snapshot test for `marketplace.json` schema.
- [ ] `release-please` or similar for changelog automation.

## v0.5 — Examples

Status: **planned** · effort: small.

- [ ] `examples/flutter-empty/` — minimal Flutter starter showing how to plug in tokens, run `/theme-create`, `/theme-port`.
- [ ] `examples/anonymized-app/` — fully sanitized Fitio-like app with 3 screens to demonstrate the pipeline end-to-end.
- [ ] Screencast / GIF of `/theme-critique` running against an example screen.

## v0.6 — Persona overrides

Status: **deferred** · effort: medium.

- [ ] Honor `personas:` overrides from `.design-workflow.yaml`:
  - disable any persona
  - override voice/tone
  - inject project-specific persona names
- [ ] Document override examples.

## Recurring sweep — quarterly

Status: **idea** · `/schedule` candidate.

Every 3 months a background agent should:

- [ ] Open the repo's issues and triage stale ones.
- [ ] Sweep the skills for reference rot (slash commands, doc paths that moved).
- [ ] Propose 1 generification PR per skill (5–10 min each).
- [ ] Compare against latest Anthropic skill template for drift.

When this repo has a remote and a few external users, set this up via `/schedule` with cadence "every 3 months".

## Out of scope

- Web-first design (Tailwind, MUI). Different aesthetic vocabulary; would require a separate `web-design-workflow` repo.
- Generic Material Design 3 helpers. M3 has its own opinions; we prefer to override them with brand-committed tokens.
- A/B testing copy generation. Out of `ux-writing`'s scope.
- Auto-generation of mockups from product requirements (vs from existing screens). Different problem.
