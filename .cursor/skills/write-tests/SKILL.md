---
name: write-tests
description: Write comprehensive, production-quality Kotlin Multiplatform tests for this project. Use when asked to write tests, review test coverage, add a test suite for a class or feature, or when following TDD for a new implementation step.
---

# Write Tests

> If context shifts to a different task type, re-read `.cursor/rules/development-process/skill-context.mdc` and switch skills accordingly.

Before writing any tests, read the following project rules:

- `.cursor/rules/coding-guidelines/testing.mdc` — primary source of truth for test standards
- `.cursor/rules/coding-guidelines/thread-safety.mdc` — concurrency constraints
- `.cursor/rules/kotlin/structured-concurrency.mdc` — coroutine patterns
- `.cursor/rules/kotlin/multiplatform/multiplatform-structured-concurrency.mdc` — KMP concurrency

Apply all of them. Do not duplicate what is already in the rules.

---

Write tests that verify real behavior — not tests that exist only to satisfy coverage. Every test must earn its place. If removing it would not reduce confidence in the code, it should not exist.

## Rules

- **No emojis or icons** anywhere in the file — not in test names, not in test data strings, not in comments.
- **No redundant tests.** Two tests that exercise the same code path with no meaningful difference must be collapsed into one.
- **No comments explaining what a test does.** The test name is self-documenting.
- **No production stubs.** Only write tests. Do not change any production file.

## Testing libraries

Use only what the subject actually needs:

| Subject | Library | When to use |
|---------|---------|-------------|
| Pure logic, data classes, sealed classes | `kotlin.test` | Always — default for all tests |
| Suspend functions, coroutine state | `kotlinx.coroutines.test` (`runTest`, `TestScope`, `UnconfinedTestDispatcher`) | Any `suspend` function or coroutine scope under test |
| `Flow` / `StateFlow` / `SharedFlow` emissions | `app.cash.turbine` (`flow.test { awaitItem() }`) | Observing emitted values from a flow |

Add `@file:OptIn(kotlinx.coroutines.ExperimentalCoroutinesApi::class)` at the top of any file using `UnconfinedTestDispatcher` or `TestScope` directly.

Do **not** use Kotest, JUnit, Mockk, or any other library not listed above.

## Test naming

All test method names follow this exact pattern:

```
`given <precondition> when <action> then <expected outcome>`
```

Be specific. Avoid vague names like `given valid input when called then works`.

## File location

Tests live in `commonTest`:

```
libraries/<name>/src/commonTest/kotlin/com/compiledplatforms/<module>/
```

## What to cover

Think through every behavioral dimension of the subject:

- **Type hierarchy / sealed classes** — each subtype is-a parent; siblings are not each other
- **Identity / equality** — `data object` singletons; `data class` equals + hashCode parity
- **Data class extras** — `copy()`, destructuring, component functions
- **Exhaustive `when`** — matching at every level of a sealed hierarchy; smart-cast field access after type check
- **Null handling** — nullable params, null returns, null vs empty
- **Boundary values** — zero, one, minimum valid, maximum valid, just-over-max
- **Edge-case strings** — empty, whitespace-only, very long, special characters (no emojis in data)
- **Validation** — `require()` / `check()` blocks throw on bad input
- **Collection behavior** — `filterIsInstance`, `distinct`, `contains`, `groupBy` where relevant
- **Order independence** — tests must not depend on execution order
- **Determinism** — no random values, no wall-clock time (use fakes or fixed values)

## What not to cover

- Kotlin language behavior already guaranteed by the compiler (e.g., a `data object` is always the same reference — test it once, not repeatedly).
- Trivially obvious delegation that adds no insight.
- Implementation details not part of the public contract.

## Structure

Group related tests inside the class. Do not use nested classes unless the subject has clearly distinct behavioral groups that would otherwise make the file unnavigable.

## Example

```kotlin
package com.compiledplatforms.example

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs
import kotlin.test.assertNotEquals
import kotlin.test.assertSame

class ExampleResultTest {

    @Test
    fun `given Success when checked against hierarchy then is Result and Success`() {
        val result: ExampleResult = ExampleResult.Success
        assertIs<ExampleResult.Success>(result)
        assertIs<ExampleResult>(result)
    }

    @Test
    fun `given Success when referenced twice then same singleton instance`() {
        assertSame(ExampleResult.Success, ExampleResult.Success)
    }

    @Test
    fun `given Failure when created then exposes message`() {
        val result = ExampleResult.Failure("timed out")
        assertEquals("timed out", result.message)
    }

    @Test
    fun `given two Failure with same message when compared then equal and same hash code`() {
        val a = ExampleResult.Failure("x")
        val b = ExampleResult.Failure("x")
        assertEquals(a, b)
        assertEquals(a.hashCode(), b.hashCode())
    }

    @Test
    fun `given all types when matched exhaustively then each case handled`() {
        val labels = listOf(ExampleResult.Success, ExampleResult.Failure("e")).map { result ->
            when (result) {
                is ExampleResult.Success -> "success"
                is ExampleResult.Failure -> "failure: ${result.message}"
            }
        }
        assertEquals(listOf("success", "failure: e"), labels)
    }
}
```
