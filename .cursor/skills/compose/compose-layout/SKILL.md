---
name: compose-layout
description: Compose layout system — layout pipeline, constraints, modifiers, alignment, weight, lazy layouts, Grid/FlexBox, custom layouts, layout coordinates, LookaheadScope, adaptive patterns, insets (Android), desktop/pointer input (CMP), Modifier.Node, and common layout mistakes. Use when building or debugging UI structure, implementing adaptive/responsive layouts, working with custom measurement, or working with layout coordinates.
disable-model-invocation: true
---

# Compose Layout

> **Adaptive-first.** Layouts respond to available window size — not device name, platform, or orientation assumption.

---

## Adaptive Layout Philosophy

Design every layout to work across compact, medium, and expanded widths from the start. Adaptive is the baseline.

- Never assume a fixed screen size, orientation, or input method.
- Layouts respond to available window constraints — not device name or platform.
- Never trigger completely different screen hierarchies just because the window resized — prefer adaptive layouts over device-specific branches.
- Test on compact (360dp), medium (600dp), and expanded (840dp+) width classes.
- Handle all input types: touch, keyboard, mouse, trackpad, stylus.

Adaptive layouts often use list-detail, supporting-pane, and multi-pane navigation patterns. Navigation-specific implementation belongs in the navigation layer.

---

## Layout Pipeline

Compose layout runs in three phases per frame:

1. **Composition** — what to show (composable tree built/updated)
2. **Layout** — where to place and how to size each node (single-pass constraints)
3. **Drawing** — painting each node

Each node is measured **once** with incoming constraints (min/max width + height). It must report its own size, then place its children. There is no second measurement pass in the standard pipeline — intrinsic measurement is the exception (see below).

---

## Constraints

Constraints define the bounds a parent proposes to a child. The full layout contract is:

1. **Parent proposes** — passes `Constraints(minWidth, maxWidth, minHeight, maxHeight)` to each child.
2. **Child chooses** — picks any size within those constraints and reports it.
3. **Parent places** — positions the child at an offset within its own bounds.

```kotlin
// Constraints carry four values:
// constraints.minWidth  — child must be at least this wide
// constraints.maxWidth  — child cannot exceed this width
// constraints.minHeight
// constraints.maxHeight
```

Common constraint modifiers:
- `fillMaxSize()` — sets min = max = parent size (forces child to fill)
- `wrapContentSize()` — removes min constraints (lets child be as small as it wants)
- `requiredSize()` — breaks the contract and forces a size regardless of parent constraints; use sparingly

---

## Modifier Ordering

Modifiers are applied sequentially, each wrapping the node from outside in. Order changes behavior:

```kotlin
Modifier
    .size(48.dp)          // 1. constrain size
    .padding(8.dp)        // 2. space inside the size constraint
    .background(color)    // 3. fill background within padded area
    .clickable { }        // 4. interaction on the shaped area
```

**Typical ordering:** size/layout → padding → background/border → interaction → drawing.

There is no single universally correct order — behavior drives order. Swapping `padding` and `background` changes whether the background fills the padded area or includes the padding.

---

## Column, Row, Box

- `Column` + `Row`: `Arrangement` controls spacing along the main axis. `Alignment` controls cross-axis alignment.
- `Arrangement.spacedBy(dp)` is preferred over manual `Spacer` calls between items.
- `Box` stacks children. Use `contentAlignment` for default alignment, or `Modifier.align()` per child.

---

## Weight and Alignment

`Modifier.weight(n)` in a `Row`/`Column` distributes remaining space proportionally after all non-weighted children are measured first.

```kotlin
Row {
    Icon(...)                                        // fixed size — measured first
    Text("Label", modifier = Modifier.weight(1f))  // fills remaining space
}
```

`Modifier.alignBy(alignmentLine)` aligns children along a shared alignment line (e.g. text baseline) across a `Row`.

---

## Lazy Layouts

