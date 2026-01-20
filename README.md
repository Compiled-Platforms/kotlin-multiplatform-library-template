# Kotlin Multiplatform Monorepo Template

A template for managing multiple Kotlin Multiplatform libraries in a single monorepo, with automated publishing to Maven Central.

## 🚀 Features

- **Monorepo Structure**: Manage multiple KMP libraries in one repository
- **Auto-Discovery**: Libraries are automatically detected from the `libraries/` directory
- **Convention Plugin**: Shared Gradle configuration to reduce boilerplate
- **Maven Central Publishing**: Pre-configured for publishing to Maven Central
- **Multiplatform Support**: JVM, Android, iOS, and Linux targets
- **CI/CD Ready**: GitHub Actions workflows for build and publish

## 📁 Project Structure

```
kotlin-multiplatform-library/
├── buildSrc/                          # Convention plugin for shared configuration
│   ├── build.gradle.kts
│   └── src/main/kotlin/
│       └── convention.library.gradle.kts   # KMP library + publishing setup
├── libraries/                         # All library modules go here
│   ├── example-library/              # Example library
│   │   ├── src/
│   │   │   ├── commonMain/kotlin/
│   │   │   ├── commonTest/kotlin/
│   │   │   ├── jvmMain/kotlin/
│   │   │   ├── androidMain/kotlin/
│   │   │   ├── iosMain/kotlin/
│   │   │   └── linuxX64Main/kotlin/
│   │   └── build.gradle.kts
│   └── README.md                      # Guide for adding new libraries
├── scripts/
│   └── create-library.sh              # Helper script to scaffold new libraries
├── .github/workflows/                 # CI/CD workflows
├── build.gradle.kts                   # Root build configuration
├── settings.gradle.kts                # Multi-project settings with auto-discovery
└── README.md
```

## 🎯 Quick Start

### Prerequisites

- Java 11 or higher
- Android SDK (for Android targets)
- Xcode (for iOS targets, macOS only)

### Clone and Build

```bash
git clone <your-repo-url>
cd kotlin-multiplatform-library
./gradlew build
```

### Adding a New Library

1. **Use the helper script** (recommended):

```bash
./scripts/create-library.sh my-new-library
```

2. **Or manually create**:

```bash
mkdir -p libraries/my-new-library/src/commonMain/kotlin
```

Create `libraries/my-new-library/build.gradle.kts`:

```kotlin
plugins {
    id("convention.library")
}

group = "io.github.yourusername"
version = "1.0.0"
description = "My new library"

mavenPublishing {
    coordinates(group.toString(), "my-new-library", version.toString())
    pom {
        name = "My New Library"
        description = "Description of your library"
        // ... other POM configuration
    }
}
```

3. **Sync Gradle** and start coding!

See [`libraries/README.md`](libraries/README.md) for detailed instructions.

## 🏗️ Convention Plugin

This monorepo uses a convention plugin to share common configuration across all libraries:

### `convention.library`
- Sets up Kotlin Multiplatform with common targets (JVM, Android, iOS, Linux)
- Configures Android library settings (minSdk 24, compileSdk 36)
- Sets up source sets and test dependencies
- Configures Maven Central publishing with signing

## 📚 Version Catalog

The monorepo uses Gradle's version catalog (`gradle/libs.versions.toml`) to centralize all dependency versions.

### Benefits
- **Single Source of Truth**: All versions defined in one place
- **Type-Safe**: IDE autocomplete for dependencies
- **Consistency**: Ensures all libraries use the same versions
- **Easy Updates**: Update a version once, applies everywhere

### Usage in Libraries

Add dependencies using the version catalog:

```kotlin
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
        }
    }
}
```

### Adding New Dependencies

Edit `gradle/libs.versions.toml`:

```toml
[versions]
ktor = "3.0.0"

[libraries]
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
```

Then use in any library:

```kotlin
implementation(libs.ktor.client.core)
```

### Pre-configured Dependencies

The catalog includes common KMP libraries:
- `kotlinx-coroutines-core`
- `kotlinx-serialization-json`
- `kotlinx-datetime`
- And more...

