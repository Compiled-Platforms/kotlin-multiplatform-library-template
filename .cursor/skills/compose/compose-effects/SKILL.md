---
name: compose-effects
description: Compose side effects — LaunchedEffect, DisposableEffect, SideEffect, produceState, rememberCoroutineScope, rememberUpdatedState, snapshotFlow, effect lifecycle, key selection, and anti-patterns. Use when triggering work tied to composition, managing resources, bridging Compose with coroutines, or choosing the right effect API.
disable-model-invocation: true
---

# Compose Effects

> All Compose effect APIs behave consistently across Compose Multiplatform targets. Platform-specific lifecycle integration belongs outside the effect itself.

---

## Decision Table

| Need | Use |
|---|---|
| Suspend work tied to composition lifetime | `LaunchedEffect` |
| Clean up a resource when composition exits | `DisposableEffect` |
| Push Compose state out to a non-Compose system | `SideEffect` |
| Launch a coroutine from a click or gesture | `rememberCoroutineScope` |
| Convert callback/suspend API into `State` | `produceState` |
| Latest callback/value in effect without restarting | `rememberUpdatedState` |
| Convert snapshot state reads into a `Flow` | `snapshotFlow` |

---

## Effect Lifecycle

Effects follow the composable lifecycle:

1. **Enter composition** → effect starts (coroutine launched, resource registered)
2. **Key changes** → previous effect is cancelled/disposed; effect restarts with new key
3. **Leave composition** → effect is cancelled/disposed

Effects must always be **restart-safe** — re-running with the same key must be idempotent.

---

## Choosing Keys

The key is the most important decision when writing an effect. It determines when the effect restarts.

**Use:**
- Stable identifiers (`userId`, `itemId`)
- Immutable values the effect logically depends on
- `Unit` only when the effect should truly run once per composition entry

**Avoid:**
- Mutable objects or collections whose identity changes unnecessarily
- Values that change on every recomposition (causes effect thrashing)
- Random or timestamp values

Choose the smallest set of values whose change should restart the effect.

```kotlin
// ✅ Restarts only when userId changes
LaunchedEffect(userId) { viewModel.loadUser(userId) }

// ❌ Restarts on every recomposition — unstable key
LaunchedEffect(user.copy()) { viewModel.loadUser(user.id) }
```

---

## LaunchedEffect

Runs a coroutine block when the composable enters composition. Cancels and relaunches when the key changes. Cancels when the composable leaves.

```kotlin
// Run once on first composition
LaunchedEffect(Unit) {
    viewModel.load()
}

// Restart whenever userId changes
LaunchedEffect(userId) {
    viewModel.loadUser(userId)
}
```

---

## DisposableEffect

For non-coroutine resources: listeners, observers, platform registrations. `onDispose` is guaranteed to run on key change or composition exit.

Always clean up fully in `onDispose` — resource leaks from `DisposableEffect` are hard to detect.

```kotlin
// Platform-neutral example — register/unregister any listener
DisposableEffect(eventBus) {
    val subscription = eventBus.subscribe { event -> handleEvent(event) }
    onDispose {
        subscription.cancel()
    }
}
```

---

## SideEffect

Runs synchronously after every successful composition commit to synchronize Compose state with external systems. No key, no coroutine.

Use only to push Compose-managed state into a non-Compose system. Not for async work. Not for one-shot actions.

```kotlin
SideEffect {
    systemUiController.setStatusBarColor(statusBarColor)
}
```

---

## produceState

Converts any async or callback-based source into a `State<T>` readable in composition. Restarts when keys change.

Prefer `collectAsState`/`collectAsStateWithLifecycle` for `Flow` sources. Use `produceState` for callback-based or suspend APIs that aren't already `Flow`.

```kotlin
val image by produceState<Bitmap?>(initialValue = null, url) {
    value = imageLoader.load(url)
}
```

For callback-based APIs, unregister using `awaitDispose`:

```kotlin
val location by produceState<Location?>(null) {
    val callback = LocationCallback { loc -> value = loc }
    locationManager.register(callback)
    awaitDispose { locationManager.unregister(callback) }
}
```

---

## rememberCoroutineScope

Provides a `CoroutineScope` tied to the composable's lifecycle. Use in event handlers — not at composition time.

```kotlin
val scope = rememberCoroutineScope()

Button(onClick = {
    scope.launch { viewModel.submit() }  // ✅ event-driven
})
```

---

## rememberUpdatedState

Provides the latest version of a value to a long-lived effect without restarting the effect. Use when a callback, lambda, or parameter changes but the effect should keep running.

```kotlin
@Composable
fun AutoDismiss(onTimeout: () -> Unit) {
    val currentOnTimeout by rememberUpdatedState(onTimeout)

    LaunchedEffect(Unit) {
        delay(3000)
        currentOnTimeout()  // always calls the most recent lambda, not the one captured at launch
    }
}
```

Prefer `rememberUpdatedState` over adding a frequently-changing value to `LaunchedEffect`'s key when restarting the effect would cause undesirable behavior (e.g. resetting a timer).

---

## snapshotFlow

Converts Compose snapshot state reads into a `Flow`. Use when you need coroutine operators (`debounce`, `mapLatest`, `combine`, etc.) on Compose state.

The reads inside the `snapshotFlow` lambda determine what is observed — when those state values change, the flow emits.

```kotlin
LaunchedEffect(Unit) {
    snapshotFlow { listState.firstVisibleItemIndex }
        .distinctUntilChanged()
        .debounce(150)
        .collect { index -> onVisibleItemChanged(index) }
}
```

---

## Coroutine Cancellation

Effects cancel their coroutines automatically — this is free cleanup. Use the right scope for the right lifetime:

```kotlin
// ✅ LaunchedEffect — cancelled when composable leaves or key changes
LaunchedEffect(id) { repository.sync(id) }

// ✅ rememberCoroutineScope — cancelled when composable leaves, launched from event
val scope = rememberCoroutineScope()
Button(onClick = { scope.launch { viewModel.submit() } })

// ❌ GlobalScope — never cancelled, outlives the composable
GlobalScope.launch { repository.sync(id) }
```

Never pass `GlobalScope` or an application-level scope into a composable.

---

## Anti-patterns

| Anti-pattern | Why it's wrong |
|---|---|
| Business logic inside an effect | Effects synchronize with external systems — logic belongs in ViewModel |
| Repository calls directly from a composable effect | ViewModel is the right boundary; composables shouldn't know about repositories |
| Long-running background work in `LaunchedEffect` | Use a ViewModel coroutine with `viewModelScope` |
| Launching coroutines directly in the composable body | Not an effect scope — use `LaunchedEffect` or an event handler |
| Nesting effects to coordinate behavior | Rethink ownership; effects should be independent |
| `SideEffect` for async work | `SideEffect` is synchronous — use `LaunchedEffect` |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Forgetting `onDispose` in `DisposableEffect` | Always implement it — even if teardown is a no-op |
| Stale callback captured in `LaunchedEffect` | Wrap with `rememberUpdatedState` |
| Adding frequently-changing values as `LaunchedEffect` keys | Use `rememberUpdatedState` for values that shouldn't restart the effect |
| `produceState` used for a `Flow` source | Use `collectAsState` or `collectAsStateWithLifecycle` instead |
| Calling `snapshotFlow` outside a coroutine context | Use inside `LaunchedEffect` or `rememberCoroutineScope` |