- `LazyColumn`/`LazyRow` only compose and measure visible items — never use `Column` with `forEach` for long lists.
- Provide a stable `key` when item identity can change, items can reorder, or item state must be preserved.
- Use `contentPadding` for padding around list content — not `Modifier.padding` on the container.
- Avoid `fillMaxSize()` inside lazy item content without a height constraint — causes infinite measurement.

```kotlin
LazyColumn(contentPadding = PaddingValues(16.dp)) {
    items(items = list, key = { it.id }) { item ->
        ItemRow(item)
    }
}
```

---

## Grid and FlexBox (Compose 1.11+)

**When to use Grid over Row/Column:**
- 2D layouts (rows and columns simultaneously)
- Adaptive column counts that fill available width
- Masonry / staggered item placement

**Grid variants:**
- `LazyVerticalGrid` / `LazyHorizontalGrid` — lazy, for large item counts
- `VerticalGrid` / `HorizontalGrid` — non-lazy, for small fixed sets
- `LazyVerticalStaggeredGrid` — masonry layout with variable item heights

```kotlin
// Adaptive columns — fills available width with columns of at least 160dp
LazyVerticalGrid(
    columns = GridCells.Adaptive(minSize = 160.dp),
) {
    items(items, key = { it.id }) { ItemCard(it) }
}

// Fixed column count
LazyVerticalGrid(columns = GridCells.Fixed(3)) { ... }
```

**FlexBox** — CSS Flexbox-inspired 1D layout with wrapping, grow, shrink, and basis control. Use when `Row`/`Column` with `weight` isn't expressive enough, or when items must wrap onto multiple lines.

---

## Custom Layouts

Use `Layout` when standard layouts can't express the measurement/placement logic. The core of `Layout` is a `MeasurePolicy`:

```kotlin
Layout(
    content = { /* children */ },
    measurePolicy = { measurables, constraints ->
        val placeables = measurables.map { it.measure(constraints) }
        val width = placeables.maxOf { it.width }
        val height = placeables.sumOf { it.height }
        layout(width, height) {
            var y = 0
            placeables.forEach { placeable ->
                placeable.placeRelative(x = 0, y = y)
                y += placeable.height
            }
        }
    }
)
```

`MeasurePolicy` is the interface that `Column`, `Row`, `Box`, and every other built-in layout implements.

Use `SubcomposeLayout` when children must be measured in multiple passes (e.g. measuring one child to determine the size available for another).

---

## Intrinsic Measurements

Intrinsic measurements answer "how large would this child want to be in an unconstrained direction?" They exist to solve specific cross-axis sizing problems, such as making all items in a `Row` the same height.

```kotlin
// Make all Row children the same height as the tallest
Row(modifier = Modifier.height(IntrinsicSize.Max)) {
    LeftContent(modifier = Modifier.fillMaxHeight())
    Divider(modifier = Modifier.fillMaxHeight().width(1.dp))
    RightContent(modifier = Modifier.fillMaxHeight())
}
```

| API | Meaning |
|---|---|
| `IntrinsicSize.Min` | Smallest size the child can be without clipping |
| `IntrinsicSize.Max` | Largest size the child wants at its natural proportions |

**Cost:** Intrinsic measurement triggers an extra measurement pass. Use only when the layout problem genuinely requires it.

---

## Alignment Lines

Alignment lines let children in a `Row` or `Column` align on a semantic axis rather than a geometric edge.

```kotlin
// Align text baselines across a Row
Row(verticalAlignment = Alignment.CenterVertically) {
    Text("Label", modifier = Modifier.alignByBaseline())
    Text("Value", fontSize = 24.sp, modifier = Modifier.alignByBaseline())
}
```

Custom alignment lines can be defined for non-text layouts:

```kotlin
val IconTopLine = HorizontalAlignmentLine(merger = { old, new -> minOf(old, new) })
```

---

## Layout Coordinates

`LayoutCoordinates` provides position information after layout. Access it via `onGloballyPositioned`:

