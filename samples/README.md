# Sample Applications

This directory contains full sample applications demonstrating how to use the libraries in this monorepo.

## Available Samples

### example-library

Demonstrates the use of `example-library` including:
- Generating Fibonacci sequences
- Taking elements from sequences
- Calculating sums and filtering

**Run it:**
```bash
./gradlew :samples:example-library:run
```

## Creating a New Sample

### 1. Create Sample Directory

```bash
mkdir -p samples/my-sample/src/{commonMain,jvmMain}/kotlin
```

### 2. Create build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    application
}

kotlin {
    jvm {
        withJava()
    }
    
    sourceSets {
        commonMain.dependencies {
            // Add the libraries you want to demonstrate
            implementation(project(":libraries:example-library"))
            implementation(project(":libraries:another-library"))
        }
    }
}

application {
    mainClass.set("MainKt")
}
```

### 3. Create Your Sample Code

**src/commonMain/kotlin/Main.kt:**
```kotlin
import com.compiledplatforms.kmp.library.fibonacci.generateFibi

fun main() {
    println("My Sample App")
    // Your sample code here
}
```

**src/jvmMain/kotlin/JvmMain.kt:**
```kotlin
fun main() {
    main()  // Call common main
}
```

### 4. Sync and Run

The sample will be auto-discovered. Just sync Gradle and run:

```bash
./gradlew :samples:my-sample:run
```

## Sample Best Practices

### ✅ DO

1. **Use project dependencies** - `implementation(project(":libraries:..."))`
   - Ensures samples always use latest library code
   - Catches breaking changes immediately

2. **Keep samples simple** - Focus on demonstrating library features
   - Clear, commented code
   - One concept per sample when possible

3. **Make samples runnable** - Users should be able to clone and run
   - Include clear instructions
   - Minimal setup required

4. **Test samples in CI** - Include in build pipeline
   - Prevents samples from breaking
   - Validates library changes don't break usage

5. **Document what's demonstrated** - Clear README in each sample
   - What features are shown
   - How to run it
   - What to expect

### ❌ DON'T

1. **Don't use published versions** in samples (use project dependencies)
2. **Don't make samples too complex** - they're for learning, not production
3. **Don't duplicate library tests** - samples show usage, tests validate correctness
4. **Don't forget to update samples** when library APIs change

## Sample Types

### Basic Samples
Simple, focused demonstrations of core features.
- Quick to understand
- Single library focus
- Minimal dependencies

### Advanced Samples
Complex, real-world usage patterns.
- Multiple libraries working together
- Integration scenarios
- Best practices demonstrations

### Platform-Specific Samples
Demonstrate platform-specific features.
- JVM-specific features
- Android app samples
- iOS app samples
- Native console apps

## Running Samples

### Run a Specific Sample
```bash
./gradlew :samples:example-library:run
```

### Build All Samples
```bash
./gradlew :samples:build
```

### List All Sample Tasks
```bash
./gradlew :samples:example-library:tasks
```

## CI Integration

Samples are automatically built in CI to ensure they stay in sync with library changes.

If a sample breaks, it means:
- ✅ Good! The CI caught a breaking change
- 🔧 Update the sample to work with the new API
- 📝 Document the breaking change

## Structure

```
samples/
├── README.md                    # This file
├── example-library/      # Sample for example-library
│   ├── README.md               # Sample-specific docs
│   ├── build.gradle.kts        # Sample build config
│   └── src/
│       ├── commonMain/kotlin/  # Common sample code
│       └── jvmMain/kotlin/     # JVM entry point
└── another-sample/             # Another sample
    └── ...
