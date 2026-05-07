# craft/

Universal design-system rules — encoded as project-agnostic prose, forked verbatim from [`nexu-io/open-design`](https://github.com/nexu-io/open-design) (Apache-2.0, originally derived from [`refero_skill`](https://github.com/referodesign/refero_skill), MIT). These docs sit upstream from any project's `docs/product.md` or `AppColors`; project tokens override only when they explicitly contradict. Sync is manual on demand — see each file's header for source SHA and `.specs/features/craft-adoption/` for the adoption record.

## Files

- **`anti-ai-slop.md`** — cardinal sins to avoid (purple gradients, glassmorphism reflex, emoji-as-icon, etc.).
- **`color.md`** — palette structure, accent discipline, semantic-vs-brand separation.
- **`state-coverage.md`** — required states (default, hover, focus, active, disabled, loading, empty, error) for every interactive surface.
- **`typography.md`** — type scale, line height, letter spacing, weight pairing rules.
- **`animation-discipline.md`** — when motion earns its frame and when it's noise.
- **`design-context.md`** — 5-tier context hierarchy and the "STOP if no Tier 1-4" refusal rule (authored from scratch v1.2.1, idea inspired by [huashu-design](https://github.com/alchaincyf/huashu-design)).

## Which skills load which docs

| Doc | Loaded by |
|---|---|
| `anti-ai-slop.md` | `theme-critique`, `theme-create`, `theme-bolder`, `frontend-design` |
| `color.md` | `theme-critique`, `theme-create`, `theme-bolder`, `frontend-design` |
| `state-coverage.md` | `theme-critique`, `theme-port`, `frontend-design` |
| `typography.md` | `theme-critique`, `theme-create`, `theme-port`, `frontend-design` |
| `animation-discipline.md` | `frontend-design` |
| `design-context.md` | `theme-critique`, `theme-create`, `theme-extend`, `theme-port`, `frontend-design` |

The wiring is declared per-skill via the `dw.craft.requires:` field — see [`docs/skill-extensions.md`](../docs/skill-extensions.md) for the namespace spec. Each wired skill carries a "Craft references" section in its body listing only the docs it declared.

## Updating

To re-sync a doc to a newer upstream SHA:

1. `gh api repos/nexu-io/open-design/contents/craft/<name>.md --jq '.content' | base64 -d > /tmp/upstream.md`
2. Replace the body of `craft/<name>.md` (keep header, update `Last sync` line + SHA).
3. Skim diff for breaking-rule changes; if a rule flips, audit the skills listed above.
