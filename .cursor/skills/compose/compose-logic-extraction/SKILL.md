---
name: compose-logic-extraction
description: Pattern for extracting testable presentation logic out of Compose composables into pure Kotlin. Use when building a composable with non-trivial logic, refactoring for testability, or when the code involves validation, state transitions, parsing, formatting, event classification, or multi-step input handling.
disable-model-invocation: true
---

# Compose Logic Extraction

## The Core Problem

Compose composables are hard to unit test directly — they require a UI harness, a test rule, and real composition. Logic buried inside a composable (validation, state transitions, input handling, formatting) becomes untestable and prone to regressions when UI changes.

**The solution:** extract all non-UI logic into a pure Kotlin file with zero Compose dependencies. Test it with `kotlin.test`. The composable becomes a thin shell that calls into the logic layer.

```
Composable (UI, layout, Compose APIs)
       ↓ calls
XxxLogic.kt (pure Kotlin — presentation logic)
       ↓ may use
Domain Layer (optional — business rules, use cases)
```

The extracted logic is **presentation logic**, not business/domain logic. It handles how the UI behaves — not what the app does.

---

## Should This Be Extracted?

**Extract when the code:**
- Contains branching rules or conditional state transitions
- Performs validation, parsing, or formatting
- Classifies or filters input
- Has multiple edge cases worth testing
- Can be tested without Compose
- Is reused by multiple composables

**Leave in the composable when it:**
- Simply maps state to a UI element
- Chooses layout or applies modifiers
- Manages focus, animation, or IME
- Uses Compose-only APIs (`remember`, `LaunchedEffect`, `Modifier`)

---

## Logic Layer Rules

Logic functions must be:
- **Deterministic** — same inputs always produce same outputs
- **Side-effect free** — no I/O, no mutation, no logging inside the function
- **Non-mutating** — do not mutate caller-owned objects; return new values
- **Immutable results** — return plain data, not `State<T>` or `MutableState`
- **Explicit** — depend only on their parameters; no global or injected state

---

## Dependencies

The logic layer must not depend on:
- Compose (`androidx.compose.*`, `org.jetbrains.compose.*`)
- Android, iOS, or Desktop platform APIs
- Navigation controllers or back stacks
- ViewModels or DI containers
- `Context`, `Activity`, or any platform runtime

It may depend on:
- Kotlin stdlib
- `kotlinx` libraries (collections, serialization, coroutines — selectively)
- Shared domain models from `commonMain`

This means extracted logic compiles unchanged in every source set. **Place it in `commonMain`** whenever it has no platform dependencies.

---

## Naming Conventions

| File | Purpose |
|---|---|
| `XxxLogic.kt` | Pure logic functions and constants |
| `XxxLogicTest.kt` | Unit tests — `kotlin.test`, no UI harness |
| `XxxLogicResult` | Result type carrying outputs + next state |
| `XxxInputEvent` | Sealed class for classified input events |

Place both `XxxLogic.kt` and `XxxLogicTest.kt` in the same package as the composable. The logic file contains only pure Kotlin — no `@Composable`, no `Modifier`, no `State`.

Logic sits beside the Material/CMP-style package split (see `compose-reusable-components`):

```
Xxx.kt / XxxDefaults.kt / XxxLogic.kt / XxxState.kt / XxxPreviews.kt
```

Do not put color tokens or `@Composable` defaults in `XxxLogic.kt` — those belong in `XxxDefaults.kt`.

---

## When Functions Are Not Enough

When presentation logic must maintain transient UI state across multiple operations, extract it into a **state holder** rather than accumulating mutable helper functions.

State holders that use `mutableStateOf` have a Compose dependency — they live alongside the composable, not in the platform-agnostic `XxxLogic.kt` file. The separation is:

```
XxxLogic.kt          ← pure Kotlin, no Compose, commonMain
XxxState.kt          ← state holder, uses mutableStateOf, lives with the composable
XxxComposable.kt     ← UI shell, uses both
```

```kotlin
// XxxState.kt — Compose dependency, lives with the composable (not in pure logic)
class SearchState(initialQuery: String = "") {
    var query by mutableStateOf(initialQuery)   // Compose — cannot go in XxxLogic.kt
    var isActive by mutableStateOf(false)
    val hasQuery: Boolean get() = query.isNotBlank()

    fun clear() { query = ""; isActive = false }
    fun activate() { isActive = true }
}
```

Use state holders for: form editing, multi-step workflows, selection state, search state, stepper state. State holder guidance is covered fully in the `compose-state` skill.

---

## Structure Pattern

