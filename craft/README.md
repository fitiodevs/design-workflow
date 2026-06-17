# craft/

Universal design-system rules — encoded as project-agnostic prose, forked verbatim from [`nexu-io/open-design`](https://github.com/nexu-io/open-design) (Apache-2.0, originally derived from [`refero_skill`](https://github.com/referodesign/refero_skill), MIT). These docs sit upstream from any project's `docs/product.md` or `AppColors`; project tokens override only when they explicitly contradict. Sync is manual on demand — see each file's header for source SHA and `.specs/features/craft-adoption/` for the adoption record.

## Files

- **`anti-ai-slop.md`** — cardinal sins to avoid (purple gradients, glassmorphism reflex, emoji-as-icon, etc.).
- **`color.md`** — palette structure, accent discipline, semantic-vs-brand separation.
- **`state-coverage.md`** — required states (default, hover, focus, active, disabled, loading, empty, error) for every interactive surface.
- **`typography.md`** — type scale, line height, letter spacing, weight pairing rules.
- **`animation-discipline.md`** — when motion earns its frame and when it's noise.
- **`design-context.md`** — 5-tier context hierarchy and the "STOP if no Tier 1-4" refusal rule (authored from scratch v1.2.1, idea inspired by [huashu-design](https://github.com/alchaincyf/huashu-design)).

### Authored docs adapted from [`wondelai/skills`](https://github.com/wondelai/skills) (MIT)

These are **not** synced from open-design — they are authored in this repo, distilling frameworks from the `wondelai/skills` collection and re-tuned for a tokens-first, hybrid-mobile workflow. Editing them is safe; no upstream sync overwrites them. Each carries its own MIT attribution header.

- **`visual-hierarchy.md`** — grayscale-first method, the weight/size/color hierarchy levers, spacing & elevation systematics, squint/blur diagnostic, symptom→cause→fix table (from `refactoring-ui`).
- **`microinteractions.md`** — Saffer's Trigger→Rules→Feedback→Loops/Modes anatomy of a single interaction; companion to `animation-discipline.md` (from `microinteractions`).
- **`usability-heuristics.md`** — Krug's three scanning laws + severity scale + dark-patterns taxonomy. Deliberately does *not* restate Nielsen 10 (Olavo owns that) (from `ux-heuristics`).
- **`platform-conventions.md`** — hybrid iOS+Android platform idioms (touch targets, safe areas, tab-bar-not-hamburger, native gestures, dynamic type, dark mode, haptics, VoiceOver+TalkBack), best-practices only (from `ios-hig-design`).

## Which skills load which docs

| Doc | Loaded by |
|---|---|
| `anti-ai-slop.md` | `theme-critique`, `theme-create`, `theme-bolder`, `frontend-design` |
| `color.md` | `theme-critique`, `theme-create`, `theme-bolder`, `frontend-design` |
| `state-coverage.md` | `theme-critique`, `theme-port`, `frontend-design` |
| `typography.md` | `theme-critique`, `theme-create`, `theme-port`, `frontend-design` |
| `animation-discipline.md` | `frontend-design`, `theme-motion` |
| `design-context.md` | `theme-critique`, `theme-create`, `theme-extend`, `theme-port`, `frontend-design` |
| `visual-hierarchy.md` | `theme-critique`, `theme-bolder`, `frontend-design` |
| `microinteractions.md` | `theme-motion`, `frontend-design` |
| `usability-heuristics.md` | `theme-critique`, `flow` |
| `platform-conventions.md` | `theme-critique`, `theme-port`, `frontend-design`, `flow` |

The wiring is declared per-skill via the `dw.craft.requires:` field — see [`docs/skill-extensions.md`](../docs/skill-extensions.md) for the namespace spec. Each wired skill carries a "Craft references" section in its body listing only the docs it declared.

## Updating

> Applies only to the open-design-synced docs (everything above the "adapted from `wondelai/skills`" subsection). The wondelai-adapted docs are authored here and have no upstream SHA — edit them directly.

To re-sync a doc to a newer upstream SHA:

1. `gh api repos/nexu-io/open-design/contents/craft/<name>.md --jq '.content' | base64 -d > /tmp/upstream.md`
2. Replace the body of `craft/<name>.md` (keep header, update `Last sync` line + SHA).
3. Skim diff for breaking-rule changes; if a rule flips, audit the skills listed above.