## 📋 BOM (Bill of Materials)

This monorepo publishes a BOM for simplified dependency management with guaranteed compatibility.

### For Library Users

Import the BOM to get tested, compatible library versions:

```kotlin
dependencies {
    // Import the BOM - specifies compatible versions
    implementation(platform("com.compiledplatforms.kmp.library:bom:1.0.0"))
    
    // Add libraries without version numbers
    implementation("com.compiledplatforms.kmp.library:example-library")
    implementation("com.compiledplatforms.kmp.library:another-library")
}
```

### Independent Versioning

- Each library has its own version (e.g., `example-library:1.5.0`, `another-library:2.3.0`)
- The BOM version (e.g., `1.0.0`) declares which library versions are tested together
- Users can override BOM versions if needed: `implementation("com.compiledplatforms.kmp.library:example-library:1.6.0")`

### For Monorepo Maintainers

See `bom/BOM_MANAGEMENT.md` for details on:
- Updating the BOM with new library versions
- Testing library combinations
- Version tracking and changelog maintenance

## 📦 Building and Testing

```bash
# Build all libraries
./gradlew build

# Build a specific library
./gradlew :libraries:example-library:build

# Run tests for all libraries
./gradlew test

# Run tests for a specific library
./gradlew :libraries:example-library:test
```

## 🎯 Sample Applications

The `samples/` directory contains full sample applications demonstrating library usage.

### Running Samples

```bash
# Run a sample application
./gradlew :samples:example-library-sample:run

# Build all samples
./gradlew :samples:build
```

### Creating New Samples

See [`samples/README.md`](samples/README.md) for detailed instructions on creating sample applications.

Samples use project dependencies to stay in sync with library changes and are automatically discovered.

## 🚢 Publishing

### Prerequisites

1. Create accounts on [Sonatype OSSRH](https://central.sonatype.org/)
2. Generate GPG keys for signing
3. Configure credentials in `~/.gradle/gradle.properties`:

```properties
mavenCentralUsername=your-username
mavenCentralPassword=your-password

signing.keyId=your-key-id
signing.password=your-key-password
signing.secretKeyRingFile=/path/to/secring.gpg
```

### Publish to Maven Central

```bash
# Publish all libraries
./gradlew publishAllPublicationsToMavenCentral

# Publish a specific library
./gradlew :libraries:example-library:publishAllPublicationsToMavenCentral
```

### GitHub Actions

The repository includes workflows for:
- **Build** (`.github/workflows/gradle.yml`): Runs on every push/PR
- **Publish** (`.github/workflows/publish.yml`): Publishes to Maven Central on release

Configure secrets in your GitHub repository:
- `OSSRH_USERNAME` - Maven Central username
- `OSSRH_PASSWORD` - Maven Central password
- `SIGNING_KEY_ID` - GPG key ID
- `SIGNING_PASSWORD` - GPG key password
- `SIGNING_SECRET_KEY_RING_FILE` - Base64 encoded GPG secret key ring

## 🎓 Supported Platforms

Each library supports the following platforms by default:
- **JVM**: Desktop applications and servers
- **Android**: Android applications (minSdk 24, compileSdk 36)
- **iOS**: iPhone and iPad (x64, arm64, simulatorArm64)
- **Linux**: Linux x64

You can customize the target platforms in your library's `build.gradle.kts`.

## 📚 Resources

- [Kotlin Multiplatform Documentation](https://kotlinlang.org/docs/multiplatform.html)
- [Publishing to Maven Central](https://www.jetbrains.com/help/kotlin-multiplatform-dev/multiplatform-publish-libraries.html)
- [Gradle Maven Publish Plugin](https://vanniktech.github.io/gradle-maven-publish-plugin/central/)
- [Central Portal Publishing Guide](https://central.sonatype.org/publish-ea/publish-ea-guide/)

## 📝 License

This template is provided as-is. Update the [LICENSE](LICENSE) file according to your needs.

## 🤝 Contributing

See [`libraries/README.md`](libraries/README.md) for guidelines on adding new libraries to this monorepo.
