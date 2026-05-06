# Design: adapter-and-wireframe

## Decisions

### D-A — Two distinct deliverables, one release

The user said v1.4.0 = adapter + wireframe-sketch. They serve different purposes:
- Adapter is foundational infrastructure (unblocks future stacks)
- Wireframe-sketch is a small UX add (early exploration step)

Bundling them keeps the v1.x release cadence reasonable but accepts that wireframe-sketch tasks will block waiting on adapter validation. Mitigation: T-13..T-17 (wireframe) parallelizable with T-08..T-12 (adapter migration), so 2-track execution if a partner agent is available.

### D-B — Adapter Plan as JSON-serialisable Python dict, not class hierarchy

Reason: the Plan is data, not behavior. JSON Schema validates shape. Adapters consume via `json.load`. No Python class plumbing means non-Python adapters (a TypeScript adapter for React Native) can read the same Plan natively.

Trade-off: type-checking is via JSON Schema, not Python `mypy`. Acceptable.

### D-C — Adapter is a script, not a skill

Adapters live in `adapters/<stack>/adapter.py`, invoked by skills via `Bash`. They're not user-facing — user never types `/flutter-adapter`. Reason: adapters are mechanical (deterministic templating); skills are LLM-driven (judgment calls). Mixing them in `skills/` confuses the surface area.

### D-D — Migration scope is theme-port + theme-extend only in v1.4

Both already deal heavily with code emission (the Dart string templates are nontrivial). Migrating both proves the contract handles real complexity. theme-create / theme-motion migrations are simpler in retrospect (less templating, more decision-making) — defer to v1.5 where the feedback from v1.4 informs the simplification.

Skills NOT migrated in v1.4 still work — they continue emitting Flutter directly. The contract doesn't force adoption; it offers a path.

### D-E — Conformance test = golden-file diff

For each example Plan in `docs/adapter-examples/`, the Flutter adapter has a known-good output in `adapters/flutter/tests/golden/`. CI / regression check: `adapter.py <plan.json> | diff - golden/<name>.dart`. Zero diff = conforming.

