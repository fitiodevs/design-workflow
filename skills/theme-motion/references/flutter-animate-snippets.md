# `flutter_animate` snippets — common patterns

Reference for Step 3 (implement) and Step 5 (preserve intent comment) of `/theme-motion`.

## Press feedback (default for any tappable card)

```dart
final pressed = useState(false);

GestureDetector(
  onTapDown: (_) => pressed.value = true,
  onTapUp: (_) => pressed.value = false,
  onTapCancel: () => pressed.value = false,
  child: AnimatedScale(
    scale: pressed.value ? 0.97 : 1.0,
    duration: AppMotion.fast,
    curve: AppCurves.enter,
    child: child,
  ),
)
```

For `flutter_animate` style:

```dart
Container(...)
  .animate(target: pressed ? 1 : 0)
  .scaleXY(end: 0.97, duration: AppMotion.fast, curve: AppCurves.enter)
```

## Shimmer for live progress

```dart
// motion: shimmer fill 2.4s linear infinite — sinaliza progresso vivo
// referência: docs/motion.md §4.2
final reduceMotion = MediaQuery.of(context).disableAnimations;

Container(...)
  .animate(onPlay: (c) => reduceMotion ? null : c.repeat())
  .shimmer(
    duration: AppMotion.shimmer,
    color: context.colors.bgSkeleton,
  );
```

## Pulse on a next-target node

```dart
Container(...)
  .animate(onPlay: (c) => c.repeat(reverse: true))
  .scaleXY(begin: 1.0, end: 1.05, duration: const Duration(milliseconds: 1800), curve: AppCurves.enter);
```

(If `AppMotion.pulse` exists, prefer it. Created literal here only because token might be absent.)

## Hero number entrance

```dart
Text(value, style: theme.textTheme.displayMedium)
  .animate()
  .fadeIn(duration: AppMotion.normal, curve: AppCurves.enter)
  .scaleXY(begin: 0.95, end: 1.0, duration: AppMotion.normal, curve: AppCurves.enter);
```

## Stagger (list of cards)

```dart
return ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, i) => CardItem(item: items[i])
    .animate(delay: (i * 50).ms)
    .fadeIn(duration: AppMotion.normal, curve: AppCurves.enter)
    .moveY(begin: 12, end: 0, duration: AppMotion.normal, curve: AppCurves.enter),
);
```

Cap at ≤8 items — beyond that the cumulative delay sabotages perceived speed.

## Route transition

```dart
GoRoute(
  path: '/celebration',
  pageBuilder: (context, state) => CustomTransitionPage(
    child: const CelebrationPage(),
    transitionDuration: AppMotion.normal,
    transitionsBuilder: (_, anim, __, child) => FadeTransition(
      opacity: CurvedAnimation(parent: anim, curve: AppCurves.enter),
      child: child,
    ),
  ),
);
```

## Reduce-motion branch (mandatory wrapper for any non-press motion)

```dart
final reduceMotion = MediaQuery.of(context).disableAnimations;

Container(...)
  .animate(onPlay: (c) => reduceMotion ? null : c.repeat())
  .fadeIn(duration: reduceMotion ? Duration.zero : AppMotion.normal);
```

What to cut with reduce-motion: infinite loops (shimmer, pulse) → static end-state; stagger between items → all appear at once; movement (slide, scale) → fade only.

What to keep: press feedback (tactile a11y), color changes for state (success, error), final layout visibility (end-state must never be invisible).
