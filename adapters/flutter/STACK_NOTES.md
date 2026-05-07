# Flutter adapter — stack notes

> Reference adapter for v1.2.0. Byte-equivalent to pre-v1.2 `theme-port` / `theme-extend` output.

## Assumed conventions

| Concern | Default path |
|---|---|
| Color tokens | `lib/core/theme/app_colors.dart` |
| Spacing tokens | `lib/core/theme/app_spacing.dart` |
| Radius tokens | `lib/core/theme/app_radius.dart` |
| Typography | `lib/core/theme/text_theme.dart` |
| Motion tokens | `lib/core/theme/app_motion.dart` |
| Widget files | `lib/features/<feature>/presentation/widgets/<name>.dart` |
| Token docs | `docs/design-tokens.md` |

Override via `.design-workflow.yaml`:

```yaml
paths:
  flutter:
    app_colors: lib/theme/colors.dart
    widgets_root: lib/ui/widgets
```

## Token role → Dart accessor

See `mappings.py` `TOKEN_ROLE_MAP`. Roles map to `context.colors.<role>` (extension on `BuildContext`) or `AppColors.<mode>.<role>` for raw access.

## Widget type → Flutter component

See `WIDGET_TYPE_MAP`. Defaults assume the project ships an `AppButton`, `AppInput`, `AppText` family. Plain `ElevatedButton` / `TextField` / `Text` fallback when no `App*` prefix detected (best-effort heuristic, future work).

## What this adapter writes

- `palette` Plan → full `AppColors` rewrite + `docs/design-tokens.md` summary append
- `widget-tree` Plan → 1 `.dart` file per top-level widget node
- `motion-set` Plan → `AppMotion` + `AppCurves` const file

## Limitations (v1.2.0)

- No partial palette merge — adapter rewrites the whole `AppColors`.
- No `flutter_animate` integration in motion-set output (planned v1.3).
- Widget tree assumes `AppButton`/`AppInput`/etc exist; emits TODO comment when missing.