Future adapters use the same Plans, produce their own goldens. Cross-stack equivalence is implicit (same input, semantically equivalent output for that stack's idiom).

### D-F — `AGENT_STACK` defaults to `flutter`, errors on unknown

A user who never sets it gets current behavior. A user who sets `stack: react-native` in v1.4 gets `Error: adapter 'react-native' not found. Available adapters: flutter` (and a pointer to the contract for contributors).

### D-G — Wireframe-sketch reuses existing knob set conceptually but ships static HTML

In open-design's skill, wireframe-sketch outputs a static HTML with multiple "tabs" (4 by default), each tab is a layout variant on the same page. We adopt verbatim. Don't try to add knobs — this is the **lo-fi exploration before commitment**, knobs go on hi-fi (Clara → tweaks).

Tab content can be themed by state (empty / populated / error / edge) leveraging `craft/state-coverage.md` — that's our delta.

### D-H — Persona for wireframe-sketch: Sketcher / Esboço

Same naming convention as theme skills (PT primary + EN alias). Sketcher fits the existing voice grammar: lo-fi explorer, questioning before committing.

## Architecture

```
<repo>/
├── adapters/                                  NEW
│   └── flutter/
│       ├── adapter.py
│       ├── mappings.py                        # token role + widget mappings
│       ├── templates/
│       │   ├── app_colors.dart.tmpl
│       │   ├── widget.dart.tmpl
│       │   └── design_tokens.md.tmpl
│       └── tests/
│           ├── conformance.py                 # runs all examples → golden diff
│           └── golden/
│               ├── palette.dart
│               ├── widget-tree.dart
│               └── motion-set.dart
├── docs/
│   ├── adapter-protocol.md                    # NEW: the contract
│   ├── adapter-plan.schema.json               # NEW: typed schema for Plans
│   └── adapter-examples/                      # NEW: 3 example Plans
│       ├── palette.json
│       ├── widget-tree.json
│       └── motion-set.json
├── config.example.yaml                        # MODIFIED: add `stack: flutter` field
├── skills/
│   ├── theme-port/SKILL.md                    # MODIFIED: emit Plan, dispatch adapter
│   ├── theme-extend/SKILL.md                  # MODIFIED: same
│   └── wireframe-sketch/                      NEW
│       ├── SKILL.md
│       ├── assets/
│       │   └── tab-template.html
│       └── references/
│           └── lo-fi-conventions.md
├── README.md                                  # MODIFIED: §What changed v1.4.0 + Adapter system section
├── .specs/project/STATE.md                    # MODIFIED: D-18, D-19
└── .claude-plugin/marketplace.json            # MODIFIED: add ./skills/wireframe-sketch, bump 1.4.0
```

## Adapter Plan format (sketch)

```json
{
  "$schema": "https://design-workflow.dev/adapter-plan.schema.json",
  "version": "1.0",
  "kind": "palette" | "widget-tree" | "motion-set",
  "tokens": {
    "palette": {
      "brandDefault": {"light": "#c96442", "dark": "#d97757"},
      "bgBase": {"light": "#f5f4ed", "dark": "#141413"},
      ...
    },
    "typography": {...},
    "spacing": {...},
    "radius": {...},
    "motion": {...}
  },
  "widgets": [
    {
      "type": "AppButton",
      "props": {"label": "Continuar", "size": "lg"},
      "children": [...]
    },
    ...
  ],
  "actions": [
    {"op": "write", "path": "lib/core/theme/app_colors.dart", "content_role": "palette"},
    {"op": "write", "path": "lib/features/coupons/presentation/widgets/milestone_slider.dart", "content_role": "widget-tree"},
    {"op": "append", "path": "docs/design-tokens.md", "content_role": "palette-summary"}
  ]
}
```

The adapter reads `tokens` + `widgets` and renders them according to its templates, then performs `actions` to write files.

## Flutter adapter structure

```python
# adapters/flutter/adapter.py
import json, sys
from mappings import TOKEN_ROLE_MAP, WIDGET_TYPE_MAP
from templates import render_app_colors, render_widget, render_design_tokens

def main(plan_path):
    plan = json.load(open(plan_path))
    if plan["kind"] == "palette":
        return emit_palette(plan)
    elif plan["kind"] == "widget-tree":
        return emit_widget_tree(plan)
    elif plan["kind"] == "motion-set":
        return emit_motion(plan)

def emit_palette(plan):
    rendered = render_app_colors(plan["tokens"]["palette"])
    for action in plan["actions"]:
        if action["op"] == "write":
            open(action["path"], "w").write(rendered)
    return 0
```

~150-200 LOC adapter (templates + mapping + dispatch). Simple but rigorous.

## Migration shape for theme-port

Before:
```
Step 5 — Implement (write Dart files directly)
```

After:
```
Step 5 — Build Adapter Plan (JSON in /tmp/<feature>-plan.json)
Step 6 — Render via adapter (Bash: python3 adapters/$STACK/adapter.py /tmp/<feature>-plan.json)
Step 7 — Validate (flutter analyze)
```

Skill body documents both old and new flows; old flow is gone after v1.4 ships.

## Wireframe-sketch differences from open-design upstream

- Triggers: add `/Esboço`, `/Sketcher` aliases (open-design only ships English keywords).
- Body: cite `craft/state-coverage.md` for tab content variation.
- Output path: `.design-spec/wireframes/<feature>/<timestamp>.html` (overwrite-safe like critique reports).
- Anti-pattern: wireframe is NOT a substitute for Clara — wireframe is for layout exploration; Clara is for typography/microcopy/refinement. Document this.

## Validation strategy

```bash
# 1. quick_validate
VAL=...
for s in skills/*/; do python3 $VAL $s 2>&1 | tail -1; done   # 21/21 valid

# 2. Adapter conformance
python3 adapters/flutter/tests/conformance.py
# diff each docs/adapter-examples/*.json output against goldens
# should print "PASS: 3/3"

# 3. Regression smoke for theme-port migration
# Pre-v1.4: capture a known frame port output (Fitio coupons milestone slider widget) → snapshot
# Post-v1.4: same input → byte-compare against snapshot

# 4. Wireframe smoke
# /wireframe-sketch "milestone slider for cupons" → confirm .design-spec/wireframes/...html exists
# open in browser → confirm 4 tabs visible, hand-drawn aesthetic, sticky-note annotations
```

## Rollback

`git tag pre-v1.4.0` before T-00.

## Estimate

- Adapter contract design + schema + 3 examples: 4h
- Flutter adapter implementation + templates + golden tests: 4h
- theme-port migration + regression smoke: 3h
- theme-extend migration: 2h
- wireframe-sketch fork + Esboço persona + state-coverage tie-in: 2h
- Pipeline docs + STATE + version + final commit: 1.5h
- **Total: ~16.5h** (matches the upper bound; defer-to-v1.5 escape hatch on REQ-A keeps it bounded)
