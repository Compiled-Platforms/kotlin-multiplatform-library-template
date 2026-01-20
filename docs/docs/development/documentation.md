# API Documentation with Dokka

This project uses [Dokka](https://kotlinlang.org/docs/dokka-introduction.html) to generate API documentation from KDoc comments in the source code.

## Overview

Dokka generates both:
- **Per-Library Documentation**: Each library has its own standalone API documentation
- **Multi-Module Documentation**: Aggregated documentation for all libraries (for GitHub Pages deployment)

## Generating Documentation

### For a Single Library

Generate documentation for a specific library:

```bash
./gradlew :libraries:example-library:dokkaGeneratePublicationHtml
```

Output location: `libraries/example-library/build/dokka/html/index.html`

### For All Libraries

Generate documentation for all libraries at once:

```bash
./gradlew dokkaGeneratePublicationHtml
```

This will generate documentation for each library in its respective `build/dokka/html/` directory.

## Viewing Documentation

After generation, open the HTML files in your browser:

```bash
# macOS
open libraries/example-library/build/dokka/html/index.html

# Linux
xdg-open libraries/example-library/build/dokka/html/index.html

# Windows
start libraries/example-library/build/dokka/html/index.html
```

## Writing KDoc Comments

Dokka uses [KDoc](https://kotlinlang.org/docs/kotlin-doc.html) - Kotlin's documentation format, similar to Javadoc.

### Basic Example

```kotlin
/**
 * Generates a Fibonacci sequence starting from custom initial values.
 *
 * This function creates an infinite sequence of Fibonacci numbers where
 * the first two elements can be customized.
 *
 * @return A [Sequence] of integers representing the Fibonacci sequence
 * @see FIRST_FIBONACCI for the default first element
 * @see SECOND_FIBONACCI for the default second element
 * @sample com.compiledplatforms.kmp.library.fibonacci.FibonacciSamples.basicUsage
 */
fun generateFibi(): Sequence<Int> = sequence {
    var a = firstElement
    yield(a)
    var b = secondElement
    yield(b)
    while (true) {
        val c = a + b
        yield(c)
        a = b
        b = c
    }
}
```

### KDoc Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `@param` | Documents a function parameter | `@param name The user's name` |
| `@return` | Documents the return value | `@return The calculated result` |
| `@throws` / `@exception` | Documents exceptions | `@throws IllegalArgumentException if value is negative` |
| `@see` | Links to related elements | `@see OtherClass` |
| `@sample` | Links to sample code | `@sample com.example.Samples.example` |
| `@since` | Version when added | `@since 1.1.0` |
| `@suppress` | Hides from documentation | `@suppress Internal API` |

### Cross-References

Link to other classes, functions, or properties:

```kotlin
/**
 * Processes data using [DataProcessor].
 * 
 * @see DataProcessor.process
 * @see [com.example.other.RelatedClass]
 */
```

### Code Blocks in KDoc

Include code examples in documentation:

```kotlin
/**
 * Calculates the sum of two numbers.
 * 
 * Example usage:
 * ```kotlin
 * val result = add(5, 3)
 * println(result) // Output: 8
 * ```
 *
 * @param a The first number
 * @param b The second number
 * @return The sum of [a] and [b]
 */
fun add(a: Int, b: Int): Int = a + b
```

## Configuration

Dokka is configured in the convention plugin at `build-logic/convention/src/main/kotlin/KmpLibraryConventionPlugin.kt`:

```kotlin
extensions.configure<org.jetbrains.dokka.gradle.DokkaExtension> {
    moduleName.set(project.name)
    
    dokkaSourceSets.configureEach {
        // Suppress obvious functions (toString, equals, hashCode, etc.)
        suppressObviousFunctions.set(true)
        
        // Link to source code on GitHub
        sourceLink {
            localDirectory.set(projectDir.resolve("src"))
            remoteUrl("https://github.com/your-org/your-repo/tree/main/${project.path.replace(":", "/")}/src")
            remoteLineSuffix.set("#L")
        }
    }
}
```

## GitHub Pages Deployment

To deploy documentation to GitHub Pages:

1. Generate documentation:
   ```bash
   ./gradlew dokkaGeneratePublicationHtml
   ```

2. Copy generated docs to a `gh-pages` branch or use GitHub Actions

3. Configure GitHub Pages to serve from the `gh-pages` branch

### Automated Deployment with GitHub Actions

Create `.github/workflows/docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
          
      - name: Generate Dokka docs
        run: ./gradlew dokkaGeneratePublicationHtml
        
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build/dokka/html
```

## Best Practices

### 1. Document Public API

Always document:
- Public classes and interfaces
- Public functions and properties
- Function parameters and return values
- Exceptions that can be thrown

### 2. Use Clear Descriptions

❌ **Bad:**
```kotlin
/** Gets the name */
fun getName(): String
```

✅ **Good:**
```kotlin
/** Returns the user's full name in "First Last" format */
fun getName(): String
```

### 3. Include Examples

Add code samples for complex functions:

```kotlin
/**
 * Filters a list of users by age range.
 *
 * Example:
 * ```kotlin
 * val adults = filterByAge(users, 18, 65)
 * ```
 *
 * @param users The list of users to filter
 * @param minAge Minimum age (inclusive)
 * @param maxAge Maximum age (inclusive)
 * @return Filtered list of users
 */
fun filterByAge(users: List<User>, minAge: Int, maxAge: Int): List<User>
```

### 4. Link Related Concepts

Use `@see` to help users discover related functionality:

```kotlin
/**
 * Encodes a string to Base64.
 *
 * @see decodeBase64 for the reverse operation
 * @see encodeHex for hexadecimal encoding
 */
fun encodeBase64(input: String): String
```

### 5. Document Platform-Specific Behavior

```kotlin
/**
 * Gets the current platform name.
 *
 * Platform-specific behavior:
 * - **JVM**: Returns "Java" with version
 * - **Android**: Returns "Android" with API level
 * - **iOS**: Returns "iOS" with version
 * - **Native**: Returns the target platform
 */
expect fun getPlatformName(): String
```

## Troubleshooting

### Documentation Not Generated

**Problem**: Dokka task completes but no files are generated

**Solution**: Check that your source files have valid KDoc comments and are in the correct source sets.

### Missing Links

**Problem**: Cross-references show as plain text instead of links

**Solution**: Use fully qualified names or ensure the referenced class is imported:
```kotlin
@see com.compiledplatforms.kmp.library.other.OtherClass
```

### Source Links Broken

**Problem**: "View Source" links don't work

**Solution**: Verify the `sourceLink` configuration matches your repository structure.

### Build Performance

**Problem**: Dokka generation is slow

**Solution**: 
- Use `--no-daemon` flag to avoid daemon conflicts
- Generate docs only when needed (not on every build)
- Consider excluding large source sets if not needed

## Resources

- [Dokka Documentation](https://kotlinlang.org/docs/dokka-introduction.html)
- [KDoc Syntax](https://kotlinlang.org/docs/kotlin-doc.html)
- [Dokka Gradle Plugin](https://kotlinlang.org/docs/dokka-gradle.html)
- [Markdown in KDoc](https://kotlinlang.org/docs/kotlin-doc.html#markdown-syntax)
