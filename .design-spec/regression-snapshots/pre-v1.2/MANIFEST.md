# Pre-v1.2.0 Flutter regression snapshot

Captured 2026-05-06 at T-00 of `multi-stack-adapter`. Used by T-18 (theme-port Flutter regression smoke) and T-22 (theme-extend Flutter byte-equivalent check) to confirm v1.2 adapter migration produces identical output.

## Source

Pulled from real Fitio Flutter app at `/media/fitiodev/FITIO/Fitio/fitio/`. These files were ported / extended **before** the adapter system existed — they represent the canonical "Flutter direct emission" output that v1.2 must reproduce byte-for-byte (modulo whitespace formatting).

## Files captured

### `flutter/core-theme/` — output of `theme-extend` and `theme-create`

| File | Pre-v1.2 emitter | Tokens covered |
|---|---|---|
| `app_colors.dart` | `theme-create` + `theme-extend` (palette role) | 29 semantic tokens × light/dark |
| `app_spacing.dart` | `theme-extend` (spacing role) | xs/sm/md/lg/xl scale |
| `app_typography.dart` | `theme-extend` (typography role) | display/title/body/caption hierarchy |
| `app_motion.dart` | `theme-motion` (motion role) | fast/normal/slow durations |
| `app_curves.dart` | `theme-motion` (motion role) | curve presets |

### `flutter/widget-tree/` — output of `theme-port`

| File | Pre-v1.2 emitter | Patterns exercised |
|---|---|---|
| `milestone_track.dart` | `theme-port` | composite container, multi-state rendering, AppColors refs |
| `milestone_empty_card.dart` | `theme-port` | empty-state widget, CTA button, padding tokens |
| `milestone_node.dart` | `theme-port` | leaf widget, conditional styling, motion calls |

## Verification protocol (T-18 + T-22)

```bash
# After v1.2 adapter migration, regenerate the same files via Plan + adapter dispatch:
# 1. Re-port the same Figma frame for milestone_track / milestone_empty_card / milestone_node
# 2. Re-run theme-extend on the same token set for app_colors / app_spacing / etc
# Then byte-diff:

diff -r --strip-trailing-cr \
  .design-spec/regression-snapshots/pre-v1.2/flutter/core-theme/ \
  /media/fitiodev/FITIO/Fitio/fitio/lib/core/theme/

diff -r --strip-trailing-cr \
  .design-spec/regression-snapshots/pre-v1.2/flutter/widget-tree/ \
  /media/fitiodev/FITIO/Fitio/fitio/lib/features/feed/presentation/widgets/

# Expected: zero output (modulo whitespace/formatting normalized by formatter).
# Any non-whitespace diff = regression — halt and investigate before commit.
```

## Acceptable diff sources (false positives)

- Trailing newline differences (some editors strip, others don't).
- Reordered imports if dart format changed normalization rules.
- Inline comment additions explaining adapter dispatch (must be confined to step-7 hooks).

## Hard regression signals (must NOT happen)

- Different `Color(0xFF...)` value for any semantic token.
- Different file path (`lib/core/theme/app_colors.dart` MUST remain the destination).
- Renamed accessor (`brandDefault` MUST remain `context.colors.brandDefault`).
- Changed widget class structure (props order, named-arg names).
- Changed `AppMotion` duration values.

If any of these appear in the diff, the adapter has drifted from byte-equivalent — fix or roll back via `git reset --hard pre-v1.2.0`.
