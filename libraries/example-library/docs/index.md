# Example Library

An example Kotlin Multiplatform library demonstrating the template structure and capabilities.

## Installation

=== "Kotlin DSL"

    ```kotlin
    dependencies {
        implementation("com.compiledplatforms.kmp.library:example-library:1.0.0")
    }
    ```

=== "Groovy DSL"

    ```groovy
    dependencies {
        implementation 'com.compiledplatforms.kmp.library:example-library:1.0.0'
    }
    ```

=== "With BOM"

    ```kotlin
    dependencies {
        // Import BOM
        implementation(platform("com.compiledplatforms.kmp.library:bom:1.0.0"))
        
        // No version needed
        implementation("com.compiledplatforms.kmp.library:example-library")
    }
    ```

## Features

- Platform-specific Fibonacci sequence generation
- Expect/actual declarations for multiplatform code
- Example of proper package structure
- Comprehensive tests for all platforms

## Usage

### Basic Usage

```kotlin
import com.compiledplatforms.kmp.library.fibonacci.generateFibi

fun main() {
    val fibonacci = generateFibi()
        .take(10)
        .toList()
    
    println(fibonacci) // [2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
}
```

### Platform-Specific Values

The library demonstrates expect/actual pattern with platform-specific starting values:

- **JVM**: Starts at 2, 3
- **Android**: Starts at 1, 2
- **iOS**: Starts at 3, 4
- **Linux**: Starts at 3, 5

## API Reference

### `generateFibi()`

Generates an infinite sequence of Fibonacci numbers.

**Returns:** `Sequence<Int>` - An infinite sequence of Fibonacci numbers

**Example:**

```kotlin
val first10 = generateFibi().take(10).toList()
```

### `firstElement` and `secondElement`

Platform-specific constants representing the starting values of the Fibonacci sequence.

**Type:** `Int` (expect/actual)

## Sample Application

A complete sample application is available at `samples/example-library-sample/`.

Run it with:

```bash
./gradlew :samples:example-library-sample:run
```

## Source Code

View the source code on [GitHub](https://github.com/compiledplatforms/kotlin-multiplatform-library-template/tree/develop/libraries/example-library).
