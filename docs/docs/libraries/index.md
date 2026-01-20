# Libraries Overview

This monorepo contains multiple Kotlin Multiplatform libraries. Each library is independently versioned and published.

## Available Libraries

### Example Library

A demonstration library showing the template structure and capabilities.

[View Documentation](../example-library/){ .md-button }

## Using the BOM

Simplify dependency management by using the Bill of Materials (BOM):

```kotlin title="build.gradle.kts"
dependencies {
    // Import the BOM
    implementation(platform("com.compiledplatforms.kmp.library:bom:1.0.0"))
    
    // Now you can use libraries without specifying versions
    implementation("com.compiledplatforms.kmp.library:example-library")
}
```

## Adding a New Library

Each library module:

- Lives in the `libraries/` directory
- Is automatically discovered by Gradle
- Shares common configuration through convention plugins
- Has its own version and release cycle
- Can have its own documentation

To create a new library:

```bash
python3 scripts/create-library.py library-name
```

## Library Structure

Each library follows this structure:

```
libraries/your-library/
├── src/
│   ├── commonMain/kotlin/          # Shared code
│   ├── commonTest/kotlin/          # Shared tests
│   ├── jvmMain/kotlin/             # JVM-specific code
│   ├── jvmTest/kotlin/             # JVM tests
│   ├── androidMain/kotlin/         # Android-specific code
│   ├── iosMain/kotlin/             # iOS-specific code
│   └── linuxX64Main/kotlin/        # Linux-specific code
├── docs/                           # Library-specific documentation
├── build.gradle.kts                # Build configuration
└── README.md                       # Library README
```

## Next Steps

- [Creating Libraries](../development/creating-libraries.md) - Learn how to create libraries
- [Publishing](../development/publishing.md) - Publish your libraries
