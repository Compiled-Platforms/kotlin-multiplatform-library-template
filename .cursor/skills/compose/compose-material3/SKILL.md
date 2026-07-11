---
name: compose-material3
description: Material3 in Compose — theme layering, color system, semantic roles, surface hierarchy, typography, shapes, elevation, spacing tokens, dark mode, dynamic color (Android), icon guidance, motion tokens, Material3 Expressive, adaptive navigation, and common theming mistakes. Use when applying theming, customizing Material components, building a design system, or ensuring consistent visual design.
disable-model-invocation: true
---

# Compose Material 3

## Design System Layering

Material3 is the foundation — not the whole design system. Build on top of it:

```
MaterialTheme            ← M3 foundation: color, typography, shapes
      ↓
AppTheme                 ← wraps MaterialTheme, provides app color schemes
      ↓
App design tokens        ← spacing, extended typography, custom colors via CompositionLocal
      ↓
App component wrappers   ← AppButton, AppCard, etc. — Material components with app defaults
      ↓
Screens                  ← consume components and tokens
```

Never flatten this stack — components that bypass the token layer become hard to retheme and test.

---

## Theme Setup

Wrap all content in `AppTheme`, which wraps `MaterialTheme`:

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    // Use a stable reference — AppSpacing has only default vals, so a singleton is fine
    MaterialTheme(
        colorScheme = if (darkTheme) AppDarkColorScheme else AppLightColorScheme,
        typography = AppTypography,
        shapes = AppShapes,
    ) {
        CompositionLocalProvider(
            LocalSpacing provides AppSpacing,  // top-level singleton, not AppSpacing()
        ) {
            content()
        }
    }
}
```

If `AppSpacing` holds mutable or computed values, use `remember` to avoid recreating it:
```kotlin
val spacing = remember { AppSpacing() }
CompositionLocalProvider(LocalSpacing provides spacing) { content() }
```

- `AppTheme` wraps `MaterialTheme` — it never replaces it.
- Define both `AppLightColorScheme` and `AppDarkColorScheme` explicitly.
- All previews use `AppTheme`, not raw `MaterialTheme`.

---

## Color System

Material3 uses semantic color roles — never use raw colors in composables.

| Role | Use for |
|---|---|
| `primary` | Key actions, active states |
| `onPrimary` | Content drawn on primary |
| `primaryContainer` | Tinted container (softer than primary) |
| `onPrimaryContainer` | Content on primaryContainer |
| `secondary` / `tertiary` | Supporting accent colors |
| `error` / `onError` | Error and destructive states |
| `surface` | Card, sheet, menu backgrounds |
| `onSurface` | Content on surface |
| `surfaceVariant` | Slightly tinted surface |
| `outline` / `outlineVariant` | Borders, dividers |
| `scrim` | Modal overlays |

```kotlin
// ✅ Semantic token
Text(color = MaterialTheme.colorScheme.onSurface)
Icon(tint = MaterialTheme.colorScheme.error)

// ❌ Hardcoded color
Text(color = Color(0xFF1C1B1F))
Text(color = Color.Red)
```

**Dark mode is automatic** — `colorScheme` returns correct values for the current theme. Never check dark mode manually to pick colors.

### Semantic Usage Rules
- Use `error` for destructive actions, validation errors, and failure states — not arbitrary reds.
- Use `on*` colors for content drawn on a surface (e.g. `onPrimary` for text on a primary button).
- Use `outline`/`outlineVariant` for borders and dividers — never hardcoded grays.
- Do not use `primary` as a generic accent everywhere — it loses semantic meaning.

---

## Dynamic Color (Android 12+)

> **Android-specific.** Use in `androidMain` only.

```kotlin
val colorScheme = when {
    dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
        if (darkTheme) dynamicDarkColorScheme(context)
        else dynamicLightColorScheme(context)
    }
    darkTheme -> AppDarkColorScheme
    else -> AppLightColorScheme
}
```

- Always provide non-dynamic fallback schemes — dynamic color requires Android 12+.
- For `commonMain`, pass color schemes as parameters or use static/generated schemes injected per platform.

---

## Surface Hierarchy

Material3 defines a surface elevation hierarchy using tonal color, not shadows. Higher tonal elevation = more primary color tinting:

| Token | Typical use |
|---|---|
| `surface` | Base screen background |
| `surfaceContainerLowest` | Sunken surface (input fields) |
| `surfaceContainerLow` | Card on surface |
| `surfaceContainer` | Default card, dialog, sheet |
| `surfaceContainerHigh` | Elevated card, bottom sheet |
| `surfaceContainerHighest` | Top-most surfaces (chips, nav bar) |
| `primaryContainer` | Tinted feature areas |

Use these tokens for backgrounds rather than arbitrary colors. `surfaceContainer` is the correct default for cards — not `surface` or `background`.

**Tonal vs shadow elevation:**
- Material3 prefers tonal elevation (color tint) over shadow elevation.
- Use `tonalElevation` on `Surface`/`Card` — it applies the correct tonal color automatically.
- Shadow elevation (`shadowElevation`) is for cases where a physical shadow is needed (e.g. FAB, dialogs on some surfaces).

---

## Typography

Material3 type scale: `displayLarge/Medium/Small`, `headlineLarge/Medium/Small`, `titleLarge/Medium/Small`, `bodyLarge/Medium/Small`, `labelLarge/Medium/Small`.

```kotlin
// ✅ Use scale tokens
Text(style = MaterialTheme.typography.titleMedium)

