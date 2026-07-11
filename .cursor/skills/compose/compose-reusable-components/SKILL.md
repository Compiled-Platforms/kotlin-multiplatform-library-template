---
name: compose-reusable-components
description: Patterns for building library-quality reusable Compose components — Material/CMP-style file layout (Xxx.kt + XxxDefaults.kt + XxxLogic.kt), stateless API design, slot APIs, event callbacks, the Defaults pattern for styling, TextField-like color tokens, parameter stability, KDoc, previews, accessibility, adaptive design, and anti-patterns. Use when building a reusable or library-facing composable, designing a component API, organizing a component package, or making a component easily stylable by callers.
disable-model-invocation: true
---

# Reusable Compose Components

> A reusable component is made reusable through five things: **state + callbacks + modifier + slots + defaults.**
>
> **Organize packages like Compose Material3** (`TextField.kt` + `TextFieldDefaults.kt` + impl), not as a single mega-file.

## Design Goals
A library-quality composable must be:
- **Easy to use** — sensible defaults, minimal required parameters
- **Easy to customize** — colors, styles, and shapes overridable without forking
- **Stateless by default** — caller owns state; component receives values and emits events
- **Theme-aware** — defaults read `MaterialTheme` so they work in any app's light/dark theme
- **Well-documented** — KDoc with usage examples, parameter descriptions, and common patterns

---

## Stateless by Default

Reusable components should prefer a controlled (stateless) API. The caller owns state; the component receives it and emits events:

```kotlin
// ✅ Controlled — caller owns state, component is stateless
@Composable
fun SlotInput(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
)

// ✅ Optional convenience helper — stateful wrapper, not the primary API
@Composable
fun rememberSlotState(initialValue: String = ""): MutableState<String> =
    remember { mutableStateOf(initialValue) }
```

Stateful convenience wrappers (`rememberXxxState`) are allowed as optional helpers, but the primary composable API must be stateless and controlled. This makes the component testable, previewable, and composable.

---

## API Structure

### Parameter Order
```kotlin
@Composable
fun ComponentName(
    // 1. Required data parameters
    value: String,
    onValueChange: (String) -> Unit,
    // 2. modifier — first optional parameter, always defaulted
    modifier: Modifier = Modifier,
    // 3. Behavioral options
    enabled: Boolean = true,
    // 4. Content slots — optional composable lambdas
    leadingContent: (@Composable () -> Unit)? = null,
    trailingContent: (@Composable () -> Unit)? = null,
    // 5. Style/appearance — always last, always defaulted
    colors: ComponentColors = ComponentDefaults.colors(),
    style: ComponentStyle = ComponentDefaults.style(),
)
```

### The Defaults Pattern
Separate colors from layout/shape/typography. Both are `@Composable` factory functions so they can read `MaterialTheme`.

**Live in `XxxDefaults.kt`** (with `XxxColors` / `XxxStyle` / animation specs) — same split as Material `TextFieldDefaults.kt`, not buried in `Xxx.kt`.

```kotlin
// XxxDefaults.kt
@Immutable
data class ComponentColors(
    val focusedTextColor: Color,
    val unfocusedTextColor: Color,
    val disabledTextColor: Color,
    val errorTextColor: Color,
    // …container, border/placeholder as needed
) {
    /** Same priority as Material TextFieldColors: disabled → error → focused → unfocused. */
    fun textColor(enabled: Boolean, isError: Boolean, focused: Boolean): Color = when {
        !enabled -> disabledTextColor
        isError -> errorTextColor
        focused -> focusedTextColor
        else -> unfocusedTextColor
    }
}

@Immutable
data class ComponentStyle(
    val size: Dp,
    val shape: Shape,
    val borderWidth: Dp,
    val textStyle: TextStyle,
)

object ComponentDefaults {

    @Composable
    fun colors(
        focusedTextColor: Color = MaterialTheme.colorScheme.onSurface,
        unfocusedTextColor: Color = MaterialTheme.colorScheme.onSurface,
        disabledTextColor: Color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.38f),
        errorTextColor: Color = MaterialTheme.colorScheme.onSurface,
        // …
    ) = ComponentColors(/* … */)

    @Composable
    fun style(
        size: Dp = 56.dp,                             // local default — acceptable for a component-specific dimension
        shape: Shape = MaterialTheme.shapes.small,    // prefer MaterialTheme.shapes over arbitrary dp
        borderWidth: Dp = 1.dp,
        textStyle: TextStyle = MaterialTheme.typography.bodyLarge,
    ) = ComponentStyle(size, shape, borderWidth, textStyle)
}
```

