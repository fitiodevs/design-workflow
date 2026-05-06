# Adapter protocol

How `design-workflow` skills emit code without knowing the target stack — and how to plug in a new stack with one PR.

> **Status:** v1.2.0 contract. Stable; additive changes welcome (new token roles, new widget types). Breaking changes require a major version bump.

---

## 1. Why a contract

Skills like `theme-port`, `theme-extend`, `theme-create`, and `theme-motion` make **judgment calls** (which token role does this color play? what state coverage does this widget need? does this screen deserve motion?) and **emit code** (Dart `Color(0xFF...)`, CSS `--brand-default`, TSX `<Button>`).

The judgment calls are universal — the same anti-AI-slop rule, the same WCAG threshold, the same "every interactive surface needs 8 states" — across Flutter, Next.js, SwiftUI, anything else. The emission is stack-coupled.

Without a boundary, every new stack means rewriting every skill's emission code. With `n` skills × `m` stacks, that's `n × m` divergent codebases.

The adapter contract puts the boundary at the right place:

```
            [skill — judgment]
                   │ emits
                   ▼
            [Adapter Plan — JSON, stack-neutral]
                   │ rendered by
                   ▼
            [adapter — mechanical, per stack]
                   │ writes
                   ▼
            [code — Dart / TSX / Swift / ...]
```

A skill emits one Plan. Each adapter renders that Plan into its stack's idiom. Adding a new stack = adding one adapter, no skill changes. Cost is `n + m`, not `n × m`.

This document is the contract. The Plan format is locked at v1.0 — all v1.2.x adapters and skills depend on it. Additive evolution (new token roles, new action ops) is fine; renames or removals require a `version: "2.0"` Plan and a major release.

---

## 2. Plan format

A Plan is a JSON document. It captures **what** the skill decided, never **how** to render. Adapters read the Plan and render to their target.

### Top-level shape

```json
{
  "$schema": "https://design-workflow.dev/adapter-plan.schema.json",
  "version": "1.0",
  "kind": "palette" | "widget-tree" | "motion-set",
  "tokens": { ... },
  "widgets": [ ... ],
  "actions": [ ... ]
}
```

| Field | Required | Purpose |
|---|---|---|
| `$schema` | Recommended | Points at the JSON Schema for editor support. |
| `version` | Yes | Plan format version. v1.2.0 emits `"1.0"`. Adapters reject unknown versions. |
| `kind` | Yes | What this Plan describes. Drives which adapter branch executes. |
| `tokens` | Yes for `palette`/`motion-set`, optional for `widget-tree` | Design tokens by role. |
| `widgets` | Yes for `widget-tree`, absent otherwise | Structural tree from theme-port. |
| `actions` | Yes | File operations the adapter performs. |

### `tokens` branches

```json
{
  "tokens": {
    "palette": {
      "<role>": {"light": "#hex", "dark": "#hex"}
    },
    "typography": {
      "<role>": {"fontFamily": "Geist", "size": 32, "weight": 600, "lineHeight": 1.2, "letterSpacing": 0}
    },
    "spacing": {"<role>": <number-px>},
    "radius":  {"<role>": <number-px>},
    "motion": {
      "<role>": {"durationMs": 250, "curve": "easeInOut"}
    }
  }
}
```

Token **roles** are semantic, not visual:
- `brandDefault`, `bgBase`, `feedbackPositive`, `borderDefault`, etc. — never `redLighter12` or `c4`.
- The role names are stable; new roles are additive.

### `widgets` array

Recursive structural tree. Each node:

```json
{
  "type": "button" | "text" | "container" | "form-group" | "image" | "icon" | "input" | ...,
  "variant": "primary" | "secondary" | ...,   // optional, type-specific
  "size":    "sm" | "md" | "lg" | "xl",       // optional
  "props":   { /* type-specific data: label, src, placeholder, ... */ },
  "children": [ /* nested widget nodes */ ]
}
```

Widget `type` enum is intentionally small and idiom-agnostic. The adapter resolves to its native primitive (`AppButton` in Flutter, `<Button>` in shadcn, etc.).

### `actions` array

Operations the adapter performs after rendering. Adapters resolve concrete paths from `role + intent + project context`.

```json
{
  "op": "write" | "append" | "patch",
  "role": "palette" | "widget-tree" | "design-tokens" | "motion" | ...,
  "intent": "tokens" | "component" | "config" | "doc-summary",
  "name": "MilestoneCta"   // optional, used for `intent: component`
}
```

The skill says "write the palette tokens" — the adapter decides whether that means `lib/core/theme/app_colors.dart` (Flutter), `app/globals.css` + `tailwind.config.ts` (Next.js+Tailwind), or `Resources/Assets.xcassets/Colors.xcassets` (SwiftUI).

### Full example: palette Plan

See `docs/adapter-examples/palette.json`.

