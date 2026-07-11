---
name: compose-animation
description: Compose animations — core principle, choosing the right API, animate*AsState, AnimatedVisibility, AnimatedContent, animateContentSize, updateTransition, Animatable, shared element transitions, animation specs, motion tokens, KMP boundaries, predictive back (Android), accessibility/reduced motion, and common mistakes. Use when adding motion, building transitions between states, animating layout changes, or implementing gesture-driven animation.
disable-model-invocation: true
---

# Compose Animation

## Core Principle

Animation is a visual response to state changes.

- **Business state drives animation** — animation state must never become the source of truth.
- **Do not start animations directly during composition** — use state-driven APIs or effects.
- **Motion should clarify state changes**, not decorate everything.
- Keep animations short, purposeful, and interruptible where the user expects it.

---

## Compose Multiplatform Notes

Prefer shared animation APIs in `commonMain`:
- `animate*AsState`, `AnimatedVisibility`, `AnimatedContent`, `updateTransition`
- `Animatable`, `rememberInfiniteTransition`, `animateContentSize`
- `SharedTransitionLayout` + `sharedElement` (verify support per target before use)

Platform-specific transitions, back gestures, window animations, and navigation-integrated transitions belong in platform source sets. Verify shared-element and navigation-transition support for each CMP target before using in shared code.

---

## Choosing the Right API

| Situation | API |
|---|---|
| Animate a single value when state changes | `animate*AsState` |
| Show/hide content with animation | `AnimatedVisibility` |
| Animate between different content | `AnimatedContent` |
| Simple size change from content change | `Modifier.animateContentSize()` |
| Coordinate multiple animations together | `updateTransition` |
| Continuous/infinite animation | `rememberInfiniteTransition` |
| Interruptible, gesture-driven, or coroutine-controlled | `Animatable` |
| Physics decay / fling | `Animatable.animateDecay()` |
| Shared element between screens or layouts | `SharedTransitionLayout` + `sharedElement` |
| Shared bounds / container transform | `SharedTransitionLayout` + `sharedBounds` |
| Draw-only transform (no layout cost) | `Modifier.graphicsLayer` + animated value |

---

## animate*AsState

The simplest API — animates a value whenever the target changes:

```kotlin
val alpha by animateFloatAsState(
    targetValue = if (visible) 1f else 0f,
    animationSpec = tween(durationMillis = 300),
    label = "alpha",
)
Box(modifier = Modifier.alpha(alpha))
```

Always provide a `label` for tooling visibility. Variants: `animateFloatAsState`, `animateDpAsState`, `animateColorAsState`, `animateIntAsState`, `animateSizeAsState`, `animateOffsetAsState`.

---

## AnimatedVisibility

Animates entering and exiting content from the composition:

```kotlin
AnimatedVisibility(
    visible = showBanner,
    enter = fadeIn() + slideInVertically { -it },
    exit = fadeOut() + slideOutVertically { -it },
) {
    Banner()
}
```

Children can use `Modifier.animateEnterExit()` for independent enter/exit animations within the parent's animation.

---

## AnimatedContent

Animates transitions between different content for the same slot:

```kotlin
AnimatedContent(
    targetState = count,
    transitionSpec = {
        if (targetState > initialState) {
            slideInVertically { it } togetherWith slideOutVertically { -it }
        } else {
            slideInVertically { -it } togetherWith slideOutVertically { it }
        }
    },
    label = "counter",
) { value ->
    Text("$value")
}
```

- `targetState` identity controls when content changes.
- Use `contentKey` when multiple target states should map to the same animated content identity (avoids unnecessary re-animation).
- Use `SizeTransform` intentionally — size animation triggers layout work.

---

## animateContentSize

Use `Modifier.animateContentSize()` for simple size changes caused by content changing:

```kotlin
Column(modifier = Modifier.animateContentSize()) {
    Text(if (expanded) longText else shortText)
}
```

Avoid it for complex parent/child choreography — use explicit transitions, `AnimatedContent`, or layout-aware animation instead.

---

## rememberInfiniteTransition

For continuous looping animations (pulsing, shimmer, loading indicators):

```kotlin
val infiniteTransition = rememberInfiniteTransition(label = "shimmer")
val alpha by infiniteTransition.animateFloat(
    initialValue = 0.3f,
    targetValue = 1f,
    animationSpec = infiniteRepeatable(
        animation = tween(800, easing = FastOutSlowInEasing),
        repeatMode = RepeatMode.Reverse,
    ),
    label = "shimmer_alpha",
)
```

Use sparingly — continuous animation consumes battery and draw budget even when the user is not interacting.

---

## updateTransition

Coordinates multiple animations that change together in response to the same state:

```kotlin
val transition = updateTransition(selected, label = "card")
val borderWidth by transition.animateDp(label = "border") { if (it) 4.dp else 1.dp }
val backgroundColor by transition.animateColor(label = "bg") {
    if (it) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface
}
```