// ❌ Never hardcode font sizes
Text(style = TextStyle(fontSize = 16.sp))
```

**Rules:**
- Start all text styles from `MaterialTheme.typography` tokens.
- Define named app text styles only when the M3 scale doesn't have the right token.
- `lineHeight` must be intentional — always set it explicitly in custom text styles, never rely on defaults.
- Use scalable typography: don't lock `fontScale` or clamp text sizes unless overflow is a genuine layout constraint.

### Non-linear Font Scaling (Android 14+)
- **Always use `sp` for text sizes** — follows user font scale preference including non-linear scaling.
- **Never use `sp` for non-text dimensions** (icon size, box height, spacing) — those will scale unexpectedly.
- If a fixed-height container must fit scaled text, use `wrapContentHeight()` rather than a hardcoded `dp` height.

---

## Shapes

Material3 shape tokens: `extraSmall`, `small`, `medium`, `large`, `extraLarge`, `full`.

```kotlin
// ✅ Use theme shape tokens
Card(shape = MaterialTheme.shapes.medium) { ... }

// ❌ Avoid arbitrary corner radii everywhere
Card(shape = RoundedCornerShape(12.dp)) { ... }
```

**Rules:**
- Use `MaterialTheme.shapes` tokens for all corner radii — it keeps shape consistent and themeable.
- For adaptive shapes that scale with component size, use `RoundedCornerShape(percent = N)` as a proportional alternative.
- Prefer `CircleShape` (`MaterialTheme.shapes.full`) for icons and avatar containers.
- Don't use arbitrary `dp` corner radii unless designing a specific one-off shape token.

---

## Elevation

- Use `tonalElevation` on `Surface` and `Card` — M3 uses color tinting to communicate elevation.
- `shadowElevation` adds a drop shadow — use for components that need to "float" (FAB, dialogs).
- Content color on a `Surface` is automatically set to `contentColorFor(backgroundColor)` — let it flow rather than overriding `LocalContentColor` manually.

```kotlin
Card(
    modifier = Modifier.fillMaxWidth(),
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.surfaceContainer,
    ),
    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
) { ... }
```

---

## Customizing Material Components

Use the component's `colors`, `shape`, `elevation`, and `textStyle` parameters — do not wrap and re-implement from scratch:

```kotlin
Button(
    colors = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.primaryContainer,
        contentColor = MaterialTheme.colorScheme.onPrimaryContainer,
    )
) { ... }
```

For app-wide component defaults, define a defaults object so call sites stay clean:

```kotlin
object AppButtonDefaults {
    val minHeight = 48.dp

    @Composable
    fun primaryColors() = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.primary,
        contentColor = MaterialTheme.colorScheme.onPrimary,
    )

    @Composable
    fun secondaryColors() = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.secondaryContainer,
        contentColor = MaterialTheme.colorScheme.onSecondaryContainer,
    )
}
```

---

## Extending the Theme (Custom Tokens)

For tokens not in Material3 (spacing, extended typography, brand colors), provide them via `CompositionLocal`:

```kotlin
data class AppSpacing(
    val xsmall: Dp = 4.dp,
    val small: Dp = 8.dp,
    val medium: Dp = 16.dp,
    val large: Dp = 24.dp,
    val xlarge: Dp = 32.dp,
)

val LocalSpacing = staticCompositionLocalOf { AppSpacing() }

object ExtendedTheme {
    val spacing: AppSpacing @Composable get() = LocalSpacing.current
}

