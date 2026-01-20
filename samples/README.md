# Sample Applications

This directory contains full sample applications demonstrating how to use the libraries in this monorepo.

## Available Samples

### example-library-sample

Demonstrates the use of `example-library` including:
- Generating Fibonacci sequences
- Taking elements from sequences
- Calculating sums and filtering

**Run it:**
```bash
./gradlew :samples:example-library-sample:run
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
import io.github.kotlin.fibonacci.generateFibi

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
./gradlew :samples:example-library-sample:run
```

### Build All Samples
```bash
./gradlew :samples:build
```

### List All Sample Tasks
```bash
./gradlew :samples:example-library-sample:tasks
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
├── example-library-sample/      # Sample for example-library
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

See the main [README](../README.md) for more information about the monorepo structure.
