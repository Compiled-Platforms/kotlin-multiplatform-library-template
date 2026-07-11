---
name: compose-performance
description: Compose performance — phases (composition/layout/draw), stability analysis, strong skipping, minimize read scope, lazy lists, allocation discipline, deferred reads, image loading, Baseline Profiles (Android), and profiling. Use when a screen is janky, recompositions are excessive, lists scroll poorly, startup is slow, or you need to audit and measure performance.
disable-model-invocation: true
---

# Compose Performance

## The Core Rule

Compose performance depends on minimizing unnecessary work across composition, layout, draw, and side effects. Skipping helps, but performance also depends on stable state, efficient layout, lazy list behavior, allocation discipline, image loading, and profiling.

**Measure before optimizing.** Speculative `remember`, `derivedStateOf`, or stability annotations without measurement add complexity without guaranteed benefit.

---

## Compose Phases

Every frame runs three phases. Optimize based on where the cost actually occurs — not every problem is recomposition:

| Phase | What happens | Optimization levers |
|---|---|---|
| **Composition** | Building/updating the UI tree — composables execute | Skipping, stability, read scope, `derivedStateOf` |
| **Layout** | Measuring and placing nodes | Avoid intrinsics, reduce nesting, defer reads |
| **Draw** | Rendering pixels | `graphicsLayer`, avoid draw-phase allocations |

---

## Performance Decision Flow

1. **Measure first** — Layout Inspector, Perfetto, Macrobenchmark, or platform profiler.
2. **Identify the phase** — composition (recomposition counts), layout (frame trace), draw (GPU overdraw), startup, scrolling, or image loading.
3. **Fix the largest measured cost.**
4. **Re-measure** to verify the fix.
5. **Do not** make speculative `remember`/`derivedStateOf`/annotation changes without evidence.

---

## Stability Analysis

Use Compose compiler reports to find composables that can't be skipped:

```
freeCompilerArgs += ["-P", "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=/path"]
```

Look for `unstable` parameters in the report.

**Common instability causes:**
- `List`, `Map`, `Set` — not guaranteed immutable; replace with `ImmutableList`/`ImmutableMap`/`ImmutableSet`
- Classes from non-Compose-compiler modules (e.g. domain models) — prefer immutable UI models, stability configuration, or wrappers
- Interfaces — prefer stable concrete UI types unless polymorphism is required; annotate only when the stability contract is true
- `var` properties — make them `val`

**Strong Skipping** (enabled by default since Kotlin/Compose compiler 2.0.20) allows composables to skip even with unstable parameters when no observable change occurred. It does not replace stable models — treat it as a safety net, not a free pass.

---

## Lambda Stability

Avoid repeatedly recreating expensive or identity-sensitive lambdas. With Strong Skipping the compiler can often handle lambda captures automatically — do not add `remember` around every lambda by default. Measure or apply it when lambda identity demonstrably affects child recomposition.

```kotlin
// Usually fine with Strong Skipping — compiler handles it
Button(onClick = { viewModel.submit(item) })

// Explicit stabilization — only when identity matters and is measured to cause recomposition
val onSubmit = remember(item) { { viewModel.submit(item) } }
Button(onClick = onSubmit)
```

---

## Minimize Read Scope

Read state as late and deep in the tree as possible. The composable that reads state is the recomposition scope — moving reads down limits how much recomposes.

```kotlin
// ❌ Entire Column recomposes when count changes
@Composable
fun Screen(state: State) {
    Column {
        Text("Count: ${state.count}")  // state read here — Column recomposes
        HeavyContent()
    }
}

// ✅ Only CountText recomposes
@Composable
fun Screen(state: State) {
    Column {
        CountText(state.count)
        HeavyContent()
    }
}

@Composable
fun CountText(count: Int) {
    Text("Count: $count")
}
```

---

## derivedStateOf

Use `derivedStateOf` when a computed value changes **less frequently** than its inputs. It caches the result and only triggers recomposition when the output actually changes.

```kotlin
// ✅ Only recomposes when isEnabled flips — not on every list/index change
val isEnabled by remember { derivedStateOf { items.isNotEmpty() && selectedIndex >= 0 } }
```

**Do not use `derivedStateOf` for:**
- Trivial or cheap calculations — overhead exceeds benefit
- Values that change as often as their inputs — no caching benefit

---

## Deferred Reads

