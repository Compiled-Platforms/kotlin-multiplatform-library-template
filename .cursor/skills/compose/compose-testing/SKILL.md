---
name: compose-testing
description: Compose UI testing — testing philosophy, KMP platform separation, semantics depth, finders, assertions, fake state, animation testing, screenshot determinism, adaptive testing, accessibility matchers, and common mistakes. Use when writing UI tests, setting up test infrastructure, testing composables in isolation, or auditing accessibility.
disable-model-invocation: true
---

# Compose Testing

## Testing Philosophy

**Test behavior, not implementation.**

- Test what the user sees and can do — not how the composable is structured internally.
- Prefer public composable API, semantics, user-visible text, roles, and content descriptions.
- Use test tags only where semantics are insufficient.
- Avoid: layout hierarchy inspection, internal state access, exact composition structure.

Always test the stateless `XxxContent` composable with fake state — never test `XxxScreen` (ViewModel-wired) in unit tests.

---

## Platform Separation

### Common Compose (all KMP targets)
Use `runComposeUiTest` from `androidx.compose.ui.test` — available in `commonTest` for KMP:

```kotlin
@Test
fun showsLoadingIndicator() = runComposeUiTest {
    setContent {
        MyContent(state = MyState(isLoading = true))
    }
    onNodeWithTag("loading_indicator").assertIsDisplayed()
}
```

Pure logic tests with `kotlin.test` run on all targets without a UI harness — prefer them for business logic.

### Android
Use `createComposeRule()` or `createAndroidComposeRule<Activity>()` in `androidTest`:

```kotlin
class MyScreenTest {
    @get:Rule val composeTestRule = createComposeRule()

    @Test
    fun `shows loading indicator`() {
        composeTestRule.setContent {
            MyContent(state = MyState(isLoading = true))
        }
        composeTestRule.onNodeWithTag("loading_indicator").assertIsDisplayed()
    }
}
```

Screenshot testing: **Paparazzi** (JVM, no device) or **Roborazzi** (Robolectric-based).
Accessibility checks: Android Accessibility Test Framework via `enableAccessibilityChecks()`.

### iOS / Web
Prefer pure logic tests (`commonTest`) and platform-level UI automation. Compose UI test APIs may have limited availability on these targets — verify per CMP release.

### Desktop
Desktop Compose UI tests use the same `runComposeUiTest` API where the test runner is available. Verify support per CMP release.

---

## Finder Priority

Prefer finders in this order — more robust matchers first:

1. **Role / semantics** — `hasRole(Role.Button)`, `hasSetTextAction()`
2. **User-visible text** — `onNodeWithText("Save")`
3. **Content description** — `onNodeWithContentDescription("Close")`
4. **Stable test tag** — `onNodeWithTag("pin_input")`
5. **Custom semantics** — `onNode(hasTestTag("x") and hasStateDescription("Selected"))`

Avoid positional selectors (`onAllNodes(isRoot())[2]`) — they are fragile and do not communicate intent.

---

## Semantics & Merged vs Unmerged Tree

By default, Compose merges semantics for accessibility. Use `useUnmergedTree = true` to target individual nodes inside a merged group:

```kotlin
// Default — merged tree (what accessibility sees)
composeTestRule.onNodeWithTag("card").assertIsDisplayed()

// Unmerged — individual nodes inside a merged container
composeTestRule.onNodeWithTag("card", useUnmergedTree = true)
    .onChildren()
    .filterToOne(hasText("Title"))
    .assertIsDisplayed()
```

Use the unmerged tree when testing reusable components where child nodes are individually meaningful.

Dump the semantics tree for debugging:
```kotlin
composeTestRule.onRoot().printToLog("SEMANTICS")
composeTestRule.onRoot(useUnmergedTree = true).printToLog("SEMANTICS_UNMERGED")
```

---

## Custom Semantics

For reusable components, expose testable state via custom semantics properties rather than internal state:

```kotlin
// Define a custom semantics key
val PinValueKey = SemanticsPropertyKey<String>("PinValue")
var SemanticsPropertyReceiver.pinValue by PinValueKey

// Apply in the component
Modifier.semantics { pinValue = currentValue }

// Query in tests
composeTestRule.onNodeWithTag("pin_input")
    .assert(SemanticsMatcher.expectValue(PinValueKey, "1234"))
```

---

## Common Assertions

```kotlin
.assertIsDisplayed()
.assertIsEnabled()
.assertIsNotEnabled()
.assertIsSelected()
.assertTextEquals("Expected")
.assertContentDescriptionEquals("Label")
.assertHasClickAction()
.assertWidthIsAtLeast(48.dp)
.assertHeightIsAtLeast(48.dp)
```

## Actions

```kotlin
.performClick()
.performTextInput("hello")
.performTextClearance()
.performScrollTo()
.performImeAction()
.performKeyInput { pressKey(Key.Backspace) }
```

---

## Fake State and Callbacks

Never use real ViewModels, repositories, or network calls in Compose tests. Pass fake state directly and capture callbacks to verify user interactions:

```kotlin
// ✅ Fake state — fast, deterministic, no I/O
@Test
fun showsNameWhenLoaded() = runComposeUiTest {
    setContent {
        ProfileContent(
            state = ProfileState(name = "Alice", isLoading = false),
            onSave = {},
        )
    }
    onNodeWithText("Alice").assertIsDisplayed()
}

// ✅ Captured callback — verify user intent
@Test
fun submitCallbackFiredOnClick() = runComposeUiTest {
    var submitted = false
    setContent {
        PinInput(
            value = "1234",
            onValueChange = {},
            onSubmit = { submitted = true },
            format = "####",
        )
    }
    onNodeWithTag("submit_button").performClick()
    assertTrue(submitted)
}

// ❌ Real ViewModel — slow, non-deterministic, hard to control
composeTestRule.setContent {
    ProfileScreen(viewModel = ProfileViewModel(realRepo))
}
```

