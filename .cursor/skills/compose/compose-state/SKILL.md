---
name: compose-state
description: Compose state management — MutableState, remember, rememberSaveable, rememberUpdatedState, StateFlow, state hoisting, single source of truth, UI state modeling, derivedStateOf, snapshot collections, and common state mistakes. Use when managing UI state, lifting state, choosing between state mechanisms, modeling loading/error/success states, or debugging stale/incorrect state.
disable-model-invocation: true
---

# Compose State

## Single Source of Truth
Every piece of state has exactly one canonical location. Other layers observe or derive from that state; they never become additional owners.

- Derived values are computed from that state — not stored separately.
- Never duplicate state across composables or layers.
- Events update the owner; observers never maintain local copies.

Violating this principle is the root cause of most state bugs in Compose: one copy updates, another doesn't, and the UI diverges.

---

## State Ownership Layers

State belongs at the layer that needs to own its lifetime and scope:

```
UI Element State       — remember { mutableStateOf() } inside a composable
        ↓
Screen State           — ViewModel.uiState: StateFlow<UiState>
        ↓
Domain / Data Layer    — in-memory cache, observable data source
        ↓
Persistence            — database, DataStore, preferences
```

- **UI element state** (animation, focus, scroll): belongs in `remember` inside the composable.
- **Screen state** (data, loading, errors): belongs in `ViewModel` as `StateFlow`.
- **Shared/cross-screen state**: belongs in a shared ViewModel or repository.
- Never hoist state higher than necessary. Never keep it lower than necessary.

---

## State Hoisting
A composable that receives values and emits events rather than owning state is **stateless** — stateless composables are reusable, testable, and previewable.

```kotlin
// ✅ Stateless — caller owns state
@Composable
fun EmailField(value: String, onValueChange: (String) -> Unit) {
    TextField(value = value, onValueChange = onValueChange)
}

// ❌ Stateful leaf — hard to test, hard to reuse
@Composable
fun EmailField() {
    var value by remember { mutableStateOf("") }
    TextField(value = value, onValueChange = { value = it })
}
```

---

## MutableState

`State<T>` is read-only observable state. `MutableState<T>` is writable observable state. `mutableStateOf()` creates a `MutableState<T>`. In composition, always wrap in `remember` so the state survives recomposition.

```kotlin
// Property syntax — requires explicit type; access via .value
val count: MutableState<Int> = remember { mutableStateOf(0) }
count.value = 1

// Delegated syntax (preferred) — reads and writes via property directly
var count by remember { mutableStateOf(0) }
count = 1
```

Prefer the `by` delegate syntax — it removes `.value` noise and reads naturally. Use the explicit form only when you need to pass the `State` object itself as a reference.

---

## remember

`remember { }` preserves object identity across recompositions. The lambda runs only on first composition.

```kotlin
val interactionSource = remember { MutableInteractionSource() }  // Created once
val filtered = remember(query) { items.filter { it.contains(query) } }  // Recomputed when query changes
```

- `remember { }` — value computed once, survives recomposition
- `remember(key) { }` — recomputed when key changes
- **`remember` and `mutableStateOf` are orthogonal**: `remember` preserves the identity and lifetime of an object across recompositions while the composable remains in the composition; `mutableStateOf` makes a value observable. You typically combine them.

```kotlin
var count by remember { mutableStateOf(0) }  // observable + survives recomposition
```

---

## rememberUpdatedState

`rememberUpdatedState(value)` captures the latest version of a value without restarting any ongoing effect. Use it when a long-lived effect (e.g. a timer, an animation, a subscription) must always invoke the latest callback or read the latest parameter.

```kotlin
@Composable
fun AutoDismiss(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)  // always latest lambda

    LaunchedEffect(Unit) {
        delay(3000)
        currentOnTimeout()  // always calls the most recent lambda, not the one captured at launch
    }
}
```

**Ownership:** `rememberUpdatedState` is a state holder. It produces a `State<T>` that the runtime keeps current. The implementation detail (using `SideEffect` internally) belongs to the effects layer — not relevant here.

---

## rememberSaveable

Use `rememberSaveable` only when the value must survive saved-state restoration supported by the current platform.

- **Android**: restores across configuration changes and process recreation.
- **Other Compose Multiplatform targets**: provide platform-specific saved-state behavior — check platform documentation.
- `rememberSaveable` has serialization cost — do not use it by default.
- Primitive types work automatically. Custom classes need a `Saver`.

```kotlin
// Platform-neutral custom Saver — serialize to/from a primitive
val saver = Saver<MyClass, String>(
    save = { it.value },
    restore = { MyClass(it) }
)
var myState by rememberSaveable(stateSaver = saver) { mutableStateOf(MyClass()) }
```

---

## StateFlow → Compose State

ViewModels expose `StateFlow<UiState>`. Collect it in the `Screen` composable — not inside reusable `Content` composables.

```kotlin
// ViewModel
private val _state = MutableStateFlow(MyUiState())
val state: StateFlow<MyUiState> = _state.asStateFlow()

// Screen composable — use the platform-appropriate collection API
val state by viewModel.state.collectAsStateWithLifecycle()  // Android (lifecycle-aware)
val state by viewModel.state.collectAsState()               // Other platforms
```

