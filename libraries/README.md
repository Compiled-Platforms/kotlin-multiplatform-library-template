# Libraries Directory

This directory contains all the Kotlin Multiplatform libraries in this monorepo.

## Structure

Each library is a separate Gradle module with its own:
- Source code (`src/`)
- Build configuration (`build.gradle.kts`)
- Tests
- Documentation

## Adding a New Library

To add a new library to the monorepo:

### 1. Create the Library Directory

```bash
mkdir -p libraries/my-new-library/src/{commonMain,commonTest}/kotlin
```

### 2. Create the Build Configuration

Create `libraries/my-new-library/build.gradle.kts`:

```kotlin
plugins {
    id("convention.library")
}

group = "io.github.kotlin"  // Update to your group
version = "1.0.0"

description = "Description of your library"

kotlin {
    sourceSets {
        commonMain.dependencies {
            // Add your dependencies here
        }
    }
}

mavenPublishing {
    coordinates(group.toString(), "my-new-library", version.toString())
    
    pom {
        name = "My New Library"
        description = "A detailed description of what this library does"
        inceptionYear = "2026"
        url = "https://github.com/your-org/your-repo/"
        
        licenses {
            license {
                name = "The Apache Software License, Version 2.0"
                url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
                distribution = "repo"
            }
        }
        
        developers {
            developer {
                id = "yourusername"
                name = "Your Name"
                url = "https://github.com/yourusername"
            }
        }
        
        scm {
            url = "https://github.com/your-org/your-repo/"
            connection = "scm:git:git://github.com/your-org/your-repo.git"
            developerConnection = "scm:git:ssh://git@github.com/your-org/your-repo.git"
        }
    }
}
```

### 3. Create Your Source Files

The convention plugin sets up the following source sets:
- `commonMain/kotlin/` - Common Kotlin code
- `commonTest/kotlin/` - Common tests
- `jvmMain/kotlin/` - JVM-specific code
- `jvmTest/kotlin/` - JVM-specific tests
- `androidMain/kotlin/` - Android-specific code
- `androidHostTest/kotlin/` - Android host tests
- `iosMain/kotlin/` - iOS-specific code
- `iosTest/kotlin/` - iOS-specific tests
- `linuxX64Main/kotlin/` - Linux-specific code
- `linuxX64Test/kotlin/` - Linux-specific tests

### 4. Sync Gradle

The library will be automatically discovered by `settings.gradle.kts`. Just sync your Gradle project:

```bash
./gradlew --refresh-dependencies
```

### 5. Verify the Library

Build and test your new library:

```bash
./gradlew :libraries:my-new-library:build
./gradlew :libraries:my-new-library:test
```

## Convention Plugin

The monorepo uses a convention plugin located in `buildSrc/` to share common configuration:

### `convention.library`
Sets up the Kotlin Multiplatform configuration with:
- **Target platforms**: JVM, Android, iOS (x64, arm64, simulatorArm64), Linux x64
- **Android SDK versions**: compile: 36, min: 24
- **JVM target**: Java 11
- **Common test dependencies**: kotlin-test
- **Maven publishing**: Pre-configured for Maven Central with signing

You can customize any of these settings in your library's `build.gradle.kts`.

## Publishing Configuration

To configure publishing, update your `gradle.properties` or `local.properties`:

```properties
# Maven Central credentials
mavenCentralUsername=your-sonatype-username
mavenCentralPassword=your-sonatype-password

# Signing configuration
signing.keyId=your-gpg-key-id
signing.password=your-gpg-password
signing.secretKeyRingFile=/path/to/secring.gpg
```

Then publish with:

```bash
./gradlew :libraries:my-new-library:publishAllPublicationsToMavenCentral
```

## Example Library

See `libraries/example-library/` for a complete example of a library in this monorepo.