```kotlin
Box(
    modifier = Modifier.onGloballyPositioned { coordinates ->
        // coordinates.size — size in pixels
        // coordinates.positionInParent() — offset from parent
        // coordinates.positionInRoot() — offset from root composable
        // coordinates.positionInWindow() — offset from window origin
        // coordinates.boundsInRoot() — Rect in root coordinates
        val positionInWindow = coordinates.positionInWindow()
    }
)
```

`onGloballyPositioned` runs after the layout phase. Do not read `LayoutCoordinates` during composition — the values are not yet available.

---

## LookaheadScope

`LookaheadScope` allows Compose to measure children with a lookahead pass — computing their final position before an animation or transition completes. This enables smooth layout-driven animations where items move to their destination positions while content is still changing.

> **Note:** `LookaheadScope` and related APIs (`animateBounds`, `Modifier.approachLayout`) are experimental and subject to change. For shared element transitions between screens, use `SharedTransitionLayout` instead — it uses `LookaheadScope` internally and has a stable API.

```kotlin
// Shared element transitions — stable API, uses LookaheadScope internally
SharedTransitionLayout {
    AnimatedContent(targetState = selected) { item ->
        if (item == null) {
            ListItem(
                modifier = Modifier.sharedElement(
                    rememberSharedContentState(key = "card"),
                    animatedVisibilityScope = this,
                )
            )
        } else {
            DetailView(
                modifier = Modifier.sharedElement(
                    rememberSharedContentState(key = "card"),
                    animatedVisibilityScope = this,
                )
            )
        }
    }
}
```

Use `LookaheadScope` directly only when building custom animated layout transitions that require lookahead measurement and `SharedTransitionLayout` doesn't cover the use case.

---

## Adaptive Patterns (Common Compose)

Use `BoxWithConstraints` to get the available width as a `Dp` value in `commonMain` — no Android dependencies required:

```kotlin
BoxWithConstraints {
    val windowWidth = maxWidth  // available width for this layout
    // ...
}
```

### List-Detail
Show list and detail side-by-side at medium/expanded, stacked at compact:

```kotlin
BoxWithConstraints {
    val windowWidth = maxWidth
    if (windowWidth < 600.dp) {
        if (selectedItem == null) ListPane() else DetailPane()
    } else {
        Row {
            ListPane(modifier = Modifier.weight(1f))
            DetailPane(modifier = Modifier.weight(2f))
        }
    }
}
```

### Supporting Pane
Primary content + contextual sidebar at expanded width:

```kotlin
BoxWithConstraints {
    Row {
        PrimaryContent(modifier = Modifier.weight(1f))
        if (maxWidth >= 840.dp) {
            SupportingPane(modifier = Modifier.width(320.dp))
        }
    }
}
```

These patterns use `BoxWithConstraints.maxWidth` — a plain `Dp` value — rather than Android-specific `WindowSizeClass`, so they work in `commonMain`.

---

## Android: Window Size and Foldables

> These APIs are Android-specific. Use in `androidMain` or behind `expect`/`actual`.

**WindowSizeClass** classifies the available window into compact / medium / expanded for screen-level layout decisions:

```kotlin
val windowSizeClass = calculateWindowSizeClass(activity)
when (windowSizeClass.widthSizeClass) {
    WindowWidthSizeClass.Compact -> SinglePaneLayout()
    WindowWidthSizeClass.Medium  -> AdaptiveLayout()
    WindowWidthSizeClass.Expanded -> TwoPaneLayout()
}
```

**Foldables:** Layouts must respect hinge regions. Interactive content should not be placed over the fold hinge. Implementation — `WindowInfoTracker`, `FoldingFeature`, fold state observation — belongs in the platform layer (`androidMain`); see the KMP skill for details.

---

## Android: Edge-to-Edge and WindowInsets

> Android-specific. Call `enableEdgeToEdge()` in every Android `Activity`.

Content draws behind system bars on Android 15+. Handle insets or content will be obscured.

