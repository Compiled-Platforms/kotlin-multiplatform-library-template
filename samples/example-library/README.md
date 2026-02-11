# Example Library Samples

Sample applications demonstrating the `example-library` (Fibonacci) across different platforms.

## What These Samples Demonstrate

- **Fibonacci sequences**: Generate sequences with `generateFibi()`
- **Sequence operations**: Take elements, sums, and filtering with `takeWhile`
- **Shared logic**: Common code in `commonMain`, platform entry points per target

## Running Samples

### JVM - CLI
- KMP Target: `jvm`
```bash
./gradlew :samples:example-library:jvm-cli:run
```

### JVM (Desktop) - Compose Multiplatform
- KMP Target: `jvm`
- Platforms: Desktop(`macOS`, `Windows`, `Linux`)
```bash
./gradlew :samples:example-library:compose-multiplatform:run
```

### Javascript (Web) - Compose Multiplatform
- KMP Target: `js`
```bash
./gradlew :samples:example-library:compose-multiplatform:jsBrowserDevelopmentRun
```

### WebAssembly (Web) - Compose Multiplatform
- KMP Target: `wasmJs`
```bash
./gradlew :samples:example-library:compose-multiplatform:wasmJsBrowserDevelopmentRun
```

### Android - Compose Multiplatform
- KMP Target: `android`
- The Android app is in the `compose-android` module (AGP application), which depends on `compose-multiplatform`.

Requires a connected Android device or emulator. To run:
1. Open Android Studio and start an emulator (Tools → Device Manager)
2. Or connect a physical device with USB debugging enabled
3. Run the app:

```bash
./gradlew :samples:example-library:compose-android:runDebug
```

_This installs the APK and launches it. To just install without launching, use `:samples:example-library:compose-android:installDebug` instead._

### iOS - Compose Multiplatform
- KMP Target: `iosArm64`, `iosX64`, `iosSimulatorArm64`

**Prerequisites:**
- Xcode installed (available from the Mac App Store)
- Xcode command line tools initialized. After installing or updating Xcode, run:
  ```bash
  sudo xcodebuild -runFirstLaunch
  ```
- Xcode license agreement accepted:
  ```bash
  sudo xcodebuild -license
  ```
  Then scroll through the license (press space), type `agree`, and enter your password.
- **iOS Simulator platform installed.** If you see errors like "iOS X.X is not installed" or "Unable to find a destination matching the provided destination specifier", install the simulator runtime: open Xcode and use the download prompt it shows, or go to **Xcode → Settings → Platforms** (or **Components** on older Xcode) and download the iOS version that matches your default SDK.

**Option 1: Run from command line (recommended)**
```bash
./gradlew :samples:example-library:compose-multiplatform:iosSimulatorRun
```

This builds the framework, compiles the iOS app, and launches it in the simulator automatically. By default, it uses the first booted simulator, or boots the first available iPhone simulator.

To specify a particular device:
```bash
./gradlew :samples:example-library:compose-multiplatform:iosSimulatorRun -PiosDevice="iPhone 16 Pro"
```

**Option 2: Run from Xcode**
1. Open the Xcode project:
```bash
open samples/example-library/compose-multiplatform/iosApp/iosApp.xcodeproj
```

2. Select your target simulator or device in Xcode

3. Click the Run button (⌘R) in Xcode

The Xcode build script automatically builds the Kotlin framework and embeds it into the iOS app
