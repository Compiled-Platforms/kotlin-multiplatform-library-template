# Installation

## Prerequisites

Before you begin, ensure you have the following installed:

- **Java 11 or higher** - Required for Gradle and Kotlin
- **Android SDK** - Required for Android targets
- **Xcode** - Required for iOS targets (macOS only)
- **Python 3** - Required for setup and library creation scripts

## Cloning the Template

```bash
git clone https://github.com/compiledplatforms/kotlin-multiplatform-library-template.git
cd kotlin-multiplatform-library-template
```

## Customizing the Template

Run the interactive setup script to customize the template with your own values:

```bash
python3 scripts/project-setup.py
```

The script will prompt you for:

- **Maven Group ID** - Your package identifier (e.g., `com.example.libraries`)
- **Project Name** - Your project name (e.g., `my-kmp-libraries`)
- **GitHub Organization** - Your GitHub username or organization
- **Developer Info** - Name and GitHub username for POM files

## Verifying Installation

Build the project to verify everything is set up correctly:

```bash
./gradlew build
```

If the build succeeds, you're ready to start developing!

## Next Steps

- [Quick Start Guide](quick-start.md) - Create your first library
- [Configuration](configuration.md) - Customize build settings
