# Design: multi-stack-adapter

## Decisions

### D-A — One contract, two reference adapters in v1.2

Originally the spec planned Flutter adapter only as reference; other stacks were "v1.5+ when there's a real consumer." User urgency on Next.js+Tailwind makes that the second reference. **Two adapters in the first release** is also better engineering: it forces the contract to handle two paradigms (widget-tree imperative + JSX/utility-first), so the design isn't accidentally Flutter-shaped.

Trade-off: ~5 extra hours on the Next.js adapter. Worth it — one paradigm can hide assumptions; two cannot.

### D-B — Adapter Plan as JSON-serialisable Python dict, not class hierarchy

The Plan is data, not behavior. JSON Schema validates shape. Adapters consume via `json.load`. No Python class plumbing means non-Python adapters (a TypeScript adapter for React Native, a Swift adapter for SwiftUI) can read the same Plan natively. Type-checking is via JSON Schema, not Python `mypy`. Acceptable.

### D-C — Adapter is a script, not a skill

Adapters live in `adapters/<stack>/adapter.py`, invoked by skills via `Bash`. They're not user-facing — user never types `/flutter-adapter`. Adapters are mechanical (deterministic templating); skills are LLM-driven (judgment calls). Mixing them in `skills/` confuses the surface area.

### D-D — Migration scope is theme-port + theme-extend in v1.2

Both already deal heavily with code emission (the Dart string templates are nontrivial). Migrating both proves the contract handles real complexity in two stacks. theme-create / theme-motion / theme-bolder / theme-quieter / theme-distill migrations are simpler in retrospect (less templating, more decision-making) — defer to v1.3 (`adapter-migration-phase-2`) where feedback from v1.2 informs the simplification.

Skills NOT migrated in v1.2 still work — they continue emitting Flutter directly. The contract doesn't force adoption; it offers a path.

### D-E — Conformance test = golden-file diff per adapter

For each example Plan in `docs/adapter-examples/`:
- Flutter adapter has a known-good output in `adapters/flutter/tests/golden/<name>.dart`.
- Next.js/Tailwind adapter has a known-good output in `adapters/nextjs-tailwind/tests/golden/<name>.{css,tsx,md}`.
- CI / regression check: each adapter runs its conformance script, diffs against own goldens. Zero diff = conforming.

Cross-stack equivalence is **semantic**, not byte-level — `palette.dart` and `palette.css` solve the same problem in their idiom.

### D-F — `stack:` config field, defaults to `flutter`, errors on unknown

Resolution order:
1. `STACK` environment variable (highest)
2. `.design-workflow.yaml` `stack:` field
3. Default: `flutter`

A user who never sets it gets current behavior. A user who sets `stack: react-native` in v1.2 gets:
```
Error: adapter 'react-native' not found. Available adapters: flutter, nextjs-tailwind.
See docs/adapter-protocol.md §"How to add a new adapter" if you'd like to contribute one.
```

### D-G — Next.js adapter detects shadcn/ui presence; falls back to plain Tailwind

If the user's project has `components.json` (shadcn config) or `@radix-ui/*` deps in `package.json`, emit shadcn primitives:
```tsx
import { Button } from "@/components/ui/button"
<Button variant="default" size="lg">Continuar</Button>
```

Else, emit plain Tailwind:
```tsx
<button className="bg-brand-default text-white px-6 py-3 rounded-lg font-medium">Continuar</button>
```

We do NOT auto-install shadcn. That's the user's choice. If they want shadcn, they `npx shadcn init` first; the adapter detects and adapts.

### D-H — Path conventions per stack

| Token type | Flutter | Next.js+Tailwind |
|---|---|---|
| Color tokens | `lib/core/theme/app_colors.dart` | `app/globals.css` (App Router) or `styles/tokens.css` (Pages Router) — auto-detected via presence of `app/` dir |
| Tailwind config update | n/a | `tailwind.config.ts` (theme.extend.colors) |
| Spacing/radius | `lib/core/theme/app_spacing.dart` | CSS vars in tokens file + Tailwind theme.extend |
| Typography | `lib/core/theme/text_theme.dart` | CSS vars + Tailwind fontFamily/fontSize/fontWeight |
| Widget files | `lib/features/<feature>/presentation/widgets/<name>.dart` | `components/<feature>/<name>.tsx` |
| Token docs | `docs/design-tokens.md` | `docs/design-tokens.md` (shared) |

Override via `.design-workflow.yaml` `paths:` block.

### D-I — Stack-aware audit reuses scan logic, swaps lint patterns

`scripts/audit_theme.py` keeps its WCAG contrast logic intact (color math is universal). The hardcode-detection regex set is loaded from `scripts/audit_lint_sets/<stack>.yaml` based on resolved stack. Adding a new stack = adding a new YAML file to the lint set dir. No code change.

## Architecture

