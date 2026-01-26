# Version Catalog

This template uses Gradle's [version catalog](https://docs.gradle.org/current/userguide/platforms.html) feature for centralized dependency management.

## Overview

All versions, dependencies, and plugins are defined in a single file:

```
gradle/libs.versions.toml
```

This provides:

- ✅ **Single source of truth** for all dependencies
- ✅ **Type-safe accessors** in build scripts (`libs.kotlin.test`)
- ✅ **Easy updates** - change version in one place
- ✅ **IDE support** - autocomplete and navigation
- ✅ **Consistent versions** across all modules

## Current Dependencies

### Platform Versions

| Setting | Version | Purpose |
|---------|---------|---------|
| **minSdk** | `24` | Minimum Android API (Android 7.0) |
| **compileSdk** | `36` | Target Android API |

### Core Tooling

| Tool | Version | Purpose | Documentation |
|------|---------|---------|:-------------:|
| **Kotlin** | `2.3.0` | Language and compiler | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/docs/home.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/JetBrains/kotlin "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Gradle** | `9.0.0` | Build tool (wrapper) | [<span style="font-size: 1.25em">:material-book:</span>](https://docs.gradle.org/current/userguide/userguide.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/gradle/gradle "GitHub Repo"){: target="_blank" rel="noopener" } |
| **AGP** | `8.13.0` | Android Gradle Plugin | [<span style="font-size: 1.25em">:material-book:</span>](https://developer.android.com/build "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://android.googlesource.com/platform/tools/base/ "GitHub Repo"){: target="_blank" rel="noopener" } |

!!! info "Version Compatibility"
    For detailed version compatibility between Kotlin, Gradle, AGP, and Xcode, see the [Official Kotlin Multiplatform Compatibility Guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html#version-compatibility){: target="_blank" rel="noopener" }.

### Build Plugins

| Plugin | Version | Purpose | Documentation |
|--------|---------|---------|:-------------:|
| **Dokka** | `2.1.0` | API documentation generation | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/docs/dokka-introduction.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/dokka "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Detekt** | `2.0.0-alpha.1` | Static code analysis | [<span style="font-size: 1.25em">:material-book:</span>](https://detekt.dev/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/detekt/detekt "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Kover** | `0.9.4` | Code coverage | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlin.github.io/kotlinx-kover/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/kotlinx-kover "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Binary Compatibility Validator** | `0.18.1` | API stability tracking | [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/binary-compatibility-validator "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Vanniktech Maven Publish** | `0.34.0` | Maven Central publishing | [<span style="font-size: 1.25em">:material-book:</span>](https://vanniktech.github.io/gradle-maven-publish-plugin/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/vanniktech/gradle-maven-publish-plugin "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Mokkery** | `3.1.1` | Mocking plugin (KSP) | [<span style="font-size: 1.25em">:material-book:</span>](https://mokkery.dev/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/lupuuss/Mokkery "GitHub Repo"){: target="_blank" rel="noopener" } |

### Testing Libraries

| Library | Version | Purpose | Documentation |
|---------|---------|---------|:-------------:|
| **kotlin-test** | `2.3.0` | Standard testing framework | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/api/latest/kotlin.test/ "Official Docs"){: target="_blank" rel="noopener" } |
| **kotlinx-coroutines-test** | `1.10.2` | Coroutine testing | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/kotlinx.coroutines "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Turbine** | `1.2.1` | Flow testing | [<span style="font-size: 1.25em">:material-book:</span>](https://cashapp.github.io/turbine/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/cashapp/turbine "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Mokkery Runtime** | `3.1.1` | Mocking library | [<span style="font-size: 1.25em">:material-book:</span>](https://mokkery.dev/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/lupuuss/Mokkery "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Kotest Assertions** | `6.1.0` | Expressive assertions | [<span style="font-size: 1.25em">:material-book:</span>](https://kotest.io/docs/assertions/assertions.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/kotest/kotest "GitHub Repo"){: target="_blank" rel="noopener" } |
| **Kotest Property** | `6.1.0` | Property-based testing (opt-in) | [<span style="font-size: 1.25em">:material-book:</span>](https://kotest.io/docs/proptest/property-based-testing.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/kotest/kotest "GitHub Repo"){: target="_blank" rel="noopener" } |

### Example Libraries

| Library | Version | Purpose | Documentation |
|---------|---------|---------|:-------------:|
| **kotlinx-coroutines-core** | `1.10.2` | Coroutines support | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/docs/coroutines-overview.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/kotlinx.coroutines "GitHub Repo"){: target="_blank" rel="noopener" } |
| **kotlinx-serialization-json** | `1.8.0` | JSON serialization | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/docs/serialization.html "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/kotlinx.serialization "GitHub Repo"){: target="_blank" rel="noopener" } |
| **kotlinx-datetime** | `0.6.1` | Date/time utilities | [<span style="font-size: 1.25em">:material-book:</span>](https://kotlinlang.org/api/kotlinx-datetime/ "Official Docs"){: target="_blank" rel="noopener" } [<span style="font-size: 1.25em">:material-github:</span>](https://github.com/Kotlin/kotlinx-datetime "GitHub Repo"){: target="_blank" rel="noopener" } |

## Version Catalog Structure

The version catalog has three main sections:

### 1. `[versions]`

Defines version numbers that can be referenced by multiple dependencies:

```toml
[versions]
kotlin = "2.3.0"
kotest = "6.1.0"
```

### 2. `[libraries]`

Defines library dependencies:

```toml
[libraries]
kotlin-test = { module = "org.jetbrains.kotlin:kotlin-test", version.ref = "kotlin" }
kotest-assertions-core = { module = "io.kotest:kotest-assertions-core", version.ref = "kotest" }
```

### 3. `[plugins]`

Defines Gradle plugins:

```toml
[plugins]
kotlinMultiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
detekt = { id = "dev.detekt", version.ref = "detekt" }
```

## Using the Version Catalog

### In Build Scripts

Access dependencies using type-safe accessors:

```kotlin
dependencies {
    // Use a library
    implementation(libs.kotlinx.coroutines.core)
    
    // Test dependencies
    testImplementation(libs.kotlin.test)
    testImplementation(libs.kotest.assertions.core)
}
```

### Apply Plugins

```kotlin
plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.detekt)
}
```

### In Convention Plugins

Access the version catalog in your convention plugins:

```kotlin
val libs = extensions.getByType<VersionCatalogsExtension>().named("libs")

dependencies {
    implementation(libs.findLibrary("kotlin-test").get())
}
```

## Adding New Dependencies

### 1. Add Version (Optional)

If multiple dependencies share the same version:

```toml
[versions]
ktor = "2.3.7"
```

### 2. Add Library

```toml
[libraries]
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-android = { module = "io.ktor:ktor-client-android", version.ref = "ktor" }
```

Or with inline version:

```toml
[libraries]
my-library = { module = "com.example:library", version = "1.0.0" }
```

### 3. Use in Build Script

```kotlin
dependencies {
    implementation(libs.ktor.client.core)
    implementation(libs.ktor.client.android)
}
```

## Version Update Strategy

### Semantic Versioning

This template follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (2.x.x) - Breaking changes
- **MINOR** (x.3.x) - New features, backward compatible
- **PATCH** (x.x.0) - Bug fixes, backward compatible

### Update Policy

| Dependency Type | Update Frequency | Strategy |
|----------------|------------------|----------|
| **Kotlin** | Stable releases | Test thoroughly, major versions may require migration |
| **Gradle** | Stable releases | Check compatibility, review deprecations |
| **AGP** | Latest stable | Match with Kotlin version requirements |
| **Plugins** | Stable releases | Review changelogs, test in feature branch |
| **Libraries** | Latest compatible | Automated via Dependabot, grouped updates |
| **Test Libraries** | Latest stable | Low risk, update frequently |

### Dependabot Integration

The template uses [Dependabot](./dependency-updates.md) to automate updates with smart grouping:

- **Kotlin ecosystem** - All Kotlin-related updates together
- **Android** - AGP and Android libraries
- **Dev tools** - Detekt, Dokka, Kover, BCV
- **Test libraries** - Testing dependencies

## Version Compatibility

### Critical Compatibility Requirements

1. **Kotlin ↔ Gradle**
   - Kotlin 2.3.0+ requires Gradle 8.5+
   - Current: Kotlin 2.3.0 + Gradle 9.0.0 ✅

2. **Kotlin ↔ AGP**
   - AGP 8.13.0 requires Kotlin 1.9.20+
   - Current: Kotlin 2.3.0 + AGP 8.13.0 ✅

3. **Gradle ↔ Java**
   - Gradle 9.0.0 requires Java 17+
   - Recommended: Java 21

4. **Mokkery ↔ Kotlin**
   - Mokkery 3.1.1 requires Kotlin 2.0.20+
   - Current: Kotlin 2.3.0 + Mokkery 3.1.1 ✅

### Compatibility Matrix

| Kotlin | Gradle | AGP | Java |
|--------|--------|-----|------|
| 2.3.0 | 9.0.0 | 8.13.0 | 17-21 |
| 2.2.0 | 8.5+ | 8.5+ | 17-21 |
| 2.1.0 | 8.1.1+ | 8.2+ | 17-21 |
| 2.0.0 | 7.6+ | 8.1+ | 17-20 |

## Security Considerations

### Vulnerability Scanning

- **Dependabot** alerts for known vulnerabilities
- **GitHub Security Advisories** notifications
- Review security updates promptly

### Pinned Versions

All versions are **explicitly pinned** in the version catalog:

- ✅ Reproducible builds
- ✅ No surprise updates
- ✅ Easier rollback if issues occur
- ✅ Security audit trail

### Version Ranges (Not Recommended)

**Avoid** version ranges in production:

```toml
# ❌ BAD - unpredictable builds
my-lib = { module = "com.example:lib", version = "1.+" }

# ✅ GOOD - explicit and reproducible
my-lib = { module = "com.example:lib", version = "1.5.2" }
```

## Generating Dependency Reports

### View All Dependencies

```bash
# List all dependencies for a module
./gradlew :libraries:example-library:dependencies

# Filter by configuration
./gradlew :libraries:example-library:dependencies --configuration jvmRuntimeClasspath
```

### Dependency Insight

```bash
# See where a specific dependency comes from
./gradlew :libraries:example-library:dependencyInsight \
  --dependency kotlin-stdlib \
  --configuration jvmRuntimeClasspath
```

### Build Scan

Enable build scans for visual dependency analysis:

```bash
./gradlew build --scan
```

## Best Practices

### DO ✅

- **Keep versions updated** - Use Dependabot for automation
- **Test updates** - Run full test suite before merging
- **Group related updates** - Update Kotlin ecosystem together
- **Document breaking changes** - Note in CHANGELOG.md
- **Pin versions explicitly** - No ranges or `latest`
- **Use semantic versioning** - Communicate impact of updates
- **Review changelogs** - Understand what changed

### DON'T ❌

- **Don't use version ranges** - Breaks reproducibility
- **Don't skip testing** - Even minor updates can break
- **Don't update everything at once** - Isolate issues
- **Don't ignore security advisories** - Update promptly
- **Don't mix major updates** - Update Kotlin separately from libraries
- **Don't forget compatibility** - Check Kotlin ↔ Gradle ↔ AGP

## Migration Guide

### From `buildSrc` Constants

**Before** (in `buildSrc/Versions.kt`):

```kotlin
object Versions {
    const val kotlin = "2.2.0"
    const val coroutines = "1.8.0"
}
```

**After** (in `gradle/libs.versions.toml`):

```toml
[versions]
kotlin = "2.3.0"
kotlinx-coroutines = "1.10.2"
```

### From Inline Versions

**Before**:

```kotlin
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
}
```

**After**:

```kotlin
dependencies {
    implementation(libs.kotlinx.coroutines.core)
}
```

## Troubleshooting

### "Cannot find version catalog" Error

**Problem**: Version catalog not accessible in build script.

**Solution**: Ensure `settings.gradle.kts` includes:

```kotlin
dependencyResolutionManagement {
    versionCatalogs {
        create("libs") {
            from(files("gradle/libs.versions.toml"))
        }
    }
}
```

### "Version conflict" Errors

**Problem**: Multiple versions of the same dependency.

**Solution**:

```kotlin
// Force a specific version
configurations.all {
    resolutionStrategy {
        force("org.jetbrains.kotlin:kotlin-stdlib:${libs.versions.kotlin.get()}")
    }
}
```

### IDE Not Recognizing Catalog

**Problem**: No autocomplete for `libs.*`.

**Solution**:
1. Sync Gradle project
2. Invalidate caches and restart IDE
3. Ensure using Gradle 7.0+

## Resources

- [Gradle Version Catalogs](https://docs.gradle.org/current/userguide/platforms.html)
- [Kotlin Compatibility Guide](https://kotlinlang.org/docs/gradle-configure-project.html#apply-the-plugin)
- [AGP Release Notes](https://developer.android.com/studio/releases/gradle-plugin)
- [Dependency Updates](./dependency-updates.md)

---

**Last Updated**: 2026-01-20  
**Template Version**: 1.0.0
