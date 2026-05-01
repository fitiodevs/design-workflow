# Contributing

Thanks for considering a contribution.

## Quick rules

- Keep skills **stack-agnostic by default**. If a skill is Flutter-only, mark it in its frontmatter with a `stacks:` hint.
- New skills go in `skills/<kebab-name>/SKILL.md` with Apache 2.0 `LICENSE.txt` next to it.
- Persona names: ship an English archetype + Portuguese alias. Don't ship single-language personas.
- Don't hardcode project paths. Read from `.design-workflow.yaml` (see `config.example.yaml`) or accept them as args.
- Reference `scripts/` from `SKILL.md` with `python3 scripts/<file>.py` — avoid project-relative imports.

## SKILL.md frontmatter

```yaml
---
name: skill-name
description: One sentence describing what it does + when to use. Include both English and Portuguese trigger words.
license: Complete terms in LICENSE.txt
---
```

## Testing

There's no test runner yet. Manual smoke test: install via `./install.sh`, invoke the skill in Claude Code on a sample Flutter project, verify expected output structure.

## Commit style

- Small, focused commits.
- Subject in imperative mood. ≤ 72 chars.
- Body explains the *why* if non-obvious.

## Conduct

Be a decent human. Concrete feedback over vague vibes.