```json
{
  "$schema": "https://design-workflow.dev/adapter-plan.schema.json",
  "version": "1.0",
  "kind": "palette",
  "tokens": {
    "palette": {
      "brandDefault": {"light": "#c96442", "dark": "#d97757"},
      "bgBase":       {"light": "#f5f4ed", "dark": "#141413"}
    }
  },
  "actions": [
    {"op": "write",  "role": "palette",        "intent": "tokens"},
    {"op": "append", "role": "design-tokens",  "intent": "doc-summary"}
  ]
}
```

---

## 3. Adapter interface

An adapter is a Python script with a single entry contract. The script lives at `adapters/<stack>/adapter.py`.

### Signature

```bash
python3 adapters/<stack>/adapter.py <plan.json> [--dry-run]
```

| Input | Type | Source |
|---|---|---|
| `<plan.json>` | filesystem path | written by the calling skill, usually `/tmp/<feature>-plan.json` |
| `--dry-run` (optional flag) | boolean | when present, adapter prints what it would write without modifying disk |

| Output | Type | Where |
|---|---|---|
| File writes per `actions[]` | filesystem effects | resolved per-stack paths |
| `stdout` | structured log | one line per write: `wrote: <path> (<bytes> bytes)` |
| `stderr` | error messages | non-empty only on failure |
| Exit code | integer | `0` success, non-zero failure |

### Required helpers

Each adapter exposes at minimum:

```python
# adapters/<stack>/adapter.py
def main(plan_path: str, dry_run: bool = False) -> int: ...

# adapters/<stack>/mappings.py
TOKEN_ROLE_MAP: dict[str, str]    # role → stack-specific accessor
WIDGET_TYPE_MAP: dict[str, str]   # widget type → stack primitive

def resolve_path(action: dict, plan: dict, project: dict | None = None) -> str: ...
```

### Project-context detection

Adapters MAY inspect the user's project to adapt output:

- Flutter: detect Material vs Cupertino theme usage; check `pubspec.yaml` for `flutter_animate` presence.
- Next.js+Tailwind: detect App Router vs Pages Router (`app/` exists?), shadcn/ui presence (`components.json` or `@radix-ui/*` deps).
- SwiftUI: detect minimum iOS deployment target.

Project-context detection lives in `mappings.py`. Skills don't pass project context; the adapter discovers it from the cwd at invocation time.

### Error contract

Adapter failures fall into three buckets:

| Bucket | When | Exit code | Behavior |
|---|---|---|---|
| Schema violation | Plan doesn't match `adapter-plan.schema.json` | 1 | Print path + JSON pointer to first violation; exit. |
| Unknown role/type | Plan uses `tokens.palette.foo` and adapter has no `foo` mapping | 2 | Print the unknown identifier + suggest closest match (Levenshtein distance ≤ 2). |
| IO error | Can't write to resolved path (permissions, missing parent dir) | 3 | Print path + OS error; exit. |

Adapters MUST be deterministic: same input Plan + same project context → byte-identical output across runs.

---

## 4. Conformance test

Every adapter ships a conformance test that proves it renders the canonical example Plans correctly.

### Goldens

For each example Plan in `docs/adapter-examples/<name>.json`, the adapter has a known-good output in `adapters/<stack>/tests/golden/<name>.<ext>`. The extension is stack-specific (`.dart`, `.css`, `.tsx`, `.swift`).

### Test script

```python
# adapters/<stack>/tests/conformance.py
import subprocess, json, sys
from pathlib import Path

EXAMPLES = ["palette", "widget-tree", "motion-set"]

passed = 0
for name in EXAMPLES:
    plan = f"docs/adapter-examples/{name}.json"
    golden_dir = Path(f"adapters/{STACK}/tests/golden/{name}/")
    output = subprocess.run(
        ["python3", f"adapters/{STACK}/adapter.py", plan, "--dry-run"],
        capture_output=True, text=True
    )
    if compare_output_to_goldens(output.stdout, golden_dir):
        passed += 1
        print(f"  PASS: {name}")
    else:
        print(f"  FAIL: {name}")

print(f"PASS: {passed}/{len(EXAMPLES)}")
sys.exit(0 if passed == len(EXAMPLES) else 1)
```

### Cross-stack equivalence

Adapters do NOT produce identical output to each other — they produce **semantically equivalent** output in their stack's idiom. The Flutter adapter's `palette.dart` and the Next.js adapter's `palette.css` solve the same problem; they're not byte-comparable.

Each adapter has its own goldens. Cross-stack comparisons are conceptual (same Plan should yield equivalent visual rendering), not automated.

### When goldens change

Goldens update when:
- The adapter intentionally changes its emission style (e.g., Flutter adapter switches from `Color(0xFF...)` to `Color.fromRGBO(...)`).
- The Plan format adds a new field that affects rendering (additive evolution).

Goldens MUST NOT update silently. A golden change without a Plan version bump or adapter changelog entry is a regression to investigate.

---

## 5. How to add a new adapter

To add support for a stack `mystack` (example: `react-native`, `vue-tailwind`, `swiftui`):

### Step 1 — Scaffold

```bash
mkdir -p adapters/mystack/{templates,tests/golden}
touch adapters/mystack/{adapter.py,mappings.py,STACK_NOTES.md}
touch adapters/mystack/tests/conformance.py
```

