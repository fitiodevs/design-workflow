# Source → Flutter widget mapping

Use this table in Step 4 of `/theme-port`. Map source-frame elements (Figma layers or HTML tags) into the project's design-system widgets before composing.

## Element → component

| Source element | Flutter widget | Notes |
|---|---|---|
| Tap target with label | `AppButton(variant: primary\|secondary\|ghost\|danger\|social)` | Pick variant by hierarchy / context |
| Single text input | `AppTextField` | Outlined; standard chrome |
| 2+ inputs in same logical block | `AppFormGroup` containing `AppTextField(bare: true)` | See `AppFormGroup` rule below |
| Card | `Card` | Defaults from theme |
| Scaffold + top bar | `AppScaffold` + `AppAppBar` | |
| Empty state | `AppEmptyState` | `title` + `message` |
| Loading | `AppLoading` / `AppSkeleton` | Skeleton preferred when a layout exists |
| Toast / banner | `AppSnackbar.show` | `kind: success\|error\|info\|warning` |
| Confirm modal | `AppDialog.confirm` / `AppDialog.destructive` | |

If no component covers, write custom in `lib/features/<feature>/presentation/widgets/`.

## `AppFormGroup` rule

**Whenever there are 2+ form fields** (`AppTextField`, dropdown, toggle) belonging to the same logical block, wrap them in `AppFormGroup`. The visual result is **one bordered card with the fields stacked and separated by dividers** (same anatomy as a `ProfileSectionContainer` in Settings).

Spec:
- `bgSurface` fill
- `borderDefault` for the outer border AND for the inner dividers (theme token — adapts light/dark automatically)
- `AppRadius.lg`
- No vertical padding on the container; each child controls its own height via `bare`

**Children must use `AppTextField(bare: true)`** — strips outline/fill, vertical padding 14px, hint in `bodyLarge/textSecondary`. Avoids double border and keeps the card as the single visible frame.

```dart
AppFormGroup(
  children: [
    AppTextField(hint: 'Nome', bare: true, controller: nomeCtrl),
    AppTextField(hint: 'Email', bare: true, controller: emailCtrl),
    AppTextField(hint: 'CPF', bare: true, controller: cpfCtrl),
    AppTextField(hint: 'Data de nascimento', bare: true, controller: dataCtrl),
  ],
)
```

```
┌─────────────────────────┐
│  Nome                   │
├─────────────────────────┤
│  Email                  │
├─────────────────────────┤
│  CPF                    │
├─────────────────────────┤
│  Data de nascimento     │
└─────────────────────────┘
```

### Exceptions

- 1 field only → `AppTextField` solto (default outlined mode), no wrapper.
- Fields from different sections (e.g. "Personal data" + "Address") → 2 separate `AppFormGroup`s, each with its own section title.
- Lone search bar / single comment → `AppTextField` default, not `bare`.
- **Do not** combine `bare: true` with `prefixIcon` — the icon ends up visually disconnected. If you need an icon, use the default mode in a standalone field outside `AppFormGroup`.
