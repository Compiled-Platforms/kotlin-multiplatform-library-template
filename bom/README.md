# BOM (Bill of Materials)

This module publishes a Bill of Materials (BOM) that manages dependency versions for all libraries in this monorepo.

## What is a BOM?

A BOM is a special type of Maven artifact that declares a set of library versions. When users import a BOM, they can add dependencies without specifying versions - the BOM provides the version.

## Usage

Users of your libraries can import the BOM to simplify dependency management:

### Gradle Kotlin DSL

```kotlin
dependencies {
    // Import the BOM
    implementation(platform("com.compiledplatforms.kmp.library:bom:1.0.0"))
    
    // Add libraries without versions
    implementation("com.compiledplatforms.kmp.library:example-library")
    implementation("com.compiledplatforms.kmp.library:another-library")
}
```

### Gradle Groovy DSL

```groovy
dependencies {
    implementation platform('com.compiledplatforms.kmp.library:bom:1.0.0')
    implementation 'com.compiledplatforms.kmp.library:example-library'
    implementation 'com.compiledplatforms.kmp.library:another-library'
}
```

## Benefits

- **Version Consistency**: All libraries use versions tested together
- **Simplified Dependency Management**: Update one version (the BOM) instead of many
- **Guaranteed Compatibility**: Libraries are tested as a set

## Auto-inclusion

All libraries in the `libraries/` directory are automatically included in the BOM via the build script. No manual configuration needed!

## Publishing

Publish the BOM alongside your libraries:

```bash
./gradlew :bom:publishAllPublicationsToMavenCentral
```
