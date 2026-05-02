# Text role hierarchy (Material 3 conventions)

Use this table when extracting text in Step 2 of `/theme-port`. **Capture only the relative ordering** of font sizes (largest → smallest) in the source frame, then map to roles below — never copy literal `fontSize` / `fontWeight`.

| Role                          | Uso                               | Base size (px) |
|-------------------------------|-----------------------------------|---------------:|
| `displayLarge/Medium/Small`   | Hero numérico, splash             | 57/45/36 |
| `headlineLarge/Medium/Small`  | Títulos de página                 | 32/28/24 |
| `titleLarge/Medium/Small`     | Títulos de card/seção/AppBar      | 22/18/16 |
| `bodyLarge/Medium/Small`      | Texto corrido                     | 16/14/12 |
| `labelLarge/Medium/Small`     | Botão, chip, caption              | 14/12/11 |

## Picking the right role

1. **Hero numbers** (saldo, contagem, valor de destaque) → `display*` (`Medium` is the safe default; `Large` only for truly hero-only screens).
2. **Page titles** (the H1 equivalent) → `headlineSmall` or `titleLarge` depending on density.
3. **Card / section titles** → `titleMedium`.
4. **Body copy** → `bodyMedium` (default), `bodyLarge` for long-form.
5. **CTAs / chips / pills / captions** → `label*`.

## Hierarchy rules

- Adjacent roles must keep ratio ≥1.25× (Material's default scale already satisfies this between adjacent steps; if you collapse two role levels, recheck).
- Don't introduce custom font weights — let `AppButton`, role defaults, and `cappedTextTheme` handle weight.
- A screen has **one anchor**. If you have 2 candidates for `displayMedium`, demote one to `headlineSmall`.

## When to use `cappedTextTheme` (cap at A+)

Elements where the layout is fixed (no reflow on font scale up): badges, pills, bottom-nav tabs, navbar section titles, chips of status, short label/caption text, point/score labels. Anywhere uncapped scaling at A++ would break the layout grid.

For everything else, use the regular `Theme.of(context).textTheme.<role>`.