// Usage
Modifier.padding(ExtendedTheme.spacing.medium)
```

Use `staticCompositionLocalOf` for tokens that never change at runtime. Use `compositionLocalOf` for tokens that may change (e.g. per-screen overrides).

---

## Icons

- Tint icons from `LocalContentColor` by default — it automatically inherits the correct on-surface color.
- Decorative icons set `contentDescription = null`.
- Interactive icon-only controls need a meaningful `contentDescription` for accessibility.
- Size icons with `dp`, never `sp`.

```kotlin
// ✅ Inherits correct tint from LocalContentColor
Icon(imageVector = Icons.Default.Favorite, contentDescription = null)

// ✅ Explicit tint when semantic meaning requires a specific color
Icon(imageVector = Icons.Default.Error, tint = MaterialTheme.colorScheme.error, contentDescription = "Error")
```

---

## Motion Tokens (Material 3 Expressive)

Material3 Expressive (2025) introduces `MotionScheme` — standardized spring-based animation tokens. Use them instead of hardcoded `spring`/`tween` specs:

```kotlin
val spec = MaterialTheme.motionScheme.defaultSpatialSpec<Dp>()
val offset by animateDpAsState(targetValue, animationSpec = spec)
```

| Token | Use for |
|---|---|
| `defaultSpatialSpec` | Spatial movement (position, size) |
| `defaultEffectsSpec` | Decorative effects (opacity, color) |
| `defaultSlowSpatialSpec` | Large or deliberate spatial changes |

Material components updated for M3 Expressive apply these tokens automatically. New components: `ButtonGroup`, `LoadingIndicator`, `FloatingToolbar`, `WideNavigationRail`.

**Shape morphing** with `Morph` is available for fluid shape transitions (FAB → sheet, chip → expanded card) — use sparingly for key transitions.

---

## Adaptive Navigation

Select the navigation component based on available window width — not device type:

| Width class | Component |
|---|---|
| Compact | `NavigationBar` (bottom) |
| Medium | `NavigationRail` (side) |
| Expanded | `PermanentNavigationDrawer` or `ModalNavigationDrawer` |

`NavigationSuiteScaffold` selects automatically:

```kotlin
NavigationSuiteScaffold(
    navigationSuiteItems = {
        items.forEach { item ->
            item(
                selected = currentDestination == item.route,
                onClick = { navigate(item.route) },
                icon = { Icon(item.icon, contentDescription = item.label) },
                label = { Text(item.label) },
            )
        }
    }
) {
    // Screen content
}
```

---

## Accessibility Requirements

- Touch targets must be at least 48×48dp — use `Modifier.minimumInteractiveComponentSize()`.
- Never communicate state by color alone — pair with text, icon, or shape.
- Disabled states must remain visually perceivable — use the component's built-in `enabled = false` parameter, which handles alpha and content color automatically via `LocalContentAlpha`. Do not manually set `alpha = 0f` or `alpha = 1f` to fake enabled/disabled state.
- Icon-only controls always need a `contentDescription`.
- Maintain sufficient color contrast — test with Android Accessibility Scanner or equivalent.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| `Color.Red` for errors | `MaterialTheme.colorScheme.error` |
| `Text(fontSize = 14.sp)` | `MaterialTheme.typography.bodyMedium` |
| `RoundedCornerShape(12.dp)` everywhere | `MaterialTheme.shapes.medium` or a named shape token |
| Hardcoded `8.dp` padding everywhere | `ExtendedTheme.spacing.small` or a named spacing token |
| Custom button built from scratch | Wrap `Button` with `AppButtonDefaults.primaryColors()` |
| `Card` with `surface` background | Use `surfaceContainer` — the correct M3 card background |
| Manually checking dark mode to pick colors | Use `MaterialTheme.colorScheme` — it's automatic |
| `primary` used as a generic accent everywhere | Use the semantically correct role (`secondary`, `tertiary`, `primaryContainer`) |
| Hardcoded gray for dividers | `MaterialTheme.colorScheme.outlineVariant` |

---

## Component Checklist
- [ ] All colors from `MaterialTheme.colorScheme` semantic roles — no raw colors
- [ ] All text styles from `MaterialTheme.typography` — no hardcoded `fontSize`
- [ ] All shapes from `MaterialTheme.shapes` — no arbitrary `dp` corner radii
- [ ] Custom tokens via `CompositionLocal` in `AppTheme` — not hardcoded in composables
- [ ] Component customization via `colors`/`shape`/`elevation` params — not re-implemented from scratch
- [ ] App-wide component defaults in `AppXxxDefaults` objects
- [ ] Light and dark `@Preview` using `AppTheme`
- [ ] Navigation uses `NavigationSuiteScaffold` or adapts to window width
- [ ] Icon-only controls have `contentDescription`
- [ ] Touch targets ≥ 48×48dp