**Why `@Composable` factories?** `MaterialTheme.colorScheme` and `MaterialTheme.typography` are only accessible inside the composition tree. Making `colors()` and `style()` `@Composable` ensures defaults always read the current theme — light, dark, or any custom theme the caller provides.

**On hardcoded sizes:** Component-specific structural dimensions (e.g. `56.dp` for a control height) are acceptable as local defaults. Use `MaterialTheme.shapes` and `MaterialTheme.typography` for visual tokens. Use app design tokens for dimensions that should be consistent across many components.

**Field-like color naming (only when the control is field-like):**
- Follow TextField / OutlinedTextField: `focused` / `unfocused` / `disabled` / `error` per channel.
- Outlined chrome → `*BorderColor`. Filled underline → `*IndicatorColor` only if the UI is truly indicator-like.
- Resolution: `(enabled, isError, focused) -> Color` on `XxxColors`, priority disabled → error → focused → unfocused.
- Skip tokens you do not paint (cursor, selection, prefix/suffix) — YAGNI.

**Other control families:** mirror that Material component instead (e.g. button-like → `containerColor` / `contentColor` / disabled variants like `ButtonColors`; chips, switches, etc. → their Defaults). Do **not** force TextField token names onto non-field components.

Simple one-off components may keep a small custom set when no Material analogue fits — keep names role-based (`contentColor`, `containerColor`), not invented per-state jargon.

---

## File Organization (Material / CMP style)

Mirror how androidx Material3 splits TextField — not Kotlin “one class per file” dogma.

```
component/
  Xxx.kt              # public composable; keep lean
  XxxDefaults.kt      # Colors, Style, Defaults, animation specs, color resolvers
  XxxLogic.kt         # pure Kotlin (required when logic is non-trivial)
  XxxState.kt         # public sealed/state API when needed
  XxxPreviews.kt      # @Preview suite
  XxxImpl.kt          # optional shared internal UI (Material TextFieldImpl.kt)
  XxxEffect.kt        # optional non-trivial effects
```

| Put here | Do not |
|---|---|
| Public composable in `Xxx.kt` | Grow `Xxx.kt` past Detekt comfort (`LongMethod` / `TooManyFunctions`) — extract |
| Colors + Defaults + resolvers in `XxxDefaults.kt` | Separate `XxxColors.kt` unless Defaults is huge |
| Testable rules in `XxxLogic.kt` | Compose imports in Logic |
| Previews in `XxxPreviews.kt` | Mix catalog demos into the library package |

Canonical in-repo example: `libraries/ui-components/.../slotinput/` (`SlotInput.kt`, `SlotInputDefaults.kt`, `SlotInputLogic.kt`, …).

---

## Slot APIs

Prefer composable slots over boolean/configuration explosion. Slots let callers compose content freely without the component knowing what it contains.

```kotlin
@Composable
fun AppListItem(
    title: @Composable () -> Unit,
    modifier: Modifier = Modifier,
    leadingContent: (@Composable () -> Unit)? = null,
    trailingContent: (@Composable () -> Unit)? = null,
    supportingContent: (@Composable () -> Unit)? = null,
)
```

