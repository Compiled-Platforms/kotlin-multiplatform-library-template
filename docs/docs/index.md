# Kotlin Multiplatform Library Template

Welcome to the documentation for the Kotlin Multiplatform Library Template. This template provides a production-ready monorepo structure for building and publishing multiple Kotlin Multiplatform libraries.

## Features

- **Monorepo Structure** - Manage multiple libraries in one repository
- **Auto-Discovery** - Libraries automatically detected from `libraries/` directory
- **Convention Plugins** - Shared Gradle configuration reduces boilerplate
- **Version Catalog** - Centralized dependency management
- **Bill of Materials (BOM)** - Simplified version management for consumers
- **Detekt Integration** - Static code analysis enforces quality standards
- **Maven Central Publishing** - Pre-configured for publishing
- **Sample Applications** - Full sample apps for each library
- **Cross-Platform** - JVM, Android, iOS, and Linux targets

## Quick Links

- [Installation Guide](getting-started/installation.md) - Set up the template
- [Quick Start](getting-started/quick-start.md) - Create your first library
- [Libraries Overview](libraries/index.md) - Browse available libraries
- [Development Guide](development/setup.md) - Contributing guidelines

## Getting Started

```bash
# Clone the template
git clone https://github.com/compiledplatforms/kotlin-multiplatform-library-template.git
cd kotlin-multiplatform-library-template

# Customize the template
python3 scripts/project-setup.py

# Build all libraries
./gradlew build

# Create a new library
python3 scripts/create-library.py my-awesome-library
```

## Architecture

This template uses a monorepo structure where each library is a separate Gradle module under the `libraries/` directory. All libraries share common configuration through convention plugins defined in `buildSrc/`.

```
kotlin-multiplatform-library-template/
├── libraries/              # All library modules
│   └── example-library/    # Example KMP library
├── bom/                    # Bill of Materials
├── samples/                # Sample applications
├── buildSrc/               # Convention plugins
├── config/                 # Detekt and other configs
└── docs/                   # Documentation
```

## Support

- [GitHub Issues](https://github.com/compiledplatforms/kotlin-multiplatform-library-template/issues)
- [Discussions](https://github.com/compiledplatforms/kotlin-multiplatform-library-template/discussions)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](about/license.md) file for details.
