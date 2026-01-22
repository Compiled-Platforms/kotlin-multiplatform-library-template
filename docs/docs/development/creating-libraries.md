# Creating Libraries

This guide covers creating new libraries in the monorepo.

## Using the Script

The easiest way to create a new library:

```bash
python3 scripts/create-library.py my-library-name
```

This automatically:

- Creates the library module structure
- Sets up build configuration
- Generates sample code and tests
- Creates a README

## Manual Creation

If you prefer to create a library manually:

### 1. Create Directory Structure

```bash
mkdir -p libraries/my-library/src/{commonMain,commonTest}/kotlin
mkdir -p libraries/my-library/src/{jvmMain,jvmTest}/kotlin
mkdir -p libraries/my-library/src/{androidMain,androidHostTest}/kotlin
mkdir -p libraries/my-library/src/{iosMain,iosTest}/kotlin
mkdir -p libraries/my-library/src/{linuxX64Main,linuxX64Test}/kotlin
```

### 2. Create build.gradle.kts

```kotlin title="libraries/my-library/build.gradle.kts"
plugins {
    id("convention.library")
}

group = "com.compiledplatforms.kmp.library"
version = "1.0.0"

description = "Description of my library"

kotlin {
    sourceSets {
        commonMain.dependencies {
            // Add dependencies here
        }
    }
}

mavenPublishing {
    coordinates(group.toString(), "my-library", version.toString())
    
    pom {
        name = "My Library"
        description = "Detailed description"
        inceptionYear = "2026"
        url = "https://github.com/compiledplatforms/kotlin-multiplatform-library-template/"
        
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
            url = "https://github.com/compiledplatforms/kotlin-multiplatform-library-template/"
            connection = "scm:git:git://github.com/compiledplatforms/kotlin-multiplatform-library-template.git"
            developerConnection = "scm:git:ssh://git@github.com/compiledplatforms/kotlin-multiplatform-library-template.git"
        }
    }
}
```

### 3. Add Source Code

Create your main source file with proper package structure:

```kotlin title="libraries/my-library/src/commonMain/kotlin/com/compiledplatforms/kmp/library/mylib/MyClass.kt"
package com.compiledplatforms.kmp.library.mylib

class MyClass {
    fun doSomething(): String {
        return "Hello from MyClass!"
    }
}
```

!!! warning "Package Structure"
    Ensure your files are in directories matching the package name to pass Detekt validation.

### 4. Add Tests

```kotlin title="libraries/my-library/src/commonTest/kotlin/com/compiledplatforms/kmp/library/mylib/MyClassTest.kt"
package com.compiledplatforms.kmp.library.mylib

import kotlin.test.Test
import kotlin.test.assertEquals

class MyClassTest {
    @Test
    fun testDoSomething() {
        val myClass = MyClass()
        assertEquals("Hello from MyClass!", myClass.doSomething())
    }
}
```

## Platform-Specific Code

Use expect/actual for platform-specific implementations:

### Common (Expect)

```kotlin title="commonMain"
expect class PlatformSpecific() {
    fun getName(): String
}
```

### JVM (Actual)

```kotlin title="jvmMain"
actual class PlatformSpecific {
    actual fun getName(): String = "JVM"
}
```

### Android (Actual)

```kotlin title="androidMain"
actual class PlatformSpecific {
    actual fun getName(): String = "Android"
}
```

## Adding Dependencies

### Common Dependencies

Add to commonMain in your library's `build.gradle.kts`:

```kotlin
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.10.1")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.8.0")
        }
    }
}
```

### Platform-Specific Dependencies

```kotlin
kotlin {
    sourceSets {
        androidMain.dependencies {
            implementation("androidx.core:core-ktx:1.12.0")
        }
        
        iosMain.dependencies {
            // iOS-specific dependencies
        }
    }
}
```

## Building and Testing

```bash
# Build your library
./gradlew :libraries:my-library:build

# Run tests
./gradlew :libraries:my-library:test

# Run Detekt
./gradlew :libraries:my-library:detekt

# Publish locally for testing
./gradlew :libraries:my-library:publishToMavenLocal
```

## Updating the BOM

After creating a library, add it to the BOM:

```kotlin title="bom/build.gradle.kts"
dependencies.constraints {
    api("com.compiledplatforms.kmp.library:example-library:1.0.0")
    api("com.compiledplatforms.kmp.library:my-library:1.0.0")  // Add this
}
```

## Next Steps

- [Publishing](publishing.md) - Publish your library to Maven Central
- [Configuration](../getting-started/configuration.md) - Advanced configuration options
