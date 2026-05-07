# React Native adapter — stack notes

> Reference adapter for v1.4.1 — React Native (bare or Expo). Renders Adapter Plans to TypeScript: `colors.ts` + `motion.ts` exports, plus `.tsx` components using RN core primitives + `StyleSheet.create()`.

## Assumed conventions

| Concern                | Default path (bare RN, `src/`) | Default path (Expo Router, `app/`) |
|---|---|---|
| Color tokens (TS)      | `src/theme/colors.ts`           | `app/theme/colors.ts`              |
| Motion tokens (TS)     | `src/theme/motion.ts`           | `app/theme/motion.ts`              |
| Widget files           | `src/components/<feature>/<name>.tsx` | `app/components/<feature>/<name>.tsx` |
| Token docs             | `docs/design-tokens.md`         | `docs/design-tokens.md`            |

Override via `.design-workflow.yaml`:

```yaml
paths:
  react_native:
    tokens_palette: src/theme/colors.ts
    tokens_motion:  src/theme/motion.ts
    components_root: src/ui
```

## Detection

`has_expo()` — `true` when **either**:
- `app.json` has a top-level `expo` key, **or**
- `package.json` has `expo` or any `expo-*` package in `dependencies`/`devDependencies`.

`app_or_src()` — `"app"` if `app/` and `app.json` co-exist (Expo Router signal), else `"src"`. Greenfield writes default to `"src"`.

In dry-run / pure-render mode (no project context), both default to bare-RN / `"src"`.

## Token role → TS accessor

29 canonical roles map to camelCase fields on a `Palette` object — emitted as `lightColors` and `darkColors` exports plus a `palettes` lookup. Components consume them via a project-supplied `useColors()` hook (`@/theme/useColors`) — the adapter does **not** ship the hook itself; downstream wires it to a context provider gated on `useColorScheme()` or a store.

Inside generated components, all colors come from the `colors` const obtained at the top of the function. Styles live in a `makeStyles(colors)` factory wrapped in `useMemo` to keep RN's `StyleSheet.create` happy without re-computing on every render:

```tsx
export function MyComponent() {
  const colors = useColors();
  const styles = useMemo(() => makeStyles(colors), [colors]);
  return <View style={styles.root}>...</View>;
}

const makeStyles = (colors: Palette) => StyleSheet.create({
  root: { backgroundColor: colors.bgBase },
});
```

This is the standard RN idiom for theme-aware styles — color refs at module scope would crash because `colors` isn't in scope there.

## Widget type → RN primitive

| Plan type   | RN component                 | Notes |
|---|---|---|
| `button`    | `Pressable`                  | Label rendered as child `<Text>`; variant + size drive style entries (primary/secondary/ghost × xs..xl). |
| `text`      | `Text`                       | Bare strings outside `<Text>` crash RN; the adapter always wraps. |
| `container` | `View`                       | `gap` defaults to `8` for stacked groups. |
| `form-group`| `View`                       | RN has no `<form>`; submission handled by the consumer. |
| `input`     | `TextInput`                  | **Self-closing**; label emitted as a sibling `<Text>` inside a wrapping `<View>` (RN's `TextInput` rejects children). |
| `select`    | `View`                       | Core RN ships no Select; downstream wires `@react-native-picker/picker`. |
| `checkbox`  | `Pressable`                  | Same — community packages or hand-roll. |
| `switch`    | `Switch`                     | Core RN. Self-closing. |
| `slider`    | `Slider`                     | Imports from `@react-native-community/slider` (separate import line). |
| `card`      | `View`                       | Default style: `bgSurfaceRaised`, `padding: 16`, `borderRadius: 12`. |
| `list`      | `FlatList`                   | Renderable; the adapter doesn't auto-fill `data` / `renderItem` — those come from the calling skill. |
| `divider`   | `View`                       | Renders as a 1px-tall line in `borderDefault`. |
| `image`     | `Image`                      | Self-closing. Source is passed through as a prop. |

Tone aliases (`tone: "muted"`) are mapped to canonical roles (`textMuted`) before lookup; literal hex values pass through unchanged.

## Curve enum → RN Easing

`linear` → `Easing.linear`; `easeIn`/`easeOut`/`easeInOut` → `Easing.in/out/inOut(Easing.ease)`; `spring` → `Easing.elastic(1)`; `bounce` → `Easing.bounce`; `decelerate` → `Easing.out(Easing.cubic)`; `anticipate` → `Easing.in(Easing.back(1.5))`.

Generated `motion.ts` imports `{ Easing, EasingFunction } from "react-native"`. Consumers compose with `react-native-reanimated` or the legacy `Animated` API as they prefer; the tokens are framework-neutral.

## What the adapter does NOT do (v1.4.1)

- **Doesn't ship `useColors()` or a theme provider.** Downstream owns that — the project decides whether to gate on `useColorScheme()`, a Redux/Zustand store, or hand a `mode` prop down. The adapter only emits the `lightColors`/`darkColors`/`palettes` exports.
- **Doesn't run `npx expo install` or `npm i @react-native-community/slider`.** When the Plan needs a community component, the import is emitted; the user installs.
- **Doesn't resolve image sources.** `image` widget passes `src` through as-is; consumer wires `require()` or remote URI handling.
- **Doesn't emit Reanimated worklets.** Motion is exported as `{ durationMs, easing }`; the consumer calls `withTiming(target, { duration, easing })` themselves.
- **Doesn't lint or format.** Output passes basic syntax checks only; run `prettier`/`eslint` after generation.

## Limitations / future work

- **Plan props can carry HTML-only attributes** (e.g. `autocomplete`, `required`). They're emitted as JSX attributes — RN will silently ignore them in production but TypeScript's strict mode may flag them. Skills emitting Plans for `react-native` should prefer RN-native props (`autoComplete`, `secureTextEntry`); this is a Plan-format coordination, not an adapter bug.
- **`onPress` is emitted as a string** (handler name) per the Plan contract; matches the next.js adapter behavior. The user replaces with a real handler in their wiring layer.
- **No `View.title`/`View.description` props in RN** — the Plan's `title`/`description` props pass through unchanged. Consumer can extract them or ignore them. Future Plan v1.1 may move these into a `meta` field per node.
- **Variant detection for shadcn-equivalent libraries** (e.g. `@gluestack-ui`, `tamagui`) is not yet automated. v1.5+ candidate.