For rapidly-changing state that affects layout or drawing (e.g. scroll-driven animation), prefer lambda-based modifiers or deferred reads so invalidation happens in the layout or draw phase rather than triggering recomposition:

```kotlin
// ❌ Reading scroll offset in composition — triggers recomposition on every scroll pixel
val offset = scrollState.value.toFloat()
Box(modifier = Modifier.offset(y = offset.dp))

// ✅ Deferred read — invalidates only the draw phase
Box(modifier = Modifier.graphicsLayer { translationY = scrollState.value.toFloat() })
```

---

## Lazy Lists

- Provide stable `key`s when item identity can change, items can be reordered, or item state must be preserved. Index-based keys (the default) cause full recomposition on insert/delete.
- Use `contentType` to help Compose reuse item compositions across different item shapes.
- Avoid creating new object instances inside `items { }` — use `remember` or pre-compute.
- Avoid nested scrollable containers in the same axis.

```kotlin
LazyColumn {
    items(items = list, key = { it.id }, contentType = { it::class }) { item ->
        ItemCard(item)
    }
}
```

---

## Avoiding Allocations in Composition

Avoid repeatedly allocating expensive, stateful, identity-sensitive, or large objects/collections during composition. Prefer `remember`, top-level constants, or precomputed models when allocation is measurable or affects identity. Small local objects that don't affect stability are often fine.

```kotlin
// ❌ New list on every recomposition — identity changes, affects skipping downstream
val items = listOf(Item(id = 1, name = "First"), Item(id = 2, name = "Second"))

// ✅ Created once — stable identity across recompositions
val items = remember { listOf(Item(id = 1, name = "First"), Item(id = 2, name = "Second")) }

// ✅ Better for truly static data — top-level constant
private val DEFAULT_ITEMS = listOf(Item(id = 1, name = "First"), Item(id = 2, name = "Second"))
```

---

## Image Performance

- Use an async image library (Coil, Kamel) — never load images synchronously on the main thread.
- Set explicit `size` on image composables so the library decodes at the correct resolution.
- Avoid `Bitmap` directly in composition — wrap in a `State` and load off-thread.

---

## Expensive Calculations

Move expensive calculations out of the composable body. Where they belong depends on what they depend on:

```kotlin
// ❌ Recalculates on every recomposition
val sorted = items.sortedBy { it.name }

// ✅ Recalculates only when items changes
val sorted = remember(items) { items.sortedBy { it.name } }

// ✅ Use derivedStateOf when the result changes less often than the input
val firstVisible by remember { derivedStateOf { listState.firstVisibleItemIndex } }
```

Calculations that depend on pixel sizes (layout results) belong in `Modifier` measurement or `SubcomposeLayout` — not in composition, where pixel values aren't available.

---

## Android: Baseline Profiles

Baseline Profiles are an Android ART optimization — not KMP-wide. They pre-compile critical code paths so they run as native code from first launch, eliminating JIT warm-up jank that is especially visible in Compose's first composition. Reduces startup time and first-frame jank by 20–40% in typical apps.

### Generate

```kotlin
@RunWith(AndroidJUnit4::class)
class BaselineProfileGenerator {
    @get:Rule val rule = BaselineProfileRule()

    @Test
    fun generate() = rule.collect(packageName = "com.example.app") {
        pressHome()
        startActivityAndWait()
        device.findObject(By.text("Login")).click()
        device.waitForIdle()
    }
}
```

### Apply

```kotlin
// build.gradle.kts
plugins { id("androidx.baselineprofile") }
dependencies { baselineProfile(project(":macrobenchmark")) }
```

- Cover app startup + top 2–3 user journeys
- Regenerate after major refactors or dependency updates
- Use `StartupMode.COLD` for realistic startup measurement
- Ship in release builds only — no effect in debug

---

## Profiling

**Android:**
1. Layout Inspector → Recomposition counts — find hot composables
2. Perfetto / systrace — identify composition/layout/draw phase costs per frame
3. Compose Tracing (`androidx.compose.runtime:runtime-tracing`) — composable names visible in Perfetto traces
4. Macrobenchmark with `FrameTimingMetric` — measure scrolling jank; `StartupTimingMetric` — measure launch time
5. Compose compiler metrics — identify unstable classes before runtime profiling

**Other platforms:**
- **iOS**: Instruments (Time Profiler, SwiftUI template)
- **Desktop (JVM)**: IntelliJ IDEA profiler or Java Flight Recorder
- **Web**: Browser DevTools Performance tab