**With Scaffold:**
```kotlin
Scaffold { innerPadding ->
    LazyColumn(contentPadding = innerPadding) { ... }
}
```
Never ignore `innerPadding` from `Scaffold`.

**Without Scaffold:**
```kotlin
Modifier.windowInsetsPadding(WindowInsets.safeDrawing)  // status + nav + cutout
Modifier.windowInsetsPadding(WindowInsets.safeContent)  // safeDrawing + IME
Modifier.imePadding()                                    // keyboard only
```

| Insets | Protects |
|---|---|
| `safeDrawing` | System bars + display cutout |
| `safeContent` | `safeDrawing` + IME |
| `ime` | Soft keyboard |
| `navigationBars` | Navigation bar only |

Insets are consumed as applied — use `Modifier.consumeWindowInsets(padding)` to prevent double-application. In `commonMain` components, accept a `PaddingValues` parameter so callers handle insets per platform.

---

## Desktop and Pointer Input (CMP)

- Mouse/trackpad users expect hover states, right-click menus, and cursor changes.
- Keyboard users expect full navigation, visible focus indicators, and standard shortcuts.
- Window resizing is continuous — layouts must reflow smoothly without triggering different screen hierarchies.
- Scrollbars are expected for scrollable content on desktop.

```kotlin
Box {
    Column(modifier = Modifier.verticalScroll(scrollState)) { ... }
    VerticalScrollbar(
        adapter = rememberScrollbarAdapter(scrollState),
        modifier = Modifier.align(Alignment.CenterEnd),
    )
}
```

**Pointer type detection:**
```kotlin
Modifier.pointerInput(Unit) {
    awaitPointerEventScope {
        val event = awaitPointerEvent()
        val isPrecise = event.changes.first().type == PointerType.Mouse
    }
}
```

---

## Custom Modifiers — Modifier.Node

`Modifier.composed` is deprecated. Use `Modifier.Node` for custom stateful modifiers:

```kotlin
private class MyBorderNode(var color: Color) : DrawModifierNode, Modifier.Node() {
    override fun ContentDrawScope.draw() {
        drawContent()
        drawRect(color = color, style = Stroke(width = 2.dp.toPx()))
    }
}

private data class MyBorderElement(val color: Color) : ModifierNodeElement<MyBorderNode>() {
    override fun create() = MyBorderNode(color)
    override fun update(node: MyBorderNode) { node.color = color }
}

fun Modifier.myBorder(color: Color): Modifier = this then MyBorderElement(color)
```

| Node interface | Purpose |
|---|---|
| `DrawModifierNode` | Custom drawing |
| `LayoutModifierNode` | Custom measurement/placement |
| `PointerInputModifierNode` | Pointer/touch input |
| `SemanticsModifierNode` | Accessibility semantics |
| `CompositionLocalConsumerModifierNode` | Read `CompositionLocal` from a node |

For simple, stateless modifier wrappers, a plain extension function is still fine.

---

## Common Layout Mistakes

| Mistake | Fix |
|---|---|
| Nested `LazyColumn` inside `LazyColumn` (same axis) | Use `items` with sections, or `LazyListScope` headers |
| Unnecessary `Box` wrappers around single children | Use `Column`/`Row` directly or a `Modifier` |
| `fillMaxSize()` everywhere — even in lazy item content | Use `fillMaxWidth()` for items; `fillMaxSize()` only at screen level |
| `weight` for fixed-size children | `weight` is for distributing remaining space — use explicit sizes for fixed children |
| Hardcoded screen widths (e.g. `Modifier.width(360.dp)`) | Use `fillMaxWidth()`, `weight`, or `BoxWithConstraints` |
| Reading layout coordinates during composition | Use `onGloballyPositioned` — coordinates aren't available until after layout |
| Branching on device name/model | Branch on available window size or pointer type instead |
| Intrinsic measurement by default | Only use when cross-axis sizing genuinely requires it — it adds a measurement pass |
| Ignoring `innerPadding` from `Scaffold` | Always propagate it — content hides behind system bars otherwise |