```kotlin
// XxxLogic.kt — pure Kotlin, no Compose imports

// Constants
const val EMPTY = ' '

// Simple extension functions
fun String.isComplete(): Boolean = none { it == EMPTY }

// Result types — carry output + next state together
data class OperationResult(
    val value: String,
    val nextFocusIndex: Int?,
)

// Stateless transformation functions — all inputs explicit
fun applyInput(
    current: String,
    input: Char,
    at: Int,
    validator: (Char) -> Boolean,
): OperationResult {
    if (!validator(input)) return OperationResult(current, at)
    val updated = current.toCharArray().also { it[at] = input }.concatToString()
    val next = if (at < current.length - 1) at + 1 else null
    return OperationResult(updated, next)
}

// Event classification via sealed class
sealed class InputEvent {
    data class Character(val char: Char) : InputEvent()
    data object Backspace : InputEvent()
    data class Paste(val text: String) : InputEvent()
}

fun classifyEvent(old: String, new: String): InputEvent { ... }
```

---

## Calling from the Composable

The composable calls logic functions inside event handlers — never during composition. For controlled (stateless) composables, results flow back to the caller via `onValueChange`:

```kotlin
@Composable
fun SearchBar(value: String, onValueChange: (String) -> Unit) {
    BasicTextField(
        value = value,
        onValueChange = { raw ->
            // ✅ Logic called in event handler — result goes to caller
            val result = applySearchInput(raw, maxLength = 100)
            onValueChange(result.sanitized)
        },
    )
}
```

For intentionally stateful composables, call logic from event handlers and update local `remember` state:

```kotlin
@Composable
fun SelfContainedForm() {
    var formState by remember { mutableStateOf(FormState()) }

    SubmitButton(onClick = {
        // ✅ Logic called in event handler — local state updated with result
        val result = validateForm(formState)
        formState = formState.copy(errors = result.errors)
    })
}
```

---

## Testing Pattern

```kotlin
// XxxLogicTest.kt — kotlin.test, no UI harness, runs on all KMP targets

class PinInputLogicTest {

    @Test
    fun `applyInput fills correct slot and advances focus`() {
        val result = applyInput("   ", '5', at = 0) { it.isDigit() }
        assertEquals("5  ", result.value)
        assertEquals(1, result.nextFocusIndex)
    }

    @Test
    fun `applyInput rejects invalid character`() {
        val result = applyInput("   ", 'A', at = 0) { it.isDigit() }
        assertEquals("   ", result.value)
    }

    @Test
    fun `isComplete returns true when all slots filled`() = assertTrue("123".isComplete())

    @Test
    fun `isComplete returns false when slot is empty`() = assertFalse("1 3".isComplete())
}
```

**Test coverage goals:**
- State transitions (normal path)
- Boundary conditions (first slot, last slot, full, empty)
- Invalid input rejection
- Idempotency where applicable
- Determinism — same input always produces same output

Run with:
```bash
./gradlew :composeApp:testDebugUnitTest --tests "your.package.*"
```

---

## Examples Across the Codebase

This pattern applies to any composable with non-trivial input handling, validation, or state transitions:

| Component | Logic file | What it contains |
|---|---|---|
| `PinInput` | `PinInputLogic.kt` | Digit placement, backspace, paste, IME classification |
| `SearchBar` | `SearchBarLogic.kt` | Query sanitization, debounce triggers, result filtering |
| `PhoneNumberInput` | `PhoneNumberLogic.kt` | Formatting, country code parsing, validity |
| `DateInput` | `DateInputLogic.kt` | Date parsing, range validation, day/month/year navigation |
| `OtpInput` | `OtpInputLogic.kt` | Character validation, slot advancement, paste detection |
| `Stepper` | `StepperLogic.kt` | Increment/decrement, min/max clamping, step validation |
| `AddressForm` | `AddressFormLogic.kt` | Field validation, format normalization |
| `FilterPanel` | `FilterLogic.kt` | Filter combination, active filter count, reset |
| `Paginator` | `PaginationLogic.kt` | Page calculation, offset computation, boundary detection |

---

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Validation logic inside `onValueChange` lambda | Extract to `validate(input): ValidationResult` |
| Formatting inside the composable body | Extract to `format(value): String` |
| Mutable singleton helper object with state | Pure function with explicit inputs/outputs |
| Compose types (`TextFieldValue`, `Color`) in logic | Use plain Kotlin types; convert at the composable boundary |
| Hidden mutable state inside logic functions | All state must be explicit parameters or returned results |
| Logic that only works on Android | Move platform-specific logic to `androidMain`; keep shared logic in `commonMain` |

---

## Extraction Checklist

- [ ] Identify all transformations, validations, and state transitions
- [ ] Create `XxxLogic.kt` in the same package — no Compose imports
- [ ] Place in `commonMain` unless it has genuine platform dependencies
- [ ] Each function has explicit inputs and a single return value or result type
- [ ] Define `XxxLogicResult` when a function produces multiple outputs
- [ ] Sealed class for input event classification when needed
- [ ] Call logic functions from event handlers only — never during composition
- [ ] Write `XxxLogicTest.kt` covering normal, edge, invalid, and boundary cases
- [ ] Composable body contains only UI structure, event wiring, and Compose-specific state
