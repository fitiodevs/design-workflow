# Customizing for your project

The skills ship with Flutter-first defaults inherited from the project they were extracted from. To use them on your own codebase, drop a `.design-workflow.yaml` at your repo root.

## Quickstart

```bash
cp /path/to/design-workflow/config.example.yaml ./.design-workflow.yaml
# edit paths to match your structure
```

## Token paths

Default Flutter layout:

```yaml
tokens:
  colors: lib/core/theme/app_colors.dart
  spacing: lib/core/theme/app_spacing.dart
  motion: lib/core/theme/app_motion.dart
  curves: lib/core/theme/app_curves.dart
  text_theme: lib/core/theme/app_theme.dart
```

If your project uses a different convention, point the config at the right files. Skills resolve tokens from these locations.

## Product doc

`theme-critique` and `ux-writing` read your product brief to:
- Run a 3-persona walkthrough of the screen.
- Score the AI-slop verdict (a screen that contradicts your product brief is slop, even if it looks fine).
- Align copy voice with documented tone.

Default: `docs/product.md`. Override:

```yaml
product:
  doc: docs/brief.md
```

## User personas

These drive the persona walkthrough in `theme-critique`. Skills want **named, concrete** personas — not "the user". Example:

```yaml
product:
  personas:
    - name: "Diego"
      context: "Engenheiro 32, casado, 1 filho. Vai à academia 3×/semana às 6h."
      goal: "Manter rotina sem virar atleta. Quer número claro de progresso."
    - name: "Marina"
      context: "Personal trainer 28. Compete em corrida de rua amadora."
      goal: "Bater PR no próximo 10k. Acompanha métricas detalhadas."
    - name: "Léo"
      context: "Estudante 19. Começou na academia há 2 meses."
      goal: "Entender se está progredindo. Tudo é novo, intimidante."
```

Concrete > abstract every time.

## Widget conventions

If your design system widgets follow a different naming pattern, adjust:

```yaml
widgets:
  prefix: My              # MyButton, MyDialog, MyScaffold
  primary_button: MyButton
  scaffold: MyScaffold
  text_field: MyInput
  dialog: MyDialog
  snackbar: MyToast
```

Skills use these names when porting Figma → widgets and when reporting violations in `theme-audit`.

## Locale

`ux-writing` enforces a single locale across user-facing strings. Default: `pt_BR`. Override:

```yaml
locale: en_US
```

## Stack hints

Currently informational; future versions will branch behaviour:

```yaml
stack:
  framework: flutter      # flutter | react-native | swift-ui | (future)
  state: riverpod         # riverpod | bloc | provider | redux | ...
  routing: go_router
  backend: supabase       # supabase | firebase | rest | graphql | ...
```

## Stack-agnostic skills

A subset works on any codebase that uses tokens:

- `theme-audit` — works on any text-based codebase if you tell it which patterns are tokens vs hardcode (Dart `Color(0xFF...)`, CSS `#hex`, etc.). Future versions will detect by language.
- `theme-create` — pure palette generation, language-agnostic. Outputs Dart by default; can be redirected.
- `theme-critique` — Nielsen 10 + AI-slop check don't depend on stack.
- `frontend-design` — outputs HTML/CSS regardless of target stack.
- `ux-writing` — operates on copy strings; any project.

Flutter-specific (today):

- `theme-port` — converts to Flutter widgets.
- `theme-extend` — emits Dart token files.
- `theme-motion` — uses `flutter_animate` API.
- `theme-bolder`, `theme-quieter`, `theme-distill` — emit Dart edits.

The roadmap is to make all stack-specific skills pluggable via adapters. Contributions welcome.

## Per-persona overrides

If you want to disable a persona or override their voice, drop a section in `.design-workflow.yaml`:

```yaml
personas:
  amplifier:
    enabled: false        # disable Brasa entirely
  critic:
    voice: "encouraging"  # default: "cutting"
```

Currently best-effort; not all skills honor every override yet.
