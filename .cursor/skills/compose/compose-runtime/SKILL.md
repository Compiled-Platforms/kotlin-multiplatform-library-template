---
name: compose-runtime
description: Deep knowledge of the Compose runtime — composition, recomposition, restart groups, stability, strong skipping, snapshot state, and debugging. Use when optimizing recomposition, debugging unexpected redraws, understanding why a composable re-executes, or working with snapshot state internals.
disable-model-invocation: true
---

# Compose Runtime

## Composable Execution Model
Composable functions must be **fast, idempotent, and side-effect free**.

Do not rely on composable execution for required behavior — recomposition may be:
- **Skipped** entirely when inputs are stable and unchanged
- **Canceled** mid-execution and restarted if state changes during composition
- **Run frequently** — more often than expected
- **Run in a different order** than declared
- **Run in parallel** in future runtime versions

Any work that must happen exactly once, has observable side effects, or depends on execution order belongs in an effect (`LaunchedEffect`, `DisposableEffect`) or a ViewModel — not directly in the composable body.

---

## Composition and the Slot Table
- The Compose runtime maintains a slot table: a linear structure that stores composition groups, remembered values, keys, node metadata, and other information needed to preserve identity across recompositions.
- On initial composition, the runtime records composition groups, remembered values, keys, and node metadata in the slot table so future recompositions can preserve identity and efficiently update only what changed.
- On recomposition, Compose determines whether each composable needs to re-execute based on parameter changes and stability analysis.

## Restart Groups
The Compose compiler inserts **restart groups** around composable scopes. These groups define where recomposition can restart and where skipping can occur. When state changes, Compose re-executes the smallest restart group that contains the state read — not the entire composition tree.

## Recomposition and Skipping
Skipping depends on compiler-generated stability analysis and parameter change detection. Stable parameters may be compared for change; unstable parameters generally prevent normal skipping unless strong skipping applies.

A composable can be skipped when:
- All parameters are determined to be stable, AND
- None of the stable parameters have changed since the last composition

**Strong Skipping:** Modern Compose uses strong skipping more aggressively, allowing composables to be skipped even when they have unstable parameters under certain conditions. Strong skipping improves recomposition behavior but does not replace immutable UI state, stable models, or proper state ownership.

## Stability
A type is stable when Compose can safely determine whether it has changed. Stable types expose stable public properties, provide meaningful equality, and ensure observable state changes notify the runtime.

Stability is inferred by the Compose compiler whenever possible. `@Immutable` and `@Stable` should only be used when the compiler cannot correctly infer the contract.

**Stable by default:**
- Primitive types (`Int`, `Boolean`, `String`, etc.)
- Lambda values — generally treated as stable, but lambda captures can still affect recomposition behavior. Avoid recreating expensive or identity-sensitive lambdas unnecessarily.
- `@Immutable` and `@Stable` annotated classes
- Classes where all public properties are stable and `val`

**Unstable by default:**
- Classes from modules not compiled with the Compose compiler plugin
- Classes with `var` properties
- Kotlin read-only collection interfaces (`List`, `Map`, `Set`) — not guaranteed immutable, so Compose treats them conservatively. Use `ImmutableList` etc. from `kotlinx.collections.immutable`.
- Interfaces — generally treated as unstable unless Compose can prove stability or the interface is explicitly annotated.

```kotlin
// ❌ Unstable — List is not guaranteed immutable
data class UiState(val items: List<Item>)

// ✅ Stable — ImmutableList guarantees immutability
@Immutable
data class UiState(val items: ImmutableList<Item>)
```

## @Immutable vs @Stable
| Annotation | Guarantee | Use when |
|---|---|---|
| `@Immutable` | All public properties are `val` and themselves immutable; object never changes after construction | Data classes used as UI state |
| `@Stable` | The type satisfies the Compose stability contract: observable state changes are visible to Compose, allowing correct recomposition. | Types with observable mutable state whose stability cannot be inferred automatically. |

**AVOID:** Using `@Stable` to silence recomposition warnings without understanding the actual stability contract.

## Strong Skipping
Strong skipping is enabled by default starting with Kotlin 2.0.20 / Compose compiler 2.0.20. It allows composables to be skipped even with unstable parameters when the runtime determines no observable change occurred. Strong skipping is a compiler/runtime optimization — not a guarantee that unstable types are "free." Rely on it as a safety net, not as a reason to skip proper stability work.

## State Read Tracking
Compose tracks snapshot state reads automatically. The **location** of a state read determines the recomposition scope — the restart group that contains the read is what gets re-executed when the state changes.

```kotlin
// ❌ Reads count at Column level — entire Column recomposes
@Composable
fun Counter(state: CounterState) {
    Column {
        Text("Count: ${state.count}")  // state.count read here — Column recomposes
        HeavyContent()
    }
}

// ✅ Move the read into a child — only CountText recomposes
@Composable
fun Counter(state: CounterState) {
    Column {
        CountText(state.count)  // read moved down
        HeavyContent()          // unaffected
    }
}

@Composable
fun CountText(count: Int) {
    Text("Count: $count")
}
```

Read frequently changing state as deep in the tree as practical. Avoid reading state in parent layout containers when only a child depends on it.

## Snapshot State
- `mutableStateOf`, `mutableStateListOf`, and `mutableStateMapOf` are snapshot-aware — reads inside composables are automatically tracked.
- Writes to snapshot state are applied atomically. Compose snapshots provide MVCC (multi-version concurrency control), allowing readers and writers to operate on isolated snapshots before changes are atomically applied — this is why snapshot reads and writes don't interfere with each other across threads.
- `snapshotFlow { }` converts snapshot state reads into a `Flow` — useful for bridging Compose state to non-Compose code.

```kotlin
// Bridge snapshot state to a Flow
val flow = snapshotFlow { myState.value }
    .distinctUntilChanged()
```

### Snapshot APIs for non-Compose code
When reading or writing snapshot state outside of composition (e.g. in a ViewModel, repository, or test), use the snapshot APIs directly:

```kotlin
// Read snapshot state outside composition — takes an isolated snapshot
val snapshot = Snapshot.takeSnapshot()
val value = snapshot.enter { myState.value }
snapshot.dispose()

// Write snapshot state outside composition — applies changes atomically
Snapshot.withMutableSnapshot {
    myState.value = newValue
    otherState.value = otherValue
    // Both writes are applied atomically when the block exits
}
```

`Snapshot.withMutableSnapshot` is the correct way to batch multiple state writes in non-Compose code. Without it, each write triggers a separate snapshot notification — which can cause redundant recompositions.

## Skippability Guidelines
- Prefer stable concrete parameter types over interfaces.
- Avoid identity-sensitive or repeatedly recreated lambdas in composable parameters.
- Avoid unstable collection types (`List`, `Map`, `Set`) in public composable parameters.
- Use compiler stability reports to verify stability rather than guessing.

## Debugging Recomposition
Use these tools to verify recomposition behavior:
- **Compose compiler stability reports** — identifies unstable parameters causing skipping to fail.
- **Layout Inspector recomposition counters** — shows how many times each composable recomposed in Android Studio.
- **Recomposition Highlighter** — visual overlay in Layout Inspector that highlights composables by recomposition frequency.
- **Compose Tracing** — adds Compose-specific trace sections for systrace/Perfetto, showing exactly which composables execute during a frame.
- **Macrobenchmark** — when performance investigation extends beyond recomposition into frame timing and jank.

Never guess at recomposition behavior — measure it.
