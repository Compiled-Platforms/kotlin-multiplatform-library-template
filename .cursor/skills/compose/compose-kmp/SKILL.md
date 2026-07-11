---
name: compose-kmp
description: Compose Multiplatform KMP — source set boundaries, commonMain API rules, expect/actual vs interface patterns, resources, lifecycle, typed navigation, platform interop, adaptive differences, version alignment, and testing in KMP. Use when building shared Compose UI, wiring platform APIs, handling lifecycle in KMP, setting up navigation, or determining what belongs in each source set.
disable-model-invocation: true
---

# Compose KMP

## What Belongs in commonMain

`commonMain` may use Compose Multiplatform-supported APIs, including:
- `org.jetbrains.compose.*`
- `org.jetbrains.androidx.*` (lifecycle, navigation, adaptive, resources)
- Supported `androidx.compose.*` and `androidx.navigation.*` APIs documented for common code

**Never in commonMain — platform SDK APIs:**
- Android: `android.*`, `Context`, `Activity`, `Intent`, `LocalContext`, platform resource IDs (`R.*`)
- iOS/macOS: `UIViewController`, `UIView`, UIKit, AppKit, or any platform framework type
- Desktop: `java.awt.*`, Swing, AWT
- Any API that requires a platform runtime to instantiate

When in doubt: if the API requires a platform context, device, or runtime to work, it does not belong in `commonMain`.

---

## Source Set Boundaries

| Source set | What belongs here |
|---|---|
| `commonMain` | Shared UI, state models, typed routes, interfaces, resources, portable logic |
| `androidMain` | Android SDK, `Activity`, `Context`, permissions, CameraX, Bluetooth, notifications |
| `iosMain` | UIKit/Swift interop, `UIViewController`, iOS permissions, iOS-specific APIs |
| `desktopMain` | Window/menu bar/tray integration, file dialogs, desktop-specific shortcuts |
| `wasmJsMain` / `jsMain` | Browser APIs, DOM interop, web-specific resource/loading behavior |

When a feature requires different implementations per platform, define the interface in `commonMain` and implement it in each platform source set.

---

## expect / actual vs Interface

Both patterns isolate platform behavior. Choose based on the situation:

**Use injected interfaces when:**
- The service has runtime dependencies (Context, permissions)
- You need test fakes
- The service integrates with dependency injection
- The platform implementation has significant setup

**Use `expect`/`actual` when:**
- The difference is a small, stateless platform fact
- No DI is involved and no test fake is needed
- A simple function or constant differs per platform

```kotlin
// expect/actual — simple platform fact
expect fun currentTimeMillis(): Long

// Interface — service with DI and platform runtime dependencies
// commonMain
interface PlatformCamera {
    suspend fun capturePhoto(): ByteArray
}

// androidMain — injected via Koin/Hilt, requires CameraX and Context
class AndroidCamera(private val context: Context) : PlatformCamera { ... }
```

Keep `expect` surfaces minimal. Shared logic lives above the boundary; platform detail lives below it.

---

## Resources

Use `composeResources` for all shared assets:

```kotlin
Text(stringResource(Res.string.app_name))
Image(painterResource(Res.drawable.logo), contentDescription = null)
val font = FontFamily(Font(Res.font.inter_regular))
```

- Never access `R.string`, `R.drawable`, or Android resource IDs from `commonMain`.
- Keep all resource access in shared UI through the generated `Res` object.
- Platform resource systems belong in platform source sets.
- **Web caveat:** `painterResource()` is synchronous on most targets, but on Web (Wasm/JS) resources may load asynchronously and initially return an empty painter. Verify image display behavior when targeting Web.

---

## Lifecycle in KMP

Use the KMP-compatible lifecycle artifacts from `org.jetbrains.androidx.lifecycle`:

```kotlin
// ✅ Use KMP-compatible lifecycle imports in commonMain
val lifecycleOwner = LocalLifecycleOwner.current

// Collect flows using the platform-appropriate lifecycle-aware API
// collectAsStateWithLifecycle() is available where the KMP lifecycle artifact supports it
val state by viewModel.state.collectAsStateWithLifecycle()
```

- Do not use Android-only lifecycle APIs (`androidx.lifecycle.Lifecycle`) in `commonMain`.
- Collect flows using the platform-appropriate lifecycle-aware API. If `collectAsStateWithLifecycle()` is not available for a target, fall back to `collectAsState()`.
- Platform-specific lifecycle hooks (`onStart`, `onStop`, `onResume`) belong in platform wiring (`androidMain`/`iosMain`), not shared composables.

---

## Navigation

Use Compose Navigation for KMP with **serializable typed routes**. Requires `androidx.navigation:navigation-compose` with KMP support:

```kotlin
// ✅ Modern typed routes — @Serializable objects and data classes
@Serializable
object Home

@Serializable
data class Detail(val id: String)

// commonMain — NavController from rememberNavController()
NavHost(navController = rememberNavController(), startDestination = Home) {
    composable<Home> { HomeScreen() }
    composable<Detail> { backStackEntry ->
        val detail: Detail = backStackEntry.toRoute()
        DetailScreen(id = detail.id)
    }
}
```

