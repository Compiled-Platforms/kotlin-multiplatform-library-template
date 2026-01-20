# Quick Start

This guide will walk you through creating your first Kotlin Multiplatform library.

## Creating a New Library

Use the provided script to scaffold a new library:

```bash
python3 scripts/create-library.py my-awesome-library
```

This creates:

- Library module at `libraries/my-awesome-library/`
- Build configuration with convention plugin
- Source sets for all targets (common, JVM, Android, iOS, Linux)
- Sample code and tests
- README with usage examples

## Project Structure

```
libraries/my-awesome-library/
├── src/
│   ├── commonMain/kotlin/
│   ├── commonTest/kotlin/
│   ├── jvmMain/kotlin/
│   ├── androidMain/kotlin/
│   ├── iosMain/kotlin/
│   └── linuxX64Main/kotlin/
├── build.gradle.kts
└── README.md
```

## Writing Code

Edit the generated files in `src/commonMain/kotlin/`:

```kotlin title="libraries/my-awesome-library/src/commonMain/kotlin/com/example/MyClass.kt"
package com.example.myawesomelib

/**
 * A simple example class.
 */
class MyClass {
    fun greet(name: String): String {
        return "Hello, $name!"
    }
}
```

## Writing Tests

Add tests in `src/commonTest/kotlin/`:

```kotlin title="libraries/my-awesome-library/src/commonTest/kotlin/com/example/MyClassTest.kt"
package com.example.myawesomelib

import kotlin.test.Test
import kotlin.test.assertEquals

class MyClassTest {
    @Test
    fun testGreet() {
        val myClass = MyClass()
        assertEquals("Hello, World!", myClass.greet("World"))
    }
}
```

## Building Your Library

```bash
# Build the library
./gradlew :libraries:my-awesome-library:build

# Run tests
./gradlew :libraries:my-awesome-library:test

# Run code quality checks
./gradlew :libraries:my-awesome-library:detekt
```

## Publishing Locally

Test your library by publishing to Maven Local:

```bash
./gradlew :libraries:my-awesome-library:publishToMavenLocal
```

## Next Steps

- [Creating Libraries](../development/creating-libraries.md) - Advanced library development
- [Publishing](../development/publishing.md) - Publishing to Maven Central
