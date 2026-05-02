# Verify-block recipes (sequence phase)

> Library of binary pass/fail checks Arquiteto uses in `tasks.md` `verify:` lists.
> Each recipe is one line that can run via Bash and return non-zero on failure.

## Static analysis

```yaml
verify:
  - "flutter analyze <path> → 0 issues"
  - "dart format --set-exit-if-changed <path>"
  - "flutter test test/<file>_test.dart"
```

## Token discipline

```yaml
verify:
  - "regex `Color\\(0x[A-F0-9]+\\)` count in <new files> = 0"
  - "regex `fontSize: \\d+` count in <new files> = 0"
  - "regex `EdgeInsets\\.(all|symmetric|only)\\(\\d+` excluding spacing-token uses in <new files> = 0"
```

## Contrast / accessibility

```yaml
verify:
  - "python scripts/check_contrast.py <token-a> <token-b> light → ≥4.5"
  - "python scripts/check_contrast.py <token-a> <token-b> dark → ≥4.5"
  - "flutter test integration_test/a11y_test.dart"
```

## Visual / structural

```yaml
verify:
  - "<widget-name> appears in lib/<path>.dart (grep)"
  - "AppColors.<token> referenced in lib/<path>.dart (grep)"
  - "TextStyles.<role> referenced in lib/<path>.dart (grep)"
```

## File existence / artifact

```yaml
verify:
  - "file lib/features/<feature>/<path>.dart exists"
  - "asset assets/icons/<name>.svg exists"
  - "build artifact build/<path> generated"
```

## Audit deltas (brownfield)

```yaml
verify:
  - "python scripts/audit_theme.py lib/features/<feature> → hex_count = 0"
  - "python scripts/audit_theme.py lib/features/<feature> → fontsize_count = 0"
```

## Composition tips

- One task → 2-5 verify items typically. <2 = under-specified; >5 = task too big.
- First verify is usually `flutter analyze` (cheap; catches typos).
- Last verify is usually a structural grep (proves the change actually happened).
- Avoid verify that depends on other tasks completing — that belongs in `blocks:`.

## Anti-patterns

- ❌ "Looks correct in browser" — qualitative, doesn't belong here.
- ❌ "User confirms" — that's a phase gate, not a task verify.
- ❌ Verify that requires manual setup (e.g. logging in to Firebase). Move setup to a separate task with its own verify.
- ❌ Verify that is the same as the task body ("widget exists" when task is "add widget"). Verify must be **independently checkable**.
