# Skill extensions: the `dw:` namespace

`design-workflow` adds project-specific metadata to its SKILL.md files. To stay compatible with the upstream Anthropic skill validator (`quick_validate.py`), all extensions live nested under the officially-allowed `metadata:` key. The `dw:` sub-namespace inside `metadata:` is reserved for design-workflow.

## Why nested under `metadata:`

The upstream validator restricts top-level frontmatter to:

```
{name, description, license, allowed-tools, metadata, compatibility}
```

Top-level `dw:` is rejected (`Unexpected key(s) in SKILL.md frontmatter: dw`). The validator treats `metadata:` as opaque — anything nested under it passes. Probe results recorded in `.specs/features/craft-adoption/tasks.md` T-07.

Choosing `metadata.dw.*` over a body-comment fallback (the alternative considered in design.md D-D) keeps the metadata in parseable YAML, surfaces it to any tool that reads frontmatter, and avoids inventing a comment-marker convention.

## Field: `metadata.dw.craft.requires`

Declares which `craft/<name>.md` documents a skill must load before producing output. List entries are bare doc names (no `.md`, no path).

### Example

From `skills/theme-create/SKILL.md`:

```yaml
---
name: theme-create
description: Creates a complete palette from scratch ...
metadata:
  dw:
    craft:
      requires: [color, typography, anti-ai-slop]
---
```

The skill body must also contain a `## Craft references` section listing the same docs in prose — see the template in `.specs/features/craft-adoption/design.md` §"SKILL.md 'Load craft references' section template". Frontmatter is the machine-readable index; the body section is what the model actually reads at runtime.

## Distinct from `od:`

Upstream `nexu-io/open-design` uses an `od:` namespace for its own extensions. We do **not** consume `od:` and we do **not** mirror our fields into it; `dw.*` is owned by this repo. If a future field has direct equivalent in `od:`, document it here and keep the names parallel.

## Adding a new field

1. Pick a sub-key under `dw.` (e.g. `dw.persona.locale`).
2. Add a section above describing scope, type, and a real example.
3. Run `quick_validate.py` against any skill that uses it to confirm the validator still passes.
4. Record the addition as a decision entry in `.specs/project/STATE.md`.