---

## Accessibility Matchers

```kotlin
// Role
onNode(hasRole(Role.Button))
onNode(hasSetTextAction())

// State
onNode(hasStateDescription("Selected"))
onNode(isSelected())
onNode(isEnabled())
onNode(isFocusable())

// Content description
onNodeWithContentDescription("Close dialog")

// Touch targets (≥ 48dp)
onNodeWithTag("icon_button")
    .assertWidthIsAtLeast(48.dp)
    .assertHeightIsAtLeast(48.dp)
```

---

## Testing Logic Separately

Extract composable logic into pure functions and test with `kotlin.test` — no UI harness needed. This is faster, more reliable, and runs on all KMP targets.

```kotlin
// Pure logic — tested without composition
@Test
fun `applyDigit fills correct slot`() {
    val result = applyDigit("   ", '5', at = 0, length = 3)
    assertEquals("5  ", result.slots)
}
```

Logic extraction patterns and full examples are covered in the `compose-logic-extraction` skill.

---

## Animation Testing

- Prefer asserting **final states** after animation completes — not intermediate frames.
- Use `awaitIdle()` after triggering state changes to let animations settle before asserting.
- For fine-grained clock control on Android, use `mainClock` on `ComposeTestRule`.

```kotlin
// ✅ awaitIdle() — works with runComposeUiTest and createComposeRule
@Test
fun showsResultAfterAnimation() = runComposeUiTest {
    setContent { AnimatedCard(visible = true) }
    awaitIdle()  // waits for all recompositions and animations to settle
    onNodeWithTag("card").assertIsDisplayed()
}

// ✅ Android: fine-grained clock control via createComposeRule
@get:Rule val composeTestRule = createComposeRule()

@Test
fun `card visible after 500ms`() {
    composeTestRule.setContent { AnimatedCard(visible = true) }
    composeTestRule.mainClock.autoAdvance = false
    composeTestRule.mainClock.advanceTimeBy(500)
    composeTestRule.onNodeWithTag("card").assertIsDisplayed()
}
```

Avoid `delay()` or `Thread.sleep()` in tests — use `awaitIdle()` or clock control.

---

## Screenshot Testing

### Determinism Requirements

Screenshot tests must be fully deterministic. Fix all sources of variance:

- Fixed theme (light and dark separately)
- Fixed density and font scale
- Fixed locale
- Deterministic clocks (no real time)
- Fake image loaders — real network images cause flakiness
- Stable test data — no random values
- Test at compact, medium, and expanded widths

```kotlin
@Test
fun `PinInput light snapshot`() {
    paparazzi.snapshot {
        AppTheme(darkTheme = false) {
            PinInput(value = "12  ", onValueChange = {}, format = "####")
        }
    }
}

@Test
fun `PinInput dark snapshot`() {
    paparazzi.snapshot {
        AppTheme(darkTheme = true) {
            PinInput(value = "12  ", onValueChange = {}, format = "####")
        }
    }
}
```

Run screenshot tests in CI. Treat diffs as failures — review before approving.

---

## Previews as Visual Anchors

Every public screen/content component and non-trivial reusable component should have previews. Tiny leaf composables do not always need them.

```kotlin
@Preview(name = "Light") @Preview(name = "Dark", uiMode = UI_MODE_NIGHT_YES)
@Composable
private fun MyComponentPreview() {
    AppTheme {
        MyComponent(state = MyComponentState.preview())
    }
}
```

Define `fun preview(): MyState` on state classes for convenient, reusable preview data.

---

## Adaptive Testing

Test adaptive layouts explicitly — phone-sized tests do not cover all cases:

```kotlin
// Test compact width
composeTestRule.setContent {
    BoxWithConstraints(modifier = Modifier.width(360.dp)) { MyScreen() }
}
// Verify expected adaptive behavior at compact — matches your design system
composeTestRule.onNodeWithTag("bottom_nav").assertIsDisplayed()

// Test expanded width
composeTestRule.setContent {
    BoxWithConstraints(modifier = Modifier.width(1200.dp)) { MyScreen() }
}
// Verify expected adaptive behavior at expanded — matches your design system
composeTestRule.onNodeWithTag("nav_rail").assertIsDisplayed()
```

**Adaptive test checklist:**
- [ ] Compact (360dp) — verify expected navigation and layout for your design system
- [ ] Medium (600–840dp) — verify adaptive layout changes
- [ ] Expanded (840dp+) — verify multi-pane and persistent chrome
- [ ] Portrait and landscape orientations
- [ ] Keyboard navigation — all interactive elements reachable via Tab
- [ ] Focus indicators visible on mouse/trackpad
- [ ] Accessibility at all widths — content descriptions and tap targets remain valid

---

## Determinism

- Do not use real clocks, network, or I/O in composable tests.
- Use `MainCoroutineRule` + `TestCoroutineScheduler` to control time in coroutine-dependent tests.
- `awaitIdle()` waits for all pending recompositions and effects before asserting.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Testing `Screen` with real ViewModel | Test `Content` with fake state and captured callbacks |
| `Thread.sleep()` or `delay()` in tests | Use `awaitIdle()` or controlled test clocks |
| Positional selectors (`onAllNodes()[2]`) | Use semantics: role, text, description, or test tag |
| Testing internal state or composition structure | Test behavior — what the user sees and can do |
| Real network calls or image loading | Inject fakes for all external dependencies |
| Only phone-size tests | Test compact, medium, and expanded widths |
| Only light theme screenshots | Provide both light and dark snapshots |
| Arbitrary screenshot data | Use stable, fixed test data and fake clocks |