**Use slots for:**
- Leading/trailing content (icons, avatars, checkboxes)
- Supporting/secondary content
- Custom labels or titles
- Action buttons
- Custom empty, error, or loading states

```kotlin
// ✅ Slot API — caller composes content freely
AppListItem(
    title = { Text("Item title") },
    leadingContent = { Icon(Icons.Default.Folder, contentDescription = null) },
    trailingContent = { IconButton(onClick = { }) { Icon(...) } },
)

// ❌ Boolean explosion — inflexible, hard to extend
AppListItem(
    title = "Item title",
    showLeadingIcon = true,
    iconRes = R.drawable.ic_folder,
    showTrailingButton = true,
)
```

---

## Composition Over Configuration

Prefer composable slots and typed configuration objects over many booleans, nullable strings, or style flags.

```kotlin
// ❌ Configuration explosion
AppCard(
    showIcon: Boolean = false,
    showSubtitle: Boolean = false,
    isError: Boolean = false,
    isWarning: Boolean = false,
    subtitleText: String? = null,
)

// ✅ Typed state + slots
AppCard(
    status: CardStatus = CardStatus.Default,  // sealed type
    subtitle: (@Composable () -> Unit)? = null,
    icon: (@Composable () -> Unit)? = null,
)
```

---

## Event Callback Conventions

Callbacks should describe **user intent**, not internal implementation details. Reusable components never navigate, never call repositories, and never hold business state.

```kotlin
// ✅ Describes intent — caller decides what to do
onSubmit: () -> Unit
onDismissRequest: () -> Unit
onItemClick: (id: String) -> Unit
onSelectionChange: (Set<String>) -> Unit

// ❌ Describes implementation or internal state
onButtonClicked: () -> Unit
onInternalStateChanged: () -> Unit
onNavigateToDetails: () -> Unit  // component should not navigate directly
```

---

## Parameter Stability

Prefer stable, immutable parameter types so the component can be skipped during recomposition.

**Prefer:**
- Primitives, `String`, `Boolean`, `Int`, `Dp`, `Color`
- `@Immutable` data classes
- `ImmutableList` / `ImmutableMap` for collections
- Plain lambdas and composable lambdas

**Avoid:**
- `MutableList`, `MutableMap`, mutable data classes
- `ViewModel` references — pass state and callbacks instead
- Repository or service references
- Navigation controllers
- Platform objects (`Context`, `Activity`)

---

## Caller Experience

**Zero config — works immediately:**
```kotlin
SlotInput(value = pin, onValueChange = { pin = it }, format = "####")
```

**Override one thing:**
```kotlin
SlotInput(
    value = pin,
    onValueChange = { pin = it },
    format = "####",
    colors = SlotInputDefaults.colors(
        focusedContainerColor = MaterialTheme.colorScheme.primaryContainer,
    ),
)
```

**Full custom style:**
```kotlin
SlotInput(
    value = pin,
    onValueChange = { pin = it },
    format = "####",
    colors = SlotInputDefaults.colors(
        focusedBorderColor = Color.Transparent,
        unfocusedBorderColor = Color.Transparent,
        focusedContainerColor = MaterialTheme.colorScheme.primaryContainer,
        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant,
    ),
    style = SlotInputDefaults.style(borderWidth = 0.dp),
)
```

The caller never needs to provide everything — only what they want to change.

---

## Dark / Light Mode

Use Material3 color role tokens as defaults — they automatically resolve to the correct value in any theme:

| Token | Light resolves to | Dark resolves to | Use for |
|---|---|---|---|
| `colorScheme.primary` | Brand color | Brand color (adapted) | Active/selected state |
| `colorScheme.outline` | Gray border | Light gray border | Inactive border |
| `colorScheme.onSurface` | Near-black | Near-white | Text/icons on surface |
| `colorScheme.surfaceVariant` | Tinted surface | Tinted surface | Subtle backgrounds |
| `colorScheme.primaryContainer` | Soft primary tint | Soft primary tint | Highlighted container |

