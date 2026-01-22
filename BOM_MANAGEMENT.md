# BOM Version Management Guide

This guide explains how to manage the BOM (Bill of Materials) and ensure library compatibility.

## Version Strategy

This monorepo uses a **coordinated release** strategy where all libraries are versioned together.

### Single Version Source

All versions are defined in `gradle/libs.versions.toml`:

```toml
[versions]
project-version = "1.0.0"  # <-- Change this to release everything
```

All libraries and the BOM pull from this single version:
- `bom/build.gradle.kts` uses `project-version`
- `libraries/*/build.gradle.kts` use `project-version`

## Release Process

### 1. Update the Version

Edit `gradle/libs.versions.toml`:

```toml
[versions]
project-version = "1.1.0"  # Update this
```

### 2. Verify Library Versions

Check that all libraries will use the new version:

```bash
./gradlew properties | grep "version:"
```

### 3. Test Compatibility

Run all tests to ensure libraries work together:

```bash
./gradlew clean build
./gradlew allTests
```

### 4. Verify BOM Contents

Generate and inspect the BOM POM:

```bash
./gradlew :bom:generatePomFileForMavenPublication

# View the generated BOM
cat bom/build/publications/maven/pom-default.xml
```

### 5. Publish Everything

Publish all libraries and the BOM together:

```bash
./gradlew publishAllPublicationsToMavenCentral
```

## Version Tracking

### What's in Each BOM Version?

Since all libraries version together, tracking is simple:

| BOM Version | All Libraries Version | Notes |
|-------------|----------------------|-------|
| 1.0.0       | 1.0.0               | Initial release |
| 1.1.0       | 1.1.0               | Added feature X |
| 2.0.0       | 2.0.0               | Breaking changes |

### Changelog Example

Create `CHANGELOG.md` in the root:

```markdown
# Changelog

## [1.1.0] - 2026-01-20

### Added
- example-library: New feature X
- another-library: Support for Y

### Fixed  
- example-library: Bug fix Z

### Libraries Included
- example-library: 1.1.0
- another-library: 1.1.0
```

## Alternative Strategy: Independent Versions

If you want libraries to have independent versions, you can maintain the BOM manually:

### Option A: Manual BOM Management

```kotlin
// bom/build.gradle.kts
dependencies.constraints {
    api("com.compiledplatforms.kmp.library:example-library:1.0.0")
    api("com.compiledplatforms.kmp.library:another-library:2.3.0")
    api("com.compiledplatforms.kmp.library:third-library:1.5.0")
}
```

Then track which BOM version contains which library versions:

| BOM Version | example-library | another-library | third-library |
|-------------|----------------|-----------------|---------------|
| 1.0.0       | 1.0.0          | 2.3.0           | 1.5.0        |
| 1.1.0       | 1.0.0          | 2.4.0           | 1.6.0        |
| 2.0.0       | 2.0.0          | 3.0.0           | 2.0.0        |

### Option B: Version Properties

Use `gradle.properties` for individual library versions:

```properties
# gradle.properties
bomVersion=1.0.0
exampleLibraryVersion=1.0.0
anotherLibraryVersion=2.3.0
thirdLibraryVersion=1.5.0
```

## Ensuring Compatibility

### 1. Integration Tests

Create a separate test project that uses the BOM:

```
test-integration/
├── build.gradle.kts
└── src/test/kotlin/
    └── IntegrationTest.kt
```

```kotlin
// test-integration/build.gradle.kts
dependencies {
    testImplementation(platform(project(":bom")))
    testImplementation("com.compiledplatforms.kmp.library:example-library")
    testImplementation("com.compiledplatforms.kmp.library:another-library")
}
```

### 2. Compatibility Matrix

Document tested combinations in `COMPATIBILITY.md`:

```markdown
# Compatibility Matrix

## BOM 1.0.0

Tested and compatible with:
- Kotlin 2.2.20
- kotlinx.coroutines 1.10.1
- Android compileSdk 36

### Known Issues
- Not compatible with kotlinx.serialization < 1.8.0
```

### 3. Automated Testing

Add a CI job that tests the BOM:

```yaml
# .github/workflows/test-bom.yml
name: Test BOM
on: [push, pull_request]

jobs:
  test-bom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test BOM Integration
        run: |
          ./gradlew :bom:build
          ./gradlew build
```

## Best Practices

### ✅ DO

1. **Version everything together** (recommended for monorepos)
2. **Test before publishing** - run full test suite
3. **Document changes** - maintain CHANGELOG.md
4. **Use tags** - tag Git commits with release versions
5. **Semantic versioning** - follow semver for BOM versions

### ❌ DON'T

1. **Publish untested combinations** - always test the full BOM
2. **Skip the changelog** - users need to know what changed
3. **Break the BOM** - ensure backward compatibility when possible
4. **Forget dependencies** - verify transitive dependencies work together

## Quick Commands

```bash
# Check current version
grep "project-version" gradle/libs.versions.toml

# Bump version (patch)
sed -i '' 's/project-version = "1.0.0"/project-version = "1.0.1"/' gradle/libs.versions.toml

# Verify BOM contents
./gradlew :bom:generatePomFileForMavenPublication
cat bom/build/publications/maven/pom-default.xml

# Test everything
./gradlew clean build allTests

# Publish everything
./gradlew publishAllPublicationsToMavenCentral

# Create Git tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Summary

**Current Setup**: All libraries and the BOM share the same version from `gradle/libs.versions.toml`.

**To Release**: 
1. Update `project-version` in `gradle/libs.versions.toml`
2. Test everything
3. Publish everything together
4. Tag the release

**Compatibility**: Test the full monorepo together - the BOM version represents a tested, compatible set of libraries.