- `NavHost` and `NavController` are available in `commonMain` via Compose Navigation for KMP.
- Do not use sealed classes with `object`/`data class` as route strings — use `@Serializable` typed routes.
- Reusable components never receive a `NavController` — screens emit navigation events upward via callbacks.
- Do not use `LocalContext`-dependent navigation helpers from `commonMain`.

---

## Platform Interop Boundaries

| Platform | Boundary rule |
|---|---|
| **Android** | Wrap Compose in `Activity`/`Fragment` only in `androidMain`. Do not reference `ComposeView` or `AndroidView` from `commonMain`. |
| **iOS** | Expose Compose through `ComposeUIViewController` from `iosMain`. SwiftUI/UIKit interop belongs in `iosMain` — not in shared composables. |
| **Desktop** | Window/menu bar/system tray integration belongs in `desktopMain`. Use `ApplicationScope` or `FrameWindowScope` only in desktop source sets. |
| **Web** | DOM and browser API interop belongs in `wasmJsMain`/`jsMain`. |

---

## Adaptive Layout in commonMain

Use common Material3 adaptive APIs for shared adaptive decisions — available via `org.jetbrains.androidx.adaptive` since CMP 1.7.3+:

```kotlin
// commonMain — no Android dependencies required
val windowSizeClass = currentWindowAdaptiveInfo().windowSizeClass
when (windowSizeClass.windowWidthSizeClass) {
    WindowWidthSizeClass.COMPACT -> CompactLayout()
    WindowWidthSizeClass.MEDIUM  -> MediumLayout()
    else                         -> ExpandedLayout()
}
```

Platform-specific adaptive APIs (fold posture, `WindowInfoTracker`, freeform window management) belong in the relevant platform source set. See platform details below.

---

## Adaptive Differences Per Platform

### Android
- Use AndroidX Window / `WindowInfoTracker` in `androidMain` for fold posture and `FoldingFeature`.
- Android 17+ (API 37): orientation lock and fixed-size opt-outs removed for large screens.
- Multi-window: test at 320dp and 1200dp+.

### iOS / iPadOS
- iPadOS Split View and Slide Over provide arbitrary window sizes — treat `maxWidth` as the layout constraint.
- `UIViewController` bounds are the Compose window — inherited from the host.

### Desktop (JVM)
- Windows are continuously resizable — layouts must reflow smoothly.
- Mouse and keyboard are primary input; touch is secondary or absent.
- Scrollbars are expected for scrollable content — use `VerticalScrollbar`/`HorizontalScrollbar` from `desktopMain`.
- Set a minimum window size to prevent broken layouts at extreme small sizes.

### Pointer vs Touch Input
In `commonMain`, use `PointerInput` APIs to detect input type:

```kotlin
Modifier.pointerInput(Unit) {
    awaitPointerEventScope {
        val event = awaitPointerEvent()
        val isMouse = event.changes.any { it.type == PointerType.Mouse }
        val isTouch = event.changes.any { it.type == PointerType.Touch }
    }
}
```

Touch: tap targets ≥ 48dp, swipe gestures.
Mouse/trackpad: hover effects, scroll wheel, right-click. Denser layouts are possible but interactive targets must remain accessible and platform-appropriate.
Stylus: pressure/tilt via `PointerInputChange`.

---

## Version Alignment

Compose Multiplatform breaks when versions drift. Keep these aligned according to JetBrains release guidance:

- Kotlin version
- Compose Multiplatform version
- Compose compiler version (auto-aligned in CMP 1.6+)
- `org.jetbrains.androidx.lifecycle` version
- `androidx.navigation` (KMP) version
- Material3 adaptive version

> CMP 1.8.0+ native/web klibs require Kotlin 2.1.0+ due to the K2 migration. Always check the [JetBrains Compose compatibility table](https://www.jetbrains.com/help/kotlin-multiplatform-dev/compose-compatibility-and-versioning.html) before upgrading.

---

## Testing in KMP

Shared UI should be testable without platform services:

- Inject fakes via interfaces — the same interface used in production, with a test implementation.
- Use `expect`/`actual` test fixtures for platform-specific test setup when needed.
- Pure logic in `commonMain` (state transformations, validation, format parsing) should be covered by `commonTest` unit tests with no UI harness.
- UI tests that require a composition host go in platform-specific test source sets.

---

## commonMain Checklist
- [ ] No platform SDK APIs (`android.*`, `Context`, `Activity`, UIKit, AWT)
- [ ] No `LocalContext` usage
- [ ] Only `androidx.*` / `org.jetbrains.*` APIs that are documented as KMP-compatible
- [ ] All strings via `Res.string.*`
- [ ] All images via `Res.drawable.*`
- [ ] Platform behavior behind `expect`/`actual` or injected interfaces
- [ ] Lifecycle via `org.jetbrains.androidx.lifecycle`
- [ ] Routes are `@Serializable` typed objects/data classes
- [ ] Reusable components never hold `NavController`
- [ ] Kotlin, CMP, lifecycle, and navigation versions aligned per JetBrains guidance