Never use hardcoded `Color(...)` values in defaults — they break dark mode.

---

## Documentation (KDoc)

Every public composable must have KDoc:

```kotlin
/**
 * A fixed-slot PIN/code input that renders individual boxes for each character.
 *
 * ## Basic usage
 * ```kotlin
 * var pin by rememberSlotState()
 * SlotInput(value = pin, onValueChange = { pin = it }, format = "####")
 * ```
 *
 * ## No border, colored background
 * ```kotlin
 * SlotInput(
 *     value = pin,
 *     onValueChange = { pin = it },
 *     format = "####",
 *     colors = SlotInputDefaults.colors(
 *         focusedBorderColor = Color.Transparent,
 *         focusedContainerColor = MaterialTheme.colorScheme.primaryContainer,
 *     ),
 *     style = SlotInputDefaults.style(borderWidth = 0.dp),
 * )
 * ```
 *
 * @param value Current slot values. Empty slots are represented by [EMPTY] (`' '`).
 * @param onValueChange Called with the updated slot string on every change.
 * @param format Slot pattern using `#` for input slots, `\#` for a literal `#`.
 * @param mask When non-null, displays this composable instead of actual characters.
 * @param charFilter Returns true for characters the component should accept.
 * @param colors Color overrides. See [SlotInputDefaults.colors].
 * @param style Shape, size, and typography overrides. See [SlotInputDefaults.style].
 */
@Composable
fun SlotInput(...) { ... }
```

---

## Previews

Provide previews covering the full range of component states:

```kotlin
@Preview(name = "Default — Light") @Preview(name = "Default — Dark", uiMode = UI_MODE_NIGHT_YES)
@Composable private fun SlotInputPreview() {
    AppTheme { SlotInput(value = "12  ", onValueChange = {}, format = "####") }
}

@Preview(name = "Complete")
@Composable private fun SlotInputCompletePreview() {
    AppTheme { SlotInput(value = "1234", onValueChange = {}, format = "####") }
}

@Preview(name = "Masked")
@Composable private fun SlotInputMaskedPreview() {
    AppTheme { SlotInput(value = "1234", onValueChange = {}, format = "####", mask = SlotInputDefaults.Mask) }
}
```

**Preview checklist:**
- [ ] Default state (light + dark)
- [ ] Customized/branded style
- [ ] Disabled state (if applicable)
- [ ] Error state (if applicable)
- [ ] Long/overflow text
- [ ] Compact and expanded widths (for layout-sensitive components)

---

## Accessibility

- Icon-only interactive controls must have a meaningful `contentDescription`.
- Decorative icons and images set `contentDescription = null`.
- Custom interactive controls expose their role and state via `Modifier.semantics { }`.
- Touch targets must be at least 48×48dp — use `Modifier.minimumInteractiveComponentSize()`.
- Disabled state is communicated via `enabled = false` on Material components, not manual alpha changes.

```kotlin
Box(
    modifier = Modifier
        .semantics {
            role = Role.Button
            stateDescription = if (selected) "Selected" else "Not selected"
        }
        .minimumInteractiveComponentSize()
)
```

---

## Helper Functions

Provide convenience APIs that reduce boilerplate for common tasks:

```kotlin
// rememberXxxState — reduces ceremony at call sites
// Use rememberSaveable when state should survive saved-state restoration
@Composable
fun rememberSlotState(initialValue: String = ""): MutableState<String> =
    rememberSaveable { mutableStateOf(initialValue) }