### Step 2 — Write `mappings.py`

```python
# adapters/mystack/mappings.py
TOKEN_ROLE_MAP = {
    "brandDefault": "<accessor in mystack idiom>",
    # ... 28 more role mappings
}

WIDGET_TYPE_MAP = {
    "button": "<button primitive in mystack>",
    # ... etc
}

def resolve_path(action, plan, project=None):
    # Map (op, role, intent) + project context → concrete path
    ...
```

The 29 canonical token roles are listed in `docs/adapter-examples/palette.json`. Cover all 29; mark any you can't map yet with a `# TODO(unsupported)` comment so the conformance test surfaces gaps.

### Step 3 — Write templates

Per output type the stack supports:
- `tokens.<ext>.tmpl` — palette + spacing + radius + typography + motion as native code/config.
- `component.<ext>.tmpl` — a single widget tree rendered.
- `design_tokens.md.tmpl` — human-readable summary (shared format across stacks).

Templates use Python `string.Template` (`$role`, `$value`) or f-strings — pick one and document in the file header.

### Step 4 — Implement `adapter.py`

```python
import json, os, sys
from .mappings import resolve_path, TOKEN_ROLE_MAP
from .templates import render

def main(plan_path, dry_run=False):
    plan = json.load(open(plan_path))
    project = detect_project()  # adapter-specific
    rendered = render(plan, project)
    for i, action in enumerate(plan["actions"]):
        path = resolve_path(action, plan, project)
        if dry_run:
            print(f"would write: {path} ({len(rendered[i])} bytes)")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(rendered[i])
            print(f"wrote: {path} ({len(rendered[i])} bytes)")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], "--dry-run" in sys.argv))
```

### Step 5 — Generate goldens

```bash
python3 adapters/mystack/adapter.py docs/adapter-examples/palette.json --dry-run > adapters/mystack/tests/golden/palette.txt
# ... eyeball the output, edit until correct
# Once correct, save as the actual golden file (e.g., palette.swift / palette.tsx / palette.vue)
```

### Step 6 — Conformance test

Copy `adapters/flutter/tests/conformance.py` as a template; change `STACK = "mystack"` and the file extensions.

### Step 7 — Register in `scripts/resolve_stack.py`

Add `"mystack"` to the known list so `STACK=mystack` resolves cleanly instead of erroring with "available adapters: ...".

### Step 8 — Wire `theme-audit` lint set (optional but recommended)

```bash
touch scripts/audit_lint_sets/mystack.yaml
```

Add regex patterns for hardcoded colors / sizes in your stack's idiom. WCAG contrast logic is universal and reused.

### Step 9 — Document

Write `adapters/mystack/STACK_NOTES.md` covering:
- Assumed project conventions (build tool, file layout).
- Override hooks (`paths:` config keys).
- Known limitations (unsupported token roles, widget types).

### Step 10 — PR

Submit a PR with:
- All adapter files under `adapters/mystack/`.
- A row added to README §Stack support.
- A row added to ROADMAP §"v1.3+ additive stacks" backlog (mark done).
- Conformance passes: `python3 adapters/mystack/tests/conformance.py` → `PASS: 3/3`.

---

## 6. Path conventions per stack

Where each Plan role lands by default. Override via `.design-workflow.yaml` `paths:` block. Future stacks (React Native, Vue+TW, Svelte+TW, plain-React, SwiftUI) document their own conventions in `adapters/<stack>/STACK_NOTES.md`.

| Role / intent | Flutter | Next.js + Tailwind |
|---|---|---|
| Palette | `lib/core/theme/app_colors.dart` | `app/globals.css` (App Router) or `styles/tokens.css` (Pages) + `tailwind.config.ts` |
| Spacing / Radius | `lib/core/theme/app_spacing.dart`, `app_radius.dart` | CSS vars + Tailwind `theme.extend` |
| Typography | `lib/core/theme/app_typography.dart` | CSS vars + Tailwind `fontFamily/fontSize/fontWeight` |
| Motion | `app_motion.dart` + `app_curves.dart` | CSS keyframes + Tailwind transition utilities |
| Widget tree | `lib/features/<feature>/presentation/widgets/<name>.dart` | `components/<feature>/<name>.tsx` |
| Token doc summary | `docs/design-tokens.md` (append) | `docs/design-tokens.md` (append, shared format) |

### Override mechanism

`.design-workflow.yaml`:

```yaml
stack: nextjs-tailwind

paths:
  nextjs_tailwind:
    tokens_css: src/styles/design-tokens.css      # override default app/globals.css
    tailwind_config: tailwind.config.mjs          # override default .ts
    components_root: src/components               # override default components/
```

The adapter's `resolve_path` consults `.design-workflow.yaml` `paths:` first, then falls back to convention. Document the per-stack override keys in `adapters/<stack>/STACK_NOTES.md`.

---

## Versioning

Plan format is at `"1.0"`. Additive changes keep major version; renames/removals bump to `"2.0"` and ship in a major release. Adapters MUST reject unknown majors: `if plan["version"].split(".")[0] != "1": sys.exit(...)`.
