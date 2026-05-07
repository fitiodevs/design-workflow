# Pre-v1.2 Flutter regression snapshots

Captured against Fitio (private app repo) `coupons_milestone_slider` widget — a known frame already ported under v1.1.x.

The snapshot intent (per task T-00) is to byte-diff future v1.2 outputs against pre-v1.2 baseline. Because design-workflow ships as a public skill repo without the Fitio app code in-tree, the actual `.dart` files live in the consumer project; this directory holds the reference path layout and the conformance harness uses the Fitio repo paths during dogfood.

## Reference: paths captured

- `lib/core/theme/app_colors.dart` (palette tokens)
- `lib/features/coupons/presentation/widgets/milestone_slider.dart` (widget tree)

## How regression is verified (T-18)

```bash
# In the Fitio project, with stack=flutter (default):
/theme-port https://figma.com/design/...?node-id=...   # the Coupons milestone slider frame
diff -r --strip-trailing-cr <pre-v1.2-snapshot>/ <new-output>/
# Expect: zero diff (modulo formatting whitespace).
```

Snapshot capture protocol on the Fitio side:

```bash
git checkout pre-v1.2.0   # tag created in T-00
cp lib/core/theme/app_colors.dart \
   lib/features/coupons/presentation/widgets/milestone_slider.dart \
   ~/scratch/pre-v1.2-snapshot/flutter/
git checkout main
```