```

## Tips

- **Keep samples updated** - They're the first thing users try
- **Use samples for documentation** - Link to them from library READMEs
- **Test samples locally** before pushing
- **Make samples copy-pasteable** - Users often start with samples

## Questions?

## Sample to KMP Target Mapping
see: https://kotlinlang.org/api/kotlin-gradle-plugin/kotlin-gradle-plugin-api/org.jetbrains.kotlin.gradle.dsl/-kotlin-multiplatform-source-set-conventions/

| Sample                  | KMP Targets Covered                                                                        | UI/Framework Options                                                    |
|-------------------------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|
| `jvm`                   | `jvm`                                                                                      | CLI, Ktor, Spring Boot, etc.                                            |
| `jvm-desktop`           | `jvm`                                                                                      | Compose Desktop, Swing, JavaFX                                          |
| `android`               | `android`                                                                                  | Jetpack Compose or XML Views                                            |
| `ios`                   | `iosArm64`, `iosX64`, `iosSimulatorArm64`                                                 | UIKit, SwiftUI, or Compose Multiplatform                                |
| `web-js`                | `js`                                                                                       | Browser: vanilla JS, HTML/CSS, React, Vue, Angular, Svelte, etc.       |
| `web-wasm`              | `wasmJs`                                                                                   | Browser with JS interop: vanilla JS, React, Vue, Angular, Svelte, etc. |
| `compose-multiplatform` | `android`, `iosArm64`, `iosX64`, `iosSimulatorArm64`, `jvm`, `js`, `wasmJs`               | Compose Multiplatform (shared UI)                                       |
| `android-native`        | `androidNativeArm32`, `androidNativeArm64`, `androidNativeX86`, `androidNativeX64`         | NDK/Native (no UI framework)                                            |
| `macos-native`          | `macosX64`, `macosArm64`                                                                   | AppKit, SwiftUI, or CLI                                                 |
| `windows-native`        | `mingwX64`                                                                                 | Win32 API, WPF interop, or CLI                                          |
| `linux-native`          | `linuxX64`, `linuxArm64`                                                   | GTK, CLI, or server                                                     |
| `watchos`               | `watchosArm32`, `watchosArm64`, `watchosX64`, `watchosSimulatorArm64`, `watchosDeviceArm64` | WatchKit, SwiftUI                                                       |
| `tvos`                  | `tvosArm64`, `tvosX64`, `tvosSimulatorArm64`                                              | UIKit for tvOS, SwiftUI                                                 |
| `nodejs`                | `js`                                                                                       | Node.js runtime: CLI, Express, Fastify, etc.                            |
| `wasm-wasi`             | `wasmWasi`                                                                                 | Server-side WASI runtime (no UI)                                        |



## Sample File Structure
### Minimum Sample Structure:
This file structure covers all the official KMP targets with at least one sample per target.
```
samples/example-library/ 
│
├── compose-multiplatform/ # android, iosArm64, iosX64, iosSimulatorArm64, jvm, js (browser), wasmJs (browser)
│
├── android-native/        # androidNativeArm32, androidNativeArm64, androidNativeX86
│
├── macos-native/          # macosX64, macosArm64
├── windows-native/        # mingwX64
├── linux-native/          # linuxX64, linuxArm64
│
├── watchos/               # watchosArm32, watchosArm64, watchosX64, watchosSimulatorArm64, watchosDeviceArm64
├── tvos/                  # tvosArm64, tvosX64, tvosSimulatorArm64`
│
├── nodejs/                # js
└── wasm-wasi/             # wasmWasi
```


### Additional Expanded Sample Structure:
This file structure demonstrates example framework-specific sample directories.
```
│
├── jvm-cli/                          # JVM CLI
├── jvm-ktor/                         # JVM with Ktor server
├── jvm-spring/                       # JVM with Spring Boot
├── jvm-{framework}/                  # JVM with other frameworks
│
├── jvm-desktop-compose/              # JVM desktop with Compose Desktop
├── jvm-desktop-swing/                # JVM desktop with Swing
├── jvm-desktop-javafx/               # JVM desktop with JavaFX
├── jvm-desktop-{framework}/          # JVM desktop with other frameworks
│
├── android-compose/                  # Android with Jetpack Compose
├── android-views/                    # Android with XML Views
├── android-{framework}/              # Android with other frameworks
│
├── ios-uikit/                        # iOS with UIKit
├── ios-swiftui/                      # iOS with SwiftUI
├── ios-{framework}/                  # iOS with other frameworks
│
├── web-js-vanilla/                   # Browser JS vanilla
├── web-js-react/                     # Browser JS with React
├── web-js-vue/                       # Browser JS with Vue
├── web-js-{framework}/               # Browser JS with other frameworks
│
├── web-wasm-vanilla/                 # Browser WasmJS vanilla (with JS interop)
├── web-wasm-react/                   # Browser WasmJS with React (with JS interop)
├── web-wasm-{framework}/             # Browser WasmJS with other frameworks
│
├── nodejs-cli/                       # Node.js CLI
├── nodejs-express/                   # Node.js with Express
├── nodejs-{framework}/               # Node.js with other frameworks
│
├── macos-native-appkit/              # macOS native with AppKit
├── macos-native-{framework}/         # macOS native with other frameworks
│
├── windows-native-win32/             # Windows native with Win32 API
├── windows-native-{framework}/       # Windows native with other frameworks
│
├── linux-native-gtk/                 # Linux native with GTK
├── linux-native-{framework}/         # Linux native with other frameworks
│
├── watchos-watchkit/                 # watchOS with WatchKit
├── watchos-swiftui/                  # watchOS with SwiftUI
├── watchos-{framework}/              # watchOS with other frameworks
│
├── tvos-uikit/                       # tvOS with UIKit
├── tvos-swiftui/                     # tvOS with SwiftUI
├── tvos-{framework}/                 # tvOS with other frameworks
│
├── android-native-ndk/               # Android NDK native (no UI)
├── android-native-{framework}/       # Android NDK with other frameworks
│
├── wasm-wasi-cli/                    # WASI CLI
├── wasm-wasi-server/                 # WASI server
└── wasm-wasi-{framework}/            # WASI with other frameworks
```

See the main [README](../README.md) for more information about the monorepo structure.