---

## Animation Specs

Use app or Material motion tokens for durations and easing — avoid arbitrary hardcoded values unless the motion is intentionally custom.

| Spec | Use for |
|---|---|
| `tween(duration, easing)` | Time-based, predictable |
| `spring(dampingRatio, stiffness)` | Physics-based, natural feel |
| `keyframes { }` | Multi-step value changes |
| `snap()` | Immediate, no animation |

```kotlin
// Physics spring — good for gesture-response UI
animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy, stiffness = Spring.StiffnessMedium)

// Time-based ease with standard Material easing
animationSpec = tween(300, easing = FastOutSlowInEasing)

// Material motion token (M3 Expressive) — preferred for consistent system motion
val spec = MaterialTheme.motionScheme.defaultSpatialSpec<Dp>()
```

When not using M3 Expressive tokens, prefer named `Spring` and `Easing` constants (`Spring.StiffnessMedium`, `FastOutSlowInEasing`, etc.) over magic numbers.

---

## Animatable

Use `Animatable` when animation needs to be interruptible, gesture-driven, coroutine-controlled, velocity-aware, or snapped/stopped/decayed:

```kotlin
val offset = remember { Animatable(0f) }

// In gesture handler:
offset.snapTo(newValue)                 // instant snap during drag
offset.animateTo(0f, spring())          // physics spring on release
offset.animateDecay(velocity, decay())  // fling with decay
offset.stop()                           // interrupt at any point
```

Key APIs: `snapTo`, `animateTo`, `animateDecay`, `stop`, `updateBounds`.

Use `pointerInput` with `detectDragGestures` for drag interactions that feed into `Animatable`.

---

## Shared Element Transitions

`SharedTransitionLayout` provides a `SharedTransitionScope` that matches content by key across `AnimatedContent` or navigation transitions:

```kotlin
SharedTransitionLayout {
    AnimatedContent(targetState = selected) { item ->
        if (item == null) {
            ListItem(
                modifier = Modifier.sharedElement(
                    rememberSharedContentState(key = "card"),  // stable identity key
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

- Use `sharedBounds` for container/bounds transforms; `sharedElement` for exact content matching.
- Use stable keys that represent shared identity — unstable keys break the transition.
- Verify support for each Compose Multiplatform target before using in `commonMain`.

---

## Android: Predictive Back

> **Android-specific.** Use in `androidMain` only. Do not use `BackHandler`, `PredictiveBackHandler`, or `BackEventCompat` in `commonMain`.

Android 14+ supports a predictive back gesture with live preview. Navigation 3 and Material3 components (`ModalBottomSheet`, `ModalNavigationDrawer`) handle predictive back automatically.

### PredictiveBackHandler (custom animation)
```kotlin
PredictiveBackHandler(enabled = showDetail) { progress: Flow<BackEventCompat> ->
    try {
        progress.collect { backEvent ->
            animationProgress = backEvent.progress  // 0f → 1f as user swipes
        }
        showDetail = false
        animationProgress = 0f
    } catch (e: CancellationException) {
        animationProgress = 0f  // user cancelled — snap back
    }
}
```

Do not use `BackHandler` and `PredictiveBackHandler` on the same composable — `PredictiveBackHandler` supersedes it.

---

## Accessibility

- Avoid flashing, excessive motion, or motion that blocks reading or comprehension.
- Provide non-motion cues for important state changes — don't rely on animation alone to communicate meaning.
- Keep animations short. Decorative animations should be skippable or avoidable.
- **Android:** Respect the user's animation scale setting. Check `Settings.Global.TRANSITION_ANIMATION_SCALE` in `androidMain` and skip or shorten animations when it is `0f`.

---

## Performance

- Use `Modifier.graphicsLayer { }` for opacity, scale, and rotation — it avoids triggering layout.
- Avoid animating properties that trigger layout (size, padding) on every frame — prefer draw-phase transforms.
- `AnimatedVisibility` keeps content in the composition during exit — it is still measured and drawn until the animation completes.
- For low-level custom animation systems, `TargetBasedAnimation` and `Animation` are available but rarely needed — prefer higher-level APIs.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Animation state becomes the source of truth | Business state drives animation — not the other way around |
| Launching animation during composition | Use state-driven APIs (`animate*AsState`) or effects |
| Hardcoded arbitrary durations | Use motion tokens or standard `AnimationSpec` constants |
| Animating size/padding on every frame | Prefer `graphicsLayer` draw transforms when layout isn't needed |
| `AnimatedContent` for simple show/hide | Use `AnimatedVisibility` |
| Shared element with unstable or changing keys | Use stable identity keys |
| `PredictiveBackHandler` in `commonMain` | Android-only — move to `androidMain` |
| `animateContentSize` for complex choreography | Use `AnimatedContent` or explicit transitions |