```
<repo>/
├── adapters/                                  NEW
│   ├── flutter/
│   │   ├── adapter.py
│   │   ├── mappings.py                        # token role + widget mappings → Dart
│   │   ├── templates/
│   │   │   ├── app_colors.dart.tmpl
│   │   │   ├── widget.dart.tmpl
│   │   │   └── design_tokens.md.tmpl
│   │   ├── STACK_NOTES.md                     # assumed conventions, override hints
│   │   └── tests/
│   │       ├── conformance.py
│   │       └── golden/
│   │           ├── palette.dart
│   │           ├── widget-tree.dart
│   │           └── motion-set.dart
│   └── nextjs-tailwind/                       NEW
│       ├── adapter.py
│       ├── mappings.py                        # token role → CSS var; widget → JSX/shadcn
│       ├── templates/
│       │   ├── tokens.css.tmpl
│       │   ├── tailwind.config.ts.tmpl
│       │   ├── component.tsx.tmpl
│       │   ├── component-shadcn.tsx.tmpl      # variant when shadcn detected
│       │   └── design_tokens.md.tmpl
│       ├── STACK_NOTES.md
│       └── tests/
│           ├── conformance.py
│           └── golden/
│               ├── palette.css
│               ├── widget-tree.tsx
│               ├── widget-tree-shadcn.tsx
│               └── motion-set.css
├── docs/
│   ├── adapter-protocol.md                    # NEW: the contract
│   ├── adapter-plan.schema.json               # NEW: typed schema for Plans
│   └── adapter-examples/                      # NEW: 3 example Plans
│       ├── palette.json
│       ├── widget-tree.json
│       └── motion-set.json
├── scripts/
│   ├── audit_theme.py                         # MODIFIED: --stack flag, loads lint set per stack
│   └── audit_lint_sets/                       # NEW
│       ├── flutter.yaml
│       └── nextjs-tailwind.yaml
├── config.example.yaml                        # MODIFIED: add `stack: flutter` + `paths:` block
├── skills/
│   ├── theme-port/SKILL.md                    # MODIFIED: emit Plan, dispatch adapter
│   ├── theme-extend/SKILL.md                  # MODIFIED: same
│   └── theme-audit/SKILL.md                   # MODIFIED: pass --stack to script
├── README.md                                  # MODIFIED: ## Stack support + §What changed v1.2.0
├── docs/ROADMAP.md                            # MODIFIED: reverse Tailwind-out-of-scope, list v1.3+ adapters
├── .specs/project/STATE.md                    # MODIFIED: D-14, D-15, D-16
└── .claude-plugin/marketplace.json            # MODIFIED: bump 1.2.0
```

## Adapter Plan format (locked sketch)

```json
{
  "$schema": "https://design-workflow.dev/adapter-plan.schema.json",
  "version": "1.0",
  "kind": "palette" | "widget-tree" | "motion-set",
  "tokens": {
    "palette": {
      "brandDefault": {"light": "#c96442", "dark": "#d97757"},
      "bgBase":       {"light": "#f5f4ed", "dark": "#141413"}
    },
    "typography": {
      "displayLg":  {"fontFamily": "Geist", "size": 32, "weight": 600, "lineHeight": 1.2}
    },
    "spacing": {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 32},
    "radius":  {"sm": 4, "md": 8, "lg": 16, "xl": 24, "full": 9999},
    "motion": {
      "fast":   {"durationMs": 150, "curve": "easeOut"},
      "normal": {"durationMs": 250, "curve": "easeInOut"}
    }
  },
  "widgets": [
    {
      "type": "button",
      "variant": "primary",
      "size": "lg",
      "props": {"label": "Continuar"},
      "children": []
    }
  ],
  "actions": [
    {"op": "write", "role": "palette",      "intent": "tokens"},
    {"op": "write", "role": "widget-tree",  "intent": "component", "name": "MilestoneCta"},
    {"op": "append","role": "design-tokens","intent": "doc-summary"}
  ]
}
```

The adapter:
1. Reads `tokens` + `widgets` according to `kind`.
2. Renders via its templates.
3. Resolves `actions[].role + intent` to concrete file paths via `mappings.py` + project-detected paths (e.g., for Next.js, checks if `app/` exists to choose App Router vs Pages Router).

## Flutter adapter dispatch

```python
# adapters/flutter/adapter.py
import json, sys
from .mappings import resolve_path
from .templates import render

def main(plan_path, dry_run=False):
    plan = json.load(open(plan_path))
    rendered = render(plan)  # dict: action_index → file content
    for i, action in enumerate(plan["actions"]):
        path = resolve_path(action, plan)
        if dry_run:
            print(f"would write: {path} ({len(rendered[i])} bytes)")
        else:
            open(path, "w").write(rendered[i])
    return 0
```

## Next.js+Tailwind adapter dispatch

Same shape, different `mappings.py` + `templates/`:

```python
# adapters/nextjs-tailwind/adapter.py
import json, os
from .mappings import resolve_path, has_shadcn, app_router_or_pages
from .templates import render

def main(plan_path, dry_run=False):
    plan = json.load(open(plan_path))
    project = {
        "shadcn": has_shadcn(),                  # checks components.json + @radix-ui deps
        "router": app_router_or_pages(),         # checks for app/ vs pages/
    }
    rendered = render(plan, project)             # picks shadcn vs plain templates
    for i, action in enumerate(plan["actions"]):
        path = resolve_path(action, plan, project)
        if dry_run:
            print(f"would write: {path} ({len(rendered[i])} bytes)")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w").write(rendered[i])
    return 0
```

## Migration shape for theme-port

Before (Flutter-only):
```
Step 5 — Implement (write Dart files directly)
```

After (stack-agnostic):
```
Step 5  — Build Adapter Plan (write /tmp/<feature>-plan.json)
Step 6  — Resolve active stack (env STACK > config.stack > "flutter")
Step 7  — Render via adapter (Bash: python3 adapters/$STACK/adapter.py /tmp/<feature>-plan.json)
Step 7.5 — Verify outputs landed at expected paths
Step 8  — Validate per stack:
            • flutter: flutter analyze
            • nextjs-tailwind: tsc --noEmit + eslint
```

Skill body documents the new flow only; old flow is gone after v1.2 ships.

## Token role → emission examples

To prove the contract is paradigm-agnostic, here are 3 token roles rendered to both stacks:

| Role | Plan input | Flutter emission | Next.js+Tailwind emission |
|---|---|---|---|
| `brandDefault` | `{"light": "#c96442", "dark": "#d97757"}` | `Color(0xFFC96442)` in `AppColors._light`, `Color(0xFFD97757)` in `AppColors._dark` | `:root { --brand-default: #c96442 } .dark { --brand-default: #d97757 }` + `tailwind.config.ts: colors.brand.default = "var(--brand-default)"` |
| `displayLg` typography | `{"fontFamily": "Geist", "size": 32, "weight": 600}` | `TextStyle(fontFamily: "Geist", fontSize: 32, fontWeight: FontWeight.w600)` in `TextTheme.displayLarge` | CSS vars + Tailwind `fontSize: { display: ["32px", { lineHeight: "1.2", fontWeight: "600" }] }` |
| Button widget (primary, lg) | `{"type": "button", "variant": "primary", "size": "lg", "props": {"label": "Continuar"}}` | `AppButton.primary(label: "Continuar", size: AppButtonSize.lg)` | shadcn: `<Button variant="default" size="lg">Continuar</Button>`; plain: `<button className="bg-brand-default text-white px-6 py-3 rounded-lg font-medium">Continuar</button>` |

Same Plan, two faithful emissions.

## Validation strategy

```bash
# 1. quick_validate
VAL=...
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done   # 19/19 valid

# 2. Adapter conformance — both adapters
python3 adapters/flutter/tests/conformance.py            # PASS: 3/3 (byte-equivalent goldens)
python3 adapters/nextjs-tailwind/tests/conformance.py    # PASS: 3/3 (semantic-equivalent goldens)

# 3. Flutter regression smoke
# Pre-v1.2: snapshot a known frame port output (Fitio coupons milestone slider) → /tmp/pre-v1.2-snapshot/
# Post-v1.2: theme-port same input with stack=flutter → byte-compare against snapshot

# 4. Next.js manual smoke
# Spin up a fresh Next.js + Tailwind project, set stack: nextjs-tailwind in config
# /theme-port the same Figma frame
# Confirm: app/globals.css has CSS vars, tailwind.config.ts has theme.extend, components/<feature>/<name>.tsx renders the structure
# Visual screenshot logged in .design-spec/smoke/v1.2.0-nextjs-port.md

# 5. Stack-aware audit smoke
# Run /theme-audit on the same Next.js project → confirm no false positives from Flutter patterns
```

## Rollback

`git tag pre-v1.2.0` before T-00.

## Estimate

- Adapter contract design + schema + 3 examples: 3.5h
- Flutter adapter implementation + templates + golden tests: 3h
- Next.js+Tailwind adapter implementation + templates + golden tests + shadcn detection: 4h
- theme-port migration + Flutter regression smoke + Next.js manual smoke: 2h
- theme-extend migration: 1h
- theme-audit stack-awareness + lint set YAMLs: 1h
- Pipeline docs + STATE + ROADMAP + version + final commit: 1.5h
- **Total: ~16h** (matches Large sizing; defer-to-tokens-only escape hatch on REQ-A keeps it bounded)

## Out-of-scope discipline

This release MUST NOT scope-creep into:
- Migrating other 5 wired skills (defer to `adapter-migration-phase-2`).
- Adding a 3rd adapter (React, RN, etc.) "while we're at it".
- Building a wireframe-sketch skill (split out, separate spec).
- Refactoring `craft/` references (out-of-band).

If T-01 (contract design) takes more than 4h, halt and trim — ship tokens-only first, defer widgets/actions to v1.3 with the Next.js adapter still landing as token sync. Still useful release.
