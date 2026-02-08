# Development Setup

This guide covers setting up your development environment for contributing to the libraries.

## Requirements

- **Java 11+** - For Kotlin compilation
- **Android SDK** - For Android targets
- **Xcode** (macOS only) - For iOS targets
- **Python 3** - For helper scripts
- **Git** - Version control

## IDE Setup

### IntelliJ IDEA / Android Studio

1. **Open Project**
   - Open the root directory in IntelliJ IDEA or Android Studio
   - Wait for Gradle sync to complete

2. **Configure Python (Optional)**
   - Install "Python Community Edition" plugin
   - Go to `Settings` → `Project` → `Python Interpreter`
   - Add system interpreter (`/usr/bin/python3`)

3. **Code Style**
   - The project uses Detekt for code quality
   - Install the Detekt plugin for IDE integration
   - Code style is enforced on build

## Project Structure

```
kotlin-multiplatform-library-template/
├── buildSrc/                      # Convention plugins
│   └── src/main/kotlin/
│       └── convention.library.gradle.kts
├── libraries/                     # Library modules
│   └── example-library/
├── bom/                          # Bill of Materials
├── samples/                      # Sample applications
├── config/                       # Configuration files
│   └── detekt/detekt.yaml
├── docs/                         # Documentation
├── scripts/                      # Helper scripts
│   ├── project-setup.py
│   └── create-library.py
└── gradle/libs.versions.toml     # Version catalog
```

## Building the Project

```bash
# Build all libraries
./gradlew build

# Build specific library
./gradlew :libraries:example-library:build

# Run tests
./gradlew test

# Run code quality checks
./gradlew detekt
```

## Running Samples

```bash
# Run JVM sample
./gradlew :samples:example-library:jvm-cli:run

# List all tasks for a sample
./gradlew :samples:example-library:jvm-cli:tasks
```

## Code Quality

### Detekt

Detekt runs automatically during build:

```bash
# Run Detekt on all modules
./gradlew detekt

# Generate Detekt config
./gradlew detektGenerateConfig
```

### Testing

```bash
# Run all tests
./gradlew test

# Run tests for specific platform
./gradlew jvmTest
./gradlew testAndroid
```

## Gradle Tasks

Common tasks:

```bash
# Clean build
./gradlew clean

# Build without tests
./gradlew assemble

# Publish to Maven Local
./gradlew publishToMavenLocal

# Check for dependency updates
./gradlew dependencyUpdates
```

## Git Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests: `./gradlew build`
4. Commit: `git commit -am "Add my feature"`
5. Push: `git push origin feature/my-feature`
6. Create a Pull Request

## Next Steps

- [Creating Libraries](creating-libraries.md) - Learn how to add new libraries
- [Publishing](publishing.md) - Publish your libraries to Maven Central
