# Next.js + Tailwind adapter — stack notes

> Reference adapter for v1.2.0 — Next.js (App Router preferred, Pages fallback) + Tailwind CSS, with optional shadcn/ui detection.

## Assumed conventions

| Concern | Default path (App Router) | Default path (Pages) |
|---|---|---|
| Color tokens (CSS vars) | `app/globals.css` | `styles/tokens.css` |
| Tailwind config | `tailwind.config.ts` | `tailwind.config.ts` |
| Widget files | `components/<feature>/<name>.tsx` | `components/<feature>/<name>.tsx` |
| Motion tokens | `app/globals.css` (CSS vars + keyframes) | `styles/tokens.css` |
| Token docs | `docs/design-tokens.md` | `docs/design-tokens.md` |

Override via `.design-workflow.yaml`:

```yaml
paths:
  nextjs_tailwind:
    tokens_css: app/globals.css
    tailwind_config: tailwind.config.ts
    components_root: components
```

## Detection

`has_shadcn()` — true when **either**:
- `components.json` exists at project root, **or**
- `package.json` has any `@radix-ui/*` in `dependencies`/`devDependencies`.

`app_router_or_pages()` — `"app"` if `app/` directory exists, else `"pages"`.

In dry-run / pure-render mode (no project context), both default to false / `"app"`.

## Token role → CSS variable

29 canonical roles map to kebab-case CSS variables (`brandDefault` → `--brand-default`). The adapter emits a `:root { ... }` block for `light` and a `.dark { ... }` block for `dark`. Tailwind theme.extend.colors then references each var via `colors.brand.default = "var(--brand-default)"`.

## Widget type → JSX

When `has_shadcn=true`, button/input/select/checkbox/switch use shadcn primitives:
```tsx
import { Button } from "@/components/ui/button";
<Button variant="default" size="lg">Continuar</Button>
```

When `has_shadcn=false`, plain Tailwind utility classes:
```tsx
<button className="bg-brand-default text-white px-6 py-3 rounded-lg font-medium">Continuar</button>
```

## Limitations (v1.2.0)

- shadcn variant mapping is best-effort — the adapter assumes `Button`, `Input`, `Select` exist if shadcn detected; doesn't run `npx shadcn add`.
- Motion emits CSS custom properties only; no `tailwindcss-animate` integration (planned v1.3).
- Tailwind config patch is additive (theme.extend.colors); doesn't merge with existing user keys — emits a snippet for the developer to integrate.