**KMP note:** Use the platform-appropriate lifecycle-aware collection API. As KMP lifecycle support evolves, prefer the most lifecycle-aware option available on each platform.

---

## derivedStateOf

Use `derivedStateOf` when a computed value changes **less frequently** than its inputs. It caches the result and only triggers recomposition when the output value actually changes.

```kotlin
// ❌ Recomputes and recomposes on every input change, even if result is identical
val isEnabled = items.isNotEmpty() && selectedIndex >= 0

// ✅ Only recomposes when isEnabled actually flips between true/false
val isEnabled by remember { derivedStateOf { items.isNotEmpty() && selectedIndex >= 0 } }
```

**Do not use `derivedStateOf` for:**
- Trivial or cheap calculations — the overhead exceeds the benefit.
- Values that change as often as their inputs — no caching benefit.
- Anything that isn't read in composition.

---

## UI State Modeling

Model screen state explicitly. Use sealed interfaces to represent mutually exclusive states:

```kotlin
sealed interface ProfileUiState {
    data object Loading : ProfileUiState
    data object Empty : ProfileUiState
    data class Success(val profile: Profile) : ProfileUiState
    data class Error(val message: String) : ProfileUiState
}
```

Or use a single data class with explicit fields when states share most of their shape:

```kotlin
@Immutable
data class ProfileUiState(
    val profile: Profile? = null,
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
) {
    val isEmpty: Boolean get() = !isLoading && profile == null && errorMessage == null
}
```

**Rules:**
- All properties are `val` — never `var` in UI state.
- Collections use `ImmutableList`/`ImmutableMap` from `kotlinx.collections.immutable`.
- Use `copy()` to produce updated state — never mutate in place.
- Derived properties (like `isEmpty`) are computed, not stored.

**SHOULD:** Transform domain models into UI models when presentation-specific formatting, localization, or derived properties are required. Keep presentation concerns out of the domain layer.

---

## Snapshot Collections

For UI element state that contains observable lists or maps, use snapshot-aware collections:

```kotlin
val items = remember { mutableStateListOf<Item>() }  // SnapshotStateList<Item>
val map = remember { mutableStateMapOf<String, Int>() }  // SnapshotStateMap<String, Int>
```

Reads and writes to `SnapshotStateList`/`SnapshotStateMap` are automatically tracked by the runtime — the composable recomposes when items are added, removed, or changed.

**When to use snapshot collections vs `ImmutableList`:**

| Use case | Prefer |
|---|---|
| ViewModel UI state | `ImmutableList` in a `StateFlow` |
| Local composable state that mutates frequently | `mutableStateListOf()` |
| Drag-to-reorder, in-place list editing | `mutableStateListOf()` |
| Data from repository/network | `ImmutableList` (transform at ViewModel layer) |

---

## SnapshotFlow

`snapshotFlow { }` observes snapshot state reads and emits whenever those observed values change, allowing non-Compose `Flow` consumers to react to Compose state.

```kotlin
val flow = snapshotFlow { myState.value }.distinctUntilChanged()
```

---

## State Holders

When UI element state becomes complex — multiple related values, derived properties, or behavior logic — extract it into a dedicated **state holder** class rather than expanding the composable.

```kotlin
class SearchState(initialQuery: String = "") {
    var query by mutableStateOf(initialQuery)
    var isActive by mutableStateOf(false)
    val hasQuery: Boolean get() = query.isNotBlank()

    fun clear() {
        query = ""
        isActive = false
    }
}

@Composable
fun rememberSearchState(initialQuery: String = ""): SearchState =
    remember { SearchState(initialQuery) }

@Composable
fun SearchBar(state: SearchState = rememberSearchState()) {
    // state holds all search-related UI state and behavior
}
```

**When to extract a state holder:**
- Two or more related pieces of state that always change together
- State with derived properties or behavior methods
- State that needs to be hoisted to a parent but is conceptually a single unit
- Reusable components with non-trivial local state (`PagerState`, `DrawerState`, `TextFieldState`)

State holders are lifecycle-scoped to the composable — they live and die with the composition. For state that must survive navigation or configuration changes, use `ViewModel`.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Duplicate state in two composables | Single source of truth — hoist to common ancestor |
| Storing derived values as separate state | Compute with `derivedStateOf` or a `val` property |
| `List` in `@Immutable` data class | Use `ImmutableList` from `kotlinx.collections.immutable` |
| `var x = remember { mutableStateOf(0) }` | `var x by remember { mutableStateOf(0) }` |
| `rememberSaveable` everywhere | Only for saved-state survival |
| `MutableState` in ViewModel | Use `StateFlow` — lifecycle-aware and testable |
| Reading state at top of `Column` | Read as deep/late in the tree as possible |
| Mutating a list in UI state directly | Replace with a new `ImmutableList` via `copy()` |
| Stale lambda in a long-lived effect | Capture with `rememberUpdatedState` |
| Exposing `MutableStateFlow` publicly | Expose `StateFlow` using `asStateFlow()` |
| Mutable domain model used directly as UI state | Convert to an immutable UI state model |
