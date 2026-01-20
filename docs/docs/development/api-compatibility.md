# API Compatibility Validation

This template uses [Binary Compatibility Validator](https://github.com/Kotlin/binary-compatibility-validator) (BCV) to ensure that your library's public API remains stable and backward-compatible across releases.

## What is Binary Compatibility?

**Binary compatibility** ensures that code compiled against an older version of your library continues to work with newer versions without recompilation. This is crucial for library maintainers to avoid breaking downstream consumers.

### Example of Breaking Changes

```kotlin
// Version 1.0.0
class MyClass {
    fun doSomething(param: String) { }
}

// Version 1.1.0 - BREAKS BINARY COMPATIBILITY ❌
class MyClass {
    fun doSomething(param: String, newParam: Int = 0) { } // Added parameter
}
```

While this change is **source-compatible** (old code still compiles), it's **binary-incompatible** because the JVM method signature changed. Code compiled against 1.0.0 will crash at runtime with `NoSuchMethodError`.

## How It Works

BCV tracks your library's public API in `.api` files committed to git. During builds, it compares the current API against these files and fails if there are unexpected changes.

### API Dump Files

Each library maintains API dumps in its `api/` directory:

```
libraries/example-library/
├── api/
│   ├── jvm/
│   │   └── example-library.api          # JVM bytecode signatures
│   └── example-library.klib.api         # Kotlin/Native ABI
```

**Example JVM API Dump:**

```
public final class com/compiledplatforms/kmp/library/fibonacci/CustomFibiKt {
	public static final fun generateFibi ()Lkotlin/sequences/Sequence;
}
```

**Example KLib API Dump:**

```
// Klib ABI Dump
// Targets: [iosArm64, iosSimulatorArm64, iosX64, linuxX64]

final fun com.compiledplatforms.kmp.library.fibonacci/generateFibi(): kotlin.sequences/Sequence<kotlin/Int>
```

## Configuration

BCV is configured in the root `build.gradle.kts`:

```kotlin
apiValidation {
    // Ignore internal packages and test projects from API validation
    ignoredPackages.addAll(listOf("internal", "benchmarks"))
    ignoredProjects.addAll(listOf("bom"))
    
    // Projects in samples/ are not libraries, exclude them
    project.subprojects.forEach { subproject ->
        if (subproject.path.startsWith(":samples:")) {
            ignoredProjects.add(subproject.name)
        }
    }
    
    // Mark any @InternalApi annotations as non-public
    nonPublicMarkers.add("com.compiledplatforms.kmp.library.InternalApi")
    
    // Enable experimental Kotlin/Native (KLib) ABI validation
    @OptIn(kotlinx.validation.ExperimentalBCVApi::class)
    klib {
        enabled = true
        strictValidation = false // Allows cross-platform builds
    }
}
```

## Gradle Tasks

BCV provides two main tasks:

### `apiDump`

Generates or updates API dump files for all libraries:

```bash
./gradlew apiDump
```

**When to use:**
- First time setting up a new library
- After intentionally changing public API
- When adding new public APIs

**Workflow:**
1. Make your code changes
2. Run `./gradlew apiDump`
3. Review the diff in `.api` files
4. Commit both code changes and updated API dumps

### `apiCheck`

Validates that the current API matches the committed dumps:

```bash
./gradlew apiCheck
```

**When to use:**
- Runs automatically as part of `./gradlew check`
- In CI/CD to catch accidental API changes
- Before committing to verify no unintended breaks

If `apiCheck` fails:
- **Intentional change?** Run `apiDump` and commit the updated dumps
- **Accidental change?** Revert your code to maintain compatibility

## Working with API Changes

### Adding New APIs ✅ Safe

Adding new public classes, methods, or properties is **safe**:

```kotlin
// Before
class MyClass {
    fun existing() { }
}

// After - Safe to add
class MyClass {
    fun existing() { }
    fun newMethod() { }  // ✅ New API, backward compatible
}
```

**Workflow:**
1. Add your new API
2. Run `./gradlew apiDump`
3. Review the diff - should only show additions
4. Commit code + updated API dumps

### Changing Existing APIs ⚠️ Requires Versioning

Modifying or removing existing APIs is a **breaking change**:

```kotlin
// Before
fun calculate(x: Int): Int

// After - BREAKING CHANGE ❌
fun calculate(x: Int, y: Int): Int  // Changed signature
```

**Workflow:**
1. Decide on versioning strategy (major version bump per SemVer)
2. Make your changes
3. Run `./gradlew apiDump`
4. Review the diff - verify all breaking changes are intentional
5. Update `CHANGELOG.md` with breaking changes
6. Commit and tag with new major version

### Deprecation Strategy (Recommended)

Instead of breaking changes, deprecate first:

```kotlin
// Step 1: Add new API, deprecate old (v1.1.0)
@Deprecated("Use calculateBoth instead", ReplaceWith("calculateBoth(x, 0)"))
fun calculate(x: Int): Int = x

fun calculateBoth(x: Int, y: Int): Int = x + y

// Step 2: Remove deprecated (v2.0.0 - major version)
fun calculateBoth(x: Int, y: Int): Int = x + y
```

## Hiding Internal APIs

Use visibility modifiers and annotations to keep APIs internal:

### 1. Kotlin Visibility

```kotlin
// Not visible to library consumers
internal class InternalHelper { }
private fun helperFunction() { }
```

### 2. Custom Annotation (Recommended)

Create an annotation to mark internal APIs:

```kotlin
// Define once in commonMain
@RequiresOptIn(
    message = "This API is internal and may change without notice.",
    level = RequiresOptIn.Level.ERROR
)
@Retention(AnnotationRetention.BINARY)
annotation class InternalApi

// Use on internal public APIs
@InternalApi
class InternalHelper {
    fun doSomething() { }
}
```

Then configure BCV to ignore it:

```kotlin
apiValidation {
    nonPublicMarkers.add("com.compiledplatforms.kmp.library.InternalApi")
}
```

### 3. Package-based (Less Recommended)

```kotlin
// Put internal code in .internal packages
package com.compiledplatforms.kmp.library.internal

class Helper { } // Ignored by BCV
```

Configure:

```kotlin
apiValidation {
    ignoredPackages.add("internal")
}
```

## CI/CD Integration

BCV is automatically integrated into the CI/CD pipeline:

### Build & Test Workflow

The `apiCheck` task runs as part of `./gradlew check`:

```yaml
# .github/workflows/build.yml
- name: Build with Gradle
  run: ./gradlew build --daemon  # Includes apiCheck
```

If API changes are detected in a PR:
- ❌ Build fails with clear error message
- 👀 Reviewer knows to check for breaking changes
- ✅ Run `apiDump` locally and commit if intentional

### Release Workflow

When publishing a release:
1. CI runs `apiCheck` to ensure dumps are up-to-date
2. If dumps are stale, build fails
3. Developer must run `apiDump` and commit before release

## Best Practices

### 1. Always Review API Diffs

When running `apiDump`, carefully review the git diff:

```bash
./gradlew apiDump
git diff libraries/*/api/
```

Look for:
- Removed APIs (breaking changes)
- Modified signatures (breaking changes)
- New APIs (safe additions)

### 2. Commit API Dumps with Code

Never commit code changes without updating API dumps:

```bash
# Wrong ❌
git add src/
git commit -m "Add new feature"

# Right ✅
./gradlew apiDump
git add src/ */api/
git commit -m "feat: add new feature"
```

### 3. Use Semantic Versioning

Follow [SemVer](https://semver.org/) strictly:
- **Major (2.0.0)**: Breaking changes (API removed/modified)
- **Minor (1.1.0)**: New features (API additions only)
- **Patch (1.0.1)**: Bug fixes (no API changes)

### 4. Document Breaking Changes

When making breaking changes:
- Update `CHANGELOG.md` with migration guide
- Add `@Deprecated` annotations before removing
- Provide clear error messages

### 5. Test Compatibility

Before releasing a breaking change:
- Search GitHub for dependent projects
- Test against popular consumers
- Provide migration tools if possible

## Troubleshooting

### `apiCheck` fails after merging main

Someone else updated the API. Pull latest and regenerate:

```bash
git pull origin main
./gradlew apiDump
```

### Need to regenerate all API dumps

```bash
# Delete old dumps
rm -rf libraries/*/api/

# Regenerate
./gradlew apiDump
```

### KLib validation fails on different OS

KLib ABI can vary by host OS. Set `strictValidation = false`:

```kotlin
klib {
    enabled = true
    strictValidation = false // Allows Linux CI to validate iOS
}
```

### Want to exclude experimental APIs

Use `@RequiresOptIn` and configure BCV:

```kotlin
@RequiresOptIn("This API is experimental and may change.")
annotation class ExperimentalApi

apiValidation {
    nonPublicMarkers.add("com.compiledplatforms.kmp.library.ExperimentalApi")
}
```

## Resources

- [Binary Compatibility Validator GitHub](https://github.com/Kotlin/binary-compatibility-validator)
- [Kotlin Binary Compatibility Guide](https://kotlinlang.org/docs/jvm-api-guidelines-backward-compatibility.html)
- [Semantic Versioning](https://semver.org/)
- [API Evolution Guidelines](https://kotlinlang.org/docs/api-guidelines-introduction.html)

## Quick Reference

```bash
# Generate/update API dumps
./gradlew apiDump

# Verify API compatibility
./gradlew apiCheck

# Check all (includes apiCheck)
./gradlew check

# View diff after apiDump
git diff libraries/*/api/
```

**Golden Rule:** If `apiCheck` fails, either:
1. Run `apiDump` if the change was intentional, or
2. Revert your code if the change was accidental

Never disable or skip `apiCheck` to "fix" a failing build!
