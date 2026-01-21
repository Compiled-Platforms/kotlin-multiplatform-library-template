# BOM Management for Independent Library Versions

This guide explains how to manage the BOM when libraries have independent versions.

## Overview

- **Each library** has its own version (e.g., `library-a:1.5.0`, `library-b:2.3.0`)
- **The BOM** has its own version (e.g., `bom:1.0.0`)
- **The BOM declares** which library versions are tested and compatible together

## Updating the BOM

### When to Release a New BOM Version

Release a new BOM version when:
1. ✅ You release a new version of any library
2. ✅ You've tested a new combination of library versions together
3. ✅ You want to recommend an updated set of library versions

### How to Update

**Step 1:** Edit `bom/build.gradle.kts`

```kotlin
dependencies.constraints {
    api("com.compiledplatforms.kmp.library:example-library:1.0.0")      // Current version
    api("com.compiledplatforms.kmp.library:another-library:2.3.0")      // Current version
    api("com.compiledplatforms.kmp.library:third-library:1.5.0")        // Current version
}
```

**Step 2:** Update the BOM version

```kotlin
version = "1.1.0"  // Increment the BOM version
```

**Step 3:** Test the combination

```bash
./gradlew clean build allTests
```

**Step 4:** Publish the BOM

```bash
./gradlew :bom:publishAllPublicationsToMavenCentral
```

## Version Tracking

### Maintain a Version Matrix

Keep track of which BOM version contains which library versions:

| BOM Version | example-library | another-library | third-library | Release Date |
|-------------|----------------|-----------------|---------------|--------------|
| 1.0.0       | 1.0.0          | 2.3.0           | 1.5.0         | 2026-01-20   |
| 1.1.0       | 1.0.0          | 2.4.0           | 1.6.0         | 2026-02-15   |
| 1.2.0       | 1.1.0          | 2.4.0           | 1.6.0         | 2026-03-10   |
| 2.0.0       | 2.0.0          | 3.0.0           | 2.0.0         | 2026-06-01   |

### Example CHANGELOG.md

```markdown
# BOM Changelog

## [1.1.0] - 2026-02-15

### Libraries Included
- example-library: 1.0.0 (unchanged)
- another-library: 2.4.0 (updated from 2.3.0)
- third-library: 1.6.0 (updated from 1.5.0)

### What's New
- Updated another-library to 2.4.0 for bug fixes
- Updated third-library to 1.6.0 for new features

### Compatibility
- Tested with Kotlin 2.2.20
- Compatible with Android compileSdk 36
```

## Workflow Example

### Scenario: Releasing a New Library Version

1. **Develop and test** `another-library:2.4.0`
2. **Publish the library**:
   ```bash
   ./gradlew :libraries:another-library:publishAllPublicationsToMavenCentral
   ```
3. **Update BOM** to include the new version:
   ```kotlin
   // bom/build.gradle.kts
   dependencies.constraints {
       api("com.compiledplatforms.kmp.library:example-library:1.0.0")
       api("com.compiledplatforms.kmp.library:another-library:2.4.0")  // Updated
       api("com.compiledplatforms.kmp.library:third-library:1.6.0")
   }
   version = "1.1.0"  // Increment BOM version
   ```
4. **Test the combination** - make sure all libraries work together
5. **Publish the BOM**:
   ```bash
   ./gradlew :bom:publishAllPublicationsToMavenCentral
   ```
6. **Update CHANGELOG.md** and **tag the release**

## Inter-library Dependencies

When libraries depend on each other, be explicit about version ranges:

### In library-b that depends on library-a:

```kotlin
// libraries/library-b/build.gradle.kts
kotlin {
    sourceSets {
        commonMain.dependencies {
            // Specify a version range that you've tested
            api("com.compiledplatforms.kmp.library:library-a:1.0.0")  // Or use version ranges
        }
    }
}
```

### BOM ensures compatibility:

```kotlin
// bom/build.gradle.kts
dependencies.constraints {
    api("com.compiledplatforms.kmp.library:library-a:1.0.0")
    api("com.compiledplatforms.kmp.library:library-b:2.0.0")  // Declares library-a:1.0.0 as dependency
}
```

When users import the BOM, they get tested versions:
```kotlin
dependencies {
    implementation(platform("com.compiledplatforms.kmp.library:bom:1.0.0"))
    implementation("com.compiledplatforms.kmp.library:library-b")  // Gets 2.0.0
    // library-a:1.0.0 is automatically included (transitive from library-b)
}
```

## Semantic Versioning for BOM

### BOM Version Scheme

- **MAJOR** (2.0.0): Breaking changes in included libraries, incompatible combinations
- **MINOR** (1.1.0): New library versions added, backward compatible
- **PATCH** (1.0.1): BOM metadata updates, no library version changes

### Example:
- `bom:1.0.0` → `bom:1.1.0`: Updated `library-b` from 2.3.0 to 2.4.0 (compatible)
- `bom:1.1.0` → `bom:2.0.0`: Updated `library-a` to 2.0.0 with breaking changes

## Best Practices

### ✅ DO

1. **Test before publishing** - Always test library combinations before releasing BOM
2. **Document changes** - Maintain clear changelog of what changed
3. **Use Git tags** - Tag each BOM release: `git tag bom-v1.0.0`
4. **Version carefully** - Follow semantic versioning for BOM
5. **Keep matrix updated** - Maintain version compatibility matrix

### ❌ DON'T

1. **Publish untested combinations** - Always verify libraries work together
2. **Skip documentation** - Users need to know what versions are included
3. **Update too frequently** - Balance freshness with stability
4. **Include incompatible versions** - Test inter-library dependencies

## Quick Reference

```bash
# Check current BOM version
grep "^version" bom/build.gradle.kts

# View BOM contents
./gradlew :bom:generatePomFileForMavenPublication
cat bom/build/publications/maven/pom-default.xml

# Test everything together
./gradlew clean build

# Publish BOM
./gradlew :bom:publishAllPublicationsToMavenCentral

# Tag release
git tag bom-v1.0.0
git push origin bom-v1.0.0
```

## Summary

With independent library versioning:
- **Libraries** release on their own schedule
- **BOM** declares tested, compatible combinations
- **Users** get simplified dependency management with guaranteed compatibility
- **You** maintain flexibility while ensuring quality