// Extension for common derived checks
fun String.isSlotComplete(length: Int): Boolean = this.length == length && none { it == EMPTY }
```

---

## Visibility & Encapsulation
- Public API: the composable function, `XxxColors`, `XxxStyle`, `XxxDefaults`, and any helper functions callers need.
- Internal: rendering helpers, layout logic, private state, and `XxxLogic.kt` functions.
- Use `internal` for anything that should not be part of the public library surface.
- Color/style types are public; resolution helpers on `XxxColors` may be public (Material does this) so callers and tests can reuse them.

---

## Adaptive-First Component Design

Components must not assume a fixed device, screen size, or input method. They adapt to available constraints.

```kotlin
// ✅ Adapts to container width
@Composable
fun AdaptiveCard(
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit,
) {
    BoxWithConstraints(modifier = modifier.fillMaxWidth()) {
        val padding = when {
            maxWidth < 600.dp -> 16.dp
            maxWidth < 840.dp -> 24.dp
            else -> 32.dp
        }
        Card(modifier = Modifier.padding(horizontal = padding)) {
            Column(content = content)
        }
    }
}

// ❌ Assumes phone layout
@Composable
fun PhoneOnlyCard(content: @Composable ColumnScope.() -> Unit) {
    Card(modifier = Modifier.width(340.dp)) { Column(content = content) }
}
```

- Expose content slots (`content: @Composable () -> Unit`) rather than prescribing internal structure.
- Support all input types: touch, mouse, keyboard, stylus.
- Provide previews at compact (360dp), medium (720dp), and expanded (1080dp) widths for layout-sensitive components.

---

## Anti-Patterns

| Anti-pattern | Better |
|---|---|
| Passing `ViewModel` into a reusable component | Pass state and callbacks |
| Many `Boolean` flags for state/content | Sealed type for state; slots for content |
| Hardcoded `Color(...)` in defaults | `MaterialTheme.colorScheme` tokens |
| Component performs navigation | Emit a callback; caller navigates |
| Component owns business state | Caller owns state; component is stateless |
| Fixed phone width (`Modifier.width(360.dp)`) | Adapt to constraints with `fillMaxWidth()` |
| Custom component built from scratch | Wrap a Material component when possible |
| `rememberXxxState` without `rememberSaveable` | Use `rememberSaveable` when state should survive configuration changes |
| Everything in one `Xxx.kt` mega-file | Split Defaults / Logic / Previews like Material |
| Invented color names when a Material analogue exists | Match that control’s tokens (field → TextField; button → Button; …) |
| TextField tokens on a button-like control | `ButtonColors`-style `containerColor` / `contentColor` |
| Color `when`s only inside the composable | `XxxColors.textColor(enabled, isError, focused)` (etc.) |

---

## Reusability Checklist
- [ ] Package split: `Xxx.kt` + `XxxDefaults.kt` (+ `XxxLogic.kt` / previews when needed)
- [ ] Primary API is stateless and controlled — caller owns state
- [ ] All required parameters first, `modifier` first optional, style last
- [ ] Content exposed via slots for flexible composition
- [ ] `XxxColors` and `XxxStyle` as `@Immutable` data classes in `XxxDefaults.kt`
- [ ] `XxxDefaults.colors()` and `XxxDefaults.style()` as `@Composable` factories reading `MaterialTheme`
- [ ] Field-like components use TextField/OutlinedTextField state token names; button-like (etc.) match that Material family
- [ ] Color resolution on `XxxColors` matches the Material analogue’s state inputs (not always TextField’s triple)
- [ ] No arbitrary hardcoded colors or typography in defaults
- [ ] Event callbacks describe user intent — no navigation or business logic
- [ ] Parameter types are stable and immutable
- [ ] KDoc with at least 2–3 usage examples and `@param` for non-obvious parameters
- [ ] Previews for default, customized, disabled, error, and long-text states
- [ ] Accessibility: `contentDescription`, semantics, and minimum touch targets
- [ ] Convenience helpers (`rememberXxxState`) use `rememberSaveable` when appropriate
- [ ] Logic extracted to `XxxLogic.kt` and covered by unit tests
- [ ] Detekt-friendly: extract before `LongMethod` / `TooManyFunctions` suppressions